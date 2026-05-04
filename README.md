# F1 Telemetry Demo

This is a beginner-friendly F1 telemetry project.

It uses:

- **Docker Compose** to run everything together
- **TimescaleDB** to store F1 telemetry data
- **SQL** to create tables and generate synthetic racing data
- **Streamlit** to show the data in a dashboard

The project is designed to help learn how data engineering tools work together in a simple Formula 1 use case.

---

## Project Overview

In Formula 1, cars produce telemetry data during races.

Telemetry data can include:

- Speed
- Throttle
- Braking
- Gear
- Tyre temperature
- Engine temperature
- Battery level
- Lap number

In this demo, the data is **synthetic**, which means it is generated for learning purposes and is not real F1 racing data.

The project stores the data in **TimescaleDB** and shows it in a **Streamlit dashboard**.

---

## Prerequisites

Before running this project, make sure you have the following installed.

---

## 1. Install Docker Desktop

Docker is used to run TimescaleDB and Streamlit without installing everything directly on your laptop.

### For Mac

Download Docker Desktop from:

```text
https://www.docker.com/products/docker-desktop/
```

Install it, then open Docker Desktop.

To check Docker is working, open Terminal and run:

```bash
docker --version
```

You should see something like:

```text
Docker version 25.x.x
```

Also check Docker Compose:

```bash
docker compose version
```

You should see something like:

```text
Docker Compose version v2.x.x
```

---

## 2. Install Git

Git is used to download and manage the project code.

Check if Git is already installed:

```bash
git --version
```

You should see something like:

```text
git version 2.x.x
```

If Git is not installed, download it from:

```text
https://git-scm.com/downloads
```

---

## 3. Install a Code Editor

You can use any code editor, but **Visual Studio Code** is recommended.

Download it from:

```text
https://code.visualstudio.com/
```

---

## Project Structure

The current project structure may look like this:

```text
f1-telemetry-demo/
├── docker-compose.yml
├── init.sql
├── app.py
├── requirements.txt
└── README.md
```

### File Explanation

| File | Purpose |
|---|---|
| `docker-compose.yml` | Starts TimescaleDB and Streamlit containers |
| `init.sql` | Creates the database table and adds synthetic F1 telemetry data |
| `app.py` | Streamlit dashboard application |
| `requirements.txt` | Python libraries required by the Streamlit app |
| `README.md` | Project instructions |

---

## Important Note About TimescaleDB and Streamlit

You do **not** need to manually install TimescaleDB or Streamlit on your laptop.

Docker Compose will run them for you.

This means:

- TimescaleDB runs inside a Docker container
- Streamlit runs inside a Docker container
- The SQL setup runs automatically from `init.sql`

So the main thing you need installed on your laptop is:

```text
Docker Desktop
```

---

## How to Run the Project

### Step 1: Open Terminal

Open Terminal on your laptop.

Go to the project folder:

```bash
cd f1-telemetry-demo
```

---

### Step 2: Start the project

Run:

```bash
docker compose up
```

If your system uses the older command, run:

```bash
docker-compose up
```

Docker will now:

1. Download the TimescaleDB image
2. Start the TimescaleDB database
3. Run the `init.sql` file
4. Install the Python packages for Streamlit
5. Start the Streamlit dashboard

---

## Open the Streamlit Dashboard

Once everything is running, open this in your browser:

```text
http://localhost:8501
```

You should now see the F1 telemetry dashboard.

---

## How to Stop the Project

To stop the running containers, press:

```text
CTRL + C
```

Then run:

```bash
docker compose down
```

This stops and removes the containers.

---

## How to Restart the Project

To start the project again:

```bash
docker compose up
```

Then open:

```text
http://localhost:8501
```

---

## How to Check Running Containers

To see if the containers are running:

```bash
docker ps
```

You should see containers for:

- TimescaleDB
- Streamlit

---

## How to Connect to TimescaleDB

To connect to the database from Terminal, first check the container name:

```bash
docker ps
```

Then connect using:

```bash
docker exec -it <timescaledb-container-name> psql -U postgres -d f1db
```

Example:

```bash
docker exec -it f1_strategy_timescaledb psql -U postgres -d f1db
```

Once inside PostgreSQL, you can list the tables:

```sql
\dt
```

You can query the telemetry table:

```sql
SELECT *
FROM f1_telemetry
LIMIT 10;
```

To exit PostgreSQL:

```sql
\q
```

---

## Example SQL Queries

### View the latest telemetry data

```sql
SELECT *
FROM f1_telemetry
ORDER BY time DESC
LIMIT 10;
```

### Find the fastest speed

```sql
SELECT 
    driver_name,
    MAX(speed_kph) AS fastest_speed
FROM f1_telemetry
GROUP BY driver_name;
```

### Average speed by lap

```sql
SELECT 
    lap_number,
    ROUND(AVG(speed_kph)::numeric, 2) AS avg_speed
FROM f1_telemetry
GROUP BY lap_number
ORDER BY lap_number;
```

### Average tyre temperature

```sql
SELECT 
    driver_name,
    ROUND(AVG(tyre_temp_c)::numeric, 2) AS avg_tyre_temp
FROM f1_telemetry
GROUP BY driver_name;
```

---

## Common Problems and Fixes

### Problem: Docker is not running

Error example:

```text
Cannot connect to the Docker daemon
```

Fix:

Open Docker Desktop and wait until it says Docker is running.

Then try again:

```bash
docker compose up
```

---

### Problem: Port 5432 is already in use

Error example:

```text
port is already allocated
```

This means another database may already be using port `5432`.

Fix:

Stop the other database or change the port in `docker-compose.yml`.

Example:

```yaml
ports:
  - "5433:5432"
```

This means your laptop will use port `5433`, but the container still uses port `5432`.

---

### Problem: Port 8501 is already in use

Streamlit uses port `8501`.

If that port is already being used, change it in `docker-compose.yml`.

Example:

```yaml
ports:
  - "8502:8501"
```

Then open:

```text
http://localhost:8502
```

---

### Problem: Database table is missing

If the table is missing, restart everything from scratch:

```bash
docker compose down -v
docker compose up
```

The `-v` removes the old database volume, so the `init.sql` file can run again from the beginning.

---

## Recommended Future Folder Structure

At the moment, all files may be in one folder.

That is okay for a first project.

Later, the project can be made cleaner like this:

```text
f1-telemetry-demo/
├── docker-compose.yml
├── README.md
├── database/
│   └── init.sql
└── streamlit_app/
    ├── app.py
    └── requirements.txt
```

This makes the project easier to understand because:

- database files go inside `database/`
- Streamlit files go inside `streamlit_app/`
- the main folder stays clean

---

## What This Project Teaches

This project teaches how different tools work together:

```text
Docker runs the environment
TimescaleDB stores the telemetry data
SQL creates and queries the data
Python connects to the database
Streamlit shows the dashboard
```

---

## Next Improvements

Possible future improvements:

- Move Streamlit files into a separate folder
- Add more drivers
- Add Ferrari-specific dashboard sections
- Add lap comparison charts
- Add fastest lap analysis
- Add tyre strategy data
- Add race position data
- Add real F1 data using FastF1
- Add screenshots to the README
- Improve the dashboard design

---

## Project Status

This is a beginner learning project.

The aim is to learn:

- Data
- Databases
- SQL
- Python
- Dashboards
- Docker
- Formula 1 telemetry
