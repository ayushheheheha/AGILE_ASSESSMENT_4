from CourseRegistration import CourseRegistrationSystem

def run_tests():
    print("--- Running Course Registration QA Tests ---")
    sys = CourseRegistrationSystem()

    print("1. Valid Registration:", sys.register_courses("S1", ["Programming"], ["DBMS", "Cloud"], max_credits=10))
    print("2. Missing Prerequisite:", sys.register_courses("S2", [], ["AI"], max_credits=10))
    print("3. Credit-Limit Violation:", sys.register_courses("S3", ["Programming", "Data Structures"], ["DBMS", "AI"], max_credits=5))
    print("4. Timetable Conflict:", sys.register_courses("S4", ["Programming", "Statistics"], ["DBMS", "ML"], max_credits=10))
    print("5. Full Course Capacity:", sys.register_courses("S5", ["Programming"], ["DBMS"], max_credits=5)) # DBMS capacity is 2, already filled by S1
    print("6. Duplicate Registration ID:", sys.register_courses("S1", ["Programming"], ["Cloud"], max_credits=10))
    print("7. Invalid Course:", sys.register_courses("S6", [], ["QuantumPhysics"], max_credits=10))
    print()

if __name__ == "__main__":
    run_tests()
