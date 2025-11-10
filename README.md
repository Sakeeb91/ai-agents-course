# Kaggle 5-Day AI Agents Course - Day 1A

## Completed Tasks ✅

### Day 1A: From Prompt to Action

You've successfully completed the following:

1. **Installed Google ADK** - The Agent Development Kit for building AI agents
2. **Configured Gemini API** - Set up authentication with your API key
3. **Built Your First Agent** - Created an agent with Google Search tool
4. **Ran Agent Queries** - Successfully tested with:
   - ADK information query (learned ADK supports Python, Java, Go)
   - Weather query (got current London weather: 13°C, light rain)
5. **Created Sample Agent** - Used `adk create` command to scaffold a new agent

## Files Created

- `day1a_first_agent.py` - Your first working AI agent script
- `sample-agent/` - ADK-generated agent template
  - `agent.py` - Agent definition
  - `.env` - Environment configuration
  - `__init__.py` - Python package file

## Running Your Agent

### Option 1: Using the Python Script
```bash
python3 day1a_first_agent.py
```

### Option 2: Using ADK CLI (from sample-agent directory)
```bash
cd sample-agent
adk run "What is AI?"
```

### Option 3: Using ADK Web Interface
```bash
cd sample-agent
adk web
# Then open http://localhost:8000 in your browser
```

## Key Learnings

### What is an AI Agent?
- Traditional LLM: `Prompt -> LLM -> Text`
- AI Agent: `Prompt -> Agent -> Thought -> Action -> Observation -> Final Answer`

### Agent Components
- **Model**: The LLM powering the agent (gemini-2.5-flash-lite)
- **Instruction**: Guiding prompt for agent behavior
- **Tools**: Capabilities the agent can use (like Google Search)
- **Runner**: Orchestrator that manages conversations

### Agent Behavior
Your agent can:
- Use Google Search for current information
- Reason about when to use tools
- Combine multiple sources of information
- Provide grounded, up-to-date answers

## Next Steps

Continue to Day 1B to learn about **architecting multi-agent systems**!

## Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Quickstart for Python](https://google.github.io/adk-docs/get-started/python/)
- [ADK Agents Overview](https://google.github.io/adk-docs/agents/)
- [ADK Tools Overview](https://google.github.io/adk-docs/tools/)
