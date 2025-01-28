from selenium import webdriver  
from selenium.webdriver.common.by import By  
import time  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException

class VisibleBrowser:  
    def __init__(self, url):  
        self.options = webdriver.ChromeOptions()  
        self.options.add_argument("--disable-infobars")  
        self.driver = webdriver.Chrome(options=self.options)  
        self.driver.get(url)  # Open website immediately  
        time.sleep(2)  # Allow page load  
    
    def inject_payload(self, element_name, payload):
        """Inject payload into a form field or URL parameter and handle alerts"""
        try:
            # For form fields
            element = self.driver.find_element(By.NAME, element_name)
            element.clear()
            element.send_keys(payload)
            element.send_keys(Keys.RETURN)
            time.sleep(2)  # Wait for page reload
            return True
        except:
            # For URL parameters
            current_url = self.driver.current_url
            if "?" in current_url:
                new_url = f"{current_url.split('?')[0]}?{element_name}={payload}"
            else:
                new_url = f"{current_url}?{element_name}={payload}"
            self.driver.get(new_url)
            time.sleep(2)
            return True


    def check_reflection(self, payload):
        """Check if the payload is reflected in the page source and handle alerts"""
        try:
            # Check for reflection in page source
            if payload in self.driver.page_source:
                print("[!] Reflection detected")
                return True
            else:
                print("[×] No reflection")
                return False
        except UnexpectedAlertPresentException:
            # If an alert is present, it means the payload executed
            print("[!] Alert triggered: Payload executed successfully!")
            try:
                # Wait for the alert to appear and dismiss it
                WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.accept()  # Dismiss the alert
                print(f"[!] Alert text: {alert_text}")
                return True
            except (TimeoutException, NoAlertPresentException):
                # If the alert disappears before we can handle it
                print("[×] Alert disappeared before handling")
                return False
            
    def check_execution(self, payload):
        """Check if the payload executed JavaScript"""
        try:
            # Wait for the alert to appear and dismiss it
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()  # Dismiss the alert
            print(f"[!] Alert triggered: {alert_text}")
            return True
        except (TimeoutException, NoAlertPresentException):
            # If no alert is present
            print("[×] No execution detected")
            return False


    def get_inputs(self):  
        """Extract inputs from the visible page"""  
        inputs = []  
        
        # Find all input fields  
        for element in self.driver.find_elements(By.TAG_NAME, 'input'):  
            inputs.append({  
                "name": element.get_attribute("name"),  
                "type": element.get_attribute("type"),  
                "id": element.get_attribute("id")  
            })  

        # Find URL parameters  
        current_url = self.driver.current_url  
        if '?' in current_url:  
            params = current_url.split('?')[1].split('&')  
            inputs.extend({"type": "url_param", "value": param} for param in params)  

        return inputs  

    def keep_alive(self):  
        """Keep browser open until manually closed"""  
        input("Press Enter to close the browser...")  
        self.driver.quit()  