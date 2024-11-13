import requests
from bs4 import BeautifulSoup
import re


def scrape_website(url):
    try:
        # Fetch the HTML content of the website
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract metadata
        metadata = {}
        for tag in soup.find_all('meta'):
            name = tag.get('name', '')
            content = tag.get('content', '')
            if name and content:
                metadata[name] = content

        # Extract all SEO keywords
        seo_keywords = set()  # Use a set to avoid duplicates
        # Search for keywords in various places where they might be specified
        for tag in soup.find_all(['meta', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
            text = tag.get_text().strip()
            # Use regex to find words containing letters, numbers, and hyphens
            keywords = re.findall(r'\b[\w\d-]+\b', text)
            seo_keywords.update(keywords)

        return metadata, list(seo_keywords)

    except requests.exceptions.RequestException as e:
        print(f"Error while fetching the website: {e}")
        return None, None
    except Exception as e:
        print(f"Error during scraping: {e}")
        return None, None

if __name__ == "__main__":
    website_url = "https://www.angelone.in/"
    metadata, seo_keywords = scrape_website(website_url)

    if metadata or seo_keywords:
        print("Metadata:")
        for name, content in metadata.items():
            print(f"{name}: {content}")
    else:
        print("No meta found")
    if metadata or seo_keywords:
        print("\nSEO Keywords:")
        for keyword in seo_keywords:
            print(keyword)
    else:
        print("No seo found.")
