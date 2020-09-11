from gazpacho import Soup
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
import time


url = "https://www.instagram.com/"
browser = webdriver.Chrome(executable_path="/mnt/l/projects/instagram-data/scraper/chromedriver.exe")
browser.get(url)
browser.implicitly_wait(5)

username = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
password = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
username.send_keys("jamie_karam")
password.send_keys("1234567")




