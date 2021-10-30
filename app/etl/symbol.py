from tortoise.transactions import atomic
from app.etl.base import BaseEtl
from app.models import Symbol


class SymbolEtl(BaseEtl):
    @atomic()
    async def run(self):
        '''Rotina de execução principal.'''

        async with self.api.get('https://api.binance.com/api/v3/exchangeInfo') as response:
            data = await response.json()

        for symbol in data['symbols']:
            await Symbol.update_or_create(name=symbol['symbol'], defaults={
                'base_asset_name': symbol['baseAsset'],
                'base_asset_precision': symbol['baseAssetPrecision'],
                'quote_asset_name': symbol['quoteAsset'],
                'quote_asset_precision': symbol['quoteAssetPrecision'],
                'is_iceberg_allowed': symbol['icebergAllowed'],
                'is_oco_allowed': symbol['ocoAllowed'],
                'is_spot_trading_allowed': symbol['isSpotTradingAllowed'],
                'is_margin_trading_allowed': symbol['isMarginTradingAllowed']
            })

        self.logger.info('Symbol sync complete')
