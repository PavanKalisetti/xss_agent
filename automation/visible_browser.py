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
        self.driver.get(url)  
        time.sleep(2)  
    
    def inject_payload(self, element_name, payload):
        try:
            element = self.driver.find_element(By.NAME, element_name)
            element.clear()
            element.send_keys(payload)
            element.send_keys(Keys.RETURN)
            time.sleep(2)  
            return True
        except:
            
            current_url = self.driver.current_url
            if "?" in current_url:
                new_url = f"{current_url.split('?')[0]}?{element_name}={payload}"
            else:
                new_url = f"{current_url}?{element_name}={payload}"
            self.driver.get(new_url)
            time.sleep(2)
            return True


    def check_reflection(self, payload):
        try:
            
            if payload in self.driver.page_source:
                print("[!] Reflection detected")
                return True
            else:
                print("[×] No reflection")
                return False
        except UnexpectedAlertPresentException:
            
            print("[!] Alert triggered: Payload executed successfully!")
            try:
                
                WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.accept()  
                print(f"[!] Alert text: {alert_text}")
                return True
            except (TimeoutException, NoAlertPresentException):
                
                print("[×] Alert disappeared before handling")
                return False
            
    def check_execution(self, payload):
        try:
            
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()  
            print(f"[!] Alert triggered: {alert_text}")
            return True
        except (TimeoutException, NoAlertPresentException):
            
            print("[×] No execution detected")
            return False


    def get_inputs(self):  
        inputs = []  
        
        
        for element in self.driver.find_elements(By.TAG_NAME, 'input'):  
            inputs.append({  
                "name": element.get_attribute("name"),  
                "type": element.get_attribute("type"),  
                "id": element.get_attribute("id")  
            })  

        
        current_url = self.driver.current_url  
        if '?' in current_url:  
            params = current_url.split('?')[1].split('&')  
            inputs.extend({"type": "url_param", "value": param} for param in params)  

        return inputs  

    def keep_alive(self):  
        input("Press Enter to close the browser...")  
        self.driver.quit()  