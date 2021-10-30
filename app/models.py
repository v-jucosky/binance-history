from tortoise.fields import ForeignKeyField, CharField, IntField, BigIntField, DecimalField, BooleanField
from tortoise.models import Model


class Symbol(Model):
    id = IntField(pk=True)

    name = CharField(max_length=20, unique=True)
    base_asset_name = CharField(max_length=10)
    base_asset_precision = IntField()
    quote_asset_name = CharField(max_length=10)
    quote_asset_precision = IntField()
    is_iceberg_allowed = BooleanField()
    is_oco_allowed = BooleanField()
    is_spot_trading_allowed = BooleanField()
    is_margin_trading_allowed = BooleanField()

    class Meta:
        unique_together = (('base_asset_name', 'quote_asset_name'), )

    def __str__(self):
        '''Representação do objeto.'''

        return self.name


class KLine(Model):
    id = IntField(pk=True)
    symbol = ForeignKeyField(model_name='models.Symbol', related_name='klines')

    trade_count = IntField()
    open_value = DecimalField(max_digits=18, decimal_places=8)
    high_value = DecimalField(max_digits=18, decimal_places=8)
    low_value = DecimalField(max_digits=18, decimal_places=8)
    close_value = DecimalField(max_digits=18, decimal_places=8)
    base_asset_volume = DecimalField(max_digits=18, decimal_places=8)
    base_asset_taker_buy_volume = DecimalField(max_digits=18, decimal_places=8)
    quote_asset_volume = DecimalField(max_digits=18, decimal_places=8)
    quote_asset_taker_buy_volume = DecimalField(max_digits=18, decimal_places=8)

    open_timestamp = BigIntField()
    close_timestamp = BigIntField()

    class Meta:
        unique_together = (('symbol', 'open_timestamp'), )

    def __str__(self):
        '''Representação do objeto.'''

        return self.id


class Trade(Model):
    id = IntField(pk=True)
    symbol = ForeignKeyField(model_name='models.Symbol', related_name='trades')

    number = IntField()
    value = DecimalField(max_digits=18, decimal_places=8)
    asset_quantity = DecimalField(max_digits=18, decimal_places=8)
    asset_price = DecimalField(max_digits=18, decimal_places=8)
    is_buyer_maker = BooleanField()
    is_best_match = BooleanField()

    execution_timestamp = BigIntField()

    class Meta:
        unique_together = (('symbol', 'number'), )

    def __str__(self):
        '''Representação do objeto.'''

        return self.id


class AggTrade(Model):
    id = IntField(pk=True)
    symbol = ForeignKeyField(model_name='models.Symbol', related_name='aggtrades')

    number = IntField()
    first_trade_number = IntField()
    last_trade_number = IntField()
    asset_quantity = DecimalField(max_digits=18, decimal_places=8)
    asset_price = DecimalField(max_digits=18, decimal_places=8)
    is_buyer_maker = BooleanField()
    is_best_match = BooleanField()

    execution_timestamp = BigIntField()

    class Meta:
        unique_together = (('symbol', 'number'), )

    def __str__(self):
        '''Representação do objeto.'''

        return self.id
