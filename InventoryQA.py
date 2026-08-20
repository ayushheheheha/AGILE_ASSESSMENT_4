from InventoryManagement import InventorySystem

def run_tests():
    print("--- Running Inventory & Supply Chain QA Tests ---\n")
    system = InventorySystem()

    # 1. Stock availability (Fulfilling from automatic optimal warehouse)
    print("Test 1: Stock Availability & Auto Warehouse Selection")
    print(system.fulfill_order("Mouse", 20)) # Warehouse A has 50
    print()

    # 2. Insufficient inventory
    print("Test 2: Insufficient Inventory")
    print(system.fulfill_order("Laptop", 100))
    print()

    # 3. Warehouse transfer
    print("Test 3: Warehouse Transfer")
    print("Before Transfer - WH A Keyboard:", system.warehouses["Warehouse A"].get("Keyboard", 0))
    print(system.transfer_stock("Warehouse C", "Warehouse A", "Keyboard", 10))
    print("After Transfer - WH A Keyboard:", system.warehouses["Warehouse A"].get("Keyboard", 0))
    print()

    # 4. Concurrent orders (Simulated sequential flow)
    print("Test 4: Simulated Concurrent Orders")
    print(system.fulfill_order("Monitor", 5))
    print(system.fulfill_order("Monitor", 5))
    print()

    # 5. Reorder threshold trigger
    print("Test 5: Reorder Threshold Detection")
    print(system.fulfill_order("Keyboard", 3)) # Triggers low stock alert
    print()

    # 6. Invalid product
    print("Test 6: Invalid Product Request")
    print(system.fulfill_order("Smartwatch", 2))
    print()

    # 7. Negative inventory prevention
    print("Test 7: Negative Inventory Prevention")
    print(system.add_product("Warehouse A", "Mouse", -15))
    print()

    # 8. Multiple warehouses status check
    print("Test 8: Multiple Warehouses Overview")
    for wh, inventory in system.warehouses.items():
        print(f"{wh}: {inventory}")

if __name__ == "__main__":
    run_tests()
