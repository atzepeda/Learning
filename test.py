real = "real"
fake = "fake"
thingOne = "thingOne"
thingTwo = "thingTwo"

def fighterStats(fName): 
    if fName=="Stephen":
        return {
            'stringOne': "STRING",
            'stringTwo': "ALSO_STRING"
        }
    else:
        return("hello")

item = {
    'Fight': "Stephen vs Neal",
    'FighterOne': fighterStats("Stephen"),
    'FighterTwo': fighterStats("Neal")
}

print(item)