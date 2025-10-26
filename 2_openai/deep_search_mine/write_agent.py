from pydantic import BaseModel, Field
from agents import Agent
from agents import Runner

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

INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words."
)


class ReportData(BaseModel):
    short_summary: str = Field(
        description="A short 2-3 sentence summary of the findings.")

    markdown_report: str = Field(description="The final report")

    follow_up_questions: list[str] = Field(
        description="Suggested topics to research further")


writer_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)


def get_writer_agent():
    return writer_agent


async def write_report(query: str, research: str):
    """ Use the writer_agent to write a report for the query """
    input = f"Query: {query}\nResearch: {research}"
    result = await Runner.run(writer_agent, input)
    logger.info("Finished writing report")
    logger.info(f"Report: {result.final_output}")
    return result.final_output


async def main():
    query = "What are the latest trends in AI?"
    research = "The latest trends in AI are: 1. LangGraph 2. CrewAI 3. AutoGen"
    report = await write_report(query, research)
    print(report)

if __name__ == "__main__":
    asyncio.run(main())
