from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
import hashlib
import random
import string
import os

db = SQLAlchemy()

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    course_type = db.Column(db.String(10), nullable=False)  # UG, PG, MBA
    department = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # CAT, ESE, SAT, Practical
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'course_type': self.course_type,
            'department': self.department,
            'semester': self.semester,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Subject {self.code}: {self.name}>'

class File(db.Model):
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    custom_filename = db.Column(db.String(255), nullable=False)
    course_type = db.Column(db.String(10), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=True)
    subject_name = db.Column(db.String(200), nullable=True)  # For backward compatibility
    file_type = db.Column(db.String(20), nullable=False, default='QP')  # QP or Syllabus
    size = db.Column(db.String(50), nullable=True)
    file_path = db.Column(db.String(500), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    subject = db.relationship('Subject', backref='files')
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'custom_filename': self.custom_filename,
            'course_type': self.course_type,
            'department': self.department,
            'semester': self.semester,
            'category': self.category,
            'subject_id': self.subject_id,
            'subject_name': self.subject_name,
            'subject_code': self.subject.code if self.subject else None,
            'file_type': self.file_type,
            'size': self.size,
            'file_path': self.file_path,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None
        }
    
    def __repr__(self):
        return f'<File {self.filename}>'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Display name from Google
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='guest')  # 'contributor' or 'guest'
    
    # OTP verification fields
    otp_hash = db.Column(db.String(64), nullable=True)  # SHA256 hash of OTP
    otp_expires_at = db.Column(db.DateTime, nullable=True)  # OTP expiry time
    otp_attempts = db.Column(db.Integer, nullable=False, default=0)  # Failed OTP attempts
    otp_lockout_until = db.Column(db.DateTime, nullable=True)  # Lockout expiry time
    ssn_email = db.Column(db.String(120), nullable=True, unique=True)  # Verified SSN email
    
    # Persistent login fields
    last_login_at = db.Column(db.DateTime, nullable=True)  # Last login timestamp
    last_verified_at = db.Column(db.DateTime, nullable=True)  # Last OTP verification
    reverify_interval_days = db.Column(db.Integer, nullable=False, default=90)  # Days before re-verification required
    auth_session_version = db.Column(db.Integer, nullable=False, default=1)  # For session invalidation
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # Default role is 'guest', contributors are verified via OTP
        if 'role' not in kwargs:
            self.role = 'guest'
    
    @property
    def is_contributor(self):
        return self.role == 'contributor'
    
    @property
    def is_guest(self):
        return self.role == 'guest'
    
    def generate_otp(self):
        """Generate a 6-digit OTP and store its hash"""
        otp = ''.join(random.choices(string.digits, k=6))
        self.otp_hash = hashlib.sha256(otp.encode()).hexdigest()
        self.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
        # Reset attempts when generating new OTP
        self.reset_otp_attempts()
        return otp
    
    def is_otp_locked_out(self):
        """Check if user is locked out from OTP attempts"""
        if not self.otp_lockout_until:
            return False
        return datetime.utcnow() < self.otp_lockout_until
    
    def increment_otp_attempts(self):
        """Increment failed OTP attempts and apply lockout if needed"""
        self.otp_attempts += 1
        if self.otp_attempts >= 5:
            # Lock out for 15 minutes after 5 failed attempts
            self.otp_lockout_until = datetime.utcnow() + timedelta(minutes=15)
    
    def reset_otp_attempts(self):
        """Reset OTP attempts after successful verification"""
        self.otp_attempts = 0
        self.otp_lockout_until = None
    
    def verify_otp(self, otp):
        """Verify OTP and check if it's not expired"""
        if not self.otp_hash or not self.otp_expires_at:
            return False
        
        # Check if user is locked out
        if self.is_otp_locked_out():
            return False
        
        # Check if OTP is expired
        if datetime.utcnow() > self.otp_expires_at:
            return False
        
        # Verify OTP hash
        otp_hash = hashlib.sha256(otp.encode()).hexdigest()
        if otp_hash == self.otp_hash:
            self.reset_otp_attempts()
            return True
        else:
            self.increment_otp_attempts()
            return False
    
    def clear_otp(self):
        """Clear OTP data after successful verification"""
        self.otp_hash = None
        self.otp_expires_at = None
        self.reset_otp_attempts()
    
    def is_verification_expired(self):
        """Check if user needs re-verification based on interval"""
        if not self.last_verified_at:
            return True  # Never verified, needs verification
        
        expiry_date = self.last_verified_at + timedelta(days=self.reverify_interval_days)
        return datetime.utcnow() > expiry_date
    
    def days_until_reverify(self):
        """Get days remaining until re-verification required"""
        if not self.last_verified_at:
            return 0  # Needs immediate verification
        
        expiry_date = self.last_verified_at + timedelta(days=self.reverify_interval_days)
        days_left = (expiry_date - datetime.utcnow()).days
        return max(0, days_left)
    
    def mark_verified(self, ssn_email):
        """Mark user as verified with SSN email and update timestamps"""
        self.role = 'contributor'
        self.ssn_email = ssn_email
        self.last_verified_at = datetime.utcnow()
        self.last_login_at = datetime.utcnow()
        self.clear_otp()
    
    def mark_login(self):
        """Update last login timestamp"""
        self.last_login_at = datetime.utcnow()
    
    def invalidate_sessions(self):
        """Increment session version to invalidate all existing sessions"""
        self.auth_session_version += 1
    
    def promote_to_contributor(self, ssn_email):
        """Promote user to contributor role after SSN email verification (legacy method)"""
        self.mark_verified(ssn_email)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'ssn_email': self.ssn_email,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'last_verified_at': self.last_verified_at.isoformat() if self.last_verified_at else None,
            'days_until_reverify': self.days_until_reverify(),
            'verification_expired': self.is_verification_expired(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.name} ({self.email})>'