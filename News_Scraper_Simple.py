# import libraries
import requests  # Import the requests module to send HTTP requests
from bs4 import BeautifulSoup  # Import BeautifulSoup to parse HTML content
import csv  # Import the csv module to handle CSV file reading and writing
import time  # Import time module to pause execution for a specified interval


def fetch_tabnak_news():
    """
    Fetches the HTML content of the Tabnak website.
    Sends a GET request to the website and returns the parsed BeautifulSoup object.
    """
    url = "https://www.tabnak.ir"  # URL of the website to scrape
    response = requests.get(url)  # Send a GET request to fetch the page content
    return BeautifulSoup(response.text, 'html.parser')  # Parse the HTML and return the BeautifulSoup object


def extract_news(soup):
    """
    Extracts news headlines, links, and other relevant data from the BeautifulSoup object.
    Returns a list of dictionaries containing extracted news information.
    """
    # Find all news items on the page using the specified CSS class
    news_items = soup.find_all('div', class_='col-xs-36 padd_box news_parent')
    extracted_data = []  # Initialize an empty list to store the extracted data

    # Loop through each news item to extract the necessary information
    for item in news_items:
        link = item.find('a', class_='title5film')  # Find the link tag containing the news title
        if link:  # If a link is found
            title = link.get('title')  # Extract the title of the news article
            href = link.get('href')  # Extract the relative URL of the news article
            target = link.get('target')  # Extract the target attribute (if present, for opening in new windows)
            # Append the extracted data as a dictionary to the list
            extracted_data.append({'title': title, 'href': href, 'target': target})

    return extracted_data  # Return the list of extracted news data


def load_existing_data(csv_file):
    """
    Loads existing data from a CSV file.
    Returns a list of dictionaries representing the rows in the CSV file.
    If the file is not found, returns an empty list.
    """
    try:
        # Open the CSV file and read its content into a list of dictionaries
        with open(csv_file, newline='', encoding='utf-8-sig') as file:
            return [row for row in csv.DictReader(file)]  # Use DictReader to convert each row into a dictionary
    except FileNotFoundError:  # If the file doesn't exist, return an empty list
        return []


def save_new_data(csv_file, new_data):
    """
    Saves new data to a CSV file.
    Appends the new data to the file, creating the header if the file is empty.
    """
    with open(csv_file, 'a', newline='', encoding='utf-8-sig') as file:
        # Create a CSV writer object that will write dictionaries to the file
        writer = csv.DictWriter(file, fieldnames=['title', 'href', 'target'])

        # If the file is empty (tell() == 0), write the header row
        if file.tell() == 0:
            writer.writeheader()

        # Write the new data to the CSV file
        writer.writerows(new_data)


def check_for_updates(csv_file='tabnak_news.csv'):
    """
    Checks for updates on the Tabnak website.
    Compares the current news articles with the existing ones in the CSV file.
    Saves any new articles found to the CSV file.
    """
    soup = fetch_tabnak_news()  # Fetch the HTML content of the Tabnak website
    current_data = extract_news(soup)  # Extract the current news data from the fetched content
    existing_data = load_existing_data(csv_file)  # Load existing data from the CSV file

    # Create a set of existing news titles to check for duplicates
    existing_titles = {item['title'] for item in existing_data}
    # Filter the current data to find news articles that aren't already in the existing data
    new_entries = [item for item in current_data if item['title'] not in existing_titles]

    # If there are new entries, save them to the CSV file and print a message
    if new_entries:
        save_new_data(csv_file, new_entries)  # Save the new entries to the CSV file
        print(f"Added {len(new_entries)} new entries.")  # Print how many new entries were added
    else:
        print("No new entries found.")  # Print a message if no new entries were found


if __name__ == "__main__":  # This block runs if the script is executed directly (not imported as a module)
    while True:  # Infinite loop to continuously check for updates
        check_for_updates()  # Check for new news articles and save them if found
        time.sleep(300)  # Pause execution for 5 minutes before checking again
