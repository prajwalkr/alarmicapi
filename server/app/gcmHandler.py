from gcm import GCM
class gcmHandler():
	############## Server side GCM configurations and imports #######
	global api_key
	api_key = 'AIzaSyAK8T3njedTjLJ50jmMGGcNGZo5aqEb-i8'
	########## finished importing prerequisites for GCM ############

	def __init__(self,gcmId,data):
		self.gcmId = gcmId
		self.data = data

	def SendGCMtxt(self):
		gcm = GCM(api_key)
		response = gcm.json_request(registration_ids = [self.gcmId],data = self.data)
		'''try:
			if 'errors' in response:
			    for error, reg_ids in response['errors'].items():	
			        # Check for errors and act accordingly
			        if error in ['NotRegistered', 'InvalidRegistration']:
			            return -1
				return 0
			return 1
		except:
			return -5'''
		return 5