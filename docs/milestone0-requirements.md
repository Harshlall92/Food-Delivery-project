# Software Requirements Specification for Milestone 0

**Objective:** Foundations of a REST API backend built with **FastAPI** utilizing structured **JSON** files for data persistence.

**Table Of Contents:**
- [Software Requirements Specification for Milestone 0](#software-requirements-specification-for-milestone-0)
  - [1. Introduction](#1-introduction)
    - [1.1 Purpose](#11-purpose)
    - [1.2 Scope](#12-scope)
    - [1.3 Definitions \& Acronyms](#13-definitions--acronyms)
  - [2. Overall Description](#2-overall-description)
    - [2.1 Product Perspective](#21-product-perspective)
    - [2.2 High-Level Architecture](#22-high-level-architecture)
    - [2.3 Constraints](#23-constraints)
  - [3. Technical \& System Requirements](#3-technical--system-requirements)
    - [3.1 Tech Stack Components](#31-tech-stack-components)
    - [3.2 Data Storage Structure](#32-data-storage-structure)
  - [4. Functional Requirements](#4-functional-requirements)
    - [4.1 System Initialization](#41-system-initialization)
    - [4.2 Restaurant Repository](#42-restaurant-repository)
    - [4.3 API Endpoints](#43-api-endpoints)
    - [4.4 Concurrency \& File Integrity](#44-concurrency--file-integrity)
    - [4.5 Service Requirements](#45-service-requirements)
  - [5. Non-Functional Requirements](#5-non-functional-requirements)
  - [6. Verification \& Testing](#6-verification--testing)
    - [6.1 API Tests](#61-api-tests)
  - [7. Requirements Identification Summary](#7-requirements-identification-summary)

---

## 1. Introduction

### 1.1 Purpose

This document defines the functional, non-functional, and technical requirements for Milestone 0.

### 1.2 Scope

Foundational layer of the backend, only exposing endpoints for server health, docs, and the list of all restaurants stored in `data/restaurants.json`.

### 1.3 Definitions & Acronyms

* **Mutex:** Mutual Exclusion Lock

---

## 2. Overall Description

### 2.1 Product Perspective

A REST API built entirely in Python using FastAPI. It reads from and writes to flat-file storage architectures.

### 2.2 High-Level Architecture

* **API Layer:** FastAPI routers managing request validataion (Pydantic models) and HTTP response lifecycle.
* **Service/Data Layer:** File-system managers handling thread-safe File I/O operations.

### 2.3 Constraints

* Data must be saved as JSON or CSV; No databases are permitted.
* Local file I/O operations must handle concurrent write locks to prevent data corruption.

---

## 3. Technical & System Requirements

### 3.1 Tech Stack Components

* **Framework:** FastAPI
* **Data Validation:** Pydantic
* **File Operations:** Standard library `json`.

### 3.2 Data Storage Structure

* **DATA-RST-001:** Restaurants must be stored in `data/restaurants.json`.
* **DATA-RST-002:** A restaurant must adhere to the `Restaurant` model.
  * **DATA-RST-003:** A restaurant must have a unique id.
  * **DATA-RST-004:** A restaurant must have a non-empty string name.
  * **DATA-RST-005:** A restaurant must have a non-empty string address.
  * **DATA-RST-006:** A restaurant must have a non-empty category.

---

## 4. Functional Requirements

### 4.1 System Initialization

* **FQ-INIT-001:** On system startup, the application must verify the existence of the `data/` directory and required file (`restaurants.json`).
* **FQ-INIT-002:** If files are missing, the system must automatically initialize them with empty base structures (e.g. `[]` for JSON).
* **FQ-INIT-003:** If `restaurants.json` contains invalid json, the system must _______.
* **FQ-INIT-004:** The system must initialize the `Restaurants` repository.

### 4.2 Restaurant Repository

* **FQ-REPO-001:** The repository must be linked to a file path (`data/restaurants.json`)
* **FQ-REPO-002:** The repository must be able to retrieve all restaurants.

### 4.3 API Endpoints

* **FQ-API-001:** Accessing the `GET /` endpoint should return `"Welcome to the Pilates Princess Food Delivery Service!"`.
* **FQ-API-002:** Accessing the `GET /health` endpoint must return `HTTP 200`.
* **FQ-API-003:** Accessing the `GET /api/restaurants` endpoint must return `HTTP 200` and a JSON array containing all restaurants stored in `data/restaurants.json`
  
### 4.4 Concurrency & File Integrity

* **FQ-SYNC-001:** Concurrent write operations to the same data file must be serialized to prevent simultaneous modification and data corruption.

### 4.5 Service Requirements

* **FQ-SERV-001:** Restaurant service must connect to the Restaurant repository.
* **FQ-SERV-002:** Restaurant service must ask the repository to return a list of all restaurants stored.

---

## 5. Non-Functional Requirements

* **NFR-RDME-001:** `README.md` must contain enough information for a new team member or TA to run the project.
  * **NFR-RDME-002:** The team name must be listed.
  * **NFR-RDME-003:** The required python version must be listed.
  * **NFR-RDME-004:** Setup instructions must be included.
    * **NFR-RDME-005:** Instructions for cloning the project.
    * **NFR-RDME-006:** Instructions for setting up the virtual environment.
    * **NFR-RDME-007:** Instructions for installing necessary dependencies
    * **NFR-RDME-008:** Instructions for how to start the application.
  * **NFR-RDME-009:** API endpoint paths must be listed.
  * **NFR-RDME-010:** The `/docs` path must be listed.
  * **NFR-RDME-011:** The location and format of represented data must be provided.
  * **NFR-RDME-012:** Instructions for how to run tests must be listed.
  * **NFR-RDME-013:** A brief repository structure must be included.

---

## 6. Verification & Testing

### 6.1 API Tests

* **TEST-API-001:** The `GET /` endpoint returns `Welcome to the Pilates Princesses Food Delivery Service!`.
* **TEST-API-002:** The `GET /health` endpoint returns `HTTP 200`
* **TEST-API-003:** The `GET /api/restaurants` endpoint returns HTTP status of 200.
* **TEST-API-004:** The `GET /api/restaurants` returns a list of restaurant objects.


---

## 7. Requirements Identification Summary

**Data Management Requirements:**

* Next ID for restaurant data requirement: `DATA-RST-007`

**Functional Requirements:**

* Next ID for initialization requirement: `FQ-INIT-005`
* Next ID for repository requirement: `FQ-REPO-003`
* Next ID for api requirement: `FQ-API-004`
* Next ID for concurrency requirement: `FQ-SYNC-002`

**Testing Requirements:**

* Next ID for api test requirement: `TEST-API-005`

**Non-Functional Requirements:**

* Next ID for `README.md` requirement: `NFR-RDME-014`
