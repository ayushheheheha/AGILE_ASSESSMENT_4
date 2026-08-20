class ICUSystem:
    def __init__(self, total_icu_beds):
        self.total_beds = total_icu_beds
        self.allocated_beds = 0
        self.patient_records = set()
        self.waiting_list = []
        self.active_patients = []

    def admit_patient(self, patient_id, age, oxygen, heart_rate, bp, temp, conditions, is_emergency=False):
        if patient_id in self.patient_records:
            return "Error: Duplicate patient ID rejected."
        if not (0 <= oxygen <= 100):
            return "Error: Invalid oxygen level."
        if not (0 <= heart_rate <= 300):
            return "Error: Invalid heart rate."

        # Calculate Priority Score
        score = 0
        if oxygen < 90: score += 40
        elif oxygen < 95: score += 20
        
        if heart_rate < 50 or heart_rate > 120: score += 30
        if temp > 39.5 or temp < 35.0: score += 20
        if "Diabetes" in conditions or "Heart Disease" in conditions: score += 10
        if age > 65: score += 10

        # Classification
        if score >= 60 or is_emergency:
            classification = "CRITICAL"
        elif score >= 40:
            classification = "HIGH"
        elif score >= 20:
            classification = "MEDIUM"
        else:
            classification = "LOW"

        patient_data = {"id": patient_id, "score": score, "class": classification, "emergency": is_emergency}
        self.patient_records.add(patient_id)

        # Allocation logic
        if is_emergency and self.allocated_beds >= self.total_beds and self.active_patients:
            # Emergency override: bump lowest priority normal patient to waiting list
            self.active_patients.sort(key=lambda x: (x['emergency'], x['score']), reverse=True)
            bumped = self.active_patients.pop()
            self.waiting_list.append(bumped)
            self.active_patients.append(patient_data)
            return f"Emergency Override: Patient {patient_id} allocated bed. Patient {bumped['id']} moved to waiting list."

        if self.allocated_beds < self.total_beds:
            self.allocated_beds += 1
            self.active_patients.append(patient_data)
            return f"Success: Patient {patient_id} admitted to ICU. Priority: {classification} (Score: {score})"
        else:
            self.waiting_list.append(patient_data)
            return f"Warning: No ICU beds available. Patient {patient_id} placed on waiting list."
