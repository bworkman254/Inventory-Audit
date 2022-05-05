# ********************************************************
# *********** Inventory Audit Program ********************
# ********************* by *******************************
# ************** Brandon Workman *************************
# ********************************************************

from datetime import date
import csv
import os


class Invaudit(object):
    csvCount = {}  # stock query count dictionary
    codeName = {}  # proct numbe name reference dictionary
    invAudit = {}  # scanned items dictionary

    #important variables
    today = str(date.today())
    has_saved = 0

    # probably pointless variables
    userinput = ""
    outputText = ""

    # save file variables
    inputfolder = "INSERT FILE HERE/"
    outputfolder = "OUTPUT FOLDER/"

    save_file_name = outputfolder + 'AuditResults-' + today + '.csv'

    ###################################
    ######### Functions Below #########
    ###################################

    def openfile(self):  # function to open stock query file
        print("Be sure that file is located in the \"INSERT FILE HERE\" folder")  # print to warn user of location
        read_file_name = input("\nPlease enter csv file name. \n(example: examplefile) (Type quit to exit): ")  # ask for file name
        if read_file_name != "quit":  # as long as file name isn't quit
            read_file_name = self.inputfolder + read_file_name + ".csv" # add folder name and file extension tol file name
            if not os.path.exists(read_file_name):  # if file doesn't exist
                print("\n\nFile not found.")  # output result
                self.openfile() # and retry
        else: # if user types quit
            self.quitprogram() # quit progra,

        reader = csv.reader(open(read_file_name, 'r')) # set reader to now opened file
        return reader # return reader

    def printcsv(self): # function to print csv input
        print("{:^15}     {:^48}     {:^15}".format("Product Code", "Product Name", "Stock Query Count"))
        print('--------------------------------------------------------------------------------------------')
        for code in self.csvCount:
            print("{:^15} --- {:^48} --- {:^15}".format(code, self.codeName[code], self.csvCount[code]))

    # noinspection SpellCheckingInspection
    def populatelists(self, reader):  # function to populate the dictionaries
        for row in reader: # for every row in csv file
            code, name, count = row  # setup 3 variables to read each colum of data in that row
            if code != "Product Number":  # exclude the title line
                self.csvCount[code] = int(float(count))  # ties stock query count to product code
                self.codeName[code] = name  # ties intem name to product code
                self.invAudit[code] = 0  # set scanned stock to 0 by default

        print("")

    def scanitems(self):  # function to scan physical stock
        userinput = ""
        while userinput != "q":  # press q to quit
            userinput = input("Scan item! (q to quit):")  # input product code
            for x in self.invAudit:  # check items in invAudit dictionary
                if userinput == x:  # make sure scanned item matches a dictionary item
                    self.invAudit[x] += 1 #  tick the match up by 1
                    print(x, " now equals ", self.invAudit[x], "\n")  # print the new total for that dictionary item

        print("\n\nExiting Scan Input\n\n")  # notify user that they have left the item scan
        self.has_saved = 0  # enable are you sure prompt when quitting program to prevent unsaved changes from being lost

    def physicalinventory(self):  # function to output scanned stock
        print("{:^80}".format("PHYSICAL INVENTORY"))
        print("{:^80}".format("--------------------\n"))
        print("{:^45}  {:^15}  {:^12}".format("Product Name", "", "Physical Count"))
        print('--------------------------------------------------------------------------------------------')
        for code in self.invAudit:
            print('{:^45}  {:^15}  {:>8}'.format(self.codeName[code], "", self.invAudit[code]))

        print("\n\n")

    def diffenceinstock(self):  # function to output the diffference between scanned stock and stock query stock
        print("{:^80}".format("DIFFERENCE IN PHYSICAL INVENTORY"))
        print("{:^80}".format("-----------------------------------\n"))
        outputtext = '{:^45}  {:^15}  {:^12}'.format("Product Name", "", "Difference in count")

        print(outputtext)
        print('_________________________________________________________________________________________')
        for code in self.invAudit:
            name = self.codeName[code]
            diff = (self.csvCount[code] - self.invAudit[code]) * -1
            outputtext = '{:^45}  {:^15}  {:>8}'.format(name, "------------", diff)
            print(outputtext)
        print("\n\n")

    def outputdifference(self):  #function to save the difference in stock
        if not os.path.isdir(self.outputfolder): # check if output folder doesn't exist
            os.mkdir(self.outputfolder)  #if not create the folder
            print("\ns", self.outputfolder, "created")
        if os.path.exists(self.save_file_name): #check if filename exists
            os.remove(self.save_file_name)  # if it does, delete it for fresh start

        outfile = open(self.save_file_name, 'x')  # create new save file

        writer = csv.writer(outfile)  # write to file

        writer.writerow(["Product Name", "Stock Query Count", "Scanned Count", "Difference in Count"]) # write title row
        for code in self.invAudit:  # reference intems in scanned items dictionary
            name = self.codeName[code]  # set item name
            diff = (self.csvCount[code] - self.invAudit[code]) * -1  # do the maths to find the difference
            writer.writerow([name, self.csvCount[code], self.invAudit[code], diff])  # write everything to a new line
        print("\nResult written to", self.save_file_name, "\n\n")  # confirmation that the file has been written
        self.has_saved = 1  # disable 'are you sure' prompt

    @staticmethod
    def printmenu(): # this just outputs the main menu to the cli
        print("\n\nMenu")
        print("-------")
        print("q - quit")
        print("i - scan items")
        print("p - current scanned stock")
        print("d - difference in scanned stock and stock query")
        print("v - stockquery stock")
        print("s - save results")

    def menu(self):  # lets the user choose what to do
        menu_input = ""
        while menu_input != "q":
            self.printmenu()  # what are the options?
            menu_input = input("\nWhat would you like to do?: ")  # make a choice
            if menu_input == "i":
                self.scanitems()  # lets scan some items
            elif menu_input == "p":
                self.physicalinventory()  # what have I scanned so far
            elif menu_input == "d":
                self.diffenceinstock()  # what is the difference from my supposed count to my actual count
            elif menu_input == "v":
                self.printcsv()  # what is my inventory supposed to be?
            elif menu_input == "s":
                self.outputdifference()  # lets save my file
        while self.has_saved == 0:  # as long as file hasn't been saved since last change, it will prompt you
            yousure = input(
                "It appears you havent saved your differences in stock. Are you sure you'd like to quit? (y/n)")
            if yousure == "y":
                self.quitprogram()  # i dont care if I havent saved, lets quit anyways
            elif yousure == "n":
                self.menu()  # i changed my mind. lets go back to the menu
        self.quitprogram() # quit program

    @staticmethod
    def quitprogram():  # function for leaving and output the creator
        print("\n\n\n\nThanks for using Inventory Audit.")
        print("Program Created by Brandon Workman May 2nd, 2022")
        print(input("\n\nPress any button to end program"))
        print("")
        quit()  # bye bye

    def main(self): # this may be redundant, but it's the main portion of the code that gets executed on startup.
        start = input("Welcome to the Inventory Audit Program! \nPress enter to continue!")
        if not os.path.isdir(self.inputfolder):  # check for input folder
            os.mkdir(self.inputfolder)  # make one if it doesnt exist
            print("\n", self.inputfolder, "created. Please insert your csv file into folder.")
        reader = self.openfile()  # lets open a file
        self.populatelists(reader)  # populate the lists with the file
        self.printcsv()  # initial output of csv contents
        self.menu()  # Show me the Menu!


self = Invaudit()  # self is this object
self.main()  # startup the main function
