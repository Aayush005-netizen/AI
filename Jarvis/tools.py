import logging
import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from livekit.agents import function_tool, RunContext

# --- CORRECTED IMPORTS AND INITIALIZATION ---

# 1. UNIFIED IMPORTS: Both the tool and its wrapper should come from
#    'langchain_google_community'. This is the most critical change.
from langchain_google_community import GoogleSearchAPIWrapper, GoogleSearchRun

# 2. ENVIRONMENT VARIABLES: Ensure your API keys are set correctly.
#    Replace the placeholder with your actual Google API Key.
os.environ["GOOGLE_API_KEY"] = "AIzaSyBwaok5lHPK0zZHvsubSvqqcHqa__zg8zU"
os.environ["GOOGLE_CSE_ID"] = "7627ff4e316a7479d"  # The ID you found earlier

# 3. SIMPLIFIED INITIALIZATION: The new version of GoogleSearchRun does not
#    need the 'api_wrapper' to be passed in. It finds the keys automatically.
#    This resolves the TypeError.
search_wrapper = GoogleSearchAPIWrapper()
google_search_tool = GoogleSearchRun(api_wrapper=search_wrapper)
# --- END OF FIXES ---


@function_tool()
async def get_weather(
    context: RunContext,  # type: ignore
    city: str) -> str:
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}."


@function_tool()
async def search_web(
    context: RunContext,  # type: ignore
    query: str) -> str:
    """
    Search the web using Google Search.
    """
    try:
        results = google_search_tool.run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."

