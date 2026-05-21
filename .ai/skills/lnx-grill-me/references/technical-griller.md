# Generalist Technical Architecture Griller

Use this griller when the spec describes a **technical solution** — system design, architectural approach, infrastructure change, or implementation strategy.

---

## Design Tree Branches

Walk these branches in order. Resolve dependencies before moving to dependent branches.

| # | Branch | Key question to ask | Depends on |
|---|---|---|---|
| 1 | Problem & Context | What technical problem is being solved and what is the current state? | — |
| 2 | Goals & Non-Goals | What must this solution achieve, and what is explicitly out of scope? | 1 |
| 3 | System Context | What are the system boundaries? What external systems interact with this one? | 1 |
| 4 | Proposed Approach | What is the high-level technical approach or architecture? | 1, 2, 3 |
| 5 | Alternatives Considered | What other approaches were evaluated and why were they rejected? | 4 |
| 6 | Data Model & Storage | What data is stored, how is it structured, and where does it live? | 4 |
| 7 | APIs & Interfaces | What interfaces are exposed or consumed? Contracts, protocols, versioning? | 4, 6 |
| 8 | Performance & Scalability | What are the load expectations and how does the design handle growth? | 4 |
| 9 | Security & Compliance | What are the auth, authz, encryption, and compliance requirements? | 3, 4, 7 |
| 10 | Error Handling & Resilience | How does the system behave under failure? Retries, fallbacks, circuit breakers? | 4, 8 |
| 11 | Testing Strategy | How will correctness be verified? Unit, integration, contract, load tests? | 4, 6, 7 |
| 12 | Deployment & Rollout | How is this deployed? Feature flags, migrations, rollback plan? | 4, 6 |
| 13 | Observability | What metrics, logs, traces, and alerts are needed? | 4, 10 |
| 14 | Open Risks & Questions | What is still unknown or unresolved? What could block delivery? | All |

---

## Domain-Specific Question Prompts

**Problem & Context**
- "What is broken or insufficient about the current system? What triggered this design effort?"

**Goals & Non-Goals**
- "What are the top 3 outcomes this solution must deliver? What will it deliberately not address?"

**System Context**
- "Draw the system boundary: what is inside this design and what is an external dependency?"

**Proposed Approach**
- "Describe the architecture in one paragraph. What are the key components and how do they interact?"

**Alternatives Considered**
- "What other approaches did you consider? Why did you rule them out?"

**Data Model & Storage**
- "What data does this system own? What is the primary storage technology and schema shape?"

**APIs & Interfaces**
- "What does the public interface look like? REST/gRPC/events? Who are the consumers?"

**Performance & Scalability**
- "What are the expected QPS, data volumes, and latency targets? What happens at 10× load?"

**Security & Compliance**
- "Who can access what? How is authentication handled? Are there data residency or audit requirements?"

**Error Handling & Resilience**
- "What happens when a downstream dependency is unavailable? How does the system recover?"

**Testing Strategy**
- "What is the minimum test suite needed to ship with confidence? What is hard to test and why?"

**Deployment & Rollout**
- "How is this shipped — big bang or incremental? Is there a migration, and can it be rolled back?"

**Observability**
- "What does 'healthy' look like in a dashboard? What alert would page someone at 2 AM?"

**Open Risks & Questions**
- "What do you not know yet that could significantly change this design?"

---

## Critic Focus Areas

When critiquing answers in this domain, pay special attention to:

- **Unmeasured performance** — claims like "fast enough" without concrete numbers
- **Missing failure modes** — descriptions of the happy path that skip partial failures, timeouts, or split-brain scenarios
- **Schema lock-in** — data model decisions that are hard to evolve without downtime
- **Implicit coupling** — components described as independent that share state or a deployment unit
- **Untested paths** — critical code paths (migrations, rollbacks, failovers) with no testing strategy
- **Observability gaps** — new failure modes introduced without corresponding alerts or dashboards
- **Security assumptions** — auth/authz described as "handled by the framework" without specifics
- **Rollout risk** — database migrations or interface changes with no backward compatibility plan
