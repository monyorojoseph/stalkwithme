import tweepy, logging, json, asyncio, websockets
from decouple import config
from tweepy.asynchronous import AsyncStream

CONSUMER_KEY=config('CONSUMER_KEY')
CONSUMER_SECRET=config('CONSUMER_SECRET')
ACCESS_TOKEN=config('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET=config('ACCESS_TOKEN_SECRET')

# streamin class
class AsyncStreamListener(AsyncStream):

    async def on_status(self, status):
        if hasattr(status, "_json"):
            print(status._json['text'])
            return status._json['text']
        return False

# async def stream():
#     # strm = AsyncStreamListener(CONSUMER_KEY, CONSUMER_SECRET,  ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#     strm.filter(track=['python'], languages=['en'])


# get places in twitter
async def twitterPlaces():
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    try:
        api.verify_credentials()
        print("Tweepy verified xd")
    except Exception as exc:
        print(f"[ TWEEPY ERROR ] {exc}")
    else:
        return dict([(str(d['country']), str(d['woeid'])) for d in api.available_trends()])
    finally:
        print("[ CLEANING UP ]")

# ws handler
async def handler(websocket):
    print('[ ANOTHER CONNECTION ]')

    # place = await twitterPlaces()
    # await websocket.send(json.dumps({"type": "places", "places":place}))
    # tweet = await stream()
    # await websocket.send(json.dumps({"type": "tweets", "tweets":tweet}))
    strm = AsyncStreamListener(CONSUMER_KEY, CONSUMER_SECRET,  ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    strm.filter(track=['gain'], languages=['en'])




# initiating ws
async def main():
    async with websockets.serve(handler, "localhost", 8001):
        await asyncio.Future()  # run forever

asyncio.run(main())
