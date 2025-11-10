# Day 1B: Agent Architectures - Complete Learning Guide

## 🎯 Core Concept: From Solo Agent to Agent Teams

### The Evolution of Agentic Systems

**Single Agent (Day 1A):**
```
User: "Research quantum computing and write a summary"
Agent: [Thinks] "I need to research AND write AND summarize"
      [Gets overwhelmed]
      [Produces inconsistent results]
```

**Multi-Agent System (Day 1B):**
```
User: "Research quantum computing and write a summary"
Coordinator: [Thinks] "This needs specialized agents"
            [Acts] Calls Research Agent → Gets findings
            [Acts] Calls Writer Agent → Gets summary
            [Responds] Delivers high-quality, specialized output
```

### The Paradigm Shift: Monolithic vs. Multi-Agent

This is the **fundamental architectural shift** from single-purpose to team-based agents:

1. **Specialization** - Each agent has one clear, focused responsibility
2. **Composability** - Agents can be mixed, matched, and reused
3. **Maintainability** - Easy to debug, test, and improve individual agents
4. **Scalability** - Add new capabilities by adding new specialized agents

---

## 🧱 The Problem with Monolithic Agents

### Why "Do-It-All" Agents Fail

Imagine building a single agent with this instruction:

```python
instruction = """You are a comprehensive research and writing assistant.
First, search for information on the topic using Google Search.
Then, analyze the findings and identify key themes.
Next, create an outline based on the themes.
After that, write a full blog post following the outline.
Then, edit the blog post for grammar and clarity.
Finally, fact-check all claims and add citations.
"""
```

**Problems with this approach:**

#### 1. Instruction Bloat
- The instruction becomes a giant wall of text
- Hard to read and maintain
- The LLM may miss or skip steps
- Unclear which part failed when something goes wrong

#### 2. Unpredictable Execution
- The LLM might skip steps: "I'll combine research and writing"
- Order may vary: Sometimes edits before writing is complete
- Tool usage becomes inconsistent
- No guaranteed workflow

#### 3. Difficult Debugging
- When output is bad, where did it fail?
- Was it bad research? Poor writing? Weak editing?
- No visibility into individual steps
- Hard to isolate and fix issues

#### 4. No Reusability
- Can't reuse the "research" part for other tasks
- Can't swap out the "writer" for a different style
- Monolithic = rigid and inflexible

#### 5. Context Window Waste
- All instructions loaded for every step
- Even when only one capability is needed
- Increases token usage and cost

---

## ✅ The Multi-Agent Solution

### The Assembly Line Metaphor

Think of multi-agent systems like a **car assembly line**:

- **Station 1 (Research Agent)**: Installs the engine (gathers information)
- **Station 2 (Writer Agent)**: Adds the body (structures content)
- **Station 3 (Editor Agent)**: Applies paint and finishing (polishes output)

Each station:
- Has **one clear job**
- Is **specialized** and good at it
- Can be **tested independently**
- Can be **replaced or upgraded** without affecting others

### The Team Metaphor

Or think of it like a **professional team**:

```
Project Manager (Root Agent)
    ↓
    ├─→ Research Specialist (Research Agent)
    ├─→ Content Writer (Writer Agent)
    └─→ Quality Editor (Editor Agent)
```

Each team member:
- Has a **specific role**
- Communicates with the **project manager**
- Passes work to the **next specialist**
- Can work **in parallel** when tasks are independent

---

## 🏗️ Multi-Agent Architecture Patterns

ADK provides **four fundamental patterns** for building multi-agent systems. Each pattern solves a specific type of workflow challenge.

---

## 🎭 Pattern 1: LLM-Based Orchestration

### The Dynamic Manager

**Concept:** A "root" agent acts as a manager, using other agents as tools. The LLM **decides dynamically** which agents to call, in what order, and with what inputs.

**Architecture:**
```
Root Coordinator (LLM-based decision maker)
    ↓ (decides what to do)
    ├─→ Research Agent (wrapped in AgentTool)
    └─→ Summarizer Agent (wrapped in AgentTool)
```

**Visual Flow:**
```
User Query: "What are quantum computers?"
    ↓
Root Agent analyzes query
    ↓
Decides: "Need current information"
    ↓
Calls: ResearchAgent tool
    ↓
Receives: Research findings
    ↓
Decides: "Now need summary"
    ↓
Calls: SummarizerAgent tool
    ↓
Receives: Concise summary
    ↓
Returns: Final answer to user
```

### How It Works

#### Step 1: Define Specialized Agents

```python
# Research Agent: ONLY does research
research_agent = Agent(
    name="ResearchAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a specialized research agent.
    Use google_search to find 2-3 relevant pieces of information
    and present findings with citations.""",
    tools=[google_search],
    output_key="research_findings",  # ← Stores result in session state
)
```

**Key points:**
- **Focused instruction**: Only research, nothing else
- **Tools**: Only needs search capability
- **output_key**: Critical! This is how data is passed between agents

#### Step 2: Define Second Specialist

```python
# Summarizer Agent: ONLY summarizes
summarizer_agent = Agent(
    name="SummarizerAgent",
    model="gemini-2.5-flash-lite",
    instruction="""Read these research findings: {research_findings}
    Create a concise summary as a bulleted list with 3-5 key points.""",
    output_key="final_summary",
)
```

