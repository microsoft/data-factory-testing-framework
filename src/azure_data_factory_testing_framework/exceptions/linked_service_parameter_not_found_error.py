class LinkedServiceParameterNotFoundError(Exception):
    def __init__(self, linked_service_name: str) -> None:
        """Error raised when a linked service expression is not found."""
        super().__init__(f"LinkedService parameter: '{linked_service_name}' not found")
