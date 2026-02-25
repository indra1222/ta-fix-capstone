"""
=============================================================================
CMS Model - Content Management System Data Model
=============================================================================
File: CMS.py
Fungsi: Mengelola data CMS content dan theme di database
Table: cms_content
    - section (VARCHAR): Nama section (e.g., 'theme', 'home', 'about')
    - content_data (JSON): Data content dalam format JSON
    - is_active (BOOLEAN): Status aktif/non-aktif
=============================================================================
"""
import json
from app.models.BaseModel import BaseModel


class CMS(BaseModel):
    """
    CMS Model untuk mengelola content dan theme
    Menggunakan table cms_content dengan struktur JSON flexible
    """
    
    # =========================================================================
    # CONTENT OPERATIONS
    # =========================================================================
    
    @classmethod
    def get_all_content(cls):
        """
        Mengambil semua CMS content yang aktif
        
        Returns:
            dict: {
                "section_name": {...},
                "section_name_2": {...}
            }
        
        Example:
            {
                "home": {"hero": {...}, "services": {...}},
                "about": {"profile": {...}, "vision": {...}}
            }
        """
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Ambil semua content yang aktif
        cursor.execute("""
            SELECT section, content_data 
            FROM cms_content 
            WHERE is_active = 1
        """)
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Process hasil query
        content = {}
        for r in rows:
            # Skip jika content null atau kosong
            if r["content_data"] is None:
                continue
            
            # Parse JSON content
            try:
                # Jika sudah dict, langsung assign
                if isinstance(r["content_data"], dict):
                    content[r["section"]] = r["content_data"]
                # Jika string, parse dulu
                elif isinstance(r["content_data"], str):
                    content[r["section"]] = json.loads(r["content_data"])
                else:
                    content[r["section"]] = r["content_data"]
            except json.JSONDecodeError:
                # Jika gagal parse, skip section ini
                continue
        
        return content
    
    @classmethod
    def upsert_section(cls, section, content_obj):
        """
        Insert atau update CMS section
        Jika section sudah ada, akan di-update
        Jika belum ada, akan di-insert
        
        Args:
            section (str): Nama section
            content_obj (dict): Content object
        
        Returns:
            bool: True jika berhasil
        
        Example:
            CMS.upsert_section('home', {
                'hero': {'title': 'Welcome', 'subtitle': '...'}
            })
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Cek apakah section sudah ada
        cursor.execute("""
            SELECT id 
            FROM cms_content 
            WHERE section = %s
        """, (section,))
        existing = cursor.fetchone()
        
        # Convert content ke JSON string
        content_json = json.dumps(content_obj, ensure_ascii=False)
        
        if existing:
            # UPDATE - section sudah ada
            cursor.execute("""
                UPDATE cms_content 
                SET content_data = %s, 
                    updated_by = 1, 
                    updated_at = NOW()
                WHERE section = %s
            """, (content_json, section))
        else:
            # INSERT - section baru
            cursor.execute("""
                INSERT INTO cms_content 
                (section, content_data, created_by, updated_by)
                VALUES (%s, %s, 1, 1)
            """, (section, content_json))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
    
    # =========================================================================
    # THEME OPERATIONS
    # =========================================================================
    
    @classmethod
    def get_theme(cls):
        """
        Mengambil theme configuration dari database
        Theme disimpan sebagai section 'theme' di cms_content
        
        Returns:
            dict: Theme configuration atau {} jika tidak ada
        
        Example:
            {
                "navbarColor": "#0a0a0a",
                "navbarTextColor": "#ffffff",
                "homeBgColor": "#000000",
                ...
            }
        """
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Ambil theme dari cms_content
        cursor.execute("""
            SELECT content_data 
            FROM cms_content 
            WHERE section = 'theme' 
            AND is_active = 1 
            LIMIT 1
        """)
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        # Parse theme data
        if row and row.get("content_data"):
            try:
                # Jika sudah dict, return langsung
                if isinstance(row["content_data"], dict):
                    return row["content_data"]
                # Jika string, parse dulu
                return json.loads(row["content_data"])
            except (json.JSONDecodeError, TypeError):
                return {}
        
        return {}
    
    @classmethod
    def upsert_theme(cls, theme_obj):
        """
        Insert atau update theme configuration
        Theme disimpan sebagai section 'theme' di cms_content
        
        Args:
            theme_obj (dict): Theme configuration object
        
        Returns:
            bool: True jika berhasil
        
        Example:
            CMS.upsert_theme({
                "navbarColor": "#0a0a0a",
                "homeBgColor": "#000000"
            })
        """
        return cls.upsert_section('theme', theme_obj)
