from django import forms
from .models import pubganalyticData
import random

class pubganalyticForm(forms.ModelForm):

	class Meta:
		model = pubganalyticData
		fields = ['requested', 'requester', 'pubg_name']
		widgets = {'requester': forms.HiddenInput()}


	def save(self, commit=True):

		game = super(pubganalyticForm, self).save(commit=False)
		if commit:
			game.save()

		return game