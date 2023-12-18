# tulip-library-search
interactive streamlit app for searching tulip apps

## Running the streamlit App

- Hosted App: navigate to https://tulip-library-search.streamlit.app/ and enter the password to get started
- Running Locally:
    1.  Clone the github repository
    2. Navigate to the home directory
    3. Run the following command
    ```streamlit run streamlit/app.py```

## App Design Overview

**Purpose: Streamlit App is intended to be a high-level sandbox for exploring new ideas for Tulip Library search and discoverability**

Structure: App is segemnented into primary sections with top-level nav buttons
1. Library Search
2. Top Installs
3. Interactive Installation (WIP)
4. Performance Visibility Quick Start Guide (WIP)

### Library Search
This section explores the possibility of enabling an LLM-based search experience.
- A subset of library assets are included in a GPT3.5-turbo prompt with guidance on providing links to most relevant apps for installation.
- Moving forward, direct installation could also be a feature
- Feedback is noted on a separate postres database.

### Top Installs
- This page is simply the top ~50 library assets sorted by top installs rolling 90 days

