import aiohttp
import asyncio
from datetime import datetime, timedelta
import platform
import sys


PRIVATBANK_API = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
CURRENCY_LIST = ['EUR', 'USD']


async def exchange(date : str):
    privatbank_api_date = PRIVATBANK_API + date
    day_rates = {}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(privatbank_api_date , ssl = False) as response:
                if response.status == 200:
                    result = await response.json()
                    exchange_result = list(filter(lambda el: el['currency'] in CURRENCY_LIST , result['exchangeRate']))
                    day_rates[date] = {el['currency'] : {'purchase': el['purchaseRate'], 'sale' : el['saleRate']}  for el in exchange_result}
                else:
                    print(f"Error status: {response.status} for {privatbank_api_date}")
                    
        except aiohttp.ClientConnectorError as err:
            print(f"Connection error with API: {privatbank_api_date} as {err}")
                
    return day_rates

async def main(number_days):
    r = []
    current_day = datetime.now()
    interval = timedelta(days = 1)
    for _ in range(number_days):
        r.append(exchange(current_day.strftime('%d.%m.%Y')))
        current_day -= interval
    return await asyncio.gather(*r)   

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        number_days = int(sys.argv[1])
        if number_days <= 10:
            r = asyncio.run(main(number_days))
        else:
            r = f"The number of days more than 10"
    except ValueError:
        r = f"Next time in console command input number days(integer) <= 10 days , ex.= python3 hw_5.py 4" 
    print(r)
