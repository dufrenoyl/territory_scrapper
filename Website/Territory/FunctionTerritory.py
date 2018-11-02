#import bs4 as BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver import ActionChains
import MySQLdb as mdb


#those headers are added to avoid to be seen as a BOT by the Website
Territorykey = 'KBHCF2zy2ti9FdO9nvd8kA'
headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0''Mozilla/5.0' }

#------------------------------------
#Class Territory
#------------------------------------

class Territory:
	def __init__(self, title, location, assignee):
		self.title = title
		self.location = location
		self.assignee = assignee
	def __str__(self):
		ostring = ""
		ostring += "Territory=[" + self.title + "," + self.location + "," + self.assignee + "]"
		return ostring

#------------------------------------
#Class Person
#  `firstname` VARCHAR(45) NULL ,
#  `middlename` VARCHAR(45) NULL ,
#  `lastname` VARCHAR(45) NULL ,
#  `address` VARCHAR(45) NOT NULL ,
#  `city` VARCHAR(45) NOT NULL ,
#  `state` ENUM('MA','NH') NULL ,
#  `zipcode` INT(5) ZEROFILL NULL ,
#  `phone` CHAR(10) NULL ,
#  `date` DATE NULL ,
#  `notes` TEXT NULL ,
#  `notfrench` TINYINT(1) NULL ,
#  `returnvisit` TINYINT(1) NULL ,
#  `iswitness` TINYINT(1) NULL ,
#  `moved` TINYINT(1) NULL ,
#  `donotdisturb` TINYINT(1) NULL ,
#  `log` TEXT NULL ,
#------------------------------------

class Person:
	def setFirst(self, firstname):
		self.firstname = firstname
	def setMiddle(self, middlename):
		self.middlename = middlename
	def setLast(self, lastname):
		self.lastname = lastname
	def setAddress(self, address):
		self.address = address
	def setNotes(self, notes):
		self.notes = notes
	def setCity(self, city):
		self.city = city
	def setState(self, state):
		self.state = state
	def setZipcode(self, zipcode):
		self.zipcode = zipcode
	def setPhone(self, phone):
		self.phone = phone
	def setNotFrench(self, notfrench):
		self.notfrench = notfrench
	def setReturnVisit(self, returnvisit):
		self.returnvisit = returnvisit
	def __str__(self):
		ostring = ""
		ostring += "Person=[" + self.firstname + "," + self.middlename + "," + self.lastname + self.address + "," + self.notes + ","+ self.city + ","+ self.state + ","+ self.zipcode + ","+ self.phone + ","+ self.notfrench + ","+ self.returnvisit + "," "]"
		return ostring

#------------------------------------
#Login Page
#------------------------------------

def LoginProcess(browser, idlogin, idpassword):
	print "-- Login Process --"
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
		WebDriverWait(browser,5).until(EC.title_contains("boston"))
	finally:
		return 0

#------------------------------------
#Browse 1 Page of Territory
#------------------------------------

def BrowseTerritories(browser):
	print "-- Browse Territory Page --"
	#xpath to the table
	xpath = '//html/body/table/tbody/tr/td[2]/table/tbody'
	#Retrieve all elements of the table Territory
	elements = browser.find_element_by_xpath(xpath)
	#Browse all the rows
	idrow = 1
	try:
		while (elements.find_element_by_xpath(xpath + '/tr[' + str(idrow) + ']')):	
			element = elements.find_element_by_xpath(xpath + '/tr[' +str(idrow)+ ']')
			title = element.find_element_by_xpath(xpath + '/tr[' +str(idrow)+ ']' + '/td/a' )
			location = element.find_element_by_xpath(xpath + '/tr[' +str(idrow)+ ']' + '/td[2]' )
			assignee = element.find_element_by_xpath(xpath + '/tr[' +str(idrow)+ ']' + '/td[3]' )
			print Territory(title.text, location.text, assignee.text)
			#Open a Territory
			BrowsePersonsTerritory(browser, element, idrow)
			idrow = idrow + 1
			break
	finally:
		return 0

