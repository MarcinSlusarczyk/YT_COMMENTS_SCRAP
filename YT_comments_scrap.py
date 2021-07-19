import string
import time
import re
import pandas as pd
import csv
from selenium import webdriver
URL = input("Wpisz link do filmu by pobrać komentarze:\n")
driver = webdriver.Chrome()
driver.get(URL)

acceptTerms = driver.find_element_by_xpath(
    '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button')
acceptTerms.click()

time.sleep(3)
 
video_titles = driver.find_elements_by_class_name('title')
for title in video_titles:
    print(title.text)
    tytul = title.text

name = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[9]/div[2]/ytd-video-secondary-info-renderer/div/div/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a').text
comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
driver.execute_script("arguments[0].scrollIntoView();", comment_section)
time.sleep(9)
last_height = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(5)
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    
driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  
                           u"\U0001F300-\U0001F5FF"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)

name_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
num_of_names = len(name_elems)
 
username = []
comment = []
for i in range(num_of_names):
    
    username.append(name_elems[i].text  )    
    comment.append(comment_elems[i].text )   
    
#generate csv
data = { 'username': username, 'comment': comment}
df_product = pd.DataFrame.from_dict(data)
df_product.to_csv(str(name) +'_komentarze.csv',  encoding='utf-8-sig')
