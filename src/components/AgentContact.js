/**
 * =============================================================================
 * AGENT CONTACT COMPONENT
 * =============================================================================
 * Komponen untuk menghubungi Agent Properti
 * Digunakan di Virtual Tour, Inspect Rumah, dan halaman lainnya
 * =============================================================================
 */

import React, { useState } from 'react';
import { NotificationManager } from './Notification';
import '../styles/AgentContact.css';

export default function AgentContact({ propertyName = "Properti", onClose }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: ''
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name || !formData.email || !formData.message) {
      NotificationManager.error('Mohon lengkapi semua field yang wajib diisi');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          subject: `Pertanyaan tentang ${propertyName}`,
          message: `Telepon: ${formData.phone}\n\n${formData.message}`
        })
      });

      const data = await response.json();

      if (data.status === 'success') {
        NotificationManager.success('Pesan berhasil dikirim! Agent kami akan menghubungi Anda segera.');
        setFormData({ name: '', email: '', phone: '', message: '' });
        if (onClose) setTimeout(onClose, 2000);
      } else {
        NotificationManager.error('Gagal mengirim pesan. Silakan coba lagi.');
      }
    } catch (error) {
      console.error('Error:', error);
      NotificationManager.error('Terjadi kesalahan. Silakan coba lagi.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="agent-contact-overlay" onClick={onClose}>
      <div className="agent-contact-modal" onClick={(e) => e.stopPropagation()}>
        <button className="agent-contact-close" onClick={onClose}>×</button>
        
        <div className="agent-contact-header">
          <h2>Hubungi Agent Properti</h2>
          <p>Dapatkan informasi lengkap tentang {propertyName}</p>
        </div>

        <form onSubmit={handleSubmit} className="agent-contact-form">
          <div className="form-group">
            <label htmlFor="name">Nama Lengkap *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Masukkan nama Anda"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="email@example.com"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="phone">Nomor Telepon</label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="08xx-xxxx-xxxx"
            />
          </div>

          <div className="form-group">
            <label htmlFor="message">Pesan *</label>
            <textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleChange}
              placeholder="Saya tertarik dengan properti ini. Mohon informasi lebih lanjut..."
              rows="4"
              required
            />
          </div>

          <div className="agent-contact-actions">
            <button 
              type="button" 
              className="btn-cancel" 
              onClick={onClose}
              disabled={loading}
            >
              Batal
            </button>
            <button 
              type="submit" 
              className="btn-submit"
              disabled={loading}
            >
              {loading ? 'Mengirim...' : 'Kirim Pesan'}
            </button>
          </div>
        </form>

        <div className="agent-contact-info">
          <p><strong>Agent kami siap membantu Anda 24/7</strong></p>
          <p>Fast Response: 0812-3456-7890</p>
        </div>
      </div>
    </div>
  );
}
