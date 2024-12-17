from logging import getLogger
from re import compile, search
from typing import AsyncGenerator, Literal

import pydantic
from aiohttp import ClientResponse, ClientSession
from bs4 import BeautifulSoup
from bs4.element import Tag
from pydantic import ValidationError

from .decorators import retry_on_401
from .usermodels import Assets, ChargeToken, DetailedChargePoint


class User:
    """Class bundling all user requests"""

    accountUrl = "https://account.shellrecharge.com"
    assetUrl = "https://ui-chargepoints.shellrecharge.com"
    userAgent = "Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0"

    def __init__(self, email: str, pwd: str, session: ClientSession):
        """Initialize user"""
        self.logger = getLogger("user")
        self.session = session
        self.__email = email
        self.__pwd = pwd

    async def authenticate(self) -> None:
        """Authenticate using email and password and retrieve an api key"""
        headers = {"User-Agent": self.userAgent}
        async with self.session.get(self.accountUrl, headers=headers) as r:
            page = await r.text()

        # Make soup
        soup = BeautifulSoup(page, "html.parser")

        # Find field values
        login_email = soup.find("input", attrs={"id": "login-email"})
        if type(login_email) is not Tag:
            raise ShellPageChangedError()
        login_pwd = soup.find(attrs={"id": "login-pwd"})
        if type(login_pwd) is not Tag:
            raise ShellPageChangedError()
        login_hidden = soup.find("input", {"type": "hidden"})
        if type(login_hidden) is not Tag:
            raise ShellPageChangedError()

        # Find the var declaration for lift_page
        script_text = soup.find("script", string=compile(r"var\s+lift_page\s*=\s*"))
        if type(script_text) is not Tag:
            raise ShellPageChangedError()
        lift_page_match = search(
            r'var\s+lift_page\s*=\s*["\']([^"\']+)["\'];',
            script_text.string or "",
        )
        if not lift_page_match:
            raise ShellPageChangedError()
        lift_page = lift_page_match.group(1)

        form_data = {
            login_email.get("name"): self.__email,
            login_pwd.get("name"): self.__pwd,
            login_hidden.get("name"): True,
        }

        async with self.session.post(
            f"{self.accountUrl}/ajax_request/{lift_page}-00",
            headers=headers,
            data=form_data,
        ) as key:
            cookie = key.cookies.get("tnm_api")
            if not cookie:
                raise LoginFailedError()
            self.cookies = {"tnm_api": cookie.value}

    @retry_on_401
    async def __get_request(self, url: str) -> ClientResponse:
        """Get request that reauthenticates when getting a 401"""
        return await self.session.get(url, cookies=self.cookies)

    @retry_on_401
    async def __post_request(
        self, url: str, headers: dict, data: str
    ) -> ClientResponse:
        """Post request that reauthenticates when getting a 401"""
        return await self.session.post(
            url, headers=headers, cookies=self.cookies, data=data
        )

    async def get_cards(self) -> AsyncGenerator[ChargeToken, None]:
        """Get the user's charging cards"""
        async with await self.__get_request(
            f"{self.assetUrl}/api/facade/v1/me/asset-overview"
        ) as response:
            assets = await response.json()

        if not assets:
            raise AssetsEmptyError()

        try:
            if pydantic.version.VERSION.startswith("1"):
                Assets.parse_obj(assets)
            else:
                Assets.model_validate(assets)
        except ValidationError as err:
            raise AssetsValidationError(err)

        for token in assets["chargeTokens"]:
            yield token

    async def get_chargers(self) -> AsyncGenerator[DetailedChargePoint, None]:
        """Get the user's private charge points"""
        async with await self.__get_request(
            f"{self.assetUrl}/api/facade/v1/me/asset-overview"
        ) as response:
            assets = await response.json()

        if not assets:
            raise AssetsEmptyError()

        try:
            if pydantic.version.VERSION.startswith("1"):
                Assets.parse_obj(assets)
            else:
                Assets.model_validate(assets)
        except ValidationError as err:
            raise AssetsValidationError(err)

        for charger in assets["chargePoints"]:
            async with await self.__get_request(
                f"{self.assetUrl}/api/facade/v1/charge-points/{charger['uuid']}"
            ) as r:
                details = await r.json()

                if not details:
                    raise DetailedChargePointEmptyError()

                try:
                    if pydantic.version.VERSION.startswith("1"):
                        DetailedChargePoint.parse_obj(details)
                    else:
                        DetailedChargePoint.model_validate(details)
                except ValidationError as err:
                    raise DetailedChargePointValidationError(err)

                yield details

    async def toggle_charger(
        self,
        charger_id: str,
        card_rfid: str,
        action: Literal["start", "stop"] = "start",
    ) -> bool:
        body = f'{{"rfid":"{card_rfid}","evseNo":0}}'
        headers = {"Accept": "text/html", "Content-Type": "application/json"}
        async with await self.__post_request(
            f"{self.assetUrl}/api/facade/v1/charge-points/{charger_id}/remote-control/{action}",
            headers=headers,
            data=body,
        ) as r:
            return 202 == r.status


class ShellPageChangedError(Exception):
    """Raised when Shell changes their website breaking the scraping."""

    pass


class LoginFailedError(Exception):
    """Raised when login failed"""

    pass


class AssetsEmptyError(Exception):
    """Raised when returned assets data is empty."""

    pass


class DetailedChargePointEmptyError(Exception):
    """Raised when returned charge point details are empty."""

    pass


class AssetsValidationError(Exception):
    """Raised when returned assets are in the wrong format."""

    pass


class DetailedChargePointValidationError(Exception):
    """Raised when returned charge point details are in the wrong format."""

    pass
