from selenium.webdriver.common.action_chains import ActionChains
import datetime
import os
import pandas as pd
from gazpacho import Soup
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

def scrape_modal(element):
    posts = element.find_element_by_xpath('//div/div/div[2]/div/div/div[1]/span/span').text
    followers = element.find_element_by_xpath('//div/div/div[2]/div/div/div[2]/span/span').get_attribute("title")
    following = element.find_element_by_xpath('//div/div/div[2]/div/div/div[3]/span/span').text
    username = element.find_element_by_xpath('//header/div[2]/div[1]/div/span/a').text
    try:
        post.find_element_by_xpath('//div/div/div[1]/div/div/div[1]/a/div/span')
        verified = True
    except:
        verified = False
    return {"followers" : followers, "following": following, "posts": posts, "username": username, "verified" : verified}

def scrape_likes_comments(element):
    soup = Soup(element.get_attribute("innerHTML"))
    try:
        likes = soup.find('div', {'class': 'Nm9Fw'}).find("button").find("span").text
    except:
        likes = None
    time_posted = soup.find('time').attrs["datetime"]
    comments =  soup.find('a', {'class': 'r8ZrO'}).find('span').text if soup.find('a', {'class': 'r8ZrO'}) else None
    post_id = soup.find('a', {'class': 'c-Yi7'}).attrs["href"]
    return {"likes": likes, "comments" : comments, "time_posted" : time_posted , "post_id" : post_id}

# scroll down to load different components into dom
def scroll_down():
    for _ in range(1):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

def get_ids(list1):
    id_list = []
    for item in list1:
        id_list.append(item.id)
    return id_list

login()
click_not_now()
click_not_now_again()
instalogo = browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a/div/div/img')
scraped_already = []
csv = []


get_ids(grab_all_posts())


for _ in range(2):
    all_posts = grab_all_posts()
    print(scraped_already)
    for post in tqdm(all_posts):
        browser.execute_script("arguments[0].scrollIntoView();", post)
        print("scroll into view")
        time.sleep(1)
        if post.id in scraped_already:
            print("Match")
            pass
        else:
            try:
                likes_and_comments = scrape_likes_comments(post)
                print("likes and comments")
                time.sleep(1)
                addtional_info = post.find_element_by_class_name('Jv7Aj')
                print("additional info")
                time.sleep(1)
                action.move_to_element(addtional_info).perform()
                print("move to link")
                time.sleep(1)
                browser.implicitly_wait(1)
                modal = browser.find_element_by_class_name('GdeD6')
                print("find modal")
                time.sleep(1)
                action.move_to_element(post).perform()
                print("move off element")
                time.sleep(1)
                posts_and_followers = scrape_modal(post)
                print("scrape modal")
                time.sleep(1)

                csv.append({**likes_and_comments, **posts_and_followers})
            except:
                print("error")
                pass
    scraped_already.extend(get_ids(all_posts))



for _ in csv:
    print(_)

















