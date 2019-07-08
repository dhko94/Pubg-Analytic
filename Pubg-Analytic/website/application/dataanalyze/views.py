from django.shortcuts import render, redirect
from .models import dataanalyzeAdmin
from django.contrib import messages

def dataanalyzeHome(request):
	contents = [c for c in dataanalyzeAdmin.objects.all()]

	return render(request=request,
				  template_name="dataanalyzeHome.html",
				  context={"contents":contents})