from collections import defaultdict
from copy import deepcopy

from common.bovespa import Bovespa


class Wallet:
    def __init__(self, unormalized_wallet=[]):
        self._wallet = self.normalize_wallet(unormalized_wallet)
        self._b3 = Bovespa()

    def value(self):

        if len(self._wallet.keys()) == 0:
            stocks_price = []
        elif len(self._wallet.keys()) == 1:
            stocks_price = [self._b3.get_current_stock_price(self._wallet.keys()[0])]
        else:
            stocks_price = self._b3.get_current_multiple_stock_prices(list(self._wallet.keys()))

        value = 0
        for price, stock in stocks_price:
            value += price * self._wallet[stock]

        return value

    def get_content(self):
        return deepcopy(dict(self._wallet))

    @staticmethod
    def normalize_wallet(unormalized_wallet):

        normalized_wallet = defaultdict(lambda: 0)
        for element in unormalized_wallet:
            key = list(element.keys())[0]
            value = element[key]
            normalized_wallet[key.upper()] += value

        return normalized_wallet