**Key points:**
- **Placeholder injection**: `{research_findings}` pulls data from session state
- **No tools**: This agent doesn't need external tools
- **Different output_key**: Creates new state entry

#### Step 3: Create the Coordinator

```python
# Root Agent: Orchestrates the workflow
root_agent = Agent(
    name="ResearchCoordinator",
    model="gemini-2.5-flash-lite",
    instruction="""You are a research coordinator.
    1. MUST call ResearchAgent tool to find information
    2. MUST call SummarizerAgent tool to create summary
    3. Present the final summary to the user""",
    tools=[
        AgentTool(research_agent),    # ← Wraps agent as callable tool
        AgentTool(summarizer_agent)
    ],
)
```

**Key points:**
- **Explicit workflow**: Instructions guide the LLM's decisions
- **AgentTool wrapper**: Makes agents callable as tools
- **No output_key**: Root typically returns directly to user

### Understanding AgentTool

`AgentTool` is how you **turn an agent into a callable tool** for another agent.

**What it does:**
```python
AgentTool(research_agent)
```

Transforms this agent into a function that:
1. The LLM can **see** in its tool list
2. The LLM can **decide** to call
3. ADK can **execute** and return results
4. Automatically handles **session state** passing

**Behind the scenes:**
```
Root Agent's internal tool list:
[
    {
        "name": "ResearchAgent",
        "description": "A specialized research agent",
        "function": <callable that runs research_agent>
    },
    {
        "name": "SummarizerAgent",
        "description": "Creates concise summaries",
        "function": <callable that runs summarizer_agent>
    }
]
```

### When to Use LLM-Based Orchestration

**Ideal for:**
- **Dynamic workflows** where the path depends on the input
- **Conditional logic** ("if X, then do Y, else do Z")
- **Flexible scenarios** where you want the LLM to decide
- **Exploratory tasks** where the best approach isn't always clear

**Examples:**
- Customer support routing (different questions need different agents)
- Adaptive learning systems (adjust based on student responses)
- Complex research (may need more or fewer steps)

**Drawbacks:**
- **Unpredictable**: LLM might skip steps or change order
- **Harder to debug**: "Why did it do that?"
- **Can be slower**: LLM decision-making adds latency
- **More token usage**: Instructions need to guide behavior

### Deep Dive: Session State and output_key

**What is Session State?**

Session state is a **shared memory** that all agents in a workflow can access. Think of it as a **shared clipboard** or **whiteboard** where agents write their results.

```python
# Session State (conceptual representation)
session_state = {
    "research_findings": "Quantum computers use qubits...",
    "final_summary": "• Quantum computers leverage superposition\n• ..."
}
```

**How output_key Works:**

1. **Agent produces output**
   ```python
   research_agent = Agent(
       output_key="research_findings",  # ← This is the key!
   )
   ```

2. **Output is stored in state**
   ```python
   # After research_agent runs:
   session_state["research_findings"] = "Quantum computers use qubits..."
   ```

3. **Next agent reads from state**
   ```python
   instruction="""Read these findings: {research_findings}"""
   # The {research_findings} placeholder is replaced with the actual value
   ```

**Why this matters:**
- **Data passing**: Agents communicate through state
- **Decoupling**: Agents don't directly call each other
- **Flexibility**: Any agent can read any state value
- **Debugging**: You can inspect state at any point

---

## 🚥 Pattern 2: Sequential Agent - The Assembly Line

### Guaranteed Execution Order

**Concept:** When you need tasks to happen in a **specific, predictable order**, use `SequentialAgent`. It runs sub-agents like an assembly line: Agent 1 → Agent 2 → Agent 3, always in that order.

**Architecture:**
```
SequentialAgent
    ↓
    Step 1: Outline Agent
    ↓ (output: blog_outline)
    Step 2: Writer Agent (uses blog_outline)
    ↓ (output: blog_draft)
    Step 3: Editor Agent (uses blog_draft)
    ↓ (output: final_blog)
```

**Visual Flow:**
```
User: "Write a blog post about AI agents"
    ↓
Sequential Agent starts
    ↓
[Step 1] Outline Agent
    ├─ Instruction: "Create a blog outline"
    ├─ Produces: Detailed outline structure
    └─ Stores: session_state["blog_outline"]
    ↓
[Step 2] Writer Agent
    ├─ Instruction: "Write blog following {blog_outline}"
    ├─ Reads: session_state["blog_outline"]
    ├─ Produces: Full blog draft
    └─ Stores: session_state["blog_draft"]
    ↓
[Step 3] Editor Agent
    ├─ Instruction: "Edit {blog_draft} for clarity"
    ├─ Reads: session_state["blog_draft"]
    ├─ Produces: Polished final blog
    └─ Stores: session_state["final_blog"]
    ↓
Return final_blog to user
```

### How It Works

#### Step 1: Define Sequential Sub-Agents

Each agent is **designed to do one step** in the pipeline:

```python
# Step 1: Create the outline
outline_agent = Agent(
    name="OutlineAgent",
    model="gemini-2.5-flash-lite",
    instruction="""Create a blog outline with:
    1. A catchy headline
    2. An introduction hook
    3. 3-5 main sections with bullet points
    4. A concluding thought""",
    output_key="blog_outline",
)

# Step 2: Write the full blog
writer_agent = Agent(
    name="WriterAgent",
    model="gemini-2.5-flash-lite",
    instruction="""Following this outline strictly: {blog_outline}
    Write a 200-300 word blog post with an engaging tone.""",
    output_key="blog_draft",
)

# Step 3: Edit and polish
editor_agent = Agent(
    name="EditorAgent",
    model="gemini-2.5-flash-lite",
    instruction="""Edit this draft: {blog_draft}
    Fix grammar, improve flow, enhance clarity.""",
    output_key="final_blog",
)
```

