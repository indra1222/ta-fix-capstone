"""
HouseType Model
Handles database operations for house types catalog
"""
from app.models.BaseModel import BaseModel
import json

class HouseType(BaseModel):
    """Model for managing house type catalog"""

    table_name = 'house_types'

    @classmethod
    def get_all(cls, include_inactive=False):
        """Get all house types
        
        Args:
            include_inactive (bool): Include inactive house types
            
        Returns:
            list: List of house types ordered by display_order
        """
        try:
            query = f"SELECT * FROM {cls.table_name}"
            if not include_inactive:
                query += " WHERE is_active = 1"
            query += " ORDER BY display_order ASC, id ASC"
            
            results = cls.fetch_all(query)
            
            # Parse JSON fields
            for house in results:
                if house.get('features') and isinstance(house['features'], str):
                    house['features'] = json.loads(house['features'])
                if house.get('specifications') and isinstance(house['specifications'], str):
                    house['specifications'] = json.loads(house['specifications'])
            
            return results
        except Exception as e:
            print(f"Error getting house types: {e}")
            return []

    @classmethod
    def get_by_id(cls, house_id):
        """Get house type by ID
        
        Args:
            house_id (int): House type ID
            
        Returns:
            dict: House type data or None
        """
        try:
            query = f"SELECT * FROM {cls.table_name} WHERE id = %s"
            house = cls.fetch_one(query, (house_id,))
            
            if house:
                # Parse JSON fields
                if house.get('features') and isinstance(house['features'], str):
                    house['features'] = json.loads(house['features'])
                if house.get('specifications') and isinstance(house['specifications'], str):
                    house['specifications'] = json.loads(house['specifications'])
            
            return house
        except Exception as e:
            print(f"Error getting house type by ID: {e}")
            return None

    @classmethod
    def get_by_category(cls, category):
        """Get house types by category
        
        Args:
            category (str): Category name
            
        Returns:
            list: List of house types in the category
        """
        try:
            query = f"""
                SELECT * FROM {cls.table_name} 
                WHERE type_category = %s AND is_active = 1
                ORDER BY display_order ASC
            """
            results = cls.fetch_all(query, (category,))
            
            # Parse JSON fields
            for house in results:
                if house.get('features') and isinstance(house['features'], str):
                    house['features'] = json.loads(house['features'])
                if house.get('specifications') and isinstance(house['specifications'], str):
                    house['specifications'] = json.loads(house['specifications'])
            
            return results
        except Exception as e:
            print(f"Error getting house types by category: {e}")
            return []

    @classmethod
    def create(cls, data):
        """Create new house type
        
        Args:
            data (dict): House type data
            
        Returns:
            int: New house type ID or None on error
        """
        try:
            # Convert lists/dicts to JSON strings
            if 'features' in data and isinstance(data['features'], (list, dict)):
                data['features'] = json.dumps(data['features'])
            if 'specifications' in data and isinstance(data['specifications'], (list, dict)):
                data['specifications'] = json.dumps(data['specifications'])
            
            fields = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {cls.table_name} ({fields}) VALUES ({placeholders})"
            
            result = cls.execute(query, tuple(data.values()))
            return result  # Returns lastrowid
        except Exception as e:
            print(f"Error creating house type: {e}")
            import traceback
            traceback.print_exc()
            return None

    @classmethod
    def update(cls, house_id, data):
        """Update house type
        
        Args:
            house_id (int): House type ID
            data (dict): Updated data
            
        Returns:
            bool: Success status
        """
        try:
            # Convert lists/dicts to JSON strings
            if 'features' in data and isinstance(data['features'], (list, dict)):
                data['features'] = json.dumps(data['features'])
            if 'specifications' in data and isinstance(data['specifications'], (list, dict)):
                data['specifications'] = json.dumps(data['specifications'])
            
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            query = f"UPDATE {cls.table_name} SET {set_clause} WHERE id = %s"
            
            values = tuple(data.values()) + (house_id,)
            cls.execute(query, values)
            return True
        except Exception as e:
            print(f"Error updating house type: {e}")
            return False

    @classmethod
    def delete(cls, house_id):
        """Delete house type (soft delete by setting is_active = 0)
        
        Args:
            house_id (int): House type ID
            
        Returns:
            bool: Success status
        """
        try:
            query = f"UPDATE {cls.table_name} SET is_active = 0 WHERE id = %s"
            cls.execute(query, (house_id,))
            return True
        except Exception as e:
            print(f"Error deleting house type: {e}")
            return False

    @classmethod
    def toggle_active(cls, house_id):
        """Toggle house type active status
        
        Args:
            house_id (int): House type ID
            
        Returns:
            bool: Success status
        """
        try:
            query = f"""
                UPDATE {cls.table_name} 
                SET is_active = NOT is_active 
                WHERE id = %s
            """
            cls.execute(query, (house_id,))
            return True
        except Exception as e:
            print(f"Error toggling house type status: {e}")
            return False

    @classmethod
    def reorder(cls, house_id, new_order):
        """Update display order
        
        Args:
            house_id (int): House type ID
            new_order (int): New display order
            
        Returns:
            bool: Success status
        """
        try:
            query = f"UPDATE {cls.table_name} SET display_order = %s WHERE id = %s"
            cls.execute(query, (new_order, house_id))
            return True
        except Exception as e:
            print(f"Error reordering house type: {e}")
            return False
