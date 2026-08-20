from RideBooking import RideBookingSystem

def run_tests():
    print("--- Running Ride-Sharing QA Tests ---")
    system = RideBookingSystem()

    print("1. Normal Booking:", system.calculate_and_book("C1", "A", "B", 10.0, 2, "Sedan", 14))
    print("2. Peak-Hour Booking:", system.calculate_and_book("C2", "A", "B", 8.0, 1, "Bike", 8))
    print("3. Night Booking:", system.calculate_and_book("C3", "A", "B", 15.0, 3, "Sedan", 23))
    print("4. Invalid Distance:", system.calculate_and_book("C4", "A", "B", 0.0, 2, "Sedan", 12))
    print("5. Invalid Passenger Count:", system.calculate_and_book("C5", "A", "B", 5.0, 5, "Bike", 12))
    print("6. Unavailable Driver:", system.calculate_and_book("C6", "A", "B", 10.0, 4, "SUV", 12))
    print("7. Maximum Discount:", system.calculate_and_book("C7", "A", "B", 12.0, 2, "Premium", 14, promo_code="MAXDISCOUNT"))
    print("8. Boundary Fare Values:", system.calculate_and_book("C8", "A", "B", 1.0, 1, "Bike", 3))
    print()

if __name__ == "__main__":
    run_tests()
