import logging
import asyncio


from history.session import LoggedSession
from tortoise import Tortoise, run_async
from history.etl.symbol import SymbolEtl
from history.etl.kline import KLineEtl
from history.etl.trade import TradeEtl


async def run():
    logger = logging.getLogger('history')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    logger.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    await Tortoise.init(config_file='./history/db.json')
    await Tortoise.generate_schemas()    

    api = LoggedSession()

    symbol_etl = SymbolEtl(api)
    kline_etl = KLineEtl(api)
    trade_etl = TradeEtl(api)

    await symbol_etl.run()

    kline_task = asyncio.create_task(kline_etl.run())
    trade_task = asyncio.create_task(trade_etl.run())

    await kline_task
    await trade_task

if __name__ == '__main__':
    run_async(run())
