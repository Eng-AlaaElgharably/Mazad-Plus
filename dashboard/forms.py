from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from .models import Profile, Auction, Bid

class NewUserForm(UserCreationForm):    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'phone', 'address']

class AddAuctionForm(forms.ModelForm):
    title = forms.CharField(max_length=30, label="Title", widget=forms.TextInput(attrs={'placeholder': 'Enter the title of auction'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter the description of auction'}), label="Description")
    startprice = forms.IntegerField(label="Start Price", widget=forms.NumberInput(attrs={'placeholder': 'Enter the start price of auction in dollars', 'min':0}))
    image = forms.ImageField()
    time = forms.IntegerField(label="Time", widget=forms.NumberInput(attrs={'placeholder': 'Enter the time of auction in hours', 'min': 0, 'max': 240}))
    class Meta:
        model = Auction
        fields = ['title', 'description', 'startprice', 'image', 'time']

class AddBidForm(forms.ModelForm):
    class Meta:
        auction_balance = forms.IntegerField(label="Bid", widget=forms.NumberInput(attrs={'placeholder': 'Enter the price of your bid', 'min':0}))
        model = Bid
        fields = ['auction_balance']
