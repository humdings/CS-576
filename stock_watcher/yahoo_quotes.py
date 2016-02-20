from urllib2 import Request, urlopen

PRICE_QUOTE_FIELDS = {
    'ask': 'a',
    'bid': 'b',
    'last_trade': 'l1',
    'volume': 'v'
}

FUNDAMENTAL_QUOTE_FILEDS = {
    'price': 'l1',
    'avg_daily_volume': 'a2',
    'market_cap': 'j1',
    'book_value': 'b4',
    'ebitda': 'j4',
    'dividend_per_share': 'd',
    'dividend_yield': 'y',
    'earnings_per_share': 'e',
    'fifty_two_week_high': 'k',
    'fifty_two_week_low': 'j',
    'fifty_day_moving_avg': 'm3',
    'two_hundred_day_moving_avg': 'm4',
    'price_earnings_ratio': 'r',
    'price_earnings_growth_ratio': 'r5',
    'price_sales_ratio': 'p5',
    'price_book_ratio': 'p6',
    'short_ratio': 's7',
    'revenue': 's6',
    'one_yr_target_price': 't8',
    'shares_outstanding': 'j2'
}


def yahoo_quotes(symbols, mappings):
    """
    Args:
        symbols: list of ticker symbols, (length <= 50, yahoo limit)
        mappings: dict of (name, yahoo id) pairs.
        For url codes see
        https://code.google.com/p/yahoo-finance-managed/wiki/enumQuoteProperty


    Returns: List of quotes
                index: quote type
                columns: symbols

    """
    url = "http://download.finance.yahoo.com/d/quotes.csv?s={}&f={}"
    url = url.format(",".join(symbols), "".join(mappings.itervalues()))
    request = Request(url)
    response = urlopen(request)
    quotes = str(response.read().decode('utf-8').strip())
    rows = (i.replace('"', "") for i in quotes.split('\n'))
    rows = (dict(zip(mappings.keys(), i.split(','))) for i in rows)
    rows = dict(zip(symbols, rows))
    for symbol, row in rows.iteritems():
        for key, value in row.iteritems():
            try:
                rows[symbol][key] = float(value)
            except ValueError:
                pass
    return rows
