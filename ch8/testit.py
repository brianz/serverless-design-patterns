import asyncio
import websockets
import time
import sys
import json

import boto3
from base64 import b64encode


URL = 'wss://ws-feed.gdax.com'


# async def hello():
#     async with websockets.connect(URL) as ws:
#         # name = input("What's your name? ")
#         # await ws.send(name)
#         # print("> {}".format(name))
#
#         greeting = await ws.recv()
#         print("< {}".format(greeting))
#
# asyncio.get_event_loop().run_until_complete(hello())
#

import gdax
from pprint import pprint as pp


#kinesis = boto3.client('kinesis')
firehose = boto3.client('firehose')


class MyWebsocketClient(gdax.WebsocketClient):

    def __init__(self, **kwargs):
        print(kwargs)
        self.message_count = 0
        #kwargs['products'] = ["BTC-USD", "ETH-USD"]
        products = ["BTC-USD", "ETH-USD"]

        kwargs['channels'] = [
            {
                "name": "ticker",
                "product_ids": products,
            },
        ]
        super().__init__(**kwargs)
        self._last_send = int(time.time())
        self.messages = []

    def on_message(self, msg):
        super().on_message(msg)

        self.message_count += 1

        print('Publishing...')
        payload = (json.dumps(msg) + "|||").encode()
        response = firehose.put_record(
                DeliveryStreamName='brianz-gdax-bz-stream',
                Record={'Data': payload}
        )
        pp(response)

    def _foo(self):
        # if not self.message_count % 100:
        #     print(msg)
        if msg.get('side', '') == 'sell':
            pp(msg)

            now = int(time.time())

            self.messages.append(msg)

            if now - self._last_send >= 0:
                print('Publishing...')
                payload = json.dumps(self.messages).encode()
                response = firehose.put_record(
                        #StreamName='bz-test',
                        DeliveryStreamName='bz-test-firehose',
                        #Data=
                        #PartitionKey=msg['time'],
                        # ExplicitHashKey='string',
                        # SequenceNumberForOrdering='string'
                        #Record={'Data': b64encode(payload)}
                )
                pp(response)
                self._last_send = now
                self.messages = []

wsClient = MyWebsocketClient(should_print=False)
wsClient.start()

print(wsClient.url, wsClient.products)

try:
    while True:
        #print("\nMessageCount =", "%i \n" % wsClient.message_count)
        pass
        time.sleep(0.5)
except KeyboardInterrupt:
    wsClient.close()
    print('closed')

if wsClient.error:
    sys.exit(1)
else:
    sys.exit(0)
