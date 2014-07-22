# -*- coding: utf_8 -*-
from __future__ import unicode_literals
import os,sys,re, pymysql, sqlite3 as lite

def welcome(strName, strBuild):
        os.system('cls') # on linux / os x	
        intYear = strBuild.split(".")[0]
        return strName+" "+strBuild+"\nby Lucy Little \n(c) "+intYear+" Lucy Little\n"

def checkArgument(minArgument):
        if len(sys.argv) > minArgument:
                return sys.argv
        else:
                return False

def gPrettyPrint(strItem, size=60):
        intLength = len(strItem)+1
        intSpace = size - intLength
        print strItem+" "+"."*intSpace,


def gDistance(target, source, focus):
        # 2nd version of gDistance as having an issue
        #focus = [["1", "8", "f"], ["1", "8", "g"]]

        # 3- completely same
        # 1- identical ***
        # 0- different

        if len(target) != len(source): # if length is different, give it 
                return 0
	if target == source:
                return 3
	else:
		result = []
		for i in range(len(target)):
                        if str(target[i]) == str(source[i]):
				result.append("1")
			else:
				temp = 0
				for j in focus:
					if str(target[i]) in j and str(source[i]) in j:
						temp = 1
				if temp == 0:
					result.append("0")
				else:
					result.append("1")
		if "0" in result:
			returnValue = 0
		else:
			returnValue = 1
		return returnValue

###################################################################################################
# DEFINE FUNCTION - CHECK MySQL SERVER CONNECTIVITY
# Usage: boolCheckServer(strHost, strUser, strPasswd, strDB)
def boolCheckServer(strHost, strUser, strPasswd, strDB):
	try:
		MySQLdb.connect(host=strHost, user=strUser, passwd=strPasswd, db=strDB)
	except:
		#raise
		return False
	else:
		return True

###################################################################################################
# DEFINE FUNCTION - INPUT DELIMITER RECOGNITION
def charCheckDelimiter(inputHeader):
	if "|leRecordType|" in inputHeader:
		return "|"
	elif "|leRecordType|" in inputHeader:
		return ","

def arrayGetConfig(configFile):
	global PRODUCT, BUILD
	try:
		fileConfig = open(configFile,"r")
	except:
		fileConfigNew = open(configFile,"w")
		fileConfigNew.write("// Default configuration file"+ """\n
// GHS Rule DB
ghsRuleServer : xxx.xxx.com
ghsRuleDB : RULEDB
ghsRuleServerID : DBname
ghsRuleServerPassword : DBpwd

// METRICS DB
MetricsServer : xxx.xxx.com
MetricsDB : METRICSDB
MetricsServerID : METRICSDBID
MetricsServerPassword : PWD

// HEADER CONFIG
InputBusinessName = BUSINESS_NAME
CountryCode = ISO_COUNTRY_CODE
LanguageCode = leLanguageCode

""")
		print "\n*** New configuration file has been created.\n*** Please restart the program."
		fileConfigNew.close()
		raw_input("\nPress enter to exit")
		sys.exit(0)
	else:
		# if configuration file exists
		dictConfig = {}

		for i in fileConfig:
			if i[0] != "/" or i.strip()!="":
				i = i.strip()
				i = re.sub(r"[\r\n]","",i)
				i = i.split(":")
				if len(i)==2:
					dictConfig[i[0].strip()] = i[1].strip()
		fileConfig.close()
		return dictConfig
		

class lucyReport:
	reportFile = ""
	fileCSV = []
	lastMsg = ""

	def open(self):
		try:
			self.fileCSV = open(self.reportFile,"w")
		except:
			return 0
		return 1

	def close(self):
		self.fileCSV.close()


	def add(self,strMessage, header=0, size=120):
		if header==0:
			self.fileCSV.write(str(strMessage+"\n"))
		elif header==1:
			intLength = len(strMessage)+1
			intSpace = size - intLength
			self.fileCSV.write("\n"+strMessage.upper()+" "+"-"*intSpace+"\n")
		else:
			self.fileCSV.write("\t"*(header-1)+strMessage+"\n")
		self.lastMsg = strMessage

	def kill(self, strMsg=""):
		if strMsg:
			temp = strMsg
		else:
			temp = self.lastMsg
		self.add("Terminated",1)
		raw_input(temp+"\n\nPress enter to finish.")
		sys.exit(0)