**Notice the data flow:**
- `outline_agent` produces `blog_outline`
- `writer_agent` reads `{blog_outline}`, produces `blog_draft`
- `editor_agent` reads `{blog_draft}`, produces `final_blog`

This creates a **dependency chain**: each step builds on the previous one.

#### Step 2: Wrap in SequentialAgent

```python
root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[
        outline_agent,   # ← Runs first
        writer_agent,    # ← Runs second
        editor_agent     # ← Runs third
    ],
)
```

**Key points:**
- **Order is guaranteed**: Always runs in the list order
- **No instruction needed**: The workflow is the structure itself
- **Automatic state passing**: Each agent's output_key is available to the next
- **Simple and predictable**: No LLM decision-making involved

### Understanding the Execution Flow

**What happens when you run:**
```python
runner = InMemoryRunner(agent=root_agent)
response = await runner.run_debug("Write a blog about AI agents")
```

**Internal execution:**

1. **User input received**: "Write a blog about AI agents"
2. **SequentialAgent starts**: Begins executing sub_agents list
3. **Run outline_agent**:
   - Input: User's original message
   - Processing: LLM generates outline
   - Output: Stored as `session_state["blog_outline"]`
4. **Run writer_agent**:
   - Input: User's original message + `session_state["blog_outline"]`
   - Processing: LLM writes blog following outline
   - Output: Stored as `session_state["blog_draft"]`
5. **Run editor_agent**:
   - Input: User's original message + `session_state["blog_draft"]`
   - Processing: LLM edits and polishes
   - Output: Stored as `session_state["final_blog"]`
6. **Return to user**: The final output (`final_blog`)

### When to Use Sequential Agents

**Ideal for:**
- **Linear pipelines** where each step builds on the previous
- **Fixed workflows** that always follow the same path
- **Data transformation chains** (raw → processed → refined)
- **Quality control** (draft → review → final)

**Examples:**
- Content creation (outline → write → edit)
- Data processing (extract → transform → load)
- Application pipelines (validate → process → store)
- Multi-step calculations (gather → compute → format)

**Advantages:**
- **Predictable**: Always runs in the same order
- **Debuggable**: Easy to see which step failed
- **Efficient**: No LLM overhead for orchestration decisions
- **Clear**: The code structure matches the workflow

**Drawbacks:**
- **Rigid**: Can't adapt to different scenarios
- **Slower**: Must complete each step before starting the next
- **Wasteful**: Runs all steps even if some aren't needed

---

## 🛣️ Pattern 3: Parallel Agent - The Multi-Tasker

### Concurrent Execution for Independent Tasks

**Concept:** When you have tasks that are **independent and can run simultaneously**, use `ParallelAgent`. It executes all sub-agents at the same time, dramatically reducing total execution time.

**Architecture:**
```
User Request
    ↓
ParallelAgent starts
    ├─→ Tech Researcher    ─┐
    ├─→ Health Researcher  ─┤ (All run simultaneously)
    └─→ Finance Researcher ─┘
           ↓ (All complete)
    Aggregator Agent (combines results)
           ↓
    Final Report
```

**Visual Flow:**
```
User: "Research Tech, Health, Finance trends"
    ↓
Parallel Agent starts
    ↓
╔══════════════════════╗
║  Concurrent Block    ║
╠══════════════════════╣
║ [Tech Researcher]    ║─→ Searches AI/ML trends (5 seconds)
║ [Health Researcher]  ║─→ Searches medical news (5 seconds)
║ [Finance Researcher] ║─→ Searches fintech trends (5 seconds)
╚══════════════════════╝
    ↓ (All finish simultaneously at ~5 seconds)
    ↓
Aggregator combines all three reports (2 seconds)
    ↓
Total time: ~7 seconds (vs. 17 seconds if sequential!)
```

### How It Works

#### Step 1: Define Independent Researcher Agents

Each agent researches a **completely separate topic**:

```python
# Tech Researcher: Focuses on AI/ML
tech_researcher = Agent(
    name="TechResearcher",
    model="gemini-2.5-flash-lite",
    instruction="""Research the latest AI/ML trends.
    Include 3 key developments, main companies involved,
    and potential impact. Keep it concise (100 words).""",
    tools=[google_search],
    output_key="tech_research",  # ← Independent output
)

# Health Researcher: Focuses on medical breakthroughs
health_researcher = Agent(
    name="HealthResearcher",
    model="gemini-2.5-flash-lite",
    instruction="""Research recent medical breakthroughs.
    Include 3 significant advances, practical applications,
    and estimated timelines. Keep it concise (100 words).""",
    tools=[google_search],
    output_key="health_research",  # ← Independent output
)

# Finance Researcher: Focuses on fintech
finance_researcher = Agent(
    name="FinanceResearcher",
    model="gemini-2.5-flash-lite",
    instruction="""Research current fintech trends.
    Include 3 key trends, market implications,
    and future outlook. Keep it concise (100 words).""",
    tools=[google_search],
    output_key="finance_research",  # ← Independent output
)
```

**Key characteristic:** These agents have **no dependencies** on each other. They can run at the same time.

