from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

class BasicCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.discovered_urls = set()
        self.input_points = []  # Format: {"url": "", "params": [], "method": "GET/POST"}

    def find_inputs(self, url):
        """Extract input points from a single page"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all forms
            for form in soup.find_all('form'):
                action = form.get('action', '')
                form_url = urljoin(self.base_url, action)
                method = form.get('method', 'GET').upper()
                inputs = [input_tag.get('name') for input_tag in form.find_all('input')]
                self.input_points.append({
                    "url": form_url,
                    "method": method,
                    "params": inputs
                })

            # Find URL parameters (e.g., ?id=123)
            links = soup.find_all('a', href=True)
            for link in links:
                href = urljoin(self.base_url, link['href'])
                if '?' in href:
                    path, params = href.split('?', 1)
                    self.input_points.append({
                        "url": path,
                        "method": "GET",
                        "params": params.split('&')
                    })

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def crawl(self):
        """Entry point for crawling"""
        self.find_inputs(self.base_url)
        return self.input_points