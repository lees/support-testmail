from django import forms
from .models import Issue

class CreateIssueForm(forms.Form):
    author_email = forms.EmailField(max_length=100)
    subject = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def save(self):
        post = Issue(**self.cleaned_data)
        post.save()
        return post
