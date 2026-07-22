# Intelligence Hub

A GitHub-based developer intelligence platform that analyzes developer activity and creates an evidence-based profile from real GitHub data.

Intelligence Hub collects repository information, programming languages, activity patterns, and contribution data to generate a developer overview with insights about coding habits and project presence.

---

## Features

## GitHub Profile Analysis

- Fetches developer information using GitHub API
- Analyzes public repositories
- Tracks stars, forks, languages, and repository activity
- Collects contribution and event data

## Developer Snapshot

Generates an overview containing:

- Repository count
- Original projects
- Stars received
- Fork activity
- Programming language usage

## Repository Intelligence

Analyzes repositories using:

- Repository metadata
- README availability
- Documentation signals
- Topics
- Project details

## Developer DNA Analysis

Creates an experimental scoring system based on GitHub activity patterns:

- Momentum
- Discipline
- Craft
- Influence
- Insight
- Resolve

Scores are generated from available GitHub evidence and are used for developer profile visualization.

## Repository Explorer

Allows users to explore repositories with:

- Repository cards
- Language information
- Stars and forks
- Direct GitHub links

---

# Tech Stack

## Backend

- Python
- FastAPI
- Jinja2 Templates

## APIs

- GitHub REST API
- GitHub GraphQL API

## Frontend

- HTML
- CSS
- Vanilla JavaScript

## Data Processing

- Requests
- Python data processing modules

---

# Project Structure

INTELLIGENCE-HUB/

├── modules/
│   ├── __init__.py
│   ├── github.py
│   ├── graphql.py
│   ├── collector.py
│   ├── fast_collector.py
│   └── analysis.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── templates/
│   ├── index.html
│   ├── profile.html
│   └── repo.html
│
├── config.py
├── main.py
├── requirements.txt
├── LICENSE
└── README.md

---


# Installation

Clone the repository:

```bash
git clone https://github.com/Unrealreally/Intelligence-Hub.git
```

Move into the project directory:

```bash
cd Intelligence-Hub
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Setup

Create a `.env` file in the root directory.

Example:

```env
GITHUB_TOKEN=your_github_token
GITHUB_GRAPHQL_TOKEN=your_github_graphql_token
```

The application uses GitHub API tokens to collect profile and repository data.

Keep your `.env` file private and do not upload it publicly.

---

# Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The application will run at:

```
http://127.0.0.1:8000
```

---

# Application Flow

## 1. Profile Collection

The application collects:

- GitHub user information
- Public repositories
- Repository metadata
- Programming languages
- Contribution activity

## 2. Repository Analysis

Repositories are processed using available repository data:

- Project information
- README presence
- Documentation signals
- Repository activity

## 3. Developer Analysis

Collected data is passed through analysis modules to generate developer insights:

- Momentum
- Discipline
- Craft
- Influence
- Insight
- Resolve

## 4. Visualization

The processed data is displayed through:

- Developer snapshot cards
- Repository intelligence cards
- Language statistics
- Developer DNA visualization

---

# API Usage

## GitHub REST API

Used for:

- User information
- Repository data
- Events
- Languages

## GitHub GraphQL API

Used for:

- Contribution data
- Additional profile information

---

# Notes

- Intelligence Hub analyzes publicly available GitHub information.
- Developer DNA scores are experimental metrics based on available activity data.
- Scores are not official measurements of programming ability.

---

# Future Improvements

Possible future improvements:

- Better repository analysis
- More detailed developer insights
- Improved scoring methods
- Additional visualization features

---

# License

This project is licensed under the MIT License.