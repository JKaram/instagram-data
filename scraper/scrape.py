from gazpacho import Soup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
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
posts = browser.find_elements_by_class_name('_8Rm4L')

def scrape_posts(post):
    # grab full post HTML
    article_innerHTML = post.get_attribute('innerHTML')
    soup = Soup(article_innerHTML)
    # grab likes for the post
    likes = soup.find('button', {'class': 'sqdOP'})[0].find('span').text
    time_posted = soup.find('time').attrs["datetime"]
    # grab comments for the post
    find_comments = browser.find_element_by_class_name('r8ZrO').get_attribute('innerHTML')
    soup = Soup(find_comments)
    comments = soup.find('span').text
    now = datetime.datetime.now()
    time.sleep(2)
    addtional_info = post.find_element_by_class_name('Jv7Aj')
    action.move_to_element(addtional_info).perform()
    modal = browser.find_element_by_class_name('GdeD6')
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
    # # grab return post info
    return {
        "likes": likes,
        "comments" : comments,
       "time_posted" : time_posted,
        "username": username,
        "is_verified":is_verified,
        "total_posts": total_posts,
        "followers": followers,
        "following": following,
        "time_scraped": now.strftime("%Y-%m-%d %H:%M:%S")
        }

for post in posts:
  print(scrape_posts(post))
  time.sleep(2)