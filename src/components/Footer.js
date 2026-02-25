import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { API_BASE_URL } from '../services/api';
import '../styles/Footer.css';

function Footer() {
  const [socialMedia, setSocialMedia] = useState([]);
  const currentYear = new Date().getFullYear();

  useEffect(() => {
    // Fetch active social media links
    fetch(`${API_BASE_URL}/api/social-media/active`)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setSocialMedia(data.data || []);
        }
      })
      .catch(err => console.error('Failed to fetch social media links:', err));
  }, []);

  const getSocialIcon = (platform) => {
    const icons = {
      'facebook': '📘',
      'instagram': '📷',
      'twitter': '🐦',
      'linkedin': '💼',
      'youtube': '📺',
      'tiktok': '🎵',
      'whatsapp': '💬'
    };
    return icons[platform.toLowerCase()] || '🔗';
  };

  return (
    <footer className="app-footer">
      <div className="footer-container">
        {/* Column 1: About */}
        <div className="footer-column">
          <h3 className="footer-heading">FurniLayout</h3>
          <p className="footer-description">
            Aplikasi AI untuk merancang tata letak furnitur ruangan Anda dengan mudah dan cepat.
          </p>
          <div className="footer-logo">
            <img src="/assets/logo.png" alt="FurniLayout Logo" className="footer-logo-img" />
          </div>
        </div>

        {/* Column 2: Quick Links */}
        <div className="footer-column">
          <h4 className="footer-heading">Quick Links</h4>
          <ul className="footer-links">
            <li><Link to="/">🏠 Home</Link></li>
            <li><Link to="/app">🎨 Designer</Link></li>
            <li><Link to="/gallery">🖼️ Gallery</Link></li>
            <li><Link to="/news">📰 News</Link></li>
            <li><Link to="/about">ℹ️ About</Link></li>
          </ul>
        </div>

        {/* Column 3: Help & Support */}
        <div className="footer-column">
          <h4 className="footer-heading">Help & Support</h4>
          <ul className="footer-links">
            <li><Link to="/faq">📖 FAQ</Link></li>
            <li><Link to="/qna">💬 Ask Question</Link></li>
            <li><Link to="/contact">📧 Contact Us</Link></li>
          </ul>
        </div>

        {/* Column 4: Follow Us */}
        <div className="footer-column">
          <h4 className="footer-heading">Follow Us</h4>
          {socialMedia.length > 0 ? (
            <ul className="footer-social">
              {socialMedia.map((social) => (
                <li key={social.id}>
                  <a 
                    href={social.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="social-link"
                  >
                    <span className="social-icon">{getSocialIcon(social.platform)}</span>
                    <span className="social-name">{social.platform}</span>
                  </a>
                </li>
              ))}
            </ul>
          ) : (
            <p className="footer-text-muted">No social media links available</p>
          )}
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="footer-bottom">
        <div className="footer-bottom-container">
          <p className="footer-copyright">
            &copy; {currentYear} FurniLayout. All Rights Reserved.
          </p>
          <div className="footer-legal">
            <Link to="/privacy">Privacy Policy</Link>
            <span className="footer-separator">|</span>
            <Link to="/terms">Terms of Service</Link>
            <span className="footer-separator">|</span>
            <span className="footer-version">v2.0.0</span>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
