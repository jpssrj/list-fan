# Critic Review Report (Stage 7)

**Target:** `docs/designs/neobrutalist_task_list.md` (`Lines 1–312`)  
**Mode:** `CRITIC`  
**Standards Evaluated:** `feature-spec-standard`

---

## Reviewer Status

| Reviewer | Status |
| :--- | :--- |
| `egm-design` | completed |
| `egm-structural` | completed |
| `egm-style` | completed |

---

## Severity Summary

* 🔴 **Blocker:** 2
* 🟡 **Major:** 4
* 🟢 **Nit:** 2
* **Total Findings:** 8

---

## Prioritized Findings (Blockers → Major → Nits)

### 1. Serverless Connection Pool Exhaustion on Neon PostgreSQL - Severity: Blocker
* **Reviewer Lens:** `egm-design`
* **Affected Scope:** Section 3.2, Lines 144–150 (`api/database.py`)
* **Discrepancy Description**: The SQLAlchemy engine is configured with a persistent connection pool (`pool_size=5, max_overflow=10`). In Vercel serverless environments, Python functions execute in ephemeral, horizontally scaled containers. If multiple concurrent requests trigger separate containers, each container instantiates its own `QueuePool`. Under moderate concurrency, this will quickly exceed Neon PostgreSQL's connection limits (default 100 connections on standard tiers) and cause connection exhaustion and query drops. Furthermore, frozen serverless containers leave idle connections open until dropped by the server, causing stale connection exceptions.
* **Rationale & Recommendation**: Serverless Python runtimes cannot safely manage persistent multi-process connection pools.
  1. Configure `create_engine` with `poolclass=NullPool` from `sqlalchemy.pool` to ensure database connections open and close per request without pooling across serverless executions:
     ```python
     from sqlalchemy.pool import NullPool
     engine = create_engine(DATABASE_URL, poolclass=NullPool, connect_args={"sslmode": "require"})
     ```
  2. Alternatively, explicitly specify the use of Neon's connection pooler URL (the pooled connection string ending in `-pooler` on port `5432` or `6543`) with `pool_recycle=300`. Update Section 3.2 to document this architectural constraint clearly.

---

### 2. Deprecated Legacy Vercel Configuration Schema - Severity: Blocker
* **Reviewer Lens:** `egm-structural`
* **Affected Scope:** Section 6, Lines 249–280 (`vercel.json`)
* **Discrepancy Description**: The specification uses Vercel's legacy configuration syntax (`"version": 2`, `"builds": [...]`, and `"routes": [...]`). Vercel has officially deprecated explicit `builds` and legacy `routes` definitions in favor of zero-config framework auto-detection and the modern `rewrites` / `headers` property schema. Deploying with deprecated `builds` declarations can result in build pipeline deprecation failures, build warnings, or incorrect route resolution between the static SPA build and the Python ASGI serverless runtime.
* **Rationale & Recommendation**: Modernize `vercel.json` to adhere to Vercel's current configuration specification using `rewrites`:
  ```json
  {
    "rewrites": [
      {
        "source": "/api/(.*)",
        "destination": "/api/index.py"
      },
      {
        "source": "/(.*)",
        "destination": "/index.html"
      }
    ]
  }
  ```
  This eliminates legacy build definitions while ensuring Vite client routes fallback cleanly to `index.html` and `/api/*` routes are consistently forwarded to the ASGI handler.

---

### 3. Serverless Cold-Start DDL Execution (`create_all`) - Severity: Major
* **Reviewer Lens:** `egm-design`
* **Affected Scope:** Section 2, Line 81 & Section 1 / Implementation Plan Reference
* **Discrepancy Description**: Section 2 describes `api/index.py` as executing table creation (`Base.metadata.create_all(bind=engine)`) during application lifespan startup. In a serverless environment, lifespan startup runs every time a cold container boots. Executing schema inspection and DDL checks across remote SSL connections to Neon PostgreSQL on every container initialization adds 200–500ms of unnecessary cold-start latency to user requests and risks catalog locks / race conditions when multiple serverless containers spin up concurrently during traffic spikes.
* **Rationale & Recommendation**: Decouple database schema creation from runtime request lifespans. Schema creation should be an out-of-band initialization step (e.g., via a standalone script `scripts/init_db.py` or Alembic migration command executed prior to deployment), leaving `api/index.py` strictly responsible for handling HTTP routing and queries.

---