#### Step 2: Create an Aggregator

After parallel execution, you need to **combine the results**:

```python
aggregator_agent = Agent(
    name="AggregatorAgent",
    model="gemini-2.5-flash-lite",
    instruction="""Combine these research findings:

    Technology: {tech_research}
    Health: {health_research}
    Finance: {finance_research}

    Create an executive summary highlighting common themes,
    surprising connections, and key takeaways (~200 words).""",
    output_key="executive_summary",
)
```

**Why the aggregator is crucial:**
- Parallel agents produce **separate outputs**
- Aggregator **synthesizes** them into a cohesive whole
- Finds **patterns** across domains
- Provides **unified insight**

#### Step 3: Compose with Parallel + Sequential

Here's where it gets interesting. You **nest** ParallelAgent inside SequentialAgent:

```python
# Step 1: Parallel research team
parallel_research_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[
        tech_researcher,
        health_researcher,
        finance_researcher
    ],
)

# Step 2: Sequential workflow: Parallel first, then Aggregator
root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[
        parallel_research_team,  # ← All three run concurrently
        aggregator_agent         # ← Runs after parallel completes
    ],
)
```

**Why this structure?**
- **ParallelAgent**: Runs all research simultaneously
- **SequentialAgent**: Ensures aggregator waits until research is done
- **Composability**: You can mix and match workflow patterns!

### Understanding the Execution Flow

**When you run:**
```python
runner = InMemoryRunner(agent=root_agent)
response = await runner.run_debug("Daily briefing on Tech, Health, Finance")
```

**Internal execution:**

1. **SequentialAgent starts**
2. **Run parallel_research_team (first sub-agent)**
   - **ParallelAgent starts**
   - Spawns three concurrent tasks:
     - Task 1: `tech_researcher` executes
     - Task 2: `health_researcher` executes
     - Task 3: `finance_researcher` executes
   - All three make Google Search API calls **simultaneously**
   - **Waits** for all three to complete
   - Results stored:
     - `session_state["tech_research"]`
     - `session_state["health_research"]`
     - `session_state["finance_research"]`
3. **Run aggregator_agent (second sub-agent)**
   - Reads all three research outputs from state
   - Combines into unified summary
   - Stores: `session_state["executive_summary"]`
4. **Return final summary to user**

### The Power of Parallelism: Time Savings

**Sequential execution time:**
```
Tech Research:    5 seconds
Health Research:  5 seconds
Finance Research: 5 seconds
Aggregation:      2 seconds
---------------------------------
Total:           17 seconds
```

**Parallel execution time:**
```
┌─ Tech Research:    5 seconds ─┐
├─ Health Research:  5 seconds ─┤ (all run simultaneously)
└─ Finance Research: 5 seconds ─┘
    Aggregation:     2 seconds
---------------------------------
Total:               7 seconds (59% faster!)
```

### When to Use Parallel Agents

**Ideal for:**
- **Independent tasks** with no dependencies
- **Speed-critical workflows** where latency matters
- **Multi-source data gathering** (APIs, databases, searches)
- **Distributed processing** (can scale across machines)

**Examples:**
- Multi-topic research (like our example)
- Parallel API calls to different services
- Concurrent database queries
- Multi-model ensemble predictions
- A/B testing different prompts simultaneously

**Advantages:**
- **Fast**: Dramatic speed improvements
- **Efficient**: Maximizes resource utilization
- **Scalable**: Can add more parallel agents easily
- **Clear**: Easy to see what runs concurrently

**Drawbacks:**
- **Resource intensive**: All agents run at once (more memory/compute)
- **Only for independent tasks**: Can't use if tasks depend on each other
- **Complexity**: Harder to debug when multiple things happen at once

### Advanced Pattern: Nested Parallelism

You can nest parallel agents for even more concurrency:

```python
# Multiple parallel teams, each with parallel sub-agents
team_alpha = ParallelAgent(
    sub_agents=[researcher_1, researcher_2, researcher_3]
)

team_beta = ParallelAgent(
    sub_agents=[analyst_1, analyst_2, analyst_3]
)

# Run both teams in parallel!
super_parallel = ParallelAgent(
    sub_agents=[team_alpha, team_beta]
)
```

This creates a **2D parallel execution**: 6 agents running simultaneously!

---

## ➰ Pattern 4: Loop Agent - The Refiner

### Iterative Improvement Until Perfection

**Concept:** When you need to **repeatedly refine output** until it meets quality standards, use `LoopAgent`. It runs sub-agents in a cycle, checking quality after each iteration, and stops when approved or max iterations reached.

**Architecture:**
```
Initial Draft
    ↓
┌───────────────────────┐
│   Loop Agent          │
│   ┌──────────────┐    │
│   │ Critic Agent │    │
│   └──────┬───────┘    │
│          ↓            │
│   ┌──────────────┐    │
│   │Refiner Agent │    │
│   └──────┬───────┘    │
│          ↓            │
│    Approved? No ──────┤ (loop back)
└──────────┬────────────┘
           ↓ Yes
    Final Output
```

**Visual Flow:**
```
User: "Write a story about a lighthouse keeper"
    ↓
Initial Writer: Creates first draft
    ↓
─────────────────────────
LOOP START (max 3 times)
─────────────────────────
    ↓
Critic Agent: Reviews draft
    ├─ Checks plot, characters, pacing
    └─ Returns: "APPROVED" or specific feedback
    ↓
Refiner Agent: Analyzes critique
    ├─ If "APPROVED" → Calls exit_loop() → STOP
    └─ If feedback → Rewrites story → LOOP BACK
    ↓
─────────────────────────
LOOP END
─────────────────────────
    ↓
Final Story
```

