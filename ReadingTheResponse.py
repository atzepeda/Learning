#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: maxschallwig
"""

import requests

url = "https://www.sherdog.com/fighter/Jack-Hermansson-61146"

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
#print(response.text)


htmlText = response.text

splitList = htmlText.split("final_result")
print(splitList)

#stringExample = "AGbCbDbE"
#print(stringExample.split("b"))


