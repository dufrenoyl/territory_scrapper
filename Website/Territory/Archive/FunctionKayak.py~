#import bs4 as BeautifulSoup
import ParsingAirlines
import re
import time
import datetime
import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
#from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver import ActionChains
import MySQLdb as mdb


#those headers are added to avoid to be seen as a BOT by the Website
kayakkey = 'KBHCF2zy2ti9FdO9nvd8kA'
headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0''Mozilla/5.0' }

########################################################################################


#odfile is a routine which reads the OD/Date and company file to process
# input: fich: filename
# output: tabfinal contains the OnD dates values to process
#         resultcie contains the list of companies to process
#         Stop contains all or nonstop to indicate the type of flights to keep

def odfile(fich):
	global comp

	#input file open
        fs = open(fich,'r')

	#read list of companies
        line = fs.readline()
	cie = ""
	resultcie = []
	Stop = ""
	comp = 0
	print str(len(line))
        print line

	#we parse the content of the first line
	for i in range(len(line)):

		#we extract each company code that we store into resultcie
		if line[i] == '*':
			comp = 1
			break
		if line[i] == ' ' and cie!="":
			resultcie.append(cie)
			cie=""
		else:

			#we interrupt reading if we see a slash /
			if line[i]=='/':
				resultcie.append(cie)
				break			
			if line[i]!='\n' and line[i]!='\r':
				cie = cie+line[i]

        #insert the last element
	if i>0:
		resultcie.append(cie)
	
        #we read the next line to check if nonstop flights only should be kept
	line = fs.readline()

	for i in range(len(line)):
		if line[0] == '*':    #in this case we keep all flight types
			Stop = "all"
		else:                 #in this case we keep nonstop only
			Stop = "nonstop"
	print Stop

        #we read the next lines which contain the OnD/Dates
	line = fs.readline()
        result = {}
        resultDate = []

        #tabfinal will contain the OnD date values for each OnD
        tabfinal = {}
        mot = ""
        nbSpace = 0
        ind = 0

	#we loop on all OnD/Dates lines
        while line != "":
                for i in range(len(line)):
                        if line[i] == ' ':
                            nbSpace +=1
                            if nbSpace < 3:
                                if nbSpace == 1:

				    #we store the origin of the OnD
                                    result["origin"] = mot
                                else:

				    #we store the destination of the OnD
                                    result["destination"] = mot
                            else:

				#we store the date
                                resultDate.append(mot)
                            mot = ""

			#We skip the line
			elif line[i] == '#':
			    break
                        elif line[i] == '\n' or line[i] == '\r' :
                            resultDate.append(mot)
                        else:
                            mot = mot + line[i]
                result["date"] = resultDate
                indice = ind
                tabfinal[indice] = result
                result = {}
                resultDate = []
                mot = ""
                line = fs.readline()
                if len(line) < 10 :    #not valid or End Of File
                  break;
                ind += 1
                nbSpace = 0
	print "OnD Date: " +str(tabfinal)
	print "Companies: " + str(resultcie)
        return tabfinal,resultcie,Stop



#parseAirlinefile is a routine which reads the company that we will parse to check the badclick
# input: fich: filename
# output: tabfinal contains the OnD dates values to process
#         resultcie contains the list of companies to process
#         Stop contains all or nonstop to indicate the type of flights to keep

def parseAirlinefile(fich):

	#input file open
        fs = open(fich,'r')

	#read list of companies
        line = fs.readline()

	#we loop on all "parse" lines
	mot =""
	nbSpace=0
	NameAirline=[]
	NameParser={}
        while line != "":
                for i in range(len(line)):
                        if line[i] == ' ':
                            nbSpace +=1

			    #we store the date
                            NameAirline.append(mot)
                            mot = ""
                        elif line[i] == '\n':
                            NameParser[NameAirline[len(NameAirline)-1]] = mot
                        else:
                            mot = mot + line[i]
                mot = ""
                line = fs.readline()
                nbSpace = 0

	return NameAirline, NameParser


