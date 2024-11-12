# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for Selenium and web scraping
# Install Chromium browser and Chromium driver for Selenium
RUN apt-get update && \
    apt-get install -y \
        chromium-driver \
        wget \
        gnupg && \
    rm -rf /var/lib/apt/lists/*

# Set up environment variables for Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromium-driver

# Copy the current directory contents into the container at /app
COPY . .

# Specify the default command to run the scraper
CMD ["python", "News_Scraper_Simple.py"]
