import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Exception NoSuchWindowException when windows get closed

class GetStatus():

    def __init__(self) -> None:
        
        self.options = webdriver.ChromeOptions();
        self.options.add_argument(f"user-data-dir={os.path.dirname(os.path.abspath(__file__))}/profile")
        self.options.add_argument("--disable-application-cache")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-browser-side-navigation")
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--remote-debugging-port=9222')
        self.options.add_argument('--headless')        
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
                
        self.driver = webdriver.Chrome(options=self.options, service=ChromeService(ChromeDriverManager().install()))
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def seturl(self):
        self.url = f"https://web.whatsapp.com/send/?phone={self.id}&text&type=phone_number&app_absent=0"
        
    def test(self):
            self.time = self.count * 10
            try:
                # Check if it is valid, if there is the "Type a message"
                self.a = WebDriverWait(self.driver, self.time).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'))).get_attribute("title")
            except TimeoutException: 
                try:
                    # Check if it is invalid, if there is the "Phone number shared via url is invalid."
                    self.a = WebDriverWait(self.driver, self.time).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[1]'))).get_attribute("innerHTML")
                except TimeoutException:                
                    if(self.count > 1):
                        count -= 1
                        self.test(self)
                except:
                    self.result = "Error."
                else:
                    if(self.a == self.checkerTextInvalid):
                        self.result = "Invalid Number."
                    else:
                        self.result = "Error."
            except:
                self.result = "Error."
            else:
                if(self.a == self.checkerTextValid):
                    self.result = "Valid Number."
                else:
                    self.result = "Error."
            finally:
                print(self.result)
                self.count = 3
                self.driver.quit()

    def run(self, id):
        
        self.options.add_argument('headless'); # not working?
        self.waitText = "Starting chat" # not being used
        self.checkerTextInvalid = "Phone number shared via url is invalid."
        self.checkerTextValid = "Type a message"
        self.id = id

        self.seturl()
        self.driver.get(self.url)

        self.count = 3
        self.test()

        return self.result
        
    def config(self):
        self.username = 'YOUR-COMPUTER-USERNAME' # OR input("Computer Username") ?
        self.driver.get("https://web.whatsapp.com/")
        self.start = input("LOGIN - PRESS ENTER")
        self.driver.quit()