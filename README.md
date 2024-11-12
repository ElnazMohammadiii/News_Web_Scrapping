# News Scraper

This repository contains multiple Python scripts designed to scrape news articles from various sources. These scripts are optimized for handling limiting and blocking, with error handling, logging, and task scheduling. Additionally, Docker and requirements.txt files make it easy to run this project in a consistent environment.

## Project Structure

- News_Scraper_Simple.py: A basic news scraping script for collecting news articles using Python and BeautifulSoup.
- News_Scraper_with_Logging_and_Error_Handling.py: A scraper with enhanced logging and error handling to ensure robust execution.
- News_Scraper_to_Mitigate-limiting-blocking.py: An advanced version of the scraper that incorporates strategies to mitigate rate-limiting.
- requirements.txt: Specifies Python dependencies required by the scrapers, facilitating an easy setup.
- Dockerfile: Docker configuration to create a containerized environment for running the news scrapers.

## Prerequisites

Ensure you have the following software installed:

- Docker: for containerized execution.
- Python 3.7+: if running locally.

## Installation

1. Clone the repository:
   
   git clone https://github.com/your-username/news-scraper.git
   cd news-scraper
   
2. Install dependencies (if running locally):
   
   pip install -r requirements.txt
   
## Running with Docker

1. Build the Docker image:
   
   docker build -t news-scraper .
   
2. Run the Docker container:
   
   docker run -d --name news-scraper news-scraper
   
This will run the scraper in a Docker container, ensuring consistent environment settings.

## Usage

Choose one of the scraping scripts depending on your requirements:

- Basic Scraper: For straightforward scraping tasks.
- Rate-Limited Scraper: Use this version to avoid rate limiting, ideal for sites with restrictions.
- Logging Scraper: For detailed logging and error reporting during scraping tasks.

To run a specific script, use the following command:

python <script_name>.py
For instance, to run the rate-limited scraper:

python News_Scraper_to_Mitigate_limiting_blocking.py

## Dependencies

This project uses the following libraries (as defined in `requirements.txt`):

- beautifulsoup4, requests: For web scraping and making HTTP requests.
- pandas, numpy: For data manipulation and analysis.
- schedule: For task scheduling.
- Other supporting libraries.

Refer to the requirements.txt file for the complete list of dependencies.

## Contributing

Feel free to open issues or submit pull requests if you find bugs or want to add features.

## License

This project is licensed under the MIT License.