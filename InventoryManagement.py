class InventorySystem:
    def __init__(self):
        # Warehouses with initial stock {product_name: quantity}
        self.warehouses = {
            "Warehouse A": {"Laptop": 10, "Mouse": 50, "Keyboard": 5},
            "Warehouse B": {"Laptop": 2, "Mouse": 5, "Monitor": 15},
            "Warehouse C": {"Keyboard": 20, "Monitor": 5, "Laptop": 15}
        }
        self.suppliers = {"Laptop": "TechCorp", "Mouse": "AccessoryInc", "Keyboard": "KeyPro", "Monitor": "DisplayCo"}
        self.reorder_thresholds = {"Laptop": 5, "Mouse": 10, "Keyboard": 5, "Monitor": 3}

    def add_product(self, warehouse, product, quantity):
        if quantity < 0:
            return "Error: Negative inventory is not allowed."
        if warehouse not in self.warehouses:
            return "Error: Invalid warehouse selected."
        
        self.warehouses[warehouse][product] = self.warehouses[warehouse].get(product, 0) + quantity
        return f"Success: Added {quantity} of {product} to {warehouse}."

    def remove_product(self, warehouse, product, quantity):
        if quantity < 0:
            return "Error: Negative quantity."
        if warehouse not in self.warehouses:
            return "Error: Invalid warehouse selected."
        if product not in self.warehouses[warehouse]:
            return f"Error: Product {product} not found in {warehouse}."
        
        current_stock = self.warehouses[warehouse][product]
        if current_stock < quantity:
            return f"Error: Insufficient inventory in {warehouse}. Available: {current_stock}"
        
        self.warehouses[warehouse][product] -= quantity
        return f"Success: Removed {quantity} of {product} from {warehouse}."

    def select_warehouse_for_order(self, product, quantity):
        # Automatically select warehouse with enough stock
        for wh_name, stock in self.warehouses.items():
            if stock.get(product, 0) >= quantity:
                return wh_name
        return None

    def fulfill_order(self, product, quantity):
        if quantity <= 0:
            return "Error: Invalid or negative order quantity."
        
        target_wh = self.select_warehouse_for_order(product, quantity)
        if not target_wh:
            return f"Error: Insufficient inventory across all warehouses for product '{product}'."
        
        self.warehouses[target_wh][product] -= quantity
        
        # Check low stock / reorder threshold
        reorder_msg = ""
        if self.warehouses[target_wh][product] <= self.reorder_thresholds.get(product, 5):
            reorder_msg = f" | {self.reorder(target_wh, product)}"

        return f"Success: Fulfilled {quantity} of '{product}' from {target_wh}.{reorder_msg}"

    def transfer_stock(self, from_wh, to_wh, product, quantity):
        if from_wh not in self.warehouses or to_wh not in self.warehouses:
            return "Error: Invalid warehouse selection."
        if quantity <= 0:
            return "Error: Quantity must be positive."
        if self.warehouses[from_wh].get(product, 0) < quantity:
            return f"Error: Insufficient stock in {from_wh} for transfer."

        self.warehouses[from_wh][product] -= quantity
        self.warehouses[to_wh][product] = self.warehouses[to_wh].get(product, 0) + quantity
        return f"Success: Transferred {quantity} of {product} from {from_wh} to {to_wh}."

    def reorder(self, warehouse, product):
        supplier = self.suppliers.get(product, "General Supplier")
        return f"REORDER ALERT: Stock low for {product} in {warehouse}. Placed reorder with {supplier}."
