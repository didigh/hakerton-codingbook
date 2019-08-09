from django import forms
from .models import CodeShare, CodeAsk, ShareComment, ShareRe, AskComment, AskRe

class ShareNew(forms.ModelForm):
    class Meta:
        model = CodeShare
        fields = ['title','image','body','codes','subject','university','score']

class AskNew(forms.ModelForm):
    class Meta:
        model = CodeAsk
        fields = ['title','image','body','codes','subject']

class ShareCommentForm(forms.ModelForm):
    class Meta:
        model = ShareComment
        fields=['contents']

class ShareReForm(forms.ModelForm):
    class Meta:
        model = ShareRe
        fields=['contents']

class AskCommentForm(forms.ModelForm):
    class Meta:
        model = AskComment
        fields=['contents']

class AskReForm(forms.ModelForm):
    class Meta:
        model = AskRe
        fields=['contents']