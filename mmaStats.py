import requests

url = "https://en.wikipedia.org/wiki/Ovince_Saint_Preux"

response = requests.get(url)

firstParse = response.text.split("infobox vcard")[1]

secondParse = response.text.split("[102]")[0]
number = len(secondParse) - 5000
print(secondParse[number:len(secondParse)-1])
#print(firstParse[0:10000])