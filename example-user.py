from asyncio import new_event_loop
from logging import DEBUG, basicConfig, error, info
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
            cards = [card async for card in usr.get_cards()]
            chargers = [charger async for charger in usr.get_chargers()]

            info(cards[0])
            info(chargers[0])

            await usr.toggle_charger(chargers[0]["id"], cards[0]["rfid"], "start")

        except LoginFailedError:
            error("Login failed, check your credentials")


if __name__ == "__main__":
    basicConfig(stream=stdout, level=DEBUG)
    loop = new_event_loop()
    loop.run_until_complete(main())
