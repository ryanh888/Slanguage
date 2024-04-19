import requests, aiohttp, asyncio, time, json, string, sys
from datetime import date
from collections import ChainMap

currentDate = date.today()

dummyList = ['have','the','banana', 'yeehaw', 'sus', '?', 'a', 'asdikuifg', 'poggers']

start_time = time.time()

def getMeaning(file):
    meaning = file["list"][0]["definition"]
    meaning = meaning.replace("[", "").replace("]", "").capitalize()
    return meaning


def getUpvotes(file):
    upvotes = str(file["list"][0]["thumbs_up"])
    return upvotes


# mostCommonWordsSet = set(line.strip() for line in open ('mostCommonWords.txt'))
with open ("commonSlang.json", "r") as f:
    commonSlangJson = json.load(f)

with open ("mostCommonWords.json", "r") as f:
    mostCommonWordsSet = json.load(f)


def commonFilter(json):
    start_time = time.time()
    slangDict = {}
    finalSlang = []
    tempSlang = []
    for message in reversed(json["messages"]):
            if "content" in message:
                words = message["content"].split()
                for word in words:
                    punctuatedWord = word.lower().translate(str.maketrans('', '', string.punctuation)).replace('?', '')
                    if word in commonSlangJson:
                        finalSlang.append(word)
                        continue
                    if punctuatedWord in commonSlangJson:
                        finalSlang.append(punctuatedWord)
                        continue
                    if word in mostCommonWordsSet:
                        continue
                    if punctuatedWord in mostCommonWordsSet:
                        continue
                    
                    if len(punctuatedWord) > 2:
                        if (punctuatedWord[-1] == 's' or punctuatedWord[-1] == 'd') and (punctuatedWord[0:-1] in mostCommonWordsSet):
                            continue
                        if (punctuatedWord[-2:] == 'nt' or punctuatedWord[-2:] == 've' or punctuatedWord[-2:] == 're' or punctuatedWord[-2:] == 'er' or punctuatedWord[-2:] == 'ly' or punctuatedWord[-2:] == 'ed' or punctuatedWord[-2:] == 'll') and (punctuatedWord[0:-3] in mostCommonWordsSet or punctuatedWord[0:-2] in mostCommonWordsSet or punctuatedWord[0:-1] in mostCommonWordsSet):
                            continue
                    if (punctuatedWord not in mostCommonWordsSet) and len(word) < 50:
                            tempSlang.append(punctuatedWord)
                            continue


    slangDict["finalSlang"] = list(set(finalSlang))
    slangDict["tempSlang"] = list(set(asyncio.run(initialUrbanFilter(tempSlang)))) #Checks to see if it exists in Urban Dictionary and has over 300 upvotes
    print("commonFilter --- %s seconds ---" % (time.time() - start_time))
    return slangDict
                    
async def finalUrbanFilter(slangList): 
    
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        tasks = []

        for word in slangList:
            task = asyncio.ensure_future(getWordMeaning(session, word))
            tasks.append(task)

        slangDict = await asyncio.gather(*tasks)
        slangArray = list(filter(None, slangDict))
        
        slangDict = dict(ChainMap(*slangArray))
        with open ("commonSlang.json", "w") as f:
            json.dump(commonSlangJson, f)
        print("urbanFilter --- %s seconds ---" % (time.time() - start_time))
        return slangDict


async def getWordMeaning(session, word):
    slangDict = {}
    url = "http://api.urbandictionary.com/v0/define?term={}".format(word)

    async with session.get(url) as response:
        file = await response.json()
        if response.status == 200:
            #if slang already exists in file and has a definition
            if file["list"] != [] and word in commonSlangJson and commonSlangJson[word] != "":  
                slangDict[word] = commonSlangJson[word]
                return slangDict

            commonSlangJson[word] = getMeaning(file)
            slangDict[word] = commonSlangJson[word]
            
            return slangDict
        else:
            return {}

async def initialUrbanFilter (tempList):
    async with aiohttp.ClientSession() as session:
        start_time = time.time()

        slangList = await asyncio.gather(*[initialFilter(session, word) for word in tempList])
        filteredList = list(filter(None, slangList))
        
        
        print("urbanFilter --- %s seconds ---" % (time.time() - start_time))
        return filteredList

async def initialFilter (session, word):
    url = "http://api.urbandictionary.com/v0/define?term={}".format(word)

    async with session.get(url) as response:
        file = await response.json()
        if response.status == 200:
            if file["list"] != [] and int(getUpvotes(file)) > 300:
                return word
        else:
            return ''


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

