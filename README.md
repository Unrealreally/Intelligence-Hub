# Intelligence Hub

A GitHub-based developer intelligence platform that analyzes developer activity and creates an evidence-based developer profile from real GitHub data.

Intelligence Hub collects repository information, programming languages, activity patterns, and contribution data to generate insights about coding habits, project presence, and development patterns.

---

# Features

## GitHub Profile Analysis

Fetches and analyzes developer information using GitHub APIs.

Includes:

- Public profile information
- Repository analysis
- Programming language usage
- Stars and forks
- Repository activity
- Contribution activity

---

## Developer Snapshot

Generates a developer overview containing:

- Repository count
- Original projects
- Stars received
- Fork activity
- Language distribution
- Development patterns

---

## Repository Intelligence

Analyzes repositories using available GitHub evidence:

- Repository metadata
- README availability
- Documentation signals
- Topics
- Project information
- Activity data

---

## Developer DNA Analysis

Creates an experimental scoring system based on GitHub activity patterns.

Dimensions:

- Momentum
- Discipline
- Craft
- Influence
- Insight
- Resolve

Scores are generated from available GitHub evidence and used for developer profile visualization.

> Developer DNA is an experimental visualization system and does not represent official programming ability.

---

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

```text
Intelligence-Hub/

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
```

---

# Installation

## Clone Repository

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

Activate the environment.

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

Create a `.env` file in the project root.

Example:

```env
GITHUB_TOKEN=your_github_token
GITHUB_GRAPHQL_TOKEN=your_github_graphql_token
```

Environment variables are used for GitHub API access.

Never upload `.env` publicly.

---

# Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Application runs at:

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

---

## 2. Repository Analysis

Repositories are analyzed using:

- Project information
- README availability
- Documentation signals
- Repository activity
- Metadata

---

## 3. Developer Analysis

Collected data is processed to generate developer insights:

- Momentum
- Discipline
- Craft
- Influence
- Insight
- Resolve

---

## 4. Visualization

Processed data is displayed through:

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
- Developer DNA scores are experimental metrics.
- Results are based only on available GitHub evidence.

---

# Future Improvements

Possible improvements:

- More advanced repository analysis
- Improved developer scoring
- Better AI-assisted insights
- More visualization features
- Additional developer metrics

---

# License

This project is licensed under the MIT License.