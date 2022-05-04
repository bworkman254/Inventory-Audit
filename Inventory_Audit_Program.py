from datetime import date
import csv
import os

csvCount = {}
codeName = {}
invAudit = {}
userInput = ""
outputText = ""

today = str(date.today())
readFileName = "stockaudit.csv"
saveFileName = 'U:/StockQueryAudits/AuditResults-' + today + '.csv'


def openfile():
    if not os.path.exists(readFileName):
        print(readFileName, "file not found. Please import stockquery audit file.")
        quit()

    reader = csv.reader(open('stockaudit.csv', 'r'))
    return reader


# noinspection SpellCheckingInspection
def printcsv(reader):
    print("{:^15}     {:^48}     {:^15}".format("Product Code", "Product Name", "Stock Query Count"))
    print('--------------------------------------------------------------------------------------------')
    for row in reader:
        code, name, count = row
        if code != "Product Number":
            csvCount[code] = 0 + int(float(count))
            codeName[code] = name
            invAudit[code] = 0
            print("{:^15} --- {:^48} --- {:^15}".format(code, codeName[code], csvCount[code]))

    print("")


def scanitems():
    while usrinput != "q":
        usrinput = input("Scan item! (q to quit):")
        for x in invAudit:
            if usrinput == x:
                invAudit[x] += 1
                print(x, " now equals ", invAudit[x])

    print("\n\nexiting input\n\n")


def physicalinventory():
    print("{:^80}".format("PHYSICAL INVENTORY"))
    print("{:^80}".format("--------------------\n"))
    print("{:^45}  {:^15}  {:^12}".format("Product Name", "", "Physical Count"))
    print('--------------------------------------------------------------------------------------------')
    for code in invAudit:
        print('{:^45}  {:^15}  {:>8}'.format(codeName[code], "", invAudit[code]))

    print("\n\n")


def diffenceinstock():
    print("{:^80}".format("DIFFERENCE IN PHYSICAL INVENTORY"))
    print("{:^80}".format("-----------------------------------\n"))
    outputtext = '{:^45}  {:^15}  {:^12}'.format("Product Name", "", "Difference in count")

    print(outputtext)
    print('_________________________________________________________________________________________')
    for code in invAudit:
        name = codeName[code]
        diff = (csvCount[code] - invAudit[code]) * -1
        outputtext = '{:^45}  {:^15}  {:>8}'.format(name, "------------", diff)
        print(outputtext)
    print("\n\n")


def outputdifference():
    if os.path.exists(saveFileName):
        os.remove(saveFileName)

    outfile = open(saveFileName, 'x')

    writer = csv.writer(outfile)

    writer.writerow(["Product Name", "Difference in Count"])
    for code in invAudit:
        name = codeName[code]
        diff = (csvCount[code] - invAudit[code]) * -1
        writer.writerow([name, diff])
    print("\nResult written to", saveFileName, "\n\n")


def printmenu():
    print("\n\nMenu")
    print("-------")
    print("q - quit")
    print("i - scan items")
    print("p - current scanned stock")
    print("d - difference in scanned stock and stock query")
    print("v - stockquery stock")
    print("s - save difference in stock to file")


def menu(reader):
    menuinput = ""
    while menuinput != "q":
        printmenu()
        menuinput = input("\nWhat would you like to do?: ")
        if menuinput == "i":
            scanitems()
        elif menuinput == "p":
            physicalinventory()
        elif menuinput == "d":
            diffenceinstock()
        elif menuinput == "v":
            printcsv(reader)
        elif menuinput == "s":
            outputdifference()


def main():
    reader = openfile()
    printcsv(reader)
    menu(reader)

    print("\n\n\n\nThanks for using Inventory Audit.")
    print("Program Created by Brandon Workman May 2nd, 2022")
    print("")


main()
