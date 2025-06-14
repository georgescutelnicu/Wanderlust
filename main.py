from flask import Flask, render_template, request, redirect, flash, url_for
from model import db, Destination, User, DestinationToUser
from api import app as api_blueprint
from api import swaggerui_blueprint
from form import RegistrationForm, LoginForm, ResendVerificationForm
from helper_functions import (get_random_locations_for_continent, get_weather, get_pagination_and_page, get_map,
                              get_title, get_info, get_city_photos, send_verification_email)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_mail import Mail
import secrets
import random
import os


# Create Flask application, register blueprints, configure database and smtp
app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(swaggerui_blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['MAIL_SERVER'] = 'smtp.zoho.eu'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.json.sort_keys = False

mail = Mail(app)
db.init_app(app)

# Create and initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# List of valid columns for filtering and number of destinations to display per page
VALID_FILTER_COLUMNS = [col.name for col in Destination.__table__.columns]
PER_PAGE = 10


# Routes
@app.route("/")
def home():
    continents = ['Europe', 'North America', 'Asia', 'South America', 'Africa', 'Oceania']
    continent_locations = {continent: get_random_locations_for_continent(continent) for continent in continents}
    return render_template("index.html", continent_locations=continent_locations, current_user=current_user)


@app.route("/all")
def get_all_destinations():
    all_destinations = db.session.query(Destination).all()

    pagination, page = get_pagination_and_page(PER_PAGE, len(all_destinations))
    destinations_on_page = all_destinations[(page - 1) * PER_PAGE:page * PER_PAGE]

    return render_template("all.html", all_destinations=destinations_on_page, pagination=pagination,
                           current_user=current_user)


@app.route("/all/<continent>")
def get_all_destinations_by_continent(continent):
    allowed_continents = ['Europe', 'North America', 'Asia', 'South America', 'Africa', 'Oceania']

    if continent not in allowed_continents:
        return render_template("404.html")

    all_destinations = db.session.query(Destination).filter_by(continent=continent).all()

    pagination, page = get_pagination_and_page(PER_PAGE, len(all_destinations))
    destinations_on_page = all_destinations[(page - 1) * PER_PAGE:page * PER_PAGE]

    return render_template("all.html", all_destinations_continent=destinations_on_page, pagination=pagination,
                           continent=continent, current_user=current_user)


@app.route("/latest")
def get_latest_destinations():
    latest_destinations = db.session.query(Destination).order_by(Destination.id.desc()).limit(5).all()

    return render_template("latest.html", latest_destinations=latest_destinations, current_user=current_user)


@app.route("/most_visited")
def get_most_visited():
    top_cities = ["London", "Singapore", "Paris", "Dubai", "New York City", "Bangkok", "Istanbul", "Antalya", "Mumbai",
                  "Rome", "Tokyo", "Taipei", "Guangzhou", "Prague", "Seoul"]
    existing_cities = []

    for city in top_cities:
        destination = Destination.query.filter_by(city=city).first()
        if destination:
            existing_cities.append(destination)

    pagination, page = get_pagination_and_page(PER_PAGE, len(existing_cities))
    destinations_on_page = existing_cities[(page - 1) * PER_PAGE:page * PER_PAGE]

    return render_template("most_visited.html", most_visited_destinations=destinations_on_page,
                           pagination=pagination, current_user=current_user)


@app.route("/<city>")
def display_city(city):
    destination = Destination.query.filter_by(city=city).first()

    if destination:
        weather = get_weather(city)
        country_info = get_info(destination.country)
        photos = get_city_photos(destination.country, city)

        if current_user.is_authenticated:

            visited_destination = DestinationToUser.query.filter_by(
                destination_id=destination.id,
                user_id=current_user.id,
                status='visited'
            ).first()

            planned_to_visit_destination = DestinationToUser.query.filter_by(
                destination_id=destination.id,
                user_id=current_user.id,
                status='plan_to_visit'
            ).first()

            return render_template("city.html", destination=destination, weather=weather, country_info=country_info,
                                   current_user=current_user, is_visited=visited_destination is not None,
                                   is_planned_to_visit=planned_to_visit_destination is not None)

        return render_template("city.html", destination=destination, weather=weather, country_info=country_info,
                               photos=photos, current_user=current_user)

    return render_template("404.html")


@app.route("/<city>/<action>")
@login_required
def update_list(city, action):
    destination = Destination.query.filter_by(city=city).first()

    if not destination:
        return render_template("404.html")

    if action == "add_visited":
        current_user.add_visited_destination(destination)
    elif action == "add_plan_to_visit":
        current_user.add_plan_to_visit_destination(destination)
    elif action == "remove_visited":
        current_user.remove_visited_destination(destination)
    elif action == "remove_plan_to_visit":
        current_user.remove_plan_to_visit_destination(destination)

    db.session.commit()

    return redirect(url_for('display_city', city=city))


@app.route("/random")
def get_random_destination():
    all_destinations = db.session.query(Destination).all()
    random_destination = random.choice(all_destinations)
    return redirect(f'/{random_destination.city}')


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():

        username = User.query.filter_by(username=form.username.data).first()
        if username:
            flash('Username already in use. Please choose a different username.')
            return render_template('register.html', form=form)

        email = User.query.filter_by(email=form.email.data).first()
        if email:
            flash('Email already in use. Please use a different email address.')
            return render_template('register.html', form=form)

        hashed_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )

        token = secrets.token_hex(32)

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            verification_token=token
        )

        db.session.add(new_user)
        db.session.commit()

        send_verification_email(new_user.email, token, app.config['MAIL_USERNAME'], mail)
        flash("Please check your email to verify your account.", "success")

        return redirect(url_for('login'))

    return render_template('register.html', form=form, errors=form.errors, current_user=current_user)


