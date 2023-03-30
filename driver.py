# import required modules
import os
import pickle
from io import BytesIO
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import requests

class GetStatus():
    def __init__(self) -> None:
        # Chrome options
        self.options = webdriver.ChromeOptions()
        #self.options.add_argument("--headless") até resolver o qrcode no popup
        self.options.add_argument('--window-size=900,600')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("start-maximized")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-browser-side-navigation")

        self.cookies_file = "whatsapp_cookies.pkl"

        # check if cookies file exists
        if os.path.exists(self.cookies_file):
            # load cookies from file
            with open(self.cookies_file, "rb") as f:
                self.cookies = pickle.load(f)
            # add cookies to options
            for cookie in self.cookies:
                self.options.add_argument(f"--cookie={cookie['name']}={cookie['value']}")

        # create driver instance
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        self.driver.get("https://web.whatsapp.com/")

    def save_cookies(self):
        # get cookies from driver
        cookies = self.driver.get_cookies()
        # save cookies to file
        with open(self.cookies_file, "wb") as f:
            pickle.dump(cookies, f)

    def seturl(self):
        self.url = f"https://web.whatsapp.com/send/?phone={self.id}&text&type=phone_number&app_absent=0"
        
    def test(self):
            self.time = self.count * 5
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
                        self.result = "Não tem WhatsApp"
                    else:
                        self.result = "Error."
            except:
                self.result = "Error."
            else:
                if(self.a == self.checkerTextValid):
                    self.result = "Instabilidade sistêmica na Meta."
                else:
                    self.result = "Error."
            finally:
                print(self.result)
                self.count = 3
                # self.driver.quit()

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
        
    def login(self):
        self.driver.get("https://web.whatsapp.com")
        #self.check_login_status()
        # WebDriverWait(self.driver, 10)
        # # Take a screenshot of the whole window
        # screenshot = self.driver.get_screenshot_as_png()
        # img = Image.open(BytesIO(screenshot))
        # # Crop the image to the region containing the QR code
        # qr_code_img = img.crop((100, 100, 350, 350))
        # qr_code_img.save("Project\qr_code.png")


    def check_login_status(driver):
        try:
            # Check if the chat list element is present, which means the user is logged in
            chat_list = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._3j8Pd")))
            return True
        except:
            return False
        else:
            self.driver.close()
            self.chrome_options.add_argument('--headless')
            driver.execute_script("window.open('https://web.whatsapp.com');")

