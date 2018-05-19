from django import forms
from .models import FarmerDetail, FarmDetail, ScheduleDetail

class FarmerForm(forms.ModelForm):

    class Meta:
        model = FarmerDetail
        fields = '__all__'

class FarmForm(forms.ModelForm):

    class Meta:
        model = FarmDetail
        fields = '__all__'

class ScheduleForm(forms.ModelForm):

    class Meta:
        model = ScheduleDetail
        fields = '__all__'