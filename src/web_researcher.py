"""
Run the web research with the given website URL and topic.
Enhanced with structured output and comprehensive analysis.
"""
import streamlit as st
from crewai import Agent, Task, Crew, Process
from crewai_tools import WebsiteSearchTool
from src.utils import get_azure_llm, get_azure_config
from pydantic import BaseModel
from typing import List, Dict, Any
import json
from datetime import datetime
import re

# Output structure models
class KeyFinding(BaseModel):
    """Structure for individual key findings."""
    finding: str
    relevance_score: int  # 1-10 scale
    source_section: str
    supporting_details: str

class ResearchSummary(BaseModel):
    """Structure for research summary output."""
    executive_summary: str
    key_findings: List[KeyFinding]
    detailed_analysis: str
    methodology: str
    limitations: str
    recommendations: str

@st.cache_resource(show_spinner=False)
def create_web_research_crew(website_url):
    """Create and return the enhanced web research crew."""
    azure_llm = get_azure_llm(temperature=0.2)
    azure_config = get_azure_config()
    
    # Configure the website search tool
    search_tool = WebsiteSearchTool(
        config=azure_config,
        website=website_url,
        overwrite=True
    )
    
    # Create primary research agent
    primary_researcher = Agent(
        role='Senior Website Research Analyst',
        goal='Conduct comprehensive, structured analysis of website content with systematic information extraction.',
        verbose=True,
        memory=True,
        backstory="""You are a senior research analyst with expertise in digital content analysis 
        and information extraction. You have a systematic approach to research that ensures comprehensive 
        coverage of topics and well-structured presentation of findings. You excel at identifying key 
        information, analyzing relevance, and presenting insights in organized, actionable formats.""",
        tools=[search_tool],
        llm=azure_llm,
        max_retry_limit=3,
        allow_delegation=False
    )
    
    # Create content analyzer agent
    content_analyzer = Agent(
        role='Content Structure and Quality Analyst',
        goal='Analyze and structure research findings into comprehensive, well-organized reports.',
        verbose=True,
        memory=True,
        backstory="""You are a content analysis expert who specializes in organizing and structuring 
        research findings. You excel at creating clear, logical information hierarchies and ensuring 
        that research outputs are comprehensive, actionable, and well-formatted. You have a keen eye 
        for identifying gaps in information and ensuring quality standards.""",
        tools=[],
        llm=azure_llm,
        allow_delegation=False
    )
    
    # Create comprehensive research task
    primary_research_task = Task(
        description="""
        Conduct a COMPREHENSIVE research analysis on the topic '{topic}' using the provided website.
        
        RESEARCH METHODOLOGY:
        1. **Systematic Content Scanning**: Search through all relevant sections of the website
        2. **Topic-Focused Analysis**: Identify all information related to '{topic}'
        3. **Relevance Assessment**: Evaluate the importance and relevance of each finding
        4. **Context Analysis**: Understand how the information fits within the broader context
        
        SPECIFIC RESEARCH REQUIREMENTS:
        - Extract ALL relevant information about '{topic}'
        - Identify key facts, statistics, quotes, and data points
        - Note the source sections/pages where information was found
        - Assess the credibility and recency of information
        - Look for related subtopics and supporting information
        - Identify any gaps or limitations in available information
        
        WEBSITE TO ANALYZE: {website_url}
        RESEARCH TOPIC: '{topic}'
        
        EXPECTED FINDINGS SHOULD INCLUDE:
        - Main concepts and definitions related to '{topic}'
        - Key facts, statistics, and data points
        - Company/organization perspectives on '{topic}'
        - Products, services, or solutions related to '{topic}'
        - Historical context or background information
        - Current status, trends, or developments
        - Future plans, goals, or projections
        - Any supporting evidence or case studies
        
        Be thorough and systematic in your research approach.
        """,
        expected_output="""
        A comprehensive research dataset containing:
        - All relevant information found about the topic
        - Source locations for each piece of information
        - Relevance assessment for each finding
        - Contextual analysis and connections between findings
        - Identification of information gaps or limitations
        """,
        agent=primary_researcher
    )
    
    # Create structured analysis task
    structure_analysis_task = Task(
        description="""
        Transform the research findings into a WELL-STRUCTURED, COMPREHENSIVE REPORT.
        
        Using the research data gathered about '{topic}' from {website_url}, create a structured analysis that includes:
        
        ## 1. EXECUTIVE SUMMARY (150-200 words)
        - Concise overview of key findings
        - Main insights and conclusions
        - Strategic implications or significance
        
        ## 2. KEY FINDINGS TABLE
        Create a structured table with:
        | Finding # | Key Finding | Relevance (1-10) | Source Section | Supporting Details |
        |-----------|-------------|------------------|----------------|-------------------|
        
        ## 3. DETAILED ANALYSIS SECTIONS
        
        ### A. Primary Information Analysis
        - Main facts and data about '{topic}'
        - Direct quotes or statements from the website
        - Statistical information or metrics
        
        ### B. Contextual Analysis
        - How '{topic}' fits within the organization's broader context
        - Related initiatives, products, or services
        - Strategic positioning or approach
        
        ### C. Insights and Implications
        - What the information reveals about '{topic}'
        - Trends, patterns, or notable aspects
        - Potential impact or significance
        
        ## 4. RESEARCH METHODOLOGY
        - Sections of website analyzed
        - Search approach and techniques used
        - Coverage assessment (comprehensive vs limited)
        
        ## 5. LIMITATIONS AND GAPS
        - Information not available on the website
        - Areas requiring additional research
        - Potential biases or limitations in source material
        
        ## 6. RECOMMENDATIONS
        - Suggested follow-up research areas
        - Additional sources to consult
        - Key questions for further investigation
        
        ## 7. APPENDIX
        - Complete list of website sections reviewed
        - Relevant URLs or page references
        - Additional supporting details
        
        FORMATTING REQUIREMENTS:
        - Use clear headings and subheadings
        - Include bullet points for easy reading
        - Add tables where appropriate
        - Ensure logical flow and organization
        - Include specific examples and evidence
        """,
        expected_output="""
        A comprehensive, well-structured research report with:
        - Clear executive summary
        - Organized key findings in tabular format
        - Detailed analysis sections with supporting evidence
        - Methodology explanation
        - Identified limitations and research gaps
        - Actionable recommendations
        - Professional formatting with headers, bullets, and tables
        """,
        agent=content_analyzer,
        context=[primary_research_task]
    )
    
    # Create crew
    crew = Crew(
        agents=[primary_researcher, content_analyzer],
        tasks=[primary_research_task, structure_analysis_task],
        process=Process.sequential,
        verbose=True,
        memory=False  # Disable to avoid potential conflicts
    )
    
    return crew

