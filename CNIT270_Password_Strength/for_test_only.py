"""
This program suppose to select 5 passwords randomly from the given txt file, and 
"""
import random

class Passwords():
    def __init__(self, provided_file:str, amount:int) -> None:
        """
        provided_file is a real string of file path
        amount is the amount of lines we need from the file
        """
        self.passwords = {}
        with open(provided_file, "r") as file:
            results = random.sample(file.readlines(), amount)

        for i in range(len(results)):
            self.passwords[results[i][:-1]] = None

    def get_result(self) -> list[int]:
        return self.passwords
    
    


if __name__ == "__main__":
    path = r"E:\aHomework\Purdue\2024 Fall\CNIT 270\Week 2\tenthousandpasswords.txt"
    test = Passwords(path, 10)
    print(test.get_result())
