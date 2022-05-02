import csv
import os

csvCount = {}
codeName = {}
invAudit = {}
usrinput = ""


if not os.path.exists('stockaudit.csv'):
    print("stockaudit.csv file not found. Please import stockquery audit file.")
    quit()

reader = csv.reader(open('stockaudit.csv', 'r'))


for row in reader:
    code, name, count = row
    if code != "Product Number":
        csvCount[code] = 0 + int(float(count))
        codeName[code] = name
        invAudit[code] = 0
        print(code, codeName[code], csvCount[code])

while usrinput != "q" :
    usrinput = input("Scan item! (q to quit):")
    for x in invAudit:
        if usrinput == x:
            invAudit[x] += 1
            print(x, " now equals ", invAudit[x])


print("exiting input")

for code in invAudit:
    print(codeName[code], csvCount[code])

print(" \n \n \n \n \n")
print("difference in inventory")

if os.path.exists('AuditResults.csv'):
    os.remove('AuditResults.csv')

outfile = open('AuditResults.csv', 'x')

writer = csv.writer(outfile)

writer.writerow(["Product Name", "Difference in Count"])

for code in invAudit:
    name = codeName[code]
    diff = (csvCount[code] - invAudit[code]) * -1
    print("Product Name ------------ Difference in count")
    print(name, "------------", diff)
    writer.writerow([name, diff])
print("\nResult written to AuditResults.csv.\n\n")
print("Thanks for using Inventory Audit.")
print("Program Created by Brandon Workman May 2nd, 2022")
print("")
