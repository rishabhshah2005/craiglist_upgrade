from django.shortcuts import render
from bs4 import BeautifulSoup
import requests, re
from urllib.parse import quote_plus
from . import models

BASE_URL = 'https://ahmedabad.craigslist.org/search/sss?query={}'

BASE_IMAGE = 'https://images.craigslist.org/{}_300x300.jpg'
# Create your views here.


def home(request):
    return render(request, 'base.html')


def search_new(request):
    input_search = request.POST.get('search')
    models.Search.objects.create(search=input_search)
    fin_url = BASE_URL.format(quote_plus(input_search))
    response = requests.get(fin_url)
    data = response.text
    sp = BeautifulSoup(data, features='html.parser')
    listings = sp.find_all('li', {'class': 'result-row'})
    final_posts = []

    for posts in listings:
        title = posts.find(class_='result-title').text
        url = posts.find('a').get('href')

        if posts.find(class_='result-price'):
            price = posts.find(class_='result-price').text
        else:
            price = 'N/A'

        final_posts.append((title, url, price))

    frontend = {
        'search': input_search,
        'final_posts': final_posts,
        }
    return render(request, 'my_2nd_app/search.html', frontend)
