from DigitalWallet import DigitalWallet

def run_tests():
    print("--- Running Wallet Security QA Tests ---\n")
    
    # Setup Wallet
    wallet = DigitalWallet(account_id="ACC123", pin="1234", initial_balance=15000.0, daily_limit=5000.0)

    # 1. Normal transaction
    print("Test 1: Normal Transaction (Deposit & Withdrawal)")
    print(wallet.deposit(2000.0))
    print(wallet.withdraw(1000.0, "1234"))
    print()

    # 2. Insufficient balance
    print("Test 2: Insufficient Balance")
    print(wallet.withdraw(50000.0, "1234"))
    print()

    # 3. Daily limit check
    print("Test 3: Daily Limit Exceeded")
    print(wallet.withdraw(4500.0, "1234")) # Should succeed (total today: 5500? wait, limit is 5000)
    # Let's test limit properly with a fresh wallet or next withdrawal
    wallet2 = DigitalWallet(account_id="ACC456", pin="0000", initial_balance=10000.0, daily_limit=2000.0)
    print(wallet2.withdraw(2500.0, "0000"))
    print()

    # 4. Multiple failed PINs
    print("Test 4: Multiple Failed PINs")
    print(wallet.withdraw(100.0, "9999"))
    print(wallet.withdraw(100.0, "8888"))
    print(wallet.withdraw(100.0, "7777"))
    print()

    # 5. Suspicious transaction (Large Amount)
    print("Test 5: Suspicious Transaction (Large Amount)")
    print(wallet.withdraw(12000.0, "1234"))
    print()

    # 6. Duplicate transaction / Frequency check
    print("Test 6: High Frequency Fraud Check (>5 in 10 mins)")
    for i in range(6):
        res = wallet.deposit(10.0)
    print(wallet.withdraw(50.0, "1234")) # 7th action in short window should trigger frequency flag
    print()

    # 7. Negative amount
    print("Test 7: Negative Amount")
    print(wallet.deposit(-500.0))
    print()

    # 8. Concurrent transactions (Simulated sequentially in single thread)
    print("Test 8: Simulated Concurrent Transfers")
    walletA = DigitalWallet("A", "1111", 5000.0)
    walletB = DigitalWallet("B", "2222", 1000.0)
    print(walletA.transfer(walletB, 1500.0, "1111"))
    print(f"Wallet A Balance: {walletA.balance}, Wallet B Balance: {walletB.balance}")

if __name__ == "__main__":
    run_tests()
