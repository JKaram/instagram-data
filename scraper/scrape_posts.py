from selenium.webdriver.common.action_chains import ActionChains
import datetime
import os
import pandas as pd
from gazpacho import Soup
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


url = "https://www.instagram.com/"
profile = "https://www.instagram.com/justinbieber/"
browser = webdriver.Chrome(executable_path="./scraper/chromedriver")

action = ActionChains(browser)

browser.get(url)

def login():
    browser.implicitly_wait(5)
    username = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    password = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    login = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
    username.send_keys("tim_stan_man")
    password.send_keys("123456789!")
    login.click()

def click_not_now_again():
    not_now = browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
    browser.implicitly_wait(5)
    not_now.click()

def scrape_user_page():
    posts = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text
    followers = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute("title")
    following = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text
    try:
        browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span')
        verified = True
    except:
        verified = False
    return {  "followers" : followers, "following": following, "posts": posts, "verified" : verified}


login()
click_not_now_again()
browser.get("https://www.instagram.com/justinbieber/")
profile = scrape_user_page()
time.sleep(2)


# Find First Post ID
def get_first_post_id():
    first_post = browser.find_element_by_class_name('v1Nh3')
    soup = Soup(first_post.get_attribute("innerHTML"))
    return soup.find('a').attrs["href"]

initial_first_post = get_first_post_id()
new_post_id = initial_first_post

while initial_first_post == new_post_id:
    new_post_id = get_first_post_id()
    time.sleep(10)
    browser.refresh()

browser.get(f"https://www.instagram.com{new_post_id}")
date_posted = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[2]/a/time').get_attribute("datetime")
user_name = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/header/div[2]/div[1]/div/span/a').get_attribute("href")

data = []
# Refresh every minute for 6 hours
for _ in tqdm(range(360)):
    time.sleep(1)
    likes = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/div/a/span').text
    time.sleep(59)
    data.append({"likes" : likes, "time_scraped": format(datetime.datetime.now()), "date_posted" : date_posted, "user_name" : user_name ,"post_id": new_post_id ,**profile})
    browser.refresh()

browser.quit()

df = pd.DataFrame(data)
df.to_csv(f'./csvs/{user_name}_{new_post_id[3:-1]}.csv')
