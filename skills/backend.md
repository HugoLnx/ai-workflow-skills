---
name: backend
description: >
  Backend development assistance for API design, database patterns, service architecture,
  validation, and error handling. Framework-aware (Express, FastAPI, Django, Rails, etc.).
  Triggers: "create endpoint", "API design", "service layer", "database query",
  "REST API", "backend pattern", "request handler", "data model".
---

## Purpose

Provide backend-specialized AI assistance covering API design, data modeling,
service architecture, input validation, error handling, and database access patterns.
Adapts to the detected framework and follows REST, GraphQL, or RPC conventions
as appropriate.

## Activation Criteria

- User asks to create API endpoints, routes, handlers, or controllers
- User mentions REST, GraphQL, gRPC, or WebSockets
- User asks about database queries, ORMs, migrations, or data models
- User asks about service layer, repositories, or business logic patterns
- User mentions "backend", "server", "API", "endpoint", "handler"

## Steps

1. **Detect framework and conventions**:
   - Node.js: Express, Fastify, NestJS, Hapi
   - Python: FastAPI, Django REST Framework, Flask, Litestar
   - Go: net/http, Gin, Echo, Chi
   - Ruby: Rails, Sinatra
   - Java/Kotlin: Spring Boot
   - C#: ASP.NET Core
   - Detect ORM: Prisma, TypeORM, SQLAlchemy, Django ORM, GORM, ActiveRecord
   - Detect API style: REST, GraphQL, tRPC, gRPC

2. **API endpoint design**:
   - Follow RESTful conventions: `GET /resources`, `POST /resources`, `PUT/PATCH /resources/:id`, `DELETE /resources/:id`
   - Use plural nouns for resource names, not verbs
   - Consistent HTTP status codes:
     - 200 OK (success with body), 201 Created, 204 No Content (success, no body)
     - 400 Bad Request (validation error), 401 Unauthorized, 403 Forbidden
     - 404 Not Found, 409 Conflict, 422 Unprocessable Entity
     - 500 Internal Server Error (never expose stack traces)
   - Version APIs: `/v1/resources` or `Accept: application/vnd.api+json;version=1`

3. **Input validation** (always validate at system boundary):
   - Validate all request body, query params, and path params
   - Use the project's validation library (Zod, Joi, Yup, Pydantic, class-validator)
   - Return 400 with a structured error body: `{ "errors": [{ "field": "email", "message": "Invalid format" }] }`
   - Never trust client input; strip unknown fields

4. **Error handling**:
   - Use a central error handler/middleware — don't handle errors inline in every route
   - Custom error classes with `statusCode`, `message`, `code` (machine-readable)
   - Log the full error server-side; return only safe error info to clients
   - Never return stack traces, SQL errors, or internal state to API clients
   - Handle async errors: use `try/catch` or a wrapper that catches promise rejections

5. **Database access patterns**:
   - Use the Repository pattern: business logic never calls the ORM directly
   - Transactions: wrap multi-step operations; handle rollback on failure
   - N+1 prevention: use eager loading / joins when fetching related data
   - Pagination: cursor-based for large datasets, offset-based for small/static sets
   - Soft deletes vs. hard deletes: decide per entity and be consistent
   - Index: foreign keys and any field used in WHERE clauses

6. **Service layer**:
   - Business logic in services, not in controllers/handlers
   - Controllers: validate input → call service → format response
   - Services: business rules, orchestration, no HTTP concerns
   - Repositories: data access only, no business rules

7. **Generate the code**:
   - Full handler/controller, service, repository (if applicable)
   - Type definitions for request/response bodies
   - Input validation schema
   - Error types if introducing new error cases

## Output Format

Complete, runnable handler/controller/service files with proper types, validation,
and error handling. Not snippets — full implementations.

## Scope

Backend source files: `src/**/*.{ts,py,go,rb,java,cs}` in server-side directories.

## Constraints

- Always validate user input — never trust it
- Never expose internal errors (stack traces, SQL details) to API clients
- Never hardcode credentials or configuration — use environment variables
- Use parameterized queries — never string-concatenate SQL
- Follow HTTP semantics correctly (correct status codes, idempotent GET/DELETE)

## Edge Cases

- **Authentication/Authorization**: Generate the endpoint but mark auth as a TODO
  with a clear placeholder (`// TODO: verify JWT token and check permissions`)
- **File uploads**: Use multipart form data; validate file type and size; store to
  object storage (S3/GCS), not local filesystem, in production
- **WebSockets or streaming**: Note that the response pattern differs; generate
  appropriate event handlers

## Cross-Ecosystem Notes

- **Cursor**: Activate with `@50-skill-backend` while working on server-side files
- **Aider**: `/add <handler-file> <service-file>`, reference the Backend section in CONVENTIONS.md
- **Codex**: Reference "Task: Backend Development" in AGENTS.md
