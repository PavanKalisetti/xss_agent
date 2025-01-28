from bs4 import BeautifulSoup  
from .visible_browser import VisibleBrowser  

class LiveCrawler:  
    def __init__(self, target_url):  
        self.browser = VisibleBrowser(target_url)  
        self.inputs = []  

    def crawl_visible_site(self):  
        """Extract inputs while user watches the browser"""  
        print("[+] Browser opened. Monitoring interactions...")  
        self.inputs = self.browser.get_inputs()  
        return self.inputs  

    def close(self):  
        self.browser.keep_alive()  # Let user inspect results before closing  