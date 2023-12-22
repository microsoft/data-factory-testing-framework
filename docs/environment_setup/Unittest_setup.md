# Data Factory - Testing Framework

## Setup 

This is an extra step for setup in case you need additional help to do it. The Unit Test does not need to rigorously  follow these steps to work. You just need to start your Python project, choose your testing library, and start to code. Though, if you need additional assistance how to do it which library to use, and some code examples. Feel free to use this guide. 

### Step by Step 

If for example you are using Visual Studio Code:

For more references: [Get Started Tutorial for Python in Visual Studio Code](https://code.visualstudio.com/docs/python/python-tutorial)

1. Open your new Python project.


![image](/docs/environment_setup/images/new_project.png)


3. Pip install the following libraries from the terminal - data-factory-testing-framework:

   References about the vs code terminal : [Integrated Terminal in Visual Studio Code](https://code.visualstudio.com/docs/terminal/basics)
  
   ### **Then data-factory-testing-framework:**
   
   ```python
   pip install data-factory-testing-framework
   ```

	### Additional Libraries

**Additionally** you could use for example <u>pytest even another</u> test library that you prefer for the Unit test: 

```python
pip install pytest
```
You could also use Poetry as a package management library:

```python
pip install poetry
```

Library Docs for reference: 

[Introduction | Documentation | Poetry - Python dependency management and packaging made easy (python-poetry.org)](https://python-poetry.org/docs/)

[pytest: helps you write better programs — pytest documentation](https://docs.pytest.org/en/7.4.x/)


![image](/docs/environment_setup/images/pipinstall_poetry.png)

#### Poetry Configuration 

 If you decide to use poetry, please follow some additional steps. Also, use this reference for more information: [Introduction | Documentation | Poetry - Python dependency management and packaging made easy (python-poetry.org)](https://python-poetry.org/docs/#installation)

 If you decide not to use it, feel free to ignore those steps.

1. Run the following on the power shell, if you are using Windows:

```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python
```

![image](/docs/environment_setup/images/power_shell_invoke.png)


![image](/docs/environment_setup/images/installing_poetry_power_shell.png)


2. Add the bin to the PATH environment variable to the path


![image](/docs/environment_setup/images/env_variable.png)


4. Add the unit test framework for testing. 

`poetry add data-factory-testing-framework`poetry 


![image](/docs/environment_setup/images/poetry_framework.png)


Let's Start testing!
