from asyncio import new_event_loop
from logging import basicConfig, DEBUG, error
from os import getenv
from sys import stdout

from aiohttp import ClientSession
from shellrecharge import Api
from shellrecharge.user import LoginFailedError

async def main():
    async with ClientSession() as session:
        try:
            api = Api(session)
            usr = await api.get_user(getenv("SHELL_USER"), getenv("SHELL_PWD"))
            [print(card) async for card in usr.get_cards()]
            [print(charger) async for charger in usr.get_chargers()]
        except LoginFailedError:
            error("Login failed, check your credentials")


if __name__ == "__main__":
    basicConfig(stream=stdout, level=DEBUG)
    loop = new_event_loop()
    loop.run_until_complete(main())