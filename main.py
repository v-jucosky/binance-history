import logging
import asyncio
import getopt
import sys


from tortoise import Tortoise, run_async
from app.etl.aggtrade import AggTradeEtl
from app.session import LoggedSession
from app.etl.symbol import SymbolEtl
from app.etl.kline import KLineEtl
from app.etl.trade import TradeEtl
from app.models import Symbol


async def run(symbols: list, arguments: list):
    await Tortoise.init(config_file='./app/db.json')
    await Tortoise.generate_schemas()

    tasks = []

    async with LoggedSession() as api:
        symbol_etl = SymbolEtl(api)

        await symbol_etl.run()

        if len(symbols):
            query = Symbol.filter(name__in=symbols)

            if not await query.count():
                logger.warning('No pair found')
                return

        else:
            query = Symbol.all()

        if 'kline' in arguments:
            kline_etl = KLineEtl(api)
            tasks.append(asyncio.create_task(kline_etl.run(query)))

        if 'trade' in arguments:
            trade_etl = TradeEtl(api)
            tasks.append(asyncio.create_task(trade_etl.run(query)))

        if 'aggtrade' in arguments:
            aggtrade_etl = AggTradeEtl(api)
            tasks.append(asyncio.create_task(aggtrade_etl.run(query)))

        for task in tasks:
            await task

if __name__ == '__main__':
    logger = logging.getLogger('app')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(module)s) %(message)s')

    logger.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    symbols = []
    argv = sys.argv[1:]
    options, arguments = getopt.getopt(argv, None, ['symbol=', ])

    for option, argument in options:
        if option in ('--symbol', ):
            symbols.append(argument.upper())

    for argument in arguments:
        if argument not in ('kline', 'trade', 'aggtrade'):
            logger.error(f'Invalid command: "{argument}"')
            exit()

    run_async(run(symbols, arguments))
