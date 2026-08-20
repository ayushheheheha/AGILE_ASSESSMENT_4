import unittest
import time
from DigitalWallet import DigitalWallet

class TestWalletSecurityQA(unittest.TestCase):

    def setUp(self):
        # Fresh initialization before each test run
        self.wallet = DigitalWallet(account_id="ACC123", pin="1111", balance=10000.0, daily_limit=5000.0)
        self.peer_wallet = DigitalWallet(account_id="ACC999", pin="9999", balance=0.0)

    def test_normal_transaction(self):
        res = self.wallet.withdraw(1000, "1111")
        self.assertIn("SUCCESS", res)
        self.assertEqual(self.wallet.balance, 9000.0)

    def test_insufficient_balance(self):
        res = self.wallet.withdraw(15000, "1111")
        self.assertIn("Insufficient balance", res)

    def test_daily_limit(self):
        # Daily limit is set to 5000.0 in setup
        res = self.wallet.withdraw(6000, "1111")
        self.assertIn("Daily transaction limit exceeded", res)

    def test_multiple_failed_pins(self):
        self.wallet.verify_pin("0000")
        self.wallet.verify_pin("0000")
        res = self.wallet.withdraw(500, "0000") # 3rd structural attempt
        self.assertIn("FRAUD_DETECTED", res)
        self.assertTrue(self.wallet.is_locked)

    def test_suspicious_transaction(self):
        # Testing single extreme transaction amount check
        res = self.wallet.withdraw(150000, "1111")
        self.assertIn("FRAUD_DETECTED", res)

    def test_negative_amount(self):
        res = self.wallet.deposit(-500)
        self.assertIn("must be positive", res)
        res2 = self.wallet.withdraw(-100, "1111")
        self.assertIn("must be positive", res2)

    def test_velocity_limit_fraud(self):
        # Force high velocity frequency (5+ transactions in rapid succession)
        for _ in range(5):
            self.wallet.deposit(10)
            self.wallet.withdraw(5, "1111")
        # The 6th withdrawal should hit the velocity limits threshold tracker
        res = self.wallet.withdraw(5, "1111")
        self.assertIn("FRAUD_DETECTED", res)

if __name__ == "__main__":
    unittest.main()
