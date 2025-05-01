from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings

def extract_clean_text(html: str) -> str:
    """
    Extract and clean main text content from HTML or XML using BeautifulSoup.
    Tries to auto-detect document type and parse accordingly.
    """
    # Suppress the XMLParsedAsHTMLWarning
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

    try:
        # Try parsing as XML first if the input looks like it (you can modify this detection logic)
        if html.strip().startswith("<?xml") or "<rss" in html.lower():
            soup = BeautifulSoup(html, 'lxml-xml')
        else:
            soup = BeautifulSoup(html, 'lxml')
    except Exception as e:
        print("Parsing error:", e)
        return ""

    # Remove unwanted tags
    for tag in soup(['script', 'style', 'nav', 'footer', 'meta', 'link', 'header', 'aside']):
        tag.decompose()

    # Focus on main content
    main = soup.find(['main', 'article']) or soup.body
    text = main.get_text(separator='\n', strip=True) if main else soup.get_text(separator='\n', strip=True)

    # Clean up excessive blank lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return '\n'.join(lines)