@app.route("/verify/<token>")
def verify_account(token):
    user = User.query.filter_by(verification_token=token).first()

    if user:
        user.enabled = True
        user.verification_token = None
        db.session.commit()
        message = "Congratulations, your account has been verified!"
    else:
        message = "Sorry, we couldn't verify your account. It may already be verified or the token might be invalid."

    return render_template("verify.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not check_password_hash(user.password, form.password.data):
            flash("Invalid email or password.")
            return redirect(url_for("login"))
        if not user.enabled:
            flash("Your account is not verified.")
            return redirect(url_for("login"))

        login_user(user)
        return redirect(url_for("home"))

    return render_template("login.html", form=form, errors=form.errors, current_user=current_user)


@app.route("/resend-verification", methods=["GET", "POST"])
def resend_verification():
    form = ResendVerificationForm()

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if user and not user.enabled:
            token = secrets.token_hex(32)
            user.verification_token = token
            db.session.commit()
            send_verification_email(user.email, token, app.config['MAIL_USERNAME'], mail)

        flash("If the email is linked to an unverified account, a new verification email has been sent.")
        return redirect(url_for("resend_verification"))

    return render_template("resend_verification.html", form=form, errors=form.errors)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()

    if user is None or user != current_user:
        return redirect(url_for("home"))

    visited_destinations = DestinationToUser.query.filter_by(
        user_id=user.id,
        status='visited'
    ).join(Destination).all()

    planned_to_visit_destinations = DestinationToUser.query.filter_by(
        user_id=user.id,
        status='plan_to_visit'
    ).join(Destination).all()

    is_mobile = any(device in str(request.user_agent).lower()
                    for device in ['android', 'iphone', 'ipad', 'windows phone'])

    map_url = get_map(visited_destinations, planned_to_visit_destinations, is_mobile)
    title = get_title(visited_destinations, planned_to_visit_destinations)

    return render_template("profile.html", current_user=current_user, visited_destinations=visited_destinations,
                           planned_to_visit_destinations=planned_to_visit_destinations, map_url=map_url, title=title)


@app.route("/generate_api_key")
@login_required
def generate_api_key():
    current_user.generate_api_key()
    db.session.commit()
    return redirect(url_for("profile", username=current_user.username))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)
