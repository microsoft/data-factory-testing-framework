from data_factory_testing_framework.functions.function_parser import parse_expression
from data_factory_testing_framework.models.base.run_parameter import RunParameter
from data_factory_testing_framework.models.base.run_parameter_type import RunParameterType
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


def test_evaluate_expression_with_nested_function():
    raw_expression = "concat('https://example.com/jobs/,', '123''', concat('&', 'abc,'))"
    expression = parse_expression(raw_expression)
    evaluated = expression.evaluate(PipelineRunState())
    assert evaluated == "https://example.com/jobs/,123'&abc,"


def test_evaluate_with_parameter():
    raw_expression = "concat('https://example.com/jobs/', pipeline().parameters.abc)"
    expression = parse_expression(raw_expression)
    state = PipelineRunState()
    state.parameters.append(RunParameter[str](RunParameterType.Pipeline, "abc", "123"))
    evaluated = expression.evaluate(state)
    assert evaluated == "https://example.com/jobs/123"

#
# def test_evaluate_with_global_parameter(self):
#     raw_expression = "concat('https://example.com/jobs/', pipeline().globalParameters.abc)"
#     expression = FunctionPart.parse(raw_expression)
#     self._state.parameters.append(RunParameter[str](ParameterType.Global, "abc", "123"))
#     evaluated = expression.evaluate[str](self._state)
#     assert evaluated == "https://example.com/jobs/123"
#
#
# def test_evaluate_with_variable(self):
#     raw_expression = "concat('https://example.com/jobs/', variables('abc'))"
#     expression = FunctionPart.parse(raw_expression)
#     self._state.variables.append(PipelineRunVariable[str]("abc", "123"))
#     evaluated = expression.evaluate[str](self._state)
#     assert evaluated == "https://example.com/jobs/123"
#
#
# def test_evaluate_with_activity_output(self):
#     raw_expression = "concat('https://example.com/jobs/', activity('abc').output.abc)"
#     expression = FunctionPart.parse(raw_expression)
#     self._state.add_activity_result(TestActivityResult("abc", {"abc": "123"}))
#     evaluated = expression.evaluate[str](self._state)
#     assert evaluated == "https://example.com/jobs/123"
#
#
# def test_evaluate_with_activity_output_and_variable(self):
#     raw_expression = "concat('https://example.com/jobs/', activity('abc').output.abc, '/', variables('abc'))"
#     expression = FunctionPart.parse(raw_expression)
#     self._state.add_activity_result(TestActivityResult("abc", {"abc": "123"}))
#     self._state.variables.append(PipelineRunVariable[str]("abc", "456"))
#     evaluated = expression.evaluate[str](self._state)
#     assert evaluated == "https://example.com/jobs/123/456"
#
#
# def test_evaluate_with_activity_output_and_variable_and_parameters(self):
#     raw_expression = ("concat('https://example.com/jobs/', activity('abc').output.abc, '/', "
#                       "variables('abc'), '/', pipeline().parameters.abc, '/', pipeline().globalParameters.abc)")
#     expression = FunctionPart.parse(raw_expression)
#     self._state.add_activity_result(TestActivityResult("abc", {"abc": "123"}))
#     self._state.variables.append(PipelineRunVariable[str]("abc", "456"))
#     self._state.parameters.append(RunParameter[str](ParameterType.Pipeline, "abc", "789"))
#     self._state.parameters.append(RunParameter[str](ParameterType.Global, "abc", "10"))
#     evaluated = expression.evaluate[str](self._state)
#     assert evaluated == "https://example.com/jobs/123/456/789/10"
#
#
# @pytest.mark.parametrize("left, right, expected", [
#     ("'abc'", "'abc'", True),
#     ("'abc'", "'abc1'", False),
#     ("1", "1", True),
#     ("1", "2", False),
# ])
# def test_evaluate_equals_expression(self, left, right, expected):
#     raw_expression = f"equals({left}, {right})"
#     expression = FunctionPart.parse(raw_expression)
#     evaluated = expression.evaluate[bool](PipelineRunState())
#     assert evaluated == expected
#
#
# @pytest.mark.parametrize("left, right, expected", [
#     (1, 1, True),
#     (1, 2, False),
#     (2, 2, True),
#     (0, -1, False),
# ])
# def test_evaluate_equals_int_expression(self, left, right, expected):
#     raw_expression = f"equals({left}, {right})"
#     expression = FunctionPart.parse(raw_expression)
#     evaluated = expression.evaluate[bool](PipelineRunState())
#     assert evaluated == expected
#
#
# @pytest.mark.parametrize("key, expected", [
#     ("SomeKey", True),
#     ("SomeKey2", True),
#     ("SomeKey3", False),
# ])
# def test_contains_dictionary_key_expression(self, key, expected):
#     state = PipelineRunState()
#     state.add_activity_result(TestActivityResult("someActivityOutputingDictionary", {
#         "SomeDictionary": {"SomeKey": "SomeValue", "SomeKey2": "SomeValue2"}}))
#     raw_expression = f"@contains(activity('someActivityOutputingDictionary').output.SomeDictionary, '{key}')"
#     expression = FunctionPart.parse(raw_expression)
#     evaluated = expression.evaluate[bool](state)
#     assert evaluated == expected
#
#
# @pytest.mark.parametrize("key, expected", [
#     ("SomeItem", True),
#     ("SomeItem2", True),
#     ("SomeItem3", False),
# ])
# def test_contains_list_item_expression(self, key, expected):
#     state = PipelineRunState()
#     state.add_activity_result(TestActivityResult("someActivityOutputingList", {"SomeList": ["SomeItem", "SomeItem2"]}))
#     raw_expression = f"@contains(activity('someActivityOutputingList').output.SomeList, '{key}')"
#     expression = FunctionPart.parse(raw_expression)
#     evaluated = expression.evaluate[bool](state)
#     assert evaluated == expected
#
#
# @pytest.mark.parametrize("substring, expected", [
#     ("PartOfString", True),
#     ("NotPartOfString", False),
# ])
# def test_contains_string_expression(self, substring, expected):
#     state = PipelineRunState()
#     state.add_activity_result(
#         TestActivityResult("someActivityOutputingString", {"SomeString": "A message that contains PartOfString!"}))
#     raw_expression = f"@contains(activity('someActivityOutputingString').output.SomeString, '{substring}')"
#     expression = FunctionPart.parse(raw_expression)
#     evaluated = expression.evaluate[bool](state)
#     assert evaluated == expected