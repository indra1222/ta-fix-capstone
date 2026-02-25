"""
=============================================================================
CMS Controller - Content Management System Controller
=============================================================================
File: CMSController.py
Fungsi: Mengelola CMS content dan theme configuration
Endpoints:
    - GET  /api/cms/content  : Mengambil semua CMS content
    - PUT  /api/cms/content  : Update CMS content section
    - GET  /api/cms/theme    : Mengambil theme configuration
    - PUT  /api/cms/theme    : Update theme configuration
=============================================================================
"""
from flask import jsonify, request
from app.models.CMS import CMS


class CMSController:
    """
    Controller untuk menangani CMS endpoints
    Mengelola content dinamis dan theme customization
    """
    
    # =========================================================================
    # CONTENT MANAGEMENT
    # =========================================================================
    
    @staticmethod
    def get_content():
        """
        GET /api/cms/content
        Mengambil semua CMS content yang aktif
        
        Returns:
            JSON: {
                "status": "success",
                "content": {
                    "section_name": {...},
                    ...
                }
            }
        """
        content = CMS.get_all_content()
        return jsonify({
            "status": "success",
            "content": content
        })
    
    @staticmethod
    def update_content():
        """
        PUT /api/cms/content
        Update atau insert CMS content section
        
        Request Body:
            {
                "section": "section_name",
                "content": {...}
            }
        
        Returns:
            JSON: {
                "status": "success",
                "content": {...}
            }
        """
        data = request.json
        section = data.get("section")
        content = data.get("content")
        
        # Validasi input
        if not section:
            return jsonify({
                "status": "error",
                "message": "Section is required"
            }), 400
        
        try:
            # Update atau insert content
            CMS.upsert_section(section, content)
            
            # Return semua content terbaru
            all_content = CMS.get_all_content()
            return jsonify({
                "status": "success",
                "content": all_content
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    # =========================================================================
    # THEME MANAGEMENT
    # =========================================================================
    
    @staticmethod
    def get_theme():
        """
        GET /api/cms/theme
        Mengambil theme configuration
        
        Returns:
            JSON: {
                "status": "success",
                "theme": {
                    "navbarColor": "#0a0a0a",
                    "homeBgColor": "#000000",
                    ...
                }
            }
        """
        theme = CMS.get_theme()
        
        # Jika tidak ada theme di database, gunakan default
        if not theme:
            theme = CMSController._get_default_theme()
        
        return jsonify({
            "status": "success",
            "theme": theme
        })
    
    @staticmethod
    def update_theme():
        """
        PUT /api/cms/theme
        Update theme configuration
        
        Request Body:
            {
                "theme": {
                    "navbarColor": "#0a0a0a",
                    "homeBgColor": "#000000",
                    ...
                }
            }
        
        Returns:
            JSON: {
                "status": "success",
                "theme": {...}
            }
        """
        data = request.json.get("theme", {})
        
        # Validasi input
        if not data:
            return jsonify({
                "status": "error",
                "message": "Theme object required"
            }), 400
        
        try:
            # Update theme di database
            CMS.upsert_theme(data)
            
            return jsonify({
                "status": "success",
                "theme": data
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    @staticmethod
    def _get_default_theme():
        """
        Generate default theme configuration
        Digunakan jika tidak ada theme di database
        
        Returns:
            dict: Default theme configuration dengan warna hitam/gelap
        """
        return {
            # Navbar styling
            "navbarColor": "#0a0a0a",
            "navbarTextColor": "#ffffff",
            "fontFamily": "'Inter', 'Poppins', 'Segoe UI', sans-serif",
            
            # Page background colors
            "homeBgColor": "#000000",      # Home page
            "aboutBgColor": "#000000",     # About page
            "newsBgColor": "#000000",      # News page
            "faqBgColor": "#000000",       # FAQ page
            "qnaBgColor": "#000000",       # Q&A page
            "contactBgColor": "#000000",   # Contact page
            "layoutBgColor": "#0a0a0a",    # Layout App page
            "tourBgColor": "#000000"       # Virtual Tour page
        }
