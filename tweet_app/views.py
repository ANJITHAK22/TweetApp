from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Tweet
from .forms import TweetForm,UserRegistrationForm
# Create your views here.
def tweet_list(req):
    tweets= Tweet.objects.all().order_by('-created_at')
    return render(req,'tweet_list.html',{'tweets':tweets})

def tweet_create(req):
    if req.method=="POST":
        form= TweetForm(req.POST,req.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)           
            tweet.user= req.user 
            tweet.save() # save data in database
            return redirect('tweet_list')
    else:      
        form=TweetForm()
    return render(req,'tweet_form.html',{'form':form})


def tweet_edit(req,tweet_id):
    tweet= get_object_or_404(Tweet,pk=tweet_id,user=req.user)
    if req.method=="POST":
        form= TweetForm(req.POST,req.FILES, instance=tweet)
        if form.is_valid():
            tweet=form.save(commit=True)           
            tweet.user= req.user 
            tweet.save() # save data in database
            return redirect('tweet_list')
    else:
        form=TweetForm(instance=tweet)
    return render(req,'tweet_form.html',{'form':form})

def tweet_delete(req,tweet_id):
    tweet= get_object_or_404(Tweet,pk=tweet_id,user=req.user)
    if req.method=="POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(req,'tweet_confirm_delete.html',{'tweet':tweet})


def register(req):
    if req.method=="POST":
        form=UserRegistrationForm(req.POST)
        if form.is_valid():
            user= form.save(commit=True)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(req,user)
            return redirect('tweet_list')
    else:
        form=UserRegistrationForm()
    return render(req,'registration/register.html',{'form':form})