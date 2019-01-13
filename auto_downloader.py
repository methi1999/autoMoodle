#import packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import os
import pickle
import json
import shutil

#load config file

try:
	with open('config.json','r') as f:
		data_in = json.load(f)

	username = data_in["username"]
	password = data_in["password"]
	to_save = data_in["to_save"]
	base_path = data_in["base_path"]
	temp = data_in["temp"]

	if temp == '.':
		temp = base_path+'/temp'

	if data_in['reset'] == 'True':
		if os.path.exists(temp):
			shutil.rmtree(temp)
		print("Starting from scratch")

except:
	print("Couldn't find config file")
	exit(0)

#make folders

if not os.path.exists(base_path):
	os.mkdir(base_path)

if not os.path.exists(temp):
	os.mkdir(temp)

for course in to_save:
	if not os.path.exists(base_path+'/'+course):
		os.mkdir(base_path+'/'+course)

#initialise browser

def enable_download_in_headless_chrome(driver, download_dir):
	driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

	params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
	command_result = driver.execute("send_command", params)

opt = Options()
opt.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=opt)
enable_download_in_headless_chrome(driver=browser, download_dir=temp)

browser.get('http://moodle.iitb.ac.in/login/index.php')

#sign-In

try:
	userElem = browser.find_element_by_id('username')
	userElem.send_keys(username)
	passElem = browser.find_element_by_id('password')
	passElem.send_keys(password)
	passElem.submit()
	
	if len(browser.find_elements_by_id('username')):
		print("Login failed. Check credentials again")
		exit(0)
	else:
		print("Successfully logged in!")
	
except:
	print("Error occured while logging in")
	exit(0)

#load links

if os.path.exists(temp+'/links.p'):

	with open(temp+'/links.p', 'rb') as f:
		links = pickle.load(f)
	print("Read course links from dump")

else:

	links = {}
	courses = browser.find_elements_by_class_name('coursename')
	# print(courses)

	for course in courses:

		html = course.get_attribute('outerHTML')
		attrs = BeautifulSoup(html, 'html.parser').a.attrs
		if course.text[:6] in to_save:
			links[course.text[:6]] = attrs['href']

	print("Dumping course links")
	with open(temp+'/'+'links.p', 'wb') as f:
		pickle.dump(links, f)

#check for already downloaded

if os.path.exists(temp+'/already_downloaded.p'):
	with open(temp+'/already_downloaded.p', 'rb') as f:
		already = pickle.load(f)
	print("Read already downloaded files from dump")
	# print(already)

else:
	already = {}
	for course in to_save:
		already[course] = []

#download		

for course_name, link in links.items():
	
	print("Current course:", course_name)
	params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': os.path.join(base_path, course_name)}}
	browser.execute("send_command", params)
	browser.get(link)

	files = browser.find_elements_by_class_name('instancename')

	# files[0].click()

	# discussions = browser.find_elements_by_class_name('author')
	
	# for discussion in discussions:
	# 	discussion.click()
	# 	attach = browser.find_elements_by_class_name('attachments')
	# 	print(len(attach))

	# browser.back()

	for file in files[1:]:
		
		inner = file.get_attribute('innerHTML')

		try:
			file_type = inner.split('>')[1].split('<')[0][1:]
		except:
			continue
		
		if file_type == 'File':

			if file.text not in already[course_name]:
				
				try:
					file.click()
					already[course_name].append(file.text)
					print("Saved:",file.text)
				except:
					print("Couldn't save",file.text)
			else:
				print("Found already downloaded", file.text)
		else:

			print("Not a file")
			
with open(temp+'/'+'already_downloaded.p', 'wb') as f:
	pickle.dump(already, f)
print("Dumped downloaded")