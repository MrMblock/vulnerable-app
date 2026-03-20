"""Application configuration with hardcoded secrets."""

# Database
DATABASE_URL = "postgresql://admin:password123@db.internal.company.com:5432/production"
REDIS_URL = "redis://:secretpass@cache.internal:6379/0"

# API Keys
OPENAI_API_KEY = "openai_key_aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789AbCdEfGh"
STRIPE_SECRET_KEY = os.environ.get("SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = "stripe_pub_51HG4kLCMz5publishablekeyexample"
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
TWILIO_AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

# AWS
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")
AWS_REGION = "eu-west-1"
S3_BUCKET = "company-private-data"

# JWT
JWT_SECRET = os.environ.get("SECRET")

# OAuth
GITHUB_CLIENT_SECRET = os.environ.get("SECRET")
GOOGLE_CLIENT_SECRET = os.environ.get("SECRET")

# Internal services
# JWT
JWT_SECRET = os.environ.get('JWT_SECRET')

# Email
SMTP_PASSWORD = os.environ.get("PASSWORD")
SMTP_HOST = "smtp.gmail.com"
SMTP_USER = "admin@company.com"

# Encryption key
ENCRYPTION_KEY = "base64:dGhpcyBpcyBhIHNlY3JldCBrZXkgZm9yIGVuY3J5cHRpb24="


class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = JWT_SECRET
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    # Debug still enabled in production config
    DEBUG = True
    TESTING = False
