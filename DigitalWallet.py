from datetime import datetime, timedelta

class DigitalWallet:
    def __init__(self, account_id, pin, initial_balance=0.0, daily_limit=5000.0):
        self.account_id = account_id
        self.pin = pin
        self.balance = initial_balance
        self.daily_limit = daily_limit
        self.transactions = []
        self.failed_pin_attempts = 0

    def verify_pin(self, entered_pin):
        if entered_pin == self.pin:
            self.failed_pin_attempts = 0
            return True
        else:
            self.failed_pin_attempts += 1
            return False

    def deposit(self, amount):
        if amount <= 0:
            return "Error: Amount must be positive."
        self.balance += amount
        self._log_transaction("DEPOSIT", amount)
        return f"Success: Deposited {amount}. New Balance: {self.balance}"

    def withdraw(self, amount, pin):
        if not self.verify_pin(pin):
            if self.failed_pin_attempts >= 3:
                return "Alert: Account locked due to multiple failed PIN attempts!"
            return "Error: Invalid PIN."
        
        if amount <= 0:
            return "Error: Amount must be positive."
        if amount > self.balance:
            return "Error: Insufficient balance."
        if self._check_daily_limit(amount):
            return "Error: Daily transaction limit exceeded."
        
        # Fraud Detection Check
        is_suspicious, reason = self._detect_fraud(amount)
        
        self.balance -= amount
        self._log_transaction("WITHDRAWAL", amount, is_suspicious, reason)
        
        if is_suspicious:
            return f"Warning: Withdrawal successful, but flagged for fraud ({reason})."
        return f"Success: Withdrew {amount}. New Balance: {self.balance}"

    def transfer(self, recipient_wallet, amount, pin):
        if not self.verify_pin(pin):
            return "Error: Invalid PIN."
        if amount <= 0:
            return "Error: Amount must be positive."
        if amount > self.balance:
            return "Error: Insufficient balance."
        
        is_suspicious, reason = self._detect_fraud(amount)
        
        self.balance -= amount
        recipient_wallet.balance += amount
        
        self._log_transaction("TRANSFER", amount, is_suspicious, reason)
        return f"Success: Transferred {amount} to {recipient_wallet.account_id}."

    def _check_daily_limit(self, amount):
        today = datetime.now().date()
        todays_total = sum(
            t['amount'] for t in self.transactions 
            if t['timestamp'].date() == today and t['type'] in ['WITHDRAWAL', 'TRANSFER']
        )
        return (todays_total + amount) > self.daily_limit

    def _detect_fraud(self, amount):
        now = datetime.now()
        
        # 1. More than 5 transactions in 10 minutes
        recent_txs = [t for t in self.transactions if now - t['timestamp'] <= timedelta(minutes=10)]
        if len(recent_txs) >= 5:
            return True, "High frequency of transactions (>5 in 10 mins)"
        
        # 2. Large transaction (e.g., > 10,000)
        if amount > 10000:
            return True, "Unusually large transaction amount"
            
        # 3. Unusual transaction amount (e.g., repeating weird patterns or decimals, simplified here as negative/zero handled elsewhere)
        if amount == 999.99: 
            return True, "Unusual transaction amount pattern"

        return False, None

    def _log_transaction(self, tx_type, amount, is_suspicious=False, fraud_reason=None):
        self.transactions.append({
            'type': tx_type,
            'amount': amount,
            'timestamp': datetime.now(),
            'suspicious': is_suspicious,
            'reason': fraud_reason
        })
