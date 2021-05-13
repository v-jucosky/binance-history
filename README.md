# Binance: History

Este repositório contém os programas necessários para realizar o download de todos os dados históricos disponibilizados pela Binance.

_Importante: é necessário ter executado a inicialização do ambiente. Veja instruções em_ [binance-host](https://github.com/vjucosky/binance-host)

Para iniciar a carga histórica, verifique o IP atribuído ao contâiner `postgres`:

```shell
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres
```

Atualize o arquivo `db.json` para apontar ao IP obtido acima. Após isso, execute:

```shell
docker compose up
```

Ao final da execução, as seguintes tabelas terão sido criadas e carregadas no banco `history`:

* `symbol`: pares negociados
* `kline`: dados dos gráficos candlestick, em intervalos de 1 minuto
* `trade`: histórico de transações realizadas
