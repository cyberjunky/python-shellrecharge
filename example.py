#!/usr/bin/env python3
"""Example code."""
import asyncio
import logging
import sys

import aiohttp

import shellrechargeev


async def main():
    """Main module."""
    location_ids = ["9b9428ab-1dfd-4230-a024-084eacf776ff"]

    async with aiohttp.ClientSession() as session:
        api = shellrechargeev.Api(session)

        for location_id in location_ids:
            locations = await api.location_by_id(location_id)
            print(locations)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
