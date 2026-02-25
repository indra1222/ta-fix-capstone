"""
Models Package
Export all models
"""
from app.models.News import News
from app.models.CMS import CMS
from app.models.Question import Question
from app.models.HouseType import HouseType

__all__ = ['News', 'CMS', 'Question', 'HouseType']
