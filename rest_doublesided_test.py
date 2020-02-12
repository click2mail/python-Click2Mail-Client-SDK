from api import c2mAPI	
print("REST IS RUNNING")	
c2m = c2mAPI.c2mAPIRest("????????","????????","0")#change to 1 for production
#Adding 1st address
address = {'First_name':'Test','Last_name':'Smith','organization':'test org','Address1':'6070 California Circle','Address2':'Apt 3','City':'Rockville','State':'MD','Zip':'20852','Country_non-US':''}
c2m.addressList.append(address)
#Adding 2nd address
address = {'First_name':'Test2','Last_name':'Smith','organization':'test org','Address1':'6060 California Circle','Address2':'Apt 3','City':'Rockville','State':'MD','Zip':'20852','Country_non-US':''}
c2m.addressList.append(address)
#setting  Print Options
po = c2mAPI.printOptions('Postcard 5 x 8','Next Day','Double Sided Postcard','Full Color','White Matte with Gloss UV Finish','Printing both sides','First Class','')
print(c2m.runAllDoubleSided('tiger.png','aligator.png','wildlife','Postcard 5 x 8','PNG',"2",po).text)
print('DOCID: ' +c2m.documentId)
print('AddressListId: ' +c2m.addressListId)
print('JobId: ' +c2m.jobId)
