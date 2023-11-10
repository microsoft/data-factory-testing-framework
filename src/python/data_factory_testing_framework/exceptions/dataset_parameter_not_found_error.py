class DatasetParameterNotFoundError(Exception):
    def __init__(self, dataset_name: str):
        super().__init__(f"Dataset parameter: '{dataset_name}' not found")