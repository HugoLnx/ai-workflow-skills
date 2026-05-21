# Game Feature Griller

Use this griller when the spec describes a **game feature** — a new mechanic, system, mode, or player-facing capability. Covers both design intent and player-experience concerns alongside implementation scope.

---

## Design Tree Branches

Walk these branches in order. Resolve dependencies before moving to dependent branches.

| # | Branch | Key question to ask | Depends on |
|---|---|---|---|
| 1 | Feature Concept & Player Value | What is the feature and what value does it add to the player experience? | — |
| 2 | Core Loop Integration | Where does this feature sit in the game loop? What player verb does it introduce or enhance? | 1 |
| 3 | Target Player Personas | Who is this feature primarily for — casual, core, or hardcore players? What is their typical session length and skill level? | 1 |
| 4 | Gameplay Mechanics & Rules | What are the explicit rules, player actions, win/fail/neutral states, and interactions? | 1, 2 |
| 5 | Scope & Non-Goals | What is the minimum shippable version? What is explicitly left for a future iteration? | 1, 4 |
| 6 | UX, Feedback & Onboarding | How does the player discover and learn this feature? What visual, audio, and haptic feedback communicates state changes? | 4, 5 |
| 7 | Progression & Balance | What is the difficulty curve, reward schedule, and impact on the game economy? | 4, 3 |
| 8 | Edge Cases & Failure States | What happens when the player exploits the feature, gets stuck, or reaches an unintended state? | 4, 6 |
| 9 | Accessibility | What colorblind modes, difficulty assists, or platform-specific accommodations are needed? | 6 |
| 10 | Platform & Input Considerations | How does this feature differ across mobile, PC, and console? Are there touch vs controller design differences? | 4, 6 |
| 11 | Monetization & Economy Impact | If applicable: does this feature interact with IAP, cosmetics, currency sinks, or sources? | 7 |
| 12 | Dependencies & Technical Risks | Which existing game systems does this feature touch? What are the main technical unknowns? | 4, 10 |
| 13 | Success Metrics | How will you know this feature is working well post-launch — retention delta, engagement rate, session length, funnel conversion? | 1, 7 |
| 14 | Phasing & Milestones | Is this delivered in phases? Are there release or live-ops deadlines? | 5, 12 |

---

## Domain-Specific Question Prompts

**Feature Concept & Player Value**
- "Describe this feature in one sentence. What is the player doing, and why is it fun or valuable?"

**Core Loop Integration**
- "Where in the game loop does this feature live — exploration, combat, progression, meta, social? What new or enhanced player verb does it introduce?"

**Target Player Personas**
- "Who is the primary audience for this feature? How often do they play, and how deep into the game are they when they encounter it?"

**Gameplay Mechanics & Rules**
- "Walk through the feature step by step from the player's perspective. What are the explicit rules? What are the win, fail, and neutral states?"

**Scope & Non-Goals**
- "What is the absolute minimum version you'd ship? What commonly requested variation are you deliberately leaving out of v1?"

**UX, Feedback & Onboarding**
- "How does the player discover this feature exists? What does the UI look like? What visual and audio feedback confirms each player action?"

**Progression & Balance**
- "How does difficulty scale? What are the reward types and schedule? Could this feature be exploited to break the economy or skip progression?"

**Edge Cases & Failure States**
- "What happens if the player spams the feature, leaves mid-session, or reaches an unintended state? What is the recovery path?"

**Accessibility**
- "Are there colorblind-impacting color choices? Is there a difficulty assist or skip option? Does anything break with larger text or reduced motion settings?"

**Platform & Input Considerations**
- "Does the feature need a different UI layout or interaction model on mobile vs PC vs console? Are there touch gesture or controller-only paths?"

**Monetization & Economy Impact**
- "Does this feature produce or consume any currency, resource, or item? Could it be used to farm or bypass a monetization gate?"

**Dependencies & Technical Risks**
- "Which existing systems (save, inventory, matchmaking, analytics) does this feature integrate with? What is the biggest technical unknown?"

**Success Metrics**
- "What metric would you check on day 7 to know this feature shipped successfully? What leading indicator tells you it's failing early?"

**Phasing & Milestones**
- "Is there a live-ops event or seasonal deadline tied to this? What does a Phase 1 vs Phase 2 cut look like?"

---

## Critic Focus Areas

When critiquing answers in this domain, pay special attention to:

- **Undefined win/fail states** — mechanics described with no clear outcome or resolution condition
- **Balance numbers without a testing basis** — tuning values stated as fact without playtesting or model validation
- **Missing discovery and onboarding path** — features that assume the player will find and understand them organically
- **Platform feature gaps** — experiences designed for one input model that degrade silently on others
- **Economy side-effects not modeled** — features that produce or consume resources without checking the downstream impact on progression pacing
- **Exploitable loops** — reward-bearing features with no rate limiting, cooldown, or cap analysis
- **Accessibility afterthought** — UI or feedback designed without considering colorblindness, motor accessibility, or cognitive load
- **Vague success metrics** — "players will enjoy it" or "engagement goes up" without a measurable definition
