import time

class DigitalWallet:
    def __init__(self, account_id, pin, balance=0.0, daily_limit=50000.0):
        self.account_id = account_id
        self.pin = pin
        self.balance = balance
        self.daily_limit = daily_limit
        self.daily_spent = 0.0
        self.transactions = []  # Stores tuples of (timestamp, amount, type)
        self.failed_pin_attempts = 0
        self.is_locked = False

    def verify_pin(self, input_pin):
        if self.is_locked:
            return False
        if input_pin == self.pin:
            self.failed_pin_attempts = 0
            return True
        else:
            self.failed_pin_attempts += 1
            if self.failed_pin_attempts >= 3:
                self.is_locked = True
            return False

    def check_fraud(self, amount, pin_verified):
        # 1. Multiple failed PIN attempts
        if self.is_locked or self.failed_pin_attempts >= 3:
            return "FRAUD_DETECTED: Account locked due to multiple failed PIN attempts."
        
        if not pin_verified:
            return "REJECTED: Invalid PIN."

        # 2. More than 5 transactions in 10 minutes (600 seconds)
        current_time = time.time()
        recent_txs = [tx for tx in self.transactions if current_time - tx[0] <= 600]
        if len(recent_txs) >= 5:
            return "FRAUD_DETECTED: High transaction frequency (Velocity limit reached)."

        # 3. Large transaction or unusual transaction amount
        if amount > 100000.0:
            return "FRAUD_DETECTED: Single transaction exceeds maximum allowable risk limit."

        return "SAFE"

    def deposit(self, amount):
        if amount <= 0:
            return "ERROR: Deposit amount must be positive."
        self.balance += amount
        self.transactions.append((time.time(), amount, "DEPOSIT"))
        return f"SUCCESS: Deposited {amount}. New Balance: {self.balance}"

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
            return "ERROR: Daily transaction limit exceeded."

        self.balance -= amount
        self.daily_spent += amount
        self.transactions.append((time.time(), amount, "WITHDRAWAL"))
        return f"SUCCESS: Withdrew {amount}. Remaining Balance: {self.balance}"

    def transfer(self, target_wallet, amount, input_pin):
        pin_ok = self.verify_pin(input_pin)
        fraud_status = self.check_fraud(amount, pin_ok)
        if fraud_status != "SAFE":
            return fraud_status

        if amount <= 0:
            return "ERROR: Amount must be positive."
        if amount > self.balance:
            return "ERROR: Insufficient balance."
        if self.daily_spent + amount > self.daily_limit:
            return "ERROR: Daily transaction limit exceeded."

        self.balance -= amount
        self.daily_spent += amount
        target_wallet.balance += amount
        
        self.transactions.append((time.time(), amount, f"TRANSFER_TO_{target_wallet.account_id}"))
        target_wallet.transactions.append((time.time(), amount, f"TRANSFER_FROM_{self.account_id}"))
        return f"SUCCESS: Transferred {amount} to {target_wallet.account_id}."
