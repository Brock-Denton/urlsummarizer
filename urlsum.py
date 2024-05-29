import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# Initialize Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(requests.Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=59681)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
service_sheets = build('sheets', 'v4', credentials=creds)

# Fetch URL content
def fetch_url_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        print(f"Error fetching URL content: {e}")
        return None

# Summarize content
def summarize_content(text):
    try:
        summarizer = pipeline('summarization', model='t5-small')
        summary = summarizer(text, max_length=200, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error summarizing content: {e}")
        return None

# Function to dynamically categorize articles based on keywords
def categorize_article(summary):
    keywords = {
        "Quantum Physics": ["quantum", "superposition", "entanglement", "quantum mechanics", "particles", "wave function"],
        "Space": ["space", "astronomy", "cosmology", "galaxy", "universe", "black hole", "planets", "stars", "astrophysics"],
        "Computing": ["computing", "algorithm", "processor", "AI", "artificial intelligence", "machine learning", "quantum computing", "data science", "neural networks"],
        "Biology": ["biology", "genetics", "evolution", "ecology", "microbiology", "molecular biology", "biotechnology"],
        "Medicine": ["medicine", "health", "disease", "treatment", "surgery", "pharmacology", "neuroscience", "mental health", "clinical trials"],
        "Physics": ["physics", "relativity", "thermodynamics", "particles", "field theory", "energy", "gravity", "electromagnetism"],
        "Chemistry": ["chemistry", "molecule", "reaction", "organic chemistry", "inorganic chemistry", "biochemistry", "chemical", "catalyst"],
        "Engineering": ["engineering", "mechanical engineering", "electrical engineering", "civil engineering", "software engineering", "robotics", "nanotechnology"],
        "Environment": ["environment", "climate change", "sustainability", "ecology", "conservation", "biodiversity", "pollution"],
        "Economics": ["economics", "finance", "market", "trade", "investment", "economy", "recession", "inflation"],
        "Social Sciences": ["sociology", "psychology", "anthropology", "political science", "education", "human behavior"],
        "Technology": ["technology", "innovation", "internet", "cybersecurity", "blockchain", "virtual reality", "augmented reality"]
    }

    categories = []
    for category, words in keywords.items():
        if any(word in summary.lower() for word in words):
            categories.append(category)

    if not categories:
        categories.append("General")

    return ", ".join(categories)

# Function to read URLs from Google Sheet
def read_urls_from_sheet(spreadsheet_id, range_name):
    sheet = service_sheets.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    urls = [row[0] for row in values[1:] if row]  # Skip header row and empty rows
    existing_summaries = {row[0]: row[1] for row in values[1:] if len(row) > 1 and row[1]}  # URLs with existing summaries
    return urls, values, existing_summaries

# Function to write summaries to Google Sheet
def write_summaries_to_sheet(spreadsheet_id, range_name, summaries, existing_values):
    values = []
    for row in existing_values:
        if row and row[0] in summaries:
            values.append([row[0], summaries[row[0]]['summary'], summaries[row[0]]['category']])
        else:
            values.append(row)
    
    body = {
        'values': values
    }
    result = service_sheets.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()

# Main function to process URLs and update Google Sheet 
def main():
    spreadsheet_id = 'your_spreadsheet_id_here'  # Replace with your spreadsheet ID
    read_range = 'Sheet1!A:C'  # Adjust range if necessary
    write_range = 'Sheet1!A:C'  # Adjust range if necessary
    
    urls, existing_values, existing_summaries = read_urls_from_sheet(spreadsheet_id, read_range)
    print(f"URLs found: {urls}")
    summaries = {}
    for url in urls:
        if url in existing_summaries:
            print(f"Skipping URL (already has summary): {url}")
            continue
        print(f"Processing URL: {url}")
        content = fetch_url_content(url)
        if content:
            print(f"Fetched content length: {len(content)}")
            summary = summarize_content(content)
            if summary:
                category = categorize_article(summary)
                summaries[url] = {'summary': summary, 'category': category}
                print(f"Summary generated for URL: {url}")
            else:
                print(f"No summary generated for URL: {url}")
        else:
            print(f"No content fetched for URL: {url}")
    print(f"Summaries: {summaries}")
    write_summaries_to_sheet(spreadsheet_id, write_range, summaries, existing_values)

if __name__ == "__main__":
    main()
