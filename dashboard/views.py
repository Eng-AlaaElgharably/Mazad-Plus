from django.shortcuts import render, redirect
from datetime import datetime, timedelta, timezone
from dashboard.models import Auction, Bid
from .forms import NewUserForm, UserUpdateForm, ProfileUpdateForm, AddAuctionForm, AddBidForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
import json
from django.db.models import Max

# Create your views here.

def updateauctions():
    auctions = Auction.objects.filter(status="Live")
    for auction in auctions:
        bids = Bid.objects.filter(auction_id = auction).count()
        auction.timeend = auction.timestart + timedelta(hours=auction.time, minutes= 2*bids)
        auction.save()
        if auction.timeend <= datetime.now(timezone.utc):
            auction.status = "Expired"
            auction.save()

def home(request):
    updateauctions()
    auctions = Auction.objects.all()
    return render(request, "home.html", {'auctions': auctions})

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your registration has been completed successfully.")
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        return render(request, "registration/register.html", {"form":form})
    form = NewUserForm()
    return render(request, "registration/register.html", {"form":form})

#@login_required
def edit(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('edit')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'edit.html', context)

def addauction(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == 'POST':
        form = AddAuctionForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.creator = request.user
            form.save()
            messages.success(request, 'Your auction has been added.')
            return redirect('addauction')
        messages.error(request, 'Error in data.')
        return render(request, 'addauction.html', {'form': form})    
    form = AddAuctionForm()
    return render(request, 'addauction.html', {'form': form})

def auctionpage(request, pk):
    auction = Auction.objects.get(pk = pk)
    bids = Bid.objects.filter(auction_id = auction).last()
    if bids == None:
        bids = Bid(auction_id = auction, user_id = request.user, auction_balance = auction.startprice)    
    if request.method == "POST":
        form = AddBidForm(request.POST)
        if form.is_valid():
            if form.instance.auction_balance > auction.startprice  and form.instance.auction_balance > bids.auction_balance:
                form.instance.user_id = request.user
                form.instance.auction_id = auction
                auction.winner = form.instance.user_id
                auction.save()
                form.save()
                updateauctions()
                auction = Auction.objects.get(pk = pk)
                bids = Bid.objects.filter(auction_id = auction).last()
                messages.success(request, "Your bid has been completed successfully.")
                return render(request, 'auctionpage.html', {'auction': auction, 'form': form, 'bids': bids})
            messages.error(request, "Your bid must be greater than start price and last bid.")
        return render(request, 'auctionpage.html', {'auction': auction, 'form': form, 'bids': bids})
    form = AddBidForm()
    return render(request, 'auctionpage.html', {'auction': auction, 'form': form, 'bids': bids})

def report(request):
    if request.user.is_staff == False:
        return redirect(home)
    auctions = Auction.objects.all()
    return render(request, "report.html", {'auctions': auctions})
