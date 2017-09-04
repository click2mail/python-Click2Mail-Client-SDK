from api import c2mAPI
c2m = c2mAPI.c2mAPIBatch("username","password","0")#change to 1 for production
c2m.batchId = 12345
print(c2m.getBatchStatus().text)