# System Requirements Document

Project: LegalGPT — Legal AI Chat-based Recommender System (India)
Date: 2025-10-05
Authors: Generated for repository

## 1. Purpose and Scope

This document describes the system requirements for LegalGPT, an open-source legal AI chat-based recommender system focused on Indian law. It captures functional and non-functional requirements, high-level architecture, data models, API contract, security and privacy constraints, deployment guidance, testing and acceptance criteria.

Intended readers: product owners, developers, testers, DevOps, and security reviewers.

## 2. Goals and Objectives

- Provide an interactive chat interface for users to ask legal questions relevant to Indian law.
- Provide accurate, sourced, and traceable answers using a Retrieval-Augmented Generation (RAG) approach.
- Persist user accounts, chat history, and feedback for auditing, recommendations, and analytics.
- Offer secure authentication and protect sensitive data.
- Be easy to deploy locally and in cloud environments.

## 3. Stakeholders

- End users (citizens seeking legal guidance)
- Legal experts and contributors (maintain knowledge base)
- Product owner / Maintainer
- DevOps / Platform engineers
- Security & Compliance reviewers

## 4. Assumptions and Constraints

- The system uses a cloud LLM provider (Gemini API or pluggable alternative). An API key is required via environment variables (e.g., `GEMINI_API_KEY`).
- SQLite is the default development DB (`backend/legal_ai_database.db`). The design allows migrating to PostgreSQL or other RDBMS.
- The system is intended for informational/research use and must include legal disclaimers; it is not a substitute for licensed legal advice.

## 5. Functional Requirements

5.1 User authentication and management
- FR-1: Users must be able to register with email (or username) + password.
- FR-2: Users must be able to login and receive a JWT access token.
- FR-3: Users can logout (client-side token discard). Server may support token revocation list later.
- FR-4: Passwords must be stored hashed (bcrypt) and protected against timing attacks.

5.2 Chat and sessions
- FR-5: Authenticated users can start chat sessions. Each session groups a sequence of messages.
- FR-6: The chat interface must allow free-text queries and suggested starter questions.
- FR-7: The system must persist user queries and responses with timestamps and session metadata.
- FR-8: Responses must include a list of sources (documents, statutes, precedents) used to produce the answer.

5.3 Retrieval and LLM integration
- FR-9: For each query, the system retrieves relevant documents from the knowledge store (in-memory, vector DB, or SQL-backed index).
- FR-10: The LLM should be invoked with a prompt that includes retrieved context and system instructions emphasizing accuracy, Indian legal jurisdiction, and citation of sources.

5.4 Feedback and analytics
- FR-11: Users should be able to upvote/downvote or flag responses; feedback is stored with query id.
- FR-12: System should collect anonymized analytics (queries per day, average response time) for monitoring and improvement.

5.5 Admin and maintenance (future)
- FR-13: Admin users will be able to upload and manage legal documents, re-index the knowledge base, and view system analytics.

## 6. Non-functional Requirements

6.1 Performance
- NFR-1: Median LLM response time (end-to-end) should be <= 5 seconds in typical dev/cloud conditions (network dependent).
- NFR-2: The backend API should handle at least 50 concurrent lightweight requests in a single small VM during early usage.

6.2 Scalability
- NFR-3: Design must allow swapping SQLite for PostgreSQL and plugging in a vector DB (e.g., FAISS, Milvus, Pinecone).

6.3 Availability and Reliability
- NFR-4: System should gracefully handle transient failures from LLM provider and surface meaningful errors to clients.

6.4 Security and Privacy
- NFR-5: All secrets (LLM API keys, JWT secrets) must be provided via environment variables and never committed.
- NFR-6: Passwords stored with bcrypt and salted (Passlib with bcrypt backend recommended).
- NFR-7: All API endpoints should require TLS in production. Local development may use HTTP with caution.
- NFR-8: Sensitive data (PII) should be stored encrypted at rest when using production datastore (e.g., full-disk/DB encryption or per-field encryption).

6.5 Compliance
- NFR-9: Provide opt-in/opt-out for data collection and a clear privacy policy; follow Indian data protection best practices.

6.6 Localization
- NFR-10: Support English as primary language; design for future multi-lingual support (Hindi, regional languages) in UI and model prompts.

## 7. High-level Architecture

Components
- Frontend (React): SPA providing login, chat UI, session list, and admin pages. Key files: `frontend/src/App.js`, components in `frontend/src/components/`.
- Backend (FastAPI): REST API that handles authentication, sessions, chat, persistence, and integration with LLM. Key files: `backend/main.py`, `backend/routes/`, `backend/services/gemini_rag_service.py`, `backend/auth/security.py`.
- Database: SQLite for development (`backend/legal_ai_database.db`). Models implemented via SQLAlchemy (users, chat_sessions, legal_queries, legal_documents, user_feedback, system_analytics).
- LLM Provider: Gemini (via genai or client library). Service wrapper: `backend/services/gemini_rag_service.py`.
- Optional Vector Store: A vector index for retrieval (not required for minimal local deployment).

Deployment
- Local dev: run backend from `backend/` (uvicorn) and frontend via `npm start` in `frontend/`.
- Production: containerized services with separate managed DB and proper secrets management (Vault, KMS), HTTPS, and autoscaling for the API layer.

