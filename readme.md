## Budget Insights
The purpose of the project is to create a custom budget that gives insight into future events by forecasting income, gain/loss, assets, and events such as job changes or large expenses in the future.
The project was also built for practice in data analyzing & visualization using python and several common packages such as pandas, tkinter, matplotlib, etc.

TODO.md is used with VSCode add-on "TODO.md Kanban Board"
    https://marketplace.visualstudio.com/items?itemName=coddx.coddx-alpha

layout.drawio is used with draw.io to visualize GUI layout as well as design UML for code organization.

## Setup - Windows
```
.\run_tests.ps1 [-build]
```
The -build flag will create a dist and install it, which then can be utilized by running:
```
budget
```
## Testing, Linting, & Coverage
This project utilizes pytest for running unit tests, pytest-cov for viewing code coverage, pylama for linting, and nox for a testing environment. If code coverage falls under 80%, linting errors exist, or any unit tests fail then the build fails.