#This routine allows to append the browser source content into the  file: nfile
#inputs: browser is the browser reference
#        label is a text to append before the output
#        nfile is the name of the appended file

def printPage(browser,label,nfile):
	myfile = open(nfile, 'a')
        myfile.write(label+'\n')
 	mypage = BeautifulSoup.BeautifulSoup(browser.page_source).prettify().decode('utf-8')
	myfile.write(mypage.encode('utf-8'))
	myfile.close()

#This routine allows to log infos into the logfile
#inputs: label to log
#        infos to log
#        logfile: file into which we are logging
def LogPage(logfile,label,infos):
        logfile.write(label)
 	logfile.write(infos)
	logfile.write('\n')


def Search_OD_Url(browser, result, option):
	URL = []

	#All cookies are suppressed before the search
	browser.delete_all_cookies()
	
	#We force AMADEUS or ITA according to option value
	if (option == "AMADEUS"):
		URL = 'http://kayak.com?xp=amadeusonly.default'
	elif (option == "ITA"):
		URL = 'http://kayak.com?xp=itaonly.default'
	else:
		URL = 'http://kayak.com'
	
	#We access the URL
	browser.get(URL)
	
	#We build the url corresponding to the OnD date to process 
	if len(result["date"]) == 2:    #case of a roundtrip
		url2 = '/#/flights/'+result["origin"]+'-'+result["destination"]+'/'+result["date"][0]+'/'+result["date"][1]
	else:                           #case of a single trip
		url2 = '/#/flights/'+result["origin"]+'-'+result["destination"]+'/'+result["date"][0]

	return URL, url2
	

#This routine allows to select which company needs to be selected
#Inputs: company is the list of companies to select
#        browser is the browser reference
#Output: browser as it may have changed
#        nclick the number of clicks done
def ClickCompany(company, browser):
	i = 0
        nclick = 0

	#We wait until all airlines have been displayed in the browser
	WebDriverWait(browser, 150).until(lambda br: br.find_element_by_id("fs_airlines_content").is_displayed())
	filters = browser.find_element_by_css_selector("div[class='filterSectionOptions'][id='fs_airlines_content']")

        #We retrieve information for all airlines displayed
	Allairlines = filters.find_elements_by_xpath(".//input[@name='airlines']")
	nb = len(Allairlines)
	while 1:
		try:
			print "Value nb1: " + str(nb)
			print "Value of i: " + str(i)
		        if (i == nb):
			  break

			#We extract the company name by reading the id attribute of the element
			NameCompany = Allairlines[i].get_attribute('id')
			print NameCompany
			cie=NameCompany.strip("fs_airlines__input")
			print cie

			#We verify if it is checked by reading the checked attribute of the element
		        checked =  Allairlines[i].get_attribute('checked')

			#if the company is not to be selected then it is unchecked
			if cie not in company and checked == 'true':

				#we uncheck it by clicking
				Allairlines[i].click()
				time.sleep(1.5)
		                nclick = nclick +1

                                # we reprocess filters and Allairlines in case the browser has moved
				filters = browser.find_element_by_css_selector("div[class='filterSectionOptions'][id='fs_airlines_content']")
				Allairlines = filters.find_elements_by_xpath(".//input[@name='airlines']")
				nb = len(Allairlines)
		except:
			stringerr = "Error in ClickCompany at number "+str(i) 
			raise Exception (stringerr)
			continue
		i = i+1
		
	return (browser,nclick)


