# News Intelligence Dashboard Pro

## Project Overview

News Intelligence Dashboard Pro is a desktop-based news analytics application developed using Python and CustomTkinter. The application collects news headlines from multiple RSS news sources and presents them through an interactive dashboard interface.

The project was designed to provide users with a centralized platform for reading, searching, analyzing, and exporting news data while also offering basic analytics such as keyword trends and sentiment distribution.

## Features

### Multi-Source News Aggregation

The application fetches real-time news headlines from multiple trusted news providers, including:

* BBC News
* Reuters
* Google News

### Interactive Dashboard

The dashboard displays:

* Total Headlines Count
* Sources Loaded
* Last Updated Time
* Trending Keyword

### News Search

Users can search news headlines using keywords and instantly filter relevant results.

### Sentiment Analysis

The application performs basic sentiment classification of headlines and displays:

* Positive News Count
* Neutral News Count
* Negative News Count

### Trending Keyword Detection

Frequently occurring keywords are analyzed and displayed to help identify trending topics.

### Top Keywords Panel

The dashboard automatically identifies and displays the most common keywords appearing across collected news headlines.

### Export Functionality

Users can export news data in:

* TXT Format
* CSV Format

### Dark Mode Support

The application provides both Light Mode and Dark Mode for improved user experience.

### Local Data Storage

Fetched news data is automatically stored in JSON format for future reference and analysis.

## Technologies Used

* Python
* CustomTkinter
* Feedparser
* JSON
* CSV
* Datetime
* Collections (Counter)

## Project Structure

```text
NewsDashboard/
│
├── news_dashboard.py
├── news_data.json
├── README.md
└── screenshots/
```

## How to Run

### Install Required Libraries

```bash
pip install customtkinter
pip install feedparser
```

### Run the Application

```bash
python news_dashboard.py
```

## Application Workflow

1. Launch the application.
2. Click the Fetch News button.
3. News headlines are retrieved from multiple RSS feeds.
4. Dashboard statistics are updated automatically.
5. Search headlines using keywords.
6. Analyze trending topics and sentiment results.
7. Export data when required.

## Learning Outcomes

This project helped in understanding:

* GUI Development using CustomTkinter
* RSS Feed Integration
* Data Processing and Analytics
* File Handling using JSON and CSV
* Dashboard Design Principles
* Python Object-Oriented Programming

## Future Enhancements

Potential improvements include:

* News Category Classification
* Advanced Sentiment Analysis using NLP
* Data Visualization Charts
* Auto Refresh Functionality
* User Authentication
* Database Integration

## Author

Police Aryan Patel
Software Developer Intern
