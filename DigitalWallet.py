import time

class DigitalWallet:
    def __init__(self, account_id, pin, balance=0.0, daily_limit=50000.0):
        self.account_id = account_id
        self.pin = pin
        self.balance = balance
        self.daily_limit = daily_limit
        self.daily_spent = 0.0
        self.transactions = []  # Stores timestamps
        self.failed_pin_attempts = 0
        self.is_locked = False

    def verify_pin(self, input_pin):
        if self.is_locked:
            return False
        if input_pin == self.pin:
            self.failed_pin_attempts = 0
            return True
        self.failed_pin_attempts += 1
        if self.failed_pin_attempts >= 3:
            self.is_locked = True
        return False

    def check_fraud(self, amount, pin_verified):
        if self.is_locked:
            return "FLAGGED: Account locked due to multiple failed PINs!"
        if not pin_verified:
            return "FLAGGED: Invalid PIN details!"
        if len(self.transactions) >= 5:
            return "FLAGGED: More than 5 transactions in 10 minutes!"
        if amount > 100000.0:
            return "FLAGGED: Unusual / Too large transaction amount!"
        return "SAFE"

    def deposit(self, amount):
        if amount <= 0:
            return "ERROR: Deposit must be positive."
        self.balance += amount
        return f"Deposited ${amount}. Balance: ${self.balance}"

    def withdraw(self, amount, input_pin):
        pin_ok = self.verify_pin(input_pin)
        fraud_status = self.check_fraud(amount, pin_ok)
        if fraud_status != "SAFE":
            return fraud_status

        if amount <= 0:
            return "ERROR: Amount must be positive."
        if amount > self.balance:
            return "ERROR: Insufficient balance."
        if self.daily_spent + amount > self.daily_limit:
            return "ERROR: Daily limit exceeded."

        self.balance -= amount
        self.daily_spent += amount
        self.transactions.append(time.time())
        return f"Withdrew ${amount}. Remaining Balance: ${self.balance}"

    def transfer(self, target_wallet, amount, input_pin):
        pin_ok = self.verify_pin(input_pin)
        fraud_status = self.check_fraud(amount, pin_ok)
        if fraud_status != "SAFE":
            return fraud_status

        if amount > self.balance:
            return "ERROR: Insufficient balance."
            
        self.balance -= amount
        target_wallet.balance += amount
        self.transactions.append(time.time())
        return f"Transferred ${amount} to {target_wallet.account_id}."
