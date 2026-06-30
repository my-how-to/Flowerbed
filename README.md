# Smart Flowerbed Management API

An asynchronous RESTful API built with FastAPI designed for community garden management. The system automates watering alerts based on live weather patterns and historical logging, and includes cold-season safety overrides to prevent infrastructural damage.

## Tech Stack
* **Language:** Python 3.12
* **Framework:** FastAPI (Asynchronous ASGI)
* **Database & ORM:** SQLite / SQLAlchemy 2.0
* **Containerization:** Docker / Docker Compose
* **HTTP Client:** HTTPX (Async requests)
* **Third-Party Integrations:** Telegram Bot API, OpenWeatherMap API

## Core Business Logic & Features
1. **Automated Watering Auditor:** A background routine evaluates historical logs alongside live meteorological parameters. If the ecosystem experiences no recorded irrigation within 7 days during the active season (mid-June to October) and ambient temperatures exceed 30°C without precipitation, an automated alert is triggered.
2. **Winter Infrastructure Protection:** If system operators switch the environment configuration to "Winter Mode", a backend evaluation script continuously scans pressure sensor feeds. If automated well valves report active pressure while in off-season status, a critical priority alert is dispatched immediately to mitigate pipe-burst hazards.
3. **Interactive Telegram Notifications:** System notifications utilize Telegram's Inline Keyboard layouts, routing field volunteers directly back to the API endpoints to submit instant logging updates.

## System Architecture

```text
flowerbed_project/
│
├── database.py      # Database engine configuration and session dependency
├── models.py        # SQLAlchemy data schemas and relational definitions
├── tasks.py         # Main business logic, trigger evaluation and cron audits
├── weather.py       # Asynchronous OpenWeatherMap integration engine
├── telegram_bot.py  # Asynchronous notification dispatcher
├── main.py          # Application entrypoint and route handlers
├── requirements.txt # Project application dependencies
├── Dockerfile       # Container construction manifest
└── docker-compose.yml# Multi-container environment orchestration layer
```

## Installation and Execution (Docker Compose)

### 1. Configure Environment Variables
Create a `.env` file in the project root directory:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_personal_or_group_chat_id
OPENWEATHER_API_KEY=your_openweathermap_api_token
CITY_LAT=55.7558
CITY_LON=37.6173
```

### 2. Launch the Application Container
Execute the following deployment command in your terminal interface:

```bash
docker-compose up --build
```

The server initialization sequence will execute, exposing the application framework on your loopback interface.

### 3. Verification and Interface Testing
Open your browser and navigate to the automated documentation suite to manually interact with the API schema:
* Interactive Swagger Interface: `http://127.0.0`
