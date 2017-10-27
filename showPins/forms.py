from django import forms
from django.core.validators import EmailValidator, URLValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from showPins.models import (
    User,
    Photo,
    Like,
    Comment,
    Card,
)

#dziala

class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ['user']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class LoginForm(forms.Form):
    login = forms.CharField(label='Login')
    password = forms.CharField(label='Haslo', widget=forms.PasswordInput)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)


class LikeCommentForm(forms.Form):
    class Meta:
        model = Like, Comment
        fields = '__all__'


