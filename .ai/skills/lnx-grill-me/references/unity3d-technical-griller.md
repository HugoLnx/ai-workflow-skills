# Unity 3D Technical Architecture Griller

Use this griller when the spec describes a **Unity 3D technical solution** — a system, feature implementation, architectural pattern, or infrastructure concern within a Unity project.

---

## Design Tree Branches

Walk these branches in order. Resolve dependencies before moving to dependent branches.

| # | Branch | Key question to ask | Depends on |
|---|---|---|---|
| 1 | Problem & Context | What technical problem is being solved and what is the current state in the Unity project? | — |
| 2 | Goals & Non-Goals | What must this solution achieve, and what is explicitly out of scope? | 1 |
| 3 | Unity Architecture Pattern | What is the overall structural approach — MonoBehaviour-centric, ScriptableObject-driven, ECS/DOTS, manager singletons, or something else? | 1, 2 |
| 4 | Component & Communication Design | How do components share state and communicate — UnityEvents, C# events, ScriptableObject channels, direct references, or message bus? | 3 |
| 5 | Rendering Pipeline | Which pipeline is in use (URP / HDRP / Built-in)? What shaders, materials, and post-processing are involved? | 3 |
| 6 | Asset Management | How are assets loaded and unloaded — direct references, Resources, Addressables, or AssetBundles? What is the memory budget? | 3 |
| 7 | Performance & Optimization | What are the target frame rate and platform specs? Where are the expected draw call, GC, and CPU/GPU bottlenecks? | 3, 5, 6 |
| 8 | Physics & Collision | Which physics system is used (PhysX / custom)? What layers, rigidbodies, triggers, and FixedUpdate budget are involved? | 3 |
| 9 | Input System | Is the new Input System or legacy Input Manager in use? Which platforms must be supported? Is rebinding required? | 3 |
| 10 | Data Persistence | How is game state saved and loaded — PlayerPrefs, JSON files, binary, cloud save? What is the save/load lifecycle? | 3 |
| 11 | Testing Strategy | What is covered by Unity Test Framework — edit mode vs play mode tests? Is there CI running tests headlessly? | 3, 4 |
| 12 | Build & Deployment | What target platforms? IL2CPP or Mono? How is the build pipeline automated, and what is the rollback strategy? | 3, 6 |
| 13 | Open Risks & Questions | What is still unknown or unresolved? What could block delivery or require a redesign? | All |

---

## Domain-Specific Question Prompts

**Problem & Context**
- "What is currently broken or insufficient in the Unity project? What triggered this design — a performance issue, a new feature requirement, a scaling problem?"

**Goals & Non-Goals**
- "What are the top 3 outcomes this solution must deliver? What will it deliberately not address?"

**Unity Architecture Pattern**
- "Is the design MonoBehaviour-heavy, ScriptableObject-driven, or using DOTS/ECS? Are there existing manager or service locator patterns in the project to follow?"

**Component & Communication Design**
- "How will components talk to each other — events, direct `GetComponent` references, ScriptableObject channels, or something else? How are dependencies injected?"

**Rendering Pipeline**
- "Which render pipeline is this project on? Are there custom shaders or render features involved? What post-processing passes matter here?"

**Asset Management**
- "Are assets loaded via Addressables, Resources, or hard references? What is the peak memory budget, and how are assets released?"

**Performance & Optimization**
- "What is the target FPS and worst-case hardware? Where do you expect the hotspots — draw calls, GC allocations, physics, or AI?"

**Physics & Collision**
- "What physics layers and collision matrices are involved? Is there a FixedUpdate budget concern? Are any custom collision queries (OverlapSphere, Raycast) performance-sensitive?"

**Input System**
- "Is the project on the new Input System package? What platforms and input devices must work at launch? Is per-player or rebindable input needed?"

**Data Persistence**
- "What game state must persist between sessions? Where is save data stored — device-local, iCloud/Google Play, or a backend? What is the migration strategy for save format changes?"

**Testing Strategy**
- "What parts of this system can be tested without entering Play Mode? Are there CI headless test runs? How are Unity-specific side effects (physics, time) handled in tests?"

**Build & Deployment**
- "Which platforms are in scope for this change? Does it require IL2CPP-specific considerations? Is there a build server, and how are platform-specific assets handled?"

**Open Risks & Questions**
- "What do you not know yet that could require a significant redesign? Are there Unity version upgrade concerns or package compatibility risks?"

---

## Critic Focus Areas

When critiquing answers in this domain, pay special attention to:

- **GC allocation hotspots** — patterns that allocate in Update/FixedUpdate (LINQ, string ops, boxing, new collections)
- **Inspector-driven coupling** — serialized direct references that make components untestable and scene-order dependent
- **Platform rendering gaps** — shader features or post-processing that work in Editor but fail on mobile or console
- **Untracked asset memory** — assets loaded without an explicit unload strategy causing memory leaks over session
- **Missing FixedUpdate budget** — physics-heavy solutions without an estimate of FixedUpdate execution cost
- **Singleton/manager sprawl** — architecture that adds yet another static manager without addressing the existing accumulation
- **Save format lock-in** — serialization choices that are hard to version or migrate as the game evolves
- **Input System split** — mixing old and new input APIs in the same project, which causes subtle platform bugs
