# Web Scraping and Database Insertion Project

## Overview

This project involves scraping data from a website, processing the data, and inserting it into a PostgreSQL database. 
The project consists of three main Python scripts (`url1.py`, `url2.py`, and `url3.py`), each of which performs different tasks related to web scraping and data insertion.

## Project Structure

- `url1.py`: This script scrapes movie data and headlines, then inserts the data into corresponding tables in the PostgreSQL database.
- `url2.py`: This script scrapes sports team data from multiple pages and inserts the data into the PostgreSQL database. It also scrapes and inserts headlines.
- `url3.py`: This script extracts headlines, descriptions, and links from an advanced web page and inserts them into the PostgreSQL database.

## Requirements

The project requires the following Python packages:
- `psycopg2-binary`: To connect and interact with the PostgreSQL database.
- `beautifulsoup4`: To parse and extract data from HTML.
- `requests`: To make HTTP requests to fetch web pages.

## Installation

To install the required packages, run:
```sh
pip install -r requirements.txt
```

## Database Setup

Ensure you have a PostgreSQL database set up with the following parameters:
- Database name: `VDT_activity`
- User: `postgres`
- Password: `root`
- Host: `localhost`
- Port: `5432`

You can modify these parameters in each script if your setup is different.

## Scripts Workflow

### url1.py

1. **Create URL Table**: The script creates a table named `url_table_1` if it does not already exist.
2. **Scrape Table Data**: It scrapes movie data from a specified URL.
3. **Insert URL Data**: It inserts the scraped movie data into the `url_table_1`.
4. **Create Headlines Table**: It creates a table named `headlines` if it does not already exist.
5. **Parse HTML and Insert Headlines**: It parses HTML content to extract headline data and inserts this data into the `headlines` table.

### url2.py

1. **Create Headlines Table**: The script creates a table named `headlines` if it does not already exist.
2. **Create URL Data Table**: It creates a table named `url_table_2` if it does not already exist.
3. **Scrape All Pages**: It extracts sports team data from multiple pages.
4. **Insert URL Data**: It inserts the scraped data into `url_table_2`.
5. **Parse HTML and Insert Headlines**: It parses HTML content to extract headline data and inserts this data into the `headlines` table.

### url3.py

1. **Create Headlines Table**: The script creates a table named `headlines` if it does not already exist.
2. **Extract Headings, Paragraphs, and Links**: It extracts headings, descriptions, and links from an advanced web page.
3. **Insert Headline Data**: It inserts the extracted data into the `headlines` table.

## Running the Scripts

To run each script, use:
```sh
python url1.py
```
```sh
python url2.py
```
```sh
python url3.py
```

## Conclusion

This project demonstrates how to automate web scraping and data insertion into a database using Python. 
Each script focuses on a specific aspect of scraping and data handling, showcasing how to handle different data extraction and insertion scenarios.
