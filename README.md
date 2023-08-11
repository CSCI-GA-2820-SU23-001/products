# NYU DevOps Project - Products Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/CSCI-GA-2820-SU23-001/products/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SU23-001/products/actions)
[![Build Status](https://github.com/CSCI-GA-2820-SU23-001/products/actions/workflows/bdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SU23-001/products/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SU23-001/products/branch/master/graph/badge.svg?token=J11SH4LKM0)](https://codecov.io/gh/CSCI-GA-2820-SU23-001/products)

This is the repository for the Products Service project for the NYU DevOps Summer 2023 class.

## Overview

This project template contains starter code for your class project. The `/service` folder contains your `models.py` file for your model and a `routes.py` file for your service. The `/tests` folder has test case starter code for testing the model and the service separately. All you need to do is add your functionality. You can use the [lab-flask-tdd](https://github.com/nyu-devops/lab-flask-tdd) for code examples to copy from.

## Automatic Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```
## Product Service APIs

### Product Operations

| Endpoint         | Methods | Rule
| ---------------  | ------- | --------------------------
| create_a_product | POST    | ```/products```
| read_a_product   | GET     | ```/products/{int:product_id}```
| update_a_product | PUT     | ```/products/{int:product_id}```
| delete_products  | DELETE  | ```/products/{int:product_id}```
| list_products    | GET     | ```/products```
| like_products    | PUT     | ```/products/{int:product_id}/like```
| purchase_product | POST    | ```/products/{int:product_id}/purchase```

## Product Service APIs - Usage 

### Create a Product

URL : `http://127.0.0.1:8000/products`

Method : POST

Auth required : No

Permissions required : No

Create a product using a JSON file that includes the product's name, description, price, category, stock, and creation date.

Example:

Request Body (JSON)
```
{
  "name": "product1",
  "price": 44.5314466590949,
  "desc": "Tv you visit among.\nAway human white much near point market. Movie certainly career sport all model us show. Light assume under bill your.",
  "category": "category10",
  "stock": 31,
  "created_date": "2008-12-03"
}


```

Success Response : `HTTP_201_CREATED`
```
[
  {
    "category": "category10",
    "create_date": "2008-12-03",
    "desc": "Tv you visit among.\nAway human white much near point market. Movie certainly career sport all model us show. Light assume under bill your.",
    "id": 76,
    "name": "product1",
    "price": 44.5314466590949,
    "stock": 31
  }
]

```
### Read a Product

URL : `http://127.0.0.1:8000/products/{int:product_id}`

Method : GET

Auth required : No

Permissions required : No

Reads a product with id provided in the URL

Example:

Success Response : `HTTP_200_OK`
```
[
  {
    "category": "category10",
    "create_date": "2008-12-03",
    "desc": "Tv you visit among.\nAway human white much near point market. Movie certainly career sport all model us show. Light assume under bill your.",
    "id": 76,
    "name": "product1",
    "price": 44.5314466590949,
    "stock": 31
  }
]

```

Failure Response : `HTTP_404_NOT_FOUND`
```
{
  "error": "Not Found",
  "message": "404 Not Found: Product with id '1' was not found.",
  "status": 404
}

```

### Update a Product

URL : `http://127.0.0.1:8000/products/{int:product_id}`

Method : PUT

Auth required : No

Permissions required : No

Updates a product with id provided in the URL according to the updated fields provided in the body

Example:

Request Body (JSON)
```
{
  "name": "product1",
  "price": 44.5314466590949,
  "desc": "Tv you visit among.\nAway human white much near point market. Movie certainly career sport all model us show. Light assume under bill your.",
  "category": "category10",
  "stock": 31,
  "created_date": "2008-12-03"
}

```


Success Response : `HTTP_200_OK`
```
[
  {
    "category": "category10",
    "create_date": "2008-12-03",
    "desc": "Tv you visit among.\nAway human white much near point market. Movie certainly career sport all model us show. Light assume under bill your.",
    "id": 76,
    "name": "product1",
    "price": 44.5314466590949,
    "stock": 31
  }
]

```

Failure Response : `HTTP_404_NOT_FOUND`
```
{
  "error": "Not Found",
  "message": "404 Not Found: Product with id '1' was not found.",
  "status": 404
}

```

### Delete a Product

URL : `http://127.0.0.1:8000/products/{int:product_id}`

Method : DELETE

Auth required : No

Permissions required : No

Deletes a Product with id

Example:

Success Response : `204 NO CONTENT`


### List Products

URL : `http://127.0.0.1:8000/products` 

Method: GET

Auth required : No

Permissions required : No

List All Products

Example:

Success Response : `HTTP_200_OK`

```
[
  {
    "category": "category10",
    "create_date": "2008-12-03",
    "desc": "Tv you visit among.\nAway human white much near point market. Movie certainly career sport all model us show. Light assume under bill your.",
    "id": 76,
    "name": "product1",
    "price": 44.5314466590949,
    "stock": 31
  }
]
```


## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - global configuration for application
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    ├── status.py          - HTTP status constants
    ├── cli_commands.py    - Flask CLI Command Extensions
    └── utils.py           - utils functions


tests/                    - test cases package
├── __init__.py           - package initializer
├── factories.py          - test Factory to make fake objects for testing
├── test_cli_commands.py  - CLI Command Extensions for Flask
├── test_models.py        - test suite for business models
└── test_routes.py        - test suite for service routes

```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
