from django import forms

class BookSearchForm(forms.Form):
    query = forms.CharField(required=True, max_length=255)

