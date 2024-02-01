"""The shellrecharge API code."""
import logging
from asyncio import CancelledError, TimeoutError

import pydantic
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from aiohttp_retry import ExponentialRetry, RetryClient
from pydantic import ValidationError
from yarl import URL

from .models import Location


class Api:
    """Class to make API requests."""

    def __init__(self, websession: ClientSession):
        """Initialize the session."""
        self.websession = websession
        self.logger = logging.getLogger("shellrecharge")

    async def location_by_id(self, location_id: str) -> Location | None:
        """
        Perform API request.
        Usually yields just one Location object with one or multiple chargers.
        """
        location = None

        url = URL(
            "https://ui-map.shellrecharge.com/api/map/v2/locations/search/{}".format(
                location_id
            )
        )
        retry_client = RetryClient(
            client_session=self.websession,
            retry_options=ExponentialRetry(attempts=3, start_timeout=5),
        )
        try:
            async with retry_client.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    if result:
                        if pydantic.version.VERSION.startswith("1"):
                            location = Location.parse_obj(result[0])
                        else:
                            location = Location.model_validate(result[0])
                    else:
                        raise LocationEmptyError()
                else:
                    self.logger.exception(
                        "HTTPError %s occurred while requesting %s",
                        response.status,
                        url,
                    )
        except ValidationError as err:
            raise LocationValidationError(err)
        except (
            ClientError,
            TimeoutError,
            CancelledError,
        ) as err:
            # Something else failed
            raise err

        return location


class LocationEmptyError(Exception):
    """Raised when returned Location API data is empty."""

    pass


class LocationValidationError(Exception):
    """Raised when returned Location API data is in the wrong format."""

    pass
