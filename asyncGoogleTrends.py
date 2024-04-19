from pytrendsasync.request import TrendReq
from datetime import date
import time, sys, asyncio

#timeout=(10, 25)
slangTrend = TrendReq(timeout=None, retries=2, backoff_factor=0.1)
category = "0"
location = ""
property = ""
timeframe = "today 5-y"
# testData2 = ["Poggers", "booba", "deez nuts", "monkas", "thicc", "cringe", "skinny legend", "brx", "bru", "leafy", "nightblue", "normie", "hello", "water"]

if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def get_Slang(wordList):
    start_time = time.time()
    responses = await asyncio.gather(*[relatedSlang(kw) for kw in wordList])
    print("get_Slang --- %s seconds ---" % (time.time() - start_time))
    return list(filter(None, responses))


async def relatedSlang(keyword):
    
    await slangTrend.build_payload([keyword], category, timeframe, location, gprop=property)
    data = await slangTrend.related_queries()
    if data[keyword]["top"] is not None:
        relatedQueriesString = ' '.join(data[keyword]["top"]["query"].iloc[0:11])
        if "mean" in relatedQueriesString or "definition" in relatedQueriesString:
            return keyword
        return None 
    return None
