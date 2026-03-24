# Scraper — Windy webcams, screenshots, and weather

Python service that periodically captures **Windy.com webcam** frames with **Playwright**, fetches **current weather** from [Open-Meteo](https://open-meteo.com) (no API key), and stores **paths + metadata + weather** in **PostgreSQL**.

## Features

- Scheduled webcam screenshots (default: every **30 minutes** per job, staggered by 5 seconds)
 PNG files under `screenshots/`
- Optional **latitude / longitude** per camera: when both are set, weather is fetched at capture time and saved on the same database row
- Database bootstrap and **additive migrations** for weather columns on existing `screenshots` tables

## Requirements

- **Python** 3.10+ (uses `dict[str, ...] | None` style typing in some modules)
- **PostgreSQL** reachable with credentials below
- **Chromium** for Playwright (installed via Playwright CLI)

## Setup

1. **Clone** the repository and create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install browser binaries** for Playwright:

   ```bash
   playwright install chromium
   ```

4. **Configure the database** — create a `.env` file in the project root (see `.gitignore`; values are not committed):

   | Variable       | Description        |
   |----------------|--------------------|
   | `DB_USER`      | PostgreSQL user    |
   | `DB_PASSWORD`  | Password           |
   | `DB_HOST`      | Host               |
   | `DB_PORT`      | Port (e.g. `5432`) |
   | `DB_NAME`      | Database name      |

   These are read in `storage/db_config.py` via `python-dotenv`.

5. **Configure jobs** in `config/config.json`:

   - `name` — unique job id (also used as scheduler job id)
   - `url` — Windy webcam page URL
   - `type` — e.g. `"screenshot"`
   - `latitude`, `longitude` — optional decimals for Open-Meteo; if either is missing, weather fields in the DB stay empty

6. **Run**:

   ```bash
   python main.py
   ```

   On startup, `main.py` calls `init_db()` (create tables / add missing weather columns), then starts the blocking scheduler.

## Project layout

| Path | Role |
|------|------|
| `main.py` | Entry point: DB init + scheduler |
| `config/config.json` | Job list (URLs, coords) |
| `scheduler/scheduler.py` | APScheduler interval jobs |
| `scrapers/web_cam_scraper.py` | Playwright screenshot + weather hook |
| `scrapers/weather_client.py` | Open-Meteo HTTP client |
| `scrapers/bas_scraper.py` | Loads job fields from config |
| `storage/db.py` | SQLAlchemy models, `save_screenshot`, migrations helper |

## Database schema (`screenshots`)

| Column | Type | Notes |
|--------|------|--------|
| `id` | integer | Primary key |
| `camera_name` | string | Job `name` |
| `image_path` | string | Local path to PNG |
| `created_at` | timestamp | Capture time |
| `weather_temp_c` | float | °C (nullable) |
| `weather_code` | int | WMO-style code from Open-Meteo (nullable) |
| `weather_wind_speed_m_s` | float | 10 m wind, m/s (nullable) |
| `weather_precipitation_mm` | float | mm (nullable) |
| `weather_relative_humidity` | int | % (nullable) |

## Weather API

- **Provider:** Open-Meteo forecast API, `current` parameters for temperature, humidity, precipitation, weather code, and wind.
- **No API key** required for fair use; respect their [terms](https://open-meteo.com/en/terms).

## Operational notes

- Screenshots are written to `screenshots/` (ignored by git in `.gitignore`). Plan disk usage if you run for a long time.
- The scheduler uses `BlockingScheduler`; the process runs until stopped (Ctrl+C or process manager).
- To change interval or stagger, edit `scheduler/scheduler.py` (`minutes=30`, `delay_between_jobs`).

