from django.db import models
from datetime import datetime
import uuid


class pubganalyticData(models.Model):

	requester = models.CharField(max_length = 100, null = False)
	pubg_name = models.CharField(max_length = 100, null = False, default = "")
	requested = models.DateTimeField("Date requested", default=datetime.now())

	requestID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


	def __str__(self):
		return self.pubg_name + " By " + self.requester 