### How It Works

#### Step 1: Create Initial Draft Agent

This agent runs **once** before the loop to create the first draft:

```python
initial_writer_agent = Agent(
    name="InitialWriterAgent",
    model="gemini-2.5-flash-lite",
    instruction="""Based on the user's prompt, write the first draft
    of a short story (100-150 words). Output only the story text.""",
    output_key="current_story",  # ← This will be refined in the loop
)
```

**Why separate?** You don't want to regenerate from scratch each loop iteration. You want to **refine** the existing draft.

#### Step 2: Create the Critic Agent

This agent **evaluates quality** and provides feedback:

```python
critic_agent = Agent(
    name="CriticAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a constructive story critic.
    Review this story: {current_story}

    Evaluate plot, characters, and pacing.
    - If well-written and complete, respond EXACTLY: "APPROVED"
    - Otherwise, provide 2-3 specific, actionable suggestions.""",
    output_key="critique",
)
```

**Key aspects:**
- **Binary decision**: Either "APPROVED" or constructive feedback
- **No tools**: Pure evaluation, no external calls
- **Specific format**: "APPROVED" must be exact for exit detection

#### Step 3: Create the Exit Mechanism

The loop needs a way to **stop**. You define a Python function:

```python
def exit_loop():
    """Call this ONLY when critique is 'APPROVED',
    indicating the story is finished."""
    return {
        "status": "approved",
        "message": "Story approved. Exiting refinement loop."
    }
```

**Why a function?** LoopAgent doesn't automatically understand "APPROVED" means "stop". You need an **explicit exit signal** that the agent can call.

#### Step 4: Create the Refiner Agent

This is the **brain of the loop** - it decides whether to exit or refine:

```python
refiner_agent = Agent(
    name="RefinerAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a story refiner.

    Story Draft: {current_story}
    Critique: {critique}

    Analyze the critique:
    - IF critique is EXACTLY "APPROVED", call the exit_loop function
    - OTHERWISE, rewrite the story incorporating the feedback""",
    output_key="current_story",  # ← OVERWRITES the draft with refined version
    tools=[FunctionTool(exit_loop)],  # ← Can call exit function
)
```

**Critical design choices:**

1. **Same output_key**: `output_key="current_story"` **overwrites** the previous draft
   - This is how refinement happens: each iteration improves the same story

2. **FunctionTool wrapper**: Makes `exit_loop()` callable by the agent
   - The agent can decide to call it based on the critique

3. **Conditional logic in instruction**: Tells agent when to exit vs. refine
   - LLM reads critique and chooses action

#### Step 5: Compose the Full System

Now you **nest** LoopAgent inside SequentialAgent:

```python
# The refinement loop: Critic → Refiner → (repeat or exit)
story_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=3,  # ← Safety limit: prevents infinite loops
)

# Full pipeline: Initial Write → Refinement Loop
root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[
        initial_writer_agent,      # Runs once
        story_refinement_loop      # Runs up to 3 times
    ],
)
```

**Why this structure?**
- **SequentialAgent**: Ensures initial draft before loop starts
- **LoopAgent**: Handles the iterative refinement
- **max_iterations**: Critical safety feature (prevents runaway loops)

### Understanding the Execution Flow

**When you run:**
```python
runner = InMemoryRunner(agent=root_agent)
response = await runner.run_debug("Write a story about a lighthouse keeper...")
```

**Internal execution:**

1. **SequentialAgent starts**
2. **Run initial_writer_agent**
   - Creates first draft of story
   - Stores: `session_state["current_story"] = "The salt spray was..."`
3. **Run story_refinement_loop (LoopAgent)**
   - **Iteration 1:**
     - **Critic Agent** reads `{current_story}`, produces `{critique}`
       - Example: "The story lacks character development. Add more about the keeper's past."
     - **Refiner Agent** reads `{current_story}` and `{critique}`
       - Sees critique is not "APPROVED"
       - Rewrites story with improvements
       - Stores: `session_state["current_story"] = "The salt spray was... For thirty years..."`
   - **Iteration 2:**
     - **Critic Agent** reads updated `{current_story}`
       - Example: "Better! But the ending feels rushed. Expand the conclusion."
     - **Refiner Agent** reads `{current_story}` and `{critique}`
       - Sees critique is not "APPROVED"
       - Rewrites with better ending
       - Stores: `session_state["current_story"] = "The salt spray was... awakened things..."`
   - **Iteration 3:**
     - **Critic Agent** reads final `{current_story}`
       - Returns: "APPROVED"
     - **Refiner Agent** reads `{critique}`
       - Sees "APPROVED"
       - **Calls exit_loop() function**
       - LoopAgent receives exit signal → **STOPS**
4. **Return final story to user**

### The Exit Mechanism Deep Dive

**How does calling `exit_loop()` actually stop the loop?**

1. **FunctionTool wrapper**:
   ```python
   tools=[FunctionTool(exit_loop)]
   ```
   This makes the function available to the agent as a tool.

2. **Agent decides to call it**:
   ```
   Agent reasoning: "The critique says APPROVED, so I should call exit_loop"
   Agent action: [function_call: exit_loop()]
   ```

