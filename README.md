# Python: Shell Recharge

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
pip3 install shellrecharge
```

## Configuration

Find the EV charger(s) you want to monitor here: https://shellrecharge.com/en-gb/find-a-charge-point look for the Serial number under details section.
Then use Add device within Home Assistant and enter the Serial number in the form.

Example:

![image](https://github.com/user-attachments/assets/33dc84d1-319e-4100-ba60-86fbefcdf04e)


## Development

To create a development environment to commit code.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install pdm
pip3 install ruff
pdm init

sudo apt install pre-commit
pip3 install pre-commit
```

Run checks before PR/Commit:

```bash
make all
```

## Example

Below provides example on how to use the library.

```python
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
            logging.error("Location validation error {}, report locaton id" % err)
        except (ClientError, TimeoutError, CancelledError) as err:
            logging.error(err)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
```

## Donations

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/cyberjunkynl/)
[![Sponsor][sponsor-shield]][sponsor]

[commits-shield]: https://img.shields.io/github/commit-activity/y/cyberjunky/python-shellrecharge.svg?style=for-the-badge
[commits]: https://github.com/cyberjunky/python-shellrecharge/commits/main
[license-shield]: https://img.shields.io/github/license/cyberjunky/python-shellrecharge.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40cyberjunky-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/cyberjunky/python-shellrecharge.svg?style=for-the-badge
[releases]: https://github.com/cyberjunky/python-shellrecharge/releases
[sponsor-shield]: https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86
[sponsor]: https://github.com/sponsors/cyberjunky
