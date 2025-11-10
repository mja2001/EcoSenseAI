[Raspberry Pi Sensors (DHT22 for temp, MQ-135 for CO2)]
↓ (MQTT Publish to env/data)
[AWS IoT Core]
↓ (MQTT Subscribe)
[FastAPI Backend]
├── Ingest Data (Validation + Store to MongoDB)
├── AI Prediction (LSTM: Spike Detection)
├── WebSocket Broadcast (Real-time Updates)
└── PDF Generation (ReportLab)
↓
[MongoDB (env_db.sensor_data)]
↓ (Poll /data or WS)
[React Dashboard (localhost:3000)]
├── Charts (Chart.js: CO2 Trends)
├── Alerts (MUI: Spike Notifications)
└── Auth (JWT Integration)