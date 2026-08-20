# Assuming DigitalWallet is imported or in the same execution scope
# from DigitalWallet import DigitalWallet

def run_tests():
    # 1. Normal Transaction & Insufficient Balance & Negative Amount
    w = DigitalWallet(pin="1234", balance=2000)
    assert w.transact("1234", 500) == "Success"
    assert w.balance == 1500
    assert w.transact("1234", 5000) == "Error: Insufficient balance"
    assert w.transact("1234", -50) == "Error: Invalid amount"

    # 2. Multiple Failed PINs (Account Lockout)
    w.transact("9999", 10)  # Fail 1
    w.transact("9999", 10)  # Fail 2
    w.transact("9999", 10)  # Fail 3 (Locks)
    assert w.transact("1234", 10) == "Locked: Too many failed PINs"

    # 3. Fraud Checks (Large Amount & High Velocity)
    w2 = DigitalWallet(pin="0000", balance=20000)
    assert w2.transact("0000", 5001) == "Flagged Fraud: Large transaction"
    
    for _ in range(5): w2.transact("0000", 10)  # 5 rapid txs
    assert w2.transact("0000", 10) == "Flagged Fraud: Too many transactions"

    # 4. Duplicate Transactions & Daily Limit Breach
    w3 = DigitalWallet(pin="1111", balance=15000)
    w3.transact("1111", 100)
    assert w3.transact("1111", 100) == "Error: Duplicate transaction detected"

    w4 = DigitalWallet(pin="1111", balance=15000)
    w4.transact("1111", 4500)
    w4.transact("1111", 4500)
    assert w4.transact("1111", 2000) == "Error: Daily limit breached"

    print("✅ All automated QA test suite assertions passed successfully!")

if __name__ == "__main__":
    run_tests()
