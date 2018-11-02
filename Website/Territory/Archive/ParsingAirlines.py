#Parsing site UA, prototype
import re
import time
import datetime
import BeautifulSoup
import FunctionKayak
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
#from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver import ActionChains
import MySQLdb as mdb


headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0''Mozilla/5.0' }


#Here we will replace a.m. by am and p.m. by pm to use the format and we return the new string
def replaceTime(Timetoreplace, infoDate, formatT):
	Time = Timetoreplace.replace("a.m.","am")
	Timefinal = Time.replace("p.m.","pm")
	print Timefinal
	dateheure = infoDate + " " + Timefinal

	#we use this format for the datetime: %a = days (MON,THU,...), %b = month (JAN,FEB,...)
	d = datetime.datetime.strptime(dateheure, formatT)
	return d


def parseInfoHA(Info):
	InfoDateTime = Info[0].find_elements_by_xpath(".//p[@class='whiteText']")
	print len(InfoDateTime)
	DateDeparture = ""
	TimeFlight = []
	if len(InfoDateTime) == 2:
		DateDeparture = InfoDateTime[0].text
		Time = InfoDateTime[1].text
		print "Date : " + str(DateDeparture)
		print "Time : " + str(Time)

		#We save the format to create our datetime
		formatT = "%b %d, %Y %I:%M%p"
	
		#We split the two times that we get
		TimetoSplit = Time.replace(" - "," ")
		print TimetoSplit
		TimeDandA = TimetoSplit.split()
		print TimeDandA
		print TimeDandA[0]
		print TimeDandA[1]
		
		# We create the list of datetime
		for i in range(len(TimeDandA)):
			d = replaceTime(TimeDandA[i],DateDeparture,formatT)
			TimeFlight.append(d)
	print "len timeflt : "+str(len(TimeFlight))
	return TimeFlight


def parseHA(URL,browser,logfile):

	#We load the browser
	browser.get(URL)
	datetimeAirline = []
	time.sleep(3)

	#We wait until element are loaded
	WebDriverWait(browser,180).until(lambda br: br.find_elements_by_css_selector("div[class='departingBox']"))

	#We write the browser's source in a file
	FunctionKayak.printPage(browser,"","HTMLParsingHA.txt")

	#We get back the date and time of the departure and the arrival
	#We go on the block which contains information
	FlightInformationContent = browser.find_elements_by_xpath(".//div[@class='tsContent']")
	print len(FlightInformationContent)

	#We will extract information related to the departure
	InfoDeparture = FlightInformationContent[0].find_elements_by_xpath(".//div[@id='departingBox']")
	print len(InfoDeparture)
	InfoReturn = FlightInformationContent[0].find_elements_by_xpath(".//div[@id='returningBox']")
	print len(InfoReturn)
	time.sleep(3)

	#Here we will get the price proposed on th HA's website
	price = browser.find_elements_by_xpath(".//div[@id='totalAmt']")
	print "len price: "+str(len(price))
	pricefin = price[0].find_elements_by_xpath(".//span[@id='totalFareAmt']")
	print "len price fin: "+str(len(pricefin))+ " price: "+str(pricefin[0].text)
	priceTicket = pricefin[0].text.replace(",","")
	print priceTicket


	#info departure flight
	time.sleep(3)
	TimeFlight1 = parseInfoHA(InfoDeparture)

	#info return flight
	time.sleep(3)
	TimeFlight2 = parseInfoHA(InfoReturn)
	
	ListFlight = []
	if (len(TimeFlight1) > 0):
		ListFlight.append(TimeFlight1)
	if (len(TimeFlight2) > 0):
		ListFlight.append(TimeFlight2)

	for i in range(len(ListFlight)):

		# We append the departure and arrival datetime
		#We will append the two datetime
		datetimeAirline.append(ListFlight[i][0])
		datetimeAirline.append(ListFlight[i][len(ListFlight[i]) - 1])
	
	#We return the list of the datetime (0 datetime, 2 or 4) and the price of the ticket
	return datetimeAirline, priceTicket


