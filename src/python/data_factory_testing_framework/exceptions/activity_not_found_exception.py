class ActivityNotFoundException(Exception):
    def __init__(self, activity_name):
        super().__init__(f"Activity with name {activity_name} not found")