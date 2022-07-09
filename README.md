# Fluctuation Filter Module

|              |                                                                  |
| ------------ | ---------------------------------------------------------------- |
| name         | Fluctuation Filter                                               |
| version      | v1.0.0                                                           |
| GitHub       | [weevenetwork/fluctuation-filter](https://hub.docker.com/r/weevenetwork/fluctuation-filter) |
| authors      | Mithila Ghuge, Paul Gaiduk                                          |

***
## Table of Content

- [Fluctuation Filter Module](#fluctuation-filter-module)
  - [Table of Content](#table-of-content)
  - [Description](#description)
  - [Module Variables](#module-variables)
  - [Module Testing](#module-testing)
  - [Dependencies](#dependencies)
  - [Input](#input)
  - [Output](#output)
    - [Example](#example)
***

## Description 

This is a Python Fluctuation Filter module and it is used to eliminate unwanted spikes from input data and provide stable output. It will delay the change of the value filtering out specific amount (instances) of different, non-persisting value. 

## Module Variables

There are 5 module variables that are required by each module to correctly function within weeve ecosystem. In development, these variables can overridden for testing purposes. In production, these variables are set by weeve Agent.

| Environment Variables | type   | Description                                       |
| --------------------- | ------ | ------------------------------------------------- |
| INPUT_LABEL           | string  | The input label on which anomaly is detected          |
| WINDOW_SIZE           | integer | The stable instance count which need to be consider   |
| SEND_ON_CHANGE        | boolean | Set true to Output data only when stable value changes|
| MODULE_NAME           | string | Name of the module                                |
| MODULE_TYPE           | string | Type of the module (Input, Processing, Output)    |
| LOG_LEVEL             | string | Allowed log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL. Refer to `logging` package documentation. |
| INGRESS_HOST          | string | Host to which data will be received               |
| INGRESS_PORT          | string | Port to which data will be received               |
| EGRESS_URLS           | string | HTTP ReST endpoint for the next module            |

## Module Testing

To test module navigate to `test` directory. In `test/assets` edit both .json file to provide input for the module and expected output. During a test, data received from the listeners are compared against expected output data. You can run tests with `make run_test`.

## Dependencies

The following are module dependencies:

* bottle
* requests

The following are developer dependencies:

* pytest
* flake8
* black

## Input

Input to this module is JSON body single object or array of objects:

Example:

```json
{
  "temperature": 15
}
```

```json
[
  {
    "temperature": 15
  },
  {
    "temperature": 21
  },
  {
    "temperature": 25
  }
]
```

## Output
Output of this module is JSON body:

```json
{
    "<INPUT_LABEL>": <Processed data>,
    "<MODULE_NAME>Time": timestamp
}
```

### Example 

```
Input data : (23,23,24,24,24,22,21,21,21,23,24,25,25,25)
Window_Size : 3
Assume previous_stable_value = x

If Send_on_change == True then 
Expected Output : (24,21,25)

If Send_on_change == False then
Expected Output :(x,x,x,x,24,24,24,24,21,21,21,21,21,25)
```
