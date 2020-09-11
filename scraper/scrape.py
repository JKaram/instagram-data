from gazpacho import Soup
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
import time


url = "https://www.instagram.com/itsborocoprunning/"
browser = webdriver.Firefox(executable_path="/mnt/l/projects/instagram-data/scrapper/geckodriver.exe")
browser.get(url)
html = browser.page_source
soup = Soup(html)