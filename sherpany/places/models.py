from __future__ import unicode_literals

from django.db import models
from django.conf import settings

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

#
# Model that represents a given point in the database
#
class Place(models.Model):
    """ Model to support the database version of the address point """
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    address = models.CharField(max_length=250)

    def __str__(self):
        return self.address

    def __eq__(self, other):
        if (self.latitude == other.latitude and self.longitude == other.longitude):
            return True
        
        return False


# 
# Class to represent the Fusion table in google, it has the basic operations
#
class FusionPlace():

	#
	# Internal method that handles the communication with Google Services using the credentials from the file
	# that is placed at the home folder. It handles the Oauth2 authentication and the request token generation.
	#
	def _getService(self):
		scopes = ['https://www.googleapis.com/auth/fusiontables']
		credentials = ServiceAccountCredentials.from_json_keyfile_name(settings.GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_JSON, scopes=scopes)
		http = credentials.authorize(httplib2.Http())
		service = build("fusiontables", "v2", http=http)
		return service

	#
	# Inserts a new addres into the Fusion Table indicated in the settings.py files
	#
	def addPlace(self, place):
		query = self._getService().query()
		template_sql = "INSERT INTO {tableName} (id, latitude, longitude, address) VALUES ({id}, {latitude}, {longitude}, '{address}')"
		sql = template_sql.format(tableName=settings.GOOGLE_FUSIONTABLE_ID, address=place.address, latitude=place.latitude, longitude=place.longitude, id=place.pk)
		query.sql(sql=sql).execute()

	#
	# Checks if the given place is already in the fusion table.
	# @returns true if the place already exists.
	#
	def addressExists(self, place):
		query = self._getService().query()
		template_sql = "SELECT * FROM {tableName} WHERE latitude={latitude} and longitude={longitude}"
		sql = template_sql.format(tableName=settings.GOOGLE_FUSIONTABLE_ID, latitude=place.latitude, longitude=place.longitude)
		res = query.sqlGet(sql=sql).execute()
		return 'rows' in res

	#
	# remove all items on the fusion table.
	#
	def removeAll(self):
		query = self._getService().query()
		template_sql = """ DELETE FROM {tableName} """
		sql = template_sql.format(tableName=settings.GOOGLE_FUSIONTABLE_ID)
		query.sql(sql=sql).execute()

	#
	# Loads all the places in the fusion table.
	# @returns all the places in the google serviceZAZ.
	#
	def loadAll(self):
		query = self._getService().query()
		template_sql = "SELECT * FROM {tableName}"
		sql = template_sql.format(tableName=settings.GOOGLE_FUSIONTABLE_ID)
		res = query.sqlGet(sql=sql).execute()

		if ('rows' in res):
			return res['rows']
		else:
			return []
