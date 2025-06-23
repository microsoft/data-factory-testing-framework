from typing import List, Optional, Union, overload

from data_factory_testing_framework.mock import Any, ExpressionMock, Scope


@overload
def mock_utcnow(datetime_str: str) -> ExpressionMock: ...

@overload
def mock_utcnow(datetime_str: str, scope: Scope) -> ExpressionMock: ...

@overload
def mock_utcnow(
    datetime_str: str,
    *,
    pipeline: Union[str, object] = None,
    activity: Union[str, object] = None,
    type_property: Union[str, object] = None
) -> ExpressionMock: ...

def mock_utcnow(
    datetime_str: str,
    scope: Optional[Scope] = None,
    *,
    pipeline: Union[str, object] = None,
    activity: Union[str, object] = None,
    type_property: Union[str, object] = None
) -> ExpressionMock:
    individual_params_provided = any(param is not None for param in [pipeline, activity, type_property])
    if scope is not None and individual_params_provided:
        raise ValueError("Cannot provide both 'scope' and individual scope parameters. Use either a Scope object or individual parameters.")
    if individual_params_provided:
        created_scope = Scope(
            pipeline=pipeline if pipeline is not None else Any,
            activity=activity if activity is not None else Any,
            type_property=type_property if type_property is not None else Any
        )
        return ExpressionMock("utcnow", datetime_str, created_scope)
    return ExpressionMock("utcnow", datetime_str, scope)

@overload
def mock_guid(guid_values: Union[str, List[str]]) -> ExpressionMock: ...

@overload
def mock_guid(guid_values: Union[str, List[str]], scope: Scope) -> ExpressionMock: ...

@overload
def mock_guid(
    guid_values: Union[str, List[str]],
    *,
    pipeline: Union[str, object] = None,
    activity: Union[str, object] = None,
    type_property: Union[str, object] = None
) -> ExpressionMock: ...

def mock_guid(
    guid_values: Union[str, List[str]],
    scope: Optional[Scope] = None,
    *,
    pipeline: Union[str, object] = None,
    activity: Union[str, object] = None,
    type_property: Union[str, object] = None
) -> ExpressionMock:
    values = [guid_values] if isinstance(guid_values, str) else guid_values
    individual_params_provided = any(param is not None for param in [pipeline, activity, type_property])
    if scope is not None and individual_params_provided:
        raise ValueError("Cannot provide both 'scope' and individual scope parameters. Use either a Scope object or individual parameters.")
    if individual_params_provided:
        created_scope = Scope(
            pipeline=pipeline if pipeline is not None else Any,
            activity=activity if activity is not None else Any,
            type_property=type_property if type_property is not None else Any
        )
        return ExpressionMock("guid", values, created_scope)
    return ExpressionMock("guid", values, scope)

@overload
def mock_rand(values: Union[int, List[int]]) -> ExpressionMock: ...

@overload
def mock_rand(values: Union[int, List[int]], scope: Scope) -> ExpressionMock: ...

@overload
def mock_rand(
    values: Union[int, List[int]],
    *,
    pipeline: Union[str, object] = None,
    activity: Union[str, object] = None,
    type_property: Union[str, object] = None
) -> ExpressionMock: ...

def mock_rand(
    values: Union[int, List[int]],
    scope: Optional[Scope] = None,
    *,
    pipeline: Union[str, object] = None,
    activity: Union[str, object] = None,
    type_property: Union[str, object] = None
) -> ExpressionMock:
    values_list = [values] if isinstance(values, int) else values
    individual_params_provided = any(param is not None for param in [pipeline, activity, type_property])
    if scope is not None and individual_params_provided:
        raise ValueError("Cannot provide both 'scope' and individual scope parameters. Use either a Scope object or individual parameters.")
    if individual_params_provided:
        created_scope = Scope(
            pipeline=pipeline if pipeline is not None else Any,
            activity=activity if activity is not None else Any,
            type_property=type_property if type_property is not None else Any
        )
        return ExpressionMock("rand", values_list, created_scope)
    return ExpressionMock("rand", values_list, scope)
