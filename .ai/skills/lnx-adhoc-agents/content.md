# lnx-adhoc-agents

Fan out a task to parallel subagents, grouped by shared context to minimize token waste.

1. **Analyze first.** Fully understand the task in the parent context — read files, trace code paths. The parent holds the mental model; subagents receive instructions, not open-ended questions.
2. **Decompose** into 2–8 independent subtasks (no cross-dependencies). If < 2 parallelizable subtasks, **stop and work inline**.
3. **Group** subtasks into 2–4 clusters by shared context (overlapping files, same domain). Each cluster = one subagent.
4. **Spawn** all clusters in a single message with parallel Agent calls. Each prompt must be self-contained: overall goal (1–2 sentences), exact file paths/lines, specific changes, patterns to follow.

## Constraints

- Max **120k tokens** per subagent — limit to 2–4 files of meaningful changes each.
- Prefer fewer meatier agents over many tiny ones (each spawn has fixed overhead).
- Never combine exploration and implementation in one agent — use Explore first, then implement.
- **Verify** all results after agents complete: check file changes, run tests, resolve conflicts.
- **Cancel** if the task is too short or simple — inline is cheaper.