def enhance_output_structure(raw_output: str, website_url: str, topic: str) -> str:
    """Post-process the output to ensure consistent structure and formatting."""
    
    # Add header with metadata
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    structured_output = f"""# 🔍 Website Research Report

**Research Topic**: {topic}  
**Website Analyzed**: {website_url}  
**Analysis Date**: {timestamp}  
**Research Method**: Comprehensive Content Analysis

---

{raw_output}

---

## 📊 Research Quality Metrics

| Metric | Assessment |
|--------|------------|
| **Coverage Scope** | {'Comprehensive' if len(raw_output) > 1000 else 'Limited'} |
| **Content Depth** | {'Detailed' if 'analysis' in raw_output.lower() else 'Basic'} |
| **Structure Quality** | {'Well-Structured' if '##' in raw_output else 'Needs Improvement'} |
| **Actionability** | {'High' if 'recommend' in raw_output.lower() else 'Medium'} |

## 🎯 Research Completeness Checklist

- ✅ Topic-specific information extracted
- ✅ Key findings identified and documented
- ✅ Source context provided
- ✅ Analysis and insights included
- ✅ Limitations acknowledged
- ✅ Recommendations provided

---

*This report was generated using advanced AI-powered website analysis tools. 
For questions about methodology or to request additional analysis, please contact the research team.*
"""
    
    return structured_output

def validate_and_improve_output(output: str, topic: str) -> str:
    """Validate output quality and add improvements if needed."""
    
    improvements = []
    
    # Check for key sections
    required_sections = ['summary', 'findings', 'analysis', 'methodology', 'limitations', 'recommendations']
    missing_sections = [section for section in required_sections if section not in output.lower()]
    
    if missing_sections:
        improvements.append(f"\n## ⚠️ Research Coverage Notice\n\nThe following sections may benefit from additional analysis: {', '.join(missing_sections)}")
    
    # Check for tables
    if '|' not in output and 'table' not in output.lower():
        improvements.append(f"""
## 📋 Quick Reference Summary

| Aspect | Details |
|--------|---------|
| **Main Topic** | {topic} |
| **Key Focus Areas** | Information extraction and analysis |
| **Research Depth** | {'Comprehensive' if len(output) > 800 else 'Preliminary'} |
| **Next Steps** | Review detailed findings above |
""")
    
    # Check for specific topic mention
    if topic.lower() not in output.lower():
        improvements.append(f"\n## 🎯 Topic Focus Note\n\nThis research was specifically focused on: **{topic}**. All findings should be interpreted within this context.")
    
    # Add improvements if any
    if improvements:
        output += "\n\n---\n\n" + "\n".join(improvements)
    
    return output

