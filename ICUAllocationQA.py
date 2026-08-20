from ICUAllocation import ICUSystem

def run_tests():
    print("--- Running ICU Resource Allocation QA Tests ---")
    icu = ICUSystem(total_icu_beds=2)

    print("1. Critical Patient:", icu.admit_patient("P1", 70, 85, 130, "140/90", 40.0, ["Heart Disease"]))
    print("2. Normal Patient:", icu.admit_patient("P2", 30, 98, 75, "120/80", 37.0, []))
    print("3. No Beds Available (Waitlist):", icu.admit_patient("P3", 45, 92, 90, "130/85", 38.0, []))
    print("4. Emergency Case Override:", icu.admit_patient("P4", 50, 88, 140, "160/100", 41.0, [], is_emergency=True))
    print("5. Duplicate Patient ID:", icu.admit_patient("P1", 70, 85, 130, "140/90", 40.0, ["Heart Disease"]))
    print("6. Invalid Oxygen Level:", icu.admit_patient("P5", 25, 105, 80, "120/80", 36.5, []))
    print("7. Invalid Heart Rate:", icu.admit_patient("P6", 40, 96, 350, "120/80", 36.5, []))
    print()

if __name__ == "__main__":
    run_tests()