# In this function, we will parse the UA's website
# We will extract flight and price information
# The parameter Flight is 
def parseInfoUA(Flight, logfile):
	TimeFlight=[]

	#Number of departures
	nbofdeparture = Flight[0].find_elements_by_xpath(".//td[@class='tdDepart EligibleCompPremierUpgrade']")

	#Number of arrivals
	nbofarrive = Flight[0].find_elements_by_xpath(".//td[@class='tdArrive EligibleCompPremierUpgrade']")

	print "nb departure: "+str(len(nbofdeparture))
	print "nb arrive: "+str(len(nbofarrive))

	#If the number of departures is not the same as the number of arrivals
	if len(nbofdeparture) != len(nbofarrive):
		print "ERROR"
	nbflight = len(nbofdeparture)

	#We get back the information about the flight
	for i in range(nbflight):

		#Departure Information
		infoDeparture = nbofdeparture[i].find_elements_by_xpath(".//div")

		#Arrival information
		infoArrive = nbofarrive[i].find_elements_by_xpath(".//div")

		#Time Departure
		TimeDeparture = nbofdeparture[i].find_elements_by_xpath(".//strong[@class='timeDepart']")

		#Date departure
		labellog = "DATE ARRIVAL : "
		FunctionKayak.LogPage(logfile, labellog, str(infoDeparture[2].text))

		#Airport departure
		labellog = "AIRPORT ARRIVAL : "
		FunctionKayak.LogPage(logfile, labellog, str(infoDeparture[3].text))

		#Time arrival
		TimeArrive = nbofarrive[i].find_elements_by_xpath(".//strong[@class='timeArrive']")

		#Date arrival
		labellog = "DATE ARRIVAL : "
		FunctionKayak.LogPage(logfile, labellog, str(infoArrive[2].text))

		#Airport arrival
		labellog = "AIRPORT ARRIVAL : "
		FunctionKayak.LogPage(logfile, labellog, str(infoArrive[3].text))
		

		formatT = "%a., %b. %d, %Y %I:%M %p"

		#Datetime Departure
		#Here we will replace a.m. by am and p.m. by pm to use the format and put the string in a datetime
		labellog = "TIME ARRIVE : "
		FunctionKayak.LogPage(logfile, labellog, str(TimeDeparture[0].text))
		d = replaceTime(TimeDeparture[0].text,infoDeparture[2].text, formatT)

		#We append the datetime in our list of datetime
		TimeFlight.append(d)

		#Datetime Arrival
		#Here we will replace a.m. by am and p.m. by pm to use the format and put the string in a datetimeprie
		labellog = "TIME ARRIVE : "
		FunctionKayak.LogPage(logfile, labellog, str(TimeArrive[0].text))
		d = replaceTime(TimeArrive[0].text,infoArrive[2].text, formatT)

		#We append the datetime in our list of datetime
		TimeFlight.append(d)
	
	#We will return our list of datetime to compare it after.
	return TimeFlight


#This function is the main function for the UA's parsing
#We will get the list of datetime back and the price
def parseUA(URL,browser,logfile):

	#We load the browser
	browser.get(URL)
	labellog = "############### UA's WEBSITE ############## : "
	FunctionKayak.LogPage(logfile, labellog, "")

	#We wait until element are loaded
	WebDriverWait(browser,180).until(lambda br: br.find_elements_by_css_selector("div[class='dtmOld']"))

	#We write the browser's source in a file
	FunctionKayak.printPage(browser,"","HTMLParsingUA.txt")

	#We get back the price proposed on the UA's website
	DetailPrice = browser.find_elements_by_xpath(".//div[@class='priceContinerB']")
	priceTotal = DetailPrice[0].find_elements_by_xpath(".//tr[@class=' total']")
	price = priceTotal[0].find_elements_by_xpath(".//td[@class='currency']")

	#We will extract flight information
	#We go through the flight details
	FlightDetails = browser.find_elements_by_xpath(".//div[@class='flightContainer']")
	labellog = "Flight details : "
	FunctionKayak.LogPage(logfile, labellog, str(len(FlightDetails)))

	#There are two different trips for a round-trip; we go through the divtrip
	Divtrip = FlightDetails[0].find_elements_by_xpath(".//div[@class='divTrips']")

	#If there is no Divtrip -> error
	if len(Divtrip) == 0:
		labellog = "ERROR : DIVTRIP == 0 !! "
		FunctionKayak.LogPage(logfile, labellog, "")

	#Detail of the departure flight
	Flight1 = Divtrip[0].find_elements_by_xpath(".//div[@class='divTrip firstChild odd']")

	#Detail of the return flight
	Flight2 = Divtrip[0].find_elements_by_xpath(".//div[@class='divTrip even']")
	ListFlight = []
	if len(Flight1) == 1:
		ListFlight.append(Flight1)
	if len(Flight2) == 1:
		ListFlight.append(Flight2)
	datetimeAirline = []
	TimeFlight=[]

	#We loop on the list of flight, 1 flight = One way, 2 = Round trip
	for i in range(len(ListFlight)):

		#We call the function to get the flight information back
		TimeFlight1 = parseInfoUA(ListFlight[i], logfile)
	
		# We append the departure and arrival datetime
		labellog = "TIME 1 : "
		FunctionKayak.LogPage(logfile, labellog, str(TimeFlight1[0]))

		#We will append the two datetime
		datetimeAirline.append(TimeFlight1[0])

		labellog = "TIME 2 : "
		FunctionKayak.LogPage(logfile, labellog, str(TimeFlight1[len(TimeFlight1) - 1]))
		datetimeAirline.append(TimeFlight1[len(TimeFlight1) - 1])
		TimeFlight.append(TimeFlight1)

	#We print every information obtained
	print price[0].text
	print price
	labellog = "PRICE : "
	FunctionKayak.LogPage(logfile, labellog, str(price[0].text))
	for i in range(len(TimeFlight)):
		print TimeFlight[i]

	
	
	priceTicket = price[0].text.strip("$")
	priceTicketfinal = priceTicket.replace(",","")

	#We return the list of the datetime (0 datetime, 2 or 4) and the price of the ticket
	return datetimeAirline, priceTicketfinal
	

