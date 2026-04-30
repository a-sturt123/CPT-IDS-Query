# CPT IDS Query

A proof of concept Discord bot that allows students to query network traffic data captured from the CPT environment. Built for Process Automation and Shell Script, Spring 2026

**Team:** Ayden Sturtevant, Darian Mongiovi

---

## Overview

This project combines a Python based packet capture pipeline with a Discord bot interface. Network traffic is captured using Scapy, stored in a PostgreSQL (or SQLite for testing) database, and made queryable through a set of Discord bot commands

---

## Project Structure

```
CPT-IDS-Query/
├── bot.py              # Entry point, loads cogs and starts the bot
├── db.py               # Database connection and shared helpers
├── scapy_ids.py        # Packet capture and database ingestion script
├── requirements.txt    # Python dependencies
└── cogs/
    ├── stats.py        # !summary, !top-ports, !flagstats
    ├── time.py         # !peak-hours, !peak-days, !traffic-over-time
    ├── lookup.py       # !flags, !port-info
    └── utils.py        # !export, !help
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/a-sturt123/CPT-IDS-Query.git
cd CPT-IDS-Query
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a .env file**
```
DISCORD_TOKEN=your_discord_bot_token
DATABASE_URL=sqlite:///test.db
```

For production, replace the SQLite URL with your PostgreSQL connection string:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

---

## Running the Capture Script

The capture script requires administrator/root privileges to access network interfaces

```bash
# Windows (run as Administrator)
python scapy_ids.py

# Linux
sudo python scapy_ids.py
```

The script listens for TCP traffic on ports 22, 23, 80, and 445 and writes incidents to the `incident_logs` table

---

## Running the Bot

```bash
python bot.py
```

The bot will load each cog and confirm the database connection on startup

---

## Bot Commands

| Command | Description |
|---|---|
| `!summary` | Overview of total incidents, unique IPs, and most targeted port |
| `!top-ports` | Top 10 most frequently targeted ports |
| `!flagstats` | Breakdown of TCP flag types across all incidents |
| `!flags <flag>` | Filter incidents by TCP flag, e.g. `!flags S` for SYN |
| `!peak-hours` | Hours of the day with the most traffic |
| `!peak-days` | Days of the week with the most traffic |
| `!traffic-over-time` | Incident counts over the last 24 periods |
| `!port-info <port>` | Look up what a port number is commonly used for |
| `!export` | Download the full incident log as a CSV file |

---

## Notes

- Source IPs are masked in all bot output and CSV exports to avoid exposing internal addresses
- SQLite is used for local testing. Switching to PostgreSQL requires updating `DATABASE_URL` in `.env` and updating `strftime` calls in `cogs/time.py` to use PostgreSQL's `EXTRACT` syntax
- The bot will start without a database connection and return a friendly error on any query command until one is available