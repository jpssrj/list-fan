# Stage 5 Report: Initial Zoom Out Architectural Review

**Target File:** [`docs/designs/neobrutalist_task_list.md`](file:///C:/Users/esjun/OneDrive/Documentos/GitHub/list-fan/docs/designs/neobrutalist_task_list.md)  
**Standard:** `zoom-out-standard`  
**Reviewer:** `egm-zoom-out` (Skeptical Architect)  

---

### Executive Summary

The proposal establishes a concise, well-bounded single-user task board that successfully rejects feature bloat (multi-user auth, nested tasks, complex metadata). The Vercel monorepo pairing Vue 3 with a serverless Python FastAPI backend backed by Neon PostgreSQL matches the product scope.

However, the architecture introduces several serverless-specific risks: runtime DDL execution on cold starts, connection pool exhaustion risks on Neon, deprecated Vercel configuration schemas, and unmitigated cold-start latency when creating tasks.

---

### Major Findings

#### Finding 1.1: Cold-Start DDL Schema Execution (`create_all` in Lifespan)
* **Severity:** **Major**
* **Affected Scope:** `docs/designs/neobrutalist_task_list.md#L373-L375` and `#L323`
* **Issue:** Executing `Base.metadata.create_all(bind=engine)` inside the FastAPI lifespan handler on application startup runs on **every container cold start**. Under traffic bursts, multiple concurrent lambdas executing `CREATE TABLE IF NOT EXISTS` concurrently cause catalog lock contention and unnecessary cold-start latency.
* **Recommendation:** Decouple DDL table creation from the runtime request path. Execute table creation via a one-off setup script or CLI command during initial database provisioning.

#### Finding 1.2: Serverless Connection Pooling Mismatch (Neon Exhaustion Risk)
* **Severity:** **Major**
* **Affected Scope:** `docs/designs/neobrutalist_task_list.md#L144-L150` and `#L361`
* **Issue:** The design configures SQLAlchemy with `pool_size=5` and `max_overflow=10` using `QueuePool`. Serverless functions scale out horizontally across independent container instances. Ten concurrent lambdas can attempt to maintain up to 150 pooled connections against Neon, exceeding free/standard serverless connection limits. Frozen instances may also leak idle connections.
* **Recommendation:** Use `NullPool` (open on demand, close immediately upon request completion) or direct requests to Neon’s pooled connection endpoint (port `6543` / `-pooler` connection string) with minimal local pooling (`pool_size=1`, `max_overflow=0`).

#### Finding 1.3: Deprecated Vercel 2.0 `builds` Specification
* **Severity:** **Major**
* **Affected Scope:** `docs/designs/neobrutalist_task_list.md#L253-L280` and `#L321`
* **Issue:** The proposed `vercel.json` uses legacy Vercel 2.0 configuration syntax (`"builds": [{"src": "api/index.py", "use": "@vercel/python"}, ...]`). Vercel has officially deprecated `builds` in favor of zero-configuration framework detection and modern `rewrites`.
* **Recommendation:** Modernize `vercel.json` by omitting deprecated `builds` and using native zero-config routing with modern `rewrites` mapping `/api/(.*)` to `/api/index.py`.

#### Finding 1.4: Compound Cold-Start Latency & Non-Optimistic Task Creation
* **Severity:** **Major**
* **Affected Scope:** `docs/designs/neobrutalist_task_list.md#L33` (Goal G1) and `#L195-L197`
* **Issue:** Goal G1 targets sub-100ms perceived response times. However, Neon serverless compute suspends after 5 minutes of inactivity. An idle task creation incurs a compound cold start (Vercel Python container startup + Neon compute wake-up and SSL handshake), taking 2–4 seconds. While toggles and deletes are handled optimistically, `POST /api/tasks` waits for `201 Created` before rendering.
* **Recommendation:** Acknowledge serverless wake-up latency in the risk section, and either include optimistic task addition with temporary local client IDs or ensure explicit UI loading/pending indicators during task submission.

---

### Minor / Nit Findings

#### Finding 2.1: YAGNI: Pinia State Management for a Flat 4-Component App
* **Severity:** **Nit**
* **Affected Scope:** `docs/designs/neobrutalist_task_list.md#L96-L97`, `#L185-L197`, and `#L340`
* **Issue:** The app is a single view with 4 flat components. Vue 3's native Reactivity API (`ref`, `reactive`, or a lightweight composable `useTasks`) handles optimistic state, filtering, and API calls with zero third-party dependencies.

#### Finding 2.2: Over-Decomposition of Backend Files for a Single Entity
* **Severity:** **Nit**
* **Affected Scope:** `docs/designs/neobrutalist_task_list.md#L78-L87` and `#L319-L329`
* **Issue:** Distributing 4 CRUD endpoints and a single entity across 7 backend files introduces indirection. Consolidating into 2–3 cohesive modules (`api/index.py`, `api/models.py`, `api/database.py`) reduces boilerplate.

#### Finding 2.3: Implementation Weeds in Design Document
* **Severity:** **Nit**
* **Affected Scope:** `docs/designs/neobrutalist_task_list.md#L134-L160`, `#L202-L247`, `#L317-L349`, and `#L354-L417`
* **Issue:** Embedding concrete Python snippets, CSS classes, and a 33-row file manifest pulls the document into low-level implementation details rather than architectural design decisions.

#### Finding 2.4: `psycopg2-binary` Serverless Runtime Compatibility
* **Severity:** **Nit**
* **Affected Scope:** `docs/designs/neobrutalist_task_list.md#L106` and `#L322`
* **Issue:** `psycopg2-binary` bundles pre-built C binaries that can exhibit glibc and dynamic library linking inconsistencies in certain Lambda / Vercel Python runtime images. Evaluating `psycopg` (v3) or pure-Python wheels simplifies container portability.
