import asyncio
import logging

import async_timeout
import pydantic
from aiohttp import ClientResponse, ClientSession
from aiohttp.client_exceptions import ClientError
from yarl import URL

from .models import Location


class Api:
    """Class to make API requests."""

    def __init__(self, websession: ClientSession):
        """Initialize the session."""
        self.websession = websession
        self.logger = logging.getLogger("shellrechargeev")

    async def location_by_id(
        self, location_id: str, **kwargs
    ) -> list[Location]:
        """
        Perform API request.
        Usually yields just one Location object and one or multiple chargers.
        """

        location_data = {}
        url_template = (
            "https://ui-map.shellrecharge.com/api/map/v2/locations/{}"
        )
        url = URL(url_template.format(location_id))

        try:
            with async_timeout.timeout(10):
                response = await self.websession.get(url)

            if response.status == 200:
                result = await response.json()
                location_data = Location.model_validate(result)
            else:
                self.logger.exception("Error %s on %s", response.status, url)

        except pydantic.ValidationError as err:
            # Fetched data not valid
            self.logger.exception(err)
            raise err

        except (
            ClientError,
            asyncio.TimeoutError,
            asyncio.CancelledError,
        ) as err:
            self.logger.exception(err)
            raise err

        return location_data

    async def request(self, method: str, url: URL, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        return await self.websession.request(
            method,
            url,
            **kwargs,
            headers=headers,
        )
