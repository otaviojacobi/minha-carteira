import unittest
from unittest.mock import MagicMock, patch

from common.wallet import Wallet


class TestWallet(unittest.TestCase):

    def test_wallet_creation(self):
        wallet = Wallet([{'wege3': 10}, {'WEGE3': 3}])
        self.assertDictEqual(wallet.get_content(), {'WEGE3': 13})

    @patch('common.wallet.Bovespa')
    def test_wallet_value(self, bovespa_mock):

        bov_mock = MagicMock()
        bov_mock.get_current_multiple_stock_prices.return_value = [(10, 'WEGE3'), (20, 'VALE3')]
        bovespa_mock.return_value = bov_mock

        wallet = Wallet([{'wege3': 10}, {'WEGE3': 3}, {'VALE3': 5}])
        self.assertEqual(wallet.value(), 230)
