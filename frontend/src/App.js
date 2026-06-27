import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [allData, setAllData] = useState(null);
  const [timePeriods, setTimePeriods] = useState({});
  const [selectedPeriod, setSelectedPeriod] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.has('logged_in') || params.has('code')) {
      setIsLoggedIn(true);
      fetchResults();
    }
  }, []);

  const getTimePeriod = (isoDateString) => {
    const date = new Date(isoDateString);
    const hour = date.getHours();
    
    if (hour >= 6 && hour < 12) return 'Morning';
    if (hour >= 12 && hour < 16) return 'Noon';
    if (hour >= 16 && hour < 21) return 'Evening';
    return 'Night';
  };

  const getDominantMood = (tracks) => {
    const counts = { Happy: 0, Mellow: 0, Energetic: 0 };
    tracks.forEach(t => {
      if (counts[t.mood] !== undefined) counts[t.mood]++;
    });
    return Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
  };

  const buildChartData = (tracksWithMoods) => {
    const hourly = {};
    for (let i = 0; i < 24; i++) {
      hourly[i] = { Happy: 0, Mellow: 0, Energetic: 0 };
    }

    tracksWithMoods.forEach(track => {
      const date = new Date(track.played_at);
      const hour = date.getHours();
      if (hourly[hour] && hourly[hour][track.mood] !== undefined) {
        hourly[hour][track.mood]++;
      }
    });

    return Object.keys(hourly).map(hour => ({
      hour: `${hour}:00`,
      Happy: hourly[hour].Happy,
      Mellow: hourly[hour].Mellow,
      Energetic: hourly[hour].Energetic
    }));
  };

  const fetchResults = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/test-data');
      const data = response.data;

      const tracksWithMoods = data.tracks.map((track, index) => ({
        ...track,
        mood: data.moods[index]
      }));

      setAllData(tracksWithMoods);
      setChartData(buildChartData(tracksWithMoods));

      const periods = {
        Morning: [],
        Noon: [],
        Evening: [],
        Night: []
      };

      tracksWithMoods.forEach(track => {
        const period = getTimePeriod(track.played_at);
        periods[period].push(track);
      });

      const periodsWithMood = {};
      Object.keys(periods).forEach(key => {
        periodsWithMood[key] = {
          tracks: periods[key],
          dominantMood: periods[key].length > 0 ? getDominantMood(periods[key]) : 'Unknown'
        };
      });

      setTimePeriods(periodsWithMood);
    } catch (error) {
      console.error('Error fetching results:', error);
    }
    setLoading(false);
  };

  if (!isLoggedIn) {
    return (
      <div className="app-container">
        <div className="login-screen">
          <h1>Spotify Mood Classifier</h1>
          <p>Connect your Spotify to analyze your listening moods</p>
          <a href="http://localhost:8000/login" className="login-button">
            Connect Spotify
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <div className="results-screen">
        <h1>Your Mood by Time of Day</h1>
        
        {loading ? (
          <p>Loading...</p>
        ) : (
          <>
            <div className="sectors-container">
              {['Morning', 'Noon', 'Evening', 'Night'].map(period => {
                const data = timePeriods[period];
                const moodColor = {
                  Happy: '#1db954',
                  Mellow: '#3457dc',
                  Energetic: '#e74c3c'
                }[data?.dominantMood] || '#666';

                return (
                  <div
                    key={period}
                    className="sector"
                    style={{ borderColor: moodColor }}
                    onClick={() => setSelectedPeriod(period)}
                  >
                    <div className="sector-time">{period}</div>
                    <div className="sector-mood" style={{ color: moodColor }}>
                      {data?.dominantMood}
                    </div>
                    <div className="sector-count">
                      {data?.tracks.length || 0} songs
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="chart-section">
              <h2>Mood Intensity Over Time</h2>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                  <XAxis 
                    dataKey="hour" 
                    stroke="#b3b3b3"
                  />
                  <YAxis 
                    stroke="#b3b3b3"
                    label={{ value: '# of Songs', angle: -90, position: 'insideLeft' }}
                  />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}
                    labelStyle={{ color: '#fff' }}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="Happy" 
                    stroke="#1db954" 
                    dot={false}
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="Mellow" 
                    stroke="#3457dc" 
                    dot={false}
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="Energetic" 
                    stroke="#e74c3c" 
                    dot={false}
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {selectedPeriod && (
              <div className="modal-overlay" onClick={() => setSelectedPeriod(null)}>
                <div className="modal" onClick={e => e.stopPropagation()}>
                  <div className="modal-header">
                    <h2>{selectedPeriod}</h2>
                    <button
                      className="modal-close"
                      onClick={() => setSelectedPeriod(null)}
                    >
                      ✕
                    </button>
                  </div>

                  <div className="modal-tracks">
                    {timePeriods[selectedPeriod]?.tracks.map((track, index) => {
                      const moodColor = {
                        Happy: '#1db954',
                        Mellow: '#3457dc',
                        Energetic: '#e74c3c'
                      }[track.mood] || '#666';

                      return (
                        <div key={index} className="modal-track">
                          <div className="track-info">
                            <span className="track-name">{track.name}</span>
                            <span className="track-artist">{track.artist}</span>
                          </div>
                          <span
                            className="track-mood-badge"
                            style={{ backgroundColor: moodColor }}
                          >
                            {track.mood}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;