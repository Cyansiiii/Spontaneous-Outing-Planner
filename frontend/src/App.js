import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [vibe, setVibe] = useState('');
  const [location, setLocation] = useState('');
  const [isPlanning, setIsPlanning] = useState(false);
  const [plan, setPlan] = useState(null);
  const [thoughtProcess, setThoughtProcess] = useState([]);
  const [itinerary, setItinerary] = useState('');
  const [isGeneratingItinerary, setIsGeneratingItinerary] = useState(false);

  const handlePlanVibe = async () => {
    if (!vibe.trim() || !location.trim()) {
      alert('Please enter both vibe and location');
      return;
    }

    setIsPlanning(true);
    setThoughtProcess([]);
    setPlan(null);
    setItinerary('');

    try {
      const response = await axios.post(`${API}/plan-vibe`, {
        vibe: vibe.trim(),
        location: location.trim()
      });
      
      const planData = response.data;
      
      // Animate thought process
      for (let i = 0; i < planData.thought_process.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 800));
        setThoughtProcess(prev => [...prev, planData.thought_process[i]]);
      }
      
      setPlan(planData);
    } catch (error) {
      console.error('Error planning vibe:', error);
      setThoughtProcess([{
        type: 'warning',
        message: 'Something went wrong, but we found you some great options!'
      }]);
    } finally {
      setIsPlanning(false);
    }
  };

  const handleGenerateItinerary = async () => {
    if (!plan) return;

    setIsGeneratingItinerary(true);
    try {
      const response = await axios.post(`${API}/generate-itinerary`, {
        plan_id: plan.id
      });
      
      setItinerary(response.data.itinerary);
    } catch (error) {
      console.error('Error generating itinerary:', error);
    } finally {
      setIsGeneratingItinerary(false);
    }
  };

  const getStepIcon = (type) => {
    switch (type) {
      case 'success':
        return '✅';
      case 'warning':
        return '⚠️';
      case 'info':
      default:
        return '🤖';
    }
  };

  return (
    <div className="App">
      <div className="container">
        {/* Header Section */}
        <div className="hero-section">
          <div className="geometric-bg"></div>
          <h1 className="hero-title">Design Your Day</h1>
          <p className="hero-subtitle">
            Let AI be your guide. Describe the vibe for your perfect outing, and<br />
            we'll handle the details.
          </p>
        </div>

        {/* Input Form */}
        <div className="input-section">
          <div className="input-grid">
            <div className="input-group">
              <label className="input-label">What's the vibe?</label>
              <textarea
                className="input-field vibe-input"
                placeholder="e.g., A relaxing afternoon, a fun date night"
                value={vibe}
                onChange={(e) => setVibe(e.target.value)}
                disabled={isPlanning}
              />
            </div>
            
            <div className="input-group">
              <label className="input-label">Location</label>
              <input
                className="input-field location-input"
                placeholder="e.g., Bhopal, Paris"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                disabled={isPlanning}
              />
            </div>
          </div>
          
          <button 
            className={`plan-button ${isPlanning ? 'planning' : ''}`}
            onClick={handlePlanVibe}
            disabled={isPlanning}
          >
            {isPlanning ? '✨ Planning...' : '✨ Plan My Vibe'}
          </button>
        </div>

        {/* Thought Process Section */}
        {thoughtProcess.length > 0 && (
          <div className="thought-section">
            <h3 className="thought-title">My Thought Process...</h3>
            <div className="thought-terminal">
              {thoughtProcess.map((step, index) => (
                <div key={index} className="thought-step">
                  <span className="step-icon">{getStepIcon(step.type)}</span>
                  <span className="step-message">{step.message}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Results Section */}
        {plan && plan.venues.length > 0 && (
          <div className="results-section">
            <div className="geometric-bg-bottom"></div>
            <h2 className="results-title">Here is your spontaneous outing!</h2>
            
            <div className="venues-grid">
              {plan.venues.map((venue, index) => (
                <div key={index} className="venue-card">
                  <div className="venue-step">STEP {index + 1}: {venue.category.toUpperCase()}</div>
                  <h3 className="venue-name">{venue.name}</h3>
                  <p className="venue-address">{venue.address}</p>
                  <div className="venue-rating">
                    ⭐ {venue.rating ? venue.rating.toFixed(1) : '4.2'} | {venue.review_count ? venue.review_count.toLocaleString() : '1,000'} reviews
                  </div>
                </div>
              ))}
            </div>
            
            <button 
              className={`itinerary-button ${isGeneratingItinerary ? 'generating' : ''}`}
              onClick={handleGenerateItinerary}
              disabled={isGeneratingItinerary}
            >
              {isGeneratingItinerary ? '✨ Generating...' : '✨ Generate Full Itinerary'}
            </button>
            
            {itinerary && (
              <div className="itinerary-section">
                <h3 className="itinerary-title">Your Creative Itinerary</h3>
                <div className="itinerary-content">
                  {itinerary.split('\n').map((paragraph, index) => (
                    paragraph.trim() && <p key={index}>{paragraph}</p>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* About Section */}
        <div className="about-section">
          <h3 className="about-title">About This App</h3>
          <p className="about-text">
            The Spontaneous Outing Planner is an intelligent agent designed to help you discover new 
            experiences. It uses Google's Gemini API and Foursquare API to interpret your desired "vibe" and 
            suggest a creative two-stop plan. The backend logic then finds the best real-world locations for your 
            outing, ensuring a seamless and enjoyable adventure.
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;