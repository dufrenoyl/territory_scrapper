#import bs4 as BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver import ActionChains
import MySQLdb as mdb


#those headers are added to avoid to be seen as a BOT by the Website
Territorykey = 'KBHCF2zy2ti9FdO9nvd8kA'
headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0''Mozilla/5.0' }


#------------------------------------
#Login Page
#------------------------------------

def LoginProcess(browser, idlogin, idpassword):
	#Locate Login+Password Input box
	inputLogin = browser.find_element_by_id("edit-name")
	inputPassword = browser.find_element_by_id("edit-pass")
	
	#Type in the Input Login
	inputLogin.send_keys(idlogin)
	inputPassword.send_keys(idpassword)
	
	browser.find_element_by_name("op").click()
	
	print browser.title
	
	try:
		#We have to wait for the login process to be done
		WebDriverWait(browser,10).until(EC.title_contains())
		
	finally:
		return 0
	

#-------------------------------------------------------------------------------------
#Main routine
#-------------------------------------------------------------------------------------
def Search_data(browser, logfile, con, DateTimesys):	

	cur=con.cursor()

	#We log 
	labellog = "INFORMATION SUR :" + str(result)
	LogPage(logfile, labellog, "")
	
	#We determine the right URL
	final_URL = Search_OD_Url(browser)
	print final_URL

	#We log the URL value
	labellog = "URL USED : "
	LogPage(logfile, labellog, str(final_URL))

	#We load the URL
	browser.get(final_url)

    #we wait for page to be loaded	
	time.sleep(2)
	
	#Connect into Login Page
	LoginProcess(browser,"boston","boston")



