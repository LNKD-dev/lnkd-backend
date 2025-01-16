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
    short_url = ShortLink.generate_short_url()
    new_link = ShortLink(original_url=original_url, short_url=short_url)
    db.session.add(new_link)
    db.session.commit()

    shorten_url = f"http://localhost:5000/{short_url}"
    return jsonify({'shorten_url': shorten_url}), 201

@bp.route('/<short_url>')
def redirect_to_original(short_url):
    link = ShortLink.query.filter_by(short_url=short_url).first()
    if not link:
        return jsonify({'error': 'Invalid short URL'}), 404
    
    link.click_count += 1
    db.session.commit()
    
    return redirect(link.original_url)

@bp.route('/stats/total_links', methods=['GET'])
def total_links():
    count = ShortLink.query.count()
    return jsonify({"total_links": count})


@bp.route("/stats/most_clicked", methods=["GET"])
def most_clicked():
    """
    Retrieve the most clicked short link from the database.
    This function queries the ShortLink table to find the link with the highest
    click count and returns its short url and click count in JSON format. If no
    links are found, it returns a JSON error message with a 404 status code.
    Returns:
        Response: A JSON response containing the short url and click count of the
                  most clicked link, or an error message if no links are found.
    """

    most_clicked_link = ShortLink.query.order_by(ShortLink.click_count.desc()).first()
    if most_clicked_link:
        return jsonify({
            "short_url": most_clicked_link.short_url,
            "click_count": most_clicked_link.click_count
        }), 200
    return jsonify({"error": "No links found"}), 404