#This routine will select nonstop only flights when requested
def ClickStops(browser,Stop):
        if (Stop == "all"):
          return browser
	i = 0

        #we locate the element containing the nonstop indicator
	filtersStop = browser.find_element_by_css_selector("div[class='filterSectionOptions'][id='fs_stops_content']")
	Allstops = filtersStop.find_elements_by_xpath(".//input[@name='stops']")
	nb = len(Allstops)
	while 1:
		try:
			print "Value of i in ClickStops: " + str(i)
		        if (i == nb):
			  break

			#We get all individual stop elements
			NameStop = Allstops[i].get_attribute('id')
			print NameStop
			checked =  Allstops[i].get_attribute('checked')

			#We check only nonstop flights and decheck others
			if NameStop!="fs_stops_0_input" and checked == 'true':

				#We decheck as it is not nonstop
				Allstops[i].click()
				time.sleep(1.5)
				filtersStop = browser.find_element_by_css_selector("div[class='filterSectionOptions'][id='fs_stops_content']")
				Allstops = filtersStop.find_elements_by_xpath(".//input[@name='stops']")
				nb = len(Allstops)
		except:
			i = i+1
			stringerr = "Error in ClickSops "
			raise Exception (stringerr)
			continue
		i = i+1
		
	return (browser)




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


def Datetimeform(dep1, arr1, format1):
	dep11 = dep1.text.replace("a"," am")
	dep12 = dep11.replace("p"," pm")			
	arr11 = arr1.text.replace("a"," am")
	arr12 = arr11.replace("p"," pm")
	dep1 = time.strptime(dep12, format1)
	arr1 = time.strptime(arr12, format1)
	datetime1 = datetime.datetime(1111,1,1,dep1.tm_hour,dep1.tm_min,dep1.tm_sec)
	datetime2 = datetime.datetime(1111,1,1,arr1.tm_hour,arr1.tm_min,arr1.tm_sec)
	return datetime1, datetime2



# ..........
#Inputs  flightresult
#        logfile is the logging file
#Output  myflt
def flightInfoDetails(flightresult,logfile):
 	myflt = []

# We locate the section that allows to retrieve the itinerary information
	itinerary = flightresult.find_elements_by_xpath(".//table[@class='inlineflightitinerarylegs']")

	#We log the itinerary number
	labellog = "ITINERARY : "
	LogPage(logfile, labellog, str(len(itinerary)))

	# We retrieve all itineraries
	myvol= itinerary[0].find_elements_by_xpath(".//tr[@class='first']")

	# We log info for each itinerary
	labellog = "Number of flights for itinerary : "
	LogPage(logfile, labellog, str(len(myflt)))
	for j in range(len(myflt)):
		labellog = "FLIGHT INFO : "
		LogPage(logfile, labellog, myflt[j].text.encode('utf-8'))
		myflt.append(myflt[j].text.strip().encode('utf-8'))

	return myflt



