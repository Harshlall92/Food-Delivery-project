# Software Requirements Specification <!-- omit from toc -->

<!-- Update this information each milestone -->

**Objective:** A Restaurant Library where customers can view search for restaurats, filter restaurants by cuisine type, and veiw the details of a single restaurant. Restaurant owners can create a new restaurant, manage thier restaurant's information, and manage thier restaurant's menu.

**Current Milestone:** Milestone 1

## Table Of Contents <!-- omit from toc -->

- [1. Introduction](#1-introduction)
  - [1.1 Purpose](#11-purpose)
  - [1.2 Document Conventions](#12-document-conventions)
  - [1.3 Scope ](#13-scope-)
    - [1.3.1 In Scope](#131-in-scope)
    - [1.3.2 Specifically Out of Scope](#132-specifically-out-of-scope)
  - [1.4 Definitions \& Acronyms ](#14-definitions--acronyms-)
- [2. Overall Description](#2-overall-description)
  - [2.1 Product Perspective](#21-product-perspective)
  - [2.2 High-Level Architecture](#22-high-level-architecture)
  - [2.2.1 API Layer](#221-api-layer)
  - [2.2.2 Service Layer](#222-service-layer)
  - [2.2.3 Repository Layer](#223-repository-layer)
  - [2.3 Product Functions](#23-product-functions)
  - [2.4 Required Architecture](#24-required-architecture)
  - [2.5 Design and Implementation Constraints](#25-design-and-implementation-constraints)
- [3. Sytem Features and Functional Requirements](#3-sytem-features-and-functional-requirements)
  - [3.1 Database](#31-database)
    - [3.1.1 Restaurants Database](#311-restaurants-database)
    - [3.1.2 Menu Items Database](#312-menu-items-database)
    - [3.1.3 Users Database](#313-users-database)
  - [3.2 Pydantic Models](#32-pydantic-models)
    - [3.2.1 Shared Models](#321-shared-models)
      - [3.2.1.1 BaseAddress Model](#3211-baseaddress-model)
    - [3.2.2 Restaurant Model](#322-restaurant-model)
      - [3.2.2.1 Restaurant Input Model](#3221-restaurant-input-model)
      - [3.2.2.2 Restaurant Output Model](#3222-restaurant-output-model)
    - [3.2.3 Menu Item Model](#323-menu-item-model)
      - [3.2.3.1 Menu Item Input Model](#3231-menu-item-input-model)
      - [3.2.3.2 Menu Item Output Model](#3232-menu-item-output-model)
    - [3.2.4 User Model](#324-user-model)
      - [3.2.4.1 AnyUser Type](#3241-anyuser-type)
      - [3.2.4.2 UserCreate Model](#3242-usercreate-model)
      - [3.2.4.3 UserUpdate Model](#3243-userupdate-model)
    - [3.2.5 Customer Model](#325-customer-model)
      - [3.2.5.1 CustomerAddress Model](#3251-customeraddress-model)
    - [3.2.6 Restaurant Owner Model](#326-restaurant-owner-model)
      - [3.2.6.1 RestaurantOwnerUpdate Model](#3261-restaurantownerupdate-model)
    - [3.2.7 Admin Model](#327-admin-model)
  - [3.3 Repository](#33-repository)
    - [3.3.1 Restaurant Repository](#331-restaurant-repository)
    - [3.3.2 Menu Item Repository](#332-menu-item-repository)
    - [3.3.3 User Repository](#333-user-repository)
  - [3.4 API Routes](#34-api-routes)
    - [3.4.1 Customer Restaurants API Route](#341-customer-restaurants-api-route)
    - [3.4.2 Restaurant Owner Restaurant API](#342-restaurant-owner-restaurant-api)
    - [3.4.3 Restaurant Owner Menu Item API](#343-restaurant-owner-menu-item-api)
    - [3.4.4 Customer Account API](#344-customer-account-api)
    - [3.4.5 Restaurant Owner Account API](#345-restaurant-owner-account-api)
      - [3.4.5.1 Create Restaurant Owner Endpoint](#3451-create-restaurant-owner-endpoint)
      - [3.4.5.2 Update Restaurant Owner Endpoint](#3452-update-restaurant-owner-endpoint)
  - [3.5 Services](#35-services)
    - [3.5.1 Restaurant Services](#351-restaurant-services)
    - [3.5.2 Menu Item Services](#352-menu-item-services)
    - [3.5.3 User Services](#353-user-services)
- [4. External Interface Requirements](#4-external-interface-requirements)
  - [4.1 User Interfaces](#41-user-interfaces)
    - [4.1.1 Customer User Interface](#411-customer-user-interface)
    - [4.1.2 Restaurant Owner User Interface](#412-restaurant-owner-user-interface)
- [5. Non-Functional Requirements](#5-non-functional-requirements)
  - [5.1 README Documentation](#51-readme-documentation)
- [6. Additional Notes](#6-additional-notes)
  - [6.1 Unique Ids \& Data Validation](#61-unique-ids--data-validation)
- [Appendix A: Analysis Models](#appendix-a-analysis-models)
  - [i. Use Case Diagram](#i-use-case-diagram)
  - [ii. Context Diagram](#ii-context-diagram)
  - [iii. Data Flow Diagrams](#iii-data-flow-diagrams)
  - [iv. Database Schema](#iv-database-schema)
  - [v. Data Models](#v-data-models)



---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) document provides a comprehensive description of the Food Delivery Application for the current milestone. The document details the functional and non-functional requirements for the application.

This SRS will serve as the foundation for the subsequent system design and development phases, ensuring that all group members have a clear understanding of what the system will do and how it will operate.


### 1.2 Document Conventions

This document will follow these conventions:

| **Term** | **Description** |
| --- | --- |
| **SHALL** | Refers to a mandatory requirement that must be fufilled for Milestone 1. The group is required to cover this feature in the current implementation phase. |
| **SHOULD** | Indicates a requirement that is not required for this milestone, but may be included |
| **MAY** | Indicates a requirement that is not required for the next two milestones, but may be included in future iterations of the project. |

Requirements are categorized as follows:

| **Requirement Number** | **Description** |
| --- | --- |
| FR- | Functional Requirements |
| NFR- | Non-Functional Requirements |
| DATA- | Data requirements |
| TEST- | Testing requirements |

Every requirement category has its own sub-categories and a unique requirement number for that sub-category.

Examples: `FR-REPO-001` or `FR-API-001`


### 1.3 Scope <!-- needs to be updated for each milestone -->

#### 1.3.1 In Scope

The application will include the following key components:

- View a list of restaurants
- Retrieve the details of a specific restaurant
- view menus from restaurants
- search or filter restaurants
- Creating a restaurant
- Updating retaurant information
- Adding menu items
- Updating menu items

#### 1.3.2 Specifically Out of Scope

- Customer registration
- Restaurant Owner registration
- Authentication
- Authorization
- Shopping Carts
- Checkout
- Orders
- Deliveries

### 1.4 Definitions & Acronyms <!-- needs to be updated for each milestone -->

- **Mutex:** Mutual Exclusion Lock
- **CRUD**: Create, Read Update, and Delete operations

---

## 2. Overall Description

### 2.1 Product Perspective

This stage of the Food Delivery Application is a more comprehensive API, expanding restaurants to include restaurant menu items, along with expanded CRUD for all data.

### 2.2 High-Level Architecture

The Food Delivery Application will follow a layered architecture, consisting of three main layers: the API layer, the Service layer, and the Repository layer. Each layer has distinct responsibilities and interacts with the other layers to provide a cohesive system.

### 2.2.1 API Layer

Handles incoming HTTP requests, and routes them to the appropriate service layer functions. Responsible for request validation, response formatting, and error handling.


### 2.2.2 Service Layer

Handles the orchestration of the application and enforces the business logic. Responsible for validating user input, and interacting with the Repository layer to retrieve and store data.

### 2.2.3 Repository Layer

Handles interaction with the data storage, and performing queries on the data. The repository layer is responsible for reading and writing data to the JSON or CSV files, and ensuring that concurrent write locks are handled properly to prevent data corruption.


### 2.3 Product Functions

This stage of the Food Delivery Application will provide the following major functions:

1. **Restaurant Management**
  - Creating new restaurants
  - Updating existing restaurants
  - Adding menu items
  - Updating menu items
2. **Customer Functionality**
  - Viewing a list of all restaurants
  - Search or filter restaurants
  - Viewing the details of a specific restaurant
  - Viewing a list of menu items of a restaurant

### 2.4 Required Architecture

All interaction between the client and the data must follow the following architecture:

```mermaid
flowchart LR

A[api] --> B[service]
B --> C[repository]
C --> D[JSON/CSV]
```

The client never sees any JSON from `data/`, instead only recieving proper Pydantic models.
The API endpoint is cannot hard-code any 

### 2.5 Design and Implementation Constraints

- Data must be saved as JSON or CSV; No databases are permitted.
- Local file I/O operations must handle concurrent write locks

---

## 3. Sytem Features and Functional Requirements

This section details the functional requirements organized by major system features. Each requirement is identified wih a [unique Id](#12-document-conventions) for treaceability and reference.

---

### 3.1 Database

For more information on the [Database Schema](#iv-database-schema) and [Data Models](#v-data-models), please refer to[Appendix A](#appendix-a-analysis-models).

#### 3.1.1 Restaurants Database

- **DATA-RST-001:** Restaurants SHALL be stored in `data/restaurants.json`
- **DATA-RST-002:** A Restaurant SHALL have a unique id.
- **DATA-RST-003:** A Restaurant SHALL have a name
- **DATA-RST-004:** A restaurant SHALL have a address.
- **DATA-RST-005:** A restaurant SHALL have a cuisine.
- **DATA-RST-006:** A restaurant SHALL have an `active` flag

#### 3.1.2 Menu Items Database

- **DATA-MUI-001:** Menu Items SHALL be stored in `data/menu_items.json`
- **DATA-MUI-002:** A Menu Item SHALL have a unique id.
- **DATA-MUI-003:** A Menu Item SHALL have a link to an exisitng restaurant
- **DATA-MUI-004:** A Menu Item SHALL have a name
- **DATA-MUI-005:** A Menu Item SHALL have a description
- **DATA-MUI-006:** A Menu Item SHALL have a price
- **DATA-MUI-007:** A Menu Item SHALL have an `active` flag

#### 3.1.3 Users Database

- **DATA-USR-001:** Users SHALL be stored in `data/users.json`
- **DATA-USR-002:** A user SHALL have a unique id
- **DATA-USR-003:** A user SHALL have an email address
  - **DATA-USR-003.1:** The email address SHALL be unique
  - **DATA-USR-003.2:** The email address SHALL be normalized to lowercase
- **DATA-USR-004:** A user SHALL have a hashed password
- **DATA-USR-005:** A user SHALL have a first name
- **DATA-USR-006:** A user SHALL have a last name
- **DATA-USR-007:** A user SHALL have an `active` flag
- **DATA-USR-008:** A user SHALL have a role

---

### 3.2 Pydantic Models

#### 3.2.1 Shared Models

##### 3.2.1.1 BaseAddress Model

- **DATA-PYD-057:** The `BaseAddress` model SHALL have an address line 1
  - **DATA-PYD-057.1:** The address line 1 SHALL be a non-empty string
  - **DATA-PYD-057.2:** The address line 1 SHALL have a maximum length of 120 characters
  - **DATA-PYD-057.3:** Surrounding whitespace SHALL be removed from the address line 1
- **DATA-PYD-058:** The `BaseAddress` model SHALL have an address line 2
  - **DATA-PYD-058.1:** The address line 2 SHALL be optional and default to `None`
  - **DATA-PYD-058.2:** The address line 2 SHALL be a non-empty string when it is provided
  - **DATA-PYD-058.3:** The address line 2 SHALL have a maximum length of 120 characters
  - **DATA-PYD-058.4:** Surrounding whitespace SHALL be removed from the address line 2
- **DATA-PYD-059:** The `BaseAddress` model SHALL have a city
  - **DATA-PYD-059.1:** The city SHALL be a non-empty string
  - **DATA-PYD-059.2:** The city SHALL have a maximum length of 50 characters
  - **DATA-PYD-059.3:** Surrounding whitespace SHALL be removed from the city
- **DATA-PYD-060:** The `BaseAddress` model SHALL have a province
  - **DATA-PYD-060.1:** The province SHALL be a two-letter Canadian province or territory code
  - **DATA-PYD-060.2:** The province SHALL accept only `AB`, `BC`, `MB`, `NB`, `NL`, `NS`, `NT`, `NU`, `ON`, `PE`, `QC`, `SK`, or `YT`
- **DATA-PYD-061:** The `BaseAddress` model SHALL have a country
  - **DATA-PYD-061.1:** The country SHALL be a string
  - **DATA-PYD-061.2:** The country SHALL always be set to `Canada`
- **DATA-PYD-062:** The `BaseAddress` model SHALL have a postal code
  - **DATA-PYD-062.1:** The postal code SHALL match the Canadian postal-code format `A1A 1A1`
  - **DATA-PYD-062.2:** The postal-code letters SHALL be uppercase

#### 3.2.2 Restaurant Model

- **DATA-PYD-001:** The `Restaurant` model SHALL have an id
  - **DATA-PYD-001.1:** The `Restaurant` model id SHALL be a UUID
  - **DATA-PYD-001.2:** The `Restaurant` model id SHALL be [unique](Api-Specification.md)
  - **DATA-PYD-001.3:** The `Restaurant` model id SHALL be generated automatically upon creation
  - **DATA-PYD-001.4:** The `Restaurant` model id SHALL be immutable once set
- **DATA-PYD-002:** The `Restaurant` model SHALL have a name
  - **DATA-PYD-002.1:** The name SHALL be a non-empty string
- **DATA-PYD-003:** The `Restaurant` model SHALL have an address
  - **DATA-PYD-003.1:** The address SHALL be a non-empty string
- **DATA-PYD-004:** The `Restaurant` model SHALL have a cuisine
  - **DATA-PYD-004.1:** The cuisine SHALL be a non-empty string
- **DATA-PYD-005:** The `Restaurant` model SHALL have an `active` flag
  - **DATA-PYD-005.1:** The `active` flag SHALL be a boolean

##### 3.2.2.1 Restaurant Input Model

- **DATA-PYD-011:** The `RestaurantInput` model SHALL have a name
  - **DATA-PYD-011.1:** The name SHALL be a non-empty string
- **DATA-PYD-012:** The `RestaurantInput` model SHALL have an address
  - **DATA-PYD-012.1:** The address SHALL be a non-empty string
- **DATA-PYD-013:** The `RestaurantInput` model SHALL have a cuisine
  - **DATA-PYD-013.1:** The cuisine SHALL be a non-empty string

##### 3.2.2.2 Restaurant Output Model

- **DATA-PYD-014:** The `RestauantOutput` model SHALL have an id
  - **DATA-PYD-014.1:** The `RestaurantOutput` model id SHALL be a UUID
  - **DATA-PYD-014.2:** The `RestaurantOutput` model id SHALL be [unique]
- **DATA-PYD-015:** The `RestaurantOutput` model SHALL have a name
  - **DATA-PYD-015.1:** The name SHALL be a non-empty string
- **DATA-PYD-016:** The `RestaurantOutput` model SHALL have an address
  - **DATA-PYD-016.1:** The address SHALL be a non-empty string
- **DATA-PYD-017:** The `RestaurantOutput` model SHALL have a cuisine
  - **DATA-PYD-017.1:** The cuisine SHALL be a non-empty string
- **DATA-PYD-018:** The `RestaurantOutput` model SHALL have an `active` flag
  - **DATA-PYD-018.1:** The `active` flag SHALL be a boolean
- **DATA-PYD-019:** The `RestaurantOutput` model SHALL have a list of menu items
  - **DATA-PYD-019.1:** The list of menu items SHALL be a list of `MenuItem` models
  - **DATA-PYD-019.2:** The list of menu items SHALL be empty if the restaurant has no menu items

#### 3.2.3 Menu Item Model

- **DATA-PYD-006:** The `MenuItem` model SHALL have an id
  - **DATA-PYD-006.1:** The `MenuItem` model id SHALL be a UUID
  - **DATA-PYD-006.2:** The `MenuItem` model id SHALL be [unique](Api-Specification.md)
  - **DATA-PYD-006.3:** THe `MenuItem` model id SHALL be generated automatically upon creation
  - **DATA-PYD-006.4:** The `MenuItem` model id SHALL be immutable once set
- **DATA-PYD-007:** The `MenuItem` model SHALL have a restaurant_id
  - **DATA-PYD-007.1:** The restaurant_id SHALL be a UUID
  - **DATA-PYD-007.2:** The restaurant_id SHALL reference an existing restaurant
  - **DATA-PYD-007.3:** The restaurant_id SHALL be immutable once set
- **DATA-PYD-008:** The `MenuItem` model SHALL have a name
  - **DATA-PYD-008.1:** The name SHALL be a non-empty string
- **DATA-PYD-009:** The `MenuItem` model SHALL have a description
  - **DATA-PYD-009.1:** The description SHALL be a non-empty string
  - **DATA-PYD-009.2:** The description SHALL have a maximum length of 500 characters
- **DATA-PYD-010:** The `MenuItem` model SHALL have a price
  - **DATA-PYD-010.1:** The price SHALL be a Decimal
  - **DATA-PYD-010.2:** The price SHALL be greater than or equal to 0.0
  - **DATA-PYD-010.3:** The price SHALL have at most 2 decimal places

##### 3.2.3.1 Menu Item Input Model

- **DATA-PYD-020:** The `MenuItemInput` model SHALL have a name
  - **DATA-PYD-020.1:** The name SHALL be a non-empty string
- **DATA-PYD-021:** The `MenuItemInput` model SHALL have a description
  - **DATA-PYD-021.1:** The description SHALL be a non-empty string
  - **DATA-PYD-021.2:** The description SHALL have a maximum length of 500 characters
- **DATA-PYD-022:** The `MenuItemInput` model SHALL have a price
  - **DATA-PYD-022.1:** The price SHALL be a Decimal
  - **DATA-PYD-022.2:** The price SHALL be greater than or equal to 0.0
  - **DATA-PYD-022.3:** The price SHALL have at most 2 decimal places

##### 3.2.3.2 Menu Item Output Model

- **DATA-PYD-023:** The `MenuItemOutput` model SHALL have an id
  - **DATA-PYD-023.1:** The `MenuItemOutput` model id SHALL be a UUID
  - **DATA-PYD-023.2:** The `MenuItemOutput` model id SHALL be [unique]
- **DATA-PYD-024:** The `MenuItemOutput` model SHALL have a name
  - **DATA-PYD-024.1:** The name SHALL be a non-empty string
- **DATA-PYD-025:** THe `MenuItemOutput` model SHALL have a description
  - **DATA-PYD-025.1:** The description SHALL be a non-empty string
  - **DATA-PYD-025.2:** The description SHALL have a maximum length of 500 characters
- **DATA-PYD-026:** The `MenuItemOutput` model SHALL have a price
  - **DATA-PYD-026.1:** The price SHALL be a Decimal
  - **DATA-PYD-026.2:** The price SHALL be greater than or equal to 0.0
  - **DATA-PYD-026.3:** The price SHALL have at most 2 decimal places
- **DATA-PYD-027:** The `MenuItemOutput` model SHALL have an `active` flag

#### 3.2.4 User Model

- **DATA-PYD-028:** The `User` model SHALL have an id
  - **DATA-PYD-028.1:** The `User` model id SHALL be a UUID
  - **DATA-PYD-028.2:** The `User` model id SHALL be unique
  - **DATA-PYD-028.3:** The `User` model id SHALL be generated automatically upon creation
  - **DATA-PYD-028.4:** The `User` model id SHALL be immutable once set
- **DATA-PYD-029:** The `User` model SHALL have an email
  - **DATA-PYD-029.1:** The email SHALL be a valid email address
  - **DATA-PYD-029.2:** The email SHALL be unique
  - **DATA-PYD-029.3:** The email SHALL be normalized to lowercase
- **DATA-PYD-030:** The `User` model SHALL have a password
  - **DATA-PYD-030.1:** The password SHALL be a non-empty string
  - **DATA-PYD-030.2:** The password SHALL not contain whitespace
  - **DATA-PYD-030.3:** The password SHALL be hashed before being stored
- **DATA-PYD-031:** The `User` model SHALL have a first name
  - **DATA-PYD-031.1:** The first name SHALL be a non-empty string
  - **DATA-PYD-031.2:** The first name SHALL be stripped and converted to title case
- **DATA-PYD-032:** The `User` model SHALL have a last name
  - **DATA-PYD-032.1:** The last name SHALL be a non-empty string
  - **DATA-PYD-032.2:** The last name SHALL be stripped and converted to title case
- **DATA-PYD-033:** The `User` model SHALL have an `active` flag
  - **DATA-PYD-033.1:** The `active` flag SHALL be a boolean
  - **DATA-PYD-033.2:** The `active` flag SHALL default to `True`

##### 3.2.4.1 AnyUser Type

- **DATA-PYD-034:** The `AnyUser` type SHALL be a union of the `Customer`, `RestaurantOwner`, and `Admin` models determined by the `role` attribute

##### 3.2.4.2 UserCreate Model

- **DATA-PYD-035:** The `UserCreate` model SHALL have an email
  - **DATA-PYD-035.1:** The email SHALL be a valid email address
- **DATA-PYD-036:** The `UserCreate` model SHALL have a password
  - **DATA-PYD-036.1:** The password SHALL be a non-empty string
- **DATA-PYD-037:** The `UserCreate` model SHALL have a confirm password
  - **DATA-PYD-037.1:** The confirm password SHALL be a non-empty string
  - **DATA-PYD-037.2:** The confirm password SHALL match the password
- **DATA-PYD-038:** The `UserCreate` model SHALL have a first name
  - **DATA-PYD-038.1:** The first name SHALL be a non-empty string
- **DATA-PYD-039:** The `UserCreate` model SHALL have a last name
  - **DATA-PYD-039.1:** The last name SHALL be a non-empty string

##### 3.2.4.3 UserUpdate Model

- **DATA-PYD-040:** The `UserUpdate` model SHALL have an email
  - **DATA-PYD-040.1:** The email SHALL be a valid email address
  - **DATA-PYD-040.2:** The email SHALL be optional and default to `None`
- **DATA-PYD-041:** The `UserUpdate` model SHALL have a password
  - **DATA-PYD-041.1:** The password SHALL be a non-empty string
  - **DATA-PYD-041.2:** The password SHALL be optional and default to `None`
- **DATA-PYD-042:** The `UserUpdate` model SHALL have a confirm password
  - **DATA-PYD-042.1:** The confirm password SHALL be optional and default to `None`
  - **DATA-PYD-042.2:** The confirm password SHALL match the password when a password is provided
- **DATA-PYD-043:** The `UserUpdate` model SHALL have a first name
  - **DATA-PYD-043.1:** The first name SHALL be optional and default to `None`
- **DATA-PYD-044:** The `UserUpdate` model SHALL have a last name
  - **DATA-PYD-044.1:** The last name SHALL be optional and default to `None`
- **DATA-PYD-053:** The `UserUpdate` model SHALL have an `active` flag
  - **DATA-PYD-053.1:** The `active` flag SHALL be a boolean
  - **DATA-PYD-053.2:** The `active` flag SHALL be optional and default to `None`

#### 3.2.5 Customer Model

- **DATA-PYD-045:** The `Customer` model SHALL extend the `User` model
- **DATA-PYD-046:** The `Customer` model SHALL have a role
  - **DATA-PYD-046.1:** The role SHALL be a string that is always set to `customer`
- **DATA-PYD-047:** The `Customer` model SHALL have a list of `CustomerAddress` models
  - **DATA-PYD-047.1:** The list of addresses SHALL default to an empty list
- **DATA-PYD-048:** The `Customer` model SHOULD have a payment method
  - **DATA-PYD-048.1:** The payment method SHALL be a string
  - **DATA-PYD-048.2:** The payment method SHALL be optional and default to `None`

##### 3.2.5.1 CustomerAddress Model

- **DATA-PYD-049:** The `CustomerAddress` model SHALL extend the `BaseAddress` model
- **DATA-PYD-054:** The `CustomerAddress` model SHALL have a label
  - **DATA-PYD-054.1:** The label SHALL be a non-empty string
  - **DATA-PYD-054.2:** The label SHALL have a maximum length of 50 characters
  - **DATA-PYD-054.3:** The label SHALL default to `Home`

#### 3.2.6 Restaurant Owner Model

- **DATA-PYD-050:** The `RestaurantOwner` model SHALL extend the `User` model
- **DATA-PYD-051:** The `RestaurantOwner` model SHALL have a role
  - **DATA-PYD-051.1:** The role SHALL be a string that is always set to `restaurant_owner`
- **DATA-PYD-052:** The `RestaurantOwner` model SHALL have a `restaurant_id`
  - **DATA-PYD-052.1:** The `restaurant_id` SHALL be optional and default to `None`
  - **DATA-PYD-052.2:** The `restaurant_id` SHALL reference an existing restaurant when it is not `None`

##### 3.2.6.1 RestaurantOwnerUpdate Model

- **DATA-PYD-055:** The `RestaurantOwnerUpdate` model SHALL extend the `UserUpdate` model
- **DATA-PYD-056:** The `RestaurantOwnerUpdate` model SHALL have a `restaurant_id`
  - **DATA-PYD-056.1:** The `restaurant_id` SHALL be optional and default to `None`
  - **DATA-PYD-056.2:** The `restaurant_id` SHALL reference an existing restaurant when it is not `None`

#### 3.2.7 Admin Model

- **DATA-PYD-063:** The `Admin` model SHALL extend the `User` model
- **DATA-PYD-063:** The `Admin` model SHALL have a role
  - **DATA-PYD-063.1:** The role SHALL be a string that is always set to `admin`
- **DATA-PYD-064:** The `Admin` model SHALL have a list of permissions
  - **DATA-PYD-064.1:** The list of permissions SHALL default to an empty list

---

### 3.3 Repository

- **FR-REPO-001:** A repository SHALL have a file path to a JSON or CSV file
- **FR-REPO-002:** A repository SHALL be able to write ti the file
- **FR-REPO-003:** A repository SHALL be able to read from the file
- **FR-REPO-004:** A repository SHALL be able to handle concurrent write locks to the file
- **FR-REPO-005**: A repository SHALL be able to handle file not found errors gracefully
  - **FR-REPO-005.1:** The repository SHALL return an empty list if the file is not found
  - **FR-REPO-005.2:** The repository SHALL create a new file if the file is not found when writing data
- **FR-REPO-006:** A repository SHALL be able to be able to return a list of all items in the repository
- **FR-REPO-007:** A repository SHALL be able to retrieve an item by its unique id
  - **FR-REPO-007.1:** The repository SHALL return `None` if the item is not found
- **FR-REPO-008:** A repository SHALL be able to add a new item to the file
- **FR-REPO-009:** A repository SHALL be able to update an existing item in the file
- **FR-REPO-010:** A repository SHOULD be able to delete an existing item from the file

#### 3.3.1 Restaurant Repository

- **FR-REPO-011:** The restaurant repository SHALL have a file path of `data/restaurants.json`
- **FR-REPO-012:** The restaurant repository SHALL be able to search for restauarnts by name
  - **FR-REPO-012.1:** The search SHALL be case-insensitive
  - **FR-REPO-012.2:** The search SHALL return a list of matching restaurants
  - **FR-REPO-012.3:** The search SHALL return an empty list if no matching restaurants are found
- **FR-REPO-013:** The restaurant repository SHALL be able to retrieve all cuisines from the list of restaurants
  - **FR-REPO-013.1:** Cuisine types SHALL be normalized
  - **FR-REPO-013.2:** The list of cuisines SHALL be unique
- **FR-REPO-014:** The restaurant repository SHALL use the `Restaurant` model as its type parameter

#### 3.3.2 Menu Item Repository

- **FR-REPO-015:** The menu item repository SHALL have a file path of `data/menu_items.json`
- **FR-REPO-016:** The menu item repository SHALL be able to retrieve all menu items for a specific restaurant
  - **FR-REPO-016.1:** The repository SHALL return an empty list if no menu items are found for the restaurant
- **FR-REPO-017:** The menu item repository SHALL use the `MenuItem` model as its type parameter

#### 3.3.3 User Repository

- **FR-REPO-018:** The user repository SHALL have a file path of `data/users.json`
- **FR-REPO-019:** The user repository SHALL use the `AnyUser` type as its type parameter
- **FR-REPO-020:** The user repository SHALL determine whether an email address already exists
  - **FR-REPO-020.1:** The repository SHALL return `True` when the email address exists
  - **FR-REPO-020.2:** The repository SHALL return `False` when the email address does not exist

---

### 3.4 API Routes

- **FR-API-001:** Accessing the `GET /` endpoint SHALL return `"Welcome to the Pilates Princess Food Delivery Service!"`.
- **FR-API-002:** Accessing the `GET /health` endpoint SHALL return `HTTP 200`.

#### 3.4.1 Customer Restaurants API Route

##### 3.4.1.1 Index Endpoint <!-- omit from toc -->

- **FR-API-003:** The index of the route SHALL be defined as `GET /restaurants`
  
- **FR-API-004:** The index SHALL return a list of all restaurants
  - **FR-API-004.1:** The index SHALL return `HTTP 200` if the request is successful
  - **FR-API-004.2:** The index SHALL return a list of restaurant objects

- **FR-API-005:** The index SHALL support searching for restaurants by name
  - **FR-API-005.1:** The endpoint SHALL be defined as `GET /restaurants?search={name}` 
  - **FR-API-005.2:** The search SHALL be case-insensitive
  - **FR-API-005.3:** The search SHALL return a list of matching restaurants
  - **FR-API-005.4:** The search SHALL return an empty list if no matching restaurants are found
  
- **FR-API-006:** The index SHALL support filtering restaurants by cuisine type
  - **FR-API-006.1:** The endpoint SHALL be defined as `GET /restaurants?cuisine={cuisine}`
  - **FR-API-006.2:** The filter SHALL be case-insensitive
  - **FR-API-006.3:** The filter SHALL return a list of matching restaurants

##### 3.4.1.2 Get by Id Endpoint <!-- omit from toc -->
- **FR-API-007:** The route must expose an endpoint to retrieve the details of a specific restaurant by its unique id
  - **FR-API-007.1:** The endpoint SHALL be defined as `GET /restaurants/{restaurant_id}`
  - **FR-API-007.2:** The endpoint SHALL return `HTTP 200` if the request is successful
  - **FR-API-007.3:** The endpoint SHALL return a `RestaurantOutput` object
  - **FR-API-007.4:** The endpoint SHALL return `HTTP 404` if the restaurant is not found

#### 3.4.2 Restaurant Owner Restaurant API

##### 3.4.2.1 Index Endpoint <!-- omit from toc -->

- **FR-API-008:** The index of the route SHALL be defined as `GET /restaurants`
- **FR-API-009:** The index SHALL return a list of all restaurants
  - **FR-API-009.1:** The index SHALL return `HTTP 200` if the request is successful
  - **FR-API-009.2:** The index SHALL return a list of restaurant objects

##### 3.4.2.2 Create Endpoint <!-- omit from toc -->

- **FR-API-010:** The route must expose an endpoint to create a new restaurant
- **FR-API-010.1:** The endpoint SHALL be defined as `POST /restaurants`
  - **FR-API-010.2:** The endpoint SHALL accept a `RestaurantInput` object
  - **FR-API-010.3:** The endpoint SHALL return `HTTP 201` if the restaurant is created successfully
  - **FR-API-010.4:** The endpoint SHALL return a `RestaurantOutput` object

##### 3.4.2.3 Get by Id Endpoint <!-- omit from toc -->

- **FR-API-011:** The route must expose an endpoint to view the details of a specific restaurant by its unique id
  - **FR-API-011.1:** The endpoint SHALL be defined as `GET /restaurants/{restaurant_id}`
  - **FR-API-011.2:** The endpoint SHALL return `HTTP 200` if the request is successful
  - **FR-API-011.3:** The endpoint SHALL return a `RestaurantOutput` object
  - **FR-API-011.4:** The endpoint SHALL return `HTTP 404` if the restaurant is not found

##### 3.4.2.4 Update Endpoint <!-- omit from toc -->

- **FR-API-012:** The route must expose an endpoint to update the details of a specific restaurant by its unique id
  - **FR-API-012.1:** The endpoint SHALL be defined as `PUT /restaurants/{restaurant_id}`
  - **FR-API-012.2:** The endpoint SHALL accept a `RestaurantInput` object
  - **FR-API-012.3:** The endpoint SHALL return `HTTP 200` if the restaurant is updated successfully
  - **FR-API-012.4:** The endpoint SHALL return a `RestaurantOutput` object
  - **FR-API-012.5:** The endpoint SHALL return `HTTP 404` if the restaurant is not found

#### 3.4.3 Restaurant Owner Menu Item API

##### 3.4.3.1 Add Menu Items for Restaurant Endpoint <!-- omit from toc -->

- **FR-API-013:** The endpoint SHALL expose an endpoint to add a new menu item to a specific restaurant by its unique id
  - **FR-API-013.1:** The endpoint SHALL be defined as `POST /restaurants/{restaurant_id}/menu`
  - **FR-API-013.2:** The endpoint SHALL accept a `MenuItemInput` object
  - **FR-API-013.3:** The endpoint SHALL return `HTTP 201` if the menu item is created successfully
  - **FR-API-013.4:** The endpoint SHALL return a `MenuItemOutput` object
  - **FR-API-013.5:** The endpoint SHALL return `HTTP 404` if the restaurant is not found

##### 3.4.3.2 Get Menu Item by Id Endpoint <!-- omit from toc -->

- **FR-API-014:** The endpoint SHALL expose an endpoint to view the details of a specific menu item by its unique id
  - **FR-API-014.1:** The endpoint SHALL be defined as `GET /restaurants/{restaurant_id}/menu/{menu_item_id}`
  - **FR-API-014.2:** The endpoint SHALL return `HTTP 200` if the request is successful
  - **FR-API-014.3:** The endpoint SHALL return a `MenuItemOutput` object
  - **FR-API-014.4:** The endpoint SHALL return `HTTP 404` if the restaurant or menu item is not found
  
##### 3.4.3.3 Update Menu Item Endpoint <!-- omit from toc -->

- **FR-API-015:** The endpoint SHALL expose an endpoint to update the details of a specific menu item by its unique id
  - **FR-API-015.1:** The endpoint SHALL be defined as `PUT /restaurants/{restaurant_id}/menu/{menu_item_id}`
  - **FR-API-015.2:** The endpoint SHALL accept a `MenuItemInput` object
  - **FR-API-015.3:** The endpoint SHALL return `HTTP 200` if the menu item is updated successfully
  - **FR-API-015.4:** The endpoint SHALL return a `MenuItemOutput` object
  - **FR-API-015.5:** The endpoint SHALL return `HTTP 404` if the restaurant or menu item is not found

#### 3.4.4 Customer Account API

##### 3.4.4.1 Create Customer Endpoint <!-- omit from toc -->

- **FR-API-016:** The system SHALL expose `POST /api/users/c` to create a customer account
  - **FR-API-016.1:** The endpoint SHALL accept a `UserCreate` object
  - **FR-API-016.2:** The endpoint SHALL return `HTTP 201` and the created `Customer` if creation succeeds
  - **FR-API-016.3:** The endpoint SHALL return `HTTP 409` if the email address already exists
  - **FR-API-016.4:** The endpoint SHALL return `HTTP 422` if the input data is invalid

##### 3.4.4.2 Update Customer Endpoint <!-- omit from toc -->

- **FR-API-017:** The system SHALL expose `PATCH /api/users/c/{customer_id}` to update a customer account
  - **FR-API-017.1:** The endpoint SHALL accept a `UserUpdate` object
  - **FR-API-017.2:** The endpoint SHALL return `HTTP 200` and the updated `Customer` if updating succeeds
  - **FR-API-017.3:** The endpoint SHALL return `HTTP 404` if the customer does not exist
  - **FR-API-017.4:** The endpoint SHALL return `HTTP 409` if the updated email address already exists
  - **FR-API-017.5:** The endpoint SHALL return `HTTP 422` if the input data is invalid

#### 3.4.5 Restaurant Owner Account API

##### 3.4.5.1 Create Restaurant Owner Endpoint

- **FR-API-018:** The system SHALL expose `POST /api/users/r` to create a restaurant owner account
  - **FR-API-018.1:** The endpoint SHALL accept a `UserCreate` object
  - **FR-API-018.2:** The endpoint SHALL return `HTTP 201` and the created `RestaurantOwner` if creation succeeds
  - **FR-API-018.3:** The endpoint SHALL return `HTTP 409` if the email address already exists
  - **FR-API-018.4:** The endpoint SHALL return `HTTP 422` if the input data is invalid

##### 3.4.5.2 Update Restaurant Owner Endpoint

- **FR-API-019:** The system SHALL expose `PATCH /api/users/r/{owner_id}` to update a restaurant owner account
  - **FR-API-019.1:** The endpoint SHALL accept a `RestaurantOwnerUpdate` object
  - **FR-API-019.2:** The endpoint SHALL return `HTTP 200` and the updated `RestaurantOwner` if updating succeeds
  - **FR-API-019.3:** The endpoint SHALL return `HTTP 404` if the restaurant owner does not exist
  - **FR-API-019.4:** The endpoint SHALL return `HTTP 404` if the provided restaurant does not exist
  - **FR-API-019.5:** The endpoint SHALL return `HTTP 409` if the updated email address already exists
  - **FR-API-019.6:** The endpoint SHALL return `HTTP 422` if the input data is invalid

---

### 3.5 Services

For aid in the development of services, please refer to the diagram in [Appendix A](#appendix-a-analysis-models) for a visual representation of the service layer and its interactions with the API and Repository layers.

Note, not all services have diagrams, but the diagrams that are present should provide a good reference for the development of the services.

#### 3.5.1 Restaurant Services

##### 3.5.1.1 Create Models <!-- omit from toc -->

- **FR-SERV-001:** The service SHALL provide a function to create a `Restaurant` object from raw json data
- **FR-SERV-002:** The service SHALL provide a function to create a `Restaurant` object from a `RestaurantInput`
- **FR-SERV-003:** The service SHALL provie a function to create a `RestaurantOutput` object from a `Restaurant` and a list of `MenuItemOutput` objects

##### 3.5.1.2 Interaction with Repository <!-- omit from toc -->

###### 3.5.1.2.1 CRUD Operations <!-- omit from toc -->

- **FR-SERV-004:** The service SHALL provide a function to retrieve all restaurants from the restaurant repository
  - **FR-SERV-004.1:** The service SHALL convert the restaurant data from the repository into a list of `RestaurantOutput` objects before returning it
  - **FR-SERV-004.2:** The service SHALL raise an error if any restaurant data is invalid or incomplete
- **FR-SERV-005:** The service SHALL provide a function to add a new restaurant to the restaurant repository
  - **FR-SERV-005.1:** The service SHALL validate the input data before adding the restaurant
  - **FR-SERV-005.2:** The service SHALL return a `RestaurantOutput` object if the restaurant is added successfully
  - **FR-SERV-005.3:** The service SHALL raise an error if the input data is invalid or incomplete
- **FR-SERV-006:** The service SHALL provide a function to retrieve a specific restaurant by its unique id from the restaurant repository
  - **FR-SERV-006.1:** The service SHALL convert the restaurant data from the repository into a `RestaurantOutput` object before returning it
  - **FR-SERV-006.2:** The service SHALL return `None` if the restaurant is not found
- **FR-SERV-007:** The service SHALL provide a function to update an existing restaurant in the restaurant repository
  - **FR-SERV-007.1:** The service SHALL validate the input data before updating the restaurant
  - **FR-SERV-007.2:** The service SHALL return a `RestaurantOutput` object if the restaurant is updated successfully
  - **FR-SERV-007.3:** The service SHALL raise an error if the input data is invalid or incomplete
  - **FR-SERV-007.4:** The service SHALL return `None` if the restaurant is not found

###### 3.5.1.2.2 Queries <!-- omit from toc -->

- **FR-SERV-008:** The service SHALL provide a function to search for restaurants by name from the restaurant repository
  - **FR-SERV-008.1:** The service SHALL convert the restaurant data from the repository into a list of `RestaurantOutput` objects before returning it
- **FR-SERV-009:** The service SHALL provide a function to retrieve all cuisines from the list of restaurants in the restaurant repository
  - **FR-SERV-009.1:** The service SHALL return a list of unique cuisine types
- **FR-SERV-01-:** The service SHALL provide a function to filter restaurants by cuisine type from the restaurant repository
  - **FR-SERV-010.1:** The service SHALL convert the restaurant data from the repository into a list of `RestaurantOutput` objects before returning it

##### 3.5.1.3 Interaction with API Layer <!-- omit from toc -->

- **FR-SERV-011:** The service SHALL provide a function to handle a request to retrieve all restaurants from the restaurant repository
- **FR-SERV-012:** The service SHALL provide a function to handle a request to add a new restaurant to the restaurant repository
- **FR-SERV-013:** The service SHALL provide a function to handle a request to retrieve a specific restaurant by its unique id from the restaurant repository
- **FR-SERV-014:** The service SHALL provide a function to handle a request to update an existing restaurant in the restaurant repository
- **FR-SERV-015:** The service SHALL provide a function to handle a request to search for restaurants by name from the restaurant repository
- **FR-SERV-016:** The service SHALL provide a function to handle a request to retrieve all cuisines from the list of restaurants in the restaurant repository
- **FR-SERV-017:** The service SHALL provide a function to handle a request to filter restaurants by cuisine type from the restaurant repository

#### 3.5.2 Menu Item Services

##### 3.5.2.1 Create Models <!-- omit from toc -->
- **FR-SERV-018:** The service SHALL provide a function to create a `MenuItem` object from raw json data
- **FR-SERV-019:** The service SHALL provide a function to create a `MenuItem` object from a `MenuItemInput`
- **FR-SERV-020:** The service SHALL provide a function to create a `MenuItemOutput` object from a `MenuItem`

##### 3.5.2.2 Interaction with Repository <!-- omit from toc -->

- **FR-SERV-021:** The service SHALL provide a function to retrieve all menu items for a specific restaurant from the menu item repository
  - **FR-SERV-021.1:** The service SHALL convert the menu item data from the repository into a list of `MenuItemOutput` objects before returning it
  - **FR-SERV-021.2:** The service SHALL raise an error if any menu item data is invalid or incomplete
- **FR-SERV-022:** The service SHALL provide a function to add a new menu item to the menu item repository
  - **FR-SERV-022.1:** The service SHALL validate the input data before adding the menu item
  - **FR-SERV-022.2:** The service SHALL return a `MenuItemOutput` object if the menu item is added successfully
  - **FR-SERV-022.3:** The service SHALL raise an error if the input data is invalid or incomplete
- **FR-SERV-023:** The service SHALL provide a function to retrieve a specific menu item by its unique id from the menu item repository
  - **FR-SERV-023.1:** The service SHALL convert the menu item data from the repository into a `MenuItemOutput` object before returning it
  - **FR-SERV-023.2:** The service SHALL return `None` if the menu item is not found
- **FR-SERV-024:** The service SHALL provide a function to update an existing menu item in the menu item repository
  - **FR-SERV-024.1:** The service SHALL validate the input data before updating the menu item
  - **FR-SERV-024.2:** The service SHALL return a `MenuItemOutput` object if the menu item is updated successfully
  - **FR-SERV-024.3:** The service SHALL raise an error if the input data is invalid or incomplete
  - **FR-SERV-024.4:** The service SHALL return `None` if the menu item is not found

##### 3.5.2.3 Interaction with API Layer <!-- omit from toc -->

- **FR-SERV-025:** The service SHALL provide a function to handle a request to create a new menu item in the menu item repository
- **FR-SERV-026:** The service SHALL provide a function to handle a request to retrieve all menu items for a specific restaurant from the menu item repository
- **FR-SERV-027:** The service SHALL provide a function to handle a request to retrieve a specific menu item by its unique id from the menu item repository
- **FR-SERV-028:** The service SHALL provide a function to handle a request to update an existing menu item in the menu item repository

#### 3.5.3 User Services

- **FR-SERV-029:** The service SHALL create a `Customer` from a `UserCreate` object
  - **FR-SERV-029.1:** The service SHALL raise `DuplicateItemError` if the email address already exists
  - **FR-SERV-029.2:** The service SHALL persist the customer in the user repository
- **FR-SERV-030:** The service SHALL update an existing customer using a `UserUpdate` object
  - **FR-SERV-030.1:** The service SHALL raise `UserNotFoundError` if the customer does not exist
  - **FR-SERV-030.2:** The service SHALL apply only fields explicitly included in the update
  - **FR-SERV-030.3:** The service SHALL raise `DuplicateItemError` if the updated email address belongs to another user
  - **FR-SERV-030.4:** The service SHALL persist and return the updated customer
- **FR-SERV-031:** The service SHALL create a `RestaurantOwner` from a `UserCreate` object
  - **FR-SERV-031.1:** The service SHALL raise `DuplicateItemError` if the email address already exists
  - **FR-SERV-031.2:** The service SHALL persist the restaurant owner in the user repository
- **FR-SERV-032:** The service SHALL update an existing restaurant owner using a `RestaurantOwnerUpdate` object
  - **FR-SERV-032.1:** The service SHALL raise `UserNotFoundError` if the restaurant owner does not exist
  - **FR-SERV-032.2:** The service SHALL verify that a provided `restaurant_id` references an existing restaurant
  - **FR-SERV-032.3:** The service SHALL raise `RestaurantNotFoundError` if the provided restaurant does not exist
  - **FR-SERV-032.4:** The service SHALL apply only fields explicitly included in the update
  - **FR-SERV-032.5:** The service SHALL raise `DuplicateItemError` if the updated email address belongs to another user
  - **FR-SERV-032.6:** The service SHALL persist and return the updated restaurant owner
  
---

## 4. External Interface Requirements

This section describes the requirements for the external interfaces of the system, including user interfaces, hardware interfaces, software interfaces, and communication interfaces.

### 4.1 User Interfaces

#### 4.1.1 Customer User Interface

- **FR-UI-001:** The system SHALL provide a user interface for customers to view a list of restaurants.
  - **FR-UI-001.1:** Linked to the API endpoint `GET /restaurants`
- **FR-UI-002:** The system SHALL provide a user interface for customers to view the details of a specific restaurant.
  - **FR-UI-002.1:** Linked to the API endpoint `GET /restaurants/{restaurant_id}`
- **FR-UI-003:** The system SHALL provide a user interface for customers to search for restaurants by name.
  - **FR-UI-003.1:** Linked to the API endpoint `GET /restaurants?search={name}`
- **FR-UI-004:** The system SHALL provide a user interface for customers to filter restaurants by cuisine type.
  - **FR-UI-004.1:** Linked to the API endpoint `GET /restaurants?cuisine={cuisine}`

#### 4.1.2 Restaurant Owner User Interface

- **FR-UI-005:** The system SHALL provide a user interface for restaurant owners to create a new restaurant.
  - **FR-UI-005.1:** Linked to the API endpoint `POST /restaurants`
  - **FR-UI-005.2:** Form should include fields as defined in the `RestaurantInput` model
- **FR-UI-006:** The system SHALL provide a user interface for restaurant owners to update the details of an existing restaurant.
  - **FR-UI-006.1:** Linked to the API endpoint `PUT /restaurants/{restaurant_id}`
  - **FR-UI-006.2:** Editable data should be limited to fields defined in the `RestaurantInput` model
  - **FR-UI-006.3:** Fields should be pre-populated with the current restaurant data
- **FR-UI-007:** The system SHALL provide a user interface for restaurant owners to add a new menu item to a specific restaurant.
  - **FR-UI-007.1:** Linked to the API endpoint `POST /restaurants/{restaurant_id}/menu`
  - **FR-UI-007.2:** Form should include fields as defined in the `MenuItemInput` model
  - **FR-UI-007.3:** The form should be associated with the specific restaurant identified by `{restaurant_id}`
- **FR-UI-008:** The system SHALL provide a user interface for restaurant owners to update the details of an existing menu item.
  - **FR-UI-008.1:** Linked to the API endpoint `PUT /restaurants/{restaurant_id}/menu/{menu_item_id}`
  - **FR-UI-008.2:** Editable data should be limited to fields defined in the `MenuItemInput` model
  - **FR-UI-008.3:** Fields should be pre-populated with the current menu item data
- **FR-UI-009:** The system SHALL provide a user interface for restaurant owners to view the details of a specific menu item.
  - **FR-UI-009.1:** Linked to the API endpoint `GET /restaurants/{restaurant_id}/menu/{menu_item_id}`

---

## 5. Non-Functional Requirements

### 5.1 README Documentation

- **NFR-RDME-001:** `README.md` SHALL contain enough information for a new team member or TA to run the project
- **NFR-RDME-002:** The team name SHALL be listed
- **NFR-RDME-003:** The required python version SHALL be listed
- **NFR-RDME-004:** Setup instructions SHALL be included
  - **NFR-RDME-004.1:** Instructions for cloning the project
  - **NFR-RDME-004.2:** Instructions for setting up the virtual environment
  - **NFR-RDME-004.3:** Instructions for installing necessary dependencies
  - **NFR-RDME-004.4:** Instructions for how to start the application
- **NFR-RDME-005:** API endpoint paths must be listed
  - **NFR-RDME-005.1:** The base URL of the API must be provided
  - **NFR-RDME-005.2:** Each endpoint must be documented with its method, path, and description
- **NFR-RDME-006:** The `/docs` path must be listed.
- **NFR-RDME-007:** The location and format of represented data must be provided
- **NFR-RDME-008:** Instructions for how to run tests must be listed
- **NFR-RDME-009:** A brief repository structure must be included

---

## 6. Additional Notes

### 6.1 Unique Ids & Data Validation

The majority of the data validation is handled by Pydantic models, which are used to validate the data before it is saved to the repository. 

Please read the documentation for the [`Field`](https://pydantic.dev/docs/validation/dev/concepts/field/) class for more information on how to validate data using Pydantic.


The unique ids for restaurants and menu items are generated using the `uuid` library, which ensures that each id is unique.
Using `default_factory=uuid.uuid7` in the Pydantic model ensures that a new unique id is generated for each new restaurant or menu item.

---

## Appendix A: Analysis Models

### i. Use Case Diagram

**i.a Customer**

```mermaid
flowchart
direction LR
subgraph "Food Delivery Application"
  A(View a list of restaurants)
  B(Filter restaurants by category)
  C(Search for restaurants by name)
  D(View details of a single restaurant)
  E(View menu of a single restaurant)
  F(Create a customer account)
  G(Update existing account information)
end

Customer@{shape: person, label: "Customer"}

Customer --> A
Customer --> B
Customer --> C
Customer --> D
Customer --> E
Customer --> F
Customer --> G
```

**i.a Restaurant Owner**

```mermaid
flowchart
direction LR

subgraph "Food Delivery Application"
  F(Create a restaurant)
  G(Update a restaurant)
  H(Add a menu item)
  I(Update a menu item)
  J(View details of a single menu item)
  K(Create a restaurant owner account)
  L(Update a restaurant owner account information)
end


RestaurantOwner@{shape: person, label: "Restaurant Mangager"}

RestaurantOwner --> F
RestaurantOwner --> G
RestaurantOwner --> H
RestaurantOwner --> I
RestaurantOwner --> J
RestaurantOwner --> K
RestaurantOwner --> L
```

### ii. Context Diagram

**ii.a System Boundaries and external entities (Level 0)**

```mermaid
flowchart LR

A[Customers] --> | Finds a restaurant | B[Food Delivery Application]
B --> | Restaurant information and Menu | A
C[Restaurant Manager / Administrator] --> | Create / Update Restaurant | B
```

**ii.b Data flows between the system and external entities (Level 1)**

```mermaid
flowchart LR
subgraph Food Delivery Application
    A(Restaurant Endppont) -- Restaurant id --> B(Id Validation)
    B -- Validated id --> DATA[(restaurants.json)]
    DATA -- Raw restaurant data --> C(Data Model Builder)
    C -- Restaurant --> A
    D -- Restaurant data --> E(Data Validation)
    E -- Validated data --> DATA
end
EXT1[Customers] -- Get Restaurant --> A(Restaurant Endpoint)
A -- Restaurant --> EXT1
EXT2[Restaurant Manager / Administrator] -- Create Restaurant --> D(Restaurant Endpoint)
```

### iii. Data Flow Diagrams

**iii.a Create Restaurant**

```mermaid
---
config:
  layout: fixed
---
flowchart TB
 subgraph subGraph0["API Layer"]
        A("Receive Restaurant Creation Request")
        E("Return Response")
  end
 subgraph subGraph1["Service Layer"]
        B{"Validate on Restaurant Model"}
        F("Raise HTTP 422")
        C("Build Restaurant Model")
        G("Return Success")
  end
 subgraph subGraph2["Repository Layer"]
        D("Save to Database")
  end
    START["START"] --> Actor["Restaurant Owner"]
    Actor -- RestaurantInput --> A
    A --> B
    B -- Invalid Data --> F
    E --> END2["END2"]
    B -- Valid Data --> C
    C -- Restaurant --> D
    D --> END1["END1"] & G
    F --> E
    G --> E

    START@{ shape: sm-circ}
    Actor@{ shape: person}
    END2@{ shape: framed-circle}
    END1@{ shape: framed-circle}
```

**iii.b Add Menu Item**

```mermaid
flowchart TB
  subgraph subGraph0["API Layer"]
          A("Receive Menu Item Creation Request")
          E("Return Response")
    end
  subgraph subGraph1["Service Layer"]
          B{"Validate on Menu Item Model"}
          H{"Validate Restaurant Id"}
          I("Raise HTTP 404")
          F("Raise HTTP 422")
          C("Build Menu Item Model")
          G("Return Success")
    end
  subgraph subGraph2["Repository Layer"]
          D("Save to Database")
    end
      START["START"] --> Actor["Restaurant Owner"]
      Actor -- MenuItemInput --> A
      A -->|Menu Item Input| B
      A -->|Restaurant Id| H
      B -- Invalid Data --> F
      H -- Invalid Restaurant Id --> I
      I --> E
      E --> END2["END2"]
      B -- Valid Data --> C
      H -- Valid Restaurant Id --> C
      C -- MenuItem --> D
      D --> END1["END1"] & G
      F --> E
      G --> E
  
      START@{ shape: sm-circ}
      Actor@{ shape: person}
      END2@{ shape: framed-circle}
      END1@{ shape: framed-circle}
```

**iii.c Get Restaurant By Id**

```mermaid
flowchart TB
  subgraph subGraph0["API Layer"]
          A("Receive Get Restaurant Request")
          E("Return Response")
    end
  subgraph subGraph1["Service Layer"]
          B{"Validate Restaurant Id"}
          F("Raise HTTP 404")
          C("Retrieve Restaurant Model")
          H("Retrieve Menu Items for Restaurant")
          I("Build RestaurantOutput Model")
          G("Return Success")
    end
  subgraph subGraph2["Repository Layer"]
          D("Get from Restaurant Database")
          J("Get from Menu Items Database")
    end
      START["START"] --> Actor["Customer"]
      Actor -- Restaurant Id --> A
      A --> B
      B -- Invalid Restaurant Id --> F
      F --> E
      E --> END2["END2"]
      B -- Valid Restaurant Id --> C
      B -- Valid Restaurant Id --> H
      C -- Restaurant Id --> D
      D -- Restaurant --> I
      I --> G
      G --> E
      H -- Restaurant Id --> J
      J -- Menu Items --> I
  
      START@{ shape: sm-circ}
      Actor@{ shape: person}
      END2@{ shape: framed-circle}
      END1@{ shape: framed-circle}
  
```

### iv. Database Schema

**Entity Relationship Diagram**

```mermaid
erDiagram
    RESTAURANT {
        UUID id PK
        string name
        string address
        string cuisine
        boolean active
    }
    MENU_ITEM {
        UUID id PK
        UUID restaurant_id FK
        string name
        string description
        decimal price
        boolean active
    }
    USER {
        UUID id PK
        string email
        string password
        string first_name
        string last_name
        boolean active
        string role
    }
    CUSTOMER {
        UUID id PK
        string role
        list addresses
        string payment_method
    }
    RESTAURANT_OWNER {
        UUID id PK
        string role
        UUID restaurant_id FK
    }
    ADMIN {
        UUID id PK
        string role
        list permissions
    }
    CUSTOMER_ADDRESS {
        string address_line_1
        string address_line_2
        string city
        string province
        string postal_code
        string country
        string label
    }

    USER ||--o| CUSTOMER : specializes
    USER ||--o| RESTAURANT_OWNER : specializes
    USER ||--o| ADMIN : specializes
    CUSTOMER ||--o{ CUSTOMER_ADDRESS : has
    RESTAURANT_OWNER ||--o| RESTAURANT : manages
    RESTAURANT ||--o{ MENU_ITEM : has
```

**Data Validation**

- **Restaurant**
  - `id`: Must be a valid UUID.
  - `name`: Must be a non-empty string.
  - `address`: Must be a non-empty string.
  - `cuisine`: Must be a non-empty string.
  - `active`: Must be a boolean.

- **Menu Item**
  - `id`: Must be a valid UUID.
  - `restaurant_id`: Must be a valid UUID that references an existing restaurant.
  - `name`: Must be a non-empty string.
  - `description`: Must be a non-empty string.
  - `price`: Must be a Decimal greater than or equal to 0.0.
  - `active`: Must be a boolean.

- **User**
  - `id`: Must be a valid, unique UUID that is generated automatically and is immutable once set.
  - `email`: Must be a valid, unique email address normalized to lowercase.
  - `password`: Must be non-empty, must not contain whitespace, and must be hashed before storage.
  - `first_name`: Must be a non-empty string.
  - `last_name`: Must be a non-empty string.
  - `active`: Must be a boolean.
  - `role`: Must be `customer`, `restaurant_owner`, or `admin`.

- **Customer**
  - `role`: Must always be `customer`.
  - `addresses`: Must contain `CustomerAddress` models and must default to an empty list.
  - `payment_method`: Must be a string when provided and must default to `None`.

- **RestaurantOwner**
  - `role`: Must always be `restaurant_owner`.
  - `restaurant_id`: Must reference an existing restaurant when provided.

- **Admin**
  - `role`: Must always be `admin`.
  - `permissions`: Must be a list of strings and must default to an empty list.

- **BaseAddress**
  - `address_line_1`: Must be a non-empty string no longer than 120 characters.
  - `address_line_2`: Must be `None` or a non-empty string no longer than 120 characters.
  - `city`: Must be a non-empty string no longer than 50 characters.
  - `province`: Must be a supported Canadian province or territory code.
  - `postal_code`: Must use the `A1A 1A1` format.
  - `country`: Must be `Canada`.

- **CustomerAddress**
  - `label`: Must be a non-empty string no longer than 50 characters and must default to `Home`.

### v. Data Models

**Class Diagram**

```mermaid
classDiagram
    class BaseModel{
      <<from pydantic>>
    }

    class RestaurantInput {
        +string name
        +string address
        +string cuisine
        +boolean active
    }
    class RestaurantOutput {
        +UUID id
        +string name
        +string address
        +string cuisine
        +boolean active
        +list[MenuItemOutput] menu_items
    }
    class MenuItemInput {
        +string name
        +string description
        +decimal price
        +boolean active
    }
    class MenuItemOutput {
        +UUID id
        +UUID restaurant_id
        +string name
        +string description
        +decimal price
        +boolean active
    }

    BaseModel <|-- RestaurantInput
    BaseModel <|-- RestaurantOutput
    BaseModel <|-- MenuItemInput 
```
**Data Validation**

- **RestaurantInput**
  - `name`: Must be a non-empty string.
  - `address`: Must be a non-empty string.
  - `cuisine`: Must be a non-empty string.
  - `active`: Must be a boolean.

- **RestaurantOutput**
  - `id`: Must be a valid UUID.
  - `name`: Must be a non-empty string.
  - `address`: Must be a non-empty string.
  - `cuisine`: Must be a non-empty string.
  - `active`: Must be a boolean.
  - `menu_items`: Must be a list of MenuItemOutput objects.

- **MenuItemInput**
  - `name`: Must be a non-empty string.
  - `description`: Must be a non-empty string.
  - `price`: Must be a Decimal greater than or equal to 0.0.

- **MenuItemOutput**
- `id`: Must be a valid UUID.
  - `restaurant_id`: Must be a valid UUID that references an existing restaurant.
  - `name`: Must be a non-empty string.
  - `description`: Must be a non-empty string.
  - `price`: Must be a Decimal greater than or equal to 0.0.
  - `active`: Must be a boolean.