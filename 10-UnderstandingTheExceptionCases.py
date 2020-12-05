#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: maxschallwig
"""

import requests

url = "http://finance.yahoo.com/quote/AAPL?p=AAPL"

response = requests.get(url)
data = {}
Indicators = {"Previous Close":[],
            "Open":[],
            "Bid":[],
            "Ask":[],
            "Day&#x27;s Range":[],
            "52 Week Range":[],
            "Volume":[],
            "Avg. Volume":[],
            "Market Cap":[],
            "Beta":[],
            "PE Ratio (TTM)":[],
            "EPS (TTM)":[],
            "Earnings Date":[],
            "Dividend &amp; Yield":[],
            "Ex-Dividend Date":[],
            "1y Target Est":[]}
print(response)
print(response.status_code)

htmlText = response.text
#print(htmlText)
for indicator in Indicators:
#    break
    print(indicator)
    splitList = htmlText.split(indicator)
    afterFirstSplit = splitList[1].split("\">")[1]
    afterSecondSplit = afterFirstSplit.split("</td>")
    dataValue = afterSecondSplit[0]
    Indicators[indicator].append(dataValue)

print(Indicators)
#stringExample = "AGbCbDbE"
#print(stringExample.split("b"))


