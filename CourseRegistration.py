class CourseRegistrationSystem:
    def __init__(self):
        self.course_catalog = {
            "DBMS": {"credits": 4, "prereq": ["Programming"], "capacity": 2, "time": "Mon 10:00"},
            "AI": {"credits": 4, "prereq": ["Data Structures"], "capacity": 2, "time": "Tue 11:00"},
            "ML": {"credits": 3, "prereq": ["Statistics"], "capacity": 2, "time": "Mon 10:00"}, # Conflicts with DBMS time
            "Cloud": {"credits": 3, "prereq": ["Networking"], "capacity": 5, "time": "Wed 14:00"}
        }
        self.student_records = {} # student_id: [registered_courses]

    def register_courses(self, student_id, completed_courses, selected_courses, max_credits=9):
        if student_id in self.student_records:
            return "Error: Duplicate student registration attempt."

        total_credits = 0
        scheduled_times = []
        registered = []

        for course in selected_courses:
            if course not in self.course_catalog:
                return f"Error: Invalid course '{course}'."
            
            details = self.course_catalog[course]

            # Verify Prerequisites
            for req in details["prereq"]:
                if req not in completed_courses:
                    return f"Error: Missing prerequisite '{req}' for course '{course}'."

            # Verify Capacity
            current_enrolled = sum(1 for s in self.student_records.values() if course in s)
            if current_enrolled >= details["capacity"]:
                return f"Error: Course '{course}' is full."

            # Verify Timetable Clashes
            if details["time"] in scheduled_times:
                return f"Error: Timetable conflict detected at '{details['time']}'."

            # Check Credit Limit
            if total_credits + details["credits"] > max_credits:
                return f"Error: Credit-limit violation. Max allowed is {max_credits}."

            total_credits += details["credits"]
            scheduled_times.append(details["time"])
            registered.append(course)

        self.student_records[student_id] = registered
        return f"Success: Registered for {registered}. Total Credits: {total_credits}"