3. **ADK detects the function call**:
   - Sees the function being called
   - Recognizes it as an exit signal
   - Terminates the LoopAgent

4. **Execution continues**:
   - LoopAgent completes
   - SequentialAgent moves to next sub-agent (none left)
   - Returns final result

**What if max_iterations is reached first?**
- The loop **stops automatically** even if not approved
- This is a safety mechanism to prevent infinite loops
- Always set `max_iterations` to a reasonable number

### When to Use Loop Agents

**Ideal for:**
- **Iterative refinement** where output needs progressive improvement
- **Quality control** with multiple review cycles
- **Trial and error** processes
- **Optimization** tasks that get better over time

**Examples:**
- Content creation with critique (stories, articles, code)
- Design iteration (generate → critique → refine → repeat)
- Problem solving (attempt → evaluate → retry with improvements)
- Testing and debugging (run test → analyze failures → fix → retest)

**Advantages:**
- **Quality improvement**: Each iteration makes output better
- **Self-correcting**: Can fix its own mistakes
- **Flexible**: Works until "good enough" (not just one-shot)
- **Controllable**: max_iterations prevents runaway loops

**Drawbacks:**
- **Slower**: Multiple iterations take time
- **More expensive**: More LLM calls = more tokens = higher cost
- **Can get stuck**: Might not improve even with more iterations
- **Complex**: Harder to design and debug than simpler patterns

### Advanced Pattern: Multi-Agent Loop with Voting

You can create sophisticated loops with multiple critics:

```python
# Multiple critics provide different perspectives
critic_plot = Agent(name="PlotCritic", instruction="Evaluate plot...")
critic_character = Agent(name="CharacterCritic", instruction="Evaluate characters...")
critic_style = Agent(name="StyleCritic", instruction="Evaluate writing style...")

# Aggregator decides if story is approved based on all critiques
aggregator = Agent(
    name="CriticAggregator",
    instruction="""Review all critiques: {plot_critique}, {character_critique}, {style_critique}.
    If ALL approve, call exit_loop(). Otherwise, synthesize feedback for refiner.""",
    tools=[FunctionTool(exit_loop)]
)

# Loop structure
refinement_loop = LoopAgent(
    sub_agents=[
        critic_plot,
        critic_character,
        critic_style,
        aggregator,  # Decides on exit
        refiner_agent
    ],
    max_iterations=5
)
```

This creates a **multi-dimensional quality assessment** system!

---

## 🧠 Deep Dive: State Management Across Patterns

### How Session State Powers Multi-Agent Systems

Every multi-agent pattern relies on **session state** to pass data between agents. Understanding state management is crucial.

### Session State Lifecycle

```python
# 1. Runner creates a session
runner = InMemoryRunner(agent=root_agent)

# Behind the scenes:
session_state = {}  # Empty state initialized

# 2. First agent runs
research_agent = Agent(output_key="research_findings")
# After execution:
session_state["research_findings"] = "Quantum computers use qubits..."

# 3. Second agent reads and writes
summarizer_agent = Agent(
    instruction="Summarize: {research_findings}",
    output_key="summary"
)
# After execution:
session_state = {
    "research_findings": "Quantum computers use qubits...",
    "summary": "Quantum computing uses superposition..."
}

# 4. State persists throughout the session
# Any subsequent agent can read any key
```

### State Injection with Placeholders

**Placeholder syntax:** `{key_name}`

When an agent's instruction contains `{research_findings}`, ADK:
1. Looks up `session_state["research_findings"]`
2. Replaces the placeholder with the actual value
3. Sends the full instruction to the LLM

**Example transformation:**

Before injection:
```python
instruction = "Summarize these findings: {research_findings}"
```

After injection (what the LLM actually sees):
```python
instruction = """Summarize these findings: Quantum computers leverage quantum
mechanical phenomena like superposition and entanglement to process information
in fundamentally different ways than classical computers..."""
```

### State Overwriting in Loops

This is critical for LoopAgent:

```python
# Iteration 1
refiner_agent = Agent(output_key="current_story")
session_state["current_story"] = "First draft..."

# Iteration 2 (OVERWRITES)
refiner_agent = Agent(output_key="current_story")
session_state["current_story"] = "Improved draft..."  # ← Overwrites!

# Iteration 3 (OVERWRITES again)
session_state["current_story"] = "Final polished version..."
```

**Why this matters:**
- Each loop iteration **improves** the same piece of content
- Without overwriting, you'd accumulate multiple versions
- The same key name creates a **refinement chain**

### Multi-Key State in Parallel

ParallelAgent populates **multiple keys simultaneously**:

```python
# All three run concurrently
parallel_agent = ParallelAgent(sub_agents=[
    tech_researcher,     # output_key="tech_research"
    health_researcher,   # output_key="health_research"
    finance_researcher   # output_key="finance_research"
])

# After completion, session_state has all three:
session_state = {
    "tech_research": "AI trends include...",
    "health_research": "Medical breakthroughs include...",
    "finance_research": "Fintech trends include..."
}

# Aggregator can access all three
aggregator = Agent(
    instruction="""Combine: {tech_research}, {health_research}, {finance_research}"""
)
```

### State Scope and Isolation

**Within a session:** All agents share the same state

```python
# Session 1
runner.run_debug("Research quantum computing")
# session_state = {"research_findings": "Quantum info..."}

# Still Session 1
runner.run_debug("What did you find?")
# Agent can still access previous research_findings
```

