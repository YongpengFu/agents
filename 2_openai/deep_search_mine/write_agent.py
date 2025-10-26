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

INSTRUCTIONS = """You are a senior researcher tasked with writing a cohesive, well-cited report for a research query.

You will be provided with:
- The original query
- Initial research from a research assistant (which includes summaries with source citations)

Your task:
1. Create an outline for the report describing structure and flow
2. Generate a comprehensive, well-cited report

IMPORTANT - Citations and References:
- Use inline citations throughout the report [1], [2], [3] format
- Extract all source URLs from the research provided
- Create a comprehensive "References" section at the END of your report
- List all sources in numbered format matching the inline citations
- Every factual claim should have a citation

Format requirements:
- Markdown format
- Lengthy and detailed (aim for 5-10 pages, at least 1000 words)
- Must end with a "## References" section listing all sources

Example:
According to recent studies [1], AI agents show significant promise [2].

## References
[1] https://example.com/study1
[2] https://example.com/article2
"""


class ReportData(BaseModel):
    short_summary: str = Field(
        description="A short 2-3 sentence summary of the findings.")

    markdown_report: str = Field(
        description="The final report in markdown format with inline citations and a References section at the end")

    sources: list[str] = Field(
        description="List of all source URLs referenced in the report")

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
