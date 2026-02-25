/**
 * =============================================================================
 * HOUSE TYPES PAGE
 * =============================================================================
 * Halaman untuk menampilkan berbagai tipe rumah
 * Sesuai dengan Use Case: User -> Tipe Rumah
 * =============================================================================
 */

import React, { useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ThemeContext } from '../contexts/ThemeContext';
import { cmsApi } from '../services/cmsApi';
import AgentContact from '../components/AgentContact';
import '../styles/HouseTypes.css';

export default function HouseTypes() {
  const { theme } = useContext(ThemeContext);
  const navigate = useNavigate();
  const [showAgentContact, setShowAgentContact] = useState(false);
  const [selectedHouse, setSelectedHouse] = useState(null);
  const [houseTypes, setHouseTypes] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch house types from backend
  useEffect(() => {
    const loadHouseTypes = async () => {
      setLoading(true);
      try {
        const response = await cmsApi.getHouseTypes(false); // only active
        if (response.status === 'success' && response.data) {
          setHouseTypes(response.data);
        } else {
          console.error('Failed to load house types:', response.message);
          // Fallback to default data if API fails
          setHouseTypes(getDefaultHouseTypes());
        }
      } catch (error) {
        console.error('Error loading house types:', error);
        // Fallback to default data if API fails
        setHouseTypes(getDefaultHouseTypes());
      } finally {
        setLoading(false);
      }
    };

    loadHouseTypes();
  }, []);

  // Default fallback data if backend is not available
  const getDefaultHouseTypes = () => [
    {
      id: 1,
      name: 'Rumah Modern',
      description: 'Desain kontemporer dengan sentuhan modern. Cocok untuk keluarga muda yang menginginkan gaya hidup praktis dan elegan.',
      price_start: 850000000,
      type_category: 'Modern',
      land_size: '10x15 m',
      building_size: '120 m²',
      bedrooms: 3,
      bathrooms: 2,
      floors: 2,
      carport: 1,
      image_url: '/assets/house-modern.jpg',
      features: ['Smart Home Ready', 'Open Space Concept', 'Large Windows', 'Modern Kitchen', 'Private Garden'],
      display_order: 1,
      is_active: 1
    },
    {
      id: 2,
      name: 'Rumah Klasik',
      description: 'Arsitektur klasik yang timeless dengan detail ornamen yang elegan. Memberikan kesan mewah dan berkelas.',
      price_start: 1200000000,
      type_category: 'Classic',
      land_size: '12x20 m',
      building_size: '180 m²',
      bedrooms: 4,
      bathrooms: 3,
      floors: 2,
      carport: 2,
      image_url: '/assets/house-classic.jpg',
      features: ['Classic Architecture', 'Elegant Details', 'Spacious Rooms', 'Grand Entrance', 'Luxury Finishes'],
      display_order: 2,
      is_active: 1
    },
    {
      id: 3,
      name: 'Rumah Contemporary',
      description: 'Perpaduan unik antara modern dan minimalis. Desain inovatif dengan material berkualitas tinggi.',
      price_start: 950000000,
      type_category: 'Contemporary',
      land_size: '10x18 m',
      building_size: '140 m²',
      bedrooms: 3,
      bathrooms: 2,
      floors: 2,
      carport: 1,
      image_url: '/assets/house-contemporary.jpg',
      features: ['Unique Design', 'High Ceiling', 'Natural Lighting', 'Premium Materials', 'Eco-Friendly'],
      display_order: 3,
      is_active: 1
    },
    {
      id: 4,
      name: 'Rumah Industrial',
      description: 'Gaya industrial yang trendy dengan ekspos material. Perfect untuk yang suka tampilan bold dan edgy.',
      price_start: 780000000,
      type_category: 'Industrial',
      land_size: '9x15 m',
      building_size: '110 m²',
      bedrooms: 3,
      bathrooms: 2,
      floors: 1,
      carport: 1,
      image_url: '/assets/house-industrial.jpg',
      features: ['Exposed Brick', 'Metal Accents', 'Open Layout', 'Loft Style', 'Urban Design'],
      display_order: 4,
      is_active: 1
    }
  ];

  const formatPrice = (price) => {
    if (!price || price === 0) return 'Hubungi Kami';
    const inMillion = price / 1000000;
    if (inMillion >= 1000) {
      return `Rp ${(inMillion / 1000).toFixed(1)}M`;
    }
    return `Rp ${inMillion.toFixed(0)}jt`;
  };

  const handleVirtualTour = (house) => {
    setSelectedHouse(house);
    navigate('/virtual-tour', { state: { houseType: house } });
  };

  const handleAutoLayout = (house) => {
    setSelectedHouse(house);
    navigate('/app', { state: { houseType: house } });
  };

  const handleContactAgent = (house) => {
    setSelectedHouse(house);
    setShowAgentContact(true);
  };

  return (
    <div className="house-types-page" style={{ 
      background: theme?.backgroundColor || '#000000',
      fontFamily: theme?.fontFamily || 'Inter, sans-serif'
    }}>
      {/* Header Section */}
      <div className="house-types-header">
        <h1>Pilih Tipe Rumah</h1>
        <p>Jelajahi berbagai tipe rumah yang sesuai dengan kebutuhan Anda</p>
      </div>

      {/* Loading State */}
      {loading ? (
        <div className="loading-container" style={{ textAlign: 'center', padding: '3rem', color: '#fff' }}>
          <p>Memuat data tipe rumah...</p>
        </div>
      ) : houseTypes.length === 0 ? (
        <div className="empty-container" style={{ textAlign: 'center', padding: '3rem', color: '#999' }}>
          <p>Belum ada tipe rumah tersedia</p>
        </div>
      ) : (
        /* House Cards Grid */
        <div className="house-types-grid">
          {houseTypes.map((house) => (
            <div key={house.id} className="house-card">
              {/* House Image */}
              <div className="house-image">
                <div className="house-image-placeholder">
                  <div className="house-image-gradient"></div>
                </div>
                <div className="house-badge">
                  {house.floors} Lantai
                </div>
              </div>

              {/* House Info */}
              <div className="house-info">
                <h3 className="house-name">{house.name}</h3>
                <p className="house-description">{house.description}</p>

                {/* Specs */}
                <div className="house-specs">
                  <div className="spec-item">
                    <span className="spec-label">Luas Tanah:</span>
                    <span className="spec-value">{house.land_size || '-'}</span>
                  </div>
                  <div className="spec-item">
                    <span className="spec-label">Luas Bangunan:</span>
                    <span className="spec-value">{house.building_size || '-'}</span>
                  </div>
                  <div className="spec-item">
                    <span className="spec-label">Kamar Tidur:</span>
                    <span className="spec-value">{house.bedrooms}</span>
                  </div>
                  <div className="spec-item">
                    <span className="spec-label">Kamar Mandi:</span>
                    <span className="spec-value">{house.bathrooms}</span>
                  </div>
                </div>

                {/* Features */}
                <div className="house-features">
                  {Array.isArray(house.features) && house.features.map((feature, idx) => (
                    <span key={idx} className="feature-tag">
                      {feature}
                    </span>
                  ))}
                </div>

                {/* Price */}
                <div className="house-price">
                  <span className="price-label">Mulai dari</span>
                  <span className="price-value">{formatPrice(house.price_start)}</span>
                </div>

              {/* Actions */}
              <div className="house-actions">
                <button 
                  className="btn-action btn-virtual"
                  onClick={() => handleVirtualTour(house)}
                >
                  Virtual Tour
                </button>
                <button 
                  className="btn-action btn-layout"
                  onClick={() => handleAutoLayout(house)}
                >
                  Auto Layout
                </button>
                <button 
                  className="btn-action btn-contact"
                  onClick={() => handleContactAgent(house)}
                >
                  Hubungi Agent
                </button>
              </div>
            </div>
          </div>
        ))}
        </div>
      )}

      {/* Info Section */}
      <div className="info-section">
        <div className="info-card">
          <h3>Kenapa Memilih Kami?</h3>
          <ul>
            <li><strong>Virtual Tour 3D:</strong> Eksplorasi rumah secara immersive</li>
            <li><strong>Auto Layout AI:</strong> Atur furnitur dengan teknologi AI</li>
            <li><strong>Inspect Detail:</strong> Lihat spesifikasi lengkap setiap ruangan</li>
            <li><strong>Agent Siap Membantu:</strong> Konsultasi langsung dengan expert</li>
          </ul>
        </div>
      </div>

      {/* Agent Contact Modal */}
      {showAgentContact && selectedHouse && (
        <AgentContact 
          propertyName={selectedHouse.name}
          onClose={() => {
            setShowAgentContact(false);
            setSelectedHouse(null);
          }}
        />
      )}
    </div>
  );
}
