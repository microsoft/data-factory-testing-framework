# Overriding expression functions

The framework interprets expressions containing functions, which are implemented within the framework, and they might contain bugs.
You can override their implementation as illustrated below:

```python
   FunctionsRepository.register("concat", lambda arguments: "".join(arguments))
   FunctionsRepository.register("trim", lambda text, trim_argument: text.strip(trim_argument[0]))
```
