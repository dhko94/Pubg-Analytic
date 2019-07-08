from django.db import models
from datetime import datetime
from tinymce.widgets import TinyMCE


class dataanalyzeAdmin(models.Model):

	title = models.CharField(max_length=100, null=False)
	published = models.DateTimeField("Date published", default=datetime.now())
	summary = models.TextField(null=True)

	formfield_overrides = {
		models.TextField: {'widget': TinyMCE()}
	}

	class Meta:
		verbose_name_plural = "Data Analyze"

	def __str__(self):
		return self.title
