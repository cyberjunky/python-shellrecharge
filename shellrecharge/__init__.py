"""The shellrecharge API code."""
import asyncio
import logging

import async_timeout
import pydantic
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from yarl import URL

from .models import Location


class Api:
    """Class to make API requests."""

    def __init__(self, websession: ClientSession):
        """Initialize the session."""
        self.websession = websession
        self.logger = logging.getLogger("shellrecharge")

    async def location_by_id(self, location_id: str) -> Location:
        """
        Perform API request.
        Usually yields just one Location object with one or multiple chargers.
        """
        location_data = {}
        url_template = (
            "https://ui-map.shellrecharge.com/api/map/v2/locations/search/{}"
        )
        url = URL(url_template.format(location_id))

        try:
            with async_timeout.timeout(10):
                response = await self.websession.get(url)

            if response.status == 200:
                result = await response.json()
                if result:
                    if pydantic.version.VERSION.startswith("1"):
                        location_data = Location.parse_obj(result[0])
                    else:
                        location_data = Location.model_validate(result[0])
            else:
                self.logger.exception("Error %s on %s", response.status, url)

        except pydantic.ValidationError as err:
            # Fetched data not valid
            self.logger.exception(err)
            raise err
        except (
            ClientError,
            TimeoutError,
            asyncio.exceptions.CancelledError,
        ) as err:
            self.logger.exception(err)
            raise err

        return location_data
