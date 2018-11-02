import sys
import urllib2
import webbrowser
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import datetime
import traceback
import FunctionTerritory

headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0''Mozilla/5.0' }
def setHeaders():
	profile = webdriver.FirefoxProfile()
	print profile	
	profile.set_preference("general.useragent.override",headers["User-Agent"])
	return profile

#Function to close all popups
def close_all_popups(driver):
	driver.window_handles
	for h in driver.window_handles[1:]:
		driver.switch_to_window(h)
		driver.close()
	driver.switch_to_window(driver.window_handles[0])
	

#Main Function
if __name__ == '__main__':

	#We get the time of our system for each search flight
	DateTimesys = datetime.datetime.now()
	
	#We generate the name for the Log file
	Namelogfile="log_"+str(DateTimesys.date())+"_"+str(DateTimesys.time())+".txt"

    #We connect to the database
	con=FunctionTerritory.DBConnect('localhost','boston','boston','TerritoryManager')
	
	#We open the log file
	logfile = open(Namelogfile, 'w')
	
	#We open two browsers ; one for Kayak and one for Badclick accesses
	profileH = setHeaders()
	browser = webdriver.Firefox(profileH)
	
	#We call the main function to process one OnD/Date
	FunctionTerritory.Search_data(browser, logfile, con, DateTimesys)

	#We will close all popups
	close_all_popups(browser)
				
	browser.close()
	con.close()