**Across sessions:** State is isolated

```python
# Session 1
runner.run_debug("Research quantum computing")

# Session 2 (new session)
runner.run_debug("What did you find?")
# Error: No research_findings in this session's state
```

### Debugging State

**Inspecting state during development:**

```python
# Access session state (ADK internal API)
session = runner.get_session("debug_session_id")
print(session.state)

# Or add a debug agent
debug_agent = Agent(
    instruction="List all keys in session state: {__state_keys__}",
    output_key="debug_info"
)
```

---

## 🎯 Decision Framework: Choosing Your Pattern

### The Workflow Decision Tree

Use this flowchart to select the right pattern:

```
┌─────────────────────────────────────┐
│  What kind of workflow do you need? │
└────────────────┬────────────────────┘
                 │
    ┌────────────┼────────────┬─────────────┐
    │            │            │             │
    ▼            ▼            ▼             ▼
 Dynamic    Strict Order  Independent   Needs
 Routing                    Tasks      Refinement
    │            │            │             │
    ▼            ▼            ▼             ▼
   LLM       Sequential   Parallel        Loop
Orchestrator   Agent       Agent         Agent
```

### Pattern Selection Matrix

| Question | Yes → | No → |
|----------|-------|------|
| Do tasks depend on previous outputs? | Sequential | Parallel |
| Does the LLM need to decide the workflow? | LLM Orchestrator | Sequential/Parallel |
| Is speed more important than order? | Parallel | Sequential |
| Does output need multiple refinements? | Loop | Sequential |
| Are there conditional branches in the flow? | LLM Orchestrator | Sequential |
| Do you need quality control iterations? | Loop | Sequential |

### Real-World Scenario Examples

#### Scenario 1: Research Report Generation

**Requirements:**
- Gather info from multiple sources (independent)
- Combine findings (depends on gathering)
- Edit final report (depends on combining)

**Best Pattern:** Parallel + Sequential hybrid
```python
# Parallel: Independent research
research_team = ParallelAgent(sub_agents=[
    source_a_researcher,
    source_b_researcher,
    source_c_researcher
])

# Sequential: Research → Combine → Edit
SequentialAgent(sub_agents=[
    research_team,
    combiner_agent,
    editor_agent
])
```

#### Scenario 2: Customer Support Routing

**Requirements:**
- Analyze customer question
- Route to appropriate specialist (billing, tech, sales)
- Handle follow-up questions

**Best Pattern:** LLM Orchestrator
```python
# Dynamic routing based on question content
support_coordinator = Agent(
    instruction="Analyze query and call the appropriate specialist",
    tools=[
        AgentTool(billing_agent),
        AgentTool(tech_support_agent),
        AgentTool(sales_agent)
    ]
)
```

#### Scenario 3: Code Review System

**Requirements:**
- Check code quality (can run independently)
- Check security (can run independently)
- Check performance (can run independently)
- If issues found → request fixes → re-check

**Best Pattern:** Parallel + Loop hybrid
```python
# Parallel: Independent checks
review_team = ParallelAgent(sub_agents=[
    quality_checker,
    security_checker,
    performance_checker
])

# Loop: Review → Fix → Re-review
review_loop = LoopAgent(
    sub_agents=[review_team, fix_agent],
    max_iterations=3
)
```

#### Scenario 4: Blog Publishing Pipeline

**Requirements:**
- Generate outline (must happen first)
- Write content (needs outline)
- Add images (needs content)
- SEO optimization (needs content)
- Final review (needs everything)

**Best Pattern:** Sequential + Parallel hybrid
```python
# Sequential start: Outline → Write
# Parallel middle: Images + SEO (independent)
# Sequential end: Review

SequentialAgent(sub_agents=[
    outline_agent,
    writer_agent,
    ParallelAgent(sub_agents=[
        image_agent,
        seo_agent
    ]),
    review_agent
])
```

---

## 🔬 Advanced Concepts

### Composability: Mixing Patterns

The true power of ADK is **composing patterns** together:

```python
# A complex workflow combining all patterns
root = SequentialAgent(sub_agents=[
    # Step 1: LLM decides data sources
    LLM_Orchestrator_for_data_gathering,

    # Step 2: Parallel processing
    ParallelAgent(sub_agents=[
        analyzer_1,
        analyzer_2,
        analyzer_3
    ]),

    # Step 3: Iterative refinement
    LoopAgent(sub_agents=[
        critic,
        refiner
    ], max_iterations=3),

    # Step 4: Final polish
    final_editor
])
```

This creates a **4-stage pipeline** with different execution strategies at each stage!

### Error Handling and Resilience

**What if an agent fails?**

```python
# Wrap critical agents with retry logic
retry_agent = Agent(
    name="ResilientResearcher",
    instruction="If search fails, try alternative queries",
    tools=[google_search],
    # ADK handles retries internally for transient failures
)
```

**What if loop doesn't converge?**

```python
# Always set max_iterations
loop = LoopAgent(
    sub_agents=[critic, refiner],
    max_iterations=5,  # ← Safety net
)

# Handle "not approved but out of iterations" case
final_checker = Agent(
    instruction="""If {current_story} wasn't approved but we're out of
    iterations, do a final best-effort polish."""
)
```

### Performance Optimization

