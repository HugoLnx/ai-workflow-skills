# lnx-grill-me: Anti-Patterns

---

### Anti-Pattern: Stacking Questions
**Novice**: "I'll ask all the scope questions at once to save time."
**Expert**: Asking multiple questions in one turn lets the user give shallow answers to all of them instead of a deep answer to one. The single-question discipline surfaces the mental model accurately.
**Timeline**: N/A — always been the correct approach for structured interviews.
**LLM mistake**: Models optimize for information throughput and batch related questions. They do not model that depth per question is more valuable than breadth per turn.
**Detection**: Any turn containing two question marks when the user hasn't answered yet.

### Anti-Pattern: Showing Recommendation Unprompted
**Novice**: "I'll include my recommended answer so the user has a starting point."
**Expert**: Surfacing the recommendation before the user answers anchors their thinking to the AI's view. The entire value of the interview is capturing the user's actual mental model. Reveal the recommendation only on explicit request.
**Timeline**: N/A — anchoring bias is well-established.
**LLM mistake**: Models are trained to be helpful by providing complete answers. Withholding a known answer feels unhelpful, so they default to sharing it.
**Detection**: Any turn with "I recommend", "I suggest", or "my answer would be" before the user has answered the current question.

### Anti-Pattern: Skipping the Critic
**Novice**: "The user gave a clear answer — I'll just move on."
**Expert**: The critic is the core mechanism for surfacing gaps. Even clear answers have edge cases and unstated assumptions. Skipping the critic leaves problems that surface late in the spec or in production.
**Timeline**: N/A — the critic is mandatory for every non-skipped answer.
**LLM mistake**: Models treat a clear, confident answer as complete. They do not proactively search for what is missing when something looks right.
**Detection**: Any transition to the next question without a critic block for the prior answer.

### Anti-Pattern: Sequential Specialist Consultation
**Novice**: "I'll ask each specialist skill one by one for their critique."
**Expert**: Specialists are independent — there is no dependency between their critiques. Calling them sequentially multiplies latency with no benefit. Always launch one subagent per specialist in a single message.
**Timeline**: N/A — parallelism is always correct here.
**LLM mistake**: Models default to sequential tool calls because that is the dominant pattern in training data. Parallel subagent patterns require explicit instruction.
**Detection**: Multiple `Agent` tool calls in separate turns for the same question's critic phase.
