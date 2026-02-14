import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

function App() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await fetch('/api/logs');
        const data = await response.json();
        setLogs(data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    fetchLogs();

    // Optional Pro-Tip: Automatically refresh the data every 5 seconds
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, []);

  // --- DATA AGGREGATION FUNCTION ---
  const getChartData = () => {
    const counts = { Plastic: 0, Metal: 0, Paper: 0, Glass: 0, Trash: 0 };
    logs.forEach(log => {
      if (counts[log.detectedClass] !== undefined) {
        counts[log.detectedClass]++;
      }
    });
    // Convert the object into an array format Recharts can read
    return Object.keys(counts).map(key => ({
      name: key,
      Total: counts[key]
    }));
  };

  if (loading) return <div>Loading Command Center Data...</div>;

  const chartData = getChartData();

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>AiGenics Command Center</h1>

      {/* --- VISUAL ANALYTICS SECTION --- */}
      <div style={{ marginBottom: '40px', height: '300px', width: '100%', maxWidth: '600px' }}>
        <h2>Waste Distribution Analytics</h2>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="Total" fill="#3b82f6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* --- LIVE RAW DATA TABLE --- */}
      <div>
        <h2>Live Waste Logs</h2>
        <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #ccc' }}>
              <th>Time</th>
              <th>Smart Bin ID</th>
              <th>Detected Class</th>
              <th>AI Confidence</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log._id} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '8px 0' }}>{new Date(log.createdAt).toLocaleTimeString()}</td>
                <td>{log.binId?.binId || 'Unknown'}</td>
                <td>{log.detectedClass}</td>
                <td>{(log.confidence * 100).toFixed(1)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;