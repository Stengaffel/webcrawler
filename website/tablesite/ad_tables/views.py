from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse

import sqlite3

def index(request):
    return HttpResponse("Hello, world. You're at the ad_tables index.")

def createTable(request, table_name):

    header = {'date': 'Date', 'title': 'Title', 'company':'Company',
            'location': 'Location', 'link': 'Link'}

    # Connect to the database
    conn = sqlite3.connect('/home/william/Documents/webcrawler/ads.sqlite')

    c = conn.cursor()
    c.execute(f"SELECT * FROM '{table_name}_ads' ORDER BY date DESC")

    rows = [{'date': date, 'title': title, 'company': company,
        'location': location, 'link': link} for (date,title,company,location,link) in c]

    context = { 'table_name': table_name, 'header': header, 'rows': rows }

    return render(request, 'ad_tables/tables.html', context)
