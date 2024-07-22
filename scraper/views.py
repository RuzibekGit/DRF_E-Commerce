from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render

import requests
from bs4 import BeautifulSoup




def scrape_receipt_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Update these selectors based on the actual HTML structure
    receipt_number_element = soup.select_one('.products-row td')
    
    print(receipt_number_element)
    print(soup.title.text)
    date_element = soup.select_one('#date')
    total_amount_element = soup.select_one('#totalAmount')
    

    table = soup.find('table')


    # Extract headers
    headers = []
    # for tr in table.find('tbody').find_all('tr'):
    #     memo = []
    #     for td in tr.find_all('td'):
    #         if td := td.text.strip():
    #             memo.append(td)
    #     if memo:
    #         headers.append(memo)
    
    # print(headers)

    rows = []

    memo = []
    memo_dict = {}
    products = table.find('tbody').find_all('tr')
    l = len(products)
    for index, tr in enumerate(products):
        
        if 'products-row' in tr.get('class', []):
            if memo_dict:
                memo.append(memo_dict)
                memo_dict = {}
            for i, td in enumerate(tr.find_all('td')):
                match i:
                    case 0:memo_dict["name"] = td.text.strip()
                    case 1:memo_dict["soni"] = td.text.strip()
                    case 2:memo_dict["narxi"] = td.text.strip()

        else:
            for i, td in enumerate(tr.find_all('td')):
                if i == 0:
                    m = td.text.strip()
                else:
                    memo_dict[m] = td.text.strip()
    memo.append(memo_dict)


    for data in memo:
        for key, val in data.items():
            print(f"{key} ==   {val}")

    

    data = {
        'receipt_number': soup.title.text,
        'shop_name': soup.title.text,
        'date': soup.title.text,
        'product': memo,
        'raw': headers
    }

    return data


class ScrapeReceiptView(APIView):
    def get(self, request, *args, **kwargs):
        data = request.data
        FB = data.get('fb')
        FM = data.get('fm')
        RS = data.get('rs')
        RC = data.get('rc')
        url = f'https://ofd.soliq.uz/check?t={FM}&r={RS}&c={RC}&s={FB}'
        if not url:
            return Response({'error': 'URL parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = scrape_receipt_data(url)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
