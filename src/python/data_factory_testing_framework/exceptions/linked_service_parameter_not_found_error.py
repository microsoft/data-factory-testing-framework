class LinkedServiceParameterNotFoundError(Exception):
    def __init__(self, linked_service_name: str):
        super().__init__(f"LinkedService parameter: '{linked_service_name}' not found")