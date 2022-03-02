# Python Processing Module Boilerplate


|              |                                                            |
| ------------ | ---------------------------------------------------------- |
| name         | Python Processing Module Boilerplate                       |
| version      | v0.0.2                                                     |
| docker image | [weevenetwork/weeve-boilerplate](https://linktodockerhub/) |
| tags         | Python, Flask, Docker, Weeve                               |
| authors      | Sanyam Arya                                                |

***
## Table of Content
- [Python Processing Module Boilerplate](#python-processing-module-boilerplate)
  - [Table of Content](#table-of-content)
  - [Description](#description)
    - [Features](#features)
  - [Environment Variables](#environment-variables)
    - [Module Specific](#module-specific)
    - [Set by the weeve Agent on the edge-node](#set-by-the-weeve-agent-on-the-edge-node)
  - [Directory Structure](#directory-structure)
    - [File Tree](#file-tree)
  - [As a module developer](#as-a-module-developer)
    - [Configuration](#configuration)
    - [Business Logic](#business-logic)
  - [Dependencies](#dependencies)
  - [Output/Egress](#outputegress)
- [VSCode Support for devcontainer](#vscode-support-for-devcontainer)

***

## Description 

This is a Python Processing Boilerplate module and it serves as a starting point for developers to build process modules for weeve platform and data services.
Navigate to [As a module developer](#as-a-module-developer) to learn how to use this module.

### Features
1. Flask ReST client
2. Request - sends HTTP Request to the next module

## Environment Variables

### Module Specific
The following module configurations can be provided in a data service designer section on weeve platform:

| Name         | Environment Variables | type   | Description                                  |
| ------------ | --------------------- | ------ | -------------------------------------------- |
| Input Label  | INPUT_LABEL           | string | The input label on which anomaly is detected |
| Output Label | OUTPUT_LABEL          | string | The output label as which data is dispatched |
| Output Unit  | OUTPUT_UNIT           | string | The output unit in which data is dispatched  |

***

Other features required for establishing the inter-container communication between modules in a data service are set by weeve agent.

### Set by the weeve Agent on the edge-node

| Environment Variables | type   | Description                                       |
| --------------------- | ------ | ------------------------------------------------- |
| MODULE_NAME           | string | Name of the module                                |
| MODULE_TYPE           | string | Type of the module (ingress, processing, egress)  |
| EGRESS_SCHEME         | string | URL Scheme                                        |
| EGRESS_HOST           | string | URL target host                                   |
| EGRESS_PORT           | string | URL target port                                   |
| EGRESS_PATH           | string | URL target path                                   |
| EGRESS_URL            | string | HTTP ReST endpoint for the next module            |


> Node: For testing all the the environment overrides can be added to the `config.env` file.

## Directory Structure

Most important resources:

| name              | description                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------ |
| image             | All resources related to Docker image (Dockerfile, entrypoint.sh, source code, requirements.txt)       |
| image/src/main.py | Entry-point for the module                                                                             |
| image/src/app     | The application directory                                                                              |
| config.env        | Environment variables for running the module                                                           |
| deploy.env        | Environment variables for deploying the module to Dockerhub                                            |
| Module.yaml       | Module's YAML file that is later used by weeve platform Data Service Designer                          |

### File Tree

```bash

├── image
│   ├── src
│   │   ├── app
│   │   │   ├── __init__.py
│   │   │   ├── config
│   │   │   │   ├── __init__.py
│   │   │   │   ├── application.py # Application/module specific configurations
│   │   │   │   ├── http_codes.py # HTTP Status codes
│   │   │   │   ├── log.py # log configuration
│   │   │   │   └── weeve.py # Weeve agent specific configurations
│   │   │   ├── module
│   │   │   │   ├── __init__.py
│   │   │   │   ├── main.py # [*] Main logic for the module
│   │   │   │   └── validation.py # [*] Validation logic for incoming data
│   │   │   ├── utils # Utility methods added here
│   │   │   │   ├── __init__.py
│   │   │   │   ├── booleanenv.py
│   │   │   │   ├── env.py
│   │   │   │   └── floatenv.py
│   │   │   └── weeve # THe weeve logic
│   │   │       ├── __init__.py
│   │   │       ├── controllers.py
│   │   │       ├── egress.py # Egress data to the next module
│   │   │       └── health.py
│   │   └── main.py
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── requirements.txt
├── config.env # Config environment variables for the module
├── deploy.env # Environment variables for deploying the module to Dockerhub
├── docker-compose.yml
├── makefile
├── Module.yaml # Used by weeve platform to generate resource in Data Service Designer section
└── README.md

```

## As a module developer

A module developer needs to add all the configuration and business logic.
### Configuration

* All the environment variables and global constants can be declared in the config package in the `image/src/app/config/application.py` file.
* It uses the utils to get values from the environment and are recommended to the developer to use.
  * env - Returns the value for the `ENVIRONMENT_VARIABLE` or the `default value`
  * boolenv - Returns the boolean value for the `ENVIRONMENT_VARIABLE` or `false`
  * floatenv - Returns the float value for the `ENVIRONMENT_VARIABLE` or `0.0`


```python
    APPLICATION = {
        "INPUT_LABEL": env("INPUT_LABEL", "temperature"),
        "OUTPUT_LABEL": env("OUTPUT_LABEL", "temperature"),
        "OUTPUT_UNIT": env("OUTPUT_UNIT", "Celsius"),
    }
 ``` 

### Business Logic
All the module logic can be written in the module package in image/src directory.
   * The files can me modified for the module
      1. `module/validation.py`
         * The function `data_validation` takes the JSON data from the previous module.
         * Incoming data can be validated here.
         * Checks if data is of type `dict` or `list`.
         * Checks if data contains required fields.
         * Validation Errors can be send back to the HTTP REST client.
         * Returns `[ data , error ]`
      2. `module/main.py`
         * The function `module_main` takes the output of the validation function as an argument.
         * All the business logic about modules are written here
         * Returns `[ data , error ]`
      3. `weeve/egress`
         * The function `send_data` takes the output of the main logic as an argument.
         * Responsible for sending the data to the next module
         * *It is not advisable to change it, but can be easily modified by altering the `send_data` function*


## Dependencies

* Flask==1.1.1
* requests
* python-dotenv

## Output/Egress
Output of this module is JSON body:

```node
{
    "<OUTPUT_LABEL>": <Processed data>,
    "output_unit": <OUTPUT_UNIT>,
    "<MODULE_NAME>Time": timestamp
}
```
 
* Here `OUTPUT_LABEL` and `OUTPUT_UNIT` are specified at the module creation and `Processed data` is data processed by Module Main function.
* However this could be modified in `image/src/weeve/egress.py`

* Modules return a 200 response for success, and 500 for error. No other return message is supported. 


# VSCode Support for devcontainer

1. VSCode can use a `docker` containerized solution for local development. [Read More about devcontainers]("https://code.visualstudio.com/docs/remote/create-dev-container).
1. `.devcontiner` directory has all the information about that.
2. Installs all the dependencies from the `requirements.txt` file.
3. Installed python packages:
    * `rope` - Used by VS code to refactor code 
    * `pylint` - for lint checks on python files
4. It also contains a nodejs `package.json` file and nodejs installed on the dev container.
     * It contains the npm script to run and watch the module code while development.
     * It provides hot refolding using a nodejs package called `nodemon`.
%. `npm run start` or simply `npm start` to run the dev server