# FutboLM

A football analytics and information system that uses LLMs to provide insights about football players, teams, and matches.

## Features

- Interactive chat interface for football-related queries
- Player statistics and analysis
- Team performance tracking
- Match summaries and insights
- Data visualization through interactive graphs
- Real-time data scraping from reliable sources

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   GSEARCH_API_KEY=your_google_search_api_key
   CSE_ID=your_custom_search_engine_id
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Technologies Used

- Python
- Flask
- Google Custom Search API
- LLM Integration
- Web Scraping
- Data Visualization

## Project Structure

- `main.py`: Main application entry point
- `LLMCalls.py`: LLM integration and query processing
- `scraper.py`: Web scraping functionality
- `search.py`: Google search integration
- `grapher.py`: Data visualization
- `templates/`: HTML templates
- `static/`: Static assets (CSS, JS)

## License

MIT License 