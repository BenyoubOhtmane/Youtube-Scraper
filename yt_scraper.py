# -*- coding: utf-8 -*-
from selenium import webdriver
from random import randint,shuffle
import requests
from bs4 import BeautifulSoup
import time
import threading
from tkinter import *
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
import csv
def set_browser():
    chromeOptions = webdriver.ChromeOptions()
    #Removing img/notifications for less CPU-usage
    prefs = {"profile.managed_default_content_settings.images": 2,"profile.default_content_setting_values.notifications": 1 }
    chromeOptions.add_experimental_option("prefs", prefs)
    chromeOptions.add_argument("--log-level=3")
    #Headless mode
    chromeOptions.add_argument("--headless")
    driver=webdriver.Chrome(executable_path="driver/chromedriver",options=chromeOptions)
    return driver
def scrape_ch(url,driver):
    driver.get(url)
    time.sleep(3)
    el=driver.find_elements_by_xpath('//*[@id="video-title"]')
    urls_len=0
    ccc=0
    while True:
        driver.execute_script("arguments[0].scrollIntoView();", el[len(el)-1])
        el=driver.find_elements_by_xpath('//*[@id="video-title"]')
        if urls_len==len(el):
            if ccc==50:
                break
            else:
                ccc=ccc+1
            
        else:
            urls_len=len(el)
            ccc=0
        print(urls_len)
    urls=[]
    for i in el:
        urls.append(i.get_attribute("href"))
    return urls
def main(accounts):
    ch_count_=10 #How many threads ..
    dd=0
    ccp=0
    def setup(account):
        try:
            print("Scraping url...")
            driver=set_browser()
            wait = WebDriverWait(driver, 10)
            driver.get(account)
            v_title = wait.until(EC.presence_of_element_located((By.XPATH,"//h1[@class='title style-scope ytd-video-primary-info-renderer']"))).text
            v_views = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-view-count-renderer span.view-count.style-scope.yt-view-count-renderer"))).text
            v_likes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text.style-scope.ytd-toggle-button-renderer.style-text"))).get_attribute("aria-label")
            #v_pub = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.date.style-scope.ytd-video-secondary-info-renderer"))).text
            #v_desc = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.content.style-scope.ytd-video-secondary-info-renderer"))).text
            v_dislikes = driver.find_elements_by_xpath('//yt-formatted-string[@id= "text" and @class = "style-scope ytd-toggle-button-renderer style-text"]')[1].get_attribute("aria-label")
            print("Session finished .... !",v_title,v_views,v_likes,v_dislikes)
            driver.quit()
            with open("output.csv", "a",encoding="utf-8") as fp:
                wr = csv.writer(fp)
                wr.writerow([v_title,v_views,v_likes,v_dislikes,account])
        except Exception as e:
            try:
                driver.quit()
            except:
                pass
            setup(account)
            pass

    while ccp+ch_count_ <= len(accounts)-1:
        accounti=accounts[ccp:ccp+ch_count_]
        threads = [threading.Thread(target=setup, args=(rl,)) for rl in accounti]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        ccp=ccp+ch_count_
    else:
        accounti=accounts[ccp:]
        threads = [threading.Thread(target=setup, args=(rl,)) for rl in accounti]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        ccp=ccp+ch_count_
        pass
if __name__=="__main__":
    driver=set_browser()
    urls=scrape_ch("https://www.youtube.com/user/MrBeast6000/videos",driver) #Scrape_ch , does scrape urls for all videos in this user's channel
    driver.quit()
    print("Starting now--")
    main(urls) #The main funtion , does check each video url in urls , and does collect data then store them in a csv file (Multithreading)