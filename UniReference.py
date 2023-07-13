import os #to clear cli
import pyperclip as pc #to copy to clipboard

class refBuild:
    def __init__(self):
        self.specialChar = ['[',']','{','}','(',')','.',',',':',';'] #special characters
        self.keywordIds = ['<','>','#','^', '~'] #keyword ids, userin, /userin, index of userins, italics marker, loop marker
        self.specialWord = ['Accessed','Available From'] #special words
        self.italics = '\033[3m' #italics starter
        self.end = '\033[0m' #italics ender
        self.inTypes = [] #input types
        self.inputs = [] #userins
        self.inputsInt = 0 #no. of ins
        self.fType = 1 #final output type
        self.pFType = -1 #prev. final output type
        self.final_ = "" #final reference
        self.finalNI = "" #final ref no italics markers
        self.citation_ = "" #final citation
        self.citationNI = "" #final cite no italics markers 
        self.temp = [] #temp string array for loops
        self.refLoop = 0
        self.clrScr()
        print("Welcome to UniReference!")#intro
        print("Created by Xyla Oldale.")
        print("The centralised referencing system for universities.")
        self.input("Press RETURN to continue ")

    def selectStyle(self): #selects uni style
        styles = []
        count = 1
        num = -1
        stylesF = open("inputFiles/styles.txt", "rt")
        print("Referencing styles available:")
        for line in stylesF: #lists available uni styles
            styles.append(line)
            print("%d. %s" %(count, line))
            count += 1
        while num == -1: #error handled input
            num = self.intIn(1, count-1, "Please select the number of the style desired: ")
        stylesF.close()
        choice = styles[num - 1]
        self.input("You have selected: %s. Press RETURN to continue " %(choice,))
        self.clrScr()
        return choice
        
    def selectSource(self, style): #selects source type
        sources = []
        count = 1
        num = -1
        file = "inputFiles/"+ style + ".txt"
        sourcesF = open(file, "rt")
        print("Referencing sources available:")
        for line in sourcesF: #lists available source types
            ind = line.find(':')
            sourceType = line[0:ind]
            sources.append(sourceType)
            print("%d. %s" %(count, sourceType))
            count += 1
        while num == -1:
            num = self.intIn(1, count-1, "Please select the number of the source desired: ")
        sourcesF.close()
        choice = sources[num - 1]
        self.input("You have selected: %s. Press RETURN to continue " %(choice,))
        self.clrScr()
        return choice

    def clrScr(self): #clears screen and adds exit message to top 
        os.system("cls")
        print("Enter 'EXIT' to close the program at any time.")
        print()
        
    def refBuilder(self, style, source): #builds reference and citation
        file = "inputFiles/" + style + ".txt"
        sourcesF = open(file, "rt") #finds ref format
        for line in sourcesF:
            if line.find(source) != -1:
                ref = line
                break
        ind = ref.find(':')
        ref = ref[ind+2:len(ref)]
        keyword = False
        italicsOn = False
        loopOn = False
        inpOn = False
        inputsInt = 0
        val = ""
        self.final_ = ""
        self.citation_ = ""
        currentDes = ""
        if source == "Other": #other sources not covered
            print("Your source type is not supported by UniReference, please visit:\n \n %s \n\nfor more assistance! \n" %(ref))
        else:
            while self.refLoop < len(ref): #loops through characters
                char = ref[self.refLoop]
                if currentDes in self.specialWord: #instant finalises special words
                    self.finalise(currentDes)
                    currentDes = ""
                if char in self.keywordIds: #sorts keywords
                    if char == '<': #userin begin
                        self.finalise(currentDes)
                        currentDes = ""
                        keyword = True
                    elif char == '>' and keyword == True: #userin complete, gets input
                        self.inTypes.append(currentDes)
                        while val == "":
                            val = str(self.userIn(currentDes))
                        self.inputs.append(val)
                        inputsInt += 1
                        self.finalise(val)
                        currentDes = ""
                        val = ""
                    elif char == '^': #sets italics
                        if italicsOn:
                            self.finalise(self.end)
                            italicsOn = False
                        else:
                            self.finalise(currentDes)
                            currentDes = ""
                            self.finalise(self.italics)
                            italicsOn = True
                    elif char == '#': #sets getting indexed input
                        if inpOn:
                            var = self.inTypes.index(currentDes)
                            if self.inputs[var] != "None" and self.inputs[var] != "Unknown" and "No " not in self.inputs[var]:
                                self.finalise(self.inputs[var])
                            currentDes = ""
                            inpOn = False
                        else:
                            self.finalise(currentDes)
                            currentDes = ""
                            inpOn = True
                    elif char == '~': #loops if more than one input is required
                        self.loop(loopOn, currentDes)
                        currentDes = ""
                        if loopOn == True:
                            loopOn = False
                        else:
                            loopOn = True
                elif char in self.specialChar: #Detects special characters
                    if currentDes != "":
                        if currentDes == 'Citation': #switches to citation
                            currentDes += char
                            self.change(2)
                            currentDes = ""   
                        else:
                            currentDes += char
                    else:
                        self.finalise(char)
                elif char == " ":
                    self.finalise(currentDes)
                    currentDes = ""
                    self.finalise(char)
                else:
                    currentDes += char
                self.refLoop += 1
            self.print() #formatted printed

    def change(self, fType): #changes finalisation type and records previous 
        if self.fType != fType:
            self.pFType = self.fType
            self.fType = fType

    def loop(self, loopOn, varStr): #loops for more inputs, for more authors etc
        if loopOn:
            self.change(0)
            try:
                ind = varStr.find(',')
            except:
                ind = -1
            if ind != -1:
                text = varStr[0:ind]
                revert = int(varStr[ind+1:len(varStr)])
                inp = self.input("Would you like to insert another " + text + " (y/n): ")
                if inp.lower() == 'y':
                    self.finalise(", ")
                    self.refLoop -= revert
                else:
                    self.change(self.pFType)
                    try:
                        ind = self.temp.index(", ")
                    except:
                        ind = -1
                    if ind != -1:
                        while ind != -1:
                            prev = ind
                            try:
                                ind = self.temp.index(", ", prev+1)
                            except:
                                ind = -1
                        self.temp[prev] = " and "
                        for y in range(0, len(self.temp)):
                            self.finalise(self.temp[y])
            else:
                self.temp = []
                count = self.inTypes.count(varStr)
                if count == 2 or count == 3: #requires "and" word to be included in citation
                    ind = self.inTypes.index(varStr)
                    prev = ind
                    for z in range(0, count - 1):
                        try:
                            ind = self.inTypes.index(varStr, prev + 1)
                            self.finalise(", ")
                            self.finalise(self.inputs[ind])
                            prev = ind
                        except:
                            print(end="")
                    self.change(self.pFType)
                    ind = self.temp.index(", ")
                    if count == 3:
                        ind = self.temp.index(", ", ind + 1)
                    self.temp[ind] = " and "
                    for zz in range(0, len(self.temp)):
                        self.finalise(self.temp[zz])
                elif count > 3: #requires "et al." in citation
                    self.change(self.pFType)
                    self.finalise(self.italics)
                    self.finalise(" et al.")
                    self.finalise(self.end)
                else:
                    self.change(self.pFType)
            loopOn = False
        else:
            self.finalise(varStr)
            loopOn = True         

    def print(self): #formatted printing
        self.clrScr()
        print("Reference:" + self.final_) #prints reference
        print("Citation:" + self.citation_) #prints citation
        print()
        print("NOTE: Copying and saving removes italics from reference and citation, replaced with '*' either side of the italicised word")
        copy = self.input("Copy reference to clipboard (y/n): ") #copying ref to clipboard, doesn't copy italic markers, replaced with *
        copy = copy.lower()
        if copy == 'y':
            pc.copy(self.finalNI)
            print("Copied reference successfully!")
        print()
        copy = self.input("Copy citation to clipboard (y/n): ") #copying cite to clipboard, doesn't copy italic markers, replaced with *
        copy = copy.lower()
        if copy == 'y':
            pc.copy(self.citationNI)
            print("Copied citation successfully!")
        print()
        self.save()

    def input(self, text): #input validation
        inp = input(text)
        if inp == "EXIT":
            self.exit()
        #checks for illegal characters, chr(92) is "\"
        elif "*" in inp or "@" in inp or "#" in inp or "/" in inp or "%" in inp or "$" in inp or "£" in inp or "<" in inp or ">" in inp or '\\' in inp or "|" in inp or chr(92) in inp or "{" in inp or "}" in inp:
            inp = -1
            print("Error: Input must not contain illegal characters (*, @, #, /, %, $, £, <, >, \, |, {, })")
        return inp
        
    def userIn(self, type): #case/switch of user input markers
        ret = ""
        if type == "lName":
            ret = self.input("Enter the last name: ")
            ret = ret.title()
        elif type == "fIn":
            ret = self.input("Enter the first initial: ")
            ret = ret.title()
        elif type == "act":
            ret = self.input("Enter the name of the Act: ")
            ret = ret.title()
        elif type == "NoP":
            ret = self.input("Enter the names of the parties (format 'claimant v defendant'): ")
            ret = ret.title()
        elif type == "abbLaw":
            ret = self.input("Enter the abbreviated form of the law report: ")
        elif type == "court":
            ret = self.input("Enter the abbreviated form of the court: ")
        elif type == "org":
            ret = self.input("Enter the organisation name: ")
            ret = ret.title()
        elif type == "accessDate":
            ret = self.input("Enter the accessed date (format DD Mon YYYY): ")
        elif type == "writeDate":
            ret = self.intIn(1000,-1,"Enter the year the source was created (format YYYY): ")
        elif type == "title":
            ret = self.input("Enter the title of the source: ")
        elif type == "place":
            ret = self.input("Enter the place of publication: ")
            ret = ret.title()
        elif type == "publish":
            ret = self.input("Enter the publisher: ")
            ret = ret.title()
        elif type == "url":
            ret = self.input("Enter the url of the webpage: ")
        elif type == "web":
            ret = self.input("Enter the name of the website: ")
            ret = ret.title()
        elif type == "journal":
            ret = self.input("Enter the name of the Journal: ")
            ret = ret.title()
        elif type == "news":
            ret = self.input("Enter the name of the Newspaper: ")
            ret = ret.title()
        elif type == "posted":
            ret = self.input("Enter the date the source was posted (format DD Mon): ")
        elif type == "level":
            ret = self.input("Enter the level of the work (BSc/MSc/PhD): ")
        elif type == "uni":
            ret = self.input("Enter the name of the university: ")
            ret = ret.title()
        elif type == "time":
            ret = self.input("Enter the timestamp for the citation (format hh:mm:ss / mm:ss): ")
        elif type == "fPage":
            ret = self.intIn(0,-1,"Enter the first page number: ")
        elif type == "lPage":
            ret = self.intIn(0,-1,"Enter the last page number: ")
        elif type == "vol":
            ret = self.intIn(0,-1,"Enter the volume number: ")
        elif type == "edition":
            ret = self.intIn(0,-1,"Enter the edition number: ")
        elif type == "issue":
            ret = self.intIn(0,-1,"Enter the issue/part number: ")
        elif type == "repNum":
            ret = self.intIn(0,-1,"Enter the report number: ")
        elif type == "chap":
            ret = self.intIn(0,-1,"Enter the chapter number: ")
        elif type == "sec":
            ret = self.input("Enter the section number (format: section(subsection)(part)): ")
        else:
            ret = self.input("Enter the " + type + ": ")
        if ret == -1:
            ret = ""
        return ret

    def finalise(self, text): #adding to correct variable
        if self.fType == 2:
            self.citation_ += text
            if text == self.italics or text == self.end:
                self.citationNI += "*"
            else:
                self.citationNI += text
        elif self.fType == 1:
            self.final_ += text
            if text == self.italics or text == self.end:
                self.finalNI += "*"
            else:
                self.finalNI += text
        elif self.fType == 0:
            self.temp.append(text)

    def intIn(self, minVal, maxVal, text): #allows integer input error handling
        num = -1
        numstr = self.input(text)
        if numstr != -1:
            numstr = numstr.title()
            if self.refLoop != 0 and ("None" in numstr or "No " in numstr or "Unknown" in numstr):
                return numstr
            try:
                num = int(numstr)
                if minVal >= -1:
                    if num < minVal: #lower integer error handling
                        print("ERROR: Please enter a number greater than", minVal)
                        num = -1
                if maxVal > -1:
                    if num > maxVal: #higher integer error handling
                        print("ERROR: Please enter a number less than", maxVal)
                        num = -1
            except: #other type error handling
                if (numstr != ""):
                    print("ERROR: Please enter a whole number")
                num = -1
        return num
    
    def save(self): #saving to file
        loop = True
        fileName = ""
        inp = self.input("Would you like to save this reference to a file (y/n): ")
        print()
        if inp.lower() == 'y':
            while loop:
                new = self.input("Would you like to save to a new file (n) or an existing file (e): ")
                print()
                if new.lower() == 'n': #new file
                    loop = False
                    try:
                        os.chdir(os.getcwd() + "\\outputFiles")
                        fileName = self.input("Enter the file name: ")
                        if fileName[-4] != ".":
                            fileName += ".txt"
                        nFile = open(fileName, "w")
                        nFile.write("References:\n")
                        nFile.write(self.finalNI + "\n")
                        nFile.close()
                        os.chdir("..")
                        print()
                        print("File created and written to successfully!")
                    except Exception as e:
                        print("ERROR: Unexpected error creating file")
                        print(e)
                elif new.lower() == 'e': #existing file
                    loop = False
                    entries = []
                    count = 0
                    overwrite = True
                    try:
                        os.chdir(os.getcwd() + "\\outputFiles") #changes directory to output files
                        print("Files available:")
                        print()
                        os.system("Dir /B") #prints files available
                        print()
                        fileName = self.input("Enter the file name: ")
                        if fileName[-4] != ".":
                            fileName += ".txt"
                        eFile = open(fileName, "r") #reads file for sorting
                        for line in eFile:
                            entries.append(line)
                            count += 1
                        j = 0
                        nEntries = []
                        for x in range(0, count+1):
                            nEntries.append(" ")
                        nEntries[0] = "References:\n"
                        i = 1
                        while i <= count: #sorts into alphabetical then saves to file
                            if ord(entries[i][j]) > ord(self.final_[j]):
                                if overwrite:
                                    i -= 1
                                nEntries[i] = self.finalNI + "\n"
                                i += 1
                                nEntries[i] = entries[i-1]
                                for k in range(i, count):
                                    nEntries[k+1] = entries[k]
                                break
                            elif ord(entries[i][j]) == ord(self.final_[j]):
                                j += 1
                                i -= 1
                                overwrite = False
                            else:
                                nEntries[i] = entries[i]
                                j = 0
                            i += 1
                        eFile.close()
                        eFile = open(fileName, "w")
                        for item in nEntries:
                            eFile.write(item)
                        eFile.close()
                        os.chdir("..") #backs out of outputFiles directory
                        print()
                        print("File written to successfully!")
                    except IndexError: #If reaches end, adds new reference to end
                        nEntries[count] = self.finalNI + "\n"
                        eFile.close()
                        eFile = open(fileName, "w")
                        for item in nEntries:
                            eFile.write(item)
                        eFile.close()
                        os.chdir("..")
                        print()
                        print("File written to successfully!")
                    except Exception as e:
                        print("ERROR: Unexpected error accessing file")
                        print("Error Message: " + str(e))
                else:
                    print("ERROR: Invalid input, try again")

    
    def reset(self): #resets variables for new reference
        self.inTypes = []
        self.inputs = []
        self.inputsInt = 0
        self.fType = 1
        self.pFType = -1
        self.final_ = "" 
        self.citation_ = ""
        self.finalNI = ""
        self.citationNI = ""
        self.temp = []
        self.refLoop = 0

    def exit(self): #exits program
        print()
        input("Thank you for using this program, press ENTER to exit ")
        os._exit(0)

    def main(self): #main selections and processing
        loop = True
        while loop == True: #looping until no more refs wanted
            self.clrScr()
            style = self.selectStyle()#selecting uni style
            source = self.selectSource(style) #selecting source type
            self.refBuilder(style, source) #builds reference and citation
            inp = self.input("Would you like to build another reference (y/n): ")
            inp = inp.lower()
            if inp == 'n':
                loop = False
            self.reset()
        input("Thank you, press ENTER to exit ")

ref = refBuild() #initialises builder
ref.main() #runs builder