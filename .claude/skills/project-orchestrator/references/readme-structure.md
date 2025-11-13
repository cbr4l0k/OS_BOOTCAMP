# README Structure Guide

A project README should be informative without being overly promotional. The goal is clarity and utility.

## Core Sections

### 1. Project Title & Brief Description (2-3 sentences)
What the project does and why it exists. No marketing fluff.

Example:
> # Weather API Service
> 
> REST API that aggregates weather data from multiple providers and exposes a unified interface. Built to solve the problem of inconsistent weather data formats across different services.

### 2. Context & Rationale
Explain the business logic or problem domain. Why does this project matter? What real-world issue does it address?

Example:
> ## Why This Exists
> 
> Weather data providers use different formats, units, and update frequencies. This creates integration headaches when building applications that need weather data. This service normalizes data from OpenWeather, WeatherAPI, and NOAA into a single consistent format, handling retries, caching, and fallbacks automatically.

### 3. Installation
Clear, step-by-step instructions. Include prerequisites.

Example:
> ## Installation
> 
> **Prerequisites:**
> - Python 3.11+
> - Docker (optional)
> 
> **Local setup:**
> ```bash
> pip install -e .
> ```
> 
> **Docker setup:**
> ```bash
> docker-compose up
> ```

### 4. Running the Project
How to actually use it. Include examples.

Example:
> ## Usage
> 
> Start the server:
> ```bash
> uvicorn src.weather_api.main:app --reload
> ```
> 
> The API runs at `http://localhost:8000`

### 5. API Endpoints / Interface
Document the actual interface - API routes, CLI commands, etc.

Example:
> ## API Endpoints
> 
> - `GET /weather/{city}` - Get current weather for a city
> - `GET /forecast/{city}` - Get 5-day forecast
> - `GET /health` - Health check endpoint
> 
> **Example request:**
> ```bash
> curl http://localhost:8000/weather/London
> ```

### 6. Architecture & Technology Choices
Explain the stack and why you chose it. Be specific about tradeoffs.

Example:
> ## Architecture
> 
> **Tech Stack:**
> - FastAPI - Async support and automatic OpenAPI docs
> - Redis - Response caching (5-minute TTL)
> - PostgreSQL - Historical data storage
> 
> **Key Design Decisions:**
> - Async architecture to handle multiple provider requests in parallel
> - Redis caching reduces API costs and improves response times
> - PostgreSQL for audit trail and analytics on weather patterns
> - Docker multi-stage builds keep production images under 100MB

### 7. Configuration (if applicable)
Environment variables, config files, etc.

Example:
> ## Configuration
> 
> Set these environment variables:
> ```
> OPENWEATHER_API_KEY=your_key
> WEATHER_API_KEY=your_key
> DATABASE_URL=postgresql://user:pass@localhost/weather
> REDIS_URL=redis://localhost:6379
> ```

## Style Guidelines

- **Be direct**: Say what something is, not what it "aims to be" or "strives to do"
- **Avoid fluff**: Skip phrases like "cutting-edge," "robust," "powerful"
- **Be specific**: "Handles 1000 requests/second" not "high performance"
- **Explain tradeoffs**: Why FastAPI over Flask? Why Redis over Memcached?
- **Use examples**: Show actual code/commands, not just descriptions
- **Keep it scannable**: Headers, code blocks, bullet points where appropriate
