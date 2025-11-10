# EcoSenseAI: Enhanced Environmental Monitoring SaaS

AI-powered SaaS platform for real-time environmental monitoring (CO2 levels, temperature) with predictive analytics, alerts, and PDF compliance reports. Data flows from IoT devices to AWS IoT Core, processed by AI models, stored in MongoDB, and visualized in a React dashboard.

## Features
- Auto-Ingestion: Real-time data ingestion via AWS IoT MQTT subscription.
- AI Predictions: LSTM model trains on startup using synthetic data (extend with real datasets). Predicts CO2 spikes.
- Dashboard Alerts: Material-UI alerts for CO2 spikes received via WebSocket.
- PDF Reports: Generate downloadable compliance reports via /report/pdf.
- JWT Authentication: Basic stub for login; middleware protects routes (extend for multi-user support).
- CI Pipeline: GitHub Actions for backend tests on push/pull requests.

## Tech Stack
- Backend: FastAPI (API/WebSockets), TensorFlow (LSTM AI), PyMongo (MongoDB), AWS IoT SDK (MQTT), ReportLab (PDFs), PyJWT (auth).
- Frontend: React 18, Chart.js (visualizations), Material-UI (alerts and components), Axios.
- IoT: AWS IoT Core, Raspberry Pi with DHT22 sensor (stubbed for CO2/MQ-135).
- Database: MongoDB (Atlas free tier recommended).
- Deployment: Docker Compose for local dev; AWS ECS for backend/IoT, Vercel for frontend.
- Testing: Pytest (backend), Jest (frontend stub).

## Quick Start
1. **Prerequisites**: Python 3.10+, Node.js 18+, Docker (optional), MongoDB Atlas (free), AWS IoT Core setup.
2. **Env Setup**: Copy `.env.example` to `.env` and fill values (e.g., AWS cert paths, Mongo URI).
3. **Backend**: `cd backend`, `pip install -r requirements.txt`, `uvicorn main:app --reload --port 8000`.
4. **Train AI** (one-time): `cd backend`, `python models/predictor.py train` (uses `data/co2_historical.csv`).
5. **Frontend**: `cd frontend`, `cp .env.example .env` (add `REACT_APP_API_URL=http://localhost:8000`), `npm install`, `npm start`.
6. **IoT (Raspberry Pi)**: `cd iot`, `pip install -r requirements.txt`, update paths in `sensor_publisher.py`, `python sensor_publisher.py`.
7. **Local Stack**: `docker-compose up` (runs backend + Mongo; start frontend separately).
8. **Test**: POST sample data to `/ingest`, view at `http://localhost:3000`. Check WS at `/ws`.

## API Endpoints
| Endpoint     | Method | Description                          | Auth Required |
|--------------|--------|--------------------------------------|---------------|
| /ingest     | POST   | Ingest sensor data (CO2, temp); runs AI prediction | No |
| /data       | GET    | Fetch last 100 sensor records        | Yes |
| /report/pdf | GET    | Generate and download PDF compliance report | Yes |
| /auth/login | POST   | Login (stub: admin/pass) returns JWT | No |
| /ws         | WS     | WebSocket for real-time updates and broadcasts | No |

## Sample Workflow
- Sensor publishes data → Backend ingests via MQTT, predicts spike → Stores in Mongo → Frontend polls WS for live chart updates → Generate PDF report on demand.

## License
MIT License.