class lucyRule:
	fields = []
	dbName = ""

	def initialize(self):
		global cur, conn
		temp = "Id INT"
		for i in self.fields:
			temp = temp + ", "+str(i)+" TEXT"
		try:
			conn = lite.connect(self.dbName)	
			conn.text_factory = str
			with conn:
				cur = conn.cursor()    
				cur.execute("DROP TABLE IF EXISTS Temp")
				#cur.execute("CREATE TABLE Temp (Id INT, Table TEXT, Country TEXT, Language TEXT, Level TEXT, ValueID TEXT, Value1 TEXT, Value2 TEXT, Value3 TEXT, Value4 TEXT, Value5 TEXT, Value6 TEXT, Value7 TEXT, Value8 TEXT, Value9 TEXT, Value10 TEXT, Value11 TEXT, Value12 TEXT)")
				cur.execute("CREATE TABLE Temp("+temp+")")
		except:
			return 0
		return 1

	#Load files
	def loadRule(self, file):
		lines = {}
		rules = {}
		delimiter = ","
		header = 0
		fields = self.fields
		initialCheckFields = [] # these fields must not be empty

		global lstFileCSV
		try:
			fileCSV = open(file.strip(),"r")
			lstFileCSV = fileCSV.readlines()
			del fileCSV
			count = 0
			stopPoint = 0
			for i in lstFileCSV:
				if header == 0:
					count+=1
					i = re.sub(r'\n$','',i) #remove new line character
					i = re.sub(u"\uFEFF","",i)
					if len(i.strip())>2: #if first two characters are not //
						if i.strip()[0]!="/" and i.strip()[1]!="/" and re.sub(r",+",",",i.strip())!=",": #and is valid

							lines[count] = i
							i = i.strip()
							# lines only has valid rule
							temp = i.split(delimiter)

							tempSQL1 = ""
							tempSQL2 = ""

							for j in range(len(temp)):
								tempSQL1 = tempSQL1 + str(fields[j]) + ","
								tempSQL2 = tempSQL2 + "'"+ str(re.sub("'","''",temp[j])) + "',"

							tempSQL1 = "id,"+str(tempSQL1)	
							tempSQL2 = "'"+str(count)+"',"+str(tempSQL2)
							cur.execute("INSERT INTO Temp ("+tempSQL1[:-1]+") VALUES ("+tempSQL2[:-1]+")")
				if header == 1:
					if count != 0:
						count+=1
						i = re.sub(r'\n$','',i) #remove new line character
						i = re.sub(u"\uFEFF","",i)
						if len(i.strip())>2: #if first two characters are not //
							if i.strip()[0]!="/" and i.strip()[1]!="/" and re.sub(r",+",",",i.strip())!=",": #and is valid

								lines[count] = i
								i = i.strip()
								# lines only has valid rule
								temp = i.split(delimiter)

								tempSQL1 = ""
								tempSQL2 = ""

								for j in range(len(temp)):
									tempSQL1 = tempSQL1 + str(fields[j]) + ","
									tempSQL2 = tempSQL2 + "'"+ str(re.sub("'","''",temp[j])) + "',"

								tempSQL1 = "id,"+str(tempSQL1)	
								tempSQL2 = "'"+str(count)+"',"+str(tempSQL2)
								cur.execute("INSERT INTO Temp ("+tempSQL1[:-1]+") VALUES ("+tempSQL2[:-1]+")")
		# print "INSERT INTO Temp ("+tempSQL1[:-1]+") VALUES ("+tempSQL2[:-1]+")"

		except:
			print("Error: failed to load file to database (line# "+str(count)+", "+str(stopPoint)+") \n")
		 	return 0

		return 1

	def close(self):
		conn.close()
		os.remove(self.dbName)

	def showLine(self, lineNumber):
		# show particular line of rule
		cur.execute("SELECT * FROM Temp where id='"+str(lineNumber)+"'")
		rows = cur.fetchall()
		return rows

	def showRawLine(self, lineNumber):
		try:
			return re.sub(r"[\r|\n]","",lstFileCSV[lineNumber-1])
		except:
			return 0

	def search(self, searchTerm, extract="",groupby=""):
		# searchTerm = [["Maintable","GHS_Global_Default_Table"],["Level","2"]]
		queryWhere = ""
		queryReturn = ""
		if groupby:
			groupby = "GROUP BY "+groupby
		if len(extract)==0:
			queryReturn = "*"
		else:
			for i in extract:
				queryReturn = queryReturn + str(i) + ", "
			queryReturn = queryReturn[:-2]

		for i in searchTerm:
			if len(i)==2:
				queryWhere = queryWhere + str(i[0]) + " = '" +str(i[1]) + "' and "
			else:
				queryWhere = queryWhere + str(i[0]) + " and "
		queryWhere = queryWhere[:-5]

		cur.execute("SELECT "+queryReturn+" FROM Temp WHERE "+queryWhere+" "+groupby)
		rows = cur.fetchall()
		return rows

	def searchDistinct(self, searchTerm, extract=""):
		# searchTerm = [["Maintable","GHS_Global_Default_Table"],["Level","2"]]
		queryWhere = ""
		queryReturn = ""
		
		if len(extract)==0:
			queryReturn = "*"
		else:
			for i in extract:
				queryReturn = queryReturn + str(i) + ", "
			queryReturn = queryReturn[:-2]
		if len(searchTerm):
			for i in searchTerm:
				queryWhere = queryWhere + str(i[0]) + " = '" +str(i[1]) + "' and "
			queryWhere = "WHERE "+queryWhere[:-5]
		else:
			queryWhere = ""
		cur.execute("SELECT DISTINCT "+queryReturn+" FROM Temp "+queryWhere)
		rows = cur.fetchall()
		return rows

	def searchCount(self, searchTerm):
		# searchTerm = [["Maintable","GHS_Global_Default_Table"],["Level","2"]]
		queryWhere = ""

		for i in searchTerm:
			queryWhere = queryWhere + str(i[0]) + " = '" +str(i[1]) + "' and "
		queryWhere = queryWhere[:-5]

		cur.execute("SELECT COUNT(*) FROM Temp WHERE "+queryWhere)
		rows = cur.fetchall()

		return rows

	def showInitialCheck(self):
		query = ""
		for i in self.initialCheckFields:
			query += str(i) + " = '' or "
		query = query[:-3]
		cur.execute("SELECT * FROM Temp WHERE "+query)
		rows = cur.fetchall()
		return rows

# print gDistance("mgr1k","mgr8k",[["8","f"],["8","g"]])
