# Neobrutalist Task List (FastAPI + Vue 3 + Tailwind CSS on Vercel with Neon PostgreSQL)

* **Author:** esjun
* **Date:** 2026-11-03

## Overview

This project provides a single-user task management application built with a Python backend (FastAPI) and a Vue 3 frontend styled with a neobrutalist aesthetic via Tailwind CSS, deployed to Vercel. The backend utilizes external serverless persistence via Neon PostgreSQL to prevent data loss in Vercel's ephemeral runtime. The application supports three primary operations: adding tasks, toggling completion status, and deleting tasks. The frontend uses a direct, pragmatic component architecture (avoiding over-engineered Atomic Design nesting) while retaining high-contrast neobrutalist visual tokens.

## Analysis

Key architectural decisions and technical trade-offs resolved during brainstorming:

1. **Serverless Persistence (Neon PostgreSQL):**
   * Vercel's serverless environment discards local filesystem changes between executions, making local SQLite files non-viable.
   * Neon PostgreSQL provides a serverless relational database accessed via connection pooling over standard PostgreSQL protocols.
   * The backend connects to Neon via SQLAlchemy with `psycopg2-binary` or `asyncpg`, managed through an environment variable `DATABASE_URL`.
   * Tables are initialized on first startup using `Base.metadata.create_all(bind=engine)` inside the FastAPI lifespan context.

2. **Direct Component Architecture:**
   * Full Atomic Design (Atoms, Molecules, Organisms, Templates, Pages) has been eliminated to match the simple 3-action scope.
   * Component breakdown is kept flat and maintainable:
     * `src/components/TaskInput.vue`: Handles text entry, trimming, validation, and submission on `Enter`.
     * `src/components/TaskItem.vue`: Renders the brutalist checkbox, strike-through styling on completion, and the delete button.
     * `src/components/TaskFilter.vue`: Filter pill selector for `All`, `Active`, and `Completed`.
     * `src/components/BrutalButton.vue`: Reusable tactile button primitive with hard offset shadows.

3. **Neobrutalism Design System Tokens:**
   * Palette: Warm parchment canvas (`#FFFDF5`), card background (`#FFFFFF`), solid border/shadow dark (`#121212`), primary yellow (`#FFE600`), completed mint (`#00F0A8`), danger coral (`#FF5C5C`).
   * Borders: `border-3 border-black` on all container cards, inputs, and buttons.
   * Shadows: Hard unblurred box-shadows `4px 4px 0px 0px #121212`.
   * Tactile Physics: Hover states translate by `2px 2px` (reducing shadow to `2px 2px 0 0 #121212`), active/pressed states translate by `4px 4px` (shadow `0px 0px 0 0`).

4. **Vercel Monorepo Deployment Configuration:**
   * Root directory hosts both Vite and the Python serverless function.
   * `api/index.py`: Exposes the FastAPI application instance for Vercel's `@vercel/python` builder.
   * `vercel.json`: Directs `/api/(.*)` requests to `api/index.py` and routes all other requests to the static frontend build output (`dist/`).

## Goals vs. Non-Goals

* **In-Scope Goals:**
  * Persistent storage of tasks using Neon PostgreSQL.
  * FastAPI REST API (`/api/tasks`) implementing create, read with filter, update completion, and delete.
  * Direct, single-tier Vue 3 Single File Components using Composition API (`<script setup lang="ts">`).
  * Custom Tailwind configuration providing neobrutalist borders, drop shadows, and color tokens.
  * Optimistic UI updates with rollback in Pinia for toggle and delete actions.
  * Production deployment configuration for Vercel via `vercel.json`.

* **Out-of-Scope Non-Goals:**
  * Local file-based SQLite database.
  * Deep 5-tier Atomic Design directory scaffolding.
  * User authentication, OAuth, multi-tenancy, or user accounts.
  * Complex task properties (tags, priority levels, subtasks, deadlines).
  * WebSockets or background celery workers.

## Alternatives Weighed

* **Local SQLite vs. Neon PostgreSQL:**
  * *Rejected:* Local SQLite loses all data on Vercel cold restarts and cannot handle serverless scaling.
  * *Chosen:* Neon PostgreSQL provides persistent cloud storage with connection pooling suitable for Vercel functions.

* **MongoDB vs. PostgreSQL:**
  * *Rejected:* MongoDB introduces document validation and an additional query paradigm for a strictly relational single-table entity.
  * *Chosen:* PostgreSQL (via Neon) provides standard SQL schema enforcement, ACID guarantees, and direct SQLAlchemy integration.

* **Atomic Design vs. Direct Single-File Components:**
  * *Rejected:* Multi-tier Atomic Design adds directory overhead for a 3-function application.
  * *Chosen:* Direct component structure focusing only on essential reusable elements.

## Key Decisions & Staging for Next Steps

1. **Entity Schema (`Task`):**
   * `id`: `INTEGER` / `number` (Primary Key, autoincrement)
   * `title`: `VARCHAR(255)` / `string` (Not null, trimmed)
   * `is_completed`: `BOOLEAN` / `boolean` (Default: `false`, indexed)
   * `created_at`: `DATETIME` / `string` (ISO 8601 UTC)
   * `updated_at`: `DATETIME` / `string` (ISO 8601 UTC)

2. **Environment Configuration:**
   * Backend requires `DATABASE_URL` (Neon PostgreSQL connection string with `sslmode=require`).

3. **Staging for `/egm-draft`:**
   * Stage 1: Configure `vercel.json` routing, FastAPI serverless entry point (`api/index.py`), and Neon SQLAlchemy connection.
   * Stage 2: Implement `/api/tasks` REST endpoints with Pydantic schemas and database models.
   * Stage 3: Setup Vite + Vue 3 + Tailwind with neobrutalism tokens (`border-3`, `shadow-brutal`).
   * Stage 4: Build direct components (`TaskInput.vue`, `TaskItem.vue`, `TaskFilter.vue`, `BrutalButton.vue`) and wire to Pinia store.
   * Stage 5: End-to-end verification and Vercel deployment readiness check.
