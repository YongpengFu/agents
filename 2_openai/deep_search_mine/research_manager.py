from agents import Runner, trace, gen_trace_id
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from write_agent import writer_agent, ReportData
from email_agent import email_agent
from search_agent import search_agent
import asyncio
import logging
from dotenv import load_dotenv
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

logger.info("Loading environment variables")
load_dotenv(override=True)
logger.info("Environment variables loaded")
# print out the environment variables
for key, value in os.environ.items():
    logger.info(f"{key}: {value}")


class ResearchManager:
    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting research...")
            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting to search..."
            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, writing report..."
            report = await self.write_report(query, search_results)
            yield "Report written, sending email..."
            await self.send_email(report)
            yield "Email sent, research complete"
            yield report.markdown_report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Use the planner_agent to plan which searches to run for the query """
        print("Planning searches...")
        result = await Runner.run(planner_agent, f"Query: {query}")
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output

    async def search(self, item: WebSearchItem) -> str:
        """ Use the search agent to run a web search for each item in the search plan """
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        result = await Runner.run(search_agent, input)
        return result.final_output

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Call search() for each item in the search plan """
        print("Searching...")
        tasks = [asyncio.create_task(self.search(item))
                 for item in search_plan.searches]
        results = await asyncio.gather(*tasks)
        print("Finished searching")
        return results

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Use the writer agent to write a report based on the search results"""
        print("Thinking about report...")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(writer_agent, input)
        print("Finished writing report")
        return result.final_output

    async def send_email(self, report: ReportData) -> ReportData:
        """ Use the email agent to send an email with the report """
        print("Writing email...")
        result = await Runner.run(email_agent, report.markdown_report)
        print("Email sent")
        return report


async def main():
    query = "What are the latest trends in AI?"
    research_manager = ResearchManager()

    # Option 1: Iterate through all the yield statements
    # This will print progress updates and the final report
    async for status_or_report in research_manager.run(query):
        print(status_or_report)
        print("-" * 80)


if __name__ == "__main__":
    asyncio.run(main())
