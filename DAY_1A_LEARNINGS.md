# Day 1A: From Prompt to Action - Complete Learning Guide

## 🎯 Core Concept: What is an AI Agent?

### The Fundamental Difference

**Traditional LLM Interaction:**
```
User: "What's the weather in London?"
LLM: "I don't have access to real-time information. My knowledge was cut off in January 2025..."
```

**AI Agent Interaction:**
```
User: "What's the weather in London?"
Agent: [Thinks] "I need current information"
       [Acts] Uses Google Search tool
       [Observes] Gets weather data
       [Responds] "The weather in London is currently 13°C with light rain..."
```

### The Agent Loop: Think → Act → Observe → Respond

This is the **core paradigm shift** from passive LLMs to active agents:

1. **Think** - The agent analyzes the request and decides if it needs more information
2. **Act** - The agent uses available tools (Google Search, APIs, databases, etc.)
3. **Observe** - The agent processes the results from the tool
4. **Respond** - The agent synthesizes information into a final answer

---

## 🧩 Agent Architecture Components

### 1. The Agent Definition

```python
root_agent = Agent(
    name="helpful_assistant",
    model="gemini-2.5-flash-lite",
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)
```

**Breaking down each component:**

#### `name` - Agent Identity
- A unique identifier for your agent
- Important when building multi-agent systems (Day 1B topic)
- Helps in logging and debugging

#### `model` - The Brain
- The underlying LLM that powers reasoning
- `gemini-2.5-flash-lite` is optimized for speed and cost
- Other options: `gemini-2.5-flash`, `gemini-2.0-pro`, etc.
- The model determines:
  - Reasoning quality
  - Speed of responses
  - Cost per query
  - Context window size

#### `description` - Self-Documentation
- Helps other agents understand this agent's purpose
- Used in multi-agent systems for routing
- Acts as metadata for the agent

#### `instruction` - The Agent's Persona & Behavior
This is **crucial** - it defines:
- **Personality**: How the agent communicates
- **When to use tools**: "Use Google Search for current info or if unsure"
- **Constraints**: What the agent should/shouldn't do
- **Decision-making logic**: How to approach problems

**Example instruction variations:**

```python
# Conservative agent - rarely uses tools
instruction = "Only use Google Search if you are completely certain you don't know the answer."

# Proactive agent - frequently uses tools
instruction = "Always verify information with Google Search, even if you think you know the answer."

# Specialized agent
instruction = "You are a weather expert. Always use Google Search for weather queries and provide detailed forecasts."
```

#### `tools` - Agent Capabilities
- Tools are **functions the agent can call**
- In this course, you used `google_search`
- Tools can be:
  - Web search
  - Database queries
  - API calls
  - File operations
  - Custom Python functions
  - Other agents (multi-agent systems)

---

### 2. The Runner - The Orchestrator

```python
runner = InMemoryRunner(agent=root_agent)
```

**What the Runner does:**

#### Session Management
- Creates and maintains conversation sessions
- Tracks conversation history
- Manages state between turns

#### Execution Orchestration
- Routes user input to the agent
- Manages the Think → Act → Observe loop
- Handles tool execution
- Aggregates responses

#### Types of Runners

**`InMemoryRunner`** (what you used):
- Stores everything in memory
- Fast and simple
- Good for:
  - Prototyping
  - Testing
  - Single-session use
- Lost when program ends

