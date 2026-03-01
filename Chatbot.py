def get_hospital_data():
    """Returns the static data needed for the UI"""
    return {
        "specialties": ['pediatrics', 'cardiology', 'general medicine', 'dentistry'],
        "slots": ['morning', 'afternoon', 'evening']
    }

def process_appointment(name, spec_choice, urgency, time_choice):
    """Processes the logic and returns the confirmation details"""
    status = "PRIORITY" if urgency == '3' else "STANDARD"
    
    summary = {
        "name": name,
        "department": spec_choice.capitalize(),
        "shift": time_choice.capitalize(),
        "status": status,
        "is_urgent": urgency == '3'
    }
    return summary