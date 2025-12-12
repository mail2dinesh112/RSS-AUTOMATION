# RSS Automation Service

An automated RSS feed processor that fetches articles, classifies them using AI, stores them in a database, and sends email summaries.

## Overview

This application is a FastAPI-based service that automatically:
1. Fetches articles from RSS feeds every 4 hours
2. Classifies articles into categories using OpenAI's GPT-3.5
3. Stores articles in a PostgreSQL database
4. Sends email summaries of new articles

## Architecture

### Core Components

#### 1. Main Application ([app/main.py](app/main.py))
- FastAPI application entry point
- Creates database tables on startup
- Starts the scheduler service
- Exposes a health check endpoint at `/`

#### 2. Scheduler ([app/scheduler.py](app/scheduler.py))
- Uses APScheduler to run the RSS processing job every 4 hours
- Orchestrates the entire workflow:
  - Fetches RSS feeds
  - Checks for duplicate articles
  - Classifies new articles
  - Saves to database
  - Sends email summaries

#### 3. RSS Service ([app/rss_service.py](app/rss_service.py))
- Fetches and parses RSS feeds using `feedparser`
- Extracts article title, link, and summary
- Implements retry logic for reliability

#### 4. Classification Service ([app/classify_service.py](app/classify_service.py))
- Uses OpenAI API (GPT-3.5-turbo) to classify articles
- Sends article title and summary for categorization
- Falls back to "Uncategorized" on errors

#### 5. Email Service ([app/email_service.py](app/email_service.py))
- Sends email summaries via SMTP (Gmail)
- Uses TLS for secure email transmission
- Notifies when new articles are found

#### 6. Database ([app/database.py](app/database.py))
- SQLAlchemy ORM for database operations
- PostgreSQL as the database backend
- Connection management and session handling

#### 7. Models ([app/models.py](app/models.py))
- `Article` model with fields:
  - `id`: Primary key
  - `title`: Article title
  - `link`: Article URL (used for duplicate detection)
  - `summary`: Article summary/description
  - `category`: AI-classified category
  - `created_at`: Timestamp

#### 8. Utilities ([app/utils.py](app/utils.py))
- `retry()` function: Retries failed operations up to 3 times with 2-second delays

### Detailed Process Flow

1. **Application Initialization**
   - FastAPI app starts ([app/main.py:5](app/main.py#L5))
   - Database tables are created automatically
   - Scheduler starts and runs the job every 4 hours ([app/scheduler.py:66](app/scheduler.py#L66))

2. **RSS Feed Fetching** ([app/scheduler.py:21](app/scheduler.py#L21))
   - Uses `feedparser` to parse the RSS feed
   - Implements retry logic (3 attempts with 2-second delays)
   - Extracts title, link, and summary from each entry

3. **Duplicate Detection** ([app/scheduler.py:28](app/scheduler.py#L28))
   - Queries database for existing articles by link
   - Skips processing if article already exists
   - Prevents duplicate entries and redundant classification

4. **AI Classification** ([app/scheduler.py:34](app/scheduler.py#L34))
   - Sends article title and summary to OpenAI API
   - Uses GPT-3.5-turbo model for classification
   - Returns category (e.g., "Technology", "Sports", "Politics")
   - Falls back to "Uncategorized" if classification fails

5. **Database Storage** ([app/scheduler.py:37-44](app/scheduler.py#L37-L44))
   - Creates Article object with all metadata
   - Commits to PostgreSQL database
   - Timestamp automatically added

6. **Email Notification** ([app/scheduler.py:49-52](app/scheduler.py#L49-L52))
   - Only sends email if new articles exist
   - Email body contains: "Title (Category)" for each article
   - Sent via Gmail SMTP with TLS encryption

## Configuration

### Environment Variables (.env file required)

```env
# RSS Feed URL
RSS_URL=https://example.com/feed.rss

# OpenAI API Key for classification
OPENAI_API_KEY=sk-your-openai-api-key

# PostgreSQL Database Connection
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Email Configuration ([app/config.py](app/config.py))

The following are hardcoded in the settings:
- **SMTP_SERVER**: smtp.gmail.com
- **SMTP_PORT**: 587
- **EMAIL_FROM**: mail2dinesh112@gmail.com
- **EMAIL_TO**: msg2mypersonal@gmail.com
- **SMTP_USERNAME**: mail2dinesh112@gmail.com
- **SMTP_PASSWORD**: (App-specific password)

> **Note**: For Gmail, you need to use an App Password, not your regular Gmail password. Generate one at: https://myaccount.google.com/apppasswords

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL database
- OpenAI API key
- Gmail account with App Password

### Steps

1. **Clone/Download the repository**
   ```bash
   cd /home/sbna/Downloads/ASSIGNMENT/automation_rss_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create .env file**
   ```bash
   cat > .env << EOF
   RSS_URL=https://your-rss-feed-url.com/feed
   OPENAI_API_KEY=sk-your-openai-api-key
   DATABASE_URL=postgresql://username:password@localhost:5432/rss_db
   EOF
   ```

4. **Set up PostgreSQL database**
   ```bash
   # Create database
   psql -U postgres
   CREATE DATABASE rss_db;
   \q
   ```

5. **Start the application**
   ```bash
   # Option 1: Using the provided script
   chmod +x start.sh
   ./start.sh

   # Option 2: Direct command
   python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Usage

### Starting the Service
```bash
./start.sh
```
This script:
- Kills any process running on port 8000
- Starts the FastAPI application
- Enables auto-reload for development

### Accessing the Service
- **Health Check**: http://localhost:8000/
- **API Docs**: http://localhost:8000/docs (auto-generated by FastAPI)

### Monitoring
The application prints detailed logs to the console:
- RSS job start/completion
- Number of articles fetched
- Processing status for each article
- Classification results
- Database operations
- Email sending status

## Database Schema

### Articles Table

| Column     | Type     | Description                          |
|------------|----------|--------------------------------------|
| id         | Integer  | Primary key (auto-increment)         |
| title      | String   | Article title                        |
| link       | String   | Article URL (unique identifier)      |
| summary    | Text     | Article summary/description          |
| category   | String   | AI-classified category               |
| created_at | DateTime | Timestamp (auto-generated)           |

## Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **feedparser**: RSS feed parsing
- **sqlalchemy**: Database ORM
- **apscheduler**: Background job scheduling
- **openai**: OpenAI API client
- **psycopg2-binary**: PostgreSQL adapter
- **python-dotenv**: Environment variable management

## Error Handling

- **RSS Fetch Failures**: Retries 3 times with 2-second delays
- **Classification Failures**: Falls back to "Uncategorized"
- **Email Failures**: Logs error but doesn't crash the job
- **Duplicate Articles**: Silently skipped (by design)

## Scheduler Settings

- **Interval**: Every 4 hours ([app/scheduler.py:66](app/scheduler.py#L66))
- **Type**: Background scheduler (non-blocking)
- **Startup**: Automatic when FastAPI app starts
- **Shutdown**: Graceful shutdown on app termination

## Troubleshooting

### Port Already in Use
The [start.sh](start.sh) script automatically kills processes on port 8000.

### Email Not Sending
- Verify Gmail App Password is correct
- Check SMTP settings in [app/config.py](app/config.py)
- Ensure "Less secure app access" or App Passwords are enabled

### Classification Fails
- Verify OpenAI API key is valid
- Check API quota/billing status
- Review logs for specific error messages


