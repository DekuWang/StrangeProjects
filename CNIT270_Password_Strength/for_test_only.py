"""
This program suppose to select 5 passwords randomly from the given txt file, and 
"""
# Implemented Modules
import json
import random
import time

# Third-party Modules
from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service

HTTP_ADDRESS_SEC = r"https://www.security.org/how-secure-is-my-password/"
HTTP_ADDRESS_PWDMETER = r"https://passwordmeter.com/"
BROWSER_USER_DATA = r"C:/Users/97456/AppData/Local/Google/Chrome/User Data/"

############BROWSER SETUP###############
chromeOptions = wb.ChromeOptions()
chromeOptions.add_argument('--ignore-certificate-errors-spki-list')
chromeOptions.add_argument("--user-data-dir=" + BROWSER_USER_DATA)
chromeOptions.add_argument("--profile-directory=Default")
#########BROWSER SETUP END##############

TIME_PATH = "//p[@class = \"result__text result__time\"]"
SUGGESTION_PATH = "//div/h2[@class = \"brand-heading\"]"



class Passwords():
    def __init__(self, provided_file:str) -> None:
        """
        provided_file is a real string of file path
        amount is the amount of lines we need from the file
        """
        self.path = provided_file


    def get_result(self, amount:int) -> list[int]:
        with open(self.path, "r") as file:
            pwd_list = random.sample(file.readlines(), amount)

        pwd_list = [i[:-1] for i in pwd_list]

        return pwd_list
    
class SendRequest():
    def __init__(self) -> None:
        self.driver = wb.Chrome(options=chromeOptions ,service=Service(r"chromedriver.exe"))
        self.result = {}
    
    def get_response_sec(self, pwd:list[int]):
        """
        This func is goal to fill the pwd blank and get the result of it.
        """
        self.driver.get(HTTP_ADDRESS_SEC)
        self.driver.implicitly_wait(5)

        pwd_blank = self.driver.find_element(By.XPATH, "//input[@id = \"password\"]")       # 第一遍会丢失元素
        pwd_blank.send_keys("test")
        pwd_blank = self.driver.find_element(By.XPATH, "//input[@id = \"password\"]")       # 再次抓取元素

        for i in pwd:
            pwd_blank.send_keys(i)
            result = {}
            result["time_needed"] = self.driver.find_element(By.XPATH, TIME_PATH).text
    
            suggestions = [i.text for i in self.driver.find_elements(By.XPATH, SUGGESTION_PATH) if i.text != "Top Tip: Protect Yourself"][:-1]
            result["Suggestion"] = suggestions
            
            if not self.result.get(i):
                self.result[i] = {}
            self.result[i]["security"] = result
            pwd_blank.clear()
        

    def get_response_pwd_meter(self, pwd:list[int]):
        self.driver.get(HTTP_ADDRESS_PWDMETER)
        time.sleep(1)

        pwd_blank = self.driver.find_element(By.XPATH, "//input[@type=\"password\"]")
        
        for i in pwd:
            pwd_blank.send_keys(i)

            result = {}
            pwd_score = self.driver.find_element(By.XPATH, "//div[@id=\"score\"]").text
            pwd_complexity = self.driver.find_element(By.XPATH, "//div[@id=\"complexity\"]").text

            result["pwd_score"] = pwd_score
            result["pwd_complexity"] = pwd_complexity
            
            if not self.result.get(i):
                self.result[i] = {}
            self.result[i]["pwd_meter"] = result

            pwd_blank.clear()

    
    def do_score(self, pwd):
        self.get_response_sec(pwd)
        self.get_response_pwd_meter(pwd)
        
        self.driver.quit()

    def get_result(self) -> dict:
        with open(r"CNIT270_Password_Strength\pwd_strength_text.json", "wb") as file:
            self.result = json.dumps(self.result, indent = 4)
            file.write(str(self.result).encode(encoding="UTF-8"))
        return self.result

    


if __name__ == "__main__":
    # test_pwd = !*bfBA7ASD(p
    path = r"E:\aHomework\Purdue\2024 Fall\CNIT 270\Week 2\tenthousandpasswords.txt"
    test_pwd = Passwords(path)
    test = SendRequest()
    test.do_score(test_pwd.get_result(5))    
    test.get_result()
