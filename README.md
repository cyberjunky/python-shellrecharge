# python-shellrechargeev
Python 3 package to retrieve public EV charger data from Shell Recharge

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]

## About

This package allows you to request data from public EV chargers using Shell Recharge.
I build it to create a home-assistant integration, it can be done with rest calls only, but then options are limited.

## Installation

```bash
pip3 install python-shellrecharge
```


## Development

To create a development environment to commit code.

```
pip3 install pdm
pip3 install ruff
pdm init

sudo apt install pre-commit
pip3 install pre-commit
```
Run checks before PR/Commit:
```
make format
make lint
make codespell
```

## Example
Below provides example on how to use the library.  

```
#!/usr/bin/env python3
"""Example code."""
import asyncio
import logging
import sys

import aiohttp

import shellrecharge


async def main():
    """Main module."""
    location_ids = ["9b9428ab-1dfd-4230-a024-084eacf776ff"]

    async with aiohttp.ClientSession() as session:
        api = shellrecharge.Api(session)

        for location_id in location_ids:
            locations = await api.location_by_id(location_id)
            print(locations)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
```

## Donations

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/cyberjunkynl/)  
[![Sponsor][sponsor-shield]][sponsor]

[python-shellrecharge]: https://github.com/cyberjunky/python-shellrecharge
[commits-shield]: https://img.shields.io/github/commit-activity/y/cyberjunky/python-shellrecharge.svg?style=for-the-badge
[commits]: https://github.com/cyberjunky/python-shellrecharge/commits/main
[license-shield]: https://img.shields.io/github/license/cyberjunky/python-shellrecharge.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40cyberjunky-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/cyberjunky/python-shellrecharge.svg?style=for-the-badge
[releases]: https://github.com/cyberjunky/python-shellrecharge/releases
[sponsor-shield]: https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86
[sponsor]: https://github.com/sponsors/cyberjunky
