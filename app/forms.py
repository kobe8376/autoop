from django import forms

class teacher_form(forms.Form):
    Tversion = forms.CharField(max_length=10)
    Tdate = forms.DateField()
    Tfile = forms.FileField()   
class student_form(forms.Form):
    Sversion = forms.CharField(max_length=10)
    Sdate = forms.DateField()
    Sfile = forms.FileField()  
