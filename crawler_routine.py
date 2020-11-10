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
import datetime
import re
import pandas as pd
import csv
import ins
import sys
import os

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
keyword = sys.argv[1]	### type keyword without spacing

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

try:
	folder_path = "../SCD/" + keyword
	if not(os.path.exists(folder_path)):
		os.makedirs(folder_path)
except OSError:
	print('Error: Cannot creating directory path is ' + folder_path)

for i in range(30):
	#---- variable list
	#----  1. pname : User's name
	#----  2. purls : User's profile link
	#----  3. plink : Post's link
	#----  4. pdate : Every single post uploaded date
	#----  6. ulocs : User's posting location
	#----  7. ptags : Tags data set every single post
	#----  8. pcont : Post's content
	#----  9. plike : Post's like count
	#---- 10. docid : Document id
	#---- 11. cdate : crawled date

	#  suggestion
	#  <DOCID>			------------>	<docid>
	#  <SOURCE>			------------>	"SNS"
	#  <SECTION>		------------>	"Instagram"
	#  <KEYWORD>		------------>	<ptags> except "'" and "," and "[" and "]"
	#  <REF_URL>		------------>	https://www.instagram.com/explore/tags/<keyword>
	#  <URL>			------------>	<plink>
	#  <TITLE>			------------>	?
	#  <CONTENT>		------------>	<ucont>
	#  <PUBLISHER>		------------>	<pname>
	#  <PUBLISH_DT>		------------>	<pdate>
	#  <CRAWL_DT>		------------>	<cdate>
	#  <ATTACH_NAME>	------------>	image url -> problem : expire problem
	#  <ATTACH_CONTENT> ------------>	
	#  <TERMS>			------------>	?
	
	#<< initialize variable for write >>#
	docid = ''
	source = ''
	ref_url = ''
	title = ''
	attach_name = ''

	try:
		exist = 0
		#<< Saving process >>#
		csv_text = []
		csv_text.append(i)

		#<sub< Get post's url and extracting document id from url >>#
		plink = ins.get_post_link(driver)	# Get post's url
		docid = ins.get_post_id(plink)		# Extracting docid from url
		csv_text.append(docid)

		#<< File open and check same docid >>#
		file_name = "../SCD/" + keyword + "/" + docid + ".SCD"
		if not(os.path.isfile(file_name)):
			new_file = open(file_name, 'w')
		else:
			exist = 1

		print("Document id is ", docid)

		#<<< Step 1 : Extract user's name >>>#
		print("Extracting", i, "post's user name and user profile link...")
		time.sleep(3)
		purls = ins.get_user_name(driver)
		pname = ins.cut_user_name(purls)
		csv_text.append(pname)
		csv_text.append(purls)
		print("--------Publisher : ", pname)
		print("--------Publisher profile link : ", purls)
	
		#<<< Step 2 : Print post's link and extracted document id >>>#
		csv_text.append(plink)
		print("--------Post link : ", plink)
		print("--------Document id : ", docid)
	
		#<<< Step 3 : Extract post uploaded, crawled date and time >>>#
		pdate = ins.get_post_date(driver)
		csv_text.append(pdate)
		
		today = datetime.datetime.now()		# for extracting crawled date and time
		date_format = "%Y%m%d%H%M%S"
		cdate = today.strftime(date_format)
		csv_text.append(cdate)
		print("--------Publish date : ", pdate)
		print("--------Crawled date : ", cdate)
		
		#<<< Step 4 : Extract user's posting location >>>#
		plocs = ins.get_user_locs(driver)
		csv_text.append(plocs)
		print("--------Location : ", plocs)
		
		#<<< Step 5 : Extract post's like count >>>#
		plike = ins.get_post_like(driver)
		csv_text.append(plike)
		print("--------Like count : ", plike)
 	
		#<<< Step 6 : Extract tags >>>#
		ptags = ins.get_post_tags(driver)
		csv_text.append(ptags)
		print("--------Tags List")
		print(ptags)
		
		#<<< Step 7 : Extract content >>>#
		pcont = ins.get_post_content(driver)
		csv_text.append(pcont)
		print("--------Content")
		print(pcont)
		print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
		print("")
		print("")

		if (exist == 0):
			#<< Text preprocessing >>#
			docid = '<DOCID>' + docid + '\n'
			source = '<SOURCE>' + 'SNS' + '\n'
			section = '<SECTION>' + 'instagram' + '\n'
			implant_ptags = '<KEYWORD>' + ",".join(ptags) + '\n'
			ref_url = '<REF_URL>' + 'https://www.instagram.com/explore/tags/' + keyword + '\n'
			plink = '<URL>' + plink + '\n'
			title = '<TITLE>' + '\n'
			pcont = '<CONTENT>' + pcont + '\n'
			pname = '<PUBLISHER>' + pname + '\n'
			pdate = '<PUBLISH_DT>' + pdate + '\n'
			cdate = '<CRAWL_DT>' + cdate + '\n'
			attach_name = '<ATTACH_NAME>' + '' + '\n'
			plike = '<ATTACH_CONTENT>' + 'likes:' + plike
			
			#<< Saving to file >>#
			new_file.write(docid)
			new_file.write(source)
			new_file.write(section)
			new_file.write(implant_ptags)
			new_file.write(ref_url)
			new_file.write(plink)
			new_file.write(title)
			new_file.write(pcont)
			new_file.write(pname)
			new_file.write(pdate)
			new_file.write(cdate)
			new_file.write(attach_name)
			new_file.write(plike)
			
			new_file.close()
			#<< Skip if exist == 1 >>#
			

	except EOFError:
		#<< Extracting exception handler >>#
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
