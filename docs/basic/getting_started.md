# Getting started

This _getting started_ focuses on novice users who are not familiar with Python or package management. It guides the user through the process of downloading the data factory pipeline files, setting up a Python project and installing the framework so that they can start writing tests.

>For experienced Python and package management users, you can skip this page and go directly to the [repository setup](repository_setup.md) page.

## Install dotnet runtime

Install the dotnet runtime (not SDK) from [here](https://dotnet.microsoft.com/en-us/download/dotnet/8.0). This is required to run some expression functions on dotnet just like in Data Factory.

## Data Factory pipeline files

The framework is designed to work with the `json` files that define the data factory pipelines and activities. Files from the data factory environment can be downloaded from your data factory environment as described in the [repository setup](repository_setup.md) page.

## Setting up the Python project

For Visual Studio Code, the guidance is:

1. Create a new folder alongside the data factory pipeline files for the test project called `tests`.
2. Open the new folder in Visual Studio Code.
3. Install the framework by installing the library the terminal with pip:

   ```bash
   pip install data-factory-testing-framework
   ```

4. Install pytest as testing library. All examples in this documentation are using pytest.

   ```bash
   pip install pytest
   ```

5. Download the pipeline files from data factory environment and place them in the project folder as described in the [repository setup](repository_setup.md) page.

Additional resources:

* [Get Started Tutorial for Python in Visual Studio Code](https://code.visualstudio.com/docs/python/python-tutorial)
* [Integrated Terminal in Visual Studio Code](https://code.visualstudio.com/docs/terminal/basics)
* [pytest: helps you write better programs — pytest documentation](https://docs.pytest.org/en/7.4.x/)

Once the setup is finished, reading the following pages is recommended to learn how to write tests for the data factory:

1. [Initializing the framework](installing_and_initializing_framework.md) (make sure to initialize the root folder of the framework with the path to the folder containing the pipeline definitions).
2. [Activity testing](activity_testing.md)
3. [Pipeline testing](pipeline_testing.md)
