import requests
from bs4 import BeautifulSoup
import psycopg2

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


def extract_headings(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    headings = []
    
    d = soup.find('h3').text
    headings.append(d)
    h4 = soup.find_all('h4')

    for tag in h4:
        headings.append(tag.get_text(strip=True))
    return headings    

def extract_para(html_content):
    soup = BeautifulSoup(html_content,'html.parser')
    info_div = soup.find('div',class_='row')
    para = info_div.find_all('p')
    description = []
    for p in para:
        description.append(p.get_text(strip=True))
    return description    
        
def extract_link(html_content):
    soup = BeautifulSoup(html_content,'html.parser')
    info_div = soup.find('div',class_='row')
    link_tag = soup.find_all('a')
    links = []
    
    for link in link_tag:
        x = link.get('href')
        links.append(f'https://www.scrapethissite.com/pages{x}')
    return links
    
url = "https://www.scrapethissite.com/pages/advanced/"
responce = requests.get(url)
html_content = responce.text
headings = extract_headings(html_content)
description = extract_para(html_content)
links = extract_link(html_content)
    
for i in range(len(headings)):
    # print([headings[i],description[i], links[i]])
    insert_headline_data(headings[i], description[i], links[i])  
print('Success!')    