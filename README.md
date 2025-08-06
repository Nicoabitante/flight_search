#  Flight Journey API


## 🛠 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [httpx](https://www.python-httpx.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Poetry](https://python-poetry.org/) for dependency management

## ⚙️ Setup Instructions

1. **Clone the repository**

    ```bash
    git clone https://github.com/Nicoabitante/flight_search.git
    cd flight_search
    ```
2. **Install Poetry**
If you don't have Poetry installed:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
3. **Install dependencies**
    ```bash
    poetry install
    ```
4. **Run App**
    ```bash
    poetry run uvicorn main:app --reload
    ```