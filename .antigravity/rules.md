# JobInsight AI - Coding Rules & Architecture Guidelines

## 1. Clean Architecture & DDD
*   **Domain**: Pure Python/TypeScript. Zero framework/library dependencies (No SQLAlchemy, Pydantic, React, Next). Contains Entities, Value Objects, Aggregates, and Domain Events.
*   **Application**: Orchestrates Domain. Uses Input/Output DTOs only. Defines Interfaces/Protocols for database, vector search, and NLP operations.
*   **Adapters**: FastAPI controllers/routers, Pydantic schemas, Next.js page components, API clients.
*   **Infrastructure**: Concrete implementations (SQLAlchemy, Qdrant client, spaCy model loading, external APIs).
*   **Dependencies**: Rule of flow: Adapters/Infrastructure -> Application -> Domain. Domain must never depend on anything.

## 2. SOLID Principles
*   **SRP (Single Responsibility)**: One class/function = one reason to change. Separate CV parsing (NLP) from storage (Postgres/Qdrant).
*   **OCP (Open-Closed)**: Extend behavior using inheritance or protocols; do not modify tested business logic.
*   **LSP (Liskov Substitution)**: Subclasses or implementations must replace their protocols/parents without breaking behavior.
*   **ISP (Interface Segregation)**: Small, focused protocols (e.g., `JobReader`, `JobWriter`) instead of monolith interfaces.
*   **DIP (Dependency Inversion)**: Always depend on abstractions (Python Protocols / TS Interfaces), not concrete classes. Inject via FastAPI `Depends`.

## 3. FastAPI & PostgreSQL
*   **Async/Sync Boundary**: Use `async/await` for I/O operations (DB, Qdrant, network). Use sync/background tasks for CPU-bound tasks (NLP parsing, ML inference).
*   **FastAPI**: Mandatory Pydantic v2 schemas for all requests/responses. Use dependency injection (`Depends`) for DB sessions and Services.
*   **PostgreSQL**: SQLAlchemy 2.0 syntax. Enforce async session lifecycle. Define database indexes on foreign keys and filter fields.
*   **Migrations**: Alembic only. Direct DB schema changes are strictly prohibited.

## 4. Qdrant & Data Science / NLP
*   **Qdrant**: Define explicit vector dimensions & distance metrics. Use payload indexing on filtering keys (salary, contract, location) for hybrid search. Always perform filtering in Qdrant, never in-memory.
*   **Pandas**: No loops (`iterrows`). Use vectorized operations (`.apply()`, vector math). Cast types early to minimize memory footprint.
*   **spaCy**: Load NLP pipeline as a Singleton. Disable unused pipeline components (`parser`, `tagger`, `lemmatizer`) dynamically during bulk inference to optimize memory/speed.
*   **Models**: Separate ML training from inference. Keep models/estimators serialized (`joblib`/`safetensors`), versioned, and loaded on app startup.

## 5. Next.js & Tailwind CSS
*   **Next.js**: React Server Components (RSC) by default for data fetching. Use `'use client'` only for interactive UI/state.
*   **TypeScript**: `strict: true`. No `any` type allowed. Always declare API response types.
*   **Tailwind**: Use utility classes exclusively. Adhere to custom CSS variables of `shadcn/ui` theme system for consistency & dark/light modes.
