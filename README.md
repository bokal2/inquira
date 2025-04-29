
# Inquira (Business Intelligence Chatbot)

An AI-powered chatbot to interact with a Relational database (PostgreSQL) using natural language.
Built with FastAPI, AWS Bedrock foundational models (Amazon Titan Text Express, Claude 3 Sonnet), LangChain, and SQLAlchemy.

---

## Features

- Query your database using natural language
- Auto-generate SQL queries based on table schema
- Generate natural language explanations for SQL responses
- Structured JSON logging for requests and SQL queries
- SQL query error handling with user-friendly responses
- Rate limiting to protect API endpoints
- Health check and Prometheus metrics exposure
- Seed sample data for development and testing

---

## Project Structure

| Location | Purpose |
|:---------|:--------|
| `main.py` | FastAPI app setup (lifespan, CORS, logging, routes, Prometheus) |
| `src/api.py` | Central route registration for agents and development scripts |
| `src/agent/controller.py` | Agent endpoint (`/agent/query`) for LLM-to-SQL pipeline |
| `src/agent/llm_setup.py` | SQL agent chains: SQL generation and response generation |
| `src/agent/prompt_template.py` | Prompt templates for SQL generation and explanations |
| `src/scripts/controller.py` | Development endpoints, including data seeding |
| `src/scripts/seed.py` | Data seeding scripts using Faker |
| `src/entities` | SQLAlchemy ORM models |
| `src/db/core.py` | Database engine and metadata initialization |
| `src/rate_limiting.py` | Rate limiter configuration using SlowAPI |
| `src/logging.py` | Structured JSON logging setup for FastAPI and SQLAlchemy |

---

## How It Works

1. The user sends a natural language question to `/agent/query`.
2. Claude 3 Sonnet (via AWS Bedrock) generates a SQL query using the database schema.
3. The application executes the generated SQL query safely on PostgreSQL.
4. Claude 3 is provided the original question, SQL query, and SQL response to generate a clean, natural language answer.
5. The final answer is returned to the user.

SQL errors are caught and returned in a friendly way.
All SQL queries and LLM outputs are logged for observability.

---

## Running the Application

1. Clone the repository:

   ```bash
   git clone https://github.com/bokal2/inquira.git
   cd inquira
   ```

2. Install dependencies:

   ```bash
   poetry install
   ```

3. Set up environment variables in a `.env` file:

   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name
   AWS_REGION=your-aws-region
   FOUNDATIONAL_MODEL=anthropic.claude-3-sonnet-20240229-v1:0
   ```

4. Run the application locally:

   ```bash
   poetry run uvicorn src.main:app --reload
   ```

5. Available endpoints:

   - OpenAPI docs: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`
   - Prometheus metrics: `http://localhost:8000/metrics`

---

## API Endpoints

| Method | URL | Description |
|:-------|:----|:------------|
| `POST` | `/agent/query` | Submit a natural language question |
| `POST` | `/dev/seed` | Seed the database with sample data |
| `GET`  | `/health` | Health check endpoint |
| `GET`  | `/metrics` | Prometheus metrics for monitoring |

---

## Technology Stack

- FastAPI
- LangChain (v0.1+)
- AWS Bedrock (Claude 3 Sonnet Model)
- SQLAlchemy
- Prometheus Instrumentator
- SlowAPI for Rate Limiting
- Python-JSON-Logger
- Faker for data seeding

---

## Example Usage

Request:

```bash
curl -X POST http://localhost:8000/agent/query \
-H "Content-Type: application/json" \
-d '{"question": "Show me the top 5 best-selling products."}'
```

Response:

```json
{
  "response": "The top 5 best-selling products are Laptop, Smartphone, Headphones, Monitor, and Keyboard based on the number of sales."
}
```

---

## Key Application Features

- Structured JSON logging for all HTTP requests, responses, and SQL queries.
- SQL query errors are caught and logged, with polite user feedback.
- Rate limiting applied globally to prevent API abuse.
- Sample data generation available for testing purposes.
- Natural language output controlled by strict prompt templates.
- Health and metrics endpoints available for observability.

---

## Future Improvements

- Add memory support for follow-up user queries.
- Intelligent auto-correction of invalid SQL queries.
- Extend support for connecting dynamically to multiple databases.
- Secure API access with authentication and authorization.
- Enable streaming responses for LLM-generated answers.

---

# Notes

- Request IDs are assigned and logged with every incoming and outgoing request.
- SQLAlchemy engine queries are logged alongside request metadata.
- Claude 3 Sonnet model used for both SQL generation and explanation tasks.
- Prometheus metrics exposed for service monitoring.
