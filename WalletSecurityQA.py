from DigitalWallet import DigitalWallet

def run_tests():
    print("🚀 Starting QA Test Suite Execution...")

    # 1. Normal Transaction, Insufficient Balance, & Negative Amount
    w = DigitalWallet(pin="1234", balance=2000)
    assert w.transact("1234", 500) == "Success"
    assert w.balance == 1500
    assert w.transact("1234", 5000) == "Error: Insufficient balance"
    assert w.transact("1234", -50) == "Error: Invalid amount"

    # 2. Multiple Failed PINs (Account Lockout)
    w.transact("9999", 10)  # Fail 1
    w.transact("9999", 10)  # Fail 2
    w.transact("9999", 10)  # Fail 3 (Locks out)
    assert w.transact("1234", 10) == "Locked: Too many failed PINs"

    # 3. Fraud Engine: Large Transaction
    w2 = DigitalWallet(pin="0000", balance=20000)
    assert w2.transact("0000", 5001) == "Flagged Fraud: Large transaction"
    
    # 4. Fraud Engine: Velocity Limit (More than 5 tx in 10 mins)
    # Note: We vary the amounts slightly [10, 11, 12...] so we don't trigger the Duplicate check!
    for i in range(5): 
        assert w2.transact("0000", 10 + i) == "Success"  
    assert w2.transact("0000", 50) == "Flagged Fraud: Too many transactions"

    # 5. Duplicate Transaction Detection
    w3 = DigitalWallet(pin="1111", balance=15000)
    assert w3.transact("1111", 100) == "Success"
    assert w3.transact("1111", 100) == "Error: Duplicate transaction detected"

    # 6. Daily Limit Breach (Limit is 10,000)
    w4 = DigitalWallet(pin="1111", balance=15000)
    assert w4.transact("1111", 4500) == "Success"
    assert w4.transact("1111", 4600) == "Success"  # Total now: 9100
    assert w4.transact("1111", 1500) == "Error: Daily limit breached"  # 9100 + 1500 = 10600 (Breached)

    print("✅ All QA test assertions passed successfully!")

if __name__ == "__main__":
    run_tests()
