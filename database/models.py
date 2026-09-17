from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    tier = db.Column(db.String(20), default="BASE")  # BASE, SILVER, GOLD
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship('Transaction', backref='member', lazy=True, cascade="all, delete-orphan")

    @property
    def live_balance(self):
        return sum(t.points for t in self.transactions)

    @property
    def lifetime_earned(self):
        return sum(t.points for t in self.transactions if t.points > 0)

    def evaluate_tier(self):
        earned = self.lifetime_earned
        if earned >= 1500:
            self.tier = "GOLD"
        elif earned >= 500:
            self.tier = "SILVER"
        else:
            self.tier = "BASE"

    def to_dict(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "name": self.name,
            "tier": self.tier,
            "balance": self.live_balance,
            "lifetime_earned": self.lifetime_earned,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    tx_type = db.Column(db.String(20), nullable=False)  # 'EARN' or 'REDEEM'
    points = db.Column(db.Integer, nullable=False)       
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)