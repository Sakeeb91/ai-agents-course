# AI Agents Course - Complete Project

> A comprehensive AI agent chat application built with Google's Agent Development Kit (ADK) and Gemini 2.5 Flash Lite, featuring multiple deployment options and beautiful custom UIs.

**Live Demo**: [Hugging Face Space](https://sakeeb-ai-agent-chat.hf.space)
**Repository**: [GitHub](https://github.com/Sakeeb91/ai-agents-course)

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

## Project Features

- **Multiple Deployment Options**: Flask web app, Gradio interface, and Hugging Face Spaces
- **Beautiful UI**: Orange-mauve gradient theme with glassmorphism effects
- **Rich Markdown Support**: Code highlighting, tables, lists, and more
- **Multi-Agent Architectures**: LLM orchestration, Sequential, and Parallel workflows
- **Production Ready**: Deployed and live on Hugging Face

## Applications

1. **Flask Web Chat** - Custom web interface (`web-chat/`)
2. **Gradio App** - Production Gradio interface (`app.py`)
3. **Multi-Agent App** - Advanced multi-agent demo (`app_multiagent.py`)

## Documentation

- [DAY_1A_LEARNINGS.md](DAY_1A_LEARNINGS.md) - Day 1A comprehensive guide
- [DAY_1B_LEARNINGS.md](DAY_1B_LEARNINGS.md) - Multi-agent architectures guide
- [GRADIO_DEPLOYMENT.md](GRADIO_DEPLOYMENT.md) - Deployment guide
- [CLAUDE.md](CLAUDE.md) - Complete session summary

## Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [Kaggle Course](https://www.kaggle.com/learn-guide/5-day-agents)
- [Live Demo](https://sakeeb-ai-agent-chat.hf.space)
- [GitHub Repository](https://github.com/Sakeeb91/ai-agents-course)
