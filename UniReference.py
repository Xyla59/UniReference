import os #to clear cli
import pyperclip as pc #to copy to clipboard

class refBuild:
    def __init__(self):
        self.specialChar = ['[',']','{','}','(',')','.',',',':',';'] #special characters
        self.keywordIds = ['<','>','#','^'] #keyword ids, userin, /userin, index of userins, italics marker
        self.specialWord = ['Accessed','Available From'] #special words
        self.italics = '\033[3m' #italics starter
        self.end = '\033[0m' #italics ender
        self.inputs = [] #userins
        self.inputsInt = 0 #no. of ins
        self.final_ = "" #final reference
        self.citation_ = "" #final citation
        os.system("cls")
        print("Welcome to UniReference")#intro
        print("Created by Xyla Oldale")
        print("The centralised referencing system for universities")
        print()
        input("Press RETURN to continue ")

    def selectStyle(self): #selects uni style
        styles = []
        count = 1
        num = -1
        stylesF = open("styles.txt", "rt")
        print("Referencing styles available:")
        for line in stylesF: #lists available uni styles
            styles.append(line)
            print("%d. %s" %(count, line))
            count += 1
        while num == -1: #error handled input
            num = self.intIn(1, count-1, "Please select the number of the style desired: ")
        stylesF.close()
        choice = styles[num - 1]
        input("You have selected: %s. Press RETURN to continue " %(choice,))
        os.system("cls")
        return choice
        
    def selectSource(self, style): #selects source type
        sources = []
        count = 1
        num = -1
        file = style + ".txt"
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
        input("You have selected: %s. Press RETURN to continue " %(choice,))
        os.system("cls")
        return choice
        
    def refBuilder(self, style, source): #builds reference and citation
        file = style + ".txt"
        sourcesF = open(file, "rt") #finds ref format
        for line in sourcesF:
            if line.find(source) != -1:
                ref = line
                break
        ind = ref.find(':')
        ref = ref[ind+1:len(ref)]
        keyword = False
        italicsOn = False
        inpOn = False
        inputsInt = 0
        self.final_ = ""
        cite = False
        self.citation_ = ""
        currentDes = ""
        if source == "Other": #other sources not covered
            print("Your source type is not supported by UniReference, please visit:\n \n %s \n\nfor more assistance! \n" %(ref))
        else:
            for x in range(len(ref)): #loops through characters
                char = ref[x]
                if currentDes in self.specialWord: #instant finalises special words
                    self.finalise(currentDes, cite)
                    currentDes = ""
                if char in self.keywordIds: #sorts keywords
                    if char == '<': #userin begin
                        self.finalise(currentDes, cite)
                        currentDes = ""
                        keyword = True
                    elif char == '>' and keyword == True: #userin complete, gets input
                        val = str(self.userIn(currentDes))
                        self.inputs.append(val)
                        inputsInt += 1
                        self.finalise(val, cite)
                        currentDes = ""
                    elif char == '^': #sets italics
                        if italicsOn:
                            self.finalise(self.end ,cite)
                            italicsOn = False
                        else:
                            self.finalise(currentDes, cite)
                            currentDes = ""
                            self.finalise(self.italics, cite)
                            italicsOn = True
                    elif char == '#': #sets getting indexed input
                        if inpOn:
                            self.finalise(self.inputs[int(currentDes)],cite)
                            currentDes = ""
                            inpOn = False
                        else:
                            self.finalise(currentDes, cite)
                            currentDes = ""
                            inpOn = True
                elif char in self.specialChar: #Detects special characters
                    if currentDes != "":
                        if currentDes == 'Citation': #switches to citation
                            currentDes += char
                            cite = True
                            self.finalise(currentDes, cite)
                            currentDes = ""   
                        else:
                            currentDes += char
                    else:
                        self.finalise(char, cite)
                elif char == " ":
                    self.finalise(currentDes, cite)
                    currentDes = ""
                    self.finalise(char, cite)
                else:
                    currentDes += char
            self.print() #formatted printed
            #debug purposes
            #for i in range(len(inputs)):
            #    print(inputs[i])

    def print(self): #formatted printing
        print()
        print("Reference:" + self.final_) #prints reference
        print(self.citation_) #prints citation
        print()
        copy = input("Copy reference to clipboard (y/n): ") #copying ref to clipboard (Error with italics)
        copy = copy.lower()
        if copy == 'y':
            pc.copy(self.final_)
            print("Copied successfully!")
        print()
        copy = input("Copy citation to clipboard (y/n): ") #copying cite to clipboard (Error with italics)
        copy = copy.lower()
        if copy == 'y':
            pc.copy(self.citation_)
            print("Copied successfully!")
        print()
        
    def userIn(self, type): #case/switch of user input markers
        ret = ""
        if type == "lName":
            ret = input("Enter the last name: ")
            ret = ret.title()
        elif type == "fIn":
            ret = input("Enter the first initial: ")
            ret = ret.title()
        elif type == "NoP":
            ret = input("Enter the names of the parties (format 'claimant v defendant'): ")
            ret = ret.title()
        elif type == "abbLaw":
            ret = input("Enter the abbreviated form of the law report: ")
        elif type == "court":
            ret = input("Enter the abbreviated form of the court: ")
        elif type == "org":
            ret = input("Enter the organisation name: ")
            ret = ret.title()
        elif type == "accessDate":
            ret = input("Enter the accessed date (format DD Mon YYYY): ")
        elif type == "writeDate":
            ret = self.intIn(1000,-1,"Enter the year the source was created (format YYYY): ")
        elif type == "title":
            ret = input("Enter the title of the source: ")
        elif type == "place":
            ret = input("Enter the place of publication: ")
            ret = ret.title()
        elif type == "publish":
            ret = input("Enter the publisher: ")
            ret = ret.title()
        elif type == "url":
            ret = input("Enter the url of the webpage: ")
        elif type == "web":
            ret = input("Enter the name of the website: ")
            ret = ret.title()
        elif type == "journal":
            ret = input("Enter the name of the Journal: ")
            ret = ret.title()
        elif type == "posted":
            ret = input("Enter the date the source was posted (format DD Mon): ")
        elif type == "level":
            ret = input("Enter the level of the work (BSc/MSc/PhD): ")
        elif type == "uni":
            ret = input("Enter the name of the university: ")
            ret = ret.title()
        elif type == "time":
            ret = input("Enter the timestamp for the citation (format hh:mm:ss / mm:ss): ")
        elif type == "fPage":
            ret = self.intIn(0,-1,"Enter the first page number: ")
        elif type == "lPage":
            ret = self.intIn(0,-1,"Enter the first page number: ")
        elif type == "vol":
            ret = self.intIn(0,-1,"Enter the volume number: ")
        elif type == "edition":
            ret = self.intIn(0,-1,"Enter the edition number: ")
        elif type == "issue":
            ret = self.intIn(0,-1,"Enter the issue/part number: ")
        elif type == "repNum":
            ret = self.intIn(0,-1,"Enter the report number: ")
        else:
            ret = input("Enter the " + type + ": ")
        if ret == -1:
            ret = ""
        return ret

    def finalise(self, text, cite): #adding to correct variable
        if cite == True:
            self.citation_
            self.citation_ += text
        else:
            self.final_ += text

    def intIn(self, minVal, maxVal, text): #allows integer input error handling
        num = -1
        numstr = input(text)
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

    def main(self): #main selections and processing
        loop = True
        while loop == True: #looping until no more refs wanted
            os.system("cls")
            style = self.selectStyle()#selecting uni style
            source = self.selectSource(style) #selecting source type
            self.refBuilder(style, source) #builds reference and citation
            inp = input("Would you like to build another reference (y/n): ")
            inp = inp.lower()
            if inp == 'n':
                loop = False

if __name__ == "__main__": #first run code
    ref = refBuild()
    ref.main()

