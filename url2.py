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

# Function to create url_data table
def create_url_data_table():
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS url_table_2 (
        name VARCHAR(255),
        year INTEGER,
        wins INTEGER,
        losses INTEGER,
        ot_losses VARCHAR(255),
        pct FLOAT,
        gf INTEGER,
        ga INTEGER,
        diff INTEGER
    );
    '''
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()

# Function to insert url data into the url_data table
def insert_url_data(data):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    insert_query = '''
    INSERT INTO url_table_2 (name, year, wins, losses, ot_losses, pct, gf, ga, diff)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''
    for row in data:
        cur.execute(insert_query, row)
    conn.commit()
    cur.close()
    conn.close()

# Function to scrape table data from a given URL
def scrape_table_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the table and its headers
    table = soup.find('table')
    headers = [header.text for header in table.find_all('th')]

    # Extract the table rows
    rows = table.find_all('tr', class_='team')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        # Convert data to proper types
        cols[1] = int(cols[1])
        cols[2] = int(cols[2])
        cols[3] = int(cols[3])
        cols[5] = float(cols[5])
        cols[6] = int(cols[6])
        cols[7] = int(cols[7])
        cols[8] = int(cols[8])
        data.append(cols)
    return data

# Function to extract pagination links and scrape data from each link
def scrape_all_pages():
    base_url = "https://www.scrapethissite.com"
    initial_url = f"{base_url}/pages/forms/"
    response = requests.get(initial_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract pagination links
    pagination_area = soup.find('div', class_='pagination-area')
    links = pagination_area.find_all('a', href=True)
    unique_links = {base_url + link['href'] for link in links}

    all_data = []
    for link in unique_links:
        data = scrape_table_data(link)
        all_data.extend(data)
    # print(unique_links)    
    return all_data

# Function to parse HTML content and extract headline data
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    info_div = soup.find('div', class_='row')

    if info_div:
        heading_tag = info_div.find('h1')
        if heading_tag:
            heading = heading_tag.text.strip()
        else:
            heading = "Heading not found"

        description_tag = soup.find('p', class_='lead')
        if description_tag:
            description = description_tag.text.strip()
        else:
            description = "Description not found"

        link_tag = soup.find('a', class_='data-attribution')
        if link_tag:
            link = link_tag.get('href')
        else:
            link = "Link not found"
    else:
        heading, description, link = "Info div not found", "", ""

    return heading, description, link

# Main code
if __name__ == '__main__':
    create_headlines_table()
    create_url_data_table()

    # Scrape all pages and insert into the database
    all_data = scrape_all_pages()
    insert_url_data(all_data)

    # Parse HTML content and insert headlines into the headlines table
    url = "https://www.scrapethissite.com/pages/forms/"
    response = requests.get(url)
    html_content = response.text
    heading, description, link = parse_html(html_content)

    insert_headline_data(heading, description, link)
    print("Success!")
