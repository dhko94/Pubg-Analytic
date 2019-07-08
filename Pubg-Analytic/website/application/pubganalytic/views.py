from django.shortcuts import render, redirect
from .models import pubganalyticData
from django.contrib import messages
from .forms import pubganalyticForm

import json
from .classFile import pubgData

def single_slug(request, single_slug):

	for p in pubganalyticData.objects.all():
		if single_slug == str(p.requestID):

			classData = pubgData(p.pubg_name)

			pieData = json.dumps(classData._getPIE(classData.playerDF))
			barData = json.dumps(classData._getBAR(classData.playerDF))
			scatterData = json.dumps(classData._getSCATTER(classData.playerDF))
			lineData = json.dumps(classData._getLINE(classData.playerDF))
			ganttData = json.dumps(classData._getGANTT(classData.playerDF))
			snipeData = classData._getSNIPE(classData.playerDF)

			return render(request = request,
						  template_name = "pubganalyticDetail.html",
						  context = 
						  {
						  	"data": 
						  		{
						  			"name": classData.name,
						  			"pie": pieData,
						  			"bar": barData,
						  			"scatter": scatterData,
						  			"line": lineData,
						  			"gantt": ganttData,
						  			"snipe": snipeData
						  		}
						  }
			)

	return HttpResponse(f"{single_slug} does not correspond to anything.")


def pubganalyticHome(request):
	contents = []
	for c in pubganalyticData.objects.all():
		if c.requester == request.user.username: contents.append(c)

	return render(request=request,
				  template_name="pubganalyticHome.html",
				  context={"contents":contents})


def pubganalyticAdd(request):
    if request.method == "POST":
        form = pubganalyticForm(request.POST, initial={'requester': request.user.username})
        if form.is_valid():
        	data = form.save()
        	messages.success(request, f"New request made : {data.requester}")

        	return redirect("pubganalytic:single_slug", data.requestID)

        else:
        	for msg in form.error_messages:
        		messages.error(request, f"{msg} : {form.error_messages[msg]}")

    form = pubganalyticForm(initial={'requester': request.user.username})
        
    return render(request = request,
				  template_name = "pubganalyticAdd.html",
				  context = {"form":form})