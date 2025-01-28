from selenium import webdriver
from selenium.webdriver.common.by import By

class HeadlessBrowser:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)

    def get_inputs(self, url):
        self.driver.get(url)
        inputs = []
        
        # Find all form fields
        for element in self.driver.find_elements(By.TAG_NAME, 'input'):
            inputs.append({
                "name": element.get_attribute("name"),
                "type": element.get_attribute("type")
            })
        
        # Find URL parameters
        current_url = self.driver.current_url
        if '?' in current_url:
            params = current_url.split('?')[1].split('&')
            inputs.extend(params)
        
        self.driver.quit()
        return inputs