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

INSTRUCTIONS = "You are a helpful research assistant. Given a search term, you search the web for that term and \
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 \
words. Capture the main points. Write succintly, no need to have complete sentences or good \
grammar. This will be consumed by someone synthesizing a report, so it's vital you capture the \
essence and ignore any fluff. Do not include any additional commentary other than the summary itself."

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
