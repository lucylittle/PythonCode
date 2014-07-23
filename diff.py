# file where the diff will be saved
fileDiff = open("diff.txt","w")

#load old file into memory
#ACCHARAS,,g,M,,,,

oldFile = open("G01_old.csv","r")
oldFileMemory = oldFile.readlines()

oldFileToken = {}
newFileToken = {}

tokenDiff = {}

for i in oldFileMemory:
	i = i.split(",")
	if i[0] not in oldFileToken:
		oldFileToken[i[0]] = [i[2],i[3]]


newFile = open("G01_new.csv","r")
newFileMemory = newFile.readlines()


for i in newFileMemory:
	i = i.split(",")
	if i[0] not in newFileToken:
		newFileToken[i[0]] = [i[2],i[3]]

for i in oldFileToken:
	if i not in newFileToken:
		if i not in tokenDiff:
			tokenDiff[i] = "Removed from old G01. Old: ["+str(oldFileToken[i][0])+","+str(oldFileToken[i][1])+"]"
	else:
		if oldFileToken[i] != newFileToken[i]:
			if i not in tokenDiff:
				tokenDiff[i] = "Changed from old G01. Old: [" + str(oldFileToken[i][0]) + "," + str(oldFileToken[i][1])+"]. New: ["+str(newFileToken[i][0])+","+str(newFileToken[i][1])+"]"

for i in newFileToken:
	if i not in oldFileToken:
		if i not in tokenDiff:
			tokenDiff[i] = "added to new G01. New: ["+str(newFileToken[i][0])+","+str(newFileToken[i][1])+"]"
	else:
		if oldFileToken[i] != newFileToken[i]:
			if i not in tokenDiff:
				tokenDiff[i] = "Changed from old G01. Old: ["+str(oldFileToken[i][0])+","+str(oldFileToken[i][1])+"]. New: ["+str(newFileToken[i][0])+","+str(newFileToken[i][1])+"]"
for i in tokenDiff:
	fileDiff.write(str(i)+"; "+str(tokenDiff[i])+"\n")