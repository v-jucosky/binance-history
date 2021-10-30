# Binance: History

Este repositório contém os programas necessários para realizar o download de todos os dados históricos disponibilizados pela Binance.

_Importante: é necessário ter executado a inicialização do ambiente. Veja instruções em [binance-host](https://github.com/vjucosky/binance-host)_

Para instalar as dependências necessárias:

```shell
pip install --no-cache-dir -r requirements.txt
```

Exemplo de uso:

```shell
py main [opções] <argumentos>
```

Opções suportadas:

* `--symbol <par>`: sincronizar somente dados do par informado

Argumentos suportados:

* `kline`: sincronizar dados dos gráficos candlestick
* `trade`: sincronizar transações
* `aggtrade`: sincronizar transações agregadas

Todas as execuções são incrementais (nenhum registro será duplicado) e os arquivos são processados dentro de transações.

Ao final da primeira execução, as seguintes tabelas terão sido criadas e carregadas no banco `history` com os dados solicitados (caso nenhum par seja informado, todos os pares serão sincronizados):

* `symbol`: pares negociados
* `kline`: dados dos gráficos candlestick, em intervalos de 1 minuto
* `trade`: histórico de transações realizadas
* `aggtrade`: histórico de transações agregadas realizadas
