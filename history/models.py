from tortoise.models import Model
from tortoise import fields


class Symbol(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=20, unique=True)
    base_asset_name = fields.CharField(max_length=10)
    base_asset_precision = fields.IntField()
    quote_asset_name = fields.CharField(max_length=10)
    quote_asset_precision = fields.IntField()
    is_iceberg_allowed = fields.BooleanField()
    is_oco_allowed = fields.BooleanField()
    is_spot_trading_allowed = fields.BooleanField()
    is_margin_trading_allowed = fields.BooleanField()

    class Meta:
        unique_together = (('base_asset_name', 'quote_asset_name'), )

    def __str__(self):
        return self.name


class KLine(Model):
    id = fields.IntField(pk=True)
    symbol = fields.ForeignKeyField(model_name='models.Symbol', related_name='klines')

    trade_count = fields.IntField()
    open_value = fields.DecimalField(max_digits=18, decimal_places=8)
    high_value = fields.DecimalField(max_digits=18, decimal_places=8)
    low_value = fields.DecimalField(max_digits=18, decimal_places=8)
    close_value = fields.DecimalField(max_digits=18, decimal_places=8)
    base_asset_volume = fields.DecimalField(max_digits=18, decimal_places=8)
    base_asset_taker_buy_volume = fields.DecimalField(max_digits=18, decimal_places=8)
    quote_asset_volume = fields.DecimalField(max_digits=18, decimal_places=8)
    quote_asset_taker_buy_volume = fields.DecimalField(max_digits=18, decimal_places=8)

    open_timestamp = fields.BigIntField()
    close_timestamp = fields.BigIntField()

    class Meta:
        unique_together = (('symbol', 'open_timestamp'), )

    def __str__(self):
        return self.id


class Trade(Model):
    id = fields.IntField(pk=True)
    symbol = fields.ForeignKeyField(model_name='models.Symbol', related_name='trades')

    number = fields.IntField()
    value = fields.DecimalField(max_digits=18, decimal_places=8)
    asset_quantity = fields.DecimalField(max_digits=18, decimal_places=8)
    asset_price = fields.DecimalField(max_digits=18, decimal_places=8)
    is_buyer_maker = fields.BooleanField()
    is_best_match = fields.BooleanField()

    execution_timestamp = fields.BigIntField()

    class Meta:
        unique_together = (('symbol', 'number'), )

    def __str__(self):
        return self.id


class AggTrade(Model):
    id = fields.IntField(pk=True)
    symbol = fields.ForeignKeyField(model_name='models.Symbol', related_name='aggtrades')

    number = fields.IntField()
    first_trade_number = fields.IntField()
    last_trade_number = fields.IntField()
    asset_quantity = fields.DecimalField(max_digits=18, decimal_places=8)
    asset_price = fields.DecimalField(max_digits=18, decimal_places=8)
    is_buyer_maker = fields.BooleanField()
    is_best_match = fields.BooleanField()

    execution_timestamp = fields.BigIntField()

    class Meta:
        unique_together = (('symbol', 'number'), )

    def __str__(self):
        return self.id