# Sous programme qui va recuperer les informations des providers, booking site,price,fares
#This routine will find fare info relative to each Provider
#Inputs: tbody is a pattern which allows to position at start of fare information
#        logfile is the logfile
#Output: BookingSites is the booking site
#        system is the system where the booking is made .eg. Amadeus , Ita, Expedia etc...
#        CostTicketProvider is the price offred by this booking site
#        FareCode are the fare codes associated to the fare
def flightInfoProviders(tbody,logfile):
	labellog = "BOOKING SITE : "
	system = ""        # will contain the name of the system on which the booking is made
	CostTicketProvider = ""
	FareCode = "" 
        Validfareinfo = False

        #we retrive the booking site name
        BookingSites = tbody.find_elements_by_xpath(".//td[@class='name']")
	print BookingSites[0].text

        #we retrieve the fare
	CostPerTicket = tbody.find_elements_by_xpath(".//td[@class='total']")
	print CostPerTicket[0].text

        #we retrive the fare codes
	FareCodes = tbody.find_elements_by_xpath(".//td[@class='fareCodes']")

       
	if len(BookingSites) !=1:
        	print "Pb len BC: "+str(len(BookingSites))
	if len(FareCodes) !=1:
		print "Pb len FC: "+str(len(FareCodes))
	if len(CostPerTicket) !=1:
		print "Pb len CT: "+str(len(CostPerTicket))

	LogPage(logfile, labellog, BookingSites[0].text)

        #we only process if there is a fare associated
	if CostPerTicket[0].text != "check rates":

		#We check if Farecodes are associated
			if len(FareCodes) > 0:
				labellog = "FARE CODE : "
				LogPage(logfile, labellog, FareCodes[0].text)
				FareCode=FareCodes[0].text
			else:
				FareCode=""
			if len(CostPerTicket) > 0 and CostPerTicket[0].text != "":
				CostTicketProvider = CostPerTicket[0].text.strip("$")
				print CostTicketProvider

                                #We extract the URL at which the booking will be made
				elsys = CostPerTicket[0].find_element_by_xpath(".//a")
				element_attribute = elsys.get_attribute('href')
				labellog = "COST PER TICKET : "
				LogPage(logfile, labellog, CostPerTicket[0].text)
			
				#We store in system the name of the system that will make the booking
				if ( element_attribute.find('AMADEUS') != -1):
					system = "AMADEUS"
				elif ( element_attribute.find('ITA') != -1):
					system = "ITA"
				elif ( element_attribute.find('KAYAK') != -1):
					system = "KAYAK"
				elif ( element_attribute.find('ORBITZ') != -1):
					system = "ORBITZ"
				elif ( element_attribute.find('CHEAPTICKETS') != -1):
					system = "CHEAPTICKETS"
				elif ( element_attribute.find('EXPEDIA') != -1):
					system = "EXPEDIA"
				elif ( element_attribute.find('TRAVELOCITY') != -1):
					system = "TRAVELOCITY"
				else:
					system = "UNKNOWN"
				labellog = "SYSTEM : "
				LogPage(logfile, labellog, system)

                                #We check that the 
                        if (CostTicketProvider != "check rates" and CostTicketProvider != ""):
				Validfareinfo = True
                        else:
                                Validfareinfo = False
			print BookingSites[0].text + system + str(float(CostTicketProvider)) + FareCode + str(Validfareinfo)
	return BookingSites, system, CostTicketProvider, FareCode , Validfareinfo


#Store in the database
def storeDBSolution(logfile, datetimeFlt, result, DateTimesys, priceTicket, place, cur):

	idrow = 0

	#We build the SELECT and INSERT for the Table Solutions for round-trip
        # the SELECT is used to check that there is no dupe; there is indeed a creation date for each solution
        # but if the script is rerun within 2 hours (parameter in TIMESTAMPDIFF) then the results are merged
	if len(result["date"]) == 2:
		SQLSelect = "SELECT id,dateCreation FROM solutions WHERE deptime1=%s and arrtime1=%s and deptime2=%s and arrtime2=%s and origin=%s and destination=%s and DateDeparture=%s and DateReturn=%s HAVING TIMESTAMPDIFF(minute,solutions.dateCreation,%s)<=120", (datetimeFlt[0].time(),datetimeFlt[1].time(),datetimeFlt[2].time(),datetimeFlt[3].time(),result["origin"],result["destination"],result["date"][0],result["date"][1],DateTimesys)
		SQLInsert = "INSERT INTO solutions(id,rank,datecreation,DateDeparture,DateReturn,deptime1,arrtime1,deptime2,arrtime2,origin,destination,price) VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (place,DateTimesys,result["date"][0],result["date"][1],datetimeFlt[0].time(),datetimeFlt[1].time(),datetimeFlt[2].time(),datetimeFlt[3].time(),result["origin"],result["destination"],float(priceTicket))

		#We build the request for single-trip
	else:
		SQLSelect = "SELECT id,dateCreation FROM solutions WHERE deptime1=%s and arrtime1=%s and origin=%s and destination=%s and DateDeparture=%s HAVING TIMESTAMPDIFF(minute,solutions.dateCreation,%s)<=120", (datetimeFlt[0].time(),datetimeFlt[1].time(),result["origin"],result["destination"],result["date"][0],DateTimesys)
		SQLInsert = "INSERT INTO solutions(id,rank,datecreation,DateDeparture,deptime1,arrtime1,origin,destination,price) VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s)", (place,DateTimesys,result["date"][0],datetimeFlt[0].time(),datetimeFlt[1].time(),result["origin"],result["destination"],float(priceTicket))		
				
	print SQLSelect
	print SQLInsert

	#We write to the log			
	labellog = "SQLSelect : "
	LogPage(logfile, labellog,str(SQLSelect))
	labellog = "SQLInsert : "
	LogPage(logfile, labellog, str(SQLInsert))

	#We execute the select and we fetch the results
	cur.execute(*SQLSelect)
	resultselect = cur.fetchall();
	print resultselect
		
	#If the solution does not exist we store it
	if (len(resultselect) == 0):		
		cur.execute(*SQLInsert)

		#We get the primary key to use it as a secondary key in the Table providers
		idrow = cur.lastrowid

	#If the solution already exists	we do not duplicate			
	else:
		print "INSERT INTO SOLUTIONS ALREADY HERE"

                #We retrieve the primary key
		idrow = resultselect[0][0]

                #We log some info
		labellog = "Solution already inserted : "

	LogPage(logfile, labellog, str(idrow))
	return idrow

