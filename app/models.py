from app import db
from flask_login import UserMixin
from datetime import datetime
import hashlib
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    urls = db.relationship('URL', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
    
    def get_id(self):
        return str(self.id)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(20), unique=True, nullable=False)
    custom_code = db.Column(db.String(20), unique=True, nullable=True)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    last_click_at = db.Column(db.DateTime, nullable=True)
    click_data = db.Column(db.Text, default='[]')
    
    def get_click_data(self):
        try:
            return json.loads(self.click_data)
        except:
            return []
    
    def add_click(self, ip=None, user_agent=None, country=None):
        self.clicks += 1
        self.last_click_at = datetime.utcnow()
        try:
            click_list = json.loads(self.click_data)
        except:
            click_list = []
        click_list.append({
            'timestamp': datetime.utcnow().isoformat(),
            'ip': ip,
            'user_agent': user_agent,
            'country': country
        })
        if len(click_list) > 1000:
            click_list = click_list[-1000:]
        self.click_data = json.dumps(click_list)
        db.session.commit()
    
    def get_clicks_by_day(self):
        data = self.get_click_data()
        days = {}
        for click in data:
            day = click['timestamp'][:10]
            days[day] = days.get(day, 0) + 1
        return days
    
    def get_clicks_by_country(self):
        data = self.get_click_data()
        countries = {}
        for click in data:
            country = click.get('country', 'Unknown')
            countries[country] = countries.get(country, 0) + 1
        return countries