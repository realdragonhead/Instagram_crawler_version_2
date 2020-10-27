### Code write date : 2020.09.28
### Tested Chrome version         85.0.4183.121
### Tested chromedriver version   same with browser
### Tested OS					  Windows, Mac OS

import requests
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import Request, urlopen
import time
import re
import pandas as pd
import csv
import ins
import sys

#*********************************** USAGE **************************************#
#--------------------------------------------------------------------------------#
#---- First of all set Chrome and chrome driver version same --------------------#
#---- Use "search" function in text editor to find 'quote' ----------------------#
#---- and then find 'instagram account' and set your instagram account ----------#
#---- Please set 'time sleeper' adequately to local computer network speed ------#
#---- 'instagram account' and 'time sleeper' is defined as 'quote' --------------#
#---- and put ins.py same directory with this code ------------------------------#
#--------------------------------------------------------------------------------#
#********************************************************************************#

#<< instagram account info handler >>#

InstaAccountFile = open("../password/password.csv", 'r', encoding='utf-8')
rdr = csv.reader(InstaAccountFile)
lines = InstaAccountFile.readlines()
account_index = []

#for i in lines: ### other way to read csv file
#	account_index.append(i)
#	print(i)

InstaAccountFile.close()

#<< Account Info >>#
# make password.csv file in ../password/
Instagram_id = lines[0]	### Essential
Instagram_pw = lines[1]	### Essential

#<< List defined >>#
tags_dataset = []	# for tags saving
csv_text = []		# for handle csv text

#<< Input string >>#
keyword = 'honda'	### type keyword without spacing
#index_num = sys.argv[2]

#%%%%%%%%
#&&&&&&&&	replace with automatic keyword input
#%%%$$%$$
#<< CSV reader function for getting search keyword >>#
## 작성해야됨

#<< Search target URL(Instagram) >>#
url = "https://www.instagram.com/explore/tags/{}/".format(keyword)

#<< To ignore certificate error >>
options = wd.ChromeOptions()
options.add_argument('ignore-certificate-errors')

#<< Web driver(Chromedriver) >>#
driver = wd.Chrome("./chromedriver/86.0.4240.22/chromedriver", chrome_options=options)
driver.get(url)

#<< Description >>#
print("###########################################################################")
print("#--v.0.02-----------------------------------------------------------------#")
print("#------------------------------ Instruction ------------------------------#")
print("#--- Hello, this is Instagram crawler, there is caution before run -------#")
print("#--- This program crawl location name, url, face, hashtag, uploaded date -#")
print("#--- AND DON'T USE ILLEGAL WAY. ------------------------------------------#")
print("#-----------------------------------------------------made by Dragonhead--#")
print("###########################################################################")
print(" ")
print(" ")
#<< Time sleeper(8sec) >>#
time.sleep(8)

#<< Popup remover >>#
try:
	if(driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div/div/button')!=None):
		driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div/div/button').click()	
except:
	print('There is no popup')

driver.find_element_by_css_selector('div.v1Nh3.kIKUG._bz0w').click()

#<< Login screen detector >>#
try:
	if(driver.find_element_by_name('username')!=None):
		ac = driver.find_element_by_name('username')	### Instagram ID insert
		ac.clear()
		ac.send_keys(Instagram_id)
		pw = driver.find_element_by_name('password')	### Instagram PW insert
		pw.clear()
		pw.send_keys(Instagram_pw)
	
		btn = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div[2]/div/div/div[1]/div/form/div[4]/button")
		btn.click()
		#<< time sleeper(10sec) >>#
		time.sleep(10)
	
except:
	print("---------------------------------------------------------------------------")
	print('-------------------- There is no login process ----------------------------')
	print("---------------------------------------------------------------------------")
	time.sleep(10)

#<< Login save screen handler >>#
try:
	driver.find_element_by_css_selector('button.sqdOP.yWX7d.y3zKF').click()
	time.sleep(6)
	driver.find_element_by_css_selector('div.v1Nh3.kIKUG._bz0w').click()
except:
	print("---------------------------------------------------------------------------")
	print("---------------------------------------------------------------------------")
	print('-------------------- There is no login save process -----------------------')
	print("---------------------------------------------------------------------------")
	print("---------------------------------------------------------------------------")
	
try:
	driver.find_element_by_css_selector('div.v1Nh3.kIKUG._bz0w').click()
except:
	print('no button')

try:
    if(driver.find_element_by_name('username')!=None):
        ac = driver.find_element_by_name('username')	### Instagram ID insert
        ac.clear()
        ac.send_keys(Instagram_id)
        pw = driver.find_element_by_name('password')	### Instagram PW insert
        pw.clear()
        pw.send_keys(Instagram_pw)

        btn = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div[2]/div/div/div[1]/div/form/div[4]/button")
        btn.click()
        #<< time sleeper(7sec) >>#
        time.sleep(7)

#<< Check there is no login screen >>#
except:
    print("---------------------------------------------------------------------------")
    print('-------------------- There is no login process ----------------------------')
    print("---------------------------------------------------------------------------")
    time.sleep(5)


for i in range(30):
	#---- variable list
	#---- 1. pname : User's name
	#---- 2. purls : User's profile link
	#---- 3. plink : Post's link
	#---- 4. pdate : Every single post uploaded date
	#---- 6. ulocs : User's posting location
	#---- 7. ptags : Tags data set every single post
	#---- 8. ucont : User content
	#---- 9. docid : Document id

	#<< time sleeper >>#
	try:
		#<< Saving process >>#
		#<<< Step 1 : Saving user's name >>>#
		csv_text = []
		csv_text.append(i)
		print(" ")
		print("saving", i, "post's user name and user profile link...")
		time.sleep(3)
		purls = ins.get_user_name(driver)
		pname = ins.cut_user_name(purls)
		csv_text.append(pname)
		csv_text.append(purls)
		print("--------user's name :", pname)
		print("--------user's profile linke :", purls)
	
		#<<< Step 2 : Saving post's link and Extracting document id >>>#
		print("saving", i, "post's link and document id...")
		plink = ins.get_post_link(driver)
		docid = ins.get_post_id(plink)
		csv_text.append(plink)
		csv_text.append(docid)
		print("--------user's post link :", plink)
		print("--------user's document id :", docid)
	
		#<<< Step 3 : Saving post update date >>>#
		print("saving", i, "post's update date...")
		pdate = ins.get_post_date(driver)
		csv_text.append(pdate)
		print("--------post is uploaded date :", pdate)
		
		#<<< Step 4 : Saving user's posting location >>>#
		print("saving", i, "post's location...")
		plocs = ins.get_user_locs(driver)
		csv_text.append(plocs)
		print("--------location :", plocs)
 	
		#<<< Step 5 : Saving tags >>>#
		print("saving", i, "post's tags")
		ptags = ins.get_post_tags(driver)
		csv_text.append(ptags)
		print("--------post's tags...", ptags)
		
		#<<< Step 6 : Saving content >>>#
		print("saving", i, "post's content")
		pcont = ins.get_post_content(driver)
		csv_text.append(pcont)
		print("--------post's content", pcont)
		print(" ")
		print(" ")

	except EOFError:
		#<< Saving exception handler >>#
		print('please input saving exception handler code')
		
	try:
		#<< Skip next page >>#
		WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a._65Bje.coreSpriteRightPaginationArrow')))
		driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()
	except:
		f.close()
		driver.close() 
	#<< Time sleeper >>#
	time.sleep(2)
driver.close()


