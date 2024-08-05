"""Zachary Buchanan, PSID: 1011703"""

import time

#Defining class for each item within the input files
class InventoryItem:
    def __init__(self, itemId, manufacturer, itemType, price, serviceDate, damaged):
        self.itemId = itemId
        self.manufacturer = manufacturer
        self.itemType = itemType
        self.price = price
        self.serviceDate = serviceDate
        self.damaged = damaged

#Defining function to read data from CSV files
def readCsvFile(filename):
    file = open(filename, 'r')
    data = []
    for line in file:
        data.append(line.strip().split(','))
    file.close()
    return data

#Defining function to write data to CSV files
def writeCsvFile(filename, data):
    file = open(filename, 'w')
    for row in data:
        file.write(','.join(row) + '\n')
    file.close()

#Defining function to merge data from the three input files to a dictionary used in creating the output files
def mergeData(manufacturerList, priceList, serviceDatesList):
    items = {}
    
    #Defining each column's value in the Manufacturer List CSV file
    for row in manufacturerList:
        itemId = row[0]
        items[itemId] = InventoryItem(
            itemId,
            row[1],
            row[2],
            None,
            None,
            row[3]
        )
    
    #Defining each column's value in the Price List CSV file
    for row in priceList:
        itemId = row[0]
        if itemId in items:
            items[itemId].price = row[1]
    
    #Defining each column's value in the Service Dates List CSV file
    for row in serviceDatesList:
        itemId = row[0]
        if itemId in items:
            items[itemId].serviceDate = row[1]
    
    return items

#Defining functions to sort inventory lists
def sortByManufacturer(item):
    return item.manufacturer

def sortByItemId(item):
    return item.itemId

def sortByServiceDate(item):
    return convertToDate(item.serviceDate)

def sortByPrice(item):
    return float(item.price)

#Defining the function to collect the current date using the time module
def getCurrentDate():
    return time.strftime('%m/%d/%Y')

#Converting the date to multiple pieces to more easily compare strings
def convertToDate(dateStr):
    month, day, year = map(int, dateStr.split('/'))
    return (year, month, day)

#Defining function to create the Full Inventory CSV file
def createFullInventory(items):
    #Sorting items by manufacturer name
    sortedItems = sorted(items.values(), key=sortByManufacturer)
    
    #Defining what entries are appended to the inventory list
    data = []
    for item in sortedItems:
        data.append([
            item.itemId,
            item.manufacturer,
            item.itemType,
            item.price,
            item.serviceDate,
            item.damaged
        ])
    
    writeCsvFile('FullInventory.csv', data)

def createItemTypeInventories(items):
    itemTypes = {}
    
    #Adding unique item types from the inventory
    for item in items.values():
        if item.itemType not in itemTypes:
            itemTypes[item.itemType] = []
        itemTypes[item.itemType].append(item)
    
    
    for itemType, itemsList in itemTypes.items():
        #Sorting items by ID number
        sortedItems = sorted(itemsList, key=sortByItemId)
        
        #Defining what entries are appended to the inventory list
        data = []
        for item in sortedItems:
            data.append([
                item.itemId,
                item.manufacturer,
                item.price,
                item.serviceDate,
                item.damaged
            ])
        
        filename = itemType.capitalize() + 'Inventory.csv'
        writeCsvFile(filename, data)

def createPastServiceDateInventory(items):
    #Defining value to compare against for service date
    today = convertToDate(getCurrentDate())
    
    #Adding items past service date to list
    pastServiceItems = [item for item in items.values() if convertToDate(item.serviceDate) < today]
    
    #Sorting items by service date
    sortedItems = sorted(pastServiceItems, key=sortByServiceDate)
    
    #Defining what entries are appended to the inventory list
    data = []
    for item in sortedItems:
        data.append([
            item.itemId,
            item.manufacturer,
            item.itemType,
            item.price,
            item.serviceDate,
            item.damaged
        ])
    
    writeCsvFile('PastServiceDateInventory.csv', data)

def createDamagedInventory(items):
    #Adding damaged items to list
    damagedItems = [item for item in items.values() if item.damaged.lower() == 'damaged']
    
    #Sorting items by price
    sortedItems = sorted(damagedItems, key=sortByPrice, reverse=True)
    
    #Defining what entries are appended to the inventory list
    data = []
    for item in sortedItems:
        data.append([
            item.itemId,
            item.manufacturer,
            item.itemType,
            item.price,
            item.serviceDate
        ])
    
    writeCsvFile('DamagedInventory.csv', data)

def main():
    #Reading Manufacturer List
    manufacturerList = readCsvFile('ManufacturerList.csv')
    
    # Reading Price List
    priceList = readCsvFile('PriceList.csv')
    
    # Reading Service Dates List
    serviceDatesList = readCsvFile('ServiceDatesList.csv')
    
    #Combining and matching all the data into one table
    items = mergeData(manufacturerList, priceList, serviceDatesList)
    
    #Calling output functions with the merged data table
    createFullInventory(items)
    createItemTypeInventories(items)
    createPastServiceDateInventory(items)
    createDamagedInventory(items)

if __name__ == '__main__':
    main()