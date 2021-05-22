import aiofiles


from history.models import Symbol, AggTrade
from tortoise.transactions import atomic
from tortoise.queryset import QuerySet
from history.etl.base import BaseEtl
from zipfile import ZipFile
from pathlib import Path
from aiofiles import os


class AggTradeEtl(BaseEtl):
    @atomic()
    async def _load_file(self, file: Path, symbol: Symbol):
        aggtrades = []

        async with aiofiles.open(file, 'r', encoding='UTF-8') as file:
            content = await file.read()

        for row in content.splitlines():
            data = row.split(',')

            aggtrades.append(
                AggTrade(
                    symbol=symbol,
                    number=data[0],
                    first_trade_number=data[3],
                    last_trade_number=data[4],
                    asset_quantity=data[2],
                    asset_price=data[1],
                    is_buyer_maker=data[6],
                    is_best_match=data[7],
                    execution_timestamp=data[5]
                )
            )

        await AggTrade.bulk_create(aggtrades, 10000)

    async def run(self, symbols: QuerySet):
        async for symbol in symbols.all():
            last_aggtrade = await AggTrade.filter(symbol=symbol).order_by('-execution_timestamp').first()

            if last_aggtrade:
                last_period = self.get_date_object(last_aggtrade.execution_timestamp)
                periods = self.generate_periods(last_period)
            else:
                periods = self.generate_periods()

            for period in periods:
                file = f'{symbol.name}-aggTrades-{period.year}-{period.month:02d}'

                if await self.download_file(f'https://data.binance.vision/data/spot/monthly/aggTrades/{symbol.name}/{file}.zip'):
                    with ZipFile(f'./stage/{file}.zip', 'r') as zipfile:
                        zipfile.extract(f'{file}.csv', './stage')

                    await self._load_file(f'./stage/{file}.csv', symbol)

                    await os.remove(f'./stage/{file}.zip')
                    await os.remove(f'./stage/{file}.csv')

        self.logger.info('Sincronização das transações agregadas concluída')
