import uuid
from datetime import datetime, timezone
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.common.error_handling import ConflictException
from app.db import db, BaseModelMixin


class Users(db.Model, BaseModelMixin):
    __tablename__ = "users"

    userId = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    # Relaciones
    tokens = db.relationship("BlacklistToken", back_populates="users")

    def __init__(self, name, password, admin):
        self.public_id = str(uuid.uuid4())
        if self.is_unique_name(name):
            self.name = name
        self.password = self.generate_password_hash(password)
        self.admin = admin

    def __repr__(self):
        return f'Users({self.name})'

    def __str__(self):
        return f'{self.name}'

    def is_admin(self):
        return self.admin

    def is_unique_name(self, name):
        if self.simple_filter(name=name):
            raise ConflictException(f"El name {name} no esta disponible.")
        return True

    def update_user(self, name=None, password=None):
        if name and self.is_unique_name(name):
            self.name = name

        if password:
            hashed_password = generate_password_hash(password, method='sha256')
            self.password = hashed_password

    @staticmethod
    def generate_password_hash(password):
        return generate_password_hash(password, method='sha256')

    def check_password_hash(self, auth_password):
        return check_password_hash(self.password, auth_password)

    def create_access_token(self):
        return create_access_token(identity=self.public_id)

    def create_refresh_token(self):
        return create_refresh_token(identity=self.public_id)


class BlacklistToken(db.Model, BaseModelMixin):
    __tablename__ = 'blacklist_tokens'

    token_id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), db.ForeignKey('users.public_id'))
    expires = db.Column(db.DateTime, nullable=False)

    # Relaciones
    users = db.relationship("Users", back_populates="tokens")

    def __init__(self, jti, token_type, user_identity, exp):
        self.jti = jti
        self.token_type = token_type
        self.user_identity = user_identity
        self.expires = datetime.fromtimestamp(exp, tz=timezone.utc)

    def __repr__(self):
        return f'BlacklistToken({self.token_id})'

    def __str__(self):
        return f'{self.token_id}'

    @staticmethod
    def check_blacklist(jti):
        token = BlacklistToken.simple_filter(jti=jti)
        return True if token else False
