"""
Run the product launch planning with the given product data.
"""
import os
import streamlit as st
from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool
from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun
from pydantic import BaseModel
from src.utils import get_azure_llm


class DuckDuckGoSearchTool(BaseTool):
    name: str = "DuckDuckGo Search"
    description: str = "Useful to search the internet about a given topic and return relevant results using DuckDuckGo search engine"

    def _run(self, query: str) -> str:
        """
        Execute the search and return results.
        
        Args:
            query (str): The search query.
        
        Returns:
            str: The search results or an error message if the search fails.
        """
        try:
            search_tool = DuckDuckGoSearchRun()
            return search_tool.run(query)
        except Exception as e:
            return f"Search failed: {str(e)}"

class MarketResearchData(BaseModel):
    """Validates input."""
    target_demographics: str
    competitor_analysis: str
    key_findings: str

@st.cache_resource(show_spinner=False)
def create_product_launch_crew():
    """Create and return the product launch crew."""
    azure_llm = get_azure_llm()
    search_tool = DuckDuckGoSearchTool()
    scrape_tool = ScrapeWebsiteTool()
    
    market_researcher = Agent(
        role="Market Researcher",
        goal="Conduct thorough market research to identify target demographics and competitors.",
        tools=[search_tool, scrape_tool],
        verbose=True,
        backstory=(
            """Analytical and detail-oriented, you excel at gathering insights about the market,
            analyzing competitors, and identifying the best strategies to target the desired audience."""
        ),
        llm=azure_llm
    )
    
    content_creator = Agent(
        role='Content Creator',
        goal="Develop engaging content for the product launch, including blogs, social media posts, and videos.",
        tools=[search_tool, scrape_tool],
        verbose=True,
        backstory=(
            """Creative and persuasive, you craft content that resonates with the audience,
            driving engagement and excitement for the product launch."""
        ),
        llm=azure_llm
    )
    
    pr_outreach_specialist = Agent(
        role="PR and Outreach Specialist",
        goal="Reach out to influencers, media outlets, and key opinion leaders to promote the product launch.",
        tools=[search_tool, scrape_tool],
        verbose=True,
        backstory=(
            """With strong networking skills, you connect with influencers and media outlets to ensure
            the product launch gains maximum visibility and coverage."""
        ),
        llm=azure_llm
    )
    
    # Create tasks
    market_research_task = Task(
        description="Conduct market research for the {product_name} launch, focusing on target demographics and competitors.",
        expected_output="A detailed report on market research findings, including target demographics and competitor analysis.",
        human_input=False,
        output_json=MarketResearchData,
        output_file="market_research.json",
        agent=market_researcher
    )
    
    content_creation_task = Task(
        description="Create content for the {product_name} launch, including blog posts, social media updates, and promotional videos.",
        expected_output="A collection of content pieces ready for publication.",
        human_input=False,
        async_execution=False,
        output_file="content_plan.txt",
        agent=content_creator
    )
    
    pr_outreach_task = Task(
        description="Contact influencers, media outlets, and key opinion leaders to promote the {product_name} launch.",
        expected_output="A report on outreach efforts, including responses from influencers and media coverage.",
        async_execution=False,
        output_file="outreach_report.md",
        agent=pr_outreach_specialist
    )
    
    # Create crew
    crew = Crew(
        agents=[market_researcher, content_creator, pr_outreach_specialist],
        tasks=[market_research_task, content_creation_task, pr_outreach_task],
        verbose=True
    )
    
    return crew

def run_product_launch(product_data):
    """Run the product launch planning with the given product data."""
    crew = create_product_launch_crew()
    result = crew.kickoff(inputs=product_data)
    
    # Collect results
    results = {
        'result': result.raw,
        'files': {}
    }
    
    # Add file outputs if they exist
    files = ['market_research.json', 'content_plan.txt', 'outreach_report.md']
    for file in files:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                results['files'][file] = f.read()
    
    return results
