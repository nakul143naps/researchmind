# ResearchMind

ResearchMind is a Streamlit research assistant that searches the web, extracts useful content from candidate sources, writes a structured research report, and reviews it with a critic step.

## Features

- Web search using Tavily
- Source scraping and content extraction
- OpenRouter-powered research writing
- AI-based criticism and improvement feedback
- Streamlit UI for interactive research workflow

## Tech Stack

- Python 3.10+
- Streamlit
- LangChain
- LangChain OpenAI-compatible models
- Tavily API
- BeautifulSoup

## Project Structure

- app.py — Streamlit UI
- agents.py — model setup and research workflow agents/chains
- pipeline.py — terminal pipeline runner
- tools.py — Tavily search and URL scraping tools
- requirements.txt — Python dependencies
- .env.example — environment variable template

## Setup

1. Create a virtual environment

   python -m venv .venv

2. Activate the environment

   Windows PowerShell:
   .\.venv\Scripts\Activate.ps1

3. Install dependencies

   pip install -r requirements.txt

4. Create a local environment file

   Copy .env.example to .env and fill in your real API keys.

   Example:

   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct
   TAVILY_API_KEY=your_tavily_api_key_here

5. Run the app

   streamlit run app.py

## Notes

- Never commit your .env file to Git.
- The repository intentionally ignores .env and other .env.* files while keeping .env.example as a placeholder template.
- The project currently expects a valid OpenRouter API key and a Tavily API key to run successfully.

## Example Local Run

   .\.venv\Scripts\Activate.ps1
   streamlit run app.py

Then open the local URL shown by Streamlit, usually:

   http://localhost:8501

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub. Do not commit `.env`; it is ignored by Git.
2. Open [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Select the `researchmind` repository, the `clean-main` branch, and `app.py` as the main file.
4. In **Advanced settings → Secrets**, add:

   ```toml
   OPENROUTER_API_KEY = "your_openrouter_api_key"
   OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct"
   TAVILY_API_KEY = "your_tavily_api_key"
   ```

5. Click **Deploy**. Streamlit Cloud installs the packages from `requirements.txt`
   and provides the public app URL when startup completes.
