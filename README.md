# Fluctuation Filter Module


|              |                                                            |
| ------------ | ---------------------------------------------------------- |
| name         | Fluctuation Filter                                         |
| version      | v0.0.1                                                     |
| docker image | [weevenetwork/fluctuation-filter](https://hub.docker.com/r/weevenetwork/fluctuation-filter) |
| tags         | Python, Flask, Docker, Weeve                               |
| authors      | Mithila Ghuge                                                |

***
## Table of Content
- [Fluctuation Filter Module](#fluctuation-filter-module)
  - [Table of Content](#table-of-content)
  - [Description](#description)
  - [Features](#features)
  - [Environment Variables](#environment-variables)
    - [Module Specific](#module-specific)
    - [Set by the weeve Agent on the edge-node](#set-by-the-weeve-agent-on-the-edge-node)
  - [Dependencies](#dependencies)
  - [Input](#input)
  - [Output/Egress](#outputegress)
    - [Example](#example)
  - [Docker Compose Example](#docker-compose-example)
***

## Description 

This is a Python Fluctuation Filter module and it is used to eliminate unwanted spikes from input data and provide stable output.
It will delay the change of the value filtering out specific amount (instances) of different, non-persisting value.


## Features
1. Flask ReST client
2. Request - sends HTTP Request to the next module
3. Filtering unstable data and providing stable output

## Environment Variables

### Module Specific
The following module configurations can be provided in a data service designer section on weeve platform:

| Name           | Environment Variables | type    | Description                                           |
| ------------   | --------------------- | ------  | ----------------------------------------------------- |
| Input Label    | INPUT_LABEL           | string  | The input label on which anomaly is detected          |
| Output Label   | OUTPUT_LABEL          | string  | The output label as which data is dispatched          |
| Window Size    | WINDOW_SIZE           | integer | The stable instance count which need to be consider   |
| Send on change | SEND_ON_CHANGE        | boolean | Set true to Output data only when stable value changes|

***

Other features required for establishing the inter-container communication between modules in a data service are set by weeve agent.

### Set by the weeve Agent on the edge-node

| Environment Variables | type   | Description                                       |
| --------------------- | ------ | ------------------------------------------------- |
| MODULE_NAME           | string | Name of the module                                |
| MODULE_TYPE           | string | Type of the module (ingress, processing, egress)  |
| INGRESS_HOST          | string | URL local host                                    |
| INGRESS_PORT          | string | URL local port                                    |
| INGRESS_PATH          | string | URL local path                                    |

## Dependencies

* Flask
* requests
* python-dotenv

## Input

Input to this module is JSON body single object or array of objects:

Example:

```node
{
  "temperature": 15,
}
```

```node
[
  {
    "temperature": 15,
  },
  {
    "temperature": 21,
  },
  {
    "temperature": 25,
  },
];
```

## Output/Egress
Output of this module is JSON body:

```node
{
    "<OUTPUT_LABEL>": <Processed data>,
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

 
* Here `OUTPUT_LABEL` are specified at the module creation and `Processed data` is data processed by Module Main function.

## Docker Compose Example

```yml
version: "3"
services:
  fluctuation_filter:
    image: weevenetwork/fluctuation-filter
    environment:
      MODULE_NAME: fluctuation-filter
      MODULE_TYPE: PROCESS
      WINDOW_SIZE: 3
      SEND_ON_CHANGE: False
      EGRESS_URL: https://hookb.in/r1YwjDyn7BHzWWJVK8Gq
      INGRESS_HOST: 0.0.0.0
      INGRESS_PORT: 80
      INGRESS_PATH: /
      INPUT_LABEL: "temperature"
      OUTPUT_LABEL: "temp"
    ports:
      - 5000:80
```
