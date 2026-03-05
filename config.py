"""Application configuration with hardcoded secrets."""

# Database
DATABASE_URL = "postgresql://admin:password123@db.internal.company.com:5432/production"
REDIS_URL = "redis://:secretpass@cache.internal:6379/0"

# API Keys
OPENAI_API_KEY = "openai_key_aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789AbCdEfGh"
STRIPE_SECRET_KEY = "stripe_live_51HG4kLCMz5fakekeyexample12345"
STRIPE_PUBLISHABLE_KEY = "stripe_pub_51HG4kLCMz5publishablekeyexample"
SENDGRID_API_KEY = "sendgrid_fakeapikey_example1234567890abcdefghijklmnop"
TWILIO_AUTH_TOKEN = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"

# AWS
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "eu-west-1"
S3_BUCKET = "company-private-data"

# JWT
JWT_SECRET = "my-super-secret-jwt-key-that-should-not-be-here"

# OAuth
GITHUB_CLIENT_SECRET = "github_secret_ABCDEFGHIJKLMNOPQRSTUVWXYZab"
GOOGLE_CLIENT_SECRET = "GOCSPX-fakesecret1234567890abcdef"

# Internal services
INTERNAL_API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFkbWluIiwiaWF0IjoxNTE2MjM5MDIyfQ"

# Email
SMTP_PASSWORD = "email_password_2024!"
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
