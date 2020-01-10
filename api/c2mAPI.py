# Hello world python program
import requests
import xml.etree.ElementTree
import uuid
class c2mAPIBatch(object):
	def __init__(self,username,password,mode):
		self.batchID = "0"
		self.jobId = "0"
		self.addressListId = "0"
		self.documentID = "0"
		self.mode = mode
		self.username = username
		self.password = password
		self.jobs = []
	def getBatchStatus(self):
		global batchID 
		headers = {'user-agent': 'my-app/0.0.1'}
		r = requests.get(self.getBatchUrl() + '/v1/batches/'+ self.batchID, auth=(self.username, self.password),headers=headers)
		return r
	def setFileName(self,fileName,filePath):
		self.fileName = fileName
		self.filePath = filePath
	def runAll(self) :
		result = self.createBatch()
		if result.status_code > 299 :
			return result
		result =self.sendPDF(self.filePath)
		if result.status_code > 299 :
			return result
		str = self.createBatchXML()#.decode(encoding="utf-8")
		result = self.sendXML(str)
		if result.status_code > 299 :
			return result
		result = self.submitBatch()
		if result.status_code > 299 :
			return result
		return self.getBatchStatus()
	def createBatchXML(self):
		from xml.etree.ElementTree import Element, SubElement, tostring
		root = Element('batch')
		username = SubElement(root, "username")
		username.text = self.username
		password = SubElement(root,"password")
		password.text = self.password
		filename = SubElement(root,"filename")
		filename.text = self.fileName
		appSignature = SubElement(root,"appSignature")
		appSignature.text = "Python SDK Batch"
		for myJob in self.jobs:
			job = SubElement(root,"job")
			startingpage = SubElement(job,"startingPage")
			startingpage.text = myJob['startPage']
			endpage = SubElement(job,"endingPage")
			endpage.text = myJob['endPage']
			printproductionoptions = SubElement(job,"printProductionOptions")
			elem = SubElement(printproductionoptions,"documentClass")
			elem.text = myJob['printOptions'].documentClass
			elem = SubElement(printproductionoptions,"layout")
			elem.text = myJob['printOptions'].layout
			elem = SubElement(printproductionoptions,"productionTime")
			elem.text = myJob['printOptions'].productionTime
			elem = SubElement(printproductionoptions,"envelope")
			elem.text = myJob['printOptions'].envelope
			elem = SubElement(printproductionoptions,"color")
			elem.text = myJob['printOptions'].color
			elem = SubElement(printproductionoptions,"paperType")
			elem.text = myJob['printOptions'].paperType
			elem = SubElement(printproductionoptions,"printOption")
			elem.text = myJob['printOptions'].printOption
			elem = SubElement(printproductionoptions,"mailClass")
			elem.text = myJob['printOptions'].mailClass
			recipients = SubElement(job,"recipients")
			for x in myJob['recipients']:
				elem = SubElement(recipients,"address")
				for key,value in x.items():
					newElem = SubElement(elem,key)
					newElem.text = value
		return tostring(root)
	def addJob(self,startPage,endPage, printOptions, returnAddress, recipients):
		job = {"startPage":startPage,"endPage":endPage,"printOptions":printOptions,"returnAddress":returnAddress,"recipients":recipients}
		self.jobs.append(job)
	def getBatchUrl(self) :
		if self.mode == "0":
			return "https://stage-batch.click2mail.com"
		else:
			return "https://batch.click2mail.com"
	def createBatch(self) :
		url = self.getBatchUrl() + '/v1/batches'
		r = requests.post(url, auth=(self.username, self.password))
		if r.status_code > 299:
			return r
		#print(r.text)
		#print(url)
		e = xml.etree.ElementTree.fromstring(r.text)
		for elem in e.iter(tag='id'):
			#global batchID 
			self.batchID= elem.text
			#print(self.batchID)
		return r
	def sendXML(self,xmlStr) :
		global batchID 
		headers = {'user-agent': 'my-app/0.0.1','content-type':'application/xml'}
		r = requests.put(self.getBatchUrl() + '/v1/batches/'+ self.batchID, auth=(self.username, self.password),headers=headers,data=xmlStr)
	    #print(r.status_code)
		#print(r.text)
		return r
	def sendPDF(self,file):
		global batchID 
		headers = {'user-agent': 'my-app/0.0.1','content-type':'application/pdf'}
		#str = open('test2.xml', 'r').read()
		files = {"file":open(file, 'rb')}
		r = requests.put(self.getBatchUrl() + '/v1/batches/'+ self.batchID, auth=(self.username, self.password),headers=headers,files=files)
		#print(r.status_code)
		#print(r.text)
		return r
	def submitBatch(self):
		global batchID 
		headers = {'user-agent': 'my-app/0.0.1'}
		r = requests.post(self.getBatchUrl() + '/v1/batches/'+ self.batchID, auth=(self.username, self.password),headers=headers)
		#print(r.status_code)
		#print(r.text)
		return r
class printOptions(object):
	
	def __init__(self,documentClass,productionTime,layout,color,paperType,printOption,mailClass,envelope):
		self.documentClass =documentClass
		self.productionTime = productionTime
		self.layout =layout
		self.color =color
		self.paperType=paperType
		self.printOption=printOption
		self.mailClass=mailClass
		self.envelope=envelope