#Main routine
def Search_data(browser, browser2, result, logfile,Namebrowfile, Company, Stop, AmadeusorITA, con, DateTimesys, methodparsing):	
	global comp
        #We get a cursor on the database 
	cur=con.cursor()

	#We log 
	labellog = "INFORMATION SUR :" + str(result)
	LogPage(logfile, labellog, "")
	
	#We determine the right URL
	final_URL = Search_OD_Url(browser, result, AmadeusorITA)
	print final_URL

	#We log the URL value
	labellog = "URL USED : "
	LogPage(logfile, labellog, str(final_URL))
	final_url = final_URL[0]+final_URL[1]

	#We load the URL
	browser.get(final_URL[0])

	#We position on the right page
	browser.get(final_url)

        #we wait for page to be loaded	
	time.sleep(2)

        #we wait for the right element to be loaded
        #elements are different for a single or a round-trip
	if len(result["date"]) == 2:      #case of a roundtrip 
		WebDriverWait(browser,180).until(lambda br: br.find_elements_by_class_name("introtext"))
	else:                             #case of a single trip
		WebDriverWait(browser,180).until(lambda br: len(br.find_elements_by_id("progressDiv")) == 0)	
	
	#We click on companies unless All are needed
        printPage(browser,"BEFORE CLICK",Namebrowfile)
	if (comp == 0):	
		browser,nb = ClickCompany(Company, browser)
	time.sleep(6)
        
        #We select the nonstop flights depending on the value of Stop	
	browser = ClickStops(browser,Stop)
	time.sleep(6)

        #Main loop to read all flight proposition for the OnD/Date
	while 1:

		#We retrieve all elements containing Flight information
		flightresult = browser.find_elements_by_css_selector("div[class='flightresult resultrow    ']")

                #nb is the number of flights on the page
		nb = len(flightresult)
		labellog = "Number of FLIGHT RESULTS : "
		LogPage(logfile, labellog, str(nb))
		nfail=0

		#We loop over all flights present on the page
		for i in range(nb):

			#we log some info
			labellog = "Position of the flight on the page : "
			LogPage(logfile, labellog, str(i))
			try:	
				labellog = "Detail Holder : "
				LogPage(logfile, labellog, "")	
                                dprice = flightresult[i].find_elements_by_xpath(".//div[@class='pricerange']")
                                if (len(dprice) != 1):
                                  print "DPRICE>>>>>>>>>>>>>>>>>"
                                else:
                                  print "DPRICE:>>>>>>>>:  "+dprice[0].text

                                # We position on the block which contain flight infos			
				tripdetails = flightresult[i].find_element_by_class_name("tripdetailholder")

				# We find aiport departure and arrivol codes
				apt = tripdetails.find_elements_by_xpath(".//div[@class='airport']")

				# We find the flight duration
				duration = tripdetails.find_elements_by_xpath(".//div[@class='duration']")
	
				# We find the times of departure (2 values for round trip)
				depart = tripdetails.find_elements_by_xpath(".//div[@class='flighttime flightTimeDeparture']")

				# We find the times of arrival   (2 values for round trip)
				arriv = tripdetails.find_elements_by_xpath(".//div[@class='flighttime flightTimeArrival']")

				# Number of stops
				stoplayovers = tripdetails.find_elements_by_xpath(".//div[@class='stopsLayovers']")

				nbrStop = re.findall(r'\d+',stoplayovers[0].text)
				nbstop = []
				if len(nbrStop) > 0:
					LogPage(logfile, 'Number of stops: ', str(int(nbrStop[0])))
					nbstop.append(int(nbrStop[0]))
				else:
					LogPage(logfile, labellog, "0")
					nbstop.append(0)

				#We compute correctly the date/time for the DB
				datetimeFlt = []
				format1 = '%I:%M %p'
				datetime1, datetime2 = Datetimeform(depart[0], arriv[0], format1)
				datetimeFlt.append(datetime1)
				datetimeFlt.append(datetime2)
			
				if len(result["date"]) == 2:
					datetime3, datetime4 = Datetimeform(depart[1], arriv[1], format1)			
					datetimeFlt.append(datetime3)
					datetimeFlt.append(datetime4)

                        	#place is the rank on the display and it will be inserted in the DB
				place = i

				# We position on all booking site proposals for the current solution
				mydeal = flightresult[i].find_elements_by_class_name("dealsinresult")

                                # We log the number of proposals by booking sites
				nbdeal = len(mydeal)
				labellog = "Number of deals proposed : "
				LogPage(logfile, labellog, str(nbdeal))
				
				# ....
				price = mydeal[0].find_element_by_class_name("dealPrice")

			        #We extracte the int value of the price
			        priceTicket = price.text.strip("$")

				# Prix du billet sur Kayak
				labellog = "Kayak Price: "
				LogPage(logfile, labellog, price.text)	
                      
                                # We look for the name of the system on which we can book by parsing the system URL
				RecupURL = {}

				# We loop through all the deals proposed to build the URL to access for booking
                                #this URL will be accessed to check Bad Clicks
				for j in range(nbdeal/2):  # we divide by 2 as Kayak has placed blank lines

					# We find the name of the Provider
					providTxt = mydeal[j].find_element_by_class_name("providerText")
					element_attribute = mydeal[j].get_attribute('rel')

                                        # We will find "in clear" AMADEUS or ITA under the rel attribute
					if ( element_attribute.find('AMADEUS') !=1):
						sys = "AMADEUS"
					elif (element_attribute.find('ITA') != -1):
						sys = "ITA"		
					else:
						sys = ""

                                        #We log some info
					labellog = "Provider: "
					LogPage(logfile, labellog, providTxt.text)

					# We build the URL that we will access for Bad Clicks and we store it in recupURL
                                        # The provider needs to have a Parser associated
					if (methodparsing.has_key(providTxt.text) and (sys=="AMADEUS" or sys=="ITA")):
						strURL = mydeal[j].get_attribute('rel')
						RecupURL[providTxt.text] = "http://kayak.com/"+str(strURL)

                                #We find the two buttons on which to click for to get flight and fare detailss
				details = flightresult[i].find_elements_by_xpath(".//button[@class='ui-button ui-button-small ui-button-gray']")
                                #We log some infos
				labellog = "nb of detail buttons : "				
				LogPage(logfile,labellog,str(len(details)))
			except :
				continue

		        #We click on the first button to retrieve flight information			
			details[0].click()

                        #we wait for all information to be present on the page
			WebDriverWait(flightresult[i], 20).until(lambda br: br.find_element_by_xpath(".//table[@class='inlineflightitinerarylegs']"))						
			
			#We retrieve all flight information
			myflt = flightInfoDetails(flightresult[i],logfile)
		

			#We click on the second button to retrieve fare details
			details[1].click()

                        #we wait for all information to be present on the page
			WebDriverWait(flightresult[i], 150).until(lambda br: br.find_element_by_xpath(".//div[@class='fareInformation active']"))			
			
                        if i == 0:
				printPage(browser,"AFTER CLICK 1",Namebrowfile)	

                        #Fare details are under the section fareInformation for each solution		
			fareinfo = flightresult[i].find_elements_by_xpath(".//div[@class='fareInformation active']")

			#We write to the log			
			labellog = "Size Fare info : "
			LogPage(logfile, labellog, str(len(fareinfo)))

                        #We position on <tbody> as the information is in a table within a <tbody> pattern
                        tbody = fareinfo[0].find_elements_by_xpath(".//tbody/tr")

                        # len(tbody) will give the number of rows in the HTML table containing the providers info
                        nprovider = len(tbody)
                        if nprovider == 0 :
                          raise Exception("TBODY: "+str(nprovider))
			
			idrow = storeDBSolution(logfile,datetimeFlt,result, DateTimesys, priceTicket, place, cur)
			
			# We loop on all providers to insert Fare information
			for j in range(nprovider):

                                #We get all fare info per provider 
				BookingSites,system,CostTicketProvider,FareCode,Validfareinfo = flightInfoProviders(tbody[j],logfile)
				print '*'+BookingSites[0].text+system+CostTicketProvider+FareCode+'*'

				#We insert only if the fare information is valid
                                if Validfareinfo :
                                        print '+'+CostTicketProvider+'+'

					#We use nrec to know if we already dealt this badclick
					nrec = cur.execute("INSERT IGNORE INTO providers (id,name,system,price,codefare,idsolution) VALUES (NULL,%s,%s,%s,%s,%s)",(BookingSites[0].text,system,float(CostTicketProvider),FareCode,idrow))
					cur.execute("SELECT LAST_INSERT_ID()")
					resultinsert = cur.fetchall();

                                        #We will need the row Id for the BadClick table
					idrow2 = resultinsert[0][0]
					labellog = "idrow2 from last_insert_id and nrec: "
			                LogPage(logfile, labellog, str(idrow2)+":"+str(nrec))

                                	#We check Bad Clicks only if the parser exists and if the flight is not already in the DB
					if (RecupURL.has_key(BookingSites[0].text) and nrec > 0):

						#We log some info
					        labellog = "Url for Bad Click : "
					        LogPage(logfile, labellog, RecupURL[BookingSites[0].text])
						datetimeAirline,priceAirline = methodparsing[BookingSites[0].text](RecupURL[BookingSites[0].text],browser2,logfile)
		                                #We consider 2 cases : round-trip and single-trip
	  					dtk1 = datetime.datetime.strptime(result["date"][0], "%Y-%m-%d")  
		                                dtk2 = 0                                 
						if len(result["date"]) == 2:        #case of round-trip						
							dtk2 = datetime.datetime.strptime(result["date"][1], "%Y-%m-%d")

		                                #We call the parser for Bad Clicks
						ValBadClick,Diff = ParsingAirlines.comparisonBadClick(datetimeFlt, float(CostTicketProvider), datetimeAirline, priceAirline, dtk1, dtk2)

						ParsingAirlines.InsertDatabaseBadClick(cur, idrow, idrow2, BookingSites[0].text, system, priceAirline, Diff, ValBadClick, logfile)
						print "Bad Clik Value : "+str(ValBadClick)

						#We log some info
					        labellog = "Bad Click Value : "
					        LogPage(logfile, labellog, str(ValBadClick))			
			con.commit()
			if (i > 3): 
				break

		print ""
		break
	

