# Generalist Feature Griller

Use this griller when the spec describes a **user-facing business feature** — a new capability, workflow, or product change.

---

## Design Tree Branches

Walk these branches in order. Each branch maps to one or more questions. Resolve dependencies (e.g. users before acceptance criteria) before moving to dependent branches.

| # | Branch | Key question to ask | Depends on |
|---|---|---|---|
| 1 | Problem | What specific problem or pain point does this feature solve? | — |
| 2 | Users & Personas | Who will use this feature, and what is their context? | 1 |
| 3 | Proposed Solution | What is the high-level description of the feature? | 1, 2 |
| 4 | Scope & Non-Goals | What is explicitly in and out of scope for this iteration? | 3 |
| 5 | Acceptance Criteria | What conditions must be true for this feature to be considered done? | 3, 4 |
| 6 | UX & Interactions | How does the user interact with the feature? Key flows and states? | 3, 5 |
| 7 | Edge Cases & Error States | What happens when things go wrong or inputs are unexpected? | 6 |
| 8 | Dependencies & Integrations | What systems, APIs, or teams does this feature depend on? | 3 |
| 9 | Constraints | What technical, legal, or business constraints apply? | 3, 8 |
| 10 | Success Metrics | How will success be measured after launch? | 1, 5 |
| 11 | Phasing & Timeline | Is this delivered in phases? Are there deadlines? | 4, 8 |

---

## Domain-Specific Question Prompts

Use these as the basis for your questions. Adapt to the specific context provided by the user.

**Problem**
- "What user pain or business problem is this feature solving? How is it handled today?"

**Users & Personas**
- "Who are the primary users? Are there secondary users or admin roles involved?"

**Proposed Solution**
- "Describe the feature in one or two sentences as if explaining it to a new team member."

**Scope & Non-Goals**
- "What is the minimum version you'd ship? What are you deliberately leaving out of this iteration?"

**Acceptance Criteria**
- "What does 'done' look like for this feature? List the top 3–5 conditions that must be true."

**UX & Interactions**
- "Walk me through the main user flow step by step. What does the user see, tap, or enter?"

**Edge Cases & Error States**
- "What happens if the user does X incorrectly? What are the failure modes?"

**Dependencies & Integrations**
- "Which other systems, APIs, or teams must be involved to build or run this feature?"

**Constraints**
- "Are there performance, compliance, accessibility, or platform constraints we must respect?"

**Success Metrics**
- "How will you know this feature is working well 30 days after launch?"

**Phasing & Timeline**
- "Does this need to ship in phases? Is there a hard deadline driven by a release or business event?"

---

## Critic Focus Areas

When critiquing answers in this domain, pay special attention to:

- **Unmeasured success** — acceptance criteria that can't be objectively verified
- **Missing error states** — happy-path-only descriptions that skip failure handling
- **Scope creep risk** — features described so broadly that any bug could be called out-of-scope
- **Undefined personas** — "users" without specifics about technical ability, frequency, or permissions
- **Implicit dependencies** — assumptions about existing infrastructure or team ownership
- **Regulatory blind spots** — data privacy, accessibility (WCAG), or compliance implications not mentioned
