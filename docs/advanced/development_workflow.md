# Recommended development workflow for Azure Data Factory (ADF) v2 and Azure Synapse Analytics

* Use ADF / Azure Synapse Analytics Git integration
* Use UI to create a feature branch, build the initial pipeline, and save it to the feature branch
* Pull feature branch locally
* Start writing unit and functional tests, run them locally for immediate feedback, and fix bugs
* Push changes to the feature branch
* Test the new features manually through the UI in a sandbox environment
* Create PR, which will run the tests in the CI pipeline
* Approve PR
* Merge to main and start deploying to dev/test/prod environments
* Run e2e tests after each deployment to validate all happy flows work on that specific environment
