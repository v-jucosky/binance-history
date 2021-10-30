import aiofiles
import logging


from datetime import datetime, date, timedelta
from app.session import LoggedSession
from aiohttp.typedefs import StrOrURL
from calendar import monthrange
from pathlib import Path


class BaseEtl():
    def __init__(self, api: LoggedSession):
        '''
        Base com funções comuns e auxiliares aos ETLs.

        Parâmetros
        ----------
        api: seção de comunicação com a Binance
        '''

        self.api = api
        self.logger = logging.getLogger(__name__)

    def get_date_object(self, timestamp: int):
        '''
        Retorna um objeto Datetime para o timestamp Binance fornecido.

        Parâmetros
        ----------
        timestamp: milisegundos desde o Epoch
        '''

        return datetime.fromtimestamp(timestamp / 1000).date()

    def generate_periods(self, last_period: date=None):
        '''
        Gera uma lista com todos os períodos entre o período informado (não incluso) e a data de hoje.

        Parâmetros
        ----------
        last_period: período a utilizar como ponto de partida para a criação da lista de períodos;
            utilizará dezembro de 2016 caso não seja fornecido
        '''

        today = date.today()

        if last_period:
            last_period = date(last_period.year, last_period.month, 1)
        else:
            last_period = date(2016, 12, 1)

        periods = [last_period, ]

        while True:
            period = periods[-1] + timedelta(days=monthrange(periods[-1].year, periods[-1].month)[1])

            if date(today.year, today.month, 1) > period:
                periods.append(period)
            else:
                break

        return periods[1:]

    async def download_file(self, str_or_url: StrOrURL):
        '''
        Realiza o download do arquivo Binance especificado, deixando o arquivo na pasta de transferências.
        Retorna True caso a operação seja bem sucedida ou False caso ocorra algum erro.

        Parâmetros
        ----------
        str_or_url: URL do arquivo em formato texto ou objeto URL
        '''

        destination = Path(f'./stage/{str_or_url.rsplit("/", 1)[-1]}')

        async with self.api.get(str_or_url) as response:
            if response.status == 200:
                async with aiofiles.open(destination, 'wb') as file:
                    await file.write(await response.read())
                
                return True

        return False
