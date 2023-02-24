from django import forms

class FileUploadForm(forms.Form):
    file1 = forms.FileField(label="Teacher's data csv")
    file2 = forms.FileField(label='Zip file of profile images')
