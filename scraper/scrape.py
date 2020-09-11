from gazpacho import Soup
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
import time


url = "https://www.instagram.com/"
browser = webdriver.Chrome(executable_path="/mnt/l/projects/instagram-data/scraper/chromedriver.exe")
browser.get(url)
html = browser.page_source
soup = Soup(html)

username = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
username.send_keys("jamie_karam")




