import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from '../services/api';
import '../styles/Gallery.css';

function Gallery() {
  const [layouts, setLayouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('public'); // 'public' or 'all'
  const [searchQuery, setSearchQuery] = useState('');
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'

  useEffect(() => {
    fetchLayouts();
  }, [filter]);

  const fetchLayouts = async () => {
    setLoading(true);
    try {
      const endpoint = filter === 'public' 
        ? `${API_BASE_URL}/api/layouts/public`
        : `${API_BASE_URL}/api/layouts`;
      
      const response = await fetch(endpoint);
      const data = await response.json();
      
      if (data.success) {
        setLayouts(data.data || []);
      } else {
        console.error('Failed to fetch layouts:', data.message);
        setLayouts([]);
      }
    } catch (error) {
      console.error('Error fetching layouts:', error);
      setLayouts([]);
    } finally {
      setLoading(false);
    }
  };

  const filteredLayouts = layouts.filter(layout => {
    if (!searchQuery) return true;
    return layout.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
           layout.room_width?.toString().includes(searchQuery) ||
           layout.room_length?.toString().includes(searchQuery);
  });

  const handleDeleteLayout = async (layoutId) => {
    if (!window.confirm('Are you sure you want to delete this layout?')) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/layouts/${layoutId}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      
      if (data.success) {
        alert('Layout deleted successfully!');
        fetchLayouts();
      } else {
        alert('Failed to delete layout: ' + data.message);
      }
    } catch (error) {
      console.error('Error deleting layout:', error);
      alert('Error deleting layout');
    }
  };

  const handleTogglePublic = async (layoutId, currentStatus) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/layouts/${layoutId}/toggle-public`, {
        method: 'PUT',
      });
      const data = await response.json();
      
      if (data.success) {
        alert(`Layout is now ${currentStatus ? 'private' : 'public'}!`);
        fetchLayouts();
      } else {
        alert('Failed to toggle visibility: ' + data.message);
      }
    } catch (error) {
      console.error('Error toggling visibility:', error);
      alert('Error toggling visibility');
    }
  };

  const handleCloneLayout = (layout) => {
    // Clone layout to designer
    window.location.href = `/app?clone=${layout.id}`;
  };

  return (
    <div className="gallery-page">
      {/* Header */}
      <div className="gallery-header">
        <h1 className="gallery-title">🖼️ Layout Gallery</h1>
        <p className="gallery-subtitle">
          Jelajahi dan dapatkan inspirasi dari koleksi layout furnitur kami
        </p>
      </div>

      {/* Controls */}
      <div className="gallery-controls">
        <div className="gallery-filters">
          <button 
            className={`filter-btn ${filter === 'public' ? 'active' : ''}`}
            onClick={() => setFilter('public')}
          >
            🌐 Public Layouts
          </button>
          <button 
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            📁 All Layouts
          </button>
        </div>

        <div className="gallery-search">
          <input 
            type="text"
            placeholder="🔍 Search layouts..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="gallery-view-toggle">
          <button 
            className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`}
            onClick={() => setViewMode('grid')}
            title="Grid View"
          >
            ⊞
          </button>
          <button 
            className={`view-btn ${viewMode === 'list' ? 'active' : ''}`}
            onClick={() => setViewMode('list')}
            title="List View"
          >
            ≡
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="gallery-content">
        {loading ? (
          <div className="gallery-loading">
            <div className="spinner"></div>
            <p>Loading layouts...</p>
          </div>
        ) : filteredLayouts.length === 0 ? (
          <div className="gallery-empty">
            <p>No layouts found</p>
            <a href="/app" className="btn-primary">Create Your First Layout</a>
          </div>
        ) : (
          <div className={`gallery-grid ${viewMode}`}>
            {filteredLayouts.map((layout) => (
              <div key={layout.id} className="layout-card">
                <div className="layout-card-preview">
                  {layout.thumbnail_url ? (
                    <img 
                      src={layout.thumbnail_url} 
                      alt={layout.name || 'Layout'} 
                      className="layout-thumbnail"
                    />
                  ) : (
                    <div className="layout-placeholder">
                      <span className="placeholder-icon">🏠</span>
                      <p>No Preview</p>
                    </div>
                  )}
                  
                  {layout.is_public && (
                    <span className="layout-badge public">Public</span>
                  )}
                </div>

                <div className="layout-card-content">
                  <h3 className="layout-name">
                    {layout.name || `Layout #${layout.id}`}
                  </h3>
                  
                  <div className="layout-info">
                    <span className="layout-info-item">
                      📏 {layout.room_width || 0}m × {layout.room_length || 0}m
                    </span>
                    <span className="layout-info-item">
                      🛋️ {Array.isArray(layout.furniture) ? layout.furniture.length : 0} items
                    </span>
                  </div>

                  {layout.created_at && (
                    <p className="layout-date">
                      📅 {new Date(layout.created_at).toLocaleDateString()}
                    </p>
                  )}

                  <div className="layout-actions">
                    <button 
                      className="btn-action btn-view"
                      onClick={() => window.location.href = `/app?view=${layout.id}`}
                    >
                      👁️ View
                    </button>
                    <button 
                      className="btn-action btn-clone"
                      onClick={() => handleCloneLayout(layout)}
                    >
                      🔄 Clone
                    </button>
                    
                    {/* Owner actions - uncomment when implementing auth */}
                    {/* <button 
                      className="btn-action btn-toggle"
                      onClick={() => handleTogglePublic(layout.id, layout.is_public)}
                      title={layout.is_public ? 'Make Private' : 'Make Public'}
                    >
                      {layout.is_public ? '🔓' : '🔒'}
                    </button>
                    <button 
                      className="btn-action btn-delete"
                      onClick={() => handleDeleteLayout(layout.id)}
                    >
                      🗑️
                    </button> */}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Gallery;
