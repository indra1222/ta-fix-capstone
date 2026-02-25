"""
HouseTypeController
Handles API endpoints for house types management
"""
from flask import jsonify, request
from app.models.HouseType import HouseType

class HouseTypeController:
    """Controller for house types CRUD operations"""

    @staticmethod
    def get_all_house_types():
        """Get all house types
        
        Query params:
            include_inactive (bool): Include inactive items
            
        Returns:
            JSON response with house types list
        """
        try:
            include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
            house_types = HouseType.get_all(include_inactive=include_inactive)
            
            return jsonify({
                'status': 'success',
                'data': house_types,
                'count': len(house_types)
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Failed to retrieve house types: {str(e)}'
            }), 500

    @staticmethod
    def get_house_type_by_id(house_id):
        """Get house type by ID
        
        Args:
            house_id (int): House type ID
            
        Returns:
            JSON response with house type data
        """
        try:
            house_type = HouseType.get_by_id(house_id)
            
            if house_type:
                return jsonify({
                    'status': 'success',
                    'data': house_type
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'House type not found'
                }), 404
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Failed to retrieve house type: {str(e)}'
            }), 500

    @staticmethod
    def get_house_types_by_category(category):
        """Get house types by category
        
        Args:
            category (str): Category name
            
        Returns:
            JSON response with house types list
        """
        try:
            house_types = HouseType.get_by_category(category)
            
            return jsonify({
                'status': 'success',
                'data': house_types,
                'count': len(house_types)
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Failed to retrieve house types: {str(e)}'
            }), 500

    @staticmethod
    def create_house_type():
        """Create new house type
        
        Expected JSON body:
            - name (required)
            - description
            - price_start
            - type_category
            - land_size
            - building_size
            - bedrooms
            - bathrooms
            - floors
            - carport
            - image_url
            - features (array)
            - specifications (object)
            - is_active
            - display_order
            
        Returns:
            JSON response with created house type ID
        """
        try:
            data = request.get_json()
            
            if not data or not data.get('name'):
                return jsonify({
                    'status': 'error',
                    'message': 'Name is required'
                }), 400
            
            # Set defaults
            data.setdefault('type_category', 'Modern')
            data.setdefault('is_active', 1)
            data.setdefault('display_order', 0)
            data.setdefault('bedrooms', 0)
            data.setdefault('bathrooms', 0)
            data.setdefault('floors', 1)
            data.setdefault('carport', 0)
            
            house_id = HouseType.create(data)
            
            if house_id:
                return jsonify({
                    'status': 'success',
                    'message': 'House type created successfully',
                    'id': house_id
                }), 201
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to create house type'
                }), 500
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({
                'status': 'error',
                'message': f'Failed to create house type: {str(e)}'
            }), 500

    @staticmethod
    def update_house_type(house_id):
        """Update house type
        
        Args:
            house_id (int): House type ID
            
        Expected JSON body:
            Any fields to update (same as create)
            
        Returns:
            JSON response with success status
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'status': 'error',
                    'message': 'No data provided'
                }), 400
            
            # Check if house type exists
            existing = HouseType.get_by_id(house_id)
            if not existing:
                return jsonify({
                    'status': 'error',
                    'message': 'House type not found'
                }), 404
            
            success = HouseType.update(house_id, data)
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'House type updated successfully'
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to update house type'
                }), 500
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Failed to update house type: {str(e)}'
            }), 500

    @staticmethod
    def delete_house_type(house_id):
        """Delete house type (soft delete)
        
        Args:
            house_id (int): House type ID
            
        Returns:
            JSON response with success status
        """
        try:
            # Check if house type exists
            existing = HouseType.get_by_id(house_id)
            if not existing:
                return jsonify({
                    'status': 'error',
                    'message': 'House type not found'
                }), 404
            
            success = HouseType.delete(house_id)
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'House type deleted successfully'
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to delete house type'
                }), 500
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Failed to delete house type: {str(e)}'
            }), 500

    @staticmethod
    def toggle_house_type_active(house_id):
        """Toggle house type active status
        
        Args:
            house_id (int): House type ID
            
        Returns:
            JSON response with success status
        """
        try:
            # Check if house type exists
            existing = HouseType.get_by_id(house_id)
            if not existing:
                return jsonify({
                    'status': 'error',
                    'message': 'House type not found'
                }), 404
            
            success = HouseType.toggle_active(house_id)
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'House type status toggled successfully'
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to toggle house type status'
                }), 500
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Failed to toggle house type status: {str(e)}'
            }), 500

    @staticmethod
    def reorder_house_type(house_id):
        """Update house type display order
        
        Args:
            house_id (int): House type ID
            
        Expected JSON body:
            - display_order (required)
            
        Returns:
            JSON response with success status
        """
        try:
            data = request.get_json()
            
            if not data or 'display_order' not in data:
                return jsonify({
                    'status': 'error',
                    'message': 'display_order is required'
                }), 400
            
            # Check if house type exists
            existing = HouseType.get_by_id(house_id)
            if not existing:
                return jsonify({
                    'status': 'error',
                    'message': 'House type not found'
                }), 404
            
            success = HouseType.reorder(house_id, data['display_order'])
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'House type order updated successfully'
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to update house type order'
                }), 500
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Failed to update house type order: {str(e)}'
            }), 500
