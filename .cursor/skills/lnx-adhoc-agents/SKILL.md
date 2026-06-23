---
description: |
  Analyze a task in the parent context, break it into 2-8 parallelizable
  subtasks, group them by shared context into 2-4 subagent batches, and fan
  out. Cancels if parallelism isn't warranted.
  NOT for: sequential tasks, single-file changes, or tasks requiring
  cross-subtask synthesis.
alwaysApply: false
---

# lnx-adhoc-agents

Fan out a task to parallel subagents, grouped by shared context to minimize token waste.

## When to use

When the current task has multiple independent work items that would benefit from parallel execution.

## Procedure

### 1. Analyze in the parent context

Before spawning anything, fully understand the task: read the relevant files, trace the code paths, identify all work items. The parent holds the mental model — subagents receive instructions, not open-ended questions.

### 2. Decompose into subtasks

Break the work into 2–8 subtasks that can run independently — no subtask should depend on another's output. If you can't identify at least 2 parallelizable subtasks, **stop here and do the work inline**.

### 3. Group by shared context

Cluster subtasks into **2–4 groups** where subtasks in the same group will read/write overlapping files or need the same domain knowledge. Each group becomes one subagent. This avoids loading the same context across multiple agents.

### 4. Write the prompts and spawn

For each group, write a single self-contained prompt that:

- States the overall goal in 1–2 sentences
- Lists the exact file paths and line numbers to touch
- Describes the specific changes to make
- Includes any constraints or patterns to follow

Spawn all groups in a **single message** with parallel Agent tool calls.

## Constraints

- Each subagent must stay under **120k tokens** — scope accordingly (2–4 files of meaningful changes per agent max)
- Prefer **fewer meatier agents** over many tiny ones — each spawn has fixed overhead
- Never ask a subagent to "explore and then implement" — split exploration (Explore agent) from implementation
- After all agents complete, **verify the results** yourself: check actual file changes, run tests, resolve conflicts
- **Cancel** if the task is too short, too simple, or has no parallelizable subtasks — doing it inline is cheaper
