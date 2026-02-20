import requests
import json
import re
import time
from bs4 import BeautifulSoup

# Define the API endpoint and polite defaults
def api_get(title: str, 
            API_URL="https://en.wikipedia.org/w/api.php", 
            USER_AGENT: str = "13411438@uva.nl)", 
            REQUEST_DELAY=0.5, 
            TIMEOUT=30
            ) -> dict | None:
    """Make a safe request to the MediaWiki API with retries and rate limiting."""
    
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    params = {
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'revisions',
        'rvprop': 'content',
        'rvslots': 'main',
    }

    try:
        response = session.get(API_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except json.JSONDecodeError:
        print("Response was not valid JSON")
        return None
    finally:
        time.sleep(REQUEST_DELAY)

    return data

def get_article_links_wikitext(title, limit=50):
    """
    Get links from a Wikipedia article before the 'See also' section
    by parsing the raw wikitext markup instead of HTML.

    Fetches the article's source wikitext via the MediaWiki API, cuts
    it off at the "== See also ==" heading, and extracts [[wikilink]]
    targets using a regular expression. Only main-namespace links are
    returned (namespace prefixes like File: or Category: are skipped).
    Links are deduplicated and returned in the order they appear in
    the source.

    Note: unlike the HTML/BeautifulSoup approach, this method DOES
    include links inside <ref> citation tags, because those appear
    inline in the wikitext source before "See also".

    Parameters:
    title (str): The title of the Wikipedia article (e.g. "Fake news")
    limit (int): Maximum number of links to return (default 50)

    Returns:
    list[dict]: A list of dictionaries, each with keys:
        - 'title' (str): The linked article's title
        - 'url'   (str): Full URL to the linked article
        Returns an empty list if the article is not found or the
        request fails.
    """
    # Fetch raw wikitext

    data = api_get(title)
    if not data or 'query' not in data:
        return []

    pages = data['query']['pages']
    page_id = list(pages.keys())[0]
    if page_id == '-1':
        return []

    wikitext = pages[page_id]['revisions'][0]['slots']['main']['*']

    # Cut off everything from "== See also ==" onward
    parts = re.split(r'==\s*See also\s*==', wikitext, maxsplit=1)
    body = parts[0]

    # Extract [[Link]] and [[Link|display text]] targets
    raw_links = re.findall(r'\[\[([^#\]|]+)', body)

    # Deduplicate while preserving order, skip non-article namespaces
    seen = set()
    links = []
    for link in raw_links:
        name = link.strip()
        # Skip namespace links like "File:", "Category:", etc.
        if not name or ':' in name:
            continue
        if name not in seen:
            seen.add(name)
            links.append({
                'title': name,
                'url': f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
            })
            if len(links) >= limit:
                break

    return links