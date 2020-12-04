#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: maxschallwig
"""

import pandas as pd

inputData = {"Data1":[1,2,3,4,5,6],
             "Data2":[5,6,7,8,9,10],
             "Data3":[9,10,11,12,13,14]}
             
             
print(inputData)

df = pd.DataFrame(inputData)
print()
print(df)
print(df.head(2))
print(df.tail(3))