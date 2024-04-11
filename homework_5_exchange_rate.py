import aiohttp
import asyncio
import json
import sys
from datetime import datetime,timedelta

API_URL = 'http://api.nbp.pl/api/exchangerates/tables/A/'
CURRENCIES = ['EUR', 'USD']

async def fetch_exchange_rates(days):
    async with aiohttp.ClientSession() as session:
        task = [fetch_exchange_rate(session, day) for day in range(1, days+1)]
        return await asyncio.gather(*task)
    
async def fetch_exchange_rate(session, days_ago):
    date = (datetime.today() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    url = f"{API_URL}{date}/"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return {date: {currency: get_currency_exchange(data, currency) for currency in CURRENCIES}}
        else:
            return {date: None}
        
def get_currency_exchange(data, currency):
    rates = {entry['currency']: entry for entry in data[0]['rates']}
    return {'sale': rates[currency]['ask'], 'purchase': rates[currency]['bid']}

def main():
    if len(sys.argv) !=2:
        print("Usage: python main.py <number of days>")
        return
    
    try:
        days = int(sys.argv[1])
        if days < 1 or days >10:
            raise ValueError
    except ValueError:
        print("Number of days must be an integer between 1 and 10")
        return
    
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(fetch_exchange_rate(days))
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()