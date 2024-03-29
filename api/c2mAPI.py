# Hello world python program
import requests
import xml.etree.ElementTree
import uuid
from datetime import datetime
from requests_toolbelt.multipart.encoder import MultipartEncoder

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
		return tostring(root,encoding='utf8')
	def addJob(self,startPage,endPage, printOptions, returnAddress, recipients):
		job = {"startPage":startPage,"endPage":endPage,"printOptions":printOptions,"returnAddress":returnAddress,"recipients":recipients}
		self.jobs.append(job)
	def getBatchUrl(self) :
		if self.mode == "0":
			return "https://stage-batch.click2mail.com"
		else:
			return "https://batch.click2mail.com"
	def createBatch(self) :
		print ("Creating Batch")
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
			print("Batch ID: ", self.batchID)
		return r
	def sendXML(self,xmlStr) :
		print ("Sending XML")
		global batchID 
		headers = {'user-agent': 'my-app/0.0.1','content-type':'application/xml'}
		r = requests.put(self.getBatchUrl() + '/v1/batches/'+ self.batchID, auth=(self.username, self.password),headers=headers,data=xmlStr)
		print("HTTP status: ", r.status_code)
		#print(r.text)
		return r
	def sendPDF(self,file):
		print ("Sending PDF")
		global batchID 
		headers = {'user-agent': 'my-app/0.0.1','content-type':'application/pdf'}
		#str = open('test2.xml', 'r').read()
		payload = open(file, 'rb')
		r = requests.put(self.getBatchUrl() + '/v1/batches/'+ self.batchID, auth=(self.username, self.password),headers=headers,data=payload)
		print("HTTP status: ", r.status_code)
		#print(r.text)
		return r
	def submitBatch(self):
		print ("Submitting batch")
		global batchID 
		headers = {'user-agent': 'my-app/0.0.1'}
		r = requests.post(self.getBatchUrl() + '/v1/batches/'+ self.batchID, auth=(self.username, self.password),headers=headers)
		print("HTTP status: ", r.status_code)
		print(r.text)
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

	def runAllDoubleSided(self,fileNameSide1,fileNameSide2,documentName,documentClass,documentFormat,addressMappingId,printOptions):
		utcNow = datetime.utcnow()
		self.pringOptions = printOptions
		self.addressMappingId = addressMappingId;

		print("uploading side1 image " + fileNameSide1)
		result = self.createDocument_v2(fileNameSide1, 'side1_'+str(utcNow), documentClass,documentFormat)
		if result.status_code > 299 :
			return result
		print(self.documentId)
		document1Id = self.documentId

		print("uploading side2 image " + fileNameSide2)
		result = self.createDocument_v2(fileNameSide2, 'side2_'+str(utcNow), documentClass,documentFormat)
		if result.status_code > 299 :
			return result
		print(self.documentId)
		document2Id = self.documentId

		print('merging sides to create document ' + documentName)
		result = self.mergeDocuments(document1Id,document2Id,documentName + '_' + str(utcNow))
		if result.status_code > 299 :
			return result
		
		print('Document merged ' + self.documentId)
		result = self.uploadAddressList()
		if result.status_code > 299 :
			return result

		print("upload address: " + result.text)
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

	def runAllFromJobTemplate(self,fileName,addressMappingId,templateName) :
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

		result = self.createJobFromTemplate(templateName)
		if result.status_code > 299 :
			return result
		result = self.updateJob()
		if result.status_code > 299 :
			return result
		result =self.submitJob()
		if result.status_code > 299 :
			return result
		return self.getJobStatus()

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

	def createDocument_v2(self,fileName,documentName,documentClass,documentFormat):
		mp_encoder = MultipartEncoder(
			fields={
				'documentFormat': documentFormat,
				'documentName': documentName,
				'documentClass': documentClass,
				'file': (fileName, open(fileName,'rb'), 'image/png')
			}
		)
		headers = {'user-agent': 'my-app/0.0.1','Content-Type': mp_encoder.content_type}
		r = requests.post(self.getRestUrl() + '/molpro/documents/',auth=(self.username, self.password),headers=headers,data=mp_encoder)
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


	def createDocument(self,fileName):
		mp_encoder = MultipartEncoder(
    			fields={
                		'documentFormat': 'PDF',
                		'documentName': 'sample Letter',
                		'documentClass': 'Letter 8.5 x 11',
				'file': (fileName, open(fileName,'rb'), 'application/pdf')
    			}
		)
		headers = {'user-agent': 'my-app/0.0.1','Content-Type': mp_encoder.content_type}
		r = requests.post(self.getRestUrl() + '/molpro/documents/',auth=(self.username, self.password),headers=headers,data=mp_encoder)
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

	def createDocumentMergeList(self,document1Id,document2Id):
		from xml.etree.ElementTree import Element, SubElement, tostring
		
		root = Element('documentList')
		child = SubElement(root, "documentId")
		child.text = document1Id
		child = SubElement(root, "documentId")
		child.text = document2Id
		return tostring(root)

	def mergeDocuments(self,document1Id,document2Id,documentName):
		xmlstr = self.createDocumentMergeList(document1Id,document2Id)
		print(xmlstr)
		headers = {'user-agent': 'my-app/0.0.1','Content-Type':'application/xml'}
		r = requests.post(self.getRestUrl() + '/molpro/documents/merge?documentName='+documentName,auth=(self.username, self.password),data=xmlstr,headers=headers)
		if r.status_code > 299 :
			return r
		#print(r.status_code)
		e = xml.etree.ElementTree.fromstring(r.text)
		for elem in e.iter(tag='id'):
			self.documentId= elem.text
			#print(self.documentId)
		return  r

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

	def updateJob(self):
		headers = {'user-agent': 'my-app/0.0.1'}
		values = {'documentId':self.documentId,'addressId':self.addressListId}
		r = requests.post(self.getRestUrl() + '/molpro/jobs/' + self.jobId + '/update',auth=(self.username, self.password),data=values)
		if r.status_code > 299 :
			return r
		#print(r.status_code)
		#print(r.text)
		#e = xml.etree.ElementTree.fromstring(r.text)
		#for elem in e.iter(tag='id'):
			#global jobId
			#self.jobId = elem.text
			#print(self.jobId)
		return r

	def createJobFromTemplate(self,templateName):
		headers = {'user-agent': 'my-app/0.0.1'}
		values = {'templateName': templateName}
		r = requests.post(self.getRestUrl() + '/molpro/jobs/jobTemplate',auth=(self.username, self.password),data=values)
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