## 8. Data Model (summary)

- users: id, email, password_hash, created_at
- chat_sessions: id, user_id, title, created_at, last_updated
- legal_queries: id, session_id, user_id, query_text, response_text, response_sources (JSON), created_at
- legal_documents: id, title, content, source_type, metadata
- user_feedback: id, query_id, user_id, rating, comment, created_at
- system_analytics: aggregated metrics or raw events

Note: See SQLAlchemy models in `backend/models` (or the project's model files) for field-level definitions.

## 9. API Endpoints (contract)

Authentication
- POST /auth/register — body: {email, password} → 201 user created
- POST /auth/login — body: {email, password} → 200 {access_token}
- GET /auth/me — header: Authorization: Bearer <token> → 200 user profile

Chat
- POST /chat/message — header: Authorization; body: {session_id?, message, metadata?} → 200 {response, sources, session_id}
- GET /chat/sessions — header: Authorization → 200 [{session_id, title, last_updated}]
- GET /chat/session/{id}/messages — header: Authorization → 200 [messages]

Feedback
- POST /feedback — header: Authorization; body: {query_id, rating, comment} → 200 OK

Admin (future)
- POST /admin/documents/upload — upload legal docs
- POST /admin/index/rebuild — trigger re-indexing

Errors
- Standardized errors with HTTP status codes and JSON: {code, message, details?}

## 10. Security Requirements

- SR-1: JWT signing key must be at least 256-bit (HMAC secret) or use asymmetric signing (RS256) in production.
- SR-2: Enforce password policies: min length 8, recommend passphrase; detect very long passwords and handle bcrypt 72-byte limit (truncate or use pre-hash with SHA256).
- SR-3: Rate-limit endpoints to mitigate abuse.
- SR-4: Log authentication events and suspicious activities.
- SR-5: Sanitize/escape any HTML returned or rendered to avoid XSS in the frontend.

## 11. Privacy / Legal Considerations

- Display clear disclaimer: informational/legal-education use only.
- Maintain a privacy policy explaining what data is stored, retention periods, and rights to delete data.
- Implement data retention controls and a user-requested data deletion flow.

## 12. Logging, Monitoring, and Observability

- Log at INFO for normal operations and ERROR for failures. Do not log secrets or full JWTs.
- Instrument timing for key paths: retrieval latency, LLM latency, DB write latency.
- Export metrics to a monitoring backend (Prometheus/Grafana) in production.

## 13. Testing Strategy

- Unit tests: business logic and utilities (auth, prompt construction, DB helpers).
- Integration tests: API endpoints (auth, chat flows) using test DB.
- E2E smoke test: register → login → send query → receive response → verify DB row.
- Load tests: simulate concurrent chat requests and measure latency.

## 14. Acceptance Criteria

- AC-1: User can register and login; password is hashed in DB.
- AC-2: Authenticated user can send a chat query and receive an answer with at least one source.
- AC-3: Chat sessions and queries are persisted and visible in the session list.
- AC-4: Feedback submission stores an entry in `user_feedback`.
- AC-5: System runs locally using provided instructions and environment variables.

## 15. Risks and Mitigations

- RISK: LLM hallucinations or incorrect legal advice.
  - Mitigation: emphasize citations, retrieve authoritative documents, include human-in-the-loop and clear disclaimers.
- RISK: Sensitive PII exposure in logs or model prompts.
  - Mitigation: scrub or redact PII before sending to the LLM; avoid logging PII.
- RISK: API key leakage.
  - Mitigation: environment variable management and secret storage, do not commit `.env`.

## 16. Operational Runbook (quick)

Local dev steps:

1. Backend

  - Ensure Python 3.10+ (project uses Pydantic v2 and FastAPI). Activate virtualenv.
  - Install dependencies (from backend/requirements.txt):

    pip install -r backend/requirements.txt

  - Create `.env` in `backend/` with at minimum:

    GEMINI_API_KEY="<your_key>"
    JWT_SECRET_KEY="<random-secret>"

  - Start server from `backend/`:

    uvicorn main:app --reload --host 127.0.0.1 --port 8000

2. Frontend

  - From `frontend/` install deps and run dev server:

    npm install
    npm start

  - Visit http://localhost:3000 (or the port shown)

3. Smoke test

  - Register, login, submit a question, verify response and that a DB record was created in `backend/legal_ai_database.db`.

## 17. Appendix

- Useful file locations in the repo:
  - Backend entrypoint: `backend/main.py`
  - Auth helpers: `backend/auth/security.py`
  - Gemini wrapper: `backend/services/gemini_rag_service.py`
  - Chat routes: `backend/routes/chat.py`
  - Frontend main file: `frontend/src/App.js`
  - Database (dev): `backend/legal_ai_database.db`

- Glossary
  - RAG — Retrieval Augmented Generation
  - LLM — Large Language Model
  - JWT — JSON Web Token

## 18. Next Steps / Roadmap

- Add a vector index (FAISS/Milvus) and robust retriever.
- Add role-based admin UI and document management.
- Add CI that runs unit/integration tests and lints before merging.
- Add E2E tests and production deployment manifests (Helm, Terraform).

---

If you'd like, I can: merge this into your README, create a condensed one-page requirements summary, or generate user stories and JIRA-style acceptance tickets from these requirements. Tell me what you'd like next.
