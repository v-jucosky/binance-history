import logging
import asyncio
import getopt
import sys


from history.session import LoggedSession
from tortoise import Tortoise, run_async
from history.etl.symbol import SymbolEtl
from history.etl.kline import KLineEtl
from history.etl.trade import TradeEtl
from history.models import Symbol


async def run(symbols: list, arguments: list):
    await Tortoise.init(config_file='./history/db.json')
    await Tortoise.generate_schemas()

    tasks = []

    async with LoggedSession() as api:
        symbol_etl = SymbolEtl(api)

        await symbol_etl.run()

        if len(symbols):
            query = Symbol.filter(name__in=symbols)

            if not await query.count():
                logger.warning('Nenhum par encontrado')
                return

        else:
            query = Symbol.all()

        if 'kline' in arguments:
            kline_etl = KLineEtl(api)
            tasks.append(asyncio.create_task(kline_etl.run(query)))

        if 'trade' in arguments:
            trade_etl = TradeEtl(api)
            tasks.append(asyncio.create_task(trade_etl.run(query)))

        for task in tasks:
            await task

if __name__ == '__main__':
    logger = logging.getLogger('history')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(module)s] [%(levelname)s] %(message)s')

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
        if argument not in ('kline', 'trade'):
            logger.error(f'Comando inválido: "{argument}"')
            exit()

    run_async(run(symbols, arguments))
