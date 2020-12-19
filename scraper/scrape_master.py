from selenium.webdriver.common.action_chains import ActionChains
import datetime
import os
import pandas as pd
import time
from tqdm import tqdm
from selenium import webdriver


url = "https://www.instagram.com/"
browser = webdriver.Chrome(executable_path="./scraper/chromedriver.exe")
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


def click_not_now():
    not_now = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
    browser.implicitly_wait(5)
    not_now.click()

def click_not_now_again():
    not_now = browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
    browser.implicitly_wait(5)
    not_now.click()

def grab_all_posts():
    posts = browser.find_elements_by_class_name('_8Rm4L')
    return posts

def scrape_modal(post):
    posts = post.find_element_by_xpath('//div/div/div[2]/div/div/div[1]/span/span').text
    followers = post.find_element_by_xpath('//div/div/div[2]/div/div/div[2]/span/span').get_attribute("title")
    following = post.find_element_by_xpath('//div/div/div[2]/div/div/div[3]/span/span').text
    username = post.find_element_by_xpath('//header/div[2]/div[1]/div/span/a').text
    verified = True if post.find_element_by_xpath('//div/div/div[1]/div/div/div[1]/a/div/span') else False
    return {"followers" : followers, "verified": verified, "following": following, "posts": posts, "username": username}

def scrape_likes_comments(post):
    likes =  post.find_element_by_xpath('//div[3]/section[2]/div/div/button/span').text
    comments = post.find_element_by_xpath('//div[3]/div[1]/div/div[2]/div[1]/a/span').text if post.find_element_by_xpath('//div[3]/div[1]/div/div[2]/div[1]/a/span') else "None"
    post_id = post.find_element_by_xpath('//div[3]/div[2]/a').get_attribute("href")
    timestamp = post.find_element_by_xpath('//div[3]/div[2]/a/time').get_attribute("datetime")
    return {"likes": likes, "comments" : comments, "post_id" : post_id, "time_posted" : timestamp }

login()
click_not_now()
click_not_now_again()
posts = browser.find_elements_by_class_name('_8Rm4L')
browser.implicitly_wait(5)
instalogo = browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a/div/div/img')

for post in posts:
    print(post.location)

# for post in tqdm(posts):
#     addtional_info = post.find_element_by_class_name('Jv7Aj')
#     action.move_to_element(addtional_info).perform()
#     modal = browser.find_element_by_class_name('GdeD6')
#     posts_and_followers = scrape_modal(modal)
#     likes_and_comments = scrape_likes_comments(post)
#     action.move_to_element(instalogo).perform()
#     print({**likes_and_comments, **posts_and_followers})