**Other runner types** (you'll learn later):
- **Persistent Runners**: Save sessions to database
- **Distributed Runners**: Run agents across multiple machines
- **Production Runners**: Handle scaling, monitoring, logging

---

### 3. Running Queries

```python
response = await runner.run_debug("What is Agent Development Kit from Google?")
```

**Understanding `run_debug()`:**

#### Why "debug"?
- Abstracts session management (creates sessions automatically)
- Perfect for prototyping and learning
- In production, you'd use explicit session management

#### The `await` keyword
- ADK uses **async/await** (asynchronous programming)
- Why? Tools might take time (API calls, web searches)
- Async allows handling multiple requests simultaneously
- **Async pattern:**
  ```python
  async def main():
      response = await runner.run_debug("query")

  asyncio.run(main())
  ```

#### What happens internally:
1. Runner creates/finds a session
2. Sends query to the agent
3. Agent (Gemini model) decides: "Do I need tools?"
4. If yes → Execute tool → Get results → Synthesize answer
5. If no → Answer directly from knowledge
6. Return response to user

---

## 🔧 How Tools Work

### The Google Search Tool

When you added `tools=[google_search]`:

```python
from google.adk.tools import google_search
```

**What happens under the hood:**

1. **Tool Declaration**: The agent knows it has access to a search function
2. **Tool Schema**: The agent knows how to call it (what parameters it accepts)
3. **Decision Making**: Based on the query, the agent decides whether to use it
4. **Execution**: If needed, ADK calls the actual Google Search API
5. **Result Processing**: The search results are fed back to the agent
6. **Synthesis**: The agent combines search results with its knowledge

### Example Tool Execution Flow

**Your query:** "What is Agent Development Kit from Google? What languages is the SDK available in?"

**Agent's internal reasoning:**
```
1. Analyze query: User wants current info about Google ADK
2. Check knowledge: I might have outdated info
3. Decision: USE google_search tool
4. Search query: "Google Agent Development Kit SDK languages"
5. Results received: [web pages about ADK]
6. Extract info: Python, Java, Go mentioned
7. Synthesize: Combine search results into coherent answer
8. Respond with grounded information
```

**Grounding Metadata:**
Notice in the output you saw `grounding_metadata` - this shows:
- Which web sources were used
- How the agent supports its claims
- Links to original sources
- This ensures **transparency** and **verifiability**

---

## 📊 Understanding the Response Object

When you ran the agent, you got back an `Event` object with rich metadata:

```python
Event(
    model_version='gemini-2.5-flash-lite',
    content=Content(...),              # The actual response text
    grounding_metadata=GroundingMetadata(...),  # Sources used
    usage_metadata=UsageMetadata(...),  # Token usage stats
    finish_reason='STOP',               # Why response ended
    ...
)
```

### Key Response Components:

#### 1. **Content** - The Answer
The actual text response from the agent

#### 2. **Grounding Metadata** - The Sources
- `grounding_chunks`: Web pages/sources used
- `grounding_supports`: Which parts of the answer came from which sources
- `search_entry_point`: Google search UI with related queries
- This is **crucial for trust** - you can verify the agent's claims

#### 3. **Usage Metadata** - Cost & Performance
```python
usage_metadata=GenerateContentResponseUsageMetadata(
    candidates_token_count=161,      # Output tokens
    prompt_token_count=64,           # Input tokens
    tool_use_prompt_token_count=87,  # Tokens used for tool calling
    total_token_count=312            # Total (affects cost)
)
```

**Why this matters:**
- Tokens = Cost (you pay per token)
- Understanding usage helps optimize:
  - Agent instructions (shorter = cheaper)
  - Tool usage (tools add tokens)
  - Response length

#### 4. **Finish Reason**
- `STOP`: Natural completion
- `MAX_TOKENS`: Hit token limit
- `SAFETY`: Content filtered
- `RECITATION`: Potential copyright issue

---

## 🎓 Key Learning Concepts

### 1. Agentic Behavior vs Direct Response

**Non-Agentic (Traditional LLM):**
- One-shot input → output
- No external information
- Static knowledge
- Can't verify or update info

**Agentic (What You Built):**
- Can seek information
- Uses tools to gather data
- Verifies and grounds responses
- Adapts to current information

### 2. Tool Use is Decision-Based

The agent **decides** when to use tools based on:
- The instruction you provided
- The nature of the query
- Its confidence in existing knowledge
- Whether the query needs current data

**This is different from:**
- Hardcoded if/else logic
- Rule-based systems
- The LLM itself makes intelligent decisions

### 3. Grounding = Trust

**Grounding** means the agent's response is backed by sources:
- You can verify claims
- Reduces hallucination
- Provides transparency
- Increases trust in AI systems

### 4. Composability

Agents are **composable** - you can:
- Add more tools
- Chain multiple agents
- Build complex workflows
- Create specialized agent teams

This sets up **Day 1B**: Multi-agent systems

---

## 🔬 Deep Dive: What Happened When You Ran Your Agent

### Query 1: "What is Agent Development Kit from Google? What languages is the SDK available in?"

**Step-by-step execution:**

1. **User Input Received**
   - Runner receives your query
   - Creates/continues session: `debug_session_id`

2. **Agent Analysis**
   - Gemini model processes the query
   - Identifies: This needs current, specific information
   - Decision: "I should use Google Search"

3. **Tool Execution**
   - ADK calls `google_search` tool
   - Search query: "Google Agent Development Kit SDK languages"
   - Google returns web results

4. **Result Processing**
   - Agent receives search results
   - Extracts relevant information:
     - ADK is an open-source framework
     - Designed for AI agents and multi-agent systems
     - Available in Python, Java, Go
     - Optimized for Gemini models

5. **Response Synthesis**
   - Combines information from multiple sources
   - Structures answer clearly
   - Adds grounding metadata
   - Returns to user

6. **Token Accounting**
   - Input: 64 tokens (your question)
   - Tool use: 87 tokens (search execution)
   - Output: 161 tokens (the response)
   - Total: 312 tokens

### Query 2: "What's the weather in London?"

**Why this is interesting:**

1. **Temporal Awareness**
   - Agent knows it needs **current** data
   - Weather changes constantly
   - Static knowledge won't work

2. **Automatic Tool Selection**
   - No explicit instruction to "search for weather"
   - Agent infers this from the instruction: "Use Google Search for current info"
   - This is **intelligent tool use**

3. **Structured Data Extraction**
   - Gets weather search results
   - Extracts: Temperature, conditions, forecast
   - Formats into readable response
   - Includes multi-day forecast

4. **Verification**
   - Grounding shows source: Google weather widget
   - You can verify by searching yourself
   - This prevents hallucination

---

## 🏗️ The ADK Project Structure

When you ran `adk create sample-agent`, it generated:

### File: `agent.py`
```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
```

**This is the core agent definition**
- Minimal, focused
- Easy to modify and extend
- Production-ready structure

### File: `.env`
```
GOOGLE_API_KEY=your_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

**Environment configuration**
- Keeps secrets separate from code
- Never commit `.env` to git
- Different configs for dev/staging/prod

### File: `__init__.py`
```python
from .agent import *
```

**Makes it a Python package**
- Allows importing: `from sample_agent import root_agent`
- Enables module structure
- Supports scaling to larger projects

---

## 🚀 ADK Development Workflow

### Three Ways to Run Agents:

#### 1. **Python Script** (What you did)
```python
import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(agent=root_agent)
response = await runner.run_debug("query")
```

**Pros:**
- Full programmatic control
- Easy to integrate into larger apps
- Good for batch processing

**Cons:**
- Need to write async code
- Manual session management
- Less interactive

#### 2. **ADK CLI**
```bash
adk run sample-agent
```

**Pros:**
- Quick testing
- Interactive mode
- No code needed

**Cons:**
- Less control
- Basic features only

#### 3. **ADK Web UI**
```bash
adk web
```

**Pros:**
- Beautiful interface
- Detailed trace logs
- See agent reasoning
- Debug tool calls
- Monitor performance

**Cons:**
- Requires running server
- Not for production
- Single-user only

---

## 💡 Key Insights & Design Patterns

### 1. Instruction Engineering

The `instruction` parameter is like **prompt engineering for agents**:

**Bad instruction:**
```python
instruction = "Be helpful."
```
- Too vague
- Agent won't know when to use tools
- Inconsistent behavior

**Good instruction:**
```python
instruction = """
You are a helpful assistant specialized in current events.
Always use Google Search for:
- News and recent events
- Weather information
- Sports scores and results
- Any time-sensitive information

Only answer from your knowledge if the user asks about:
- Historical facts
- General knowledge
- Explanations of concepts
"""
```
- Clear guidelines
- Specific tool usage rules
- Predictable behavior

### 2. Tool Selection Strategy

**Conservative (Faster, Cheaper):**
```python
instruction = "Only use tools if absolutely necessary."
```

**Aggressive (More Accurate, Slower):**
```python
instruction = "Always verify answers with tools when available."
```

**Balanced (What you used):**
```python
instruction = "Use Google Search for current info or if unsure."
```

### 3. Model Selection Tradeoffs

| Model | Speed | Cost | Quality | Use Case |
|-------|-------|------|---------|----------|
| gemini-2.5-flash-lite | ⚡⚡⚡ | $ | ⭐⭐ | Quick queries, high volume |
| gemini-2.5-flash | ⚡⚡ | $$ | ⭐⭐⭐ | General purpose |
| gemini-2.0-pro | ⚡ | $$$ | ⭐⭐⭐⭐ | Complex reasoning |

---

## 🎯 What Makes This "Agentic"?

### Traditional Approach (Non-Agentic):
```python
# Hardcoded logic
if "weather" in query:
    result = weather_api.get_weather()
elif "news" in query:
    result = news_api.get_news()
else:
    result = llm.generate(query)
```

**Problems:**
- Brittle rule-based logic
- Can't handle edge cases
- Requires updating code for new scenarios
- No reasoning, just pattern matching

### Agentic Approach (What You Built):
```python
# Agent decides
agent = Agent(
    instruction="Use tools when you need current information",
    tools=[google_search, weather_api, news_api]
)
# Agent intelligently chooses which tool (if any) to use
```

**Advantages:**
- Agent reasons about tool selection
- Handles novel scenarios
- Adapts to query nuances
- No code changes needed for new queries
- Can combine multiple tools intelligently

---

## 🔮 What's Next? (Preview of Day 1B)

You've built a **single agent**. But real-world systems often need **multiple agents**:

### Multi-Agent Systems:
- **Specialist Agents**: Each handles specific domains
- **Router Agent**: Directs queries to the right specialist
- **Coordinator Agent**: Manages complex multi-step tasks
- **Verification Agent**: Checks other agents' work

**Example multi-agent workflow:**
```
User: "Plan a trip to Paris with weather considerations"

Router Agent → Determines this needs multiple specialists
    ↓
Travel Agent → Finds flights and hotels
    ↓
Weather Agent → Gets Paris forecast
    ↓
Coordinator Agent → Combines information
    ↓
Final Response: Integrated travel plan with weather info
```

This is what you'll learn in **Day 1B: Architecting Multi-Agent Systems**!

---

## 📚 Summary: What You Truly Learned

### Technical Skills:
✅ How to install and configure Google ADK
✅ How to define an AI agent with tools
✅ How to use the Runner pattern for orchestration
✅ How to execute agent queries asynchronously
✅ How to read and interpret agent responses
✅ How to use ADK CLI for project scaffolding

### Conceptual Understanding:
✅ The difference between LLMs and AI Agents
✅ The Think → Act → Observe → Respond loop
✅ How agents make decisions about tool usage
✅ What grounding means and why it matters
✅ How to design agent instructions
✅ Token usage and cost implications

### Software Engineering:
✅ Async/await patterns in Python
✅ Environment variable management
✅ Project structure and organization
✅ Session management concepts
✅ API key security practices

### AI/LLM Concepts:
✅ Tool calling and function execution
✅ Prompt engineering for agents
✅ Model selection criteria
✅ Grounding and source attribution
✅ Token counting and optimization

---

## 🎓 Advanced Topics (For Deeper Understanding)

### How Does the Agent "Decide" to Use Tools?

The LLM (Gemini) receives a **tool specification** in a special format:

```json
{
  "name": "google_search",
  "description": "Searches Google for current information",
  "parameters": {
    "query": "string - the search query"
  }
}
```

The model's training allows it to:
1. Understand it has access to this function
2. Recognize queries that need it
3. Generate a **function call** instead of text
4. Process the function results
5. Synthesize the final response

This is called **function calling** or **tool use** and is a special capability of modern LLMs.

### Grounding vs Hallucination

**Hallucination**: When LLMs generate plausible but false information
```
User: "Who won the 2024 Nobel Prize in Physics?"
LLM: "Dr. Jane Smith won for her work on quantum computing."
# This might be completely made up!
```

**Grounding**: Agent backs up claims with sources
```
User: "Who won the 2024 Nobel Prize in Physics?"
Agent: [Searches web] "According to nobelprize.org,
        John Hopfield and Geoffrey Hinton won for discoveries
        enabling machine learning with artificial neural networks."
Sources: [links to nobelprize.org]
# Verifiable and accurate!
```

### Why Async/Await?

**Synchronous (blocking):**
```python
response1 = agent.run("query 1")  # Wait 5 seconds
response2 = agent.run("query 2")  # Wait 5 seconds
# Total: 10 seconds
```

**Asynchronous (non-blocking):**
```python
response1, response2 = await asyncio.gather(
    agent.run("query 1"),  # Both run simultaneously
    agent.run("query 2")
)
# Total: 5 seconds (parallelized!)
```

This matters for:
- Building fast UIs
- Handling multiple users
- Scaling to production
- Efficient resource usage

---

## 🏆 Congratulations!

You've not just run some code - you've learned the **foundational architecture of modern AI agents**. This same pattern powers:

- **Customer service chatbots** that look up account info
- **Research assistants** that search papers and databases
- **Code assistants** that run tests and check documentation
- **Multi-agent systems** that coordinate complex tasks

The concepts you learned today are the building blocks for all agent-based AI systems!

**Keep going - Day 1B awaits! 🚀**
