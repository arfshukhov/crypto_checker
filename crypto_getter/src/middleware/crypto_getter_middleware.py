from model import *

import asyncio

class Reader:
    """
    Класс Reader для работы с данными цен криптовалют.
    """
    @classmethod
    async def get_price_by_ticker(cls, ticker):
        """
        Получает все цены по заданному тикеру
        :param ticker: Тикер криптовалюты (например, 'btc_usdt').
        :return: Словарь с ценами и количеством записей.
        """
        async with async_session() as session:
            result = await session.execute(select(Price).filter(Price.ticker == ticker))
            prices = result.scalars().all()

            data = {"data": [], "count": 0}
            for price in prices:
                price_dict = price.__dict__
                price_dict["timestamp"] = price.timestamp.__str__()
                del price_dict["id"]
                price_dict.pop("_sa_instance_state", None)
                data["data"].append(price_dict)
                data["count"] += 1
            return data

    @classmethod
    async def get_last_price_by_ticker(cls, ticker):
        """
        Получает последнюю цену по заданному тикеру
        :param ticker: Тикер криптовалюты (например, 'btc_usdt').
        :return: Словарь с последней ценой и временной меткой.
        """
        async with async_session() as session:
            result = await session.execute(
                select(Price).filter(Price.ticker == ticker)
                                           .order_by(Price.timestamp.desc()))
            price = result.scalars().first()
            price_dict = price.__dict__
            price_dict["timestamp"] = price.timestamp.__str__()
            price_dict.pop("_sa_instance_state")
            return price_dict

    @classmethod
    async def get_by_date(cls, ticker, from_date, to_date):
        """
        Получает цены по заданному тикеру за указанный диапазон дат
        :param ticker: Тикер криптовалюты (например, 'btc_usdt').
        :param from_date: Начальная дата в формате 'YYYY-MM-DD'.
        :param to_date: Конечная дата в формате 'YYYY-MM-DD'.
        :return: Словарь с ценами и количеством записей за указанный период.
        """
        async with async_session() as session:
            result = await session.execute(
                select(Price).filter(Price.ticker == ticker, Price.timestamp.between(from_date, to_date))
            )
            prices = result.scalars().all()
            data = {"data": [], "count": 0}
            for price in prices:
                price_dict = price.__dict__
                price_dict["timestamp"] = price.timestamp.__str__()
                del price_dict["id"]
                price_dict.pop("_sa_instance_state", None)
                data["data"].append(price_dict)
                data["count"] += 1
            return data

