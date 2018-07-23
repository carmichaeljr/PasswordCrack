import sys
import time
import zipfile
import itertools

ZIP_FILE_NAME = "planz.zip"		# The file name of the zip file.
FIRST_HALF_PASSWORD = "Super"	# The first part of the password. We know this for sure!
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
EXTRA_CHARACTERS="!@#$%^&*()_+~`-={[}]\|;:'\",<.>/?"
NUMBERS="0123456789"


def getLenOfPassword():
	rv=0
	inputValid=False
	while not inputValid:
		try:
			rv=int(input("?> What is the length of the password? "))
			inputValid=True
		except Exception:
			print("!> Please enter an integer valie.")
	return rv

		
def checkListAgainstList(list1, list2):
	rv=list()
	for char1 in list1:
		for char2 in list2:
			rv.append("{0}{1}".format(char1,char2))
	return rv
			
			
def orderPosibilitiesLists(allPossibilitiesList, numOfCharsNeeded):
	#Generates the pattern:
	# 1,1,1		2,1,1	3,1,1
	# 1,1,2     2,1,2   3,1,2
	# 1,1,3     2,1,3   3,1,3
	# 1,2,1     2,2,1   3,2,1
	# 1,2,2     2,2,2   3,2,2
	# 1,2,3     2,2,3   3,2,3
	# 1,3,1     2,3,1   3,3,1
	# 1,3,2     2,3,2   3,3,2
	# 1,3,3     2,3,3   3,3,3
	#...where each number represents a list
	tickerList=list()
	yieldList=list()
	for x in range(0,numOfCharsNeeded):
		tickerList.append(0)
		yieldList.append(list())
	while tickerList[0]<len(allPossibilitiesList):
		for x in range(len(tickerList)-1,0,-1):
			if tickerList[x]>=len(allPossibilitiesList):
				tickerList[x-1]+=1
				tickerList[x]=0
		if tickerList[0]<len(allPossibilitiesList):
			for x in range(0,len(yieldList)):
				yieldList[x]=allPossibilitiesList[tickerList[x]]
			yield yieldList
		tickerList[len(tickerList)-1]+=1
				
				
def getTotalNumOfPassords(allPossibilitiesList,numOfCharsNeeded):
	totalNumOfChars=(len(allPossibilitiesList[0])+len(allPossibilitiesList[1])+\
			len(allPossibilitiesList[2]))
	# totalNumOfCharsWithRepeats=totalNumOfChars*2
	return (totalNumOfChars**numOfCharsNeeded)
					
					
def generatePasswords(allPossibilitiesGenerator):
	for possibilityList in allPossibilitiesGenerator:
		tickerList=list()	#ticker list represents position in each sub-list
		endOfCurrentPossibilities=False;
		for x in range(0,len(possibilityList)):
			tickerList.append(0)
		while not endOfCurrentPossibilities:
			for x in range(len(tickerList)-1,-1,-1):
				if x==0 and tickerList[x]>=len(possibilityList[x]):
					endOfCurrentPossibilities=True
				elif tickerList[x]>=len(possibilityList[x]):
					tickerList[x-1]+=1
					tickerList[x]=0
			if not endOfCurrentPossibilities:
				yieldStr=""
				for x in range(0,len(possibilityList)):
					yieldStr+=possibilityList[x][tickerList[x]]
				yield yieldStr
			tickerList[len(tickerList)-1]+=1

				
def bruteForce(corruptFile, passwordGenerator, totalNumOfPassowrds):
	rv=""
	count=0
	for possibility in passwordGenerator:
		count+=1
		iterationPswd=FIRST_HALF_PASSWORD+possibility
		printProgress(iterationPswd,count,totalNumOfPassowrds)
		if extractFile(corruptFile,iterationPswd):
			rv=iterationPswd
			break;
	print()
	return rv;
	
	
def extractFile(givenFile, password):
    try:
        givenFile.extractall(pwd=password.encode())
        return True
    except KeyboardInterrupt:
        exit(0)
    except zipfile.BadZipFile:
        pass #Means pswd was incorrect
    except RuntimeError:
        pass	#Means pswd was incorrect


def printProgress(pswd,currentPswd,totalPswd):
	progressBar="["
	progressBar+="#"*(int(20*currentPswd/totalPswd))
	progressBar+=" "*(int(20*(totalPswd-currentPswd)/totalPswd))
	progressBar+="]"
	percent=100*(currentPswd/totalPswd)
	print("\rTrying pswd: {0}  [{1} of {2}] {3}: {4}%".format(
			pswd,currentPswd,totalPswd,
			progressBar,percent),end="")
	
	
def printInformation(pswd):
	if not pswd=="":
		print("Success: pswd found")
		print("  . Pswd: {0}".format(pswd))
	else:
		print("Failure: pswd not found")
	
	
def debug():
	lenOfPassword=getLenOfPassword()
	allPossibilitiesList=[['1','2','3'],['4','5','6'],['7','8','9']]
	allPossibilities=orderPosibilitiesLists(allPossibilitiesList,lenOfPassword)
	totalNumOfPassowrds=getTotalNumOfPassords(allPossibilitiesList,lenOfPassword)
	
	with zipfile.ZipFile(ZIP_FILE_NAME,"r") as corruptFile:
		counter=0
		allPasswords=generatePasswords(allPossibilities)
		pswd=bruteForce(corruptFile,allPasswords,totalNumOfPassowrds)
		printInformation(pswd)
	
	
def run():
	lenOfPassword=getLenOfPassword()
	corruptFile = zipfile.ZipFile(ZIP_FILE_NAME)	#The reference to the zip file we cannot open...
	allPossibilitiesList=[ALPHABET,EXTRA_CHARACTERS,NUMBERS]
	allPossibilities=orderPosibilitiesLists(allPossibilitiesList,lenOfPassword)
	totalNumOfPassowrds=getTotalNumOfPassords(allPossibilitiesList,lenOfPassword)
	
	allPasswords=generatePasswords(allPossibilities)
	pswd=bruteForce(corruptFile,allPasswords,totalNumOfPassowrds)
	printInformation(pswd)

	
def main():
	# argv[0] is the name of the program running(aka. this script)
	if len(sys.argv)>1 and sys.argv[1]=="debug":	
		debug()
	else:
		run()
	
main()


#================================ OLD SHIT ==================================================
# # We know they always have 3 characters after Super...
# # For every possible combination of 3 letters from alphabet...
# for c in itertools.product(alphabet, repeat=3):
    # # Slowing it down on purpose to make it work better with the web terminal
    # # Remove at your peril
    # time.sleep(0.001)
    # # Add the three letters to the first half of the password.
    # password = first_half_password+''.join(c)
    # # Try to extract the file.
    # print "Trying: %s" % password
    # # If the file was extracted, you found the right password.
    # if extractFile(zip_file, password):
        # print '*' * 20
        # print 'Password found: %s' % password
        # print 'Files extracted...'
        # exit(0)

# # If no password was found by the end, let us know!
# print 'Password not found.'
