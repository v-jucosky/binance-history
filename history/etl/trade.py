import aiofiles


from tortoise.transactions import atomic
from history.models import Symbol, Trade
from tortoise.queryset import QuerySet
from history.etl.base import BaseEtl
from zipfile import ZipFile
from pathlib import Path
from aiofiles import os


class TradeEtl(BaseEtl):
    @atomic()
    async def _load_file(self, file: Path, symbol: Symbol):
        trades = []

        async with aiofiles.open(file, 'r', encoding='UTF-8') as file:
            content = await file.read()

        for row in content.splitlines():
            data = row.split(',')

            trades.append(
                Trade(
                    symbol=symbol,
                    number=data[0],
                    value=data[3],
                    asset_quantity=data[2],
                    asset_price=data[1],
                    is_buyer_maker=data[5],
                    is_best_match=data[6],
                    trade_timestamp=data[4]
                )
            )

        await Trade.bulk_create(trades, 10000)

    async def run(self, symbols: QuerySet):
        async for symbol in symbols.all():
            last_trade = await Trade.filter(symbol=symbol).order_by('-trade_timestamp').first()

            if last_trade:
                last_period = self.get_date_object(last_trade.trade_timestamp)
                periods = self.generate_periods(last_period)
            else:
                periods = self.generate_periods()

            for period in periods:
                file = f'{symbol.name}-trades-{period.year}-{period.month:02d}'

                if await self.download_file(f'https://data.binance.vision/data/spot/monthly/trades/{symbol.name}/{file}.zip'):
                    with ZipFile(f'./stage/{file}.zip', 'r') as zipfile:
                        zipfile.extract(f'{file}.csv', './stage')

                    await self._load_file(f'./stage/{file}.csv', symbol)

                    await os.remove(f'./stage/{file}.zip')
                    await os.remove(f'./stage/{file}.csv')

        self.logger.info('Sincronização das transações concluída')
