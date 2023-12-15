Addinf# Data Factory - Testing Framework

## Setup 

This is an extra step for setup in case you need additional help to do it . The Unit Test does not need to rigorously  follow this steps to work. You just need to start you python project , choose your testing library and starting to code. Though, if you need additional assistance how to do it which library to use and some code examples. Feel free to use this guide. 

### Step by Step 

If for example you are using Visual Studio Code:

For more references: [Get Started Tutorial for Python in Visual Studio Code](https://code.visualstudio.com/docs/python/python-tutorial)

1) Open your new python project. 

![image-20231214103440277](C:\Users\lilem\AppData\Roaming\Typora\typora-user-images\image-20231214103440277.png)

2. Pip install the following libraries from the terminal - data-factory-testing-framework:

   References about the vs code terminal : [Integrated Terminal in Visual Studio Code](https://code.visualstudio.com/docs/terminal/basics)

   

   Please note, data-factory-testing-framework has dependencies on the following libraries:
   
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



![image-20231214111124512](C:\Users\lilem\AppData\Roaming\Typora\typora-user-images\image-20231214111124512.png)



#### Poetry Configuration 

 If you decide to use poetry, please follow some additional steps. Also use this reference for more information: [Introduction | Documentation | Poetry - Python dependency management and packaging made easy (python-poetry.org)](https://python-poetry.org/docs/#installation)

 If you decide not to use, feel free to ignore those steps.

1. Run the following on the power shell, if you are suing windows:

```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python
```

![image-20231214113918331](C:\Users\lilem\AppData\Roaming\Typora\typora-user-images\image-20231214113918331.png)

2. Add the bin the PATH environment variable the path

![image-20231214114439582](C:\Users\lilem\AppData\Roaming\Typora\typora-user-images\image-20231214114439582.png) 

![image-20231214114603087](C:\Users\lilem\AppData\Roaming\Typora\typora-user-images\image-20231214114603087.png)

3. Add the unit test framework for testing. 

`poetry add data-factory-testing-framework`poetry 

![image-20231214124838477](C:\Users\lilem\AppData\Roaming\Typora\typora-user-images\image-20231214124838477.png)

Lets Start testing!
