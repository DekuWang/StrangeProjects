"""
This program suppose to select 5 passwords randomly from the given txt file, and 
"""
import random
import time
import json
from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service

HTTP_ADDRESS = r"https://www.security.org/how-secure-is-my-password/"
BROWSER_USER_DATA = r"C:/Users/97456/AppData/Local/Google/Chrome/User Data/"

############BROWSER SETUP###############
chromeOptions = wb.ChromeOptions()
chromeOptions.add_argument('--ignore-certificate-errors-spki-list')
chromeOptions.add_argument("--user-data-dir=" + BROWSER_USER_DATA)
chromeOptions.add_argument("--profile-directory=Default")
#########BROWSER SETUP END##############

RESULT_FORMAT = {
    "time_needed": None,
    "Suggestion": None
    }

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
        self.driver.get(HTTP_ADDRESS)
        self.driver.implicitly_wait(5)
        self.driverAction = ActionChains(self.driver)
        self.result = {}
    
    def get_response(self, pwd:list[int]):
        """
        This func is goal to fill the pwd blank and get the result of it.
        """
        pwd_blank = self.driver.find_element(By.XPATH, "//input[@id = \"password\"]")       # 第一遍会丢失元素
        pwd_blank.send_keys("test")
        pwd_blank = self.driver.find_element(By.XPATH, "//input[@id = \"password\"]")       # 再次抓取元素


        while pwd:
            current_pwd = pwd.pop()
            pwd_blank.clear()
            pwd_blank.send_keys(current_pwd)
            result = RESULT_FORMAT.copy()
            result["time_needed"] = self.driver.find_element(By.XPATH, TIME_PATH).text
    
            suggestions = [i.text if i.text != "Top Tip: Protect Yourself" else None for i in self.driver.find_elements(By.XPATH, SUGGESTION_PATH)][:-1]
            result["Suggestion"] = suggestions

            self.result[current_pwd] = result
            time.sleep(1)

        self.driver.quit()

    def get_result(self) -> dict:
        with open("pwd_strength_text.json", "wb") as file:
            self.result = json.dumps(self.result, indent = 2)
            file.write(str(self.result).encode(encoding="UTF-8"))
        return self.result

    


if __name__ == "__main__":
    # test_pwd = !*bfBA7ASD(p
    path = r"E:\aHomework\Purdue\2024 Fall\CNIT 270\Week 2\tenthousandpasswords.txt"
    test_pwd = Passwords(path)
    test = SendRequest()
    test.get_response(test_pwd.get_result(5))    
    test.get_result()