**Token efficiency:**
```python
# Bad: Long, repeated instructions
instruction = """You are a highly skilled, world-class expert researcher
with decades of experience..."""  # 200 tokens, repeated every call

# Good: Concise instructions
instruction = "Research the topic thoroughly and cite sources."  # 8 tokens
```

**State minimization:**
```python
# Bad: Storing entire documents in state
output_key = "full_research_paper"  # 50,000 tokens in state

# Good: Store summaries
output_key = "research_summary"  # 500 tokens in state
# Keep full paper in a separate storage system
```

**Parallel optimization:**
```python
# Identify independent tasks and parallelize aggressively
# This 8-agent parallel execution is fine:
ParallelAgent(sub_agents=[
    agent_1, agent_2, agent_3, agent_4,
    agent_5, agent_6, agent_7, agent_8
])
# As long as they're truly independent!
```

---

## 💡 Key Insights & Design Patterns

### 1. Single Responsibility Principle

Each agent should have **one clear job**:

**Bad:**
```python
do_everything_agent = Agent(
    instruction="Research, analyze, write, edit, and format"
)
```

**Good:**
```python
research_agent = Agent(instruction="Only research")
writer_agent = Agent(instruction="Only write")
editor_agent = Agent(instruction="Only edit")
```

### 2. Explicit State Management

Always use clear, descriptive `output_key` names:

**Bad:**
```python
output_key="result"  # What kind of result?
output_key="data"    # What data?
output_key="output"  # Too generic
```

**Good:**
```python
output_key="research_findings"
output_key="blog_draft"
output_key="quality_score"
```

### 3. Instruction Clarity

Be explicit about inputs and outputs:

**Bad:**
```python
instruction="Write something"
```

**Good:**
```python
instruction="""Read the outline: {blog_outline}
Write a 300-word blog post with sections 1, 2, and 3.
Use an engaging, conversational tone."""
```

### 4. Deterministic When Possible

Prefer Sequential/Parallel over LLM Orchestration when the workflow is known:

**When workflow is fixed:**
```python
# Use SequentialAgent (deterministic)
SequentialAgent(sub_agents=[step1, step2, step3])
```

**When workflow varies:**
```python
# Use LLM Orchestrator (dynamic)
Agent(tools=[AgentTool(option_a), AgentTool(option_b)])
```

### 5. Fail Fast with Validation

Add validation agents early in the pipeline:

```python
SequentialAgent(sub_agents=[
    input_validator,      # ← Fails fast if input is bad
    expensive_operation,  # Only runs if input is valid
    output_formatter
])
```

---

## 🏆 Summary: What You've Learned

### Technical Skills

✅ How to build multi-agent systems with ADK
✅ Four fundamental workflow patterns (LLM, Sequential, Parallel, Loop)
✅ How to use `output_key` for state management
✅ How to wrap agents with `AgentTool`
✅ How to compose patterns together (nesting)
✅ How to handle iterative refinement with loops
✅ How to create exit conditions for loops

### Architectural Understanding

✅ Why monolithic agents fail at scale
✅ The benefits of specialized agent teams
✅ When to use each workflow pattern
✅ How to design agent collaboration
✅ How data flows through multi-agent systems
✅ State management and session isolation
✅ Performance optimization strategies

### Design Patterns

✅ Single Responsibility Principle for agents
✅ Assembly line pattern (Sequential)
✅ Multi-tasking pattern (Parallel)
✅ Refinement cycle pattern (Loop)
✅ Dynamic routing pattern (LLM Orchestrator)
✅ Hybrid patterns (combining workflows)

---

## 🚀 What's Next?

You've mastered multi-agent **architecture**. You know how to design workflows and coordinate agent teams.

**Day 2** will teach you:
- **Custom Function Tools**: Write your own Python functions as agent tools
- **MCP Integration**: Connect to external services and APIs
- **Long-Running Operations**: Handle async tasks and background jobs
- **Production Patterns**: Error handling, logging, monitoring

You're building a complete skill set for production-grade agent systems!

---

## 📚 Appendix: Quick Reference

### Agent Types Cheat Sheet

```python
# 1. LLM Orchestrator (Dynamic)
root = Agent(
    tools=[AgentTool(agent_a), AgentTool(agent_b)]
)

# 2. Sequential (Fixed Order)
seq = SequentialAgent(
    sub_agents=[agent_a, agent_b, agent_c]
)

# 3. Parallel (Concurrent)
par = ParallelAgent(
    sub_agents=[agent_a, agent_b, agent_c]
)

# 4. Loop (Iterative)
loop = LoopAgent(
    sub_agents=[critic, refiner],
    max_iterations=3
)
```

### State Management Cheat Sheet

```python
# Writing to state
agent = Agent(output_key="my_key")
# After execution: session_state["my_key"] = agent_output

# Reading from state
agent = Agent(instruction="Use this data: {my_key}")
# Placeholder replaced with session_state["my_key"]

# Overwriting state (loops)
agent = Agent(output_key="current_draft")
# Each execution overwrites session_state["current_draft"]
```

### Pattern Selection Cheat Sheet

| Use Case | Pattern | Why |
|----------|---------|-----|
| Data pipeline (ETL) | Sequential | Order matters |
| Multi-API calls | Parallel | Independent, speed |
| Customer routing | LLM Orchestrator | Dynamic decisions |
| Content refinement | Loop | Iterative quality |
| Report generation | Sequential + Parallel | Hybrid approach |

---
