import json

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request, jsonify
from flask import url_for
from werkzeug.utils import secure_filename
from datetime import datetime
from werkzeug.exceptions import abort

from tour.db import get_db

bp = Blueprint("index", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    tours = db.execute(
        "SELECT id, image, title, description, start_date, end_date, price, distance, travel_by"
        " FROM tours"
        " ORDER BY created DESC"
    ).fetchall()
    days_counts = []
    for tour in tours:
        start_date = datetime.strptime(tour['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(tour['end_date'], "%Y-%m-%d").date()
        # tour['days'] = (end_date - start_date).days  --->> Not working!
        days_counts.append((end_date - start_date).days)
    return render_template("index.html", tours=tours, days_counts=days_counts, tour_counts=len(days_counts))


@bp.route("/create_post", methods=['POST'])
def create_post():
    """Create a new post for the current user."""
    print(request.method)
    print(request.form)
    print(request.data)
    if request.method == "POST":
        title = request.form["title"]
        image = request.files.get('image')
        if image:
            imgname = secure_filename(image.filename)
            image.save('tour/static/uploads/' + imgname)
            image = imgname

        description = request.form.get('description')
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        price = request.form["price"]
        distance = request.form["distance"]
        travel_by = request.form["travel_by"]

        db = get_db()
        db.execute(
            "INSERT INTO tours (image, title, description, start_date, end_date, price, distance, travel_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (image, title, description, start_date, end_date, price, distance, travel_by),
        )
        db.commit()

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        tour = {'image': image, 'title': title, 'description': description, 'start_date': start_date,
                'end_date': end_date, 'price': price, 'distance': distance, 'travel_by': travel_by}
        tour['end_date'] = (end_date - start_date).days
        return tour
    return {'error': 'request must be POST'}
