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


# def click_not_now():
#     not_now = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
#     browser.implicitly_wait(5)
#     not_now.click()

def click_not_now_again():
    not_now = browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
    browser.implicitly_wait(5)
    not_now.click()

def grab_all_posts():
    posts = browser.find_elements_by_class_name('_8Rm4L')
    return posts

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

def scrape_time_posted(element):
    soup = Soup(element.get_attribute("innerHTML"))
    time_posted = soup.find('time').attrs["datetime"]
    post_id = soup.find('a', {'class': 'c-Yi7'}).attrs["href"]
    user_id = soup.find('a', {'class': 'sqdOP'}).attrs["href"]
    comments =  soup.find('a', {'class': 'r8ZrO'}).find('span').text if soup.find('a', {'class': 'r8ZrO'}) else None
    try:
        likes = soup.find('div', {'class': 'Nm9Fw'}).find("span").text
    except:
        likes = None
    return {  "likes" : likes, "comments": comments, "post_id" : post_id,  "time_posted" : time_posted, "user_id" : user_id}

# scroll down to load different components into dom
def scroll_down():
    for _ in range(2):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

def get_ids(list1):
    id_list = []
    for item in list1:
        id_list.append(item.id)
    return id_list

login()
# click_not_now()
click_not_now_again()


data = []
for _ in tqdm(range(5)):
    if _ != 0: scroll_down()
    posts = grab_all_posts()
    for post in posts:
        user_info = scrape_time_posted(post)
        browser.execute_script(f"window.open('{user_info['user_id']}', '_blank')")
        browser.switch_to.window(browser.window_handles[-1])
        time.sleep(1)
        more_info = scrape_user_page()
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        browser.window_handles.pop()
        data.append({**user_info, **more_info, "time_scraped": format(datetime.datetime.now())})

browser.quit()

def remove_dupicates(arr):
    output = []
    for post in arr:
        if post["post_id"] in output:
            pass
        output.append(post)
    return output



df = pd.DataFrame(remove_dupicates(data))
df.to_csv(f'./csvs/{datetime.datetime.now()}.csv')
df.to_csv('./csvs/instagram_master.csv', mode='a', header=False)