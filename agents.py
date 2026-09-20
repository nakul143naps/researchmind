from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url 
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

load_dotenv()

def get_setting(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st
        return st.secrets.get(name, default)
    except Exception:
        return default

# Model setup using OpenRouter
openrouter_api_key = get_setting("OPENROUTER_API_KEY") or get_setting("OPENAI_API_KEY")
if not openrouter_api_key:
    raise ValueError(
        "Missing OpenRouter credentials. Set OPENROUTER_API_KEY in your .env file "
        "or set OPENAI_API_KEY to the same value."
    )

llm = ChatOpenAI(
    model=get_setting("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct"),
    temperature=0,
    api_key=openrouter_api_key,
    base_url=get_setting("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
)

# 1st agent (Search Agent)
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="You are an expert web search assistant. Find recent, reliable, and detailed information for the user's query."
    )

# 2nd agent (Reader Agent)
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="You are a precise web scraping assistant. Extract deep and clean text content from target URLs."
    )

# Writer chain 
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic chain 
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()

# Keep older Streamlit Cloud configurations usable if they still point at this
# module instead of the actual UI entry point.
main_file = getattr(sys.modules.get("__main__"), "__file__", "")
if main_file and Path(main_file).resolve() == Path(__file__).resolve():
    import runpy

    runpy.run_path(str(Path(__file__).with_name("app.py")), run_name="__main__")