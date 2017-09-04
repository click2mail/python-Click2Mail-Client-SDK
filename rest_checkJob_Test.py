from api import c2mAPI
print("Checking Job")
c2m = c2mAPI.c2mAPIRest("username","password","0")#change to 1 for production
c2m.jobId = "12345"
print(c2m.getJobStatus().text)