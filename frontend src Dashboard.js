import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Alert } from '@mui/material';
import axios from 'axios';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function Dashboard() {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      { label: 'CO2 Levels (ppm)', data: [], borderColor: 'rgb(75, 192, 192)', tension: 0.1 },
      { label: 'Temperature (°C)', data: [], borderColor: 'rgb(255, 99, 132)', tension: 0.1 }
    ]
  });
  const [alerts, setAlerts] = useState([]);  // For spike alerts (from first doc)

  useEffect(() => {
    // Fallback poll if WS fails
    const fetchData = async () => {
      try {
        const response = await axios.get(`${API_URL}/data`);
        const data = response.data;
        setChartData({
          labels: data.map(d => new Date(d.timestamp * 1000).toLocaleTimeString()),
          datasets: [
            { ...chartData.datasets[0], data: data.map(d => d.co2) },
            { ...chartData.datasets[1], data: data.map(d => d.temp) }
          ]
        });
        // Check for spikes
        const newAlerts = data.filter(d => d.prediction === "Spike likely").slice(-5).map(d => `CO2 Spike: ${d.co2}ppm at ${new Date(d.timestamp * 1000).toLocaleTimeString()}`);
        setAlerts(newAlerts);
      } catch (error) {
        console.error('Fetch error:', error);
      }
    };

    fetchData();  // Initial load
    const interval = setInterval(fetchData, 30000);  // Poll every 30s

    // WS for real-time
    const ws = new WebSocket(`${API_URL.replace('http', 'ws')}/ws`);
    ws.onopen = () => console.log('WS connected');
    ws.onmessage = (event) => {
      try {
        const newData = JSON.parse(event.data);
        setChartData(prev => ({
          labels: [...prev.labels.slice(-9), new Date(newData.timestamp * 1000).toLocaleTimeString()],
          datasets: [
            { ...prev.datasets[0], data: [...prev.datasets[0].data.slice(-9), newData.co2] },
            { ...prev.datasets[1], data: [...prev.datasets[1].data.slice(-9), newData.temp] }
          ]
        }));
        if (newData.prediction === "Spike likely") {
          setAlerts(prev => [...prev.slice(-4), `CO2 Spike: ${newData.co2}ppm`]);
        }
      } catch (e) {
        console.error('WS parse error:', e);
      }
    };
    ws.onerror = (e) => console.error('WS error:', e);

    return () => {
      clearInterval(interval);
      ws.close();
    };
  }, []);

  const options = {
    responsive: true,
    plugins: { legend: { position: 'top' }, title: { display: true, text: 'Environmental Metrics' } }
  };

  return (
    <div style={{ padding: '20px' }}>
      <Line data={chartData} options={options} />
      {alerts.map((alert, idx) => <Alert key={idx} severity="warning">{alert}</Alert>)}
    </div>
  );
}

export default Dashboard;