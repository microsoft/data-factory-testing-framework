class DataFactoryElementEvaluationError(Exception):
    """DataFactoryElementEvaluationError.

    This exception is raised when an error occurs while evaluating a DataFactoryElement.
    It is a technical error and should not occur in normal operation of the framework.
    This assumes that the expression is valid and the state is correct.
    """

    pass
