from app.database import db
import random
import string

class ShortLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(255), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)
    click_count = db.Column(db.Integer, default=0) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    @staticmethod
    def calculate_length():
        total_links = ShortLink.query.count()
        length = 3
        while total_links >= 62 ** length:
            length += 1
        return length
    

    @staticmethod
    def generate_short_url():
        length = ShortLink.calculate_length()
        short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        if not ShortLink.query.filter_by(short_url=short_url).first():
            return short_url
        
    
    