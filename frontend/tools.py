from urllib.parse import urlencode

from django.shortcuts import reverse

import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta


def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urlencode(get)
    return url


def initial_date(request, months=12):
    #  gets the initial last three months or the session date
    date_now = datetime.datetime.today()
    date_range = request.GET.get('date_range', False)

    if date_range:
        try:
            date_range = date_range.split('-')
            date_range[0] = date_range[0].replace(' ','')
            date_range[1] = date_range[1].replace(' ','')
            date_start = datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
            date_end = datetime.datetime.strptime(date_range[1],'%m/%d/%Y')
        except:
            print('except hitted')
            date_three_months_ago = date_now - relativedelta(months=months)
            date_start = date_three_months_ago
            date_end = date_now
            date_range = '%s - %s' % (str(date_three_months_ago).split(' ')[0].replace('-','/'),str(date_now).split(' ')[0].replace('-','/'))
            # request.session['date_range'] = '%s - %s'%(str(date_three_months_ago).split(' ')[0].replace('-','/'),str(date_now).split(' ')[0].replace('-','/'))
    else:
        date_start = datetime.datetime.now()
        date_end = datetime.datetime.now() + timedelta(days=30*months)
    return [date_start, date_end, date_range]
