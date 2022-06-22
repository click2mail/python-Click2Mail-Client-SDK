from api import c2mAPI
print("REST IS RUNNING")
c2m = c2mAPI.c2mAPIRest("username",password","0")#change to 1 for production
#Adding 1st address
address = {'First_name':'Test','Last_name':'Smith','organization':'test org','Address1':'12345 test ave','Address2':'Apt 3','City':'Oak Brook','State':'IL','Zip':'60523','Country_non-US':''}
c2m.addressList.append(address)
#Adding 2nd address
address = {'First_name':'Test2','Last_name':'Smith','organization':'test org','Address1':'12345 test ave','Address2':'Apt 3','City':'Oak Brook','State':'IL','Zip':'60523','Country_non-US':''}
c2m.addressList.append(address)
print(c2m.runAllFromJobTemplate("test.pdf","2","testJobTemplate").text)
print('DOCID: ' +c2m.documentId)
print('AddressListId: ' +c2m.addressListId)
print('JobId: ' +c2m.jobId)
