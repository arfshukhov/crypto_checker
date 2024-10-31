from fastapi import FastAPI, APIRouter
from starlette.responses import JSONResponse

from setings import ServerSettings

import asyncio

from ..middleware.crypto_getter_middleware import Reader

router = APIRouter()

@router.get("/all_values/{ticker}", tags=["crypto"])
async def get_all_values_by_ticker(ticker: str):
    """
    Обработчик запроса для получения всех цен по тикеру.
    :param ticker: Тикер криптовалюты.
    :return: JSON с данными цен и количеством записей.
    """
    try:
        data = await Reader.get_price_by_ticker("btc_usdt")
        return JSONResponse(data, status_code=200)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=422)


@router.get("/current_value/{ticker}", tags=["crypto"])
async def get_current_value(ticker: str):
    """
    Обработчик запроса для получения последней цены по тикеру.
    :param ticker: Тикер криптовалюты.
    :return: JSON с последней ценой и временной меткой.
    """
    try:
        data = await Reader.get_last_price_by_ticker("btc_usdt")
        return JSONResponse(data, status_code=200)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=422)

@router.get("/values_by_date_range/{ticker}", tags=["crypto"])
async def get_values_by_date_range(ticker: str, start_date, end_date):
    """
    Обработчик запроса для получения цен по тикеру за указанный диапазон дат.
    :param ticker: Тикер криптовалюты.
    :param start_date: Начальная дата в формате 'YYYY-MM-DD'.
    :param end_date: Конечная дата в формате 'YYYY-MM-DD'.
    :return: JSON с данными цен и количеством записей за указанный период.
    """
    try:
        data = await Reader.get_by_date(ticker, start_date, end_date)
        return JSONResponse(data, status_code=200)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=422)
