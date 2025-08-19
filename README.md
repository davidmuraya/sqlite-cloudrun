# sqlite-cloudrun

## Project Objective

This project explores whether Google Cloud Run can reliably run a FastAPI application using SQLite as the backend database, with the SQLite file stored in a Google Cloud Storage (GCS) bucket. The goal is to evaluate the feasibility, performance, and reliability of this architecture for transactional workloads.

---

## Key Implementation Details

### 1. Transaction Commit on Application Shutdown

- The application uses FastAPI's startup and shutdown events to manage database state.
- On shutdown, a `wal_checkpoint(TRUNCATE)` is executed to ensure all transactions in the Write-Ahead Log (WAL) are flushed and committed to the main SQLite file. This is handled in `app/config/events.py`:

    ```python
    with engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA wal_checkpoint(TRUNCATE);")
    ```

- This approach helps maintain data integrity, especially when using a network-mounted database file.

---

### 2. Database Connection Tweaks

- The database connection is configured with several performance-oriented PRAGMA settings:

  - `journal_mode=WAL`: Enables concurrent reads and writes.
  - `synchronous=NORMAL`: Balances performance and durability.
  - `cache_size=10000`: Increases the in-memory cache for faster operations.
  - `temp_store=MEMORY`: Stores temporary tables in RAM for speed.
  - `busy_timeout=5000`: Waits up to 5 seconds if the database is locked.

- The connection uses `check_same_thread=False` to allow multi-threaded access, which is necessary for FastAPI's async request handling.
- All configuration is handled in `app/services/database/database.py`.

---

### 3. GCS Storage Mount Options in Cloud Build

- The Cloud Run service is deployed with the SQLite database file mounted from a GCS bucket using GCSFuse.
- Cloud Build (`cloudbuild.yaml`) specifies mount options for performance:
  - `metadata-cache-ttl-secs=0`: Disables metadata caching for consistency.
  - `type-cache-max-size-mb=4`: Limits type cache size to reduce memory usage.
- The database file is mounted at `/gcs/core.db` and the application is configured to use this path via environment variables.

---

### 4. Load Testing with Locust

- The project includes a Locust test suite (`app/tests/locustfile.py`) to simulate realistic API usage:
  - Listing products with random pagination.
  - Creating, updating, and deleting products.
  - Fetching random products.
- These tests help evaluate the application's performance and concurrency handling when using SQLite over a network-mounted file.

---

## How to Run the Project

### Prerequisites

- Python 3.9+
- Docker
- Google Cloud SDK (for deployment)
- A GCS bucket for the SQLite file

### Local Development

1. **Install dependencies:**

    ```
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    pip install -r requirements.txt
    ```

2. **Set environment variables:**
    - Create a `.env` file with:

    ```
    DB=/path/to/local/core.db
    ```

3. **Run the application:**
    ```
    uvicorn app.main:app --reload
    ```

### Deploy to Cloud Run

1. **Configure your GCS bucket and upload an initial SQLite file if needed.**

2. **Build and deploy using Cloud Build:**
    Ensure you have the Google Cloud SDK installed and authenticated. Enable the Cloud Build API.

    ```
    gcloud builds submit --config cloudbuild.yaml
    ```

3. **Cloud Build will:**
    - Build and push the Docker image.
    - Deploy to Cloud Run with the GCS bucket mounted.
    - Set environment variables and mount options for optimal SQLite performance.

### Running Load Tests

1. **Install Locust and Faker:**
    - If you have commented out `locust` and `faker` in your `requirements.txt`, uncomment those lines.
    - Then install the dependencies:

    ```
    pip install locust faker
    ```

2. **Run Locust:**
    ```
    locust -f app/tests/locustfile.py
    ```
    - Open the Locust web UI and start the test to simulate API usage.

---

## Notes and Considerations

- **SQLite on GCS**: While WAL mode and PRAGMA tweaks improve performance, SQLite is not designed for network filesystems. This setup is experimental and not recommended for production workloads.
- **Data Consistency**: The WAL checkpoint on shutdown helps, but abrupt shutdowns or network issues may still cause data loss or corruption.
- **Alternatives**: For production, consider using a managed database like Cloud SQL or Firestore.

---

## License

MIT License
