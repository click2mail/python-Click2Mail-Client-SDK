from api import c2mAPI
c2m = c2mAPI.c2mAPIBatch("username","password","0")#change to 1 for production
c2m.setFileName("myFileName","test.pdf") #set the name ane file path for batch

po = c2mAPI.printOptions('Letter 8.5 x 11','Next Day','Address on Separate Page','Full Color','White 24#','Printing both sides','First Class','#10 Double Window')
ad = c2mAPI.returnAddress("John Doe","MyCompany","12345 Test St","ste 335","Oak Brook","IL","60523")

addList = [] #For Batch please populate address fields appropriately, field names cannot change
address = {'name':'test','organization':'test2','address1':'1235 test street','address2':'ste 1234','address3':'','city':'Oak Brook','state':'IL','postalCode':'60523','country':'US'}	
addList.append(address)
address = {'name':'test2','organization':'test2','address1':'1235 test street','address2':'ste 1234','address3':'','city':'Oak Brook','state':'IL','postalCode':'60523','country':'US'}	
addList.append(address)

#start page, end page, print options, return address, address List for page range
c2m.addJob("1","2",po,ad,addList)


#starting second job in batch
addList = []
address = {'name':'test3','organization':'test2','address1':'1235 test street','address2':'ste 1234','address3':'','city':'Oak Brook','state':'IL','postalCode':'60523','country':'US'}	
addList.append(address)
address = {'name':'test4','organization':'test2','address1':'1235 test street','address2':'ste 1234','address3':'','city':'Oak Brook','state':'IL','postalCode':'60523','country':'US'}	
addList.append(address)
c2m.addJob("3","5",po,ad,addList)

print(c2m.runAll().text)

#To start a second batch initiate class again
#c2m = c2mAPIBatch.c2mAPIBatch("username","password","0")#change to 1 for production
#c2m.setFileName("myFileName","test.pdf") #set the name ane file path for batch
