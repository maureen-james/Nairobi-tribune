from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
import datetime as dt
from .models import Article
from django.core.exceptions import ObjectDoesNotExist
from .forms import NewsLetterForm
from newsapi import NewsApiClient 

# Create your views here.
def home(request):
    newsapi = NewsApiClient(api_key='90ebc1f08f0c4367b67eeeb0164a5e7b')
    topnews = newsapi.get_top_headlines('cnn')   # source=ndtv, bbc-news, cnn,techcrunch,foxnews.

    latest = topnews['articles']
    print(topnews)
    title = []
    desc = []
    url = []
    author = []
    date = []

    for i in range(len(latest)):
        news = latest[i]

        title.append(news['title'])
        desc.append(news['description'])
        url.append(news['url'])
        author.append(news['author'])
        date.append(news['publishedAt'])

    all_news = zip(title, desc, url, author, date)

    context = {
        'all_news': all_news
    }

    return render(request, "all-news/index.html", context)


def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()

  

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            print('valid')
    else:
        form = NewsLetterForm()
    return render(request, 'all-news/todays-news.html', {"date": date,"news":news,"letterForm":form})



def past_days_news(request, past_date):
    try:
        # Converts data from the string Url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()
    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_today)

    news = Article.days_news(date)
    return render(request, 'all-news/past-news.html',{"date": date,"news":news})



def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})  

def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"all-news/article.html", {"article":article}) 
             