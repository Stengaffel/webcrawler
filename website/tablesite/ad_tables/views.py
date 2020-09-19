from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse

import sqlite3

def index(request):
    return HttpResponse("Hello, world. You're at the ad_tables index.")

def createTable(request, table_name):

    header = ['Date', 'Title', 'Company', 'Location', 'Link']

    rows = [('2020-09-19', 'Title one', 'Company one', 'Location one', 'Link one'),
             ('2020-09-20', 'Title two', 'Company two', 'Location two', 'Link two')]

    # Connect to the database
    conn = sqlite3.connect('/home/william/Documents/webcrawler/ads.sqlite')

    c = conn.cursor()
    c.execute("SELECT * FROM indeed_ads")
    rows = [{'date': date, 'title': title, 'company': company,
        'location': location, 'link': link} for (date,title,company,location,link) in c]

    context = { 'header': header, 'rows': rows }

    return render(request, 'ad_tables/tables.html', context)




class TableView(ListView):

    def getElements():
        elems = [('2020-09-19', 'Title one', 'Company one', 'Location one', 'Link one'),
                 ('2020-09-20', 'Title two', 'Company two', 'Location two', 'Link two')]
        return render(request, 'ad_tables/', {'elems': elems})
