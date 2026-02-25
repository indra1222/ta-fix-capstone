import React, { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ThemeContext } from '../contexts/ThemeContext';
import UnityPlayer from '../components/UnityPlayer';
import AgentContact from '../components/AgentContact';
import '../styles/VirtualTour.css';

export default function VirtualTour() {
  const { theme } = useContext(ThemeContext);
  const navigate = useNavigate();
  const [showAgentContact, setShowAgentContact] = useState(false);
  const [tourMode, setTourMode] = useState('explore'); // explore, inspect
  
  const handleInspectRumah = () => {
    setTourMode('inspect');
  };

  const handleEksplorasiTour = () => {
    setTourMode('explore');
  };

  const handleAutoLayout = () => {
    navigate('/app');
  };

  const handleHubungiAgent = () => {
    setShowAgentContact(true);
  };
  
  return (
    <div className="virtual-tour-page" style={{ background: theme?.tourBgColor || '#000000' }}>
      <div className="tour-header">
        <h1>Virtual Tour Interaktif 3D</h1>
        <p>Jelajahi ruang dalam format 360-degree yang immersive</p>
        <div className="tour-mode-indicator">
          {tourMode === 'explore' ? 'Mode: Eksplorasi Virtual Tour' : 'Mode: Inspect Rumah'}
        </div>
      </div>

      {/* Feature Menu */}
      <div className="tour-feature-menu">
        <button 
          className={`feature-btn ${tourMode === 'explore' ? 'active' : ''}`}
          onClick={handleEksplorasiTour}
          title="Jelajahi properti secara bebas"
        >
          Eksplorasi Virtual Tour
        </button>
        <button 
          className={`feature-btn ${tourMode === 'inspect' ? 'active' : ''}`}
          onClick={handleInspectRumah}
          title="Inspect detail ruangan dan properti"
        >
          Inspect Rumah
        </button>
        <button 
          className="feature-btn"
          onClick={handleAutoLayout}
          title="Atur tata letak furnitur otomatis"
        >
          Auto Layout
        </button>
        <button 
          className="feature-btn feature-btn-primary"
          onClick={handleHubungiAgent}
          title="Hubungi agent untuk info lebih lanjut"
        >
          Hubungi Agent Properti
        </button>
      </div>

      <div className="tour-container">
        <UnityPlayer mode={tourMode} />
        
        {/* Inspect Info Panel */}
        {tourMode === 'inspect' && (
          <div className="inspect-info-panel">
            <h3>Mode Inspect Rumah</h3>
            <ul>
              <li>Klik pada objek untuk melihat detail</li>
              <li>Gunakan mouse untuk zoom in/out</li>
              <li>Lihat dimensi dan spesifikasi ruangan</li>
            </ul>
          </div>
        )}
      </div>

      <div className="tour-controls">
        <button className="btn-back-home" onClick={() => navigate('/')}>
          ← Kembali ke Home
        </button>
      </div>

      {/* Agent Contact Modal */}
      {showAgentContact && (
        <AgentContact 
          propertyName="Virtual Tour Properti"
          onClose={() => setShowAgentContact(false)}
        />
      )}
    </div>
  );
}
