# Data Factory - Testing Framework

## Setup 

This is an extra step for setup in case you need additional help to do it. The Unit Test does not need to rigorously  follow these steps to work. You just need to start your Python project, choose your testing library, and start to code. Though, if you need additional assistance how to do it which library to use, and some code examples. Feel free to use this guide. 

### Step by Step 

If for example you are using Visual Studio Code:

For more references: [Get Started Tutorial for Python in Visual Studio Code](https://code.visualstudio.com/docs/python/python-tutorial)

1. Open your new Python project. 
![image](https://github.com/LiliamLeme/data-factory-testing-framework/assets/62876278/9f76474d-b365-43e5-8fb0-dc074cdb1584)



2. Pip install the following libraries from the terminal - data-factory-testing-framework:

   References about the vs code terminal : [Integrated Terminal in Visual Studio Code](https://code.visualstudio.com/docs/terminal/basics)

   

   Please note, that the data-factory-testing-framework has dependencies on the following libraries:
   
   ```
   pip install sentence-transformers
   
   pip install Flask
   
   pip install tensorflow 
   
   pip install Werkzeug
   ```

   

   ### **Then data-factory-testing-framework:**

   
   
   ```
   pip install data-factory-testing-framework
   ```



	### Testing Libraries



**Additionally** you could use for example <u>pytest or poetry( or both) or even another</u> library that you prefer for the Unit test: 

```
pip install pytest
pip install poetry
```

Library Docs for reference: 

[Introduction | Documentation | Poetry - Python dependency management and packaging made easy (python-poetry.org)](https://python-poetry.org/docs/)

[pytest: helps you write better programs — pytest documentation](https://docs.pytest.org/en/7.4.x/)


![image](https://github.com/LiliamLeme/data-factory-testing-framework/assets/62876278/2d40fa37-36d4-4315-8613-24b701210855)




#### Poetry Configuration 

 If you decide to use poetry, please follow some additional steps. Also, use this reference for more information: [Introduction | Documentation | Poetry - Python dependency management and packaging made easy (python-poetry.org)](https://python-poetry.org/docs/#installation)

 If you decide not to use it, feel free to ignore those steps.

1. Run the following on the power shell, if you are using Windows:

```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python
```

![image](https://github.com/LiliamLeme/data-factory-testing-framework/assets/62876278/7e640198-8d37-46eb-97d1-d82765633eb0)


2. Add the bin to the PATH environment variable to the path
![image](https://github.com/LiliamLeme/data-factory-testing-framework/assets/62876278/43c1f4e8-b57a-4a19-adc2-d122c90d8713)


3. Add the unit test framework for testing. 

`poetry add data-factory-testing-framework`poetry 
![image](https://github.com/LiliamLeme/data-factory-testing-framework/assets/62876278/2043c19f-b34d-4d29-af96-b505c3f96e82)

Let's Start testing!
