from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from snipt.snippet.models import Snippet
from django import forms

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username, password and email.
    """
    username = forms.RegexField(max_length=30, regex=r'^\w+$')
    password1 = forms.CharField(max_length=60, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=60, widget=forms.PasswordInput)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ("username",)
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))
    
    def clean_password2(self):
        try:
            password1 = self.cleaned_data["password1"]
        except KeyError:
            raise forms.ValidationError(_("The two password fields didn't match."))
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        fields = ('code','description','tags','lexer','public',)
