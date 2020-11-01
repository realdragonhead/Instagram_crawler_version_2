import re
import sys
import csv
import time
import urllib.request
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#---- Function list
#----  1. get_user_name(driver)
#----  2. get_post_link(driver)
#----  3. get_post_id(document_link)
#----  4. get_post_date(driver)
#----  5. get_user_locs(driver)
#----  6. get_post_tags(driver)
#----  7. get_post_content(driver)
#----  8. get_post_like(driver)
#----  9. cut_user_name(driver)
#---- 10. remove_hashtag(target_list)

# Extract user's name
def get_user_name(driver):
	try:
		target = driver.find_element_by_css_selector('.sqdOP.yWX7d._8A5w5.ZIAjV')
		name_result = target.get_attribute('href')
		return name_result
	except:
		return " "

# Extract post's link
def get_post_link(driver):
	try:
		target = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a')
		link_result = target.get_attribute('href')
		return link_result 
	except:
		return " "

# Extract document id from post's link
def get_post_id(document_link):
	try:
		document_id = document_link.replace('https://www.instagram.com/p/', '')
		document_id = document_id.replace('/', '')
		return document_id
	except:
		return " "

# Extract post's uploaded date
def get_post_date(driver):
	try:
		target = driver.find_element_by_css_selector('time.FH9sR.Nzb55')
		date_result = target.get_attribute('datetime')
		date_result = date_result.replace('-', '')
		date_result = date_result.replace('T', '')
		date_result = date_result.replace(':', '')
		date_result = date_result.replace('.000Z', '')
		return date_result 
	except:
		return " "

# Extract user's location
def get_user_locs(driver):
	try:
		target = driver.find_element_by_css_selector('a.O4GlU')
		locs_result = target.get_attribute('text')
		return locs_result
	except:
		return " "

# Extract post's tag's in array
def get_post_tags(driver):
	try:
		target = driver.find_element_by_css_selector('.C7I1f.X7jCj')
		target_html = target.get_attribute('innerHTML')
		tagslist = re.findall('#[A-Za-z0-9가-힣]+', target_html)
		tags_result = remove_hashtag(tagslist)
		return tags_result
	except:
		return " "

# Extract all content in post
def get_post_content(driver):
	try:
		target = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span')
		post_content = target.text
		return post_content
	except:
		return " "
	

# Extract user's name from user's profile linke
def cut_user_name(name):
	return name[26:-1]

# Remove hashtag simbol in text
def remove_hashtag(target_list):
	removed_result  = []
	tags_temp = ''.join(target_list).replace("#", " ")
	tags_temps = tags_temp.split(" ")
	for tag in tags_temps:
		removed_result.append(tag)
	return removed_result

