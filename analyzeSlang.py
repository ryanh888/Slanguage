from flask import request
from flask.helpers import make_response
import csv
import json
from urbanDictInfo import *
from asyncGoogleTrends import *

class AnalyzeSlang:
    def __init__(self, socialMedia):
        self.__socialMedia = socialMedia
        self.__slangs = None
        self.__slangDict = None
        self.__data = None          #Nested Dictionary of messages, timestamp, username
        self.__names = []
        self.__wordCount = {}
        self.__topTen = {}
        self.__totalSent = None
        self.__topTenSlangWords = {}
        self.__slangCountPerPerson = {}
        self.__personalSlangDict = {}

        self.__getJSON() 
        self.__getSlang()
        self.__getNames()
        self.__getWordCount()
        self.__getTopTen()
        self.__getTotalSent()
        self.__getTopTenSlangWords()
        self.__getTopTenSlangCountPerPerson()
        # self.__newSlang()

    def __getSlang(self):
        if (self.__data) != None:
            slangList = []
            slangDict = commonFilter(self.__data)
            updatedSlangList = asyncio.run(get_Slang(slangDict["tempSlang"]))
            combinedSlangList = slangDict['finalSlang']+ updatedSlangList
            slangDict = asyncio.run(finalUrbanFilter(combinedSlangList))
            self.__slangDict = slangDict
            for slang in slangDict:
                slangList.append(slang)
            
            
            self.__slangs = slangList
            

    # def __newSlang(self):
    #     if (self.__slangs) != None:
    #         with open ("commonSlang.json", "r") as f:
    #             commonSlangJson = json.load(f)
    #         for word in self.__slangs:
    #             punctuatedWord = word.lower().translate(str.maketrans('', '', string.punctuation)).replace('?', '')
    #             if punctuatedWord not in commonSlangJson:
    #                 commonSlangJson[word.strip()] = ''
    #         with open ("commonSlang.json", "w") as f:
    #             json.dump(commonSlangJson, f)

    def __getJSON(self):
        mydict = (request.files['file']).read()
        file = make_response(mydict)
        file.mimetype = 'application/json'
        file.close()
        self.__data = file.json

    def __getNames(self):
        if self.__socialMedia == "facebook" or self.__socialMedia == "instagram":
            for participant in self.__data["participants"]:
                self.__names.append(participant["name"])
        if self.__socialMedia == "discord":
            for message in self.__data["messages"]:
                if message["author"]["name"] not in self.__names:
                    self.__names.append(message["author"]["name"])

    def __getWordCount(self):
        for message in reversed(self.__data["messages"]):
            if "content" in message:
                words = message["content"].split()
                for word in words:
                    if word in self.__wordCount:
                        self.__wordCount[word] += 1
                    else:
                        self.__wordCount[word] = 1

    def __getTopTen(self):
        sortedKeys = sorted(self.__wordCount, key=self.__wordCount.get)
        for i in range(1, 11):
            self.__topTen[sortedKeys[len(sortedKeys) - i]] = self.__wordCount[sortedKeys[len(sortedKeys) - i]]

    def __getTotalSent(self):
        self.__totalSent = {"totalMessages": [], "totalWords": []}
        for name in self.__names:
            msgCount = 0
            wordCount = 0
            for message in self.__data["messages"]:
                if self.__socialMedia == "facebook" or self.__socialMedia == "instagram":
                    if message["sender_name"] == name:
                        msgCount += 1

                        if "content" in message:
                            words = message["content"].split()
                            wordCount += len(words)
                
                if self.__socialMedia == "discord":
                    if message["author"]["name"] == name:
                        msgCount += 1

                        if "content" in message:
                            words = message["content"].split()
                            wordCount += len(words)

            self.__totalSent["totalMessages"].append(msgCount)
            self.__totalSent["totalWords"].append(wordCount)

    def __getTopTenSlangWords(self):
        slangCount = {}
        for slang in self.__slangs:
            
            for message in self.__data["messages"]:
                if "content" in message:
                    sentence = message["content"].split()
                    for word in sentence:
                        if word == slang or word.lower().translate(str.maketrans('', '', string.punctuation)).replace('?', '') == slang:
                            if slang in slangCount:
                                slangCount[slang] += 1
                            else:
                                slangCount[slang] = 1

        sortedKeys = sorted(slangCount, key=slangCount.get)
        if len(sortedKeys) < 10:
            for i in range(1, len(sortedKeys)+1):
                self.__topTenSlangWords[sortedKeys[len(sortedKeys) - i]] = slangCount[sortedKeys[len(sortedKeys) - i]]
        if len(sortedKeys) >= 10:
            for i in range(1, 11):
                self.__topTenSlangWords[sortedKeys[len(sortedKeys) - i]] = slangCount[sortedKeys[len(sortedKeys) - i]]

    def __getTopTenSlangCountPerPerson(self):
        for slang in [*self.__topTenSlangWords.keys()]:
            for name in self.__names:
                slangCount = 0
                for message in self.__data["messages"]:
                    if self.__socialMedia == "facebook" or self.__socialMedia == "instagram":
                        if "content" in message and message["sender_name"] == name:
                            sentence = message["content"].split()
                            for word in sentence:
                                if word == slang or word.lower().translate(str.maketrans('', '', string.punctuation)).replace('?', '') == slang:
                                    slangCount += 1
                    if self.__socialMedia == "discord":
                        if "content" in message and message["author"]["name"] == name:
                            sentence = message["content"].split()
                            for word in sentence:
                                if word == slang or word.lower().translate(str.maketrans('', '', string.punctuation)).replace('?', '') == slang:
                                    slangCount += 1

                if slang in self.__slangCountPerPerson:
                    self.__slangCountPerPerson[slang].append(slangCount)
                else:
                    self.__slangCountPerPerson[slang] = [slangCount]

    def __getPersonalSlangDict(self):
        for name in self.__names: 
            personalSlangCount = {}           
            for slang in [*self.__slangs]:
                for message in self.__data["messages"]:
                    if self.__socialMedia == "facebook" or self.__socialMedia == "instagram":
                        if "content" in message and message["sender_name"] == name:
                            sentence = message["content"].split()
                            for word in sentence:
                                if word == slang or word.lower().translate(str.maketrans('', '', string.punctuation)).replace('?', '') == slang:
                                    if word in personalSlangCount or word.lower().translate(str.maketrans('', '', string.punctuation)).replace('?', '') in personalSlangCount:
                                        personalSlangCount[slang] +=  1
                                    else: 
                                        personalSlangCount[slang] = 1

                    if self.__socialMedia == "discord":
                        if "content" in message and message["author"]["name"] == name:
                            sentence = message["content"].split()
                            for word in sentence:
                                if word == slang or word.lower().translate(str.maketrans('', '', string.punctuation)).replace('?', '') == slang:
                                    if word in personalSlangCount or word.lower().translate(str.maketrans('', '', string.punctuation)).replace('?', '') in personalSlangCount:
                                        personalSlangCount[slang] +=  1
                                    else: 
                                        personalSlangCount[slang] = 1
            self.__personalSlangDict[name] = personalSlangCount
        return self.__personalSlangDict

    def createCSV(self, userName):
        for name in self.__names:
            if userName == name:
                self.__userExists = True
                csvFile = open("messages.csv", "w", encoding='utf-8', newline='')
                csvWriter = csv.writer(csvFile)
                csvWriter.writerow(["Content", "Context"])
                for message in self.__data["messages"]:
                    if self.__socialMedia == "facebook" or self.__socialMedia == "instagram":
                        if message["sender_name"] == userName and "content" in message:
                            csvWriter.writerow([message["content"]])
                    if self.__socialMedia == "discord":
                        if message["author"]["name"] == userName and "content" in message:
                            csvWriter.writerow([message["content"]])
                break

        if not self.__userExists:
            raise NameError("Invalid Name")

    def getTemplateSetup(self):
        
        template = {"topTenWords": list(self.__topTen.keys()),
                    "topTenWordCount": list(self.__topTen.values()),
                    "names": self.__names,
                    "totalMessages": list(self.__totalSent["totalMessages"]),
                    "totalWords": list(self.__totalSent["totalWords"]),
                    "topTenSlang": list(self.__topTenSlangWords.keys()),
                    "topTenSlangCount": list(self.__topTenSlangWords.values()),
                    "topTenSlangCountPerPerson": list(self.__slangCountPerPerson.values()),
                    "slangMeaning": self.__slangDict,
                    "slangListLength": len(self.__topTenSlangWords.keys()),
                    "personalSlangDict": self.__getPersonalSlangDict(),
                    }

        return(template)

    def getParticipantNames(self):
        return self.__names
