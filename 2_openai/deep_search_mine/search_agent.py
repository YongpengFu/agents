from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
from agents.model_settings import ModelSettings
from pydantic import BaseModel, Field
import os
import asyncio
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

logger.info("Loading environment variables")
load_dotenv(override=True)
logger.info("Environment variables loaded")
# print out the environment variables
for key, value in os.environ.items():
    logger.info(f"{key}: {value}")

INSTRUCTIONS = """You are a helpful research assistant. Given a search term, you search the web for that term and 
produce a concise summary of the results with proper citations.

Your output should:
1. Provide a 2-3 paragraph summary (less than 300 words) capturing the main points
2. Include inline citations using [1], [2], [3] format
3. End with a "Sources:" section listing all referenced URLs
4. Write succinctly - this will be consumed by someone synthesizing a larger report

Format example:
According to recent research [1], AI agents are becoming more sophisticated. The market is expected to grow significantly [2].

Sources:
[1] https://example.com/article1
[2] https://example.com/article2
"""

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)


def get_search_agent():
    logger.info("Getting search agent")
    return search_agent


async def search(query: str):
    logger.info(f"Searching for: {query}")
    result = await Runner.run(get_search_agent(), query)
    logger.info(f"Search result: {result.final_output}")
    return result.final_output


async def main():
    query = "Latest AI Agent frameworks in 2025"
    result = await search(query)
    logger.info(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
