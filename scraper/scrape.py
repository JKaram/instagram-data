from gazpacho import Soup
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import os




url = "https://www.instagram.com/"
browser = webdriver.Chrome(executable_path="./scraper/chromedriver.exe")
browser.get(url)
browser.implicitly_wait(5)

username = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
password = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
login = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
username.send_keys("")
time.sleep(1)
password.send_keys("")
time.sleep(2)
login.click()