#The goal of this function is to compare information from Kayak and information obtained on the booking site
def comparisonBadClick(datetimeKayak, priceKayak, datetimeAirline, priceAirline, dateA, dateR):

	print datetimeKayak
	print datetimeAirline

	#Difference price
	try:
		Diff = float(priceKayak) - float(priceAirline)
	except:
		return -3,0

	#If the difference is <1, we do not care
	if (Diff < 1 and Diff > -1):
		Diff = 0

	#If prices are different, it is a badclik
	if (float(priceKayak) - float(priceAirline) > float(1.0)) or (float(priceKayak) - float(priceAirline) < float(-1.0)):
		return -1,Diff

	#We will compare the datetimes obtained from the two website
	#We check if the number of departure and arrival is the same, if not, it is a badclick
	elif len(datetimeKayak) != len(datetimeAirline):
		print str(len(datetimeKayak)) + " != " +str(len(datetimeAirline))
		return -2,Diff
	else:	

		#Here we will check if every datetime is the same
		for i in range(len(datetimeKayak)):
			print datetimeKayak[i]
			print datetimeAirline[i]

			#If the datetime is not the same and the departure date is not the same, it is a bad click
			if (((datetimeKayak[i].time()>datetimeAirline[i].time()) or (datetimeKayak[i].time()<datetimeAirline[i].time())) or ((dateA.date() < datetimeAirline[0].date()) or dateA.date() > datetimeAirline[0].date())):
				print datetimeKayak[i].time() 
				print datetimeAirline[i].time()
				print dateA 
				print datetimeAirline[0].date()
				return -2,Diff

			#There is a return flight
			if dateR != 0:

				#If the datetime is not the same and the return date is not the same, it is a bad click
				if (((datetimeKayak[i].time()>datetimeAirline[i].time()) or (datetimeKayak[i].time()<datetimeAirline[i].time())) or (dateR.date() != datetimeAirline[2].date())):
					print "pb retour"
					print datetimeKayak[i].time() 
					print datetimeAirline[i].time()
					print dateR.date()
					print datetimeAirline[2].date()
					return -2,Diff
	
	#We return the value of the badclik, 0 it is not a badclik, -1 and -2 it is.
	return 0,Diff


#Store result in a database
def InsertDatabaseBadClick(cur, idsolution, idprovider, name, system, WebSitePrice, Diff, BCValue, logfile):
	SQLInsert = "INSERT IGNORE INTO BadClick (id,idsolution,idprovider,name,system,WebSite_Price,diff_WebSite_Kayak,BadClickValue) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s)",(idsolution, idprovider, name, system, WebSitePrice, Diff, BCValue)
	cur.execute(*SQLInsert)
	labellog = "SQLINSERT BAD CLICK : "
	FunctionKayak.LogPage(logfile, labellog,str(SQLInsert))


