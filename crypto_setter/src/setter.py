import sys
from typing import Union
import aiohttp
import datetime
import asyncio

from model import (
    Price, init_db, async_session
)


class Writer:
    def __init__(self, ticker:str):
        self.ticker: str = ticker

    async def fetch_price(self, session):
        url = f"https://www.deribit.com/api/v2/public/get_index_price?index_name={self.ticker}"
        async with session.get(url) as response:
            data = await response.json()
            price = data["result"]["index_price"]
            return self.ticker, price

    async def save_price(self, ticker, price, db):
        timestamp = datetime.datetime.now()
        new_price = Price(ticker=ticker, price=price, timestamp=timestamp)
        db.add(new_price)
        await db.commit()
        print(f"Saved {ticker} price: {price} at {timestamp}")

    async def start_querying(self):
        await init_db()
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session, async_session() as db:
            while True:
                # Получаем текущие цены
                task = self.fetch_price(session)
                ticker, price = await task

                await self.save_price(ticker, price, db)

                # Ждем минуту до следующего запроса
                await asyncio.sleep(60)


async def start_querying():
    # Instantiate Writer objects for each ticker
    writer_btc = Writer("btc_usdt")
    writer_eth = Writer("eth_usdt")

    # Run both querying processes concurrently
    await asyncio.gather(
        writer_btc.start_querying(),
        writer_eth.start_querying()
    )

if __name__ == "__main__":
    asyncio.run(start_querying())