#------------------------------------
#Browse persons of a Territory
#------------------------------------

def BrowsePersonsTerritory(browser, element, idrow):
	print "-- Browse Persons of a Territory --"
	#Open Territory URL
	xpath = '//html/body/table/tbody/tr/td[2]/table/tbody/tr[' +str(idrow)+ ']' + '/td/a'
	try:
		#click on a territory
		title = element.find_element_by_xpath(xpath)
		URL_title = title.text
		title.click()
		WebDriverWait(browser,5).until(EC.title_contains(URL_title))
		#click on the persons tab
		tab_person = browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/ul/li[3]/a')
		tab_person.click()

		#Browse all the persons
		idperson = 1
		xpathPersons = '/html/body/table/tbody/tr/td[2]/form/table/tbody'
		while (browser.find_element_by_xpath(xpathPersons + '/tr[' +str(idperson)+ ']' +'/td[2]/a')):
			link_name = browser.find_element_by_xpath(xpathPersons + '/tr[' +str(idperson)+ ']' +'/td[2]/a')
			print link_name.text
			idperson = idperson + 1
			link_name.click()
			BrowsePerson(browser)
		
	finally:
		return 0

#------------------------------------
#Parse a Person
#------------------------------------
def BrowsePerson(browser):
	print "-- Parse Person --"
	xpath = '/html/body/table/tbody/tr/td[2]/div[2]/div'
	idattribute = 2
	#Creation of the switch
	switch = {
		'First': 'setFirst',
		'Middle': 'setMiddle',
		'Last': 'setLast'
	}
	try:
		while (browser.find_element_by_xpath(xpath + '/b[' +str(idattribute)+ ']')):
			attribute = browser.find_element_by_xpath(xpath + '/b[' +str(idattribute)+ ']')
			print "titi"
			attribute_text = browser.find_element_by_xpath(xpath + '/b[' +str(idattribute)+ ']')
			print attribute.text
			print "toto"
			print attribute_text.text
			#Creation of a Person
			#p = Person()		
			#switch[attribute.text]()
			idattribute = idattribute + 1
			#print p
	finally:
		return 0

#------------------------------------
#Connection to Database
#------------------------------------
#Connection to the database
#Inputs: host is the hostname
#        user is the MySQL username
#        password is the MySQL password
#        db is the name of the MySQL instance
#Output  con is the connection reference
def DBConnect(host,user,password,db):
	try:
		con= mdb.connect(host,user,password,db)
		return con
	except mdb.Error, e:
		print "Error %d %s" % (e.args[0],e.args[1])
		return -1

#------------------------------------
#Provide URL to start with
#------------------------------------
def Load_Url(browser, URL):
	
	#We access the URL
	print "URL: " + URL
	browser.get(URL)


#-------------------------------------------------------------------------------------
#Main routine
#-------------------------------------------------------------------------------------
def Search_data(browser, con):	

	cur=con.cursor()
	
	#All cookies are suppressed before the search
	browser.delete_all_cookies()

	#We determine the right URL
	URL = 'http://fr.termanager.com'
	Load_Url(browser, URL)

    	#we wait for page to be loaded	
	time.sleep(1)
	
	#Connect into Login Page
	LoginProcess(browser,"boston","boston")

	#We start parsing Territories
	territory_link = browser.find_element_by_partial_link_text('territories').click()
		
	#We have to wait for the territory page to be loaded
	WebDriverWait(browser,5).until(EC.title_contains("territories"))

	#Parse the HTML table
	try:		
		# Number of Pages	
		page = 1
		while (page <= 12):
			#Retrieve all elements of the table Territory			
			BrowseTerritories(browser)
			break
			#Go to next page
			Load_Url(browser, URL + "/territories?page=" + str(page))
			page = page + 1
	finally:
		return 0

