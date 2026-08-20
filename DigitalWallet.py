import datetime

class DigitalWallet:
    def __init__(self, pin, balance=1000):
        self.pin, self.balance, self.history, self.fails = pin, balance, [], 0

    def transact(self, pin, amount, tx_type="Withdrawal"):
        now = datetime.datetime.now()
        if amount <= 0: return "Error: Invalid amount"
        if self.fails >= 3: return "Locked: Too many failed PINs"
        if pin != self.pin:
            self.fails += 1
            return "Error: Invalid PIN"
        self.fails = 0

        # Fraud Engine
        recent = sum(1 for t in self.history if (now - t['time']).total_seconds() < 600)
        if recent >= 5: return "Flagged Fraud: Too many transactions"
        if amount > 5000: return "Flagged Fraud: Large transaction"

        # Limits & Duplicates
        daily = sum(t['amt'] for t in self.history if t['time'].date() == now.date() and t['type'] == "Withdrawal")
        if daily + amount > 10000: return "Error: Daily limit breached"
        if tx_type == "Withdrawal" and amount > self.balance: return "Error: Insufficient balance"
        if self.history and self.history[-1]['amt'] == amount and (now - self.history[-1]['time']).total_seconds() < 2:
            return "Error: Duplicate transaction detected"

        # Execute
        if tx_type == "Withdrawal": self.balance -= amount
        else: self.balance += amount
        self.history.append({'time': now, 'type': tx_type, 'amt': amount})
        return "Success"
