from tortoise.transactions import atomic
from history.etl.base import BaseEtl
from history.models import Symbol


class SymbolEtl(BaseEtl):
    @atomic()
    async def run(self):
        async with self.api.get('https://api.binance.com/api/v3/exchangeInfo') as response:
            data = await response.json()

        for symbol in data['symbols']:
            await Symbol.update_or_create(name=symbol['symbol'], defaults={
                'base_asset': symbol['baseAsset'],
                'base_asset_precision': symbol['baseAssetPrecision'],
                'quote_asset': symbol['quoteAsset'],
                'quote_asset_precision': symbol['quoteAssetPrecision'],
                'iceberg_allowed': symbol['icebergAllowed'],
                'oco_allowed': symbol['ocoAllowed'],
                'spot_trading_allowed': symbol['isSpotTradingAllowed'],
                'margin_trading_allowed': symbol['isMarginTradingAllowed']
            })
