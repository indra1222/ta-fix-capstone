"""
API Routes
Define all API routes
"""
from flask import Blueprint
from app.controllers import (
    NewsController,
    CMSController,
    QuestionController,
    AuthController,
    FurnitureController
)
from app.controllers.FAQController import FAQController
from app.controllers.LayoutController import LayoutController
from app.controllers.ContactController import ContactController
from app.controllers.HouseLayoutController import HouseLayoutController
from app.controllers.SocialMediaController import SocialMediaController
from app.controllers.HouseTypeController import HouseTypeController

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')

# ===== STATUS =====
@api.route('/status', methods=['GET'])
def status():
    from flask import jsonify
    return jsonify({
        "status": "success",
        "service": "FurniLayout API",
        "version": "2.0.0"
    })

# ===== NEWS ROUTES =====
@api.route('/news', methods=['GET'])
def get_news():
    return NewsController.index()

@api.route('/news/<int:news_id>', methods=['GET'])
def get_news_detail(news_id):
    return NewsController.show(news_id)

@api.route('/news', methods=['POST'])
def create_news():
    return NewsController.store()

@api.route('/news/<int:news_id>', methods=['PUT'])
def update_news(news_id):
    return NewsController.update(news_id)

@api.route('/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    return NewsController.destroy(news_id)

# ===== FAQ ROUTES =====
@api.route('/faqs', methods=['GET'])
def get_faqs():
    """Get all FAQs (for admin)"""
    return FAQController.index()

@api.route('/faqs/active', methods=['GET'])
def get_active_faqs():
    """Get active FAQs (for public)"""
    return FAQController.get_active()

@api.route('/faqs/category/<category>', methods=['GET'])
def get_faqs_by_category(category):
    """Get FAQs by category"""
    return FAQController.get_by_category(category)

@api.route('/faqs/<int:faq_id>', methods=['GET'])
def get_faq_detail(faq_id):
    return FAQController.show(faq_id)

@api.route('/faqs', methods=['POST'])
def create_faq():
    return FAQController.store()

@api.route('/faqs/<int:faq_id>', methods=['PUT'])
def update_faq(faq_id):
    return FAQController.update(faq_id)

@api.route('/faqs/<int:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    return FAQController.destroy(faq_id)

# ===== FURNITURE ROUTES =====
@api.route('/furniture', methods=['GET'])
def get_furniture():
    return FurnitureController.index()

@api.route('/furniture/<int:furniture_id>', methods=['GET'])
def get_furniture_detail(furniture_id):
    return FurnitureController.show(furniture_id)

# ===== CMS ROUTES =====
@api.route('/cms/content', methods=['GET'])
def get_cms_content():
    return CMSController.get_content()

@api.route('/cms/content', methods=['PUT'])
def update_cms_content():
    return CMSController.update_content()

@api.route('/cms/theme', methods=['GET'])
def get_theme():
    return CMSController.get_theme()

@api.route('/cms/theme', methods=['PUT'])
def update_theme():
    return CMSController.update_theme()

# ===== QUESTION ROUTES =====
@api.route('/questions', methods=['POST'])
def submit_question():
    return QuestionController.store()

@api.route('/questions/answered', methods=['GET'])
def get_answered_questions():
    return QuestionController.get_answered()

@api.route('/questions/all', methods=['GET'])
def get_all_questions():
    return QuestionController.index()

@api.route('/questions/<int:question_id>/answer', methods=['PUT'])
def answer_question(question_id):
    return QuestionController.answer(question_id)

@api.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    return QuestionController.destroy(question_id)

# ===== AUTH ROUTES =====
@api.route('/cms/login', methods=['POST'])
def admin_login():
    return AuthController.login()

# ===== LAYOUT ROUTES =====
@api.route('/layout/predict', methods=['POST'])
def predict_layout():
    return LayoutController.predict_batch()

@api.route('/layout/recommendations', methods=['POST'])
def get_recommendations():
    return LayoutController.get_floor_recommendations()

@api.route('/layout/reset', methods=['POST'])
def reset_layout():
    return LayoutController.reset_layout()

@api.route('/layout/auto-place', methods=['POST'])
def auto_place_furniture():
    return LayoutController.auto_place_furniture()

@api.route('/layout/model-info', methods=['GET'])
def get_model_info():
    """Get AI model information and metrics"""
    from app.services.LayoutService import LayoutService
    from flask import jsonify
    import joblib
    from config import Config
    
    try:
        # Try to load model metadata
        metadata = joblib.load(Config.METADATA_PATH)
        
        return jsonify({
            "status": "success",
            "model_loaded": True,
            "version": metadata.get('version'),
            "date": metadata.get('date'),
            "furniture_count": metadata.get('furniture_count'),
            "training_samples": metadata.get('samples'),
            "regression": metadata.get('regression'),
            "classification": metadata.get('classification')
        })
    except:
        return jsonify({
            "status": "warning",
            "model_loaded": False,
            "message": "AI model not loaded. Using grid search fallback.",
            "instructions": "Upload model_auto_layout (8).pkl to app/services/ directory"
        })

# ===== UPLOAD ROUTES =====
@api.route('/news/upload-image', methods=['POST'])
def upload_news_image():
    return NewsController.upload_image()

@api.route('/news/images/<filename>', methods=['GET'])
def serve_image(filename):
    return LayoutController.serve_news_image(filename)

# ===== CONTACT ROUTES =====
@api.route('/contact', methods=['POST'])
def submit_contact():
    """Submit contact form"""
    return ContactController.store()

@api.route('/contact/messages', methods=['GET'])
def get_contact_messages():
    """Get all contact messages (admin)"""
    return ContactController.index()

@api.route('/contact/messages/unread', methods=['GET'])
def get_unread_messages():
    """Get unread messages (admin)"""
    return ContactController.get_unread()

@api.route('/contact/messages/<int:message_id>/read', methods=['PUT'])
def mark_message_read(message_id):
    """Mark message as read"""
    return ContactController.mark_read(message_id)

@api.route('/contact/messages/<int:message_id>', methods=['DELETE'])
def delete_contact_message(message_id):
    """Delete contact message"""
    return ContactController.destroy(message_id)

# ===== HOUSE LAYOUT ROUTES =====
@api.route('/layouts', methods=['GET'])
def get_all_layouts():
    """Get all saved layouts (admin)"""
    return HouseLayoutController.index()

@api.route('/layouts/public', methods=['GET'])
def get_public_layouts():
    """Get public layouts"""
    return HouseLayoutController.get_public()

@api.route('/layouts/user/<int:user_id>', methods=['GET'])
def get_user_layouts(user_id):
    """Get layouts by user ID"""
    return HouseLayoutController.get_by_user(user_id)

@api.route('/layouts/<int:layout_id>', methods=['GET'])
def get_layout_detail(layout_id):
    """Get single layout detail"""
    return HouseLayoutController.show(layout_id)

@api.route('/layouts', methods=['POST'])
def save_layout():
    """Save new layout"""
    return HouseLayoutController.store()

@api.route('/layouts/<int:layout_id>', methods=['PUT'])
def update_saved_layout(layout_id):
    """Update saved layout"""
    return HouseLayoutController.update(layout_id)

@api.route('/layouts/<int:layout_id>/toggle-public', methods=['PUT'])
def toggle_layout_public(layout_id):
    """Toggle layout public status"""
    return HouseLayoutController.toggle_public(layout_id)

@api.route('/layouts/<int:layout_id>', methods=['DELETE'])
def delete_saved_layout(layout_id):
    """Delete saved layout"""
    return HouseLayoutController.destroy(layout_id)

# ===== SOCIAL MEDIA ROUTES =====
@api.route('/social-media', methods=['GET'])
def get_social_media():
    """Get all social media links (admin)"""
    return SocialMediaController.index()

@api.route('/social-media/active', methods=['GET'])
def get_active_social_media():
    """Get active social media links (public)"""
    return SocialMediaController.get_active()

@api.route('/social-media', methods=['POST'])
def create_social_media():
    """Create social media link"""
    return SocialMediaController.store()

@api.route('/social-media/<int:social_id>', methods=['PUT'])
def update_social_media(social_id):
    """Update social media link"""
    return SocialMediaController.update(social_id)

@api.route('/social-media/<int:social_id>', methods=['DELETE'])
def delete_social_media(social_id):
    """Delete social media link"""
    return SocialMediaController.destroy(social_id)


# ===== HOUSE TYPES ROUTES =====
@api.route('/house-types', methods=['GET'])
def get_house_types():
    """Get all house types"""
    return HouseTypeController.get_all_house_types()

@api.route('/house-types/<int:house_id>', methods=['GET'])
def get_house_type_detail(house_id):
    """Get house type by ID"""
    return HouseTypeController.get_house_type_by_id(house_id)

@api.route('/house-types/category/<category>', methods=['GET'])
def get_house_types_by_category(category):
    """Get house types by category"""
    return HouseTypeController.get_house_types_by_category(category)

@api.route('/house-types', methods=['POST'])
def create_house_type():
    """Create new house type"""
    return HouseTypeController.create_house_type()

@api.route('/house-types/<int:house_id>', methods=['PUT'])
def update_house_type(house_id):
    """Update house type"""
    return HouseTypeController.update_house_type(house_id)

@api.route('/house-types/<int:house_id>', methods=['DELETE'])
def delete_house_type(house_id):
    """Delete house type"""
    return HouseTypeController.delete_house_type(house_id)

@api.route('/house-types/<int:house_id>/toggle-active', methods=['PUT'])
def toggle_house_type_active(house_id):
    """Toggle house type active status"""
    return HouseTypeController.toggle_house_type_active(house_id)

@api.route('/house-types/<int:house_id>/reorder', methods=['PUT'])
def reorder_house_type(house_id):
    """Update house type display order"""
    return HouseTypeController.reorder_house_type(house_id)