### 4. Architectural Ambiguity in Task Filtering Responsibility - Severity: Major
* **Reviewer Lens:** `egm-structural`
* **Affected Scope:** Section 3.3, Line 166 vs Section 4.2, Lines 185–197
* **Discrepancy Description**: Section 3.3 specifies `GET /api/tasks` supporting a query parameter `filter=all|active|completed`. In contrast, Section 4.2 states that the Pinia store maintains all tasks locally and computes `filteredTasks` and `taskCounts` (counts of all, active, and completed tasks) using reactive client-side getters. If the client queries the filtered endpoint (`/api/tasks?filter=active`), the Pinia store cannot compute counts for all and completed tasks without making redundant server requests. If the frontend loads all tasks once and filters client-side, the backend query filter parameter is redundant and its usage scope is undefined.
* **Rationale & Recommendation**: Resolve the architectural boundary:
  - Clarify that `GET /api/tasks` defaults to returning all tasks for the SPA, enabling Pinia to maintain single-source-of-truth task counts and client-side filtering without network roundtrips.
  - State whether the `?filter=` query parameter is intended purely for external/headless REST consumers, or modify the endpoint contract to return aggregate metadata alongside filtered results (`{ tasks: Task[], counts: { all: int, active: int, completed: int } }`).

---

### 5. Missing PostgreSQL Timestamp Auto-Update Mechanism - Severity: Major
* **Reviewer Lens:** `egm-design`
* **Affected Scope:** Section 3.1, Lines 119–125 (`CREATE TABLE tasks`)
* **Discrepancy Description**: The SQL schema defines `updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL`. Unlike MySQL, PostgreSQL does not automatically update timestamp columns on `UPDATE` statements when defined with `DEFAULT CURRENT_TIMESTAMP`. Without an explicit database trigger or ORM-level `onupdate` specification, `updated_at` will remain frozen at the initial creation timestamp across all `PATCH` updates.
* **Rationale & Recommendation**: Explicitly specify the update strategy in Section 3.1:
  - In SQLAlchemy model definitions, declare `updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())`.
  - Or include the standard PostgreSQL trigger in the SQL schema:
    ```sql
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ language 'plpgsql';

    CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
    ```

---

### 6. Missing WAI-ARIA Semantics for Custom Neobrutalist Controls - Severity: Major
* **Reviewer Lens:** `egm-structural`
* **Affected Scope:** Section 4.1, Lines 178–184 & Goal G5 (Line 37)
* **Discrepancy Description**: Goal G5 establishes strict requirements for keyboard accessibility and tactile operation. However, Section 4.1 describes a custom brutalist square checkbox in `TaskItem.vue` and custom `BrutalButton` delete triggers without specifying accessibility semantics (`role="checkbox"`, `aria-checked`, `tabindex="0"`, or screen-reader accessible labels on delete buttons). Custom interactive elements lacking native form tags or ARIA labels are inaccessible to screen readers and violate accessible interactive standards.
* **Rationale & Recommendation**: Detail the accessibility requirements in Section 4.1:
  - Recommend implementing `TaskItem.vue`'s brutalist checkbox using a visually hidden native `<input type="checkbox">` styled with CSS peer selectors, preserving native keyboard toggling (`Space`), focus indication, and screen-reader accessibility out-of-the-box.
  - Require an `aria-label="Delete task: {task.title}"` attribute on the delete button primitive.

---

### 7. Contradiction in Tactile Interaction Physics Values - Severity: Nit
* **Reviewer Lens:** `egm-style`
* **Affected Scope:** Goal G2 (Line 34), Section 4.1 (Line 183) & Section 5 (Lines 235–247)
* **Discrepancy Description**: Goal G2 and Section 4.1 state that buttons use tactile press states of `translate(2px, 2px)`. However, the CSS specification in Section 5 defines `.brutal-interactive:hover` as `translate(2px, 2px)` and `.brutal-interactive:active` (press) as `translate(4px, 4px)` with `box-shadow: 0px 0px 0px 0px #121212`.
* **Rationale & Recommendation**: Harmonize the documentation terminology across Goals, Component Descriptions, and Section 5:
  - Hover state: `translate(2px, 2px)` with shadow `2px 2px 0px 0px #121212`.
  - Active/Press state: `translate(4px, 4px)` with shadow `0px 0px 0px 0px #121212`.

---

### 8. Undefined API Error Response Envelope in Endpoint Contracts - Severity: Nit
* **Reviewer Lens:** `egm-style`
* **Affected Scope:** Section 3.3, Lines 163–175
* **Discrepancy Description**: Section 3.3 lists `422 Unprocessable Entity` and `404 Not Found` response codes, but does not define the schema or payload structure for errors. The frontend Pinia store requires a predictable error envelope (e.g., FastAPI's standard `{ "detail": string | list }` structure) to reliably extract and render human-readable messages in optimistic UI rollback notifications.
* **Rationale & Recommendation**: Add a standard error response schema entry to Section 3.3 specifying FastAPI's `{ "detail": "string" }` format for 404s and validation error array format for 422s, ensuring seamless client-side error parsing.
