class RideBookingSystem:
    def __init__(self):
        # Available drivers mapped by vehicle type
        self.available_drivers = {
            "Bike": ["Driver_Alex", "Driver_Sam"],
            "Sedan": ["Driver_John"],
            "SUV": [],
            "Premium": ["Driver_James"]
        }

    def calculate_and_book(self, customer_id, pickup, drop, distance, passengers, vehicle_type, booking_hour, promo_code=None):
        # Validation checks
        if distance <= 0:
            return "Error: Distance must be greater than zero."
        
        max_passengers = {"Bike": 1, "Sedan": 4, "SUV": 6, "Premium": 4}
        if vehicle_type not in max_passengers:
            return "Error: Invalid vehicle type."
        if passengers <= 0 or passengers > max_passengers[vehicle_type]:
            return f"Error: Invalid passenger count for {vehicle_type}."
        
        if booking_hour < 0 or booking_hour > 23:
            return "Error: Invalid booking time."
            
        if not self.available_drivers.get(vehicle_type):
            return f"Error: No available drivers for {vehicle_type}."

        # Fare calculation parameters
        base_fares = {"Bike": 30.0, "Sedan": 50.0, "SUV": 80.0, "Premium": 120.0}
        per_km_rates = {"Bike": 10.0, "Sedan": 15.0, "SUV": 22.0, "Premium": 35.0}

        base = base_fares[vehicle_type]
        distance_fare = distance * per_km_rates[vehicle_type]
        
        # Surcharges
        peak_surcharge = 0.25 * (base + distance_fare) if (7 <= booking_hour <= 10 or 17 <= booking_hour <= 20) else 0.0
        night_surcharge = 0.15 * (base + distance_fare) if (22 <= booking_hour or booking_hour <= 5) else 0.0
        passenger_surcharge = 10.0 * max(0, passengers - 2)
        
        # Promotional discount
        discount = 50.0 if promo_code == "MAXDISCOUNT" else (10.0 if promo_code == "SAVE10" else 0.0)

        total_fare = max(0.0, base + distance_fare + peak_surcharge + night_surcharge + passenger_surcharge - discount)

        # Assign driver
        assigned_driver = self.available_drivers[vehicle_type].pop(0)

        return {
            "Status": "Success",
            "Customer": customer_id,
            "Vehicle": vehicle_type,
            "Assigned Driver": assigned_driver,
            "Final Fare": round(total_fare, 2)
        }
