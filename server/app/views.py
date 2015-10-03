from .models import user
from django.core.exceptions import ObjectDoesNotExist
from json import *
from django.http import HttpResponse
from gcmHandler import gcmHandler								# My own GCM Handler
from django.views.decorators.csrf import *

class Alarm():
	def __init__(self,request,Type):
		try:
			self.data = loads(request.body)						# load Json data into object
			self.type = Type									# get whether the message has picture/video/text...
		except:
			self.data = self.type = None 						# Something went wrong...

	def TxtAlarm(self):
		response = None
		try:
			sender = self.data['from']							# sender phone no.
			receiver = self.data['to']				  			# receiver phone no.
			try:
				receiver = user.objects.get(phNum = int(receiver))	# check if receiver phone no. exists in DB.
			except:
				response = 'receiver absent'				# return that it doesn't exist
				return response
			try:
				sender = user.objects.get(phNum = int(sender))	# check if sender phone no. exists in DB.
			except:
				response = 'sender absent'					# return that it doesn't exist
				return response
			response = self.SendTxtAlarm()						# send the data
		except:
			response = 	'invalid request'
			return -1 									# some data missing => invalid request
		return response											# response from SendTxt()

	def SendTxtAlarm(self):
		sender = self.data['from']								# sender
		receiver = self.data['to']								# receiver
		recipientId = user.objects.get(phNum = int(receiver)).gcmId
		data = {
			"time":self.data['time'],
			"msg":self.data['msg'],
			"to":receiver,
			"from":sender,
			"id":self.data['id'],
			"nick":user.objects.get(phNum = int(sender)).nick,
			"hide":self.data['hide']
		}
		gcm = gcmHandler(recipientId,data)
		response = gcm.SendGCMtxt()
		'''if response == -5:

		if response == -1:
			#user.objects.filter(phNum = int(receiver)).delete()				# remove from DB.
			response = "receiver absent"
			return response
		if response == 0:
			return "alarm setting failed"'''
		return response

############################# Sender's part over ##############################################

class Feedback():
	def __init__(self,request):
		try:
			self.data = loads(request.body)						# load Json data into object
		except:
			self.data = self.type = None 						# Something went wrong...

	def TxtFeedback(self):										# get a text-feedback
		response = None
		try:
			sender = self.data['sender']						# sender phone no.
			receiver = self.data['receiver']		  			# receiver phone no.
			try:
				receiver = user.objects.get(phNum = receiver)	# check if receiver phone no. exists in DB.
			except ObjectDoesNotExist:
				response = {"result":'receiver absent'}			# return that it doesn't exist
				return response
			try:
				sender = user.objects.get(phNum = sender)		# check if sender phone no. exists in DB.
			except ObjectDoesNotExist:
				response = {"result":'receiver absent'}			# return that it doesn't exist
				return response
			response = self.SendFeedback()						# send the data
		except:
			response = {'result':'invalid request'}
			return response 									# some data missing => invalid request
		return response											# response from SendFeedback()

	def SendFeedback(self):
		Fsender = self.data['sender']
		Freceiver = self.data['receiver']
		del self.data['receiver']
		# send this self.data 

######################### Feedback  part over #######################################

class User():
	def __init__(self,request):
		try:
			User_data = loads(request.body)
			self.gcmId = User_data['gcm']
			self.phNo = int(User_data['pno'])
			self.nick = User_data['nick']
		except:
			self.gcmId = self.phNo = self.nick = None

####################### New User registration part over ###############################

######################## Main part below which shall call the above appropriate functions ############
@csrf_exempt
def NewUser(request):
	data = None 										# data to send
	newUser = User(request)								# first time registration
	if newUser.gcmId == None:							# the data is invalid...
		return HttpResponse('invalid data')
	try:   												# user already exists
		p = user.objects.filter(phNum = newUser.phno, gcmId = newUser.gcmId)
		p.gcmId = newUser.gcmId
		p.save()
		return HttpResponse('success')						# success.
	except:													# new user. 
		user(phNum = newUser.phNo,gcmId = newUser.gcmId,nick = newUser.nick).save()# store phone number and gcmId in DB.
		return HttpResponse('success')						# success. 

@csrf_exempt
def NewTxtAlarm(request):									# sending a new message
	data = None   										# Initial data is none
	new_alarm = Alarm(request,'text')					# Create a Python NewAlarm object
	if new_alarm.type == None:							# Object creation failed...
		return HttpResponse('invalid data')
	response = new_alarm.TxtAlarm()						# Handle a text alarm
	if response == -2:
		return HttpResponse(status = 404)
	elif response == -1:
		return HttpResponse(status = 300)
	return HttpResponse(response)

def NewImgAlarm(request):
	pass

def feedback(request):									# Send a feedback
	feedbackData = Feedback(request)					# Create a Python Feedback object
	if feedbackData.type == None:							# Object creation failed...
		return HttpResponse('invalid feedback')
	elif feedbackData.type == 'text':					# Handle a text only feedback
		response = feedbackData.TxtFeedback()
		return HttpResponse(response)
	elif feedbackData.type == 'picture':
		pass
		# todo
	elif feedbackData.type == 'audio':
		pass
		# todo
	elif feedbackData.type == 'video':
		pass
		# todo
	return HttpResponse('invalid data')					# If none of the above...

