class DatasetParameterNotFoundError(Exception):
    def __init__(self, dataset_name: str) -> None:
        """Error raised when a dataset expression is not found."""
        super().__init__(f"Dataset parameter: '{dataset_name}' not found")
