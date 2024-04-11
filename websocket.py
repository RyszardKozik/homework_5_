import asyncio
import websockets
from aiofile import AIOFile, Writer
from datetime import datetime
import json

exchange_rates = {
    '03.11.2022': {
        'EUR': {'sale': 39.4, 'purchase': 38.4},
        'USD': {'sale': 39.9, 'purchase': 39.4},
        'GBP': {'sale': 45.2, 'purchase': 44.1},
        'CHF': {'sale': 42.8, 'purchase': 41.7}
    },
    '02.11.2022': {
        'EUR': {'sale': 39.4, 'purchase': 38.4},
        'USD': {'sale': 39.9, 'purchase': 39.4},
        'GBP': {'sale': 45.2, 'purchase': 44.1},
        'CHF': {'sale': 42.8, 'purchase': 41.7}
    }
}

async def handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        command = data.get('command')
        if command == 'exchange':
            currency = data.get('currency')
            response = await get_exchange_rates(currency)
            await websocket.send(json.dumps(response))
            await log_exchange_command(command, currency)
        else:
            data = f"Data received as:  {data}!"
            print(data)
            await websocket.send(data)

async def get_exchange_rates(currency):
    response = []
    for date, rates in exchange_rates.items():
        if currency in rates:
            response.append({date: rates[currency]})
    return response

async def log_exchange_command(command, currency):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp}: Command '{command}' executed for currency '{currency}'\n"
    async with AIOFile("exchange_log.txt", 'a') as afp:
        writer = Writer(afp)
        await writer(log_entry)

async def main():
    async with websockets.serve(handler, "localhost", 8000):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())