#!/usr/bin/env python3
import sys
import shellrechargeev
import aiohttp
import asyncio
import logging


async def main():
    location_ids = [
        "3321718",
        "3357677",
        "2875456",
        "2746503",
    ]

    async with aiohttp.ClientSession() as session:
        api = shellrechargeev.Api(session)

        for location_id in location_ids:
            locations = await api.location_by_id(location_id)
            print(locations)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
