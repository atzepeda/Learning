#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: maxschallwig
"""

import requests

url = "http://finance.yahoo.com/quote/AAPL?p=AAPL"

response = requests.get(url)
Indicators = ["Previous Close",
            "Open",
            "Bid",
            "Ask",
            "Day's Range",
            "52 Week Range",
            "Volume",
            "Avg. Volume",
            "Market Cap",
            "Beta",
            "PE Ratio (TTM)",
            "EPS (TTM)",
            "Earnings Date",
            "Dividend & Yield",
            "Ex-Dividend Date",
            "1y Target Est"]
print(response)
print(response.status_code)

htmlText = response.text

splitList = htmlText.split("Previous Close")
print(len(splitList))

#stringExample = "AGbCbDbE"
#print(stringExample.split("b"))


