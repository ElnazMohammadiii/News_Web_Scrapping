# import libraries
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

# Set up logging configuration
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

BASE_URL = "https://www.tabnak.ir"



def fetch_tabnak_news():
    """
    Fetches the HTML content of the news page.
    Returns the parsed BeautifulSoup object of the page content.
    :return:
    """
    url = BASE_URL
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return None
    return BeautifulSoup(response.text, 'html.parser')


def extract_news(soup):
    """
    Extracts news headlines, links, and other data from the parsed BeautifulSoup object.
    """
    news_items = soup.find_all('div', class_='col-xs-36 padd_box news_parent')
    extracted_data = []

    for item in news_items:
        link = item.find('a', class_='title5film')
        if link:
            title = link.get('title', '').strip()  # Strip whitespace from title
            href = link.get('href', '')
            if href:
                href = f"{BASE_URL}{href}".strip()  # Strip whitespace from URL

            if title and href:  # Only add if both title and href are non-empty
                extracted_data.append({
                    'title': title,
                    'href': href,
                    'timestamp': datetime.now().isoformat()
                })

    return extracted_data


def load_existing_data(csv_file):
    """
    Loads existing data from CSV file with proper error handling and data cleaning.
    """
    try:
        # Read CSV with proper encoding and handle missing values
        df = pd.read_csv(csv_file, encoding='utf-8-sig', on_bad_lines='skip')

        # Clean the data
        df['title'] = df['title'].astype(str).str.strip()
        df['href'] = df['href'].astype(str).str.strip()

        # Drop duplicates based on title and href
        df = df.drop_duplicates(subset=['title', 'href'])

        # Convert to list of dictionaries
        return df.to_dict('records')
    except FileNotFoundError:
        logging.info(f"No existing file found at {csv_file}. Starting fresh.")
        return []
    except Exception as e:
        logging.error(f"Error loading existing data: {e}")
        return []


def save_new_data(csv_file, new_data):
    """
    Saves new data to CSV file with proper error handling.
    """
    try:
        df = pd.DataFrame(new_data)
        df.to_csv(csv_file, mode='a', index=False,
                  header=not pd.io.common.file_exists(csv_file),
                  encoding='utf-8-sig')
        logging.info(f"Successfully saved {len(new_data)} new entries.")
    except Exception as e:
        logging.error(f"Error saving data: {e}")


def check_for_updates(csv_file='tabnak_news.csv'):
    """
    this function check site for new updates
    :param csv_file: this is the log file for scrapped titles
    :return:
    """
    # Fetch and extract current news
    soup = fetch_tabnak_news()
    if soup is None:
        return

    # Extract current news data
    current_data = extract_news(soup)
    if not current_data:
        logging.info("No data extracted from the website.")
        return

    # Load existing data
    existing_data = load_existing_data(csv_file)

    # Create a set of (title, href) tuples from existing data for comparison
    existing_items = {(item['title'].strip(), item['href'].strip())
                      for item in existing_data if 'title' in item and 'href' in item}

    # Filter out duplicates from current data
    new_entries = []
    for item in current_data:
        current_key = (item['title'].strip(), item['href'].strip())
        if current_key not in existing_items:
            new_entries.append(item)
            existing_items.add(current_key)  # Add to set to prevent duplicates within same batch


    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save new entries if any found
    if new_entries:
        save_new_data(csv_file, new_entries)
        logging.info(f"Added {len(new_entries)} new unique entries.")
        print(f"{current_time}    Added {len(new_entries)} new unique entries.")
    else:
        logging.info("No new unique entries found.")
        print(f"{current_time}    No new unique entries found.")


if __name__ == "__main__":
    # Add initial delay to ensure proper startup
    time.sleep(5)

    while True:
        try:
            check_for_updates()
            # Sleep for 5 minutes (300 seconds)
            time.sleep(5*60)
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            print(f"Error in main loop: {e}")
            # Sleep for 1 minute before retrying in case of error
            time.sleep(1*60)