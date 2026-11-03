# Stage 9: Implementation Readiness Review Report

**Target:** [`docs/designs/neobrutalist_task_list.md`](file:///C:/Users/esjun/OneDrive/Documentos/GitHub/list-fan/docs/designs/neobrutalist_task_list.md) (`Lines 313–418`)  
**Context:** Full design document [`docs/designs/neobrutalist_task_list.md`](file:///C:/Users/esjun/OneDrive/Documentos/GitHub/list-fan/docs/designs/neobrutalist_task_list.md), [`critic_report.md`](file:///C:/Users/esjun/OneDrive/Documentos/GitHub/list-fan/critic_report.md), and [`intermediate_zoom_out_report.md`](file:///C:/Users/esjun/OneDrive/Documentos/GitHub/list-fan/intermediate_zoom_out_report.md)  
**Mode:** `IMPLEMENTATION_READINESS`  
**Standards Evaluated:** `implementation-readiness-standard`

---

## Reviewer Status

| Reviewer | Status |
| :--- | :--- |
| `egm-implementation-readiness` | completed |
| `egm-codebase-details` | completed |
| `egm-style` | completed |

---

## Severity Summary

* 🔴 **Blocker:** 2
* 🟡 **Major:** 7
* 🟢 **Nit:** 4
* **Total Findings:** 13

---

## Prioritized Findings (Blockers → Major → Nits)

### 1. Persistence of Serverless Connection Pooling (`QueuePool`) in Implementation Plan - Severity: Blocker
* **Reviewer Lens:** `egm-implementation-readiness` / `egm-codebase-details`
* **Affected Scope:** Lines 325 (`api/database.py` in File Manifest) & Line 361 (Phase 2.1)
* **Discrepancy Description**: Line 361 instructs: *"Configure SQLAlchemy engine with `pool_size=5`, `max_overflow=10`, `pool_pre_ping=True`, and `connect_args={"sslmode": "require"}`."* In Vercel serverless environments, each ephemeral Lambda instance instantiates its own `QueuePool`. With `pool_size=5, max_overflow=10`, modest traffic concurrency spins up to 150 pooled connections against Neon, exceeding its standard 100 connection limit and dropping queries.
* **Recommendation**: Update Lines 325 and 361 to prescribe `poolclass=NullPool` from `sqlalchemy.pool` (or Neon's `-pooler` endpoint on port `6543`).

---

### 2. Persistence of Deprecated Vercel 2.0 `builds` Configuration Schema - Severity: Blocker
* **Reviewer Lens:** `egm-implementation-readiness` / `egm-codebase-details`
* **Affected Scope:** Line 321 (`vercel.json` in File Manifest) & Line 414 (Phase 5.2)
* **Discrepancy Description**: Line 321 defines `vercel.json` as mapping `@vercel/python` and `@vercel/static-build`. Modern Vercel deprecates explicit `builds` in favor of zero-configuration framework auto-detection and modern `rewrites`. Specifying legacy builds risks build failures or routing collision.
* **Recommendation**: Modernize `vercel.json` to use zero-config routing:
  ```json
  {
    "rewrites": [
      { "source": "/api/(.*)", "destination": "/api/index.py" },
      { "source": "/(.*)", "destination": "/index.html" }
    ]
  }
  ```

---

### 3. Serverless Cold-Start DDL Execution (`create_all`) in Lifespan & Missing Setup Script - Severity: Major
* **Reviewer Lens:** `egm-implementation-readiness` / `egm-codebase-details`
* **Affected Scope:** Line 323 (File Manifest) & Line 374 (Phase 2.5)
* **Discrepancy Description**: Running `Base.metadata.create_all` during lifespan startup executes on every container cold start, adding 200–500ms of latency and risking catalog locks during traffic spikes. The manifest lacks a standalone database provisioning script.
* **Recommendation**:
  1. Remove `create_all` from runtime lifespan startup in `api/index.py`.
  2. Add `scripts/init_db.py` to the manifest and execute it once out-of-band during initial setup.

---

### 4. Architectural Contradiction: Backend Query Filtering vs. Client-Side Store Filtering - Severity: Major
* **Reviewer Lens:** `egm-implementation-readiness` / `egm-style`
* **Affected Scope:** Line 329 & Line 369 (Phase 2.4) vs. Line 392–393 (Phase 4.2)
* **Discrepancy Description**: Line 369 specifies that `GET /api/tasks` supports query parameter `filter=all|active|completed`. Meanwhile, Phase 4.2 specifies that `taskStore.ts` computes `filteredTasks` and `taskCounts` reactively client-side. If the frontend filters locally, the backend `?filter=` parameter is redundant dead code.
* **Recommendation**: Eliminate `?filter=` from the backend specification. `GET /api/tasks` returns `List[TaskResponse]` ordered by `is_completed ASC, created_at DESC`, while Pinia derives filtered views in memory.

---

### 5. Native `fetch` Silent Rejection Gap in `taskApi.ts` Breaking Optimistic Rollback - Severity: Major
* **Reviewer Lens:** `egm-implementation-readiness` / `egm-codebase-details`
* **Affected Scope:** Line 339 (File Manifest) & Line 390 (Phase 4.1) vs. Lines 395–396 (Phase 4.2)
* **Discrepancy Description**: Native `fetch()` does not reject on HTTP 4xx or 5xx responses (such as `404` or `422`). Without checking `res.ok`, methods will treat error statuses as successful, and Pinia's optimistic rollback blocks will never execute.
* **Recommendation**: Explicitly specify the error-handling check in `taskApi.ts`:
  ```typescript
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(errorData.detail || `Request failed with status ${res.status}`);
  }
  ```

---

### 6. Missing Critical Tooling & Runtime Dependencies in Manifest - Severity: Major
* **Reviewer Lens:** `egm-codebase-details`
* **Affected Scope:** Lines 322 & 330 (File Manifest) and Lines 355–356 (Phase 1)
* **Discrepancy Description**: Frontend manifest omits `@vitejs/plugin-vue` and `typescript` (needed to build `.vue` SFCs). Backend manifest omits `python-dotenv` (needed to parse `.env` during local `uvicorn` development).
* **Recommendation**: Add `@vitejs/plugin-vue` and `typescript` to `package.json` devDependencies, and add `python-dotenv` to `requirements.txt`.

---

### 7. Re-emergence of "Creation Timestamp" on `TaskItem.vue` - Severity: Major
* **Reviewer Lens:** `egm-implementation-readiness` / `egm-style`
* **Affected Scope:** Line 400 (Phase 4.3) vs. Line 343, Section 4.1, and Non-Goal NG2
* **Discrepancy Description**: Line 400 instructs building `TaskItem.vue` with "creation timestamp", directly contradicting Line 343 and Non-Goal NG2.
* **Recommendation**: Delete `creation timestamp` from Line 400.

---

### 8. Pessimistic Task Creation Lacking UI In-Flight / Submitting State - Severity: Major
* **Reviewer Lens:** `egm-implementation-readiness` / `egm-codebase-details`
* **Affected Scope:** Line 342 & Line 399 (Phase 4.3) vs. Line 397 (Phase 4.2)
* **Discrepancy Description**: Task creation is pessimistic. During cold starts (2–4s), if the form and submit button are not disabled, users can submit duplicate tasks.
* **Recommendation**: Add `isSubmitting: boolean` state and disable the input and submit button during task creation with tactile pending feedback (`"ADDING..."`).

---

### 9. Missing Keyboard & Screen-Reader Semantics on Custom Controls - Severity: Major
* **Reviewer Lens:** `egm-implementation-readiness` / `egm-codebase-details`
* **Affected Scope:** Lines 341–343 & Lines 399–400 vs. Line 412 and Goal G5
* **Discrepancy Description**: Custom square checkboxes and delete triggers lack explicit ARIA and focus semantics for keyboard navigation and screen readers.
* **Recommendation**: Implement `TaskItem.vue`'s checkbox using a visually hidden native input (`<input type="checkbox" class="sr-only peer">`) with a styled label, and add `aria-label="Delete task: {task.title}"` to `BrutalButton`.

---

### 10. Pydantic v2 Whitespace Trimming & ConfigDict Precision - Severity: Nit
* **Recommendation**: Use `Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]` and `model_config = ConfigDict(from_attributes=True)`.

### 11. FastAPI 204 No Content Return Semantics - Severity: Nit
* **Recommendation**: Explicitly specify `return fastapi.Response(status_code=status.HTTP_204_NO_CONTENT)`.

### 12. Unspecified Google Font Family Name - Severity: Nit
* **Recommendation**: Explicitly specify `Space Grotesk` in `index.html` and `tailwind.config.js`.

### 13. Missing Error Notification Display in Application Assembly - Severity: Nit
* **Recommendation**: Add a brutalist error banner in `src/App.vue` conditionally rendered when `taskStore.errorMessage` is non-null.
