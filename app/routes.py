from flask import render_template, request, redirect, url_for, flash, make_response, jsonify
from app import app, db
from app.models import User, URL
from app.utils import generate_short_code, get_country_from_ip
from app.translations import get_text
from app.forms import RegistrationForm, LoginForm, URLForm, ContactForm
from app.decorators import login_required_custom
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
import base64
import json
import os

def get_language():
    lang = request.cookies.get('language')
    if lang in ['fa', 'en']:
        return lang
    accept_lang = request.accept_languages.best_match(['fa', 'en'])
    return accept_lang if accept_lang else 'fa'

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

@app.route('/', methods=['GET', 'POST'])
def index():
    lang = get_language()
    t = lambda key: get_text(lang, key)
    form = URLForm()
    
    if form.validate_on_submit():
        original_url = form.original_url.data
        custom_code = form.custom_code.data
        expires_days = form.expires_days.data
        
        if current_user.is_authenticated:
            existing = URL.query.filter_by(original_url=original_url, user_id=current_user.id).first()
        else:
            existing = URL.query.filter_by(original_url=original_url).first()
        
        if existing:
            short_url = request.host_url + existing.short_code
            recent_links = URL.query.order_by(URL.id.desc()).limit(5).all()
            return render_template('index.html', t=t, lang=lang, form=form, 
                                 short_url=short_url, short_code=existing.short_code,
                                 recent_links=recent_links)
        
        if custom_code:
            if URL.query.filter_by(short_code=custom_code).first():
                flash('این کد دلخواه قبلاً استفاده شده است.', 'error')
                recent_links = URL.query.order_by(URL.id.desc()).limit(5).all()
                return render_template('index.html', t=t, lang=lang, form=form, recent_links=recent_links)
            short_code = custom_code
        else:
            short_code = generate_short_code(6)
            while URL.query.filter_by(short_code=short_code).first():
                short_code = generate_short_code(6)
        
        expires_at = None
        if expires_days > 0:
            expires_at = datetime.utcnow() + timedelta(days=expires_days)
        
        new_url = URL(
            original_url=original_url,
            short_code=short_code,
            custom_code=custom_code if custom_code else None,
            expires_at=expires_at,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(new_url)
        db.session.commit()
        
        short_url = request.host_url + short_code
        recent_links = URL.query.order_by(URL.id.desc()).limit(5).all()
        return render_template('index.html', t=t, lang=lang, form=form,
                             short_url=short_url, short_code=short_code,
                             recent_links=recent_links)
    
    recent_links = URL.query.order_by(URL.id.desc()).limit(5).all()
    return render_template('index.html', t=t, lang=lang, form=form, recent_links=recent_links)

@app.route('/<short_code>')
def go_to_link(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first_or_404()
    
    if url_entry.expires_at and url_entry.expires_at < datetime.utcnow():
        flash('این لینک منقضی شده است.', 'error')
        return redirect(url_for('index'))
    
    ip = get_client_ip()
    user_agent = request.headers.get('User-Agent')
    country = get_country_from_ip(ip)
    url_entry.add_click(ip=ip, user_agent=user_agent, country=country)
    
    return redirect(url_entry.original_url)

@app.route('/stats/<short_code>')
def show_stats(short_code):
    lang = get_language()
    t = lambda key: get_text(lang, key)
    url_entry = URL.query.filter_by(short_code=short_code).first_or_404()
    
    if current_user.is_authenticated and url_entry.user_id and url_entry.user_id != current_user.id:
        flash('شما دسترسی به این لینک ندارید.', 'error')
        return redirect(url_for('index'))
    
    click_data = url_entry.get_click_data()
    clicks_by_day = url_entry.get_clicks_by_day()
    clicks_by_country = url_entry.get_clicks_by_country()
    
    # QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(request.host_url + short_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return render_template('stats.html', t=t, lang=lang, url=url_entry,
                         click_data=click_data, clicks_by_day=clicks_by_day,
                         clicks_by_country=clicks_by_country, qr_base64=qr_base64)

@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = get_language()
    t = lambda key: get_text(lang, key)
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('ایمیل یا رمز عبور اشتباه است.', 'error')
    
    return render_template('login.html', t=t, lang=lang, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    lang = get_language()
    t = lambda key: get_text(lang, key)
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('ثبت‌نام با موفقیت انجام شد! حالا وارد شوید.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', t=t, lang=lang, form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('شما خارج شدید.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    lang = get_language()
    t = lambda key: get_text(lang, key)
    
    user_urls = URL.query.filter_by(user_id=current_user.id).order_by(URL.id.desc()).all()
    total_clicks = sum(url.clicks for url in user_urls)
    total_urls = len(user_urls)
    
    return render_template('dashboard.html', t=t, lang=lang, user_urls=user_urls,
                         total_clicks=total_clicks, total_urls=total_urls)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    lang = get_language()
    t = lambda key: get_text(lang, key)
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
        if username:
            current_user.username = username
        if email:
            current_user.email = email
        
        db.session.commit()
        flash('پروفایل با موفقیت به‌روزرسانی شد!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', t=t, lang=lang, user=current_user)

@app.route('/about')
def about():
    lang = get_language()
    t = lambda key: get_text(lang, key)
    return render_template('about.html', t=t, lang=lang)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    lang = get_language()
    t = lambda key: get_text(lang, key)
    form = ContactForm()
    
    if form.validate_on_submit():
        flash('پیام شما با موفقیت ارسال شد!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', t=t, lang=lang, form=form)

@app.route('/terms')
def terms():
    lang = get_language()
    t = lambda key: get_text(lang, key)
    return render_template('terms.html', t=t, lang=lang)

@app.route('/privacy')
def privacy():
    lang = get_language()
    t = lambda key: get_text(lang, key)
    return render_template('privacy.html', t=t, lang=lang)

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang not in ['fa', 'en']:
        lang = 'fa'
    response = make_response(redirect(request.referrer or url_for('index')))
    response.set_cookie('language', lang, max_age=60*60*24*365)
    return response

@app.errorhandler(404)
def page_not_found(e):
    lang = get_language()
    t = lambda key: get_text(lang, key)
    return render_template('404.html', t=t, lang=lang), 404

