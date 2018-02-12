import requests
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

PUBLIC_API_URL = 'https://query.yahooapis.com/v1/public/yql'
DATATABLES_URL = 'store://datatables.org/alltableswithkeys'

response = requests.get(PUBLIC_API_URL + '?' + urlencode({
            'q': 'APPL',
            'format': 'json',
            'env': DATATABLES_URL
            }))

print response.status_code
print response.text