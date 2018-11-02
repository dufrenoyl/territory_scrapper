import FunctionKayak
import ParsingAirlines
import sys
import csv
import time
import urllib2
#import bs4 as BeautifulSoup
import BeautifulSoup
import webbrowser
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
#from pyvirtualdisplay import Display
from selenium import webdriver
import datetime
import traceback

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
	


if __name__ == '__main__':

	#We get the time of our system for each search flight
	DateTimesys = datetime.datetime.now()
	
	#We generate the name for the Log file
	Namelogfile="log_"+str(DateTimesys.date())+"_"+str(DateTimesys.time())+".txt"

	#We generate the name for the Error file
	Nameerrfile="err_"+str(DateTimesys.date())+"_"+str(DateTimesys.time())+".txt"

	#Browser file used to save the browser source when an error occured
	Namebrowfile = "HTMLFile_"+str(DateTimesys.date())+"_"+str(DateTimesys.time())+".txt"	

	odList = {} # contains all OnD/Date retrieved from the input file
	odLine = {} # used as we process OnDs one by one

	if (len(sys.argv) != 4):
          print "Not enough parameters: "+str(len(sys.argv))
          exit(0)
	fileName = sys.argv[1]  #OnD file
	fileNameParse = sys.argv[2] #Parser file
	system = sys.argv[3]    #system to consider: AMADEUS,ITA or All

	odList,company,Stop = FunctionKayak.odfile(fileName)
	NameAirline, NameParser = FunctionKayak.parseAirlinefile(fileNameParse)

	#methodparsing is a Python dico used for Bad click access
	#it associates the Airleine name with the Python method to execute to parse the airline website
	methodparsing = {}
	for i in range(len(NameParser)):
		methodparsing[NameAirline[i]] = getattr(ParsingAirlines,NameParser[NameAirline[i]])
		print methodparsing[NameAirline[i]]
	
	print NameAirline
	print NameParser

        #We connect to the database
	con=FunctionKayak.DBConnect('localhost','lucas','lucas','kayak')

	# we loop on all ODs contained in the Input file
	for rr in range(len(odList)):

		#We verify that the each OnD/Date line is correct
		odLine = odList[rr]
		if (len(odLine["date"])>0 and len(odLine["origin"])>0 and len(odLine["destination"])>0):		
			print odLine
			j=0
			start = time.time()
			try:

				#We open the log file
				logfile = open(Namelogfile, 'w')

				#We open two browsers ; one for Kayak and one for Badclick accesses
				profileH = setHeaders()
				browser = webdriver.Firefox(profileH)
				profileH = setHeaders()
				browser2 = webdriver.Firefox(profileH)

				#We call the main function to process one OnD/Date
				FunctionKayak.Search_data(browser, browser2, odLine, logfile, Namebrowfile, company, Stop, system, con, DateTimesys, methodparsing)

				#We will close all popups
				close_all_popups(browser)
				close_all_popups(browser2)
				browser.close()
				browser2.close()

			except Exception as ex:

				#We log in the error file in case of error
				tb = traceback.format_exc()
				errfile = open(Nameerrfile, 'a')
				errfile.write(str(odLine))
				errfile.write('\n')
				errfile.write(str(ex)+tb)
				errfile.write('\n')
				errfile.close()

                                #log browser source if error
				FunctionKayak.printPage(browser,"",Namebrowfile)
				close_all_popups(browser)
				close_all_popups(browser2)
				browser.close()
				browser2.close()
				continue

			print "Time spent : "+ str(time.time() - start)

	con.close()

