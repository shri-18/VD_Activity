import psycopg2
from bs4 import BeautifulSoup
import requests

# Database connection parameters
db_params = {
    'dbname': 'VDT_activity',
    'user': 'postgres',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

# Function to create url_table
def create_url_table():
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS url_table_1 (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        nominations INTEGER,
        awards INTEGER,
        best_picture BOOLEAN
    );
    '''
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()

# Function to insert data into the url_table
def insert_url_data(data):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    insert_query = '''
    INSERT INTO url_table (title, nominations, awards, best_picture)
    VALUES (%s, %s, %s, %s);
    '''
    cur.executemany(insert_query, data)
    conn.commit()
    cur.close()
    conn.close()

# Function to scrape table data
def scrape_table_data():
    url = "https://www.scrapethissite.com/pages/ajax-javascript/#2015"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table_body = soup.find('table')
    rows = table_body.find_all('tr', class_='film')
    # print(table_body)
    table_content = []
    for row in rows:
        title = row.find('td', class_='film-title').text.strip()
        nominations = int(row.find('td', class_='film-nominations').text.strip())
        awards = int(row.find('td', class_='film-awards').text.strip())
        best_picture = True if row.find('td', class_='film-best-picture').find('i') else False
        table_content.append((title, nominations, awards, best_picture))
    # print(table_content)
    return table_content

# Function to create headlines table
def create_headlines_table():
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS headlines (
        id SERIAL PRIMARY KEY,
        heading TEXT NOT NULL,
        description TEXT,
        link TEXT
    );
    '''
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()

# Function to insert headline data into the headlines table
def insert_headline_data(heading, description, link):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    insert_query = '''
    INSERT INTO headlines (heading, description, link)
    VALUES (%s, %s, %s);
    '''
    cur.execute(insert_query, (heading, description, link))
    conn.commit()
    cur.close()
    conn.close()

# Function to parse HTML content and extract headline data
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    heading_tag = soup.find('h1')
    heading = heading_tag.text.strip() if heading_tag else "Heading not found"

    description_tag = soup.find('p', class_='lead')
    description = description_tag.text.strip() if description_tag else "Description not found"

    link_tag = soup.find('a', class_='data-attribution')
    link = link_tag['href'] if link_tag else "Link not found"

    return heading, description, link

# Main code
if __name__ == '__main__':
    create_url_table()

    # Scrape table data
    table_data = scrape_table_data()

    # Insert data into the url_table
    insert_url_data(table_data)

    # Parse HTML content and insert headline data into the headlines table
    url = "https://www.scrapethissite.com/pages/ajax-javascript/#2015"
    response = requests.get(url)
    html_content = response.text
    heading, description, link = parse_html(html_content)

    create_headlines_table()
    insert_headline_data(heading, description, link)
    print("Success!")
