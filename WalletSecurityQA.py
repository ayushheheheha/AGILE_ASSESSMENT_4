from DigitalWallet import DigitalWallet

def run_security_tests():
    print("=== STARTING AUTOMATED QA WALLET SECURITY TESTS ===\n")

    # 1. Test Normal Transaction
    w1 = DigitalWallet("ACC1", "1111", balance=5000.0)
    print(f"Test 1 (Normal Withdraw): {w1.withdraw(1000, '1111')}")

    # 2. Test Insufficient Balance
    w2 = DigitalWallet("ACC2", "2222", balance=100.0)
    print(f"Test 2 (Low Balance): {w2.withdraw(500, '2222')}")

    # 3. Test Daily Limit
    w3 = DigitalWallet("ACC3", "3333", balance=20000.0, daily_limit=2000.0)
    print(f"Test 3 (Daily Limit Exceeded): {w3.withdraw(3000, '3333')}")

    # 4. Test Multiple Failed PINs
    w4 = DigitalWallet("ACC4", "4444", balance=1000.0)
    w4.withdraw(100, "9999") # Fail 1
    w4.withdraw(100, "8888") # Fail 2
    print(f"Test 4 (Failed PINs/Lock): {w4.withdraw(100, '7777')}")

    # 5. Test Suspicious / Large Transaction
    w5 = DigitalWallet("ACC5", "5555", balance=200000.0)
    print(f"Test 5 (Suspicious Size): {w5.withdraw(150000, '5555')}")

    # 6. Test Negative Amount
    w6 = DigitalWallet("ACC6", "6666", balance=1000.0)
    print(f"Test 6 (Negative Deposit): {w6.deposit(-50)}")

    # 7. Test Velocity Limit (More than 5 transactions)
    w7 = DigitalWallet("ACC7", "7777", balance=1000.0)
    for _ in range(5):
        w7.withdraw(10, "7777") # Create 5 fast transactions
    print(f"Test 7 (Velocity Fraud): {w7.withdraw(10, '7777')}")

    # 8. Test Concurrent/Transfer Transactions
    sender = DigitalWallet("SENDER", "1234", balance=500.0)
    receiver = DigitalWallet("RECEIVER", "5678", balance=0.0)
    print(f"Test 8 (Transfer): {sender.transfer(receiver, 200, '1234')}")
    print(f"Receiver Final Balance: ${receiver.balance}")

if __name__ == "__main__":
    run_security_tests()
