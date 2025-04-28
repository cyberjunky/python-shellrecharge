#!/usr/bin/env python3
"""Example code."""
import asyncio
import logging
import sys
from asyncio import CancelledError

import aiohttp
from aiohttp.client_exceptions import ClientError

import shellrecharge
from shellrecharge import LocationEmptyError, LocationValidationError


async def main():
    """Main module."""

    # Some random stations
    location_ids = ["9b9428ab-1dfd-4230-a024-084eacf776ff", "682154", "9cf6c16b-b043-4ba8-b7ca-872f82a0faf4"]

    async with aiohttp.ClientSession() as session:
        try:
            api = shellrecharge.Api(session)
            for location_id in location_ids:
                location = await api.location_by_id(location_id)
                logging.info(location)
        except LocationEmptyError:
            logging.error("No data returned, check location id")
        except LocationValidationError as err:
            logging.error("Location validation error %s, report location id", err)
        except (ClientError, TimeoutError, CancelledError) as err:
            logging.error(err)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