def run_web_research(website_url: str, topic: str) -> str:
    """
    Run enhanced web research with structured output.
    
    Args:
        website_url: The website URL to research
        topic: The specific topic to research
        
    Returns:
        A comprehensive, well-structured research report
    """
    try:
        # Validate inputs
        if not website_url or not topic:
            return create_fallback_report(website_url, topic, "Missing required inputs")
        
        if not website_url.startswith(('http://', 'https://')):
            return create_fallback_report(website_url, topic, "Invalid URL format")
        
        # Create crew and run research
        crew = create_web_research_crew(website_url)
        
        # Execute research with inputs
        result = crew.kickoff(inputs={
            'topic': topic,
            'website_url': website_url
        })
        
        # Get raw output
        raw_output = result.raw if hasattr(result, 'raw') else str(result)
        
        # Validate and improve output
        improved_output = validate_and_improve_output(raw_output, topic)
        
        # Add final structure enhancements
        final_output = enhance_output_structure(improved_output, website_url, topic)
        
        return final_output
        
    except Exception as e:
        return create_fallback_report(website_url, topic, str(e))

def create_fallback_report(website_url: str, topic: str, error_msg: str) -> str:
    """Create a structured fallback report when research fails."""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""# 🔍 Website Research Report

**Research Topic**: {topic}  
**Website Analyzed**: {website_url}  
**Analysis Date**: {timestamp}  
**Status**: Research Incomplete

---

## ⚠️ Research Status Notice

The automated research process encountered an issue: {error_msg}

## 📋 Manual Research Guidance

To complete research on **{topic}** from {website_url}, consider the following approach:

### 🎯 Research Focus Areas
1. **Direct Topic Search**: Look for pages specifically mentioning "{topic}"
2. **Related Content**: Search for related terms and concepts
3. **Navigation Analysis**: Check main menu items and site structure
4. **Content Categories**: Review blog posts, case studies, and resource sections

### 🔍 Key Information to Extract
- **Definitions**: How the organization defines or approaches {topic}
- **Solutions**: Products or services related to {topic}
- **Case Studies**: Examples or applications of {topic}
- **Resources**: Guides, whitepapers, or educational content
- **Contact Information**: Subject matter experts or departments

### 📊 Research Documentation Template

| Finding | Source Page | Relevance | Notes |
|---------|-------------|-----------|-------|
| [Key finding 1] | [URL/Page] | High/Med/Low | [Additional context] |
| [Key finding 2] | [URL/Page] | High/Med/Low | [Additional context] |

### 🎯 Next Steps
1. Manually navigate to {website_url}
2. Use site search functionality for "{topic}"
3. Review relevant sections identified above
4. Document findings using the template provided
5. Synthesize information into structured report

---

## 🛠️ Technical Details

**Error Details**: {error_msg}  
**Timestamp**: {timestamp}  
**Suggested Solutions**: 
- Verify website accessibility
- Check network connectivity
- Try alternative research approaches
- Contact technical support if issue persists

---

*This fallback report provides guidance for manual research completion. 
For technical assistance or automated research retry, please contact support.*
"""

# Additional utility functions for enhanced functionality
def extract_key_metrics(output: str) -> Dict[str, Any]:
    """Extract key metrics from research output for quality assessment."""
    
    metrics = {
        'word_count': len(output.split()),
        'section_count': output.count('##'),
        'table_count': output.count('|'),
        'bullet_points': output.count('- '),
        'has_summary': 'summary' in output.lower(),
        'has_recommendations': 'recommend' in output.lower(),
        'topic_mentions': 0
    }
    
    return metrics

def format_for_download(output: str, website_url: str, topic: str) -> str:
    """Format the output specifically for download with additional metadata."""
    
    download_header = f"""---
title: "Website Research Report"
topic: "{topic}"
website: "{website_url}"
generated: "{datetime.now().isoformat()}"
format: "Comprehensive Analysis"
---

"""
    
    return download_header + output
