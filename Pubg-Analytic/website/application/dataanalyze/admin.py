from django.contrib import admin
from .models import dataanalyzeAdmin
from tinymce.widgets import TinyMCE
from django.db import models
# Register your models here.

class dataanalyzeAdmins(admin.ModelAdmin):

	fieldsets = [
		("Title/date", {"fields": ["title", "published"]}),
		("Summary", {"fields": ["summary"]})
	]

	formfield_overrides = {
		models.TextField: {'widget': TinyMCE()}
	}


admin.site.register(dataanalyzeAdmin, dataanalyzeAdmins)