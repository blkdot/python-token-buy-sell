#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests


def run_query(query):  # A simple function to use requests.post to make the API call.
    headers = {'X-API-KEY': 'BQY41mDV60sSrVDgrV7O6DozccIeoN9d'}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,
                        query))


# The GraphQL query

query = """
{
  ethereum(network: bsc) {
    dexTrades(
    options: {desc: "block.timestamp.time", limit: <N>}
    baseCurrency: {is: "<CONTRACT>"}
    quoteCurrency: {is: "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"}
    ) {
    block {
      timestamp {
        time(format: "%Y-%m-%d %H:%M:%S")
      }
    }
    transaction {
      hash
    }
    tradeAmount(in: USD)
      side
    }
  }
}
"""

while True:
  try:
    result = run_query(query)  # Execute the query
    #print('Result - {}'.format(result))
    numrecords = len(result['data']['ethereum']['dexTrades'])
    result = result['data']['ethereum']['dexTrades']
    amount_buy = 0
    amount_sell = 0
    for x in range(numrecords) :
      # print(result[x]['block']['timestamp']['time'] + ' ' + result[x]['transaction']['hash'] + ' ' + result[x]['side'] + ' ' + str(result[x]['tradeAmount']) + 'USD')
      if result[x]['side'] == 'BUY':
        amount_buy += result[x]['tradeAmount']
      if result[x]['side'] == 'SELL':
        amount_sell += result[x]['tradeAmount']
    prc_buy = amount_buy / (amount_buy + amount_sell)
    print(str(prc_buy) + '%')
  except:
    print('query error')


