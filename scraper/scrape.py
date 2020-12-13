from gazpacho import Soup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os




url = "https://www.instagram.com/"
browser = webdriver.Chrome(executable_path="./scraper/chromedriver.exe")
action = ActionChains(browser)


browser.get(url)
browser.implicitly_wait(5)

username = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
password = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
login = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
username.send_keys("tim_stan_man")
password.send_keys("123456789!")
time.sleep(2)
login.click()
time.sleep(6)
# Target userimage
content = browser.find_element_by_class_name('Jv7Aj')
time.sleep(2)
# hover image and reveal modal
action.move_to_element(content).perform()
# target modal
modal = browser.find_element_by_class_name('GdeD6')
# grab innerHTML from modal
innerHTML = modal.get_attribute('innerHTML')
#convert to soup HTML
soup = Soup(innerHTML)
# grab username
username = soup.find('a', {'class': 'FPmhX'}).text
# grab list of user details
account_details = soup.find('span', {'class': 'g47SY'})
# save deatils in variables
total_posts = account_details[0].text
followers = account_details[1].attrs["title"]
following = account_details[2].text

# check if verified
is_verified = True
if soup.find('span', {'class': 'mTLOB'}) == None:
     is_verified = False

# grab likes for the post
find_likes = browser.find_element_by_class_name('Nm9Fw').get_attribute('innerHTML')
soup = Soup(find_likes)
likes = soup.find('span').text



print(is_verified)

