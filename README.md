# Pilates Princesses' Food Delivery Application

COSC 310 - Software Engineering
Team Name: Pilates Princesses

The Pialtes Princesses Food Delivery Application is a REST API that can retrieve all restaurants stored in a JSON restaurants database.

## Installation & Setup

Follow these steps to set up the project locally.

### Prerequisites

- **Python**: Version 3.14.7 is required. Download it [here](https://www.python.org/downloads/release/python-3147/).

### Step-By-Step Instructions

#### 1. Clone the Repository

If you have Git installed:

```bash
git clone https://github.com/Harshlall92/Food-Delivery-project
cd Food-Delivery-project
```

If you don't have Git installed, click on the green `<> Code` button on the right side of the screen, then scroll down and click `Download ZIP`. Extract the project in your file explorer and open it in your preferred IDE (VSCode).

#### 2. Create a Virtual Environment

Once the project is open in your IDE, open a terminal.

If your terminal is not in the project directory, use:

```bash
cd path/to/project
```

Once the terminal is in the project directory use:

```bash
python -m venv .venv
```

to create the virutal environment.

#### 3. Activate the virual environment

- **Windows (PowerShell)**:

```bash
.\venv\Scripts\Activate.ps1
```

- **Windows (Command Prompt)**:

```cmd
venv\Scripts\activate.bat
```

- **macOS / Linux**:

```bash
source venv/bin/activate
```

#### 4. Install Dependencies

Install the required packages listed in `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

To start the application, run the following command in your terminal:

```bash
uvicorn app.main:app --reload
```

The application can then be opened in your web browser at [http://127.0.0.1:8000](http://127.0.0.1:8000)

### API Endpoint Paths

- `/`
- `/health`
- `/restaurants`

API documentation can be found at: `/docs`


## Representative Data

- **Restaurants**: [Food-Delivery-project/data/restaurants.json](https://github.com/Harshlall92/Food-Delivery-project/blob/main/data/restaurants.json)

## Tests

Tests can be run with the following command in your terminal:

```bash
pytest -v
```

## Repository Structure

```
Food-Delivery-project/
├── app/
│   ├── api/
│   │   └── routes/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── data/
│   └── restaurants.json
├── docs/
│   └── milestone0-requirements.md
├── scrum/
│   └── team-agreement.md
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```