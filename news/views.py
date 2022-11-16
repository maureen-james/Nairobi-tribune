from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
import datetime as dt
# from .models import Article
from django.core.exceptions import ObjectDoesNotExist
from .forms import NewsLetterForm
# Create your views here.
def welcome(request):
    return HttpResponse('Welcome to the Nairobi Tribune')

def news_today(request):
    date = dt.date.today()
    # return render(request, 'all-news/today-news.html',{'date': date})
  

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            print('valid')
    else:
        form = NewsLetterForm()
    return render(request, 'all-news/today-news.html', {"date": date,"news":news,"letterForm":form})  