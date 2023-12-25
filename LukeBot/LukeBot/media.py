import random
from selenium import webdriver
from selenium.webdriver.common.by import By

def getGIF(inputStr: str) -> str: # Function for grabbing random gif given string
    inputStr = inputStr.replace(' ', '-') # spaces become %20 in image search. ############### LATER SHOULD IMPLEMENT MORE SUCH AS '+' ##############
    
    driver = webdriver.Chrome()
    driver.get("https://tenor.com/search/" + inputStr + "-gifs")
    
    links = [f"{img.get_attribute('src')}" for img in driver.find_elements(By.XPATH, "//div[@class='Gif']//img[@src]")] # grabs all links on first page of imgur search
    driver.quit()
    return random.choice(links)
    