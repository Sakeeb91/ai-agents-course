#!/usr/bin/env python3
"""
Day 1A: From Prompt to Action
Your First AI Agent with Google ADK
"""

import os
import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search

# Set up API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY environment variable is required.\n"
        "Set it with: export GOOGLE_API_KEY=your-key"
    )

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

print("=" * 80)
print("🚀 Day 1A: Your First AI Agent - From Prompt to Action")
print("=" * 80)
print()

# Section 2.2: Define your agent
print("📝 Step 1: Defining the agent...")
root_agent = Agent(
    name="helpful_assistant",
    model="gemini-2.5-flash-lite",
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)
print("✅ Root Agent defined.")
print()

# Section 2.3: Run your agent
print("📝 Step 2: Creating the runner...")
runner = InMemoryRunner(agent=root_agent)
print("✅ Runner created.")
print()

async def run_agent_query(query):
    """Run a query with the agent and display the response."""
    print(f"🤔 Query: {query}")
    print("-" * 80)
    response = await runner.run_debug(query)
    print(f"💡 Response: {response}")
    print("-" * 80)
    print()

async def main():
    # First query from the course
    print("📝 Step 3: Running the agent with the course question...")
    print()
    await run_agent_query(
        "What is Agent Development Kit from Google? What languages is the SDK available in?"
    )

    # Section 2.5: Your Turn! - Custom question
    print("📝 Step 4: Testing with a current events question...")
    print()
    await run_agent_query("What's the weather in London?")

    print("=" * 80)
    print("✅ Congratulations! You've successfully run your first AI Agent!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
