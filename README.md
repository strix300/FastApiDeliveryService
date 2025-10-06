Delivery Service API

A FastAPI project for managing shipments, calculating delivery prices, and handling asynchronous updates via Kafka.
Uses PostgreSQL as database, Redis for caching exchange rates, and AIKafka for asynchronous messaging.

Features
	•	CRUD operations for shipments.
	•	Automatic calculation of delivery prices using:
	•	Weight
	•	Content cost
	•	USD to RUB exchange rate (fetched from Central Bank of Russia API and cached in Redis).
	•	Asynchronous task processing with Kafka consumer.
	•	PostgreSQL database with SQLAlchemy async ORM.
	•	Redis caching for exchange rates to reduce API calls.

Technologies
	•	Python 3.13+
	•	FastAPI
	•	SQLAlchemy (async)
	•	PostgreSQL
	•	Redis
	•	Kafka / AIKafka
	•	Docker & Docker Compose

API Endpoints
Shipments
	•	GET /shipments/ – List shipments with pagination and filtering
	•	POST /shipments/ – Create a new shipment
	•	GET /shipments/{id} – Get shipment by ID
	•	GET /types/ – Get shipment types
	•	POST /types/ – Create a new shipment type

Project Structure
app/
├── core/
│   ├── db.py          # Async DB setup
│   └── settings.py    # Configuration
├── models/            # SQLAlchemy models
├── routes/            # FastAPI routers
├── services/          # Business logic
├── tasks/             # Kafka consumer tasks
└── utils/             # Helper functions (delivery price, get/create session_id)

Getting Started
1. Clone repository
git clone https://github.com/your-username/delivery-service.git
cd delivery-service

2. Create .env file

3. Run with Docker Compose
docker-compose up --build