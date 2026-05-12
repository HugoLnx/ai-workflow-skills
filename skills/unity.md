---
name: unity
description: >
  Unity-specific AI assistance for C# game development. Covers MonoBehaviour patterns,
  ScriptableObject design, coroutines vs. async/await, Unity lifecycle, performance
  optimization, and editor scripting. Triggers: "unity component", "monobehaviour",
  "scriptableobject", "coroutine", "unity pattern", "game object", "unity project".
---

## Purpose

Provide AI assistance specialized for Unity C# game development. Understands Unity's
component model, lifecycle methods, serialization system, and the specific patterns
and constraints that differ from standard C# application development.

## Activation Criteria

- User mentions Unity, MonoBehaviour, GameObject, ScriptableObject, or Prefab
- User asks about coroutines, Unity lifecycle, or Unity-specific patterns
- User asks about Unity editor scripting, inspector customization, or build pipelines
- User asks about Unity performance, profiling, or optimization
- The project contains `Assets/`, `ProjectSettings/`, or `*.unity` files

## Steps

1. **Identify Unity context**:
   - Check for `Assets/`, `ProjectSettings/`, `Packages/manifest.json`
   - Detect Unity version from `ProjectSettings/ProjectVersion.txt`
   - Detect render pipeline (URP, HDRP, Built-in) from package manifest
   - Detect scripting backend (Mono vs. IL2CPP) from Player Settings

2. **Apply Unity-specific conventions**:

   **MonoBehaviour classes**:
   - Class name must match file name exactly
   - Never use constructors — use `Awake()` or `Start()` for initialization
   - Prefer `Awake()` for self-initialization, `Start()` for cross-component references
   - Cache component references in `Awake()`, not in `Update()`
   - Use `[SerializeField]` over `public` for inspector-exposed fields
   - Never call `new` on MonoBehaviours — use `AddComponent<>()` or `Instantiate()`

   **Lifecycle order** (for documentation):
   Awake → OnEnable → Start → FixedUpdate → Update → LateUpdate → OnDisable → OnDestroy

   **ScriptableObjects**:
   - Use for shared data that doesn't need a scene instance
   - Use `[CreateAssetMenu]` attribute for inspector creation
   - Good use cases: game config, item databases, event channels, audio clips config
   - Avoid storing session-state in ScriptableObjects (they persist between Play Mode runs in editor)

3. **Coroutines vs. async/await**:
   - Prefer coroutines for Unity-specific timing (`WaitForSeconds`, `WaitForEndOfFrame`, `WaitUntil`)
   - Use `async/await` (with UniTask or built-in) for I/O operations, web requests, file loading
   - Never mix Unity's `Coroutine` system with standard `Task` without a bridge library
   - Always store coroutine references if you need to stop them: `private Coroutine _myRoutine;`

4. **Performance conventions**:
   - Cache `GetComponent<>()` calls — never call in `Update()`
   - Use `Object.FindObjectOfType<>()` sparingly — only during initialization
   - Use `CompareTag()` instead of `tag ==` string comparison
   - Avoid allocations in `Update()` (string concatenation, LINQ, `new` expressions)
   - Use object pooling for frequently instantiated/destroyed objects
   - Profile with Unity Profiler before optimizing — don't guess

5. **Code generation for Unity**:
   - When creating a MonoBehaviour: include class-level `[RequireComponent]` if needed
   - When creating editor scripts: place in `Editor/` directory, use `[CustomEditor]` or `[CustomPropertyDrawer]`
   - When creating a singleton: use a thread-safe pattern with `Application.isPlaying` check
   - When creating an event system: prefer UnityEvent or ScriptableObject event channels

## Output Format

Complete C# script files placed in the appropriate Unity directory structure.
Include `using` statements, proper class structure, and Unity lifecycle methods in canonical order.

## Scope

`Assets/**/*.cs` — all C# files in Unity Assets directory.

## Constraints

- Follow Unity's lifecycle; do not use standard C# patterns that conflict with Unity's object model
- Do not use `System.Threading.Thread` directly — use Unity's Job System for CPU-bound parallelism
- Do not allocate in hot paths (`Update`, `FixedUpdate`, `OnGUI`)
- Respect IL2CPP compatibility: avoid reflection-heavy code, ensure `[Preserve]` attributes
  where needed for AOT compilation

## Edge Cases

- **Domain Reload disabled**: Warn that static fields and events must be manually reset
  in `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]`
- **WebGL target**: No threading, no file system access, limited memory — note constraints
- **Addressables**: Loading is async; always use `AsyncOperationHandle` and release handles
- **Unity 6+ features**: Note when a pattern requires Unity 6 or higher

## Cross-Ecosystem Notes

- **Cursor**: Activate with `@50-skill-unity` while C# Unity scripts are open
- **Aider**: `/add <script.cs>`, reference the Unity section in CONVENTIONS.md
- **Codex**: Reference "Task: Unity C# Development" in AGENTS.md
