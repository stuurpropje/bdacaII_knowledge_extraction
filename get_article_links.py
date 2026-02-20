import requests
import json
import re
import time
from bs4 import BeautifulSoup

# Define the API endpoint and polite defaults
API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "MediaWikiAPITutorial/1.0 (contact: 13411438@uva.nl)"
REQUEST_DELAY = 0.5  # seconds between requests
TIMEOUT = 30

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

def api_get(params: dict) -> dict | None:
    """Make a safe request to the MediaWiki API with retries and rate limiting."""
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
    params = {
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'revisions',
        'rvprop': 'content',
        'rvslots': 'main',
    }

    data = api_get(params)
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


def get_article_links(title, limit=50):
    """
    Get links from a Wikipedia article that appear in the rendered body,
    excluding links from "See also" and later sections (References,
    External links, Notes, Further reading, Bibliography).

    Uses the MediaWiki parse API to fetch the rendered HTML, then
    BeautifulSoup to extract <a> tags before the first stop-section
    heading. Only main-namespace article links are returned (no
    File:, Category:, etc.). Links are deduplicated and returned in
    the order they appear on the page.

    Note: links inside <ref> citations are NOT included because the
    rendered HTML moves them to the References section at the bottom.

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
    params = {
        'action': 'parse',
        'page': title,
        'prop': 'text',
        'format': 'json'
    }
    
    data = api_get(params)
    if not data or 'parse' not in data:
        return []
    
    html = data['parse']['text']['*']
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find where "See also" or similar sections start
    stop_sections = ['See also', 'References', 'External links', 'Notes', 'Further reading', 'Bibliography']
    stop_element = None
    
    for heading in soup.find_all('h2'):
        # New MediaWiki HTML: <h2 id="See_also">See also</h2>
        heading_text = heading.get_text(strip=True)
        # Strip any "[edit]" suffix that MediaWiki may include
        heading_text = heading_text.replace('[edit]', '').strip()
        if heading_text in stop_sections:
            # The h2 may be wrapped in a <div class="mw-heading">, remove from there
            parent = heading.parent
            if parent and parent.has_attr('class') and 'mw-heading' in parent.get('class', []):
                stop_element = parent
            else:
                stop_element = heading
            break
    
    # If we found a stop point, remove everything after it
    if stop_element:
        for sibling in list(stop_element.next_siblings):
            sibling.extract()
        stop_element.extract()
    
    # Now extract links from the remaining content
    links = []
    seen = set()
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Only include links to main namespace articles
        if href.startswith('/wiki/') and ':' not in href.split('/wiki/')[1]:
            link_title = href.split('/wiki/')[1].replace('_', ' ')
            link_title = requests.utils.unquote(link_title)
            
            if link_title not in seen:
                seen.add(link_title)
                links.append({
                    'title': link_title,
                    'url': f'https://en.wikipedia.org{href}'
                })
                if len(links) >= limit:
                    break
    
    return links