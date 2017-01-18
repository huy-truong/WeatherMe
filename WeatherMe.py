from __future__ import print_function

import json
import time
import sys


if sys.version_info > (3, 0):
    import http.client as httpclient
else:
    import httplib as httpclient


API_KEY = 'DYebZypGF6OeioADUC4JD3pZggC7Hgbg'


def getAddress():
    trial = 0
    while trial<2:
        try:
            conn = httpclient.HTTPConnection('ipecho.net')
            conn.request('GET', '/plain')
            resp = conn.getresponse().read().decode(encoding='utf-8')
            # data = json.loads(resp)
            data = resp
            conn.close()
            return data
        except:
            trial=trial+1
    trial=0
    while trial < 2:
        try:
            conn = httpclient.HTTPSConnection('wtfismyip.com', 2)
            conn.request('GET', '/json')
            resp = conn.getresponse().read().decode(encoding='utf-8')
            data = json.loads(resp)
            conn.close()
            return data['YourFuckingIPAddress']
        except:
                    trial = trial + 1
    return None



def getLocationId(address):
    trial = 0
    resp = ''
    while trial < 2:
        try:
            x = httpclient.HTTPConnection('dataservice.accuweather.com', timeout=3)
            sublink = '/locations/v1/cities/ipaddress?' + 'apikey=' + API_KEY + '&q=' + address
            x.request('GET', sublink)

            resp = x.getresponse().read().decode(encoding='utf-8')
            data = json.loads(resp)
            x.close()
            return data['Key'],data['LocalizedName']
        except:
            print('Trying to locate ...')
            time.sleep(5)
            trial = trial + 1
    return None


def getWeather(id):
    trial = 0
    resp = ''
    while trial < 2:
        try:
            x = httpclient.HTTPConnection('dataservice.accuweather.com', timeout=3)
            sublink = '/forecasts/v1/daily/1day/' +id+ '?apikey=' + API_KEY+'&metric=true&details=true'
            x.request('GET', sublink)

            resp = x.getresponse().read().decode(encoding='utf-8')
            data = json.loads(resp)
            x.close()
            return data['DailyForecasts']
        except:
            print('Trying to locate ...')
            time.sleep(5)
            trial = trial + 1
    return None



if __name__ == "__main__":
    address = getAddress()
    if address == None:
        pass
    id, name = getLocationId(address)
    forecast = getWeather(id)[0]
    print()
    print('-'*30)
    print('Location : %s'%name,end='\n\n')

    print('Temperature : \n\tMaximum: {} C\n\tMininum: {} C'.format(forecast['Temperature']['Maximum']['Value'],
                                                                    forecast['Temperature']['Minimum']['Value']),'\n\n')
    print('Real Feel Temperature : \n\tMaximum: {} C\n\tMininum: {} C'.format(forecast['RealFeelTemperature']['Maximum']['Value'],
                                                                    forecast['RealFeelTemperature']['Minimum']['Value']),'\n\n')
    print('Real Feel Temperature Shade : \n\tMaximum: {} C\n\tMininum: {} C'.format(
        forecast['RealFeelTemperatureShade']['Maximum']['Value'],
        forecast['RealFeelTemperatureShade']['Minimum']['Value']),'\n\n')
    print('Day   : {}\n\tRain: {} mm\n\tSnow: {} cm'.format(forecast['Day']['LongPhrase'],forecast['Day']['Rain']['Value'],forecast['Day']['Snow']['Value']),'\n\n')
    print('Night : {}\n\tRain: {} mm\n\tSnow: {} cm'.format(forecast['Night']['LongPhrase'],forecast['Night']['Rain']['Value'],forecast['Night']['Snow']['Value']),'\n\n')


