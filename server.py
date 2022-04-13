import tweepy, os, signal, json, asyncio, websockets
from decouple import config
from tweepy.asynchronous import AsyncStream

CONSUMER_KEY='hiGbtbeGwBwgwEBccj4oteKAF'
CONSUMER_SECRET='WFZXFeAWC8LVGYOGVTMbevOKwib092j1RUEtwwMGtY7CQe5VyH'
ACCESS_TOKEN='1417225484971085827-vXozJSDAUOTwwyC3xkeI6z0Mfzwdtf'
ACCESS_TOKEN_SECRET='4qzPCkx7lvKIxYlhXMpeyzhDdsZaO02iuJTKZEX4TO3Sd'

# CONSUMER_KEY=config('CONSUMER_KEY')
# CONSUMER_SECRET=config('CONSUMER_SECRET')
# ACCESS_TOKEN=config('ACCESS_TOKEN')
# ACCESS_TOKEN_SECRET=config('ACCESS_TOKEN_SECRET')

# streamin class
class AsyncStreamListener(AsyncStream):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, websocket ):
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret)
        self._websocket = websocket

    async def on_status(self, status): 
        if hasattr(status, "_json"):
            data = status._json
            if hasattr(data, "retweeted_status"):
                return False
            await self._websocket.send(json.dumps(
                    {
                        "type":"tweets", 
                        "time": data['created_at'],
                        "text": data['text'],
                        "name": data['user']['screen_name']
                    }
                ))
            print(data['created_at'], data["text"])
        return False

# get places in twitter
async def twitterPlaces(websocket):
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    try:
        api.verify_credentials()
        print("Tweepy verified xd")
    except Exception as exc:
        print(f"[ TWEEPY ERROR ] {exc}")
    else:
        places = dict([(str(d['country']), str(d['woeid'])) for d in api.available_trends()])
        await websocket.send(json.dumps({"type": "places", "places":places}))
    finally:
        print("[ CLEANING UP ]")


async def mainTwitterHandler(websocket):

    await twitterPlaces(websocket)
    await asyncio.sleep(0.1)
    strm = AsyncStreamListener(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, websocket)
    strm.filter(track=["spiderman"], languages=['en'])
    
    async for message in websocket:
        print('yes', id(message))



# ws handler
async def handler(websocket):
    print('[ ANOTHER CONNECTION ]')
    await mainTwitterHandler(websocket)
    

# initiating ws
async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    port = int(os.environ.get("PORT", "8001"))
    async with websockets.serve(handler, "", port):
        await stop  # run forever

if __name__ == "__main__":
    asyncio.run(main())