class returnAddress(object):
	def __init__(self,name,organization,address1,address2,city,state,postalCode):
		self.name = name
		self.organization = organization
		self.address1 = address1
		self.address2 = address2
		self.city = city
		self.state = state
		self.postalCode = postalCode
class c2mAPIRest(object) :
	def __init__(self,username,password,mode):
		self.batchID = "0"
		self.jobId = "0"
		self.addressListId = "0"
		self.documentId = "0"
		self.mode = mode
		self.username = username
		self.password = password
		self.addressList = []
		self.addressMappingId = "0"
		
	def runAll(self,fileName,addressMappingId,printOptions) :
		self.pringOptions = printOptions
		self.addressMappingId = addressMappingId;
		result = self.createDocument(fileName)
		if result.status_code > 299 :
			return result
		#print(self.documentId)
		result = self.uploadAddressList()
		if result.status_code > 299 :
			return result
		e = xml.etree.ElementTree.fromstring(result.text)
		for elem in e.iter(tag='status'):
			self.addressStatus =  elem.text
		while self.addressStatus != "3":
			result = self.getAddressStatus()
			if result.status_code > 299 :
				return result
			e = xml.etree.ElementTree.fromstring(result.text)
			for elem in e.iter(tag='status'):
				self.addressStatus =  elem.text
			print("Waiting On AddresList")
		
		result = self.createJob(printOptions)
		if result.status_code > 299 :
			return result
		result =self.submitJob()
		if result.status_code > 299 :
			return result
		return self.getJobStatus()
	def getRestUrl(self) :
		if self.mode == "0":
			return "https://stage-rest.click2mail.com"
		else:
			return "https://rest.click2mail.com"
	def createDocument(self,fileName):
		headers = {'user-agent': 'my-app/0.0.1'}
		files = {'file': ('file.pdf', open(fileName,'r+b'), 'application/pdf'),
        	'documentFormat': 'PDF',
        	'documentName': 'sample Letter',
        	'documentClass': 'Letter 8.5 x 11'
    	}
		r = requests.post(self.getRestUrl() + '/molpro/documents/',auth=(self.username, self.password),headers=headers,files=files)
		if r.status_code > 299 :
			return r
		#print(r.status_code)
		#print(r.text)
		e = xml.etree.ElementTree.fromstring(r.text)
		for elem in e.iter(tag='id'):
			#global documentID
			self.documentId = elem.text
			#print(documentID)
		return r
	def createAddressList(self,addressMappingId):
		from xml.etree.ElementTree import Element, SubElement, tostring

		root = Element('addressList')
		child = SubElement(root, "addressListName")
		child.text = str(uuid.uuid4())
		child2 = SubElement(root,"addressMappingId")
		child2.text = addressMappingId
		addresses = SubElement(root,"addresses")
		for x in self.addressList:
			elem = SubElement(addresses,"address")
			for key,value in x.items():
				newElem = SubElement(elem,key)
				newElem.text = value
		return tostring(root)
	def uploadAddressList(self):
		xmlstr = self.createAddressList(self.addressMappingId)
		print(xmlstr)
		headers = {'user-agent': 'my-app/0.0.1','Content-Type':'application/xml'}
		r = requests.post(self.getRestUrl() + '/molpro/addressLists/',auth=(self.username, self.password),data=xmlstr, headers=headers)
		if r.status_code > 299 :
			return r
		#print(r.status_code)
		e = xml.etree.ElementTree.fromstring(r.text)
		for elem in e.iter(tag='id'):
			self.addressListId= elem.text
			#print(self.addressListId)
		return	r
	def getAddressListStatus(self):
		headers = {'user-agent': 'my-app/0.0.1','content-type':'application/xml'}
		r = requests.get(self.getRestUrl() + '/molpro/addressLists/' + self.addressListId,auth=(self.username, self.password),data=xmlstr)
		#print(r.status_code)
		#e = xml.etree.ElementTree.fromstring(r.text)
		return	r
	def createJob(self,printOptions):
		headers = {'user-agent': 'my-app/0.0.1'}
		values = {'documentClass': printOptions.documentClass,'layout':printOptions.layout,'productionTime':printOptions.productionTime,'envelope':printOptions.envelope,'color':printOptions.color,'paperType':printOptions.paperType,'printOption': printOptions.printOption,'documentId':self.documentId,'addressId':self.addressListId}
		r = requests.post(self.getRestUrl() + '/molpro/jobs/',auth=(self.username, self.password),data=values)
		if r.status_code > 299 :
			return r
		#print(r.status_code)
		#print(r.text)
		e = xml.etree.ElementTree.fromstring(r.text)
		for elem in e.iter(tag='id'):
			#global jobId 
			self.jobId = elem.text
			#print(self.jobId)
		return r	
	def submitJob(self):
		#global jobId
		headers = {'user-agent': 'my-app/0.0.1'}
		values = {'billingType': 'User Credit'}
		r = requests.post(self.getRestUrl() + '/molpro/jobs/' + self.jobId + '/submit',auth=(self.username, self.password),data=values)
		if r.status_code > 299 :
			return r
		#print(r.status_code)
		#print(r.text)
		e = xml.etree.ElementTree.fromstring(r.text)
		return r
	def getJobStatus(self):
		headers = {'user-agent': 'my-app/0.0.1'}
		r = requests.get(self.getRestUrl() + '/molpro/jobs/' + self.jobId ,auth=(self.username, self.password))
		#print(r.status_code)
		#print(r.text)
		e = xml.etree.ElementTree.fromstring(r.text)
		return r
