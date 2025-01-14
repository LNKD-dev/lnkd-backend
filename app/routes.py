from flask import Blueprint, request, jsonify, redirect
from app.database import db
from app.models import ShortLink

bp = Blueprint("routes", __name__)

@bp.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400
    short_code = ShortLink.generate_short_url()
    new_link = ShortLink(original_url=original_url, short_url=short_code)
    db.session.add(new_link)
    db.session.commit()

    shorten_url = f"http://localhost:5000/{short_code}"
    return jsonify({'shorten_url': shorten_url}), 201

@bp.route('/<short_url>')
def redirect_to_original(short_url):
    link = ShortLink.query.filter_by(short_url=short_url).first()
    if not link:
        return jsonify({'error': 'Invalid short URL'}), 404
    
    return redirect(link.original_url)

