from datetime import datetime
from flask import current_app
from sqlalchemy import Text, Float, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship, backref
from extensions import db
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime, timedelta
import bcrypt

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    token_version = db.Column(db.Integer, default=1, nullable=False)
    # ==================== PROFILE FIELDS ====================
    verified = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    subscription_plan = db.Column(db.String(50), default='free')
    trial_plan = db.Column(db.String(32), nullable=True)
    trial_ends_at = db.Column(db.DateTime, nullable=True)
    
    country = db.Column(db.String(64), default='default')
    currency = db.Column(db.String(16), default='USD')
    preferred_language = db.Column(db.String(8), default='en')
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=True)
    industry = db.Column(db.String(64), default='Healthcare')
    company_name = db.Column(db.String(256))
    company_logo = db.Column(db.String(512))
    timezone = db.Column(db.String(64), default='UTC')
    user_type = db.Column(db.String(20), default='user')
    role = db.Column(db.String(64), default='user')
    is_system_team = db.Column(db.Boolean, default=False)
    
    # ==================== DOCUMENT VERIFICATION ====================
    documents_uploaded = db.Column(db.Boolean, default=False)
    documents_verified = db.Column(db.Boolean, default=False)
    documents_uploaded_at = db.Column(db.DateTime, nullable=True)
    
    # ==================== ACTIVITY TRACKING ====================
    login_count = db.Column(db.Integer, default=0)
    activity_count = db.Column(db.Integer, default=0)
    total_session_duration = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, nullable=True)
    performance_score = db.Column(db.Integer, default=0)
    performance_grade = db.Column(db.String(5), default='F')
    login_frequency = db.Column(db.Float, default=0)
    activity_rate = db.Column(db.Float, default=0)
    avg_session_duration = db.Column(db.Float, default=0)
    
    # ==================== ADMIN FIELDS ====================
    admin_tier = db.Column(db.String(20), default='company')
    is_platform_owner = db.Column(db.Boolean, default=False)
    platform_permissions = db.Column(db.JSON, default=list)
    
    # ✅ COMPANY ID with ForeignKey
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    
    # ✅ FIX: Add foreign_keys to the relationship
    company = db.relationship('Company', foreign_keys=[company_id], back_populates='users')
    
    admin_role = db.Column(db.String(64), nullable=True)
    admin_level = db.Column(db.String(20), default='standard')
    
    approval_status = db.Column(db.String(20), default='pending')
    approved_at = db.Column(db.DateTime, nullable=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    rejected_at = db.Column(db.DateTime, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    
    # ==================== SUBSCRIPTION FIELDS ====================
    subscription_status = db.Column(db.String(20), default='inactive')
    billing_cycle = db.Column(db.String(20), default='1_month')
    subscription_starts_at = db.Column(db.DateTime, nullable=True)
    subscription_ends_at = db.Column(db.DateTime, nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    payment_gateway = db.Column(db.String(50), nullable=True)
    payment_id = db.Column(db.String(100), nullable=True)
    last_payment_date = db.Column(db.DateTime, nullable=True)
    next_payment_date = db.Column(db.DateTime, nullable=True)
    
    monthly_uploads_used = db.Column(db.Integer, default=0)
    monthly_api_calls_used = db.Column(db.Integer, default=0)
    monthly_ai_requests_used = db.Column(db.Integer, default=0)
    monthly_video_minutes_used = db.Column(db.Integer, default=0)
    usage_reset_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    is_enterprise = db.Column(db.Boolean, default=False)
    enterprise_features = db.Column(db.JSON, nullable=True)
    custom_requirements = db.Column(db.Text, nullable=True)
    
    employee_id = db.Column(db.String(50), unique=True, nullable=True, index=True) 
    employee_count = db.Column(db.Integer, default=0)
    department = db.Column(db.String(128), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    
    # ==================== ACCOUNT STATUS ====================
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ==================== AVATAR ====================
    avatar_url = db.Column(db.String(500), nullable=True)

    # ==================== PDF GENERATION ====================
    daily_pdf_generations = db.Column(db.Integer, default=0)
    monthly_pdf_generations = db.Column(db.Integer, default=0)
    total_pdf_documents = db.Column(db.Integer, default=0)
    last_pdf_generation_at = db.Column(db.DateTime, nullable=True)
    pdf_templates_created = db.Column(db.Integer, default=0)
    max_pdf_templates = db.Column(db.Integer, default=10)

    # ==================== RELATIONSHIPS ====================
    # ✅ All relationships with foreign_keys specified
    assigned_tasks = db.relationship('Task', back_populates='assigned_to', foreign_keys='Task.assigned_to_id')
    training_records = db.relationship('TrainingRecord', back_populates='user', foreign_keys='TrainingRecord.user_id')
    camera_feeds = db.relationship('CameraFeed', backref='user', lazy=True, cascade='all, delete-orphan')
    ai_requests = db.relationship('AIRequest', backref='user', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='user', lazy=True, cascade='all, delete-orphan')
    subscriptions = db.relationship('Subscription', backref='user', lazy=True, cascade='all, delete-orphan')
    risk_assessments = db.relationship('RiskAssessment', back_populates='assessor', foreign_keys='RiskAssessment.assessed_by')
    emergency_drills = db.relationship('EmergencyDrill', back_populates='coordinator', foreign_keys='EmergencyDrill.coordinator_id')
    waste_disposals = db.relationship('WasteDisposal', back_populates='disposer', foreign_keys='WasteDisposal.disposed_by')
    patient_safety_incidents = db.relationship('PatientSafetyIncident', back_populates='reporter', foreign_keys='PatientSafetyIncident.reported_by')
    fall_risk_assessments = db.relationship('FallRiskAssessment', back_populates='assessor', foreign_keys='FallRiskAssessment.assessed_by')
    medication_safety_checks = db.relationship('MedicationSafetyCheck', back_populates='administrator', foreign_keys='MedicationSafetyCheck.administered_by')
    indoor_air_quality = db.relationship('IndoorAirQuality', back_populates='measurer', foreign_keys='IndoorAirQuality.measured_by')
    surface_sanitation = db.relationship('SurfaceSanitation', back_populates='tester', foreign_keys='SurfaceSanitation.tested_by')
    employee_health_screenings = db.relationship('EmployeeHealthScreening', back_populates='conductor', foreign_keys='EmployeeHealthScreening.conducted_by')
    workplace_ergonomics = db.relationship('WorkplaceErgonomics', back_populates='assessor', foreign_keys='WorkplaceErgonomics.assessed_by')
    safety_kpis = db.relationship('SafetyKPI', back_populates='creator', foreign_keys='SafetyKPI.created_by')
    safety_kpi_measurements = db.relationship('SafetyKPIMeasurement', back_populates='measurer', foreign_keys='SafetyKPIMeasurement.measured_by')
    safety_documents = db.relationship('SafetyDocument', back_populates='creator', foreign_keys='SafetyDocument.created_by')
    document_reviews = db.relationship('DocumentReview', back_populates='reviewer', foreign_keys='DocumentReview.reviewer_id')
    improvement_initiatives = db.relationship('ImprovementInitiative', back_populates='proposer', foreign_keys='ImprovementInitiative.proposed_by')
    corrective_actions = db.relationship('CorrectiveAction', back_populates='assignee', foreign_keys='CorrectiveAction.assigned_to')
    
    approved_admins = db.relationship('User', backref=db.backref('approver', remote_side=[id]))
    subscription_history = db.relationship('SubscriptionHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    payment_history = db.relationship('PaymentHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    def to_dict(self):
        """Convert user to dictionary with admin-specific fields"""
        base_dict = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'department': self.department,
            'phone': self.phone,
            'avatar_url': self.avatar_url,
            'is_active': self.is_active,
            'verified': self.verified,
            'is_verified': self.is_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'company_name': self.company_name,
            'industry': self.industry,
            'user_type': self.user_type,
            'is_system_team': self.is_system_team,
            'country': self.country,
            'preferred_language': self.preferred_language,
            'employee_count': self.employee_count,
            'subscription_plan': self.subscription_plan,
            'effective_plan': self.get_effective_plan(),
            'is_trial_active': self.is_trial_active(),
            'subscription_status': self.subscription_status,
            'billing_cycle': self.billing_cycle,
            'approval_status': self.approval_status,
            'timezone': self.timezone,
            'hospital_id': self.hospital_id,
            'is_enterprise': self.is_enterprise,
            'enterprise_features': self.enterprise_features,
            'logo_url': self.company_logo,  # User's company logo
            'company_logo': self.company_logo,  # Alternative name for consistency
            'company_id': self.company_id,  # Also include company_id for reference
            'company': {
                'id': self.company_id,
                'name': self.company_name,
                'logo_url': self.company_logo
        } if self.company_id else None
        }
        
        # Add document-related fields
        document_dict = {
            'documents_uploaded': self.documents_uploaded,
            'documents_verified': self.documents_verified,
            'documents_uploaded_at': self.documents_uploaded_at.isoformat() if self.documents_uploaded_at else None
        }
        base_dict.update(document_dict)
        
        # Add admin-specific fields if user is admin
        if self.user_type in ['admin', 'safetypro', 'system', 'platform_owner']:
            admin_dict = {
                'admin_role': self.admin_role,
                'admin_level': self.admin_level,
                'admin_tier': self.admin_tier,
                'is_platform_owner': self.is_platform_owner,
                'platform_permissions': self.platform_permissions,
                'approved_at': self.approved_at.isoformat() if self.approved_at else None,
                'approved_by': self.approved_by,
                'rejected_at': self.rejected_at.isoformat() if self.rejected_at else None,
                'rejection_reason': self.rejection_reason,
                'custom_requirements': self.custom_requirements,
                'payment_method': self.payment_method,
                'payment_gateway': self.payment_gateway,
                'address': self.address,
                'website': self.website,
                'trial_ends_at': self.trial_ends_at.isoformat() if self.trial_ends_at else None,
                'trial_plan': self.trial_plan,
                'currency': self.currency,
                'company_logo': self.company_logo,
                'last_payment_date': self.last_payment_date.isoformat() if self.last_payment_date else None,
                'next_payment_date': self.next_payment_date.isoformat() if self.next_payment_date else None,
                'payment_id': self.payment_id,
                'subscription_starts_at': self.subscription_starts_at.isoformat() if self.subscription_starts_at else None,
                'subscription_ends_at': self.subscription_ends_at.isoformat() if self.subscription_ends_at else None
            }
            base_dict.update(admin_dict)
        
        # Add usage tracking fields for all users
        usage_dict = {
            'monthly_uploads_used': self.monthly_uploads_used,
            'monthly_api_calls_used': self.monthly_api_calls_used,
            'monthly_ai_requests_used': self.monthly_ai_requests_used,
            'monthly_video_minutes_used': self.monthly_video_minutes_used,
            'remaining_limits': self.get_remaining_limits(),
            'usage_reset_date': self.usage_reset_date.isoformat() if self.usage_reset_date else None
        }
        base_dict.update(usage_dict)
        
        # Add activity tracking fields
        activity_dict = {
            'login_count': self.login_count,
            'activity_count': self.activity_count,
            'performance_score': self.performance_score,
            'performance_grade': self.performance_grade,
            'login_frequency': self.login_frequency,
            'activity_rate': self.activity_rate,
            'avg_session_duration': self.avg_session_duration,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'total_session_duration': self.total_session_duration
        }
        base_dict.update(activity_dict)
        
        return base_dict
    
    def is_admin_approved(self):
        """Check if admin is approved and active"""
        if self.user_type not in ['admin', 'safetypro', 'system', 'platform_owner']:
            return False
        return (self.verified and  # Email verified
                self.approval_status == 'approved' and  # Manually approved
                self.is_active)  # Account active
    
    def can_login(self):
        """Check if user can login"""
        if not self.verified:
            return False, "Email not verified"
        
        if self.user_type in ['admin', 'safetypro', 'system', 'platform_owner']:
            if self.approval_status != 'approved':
                return False, f"Admin account {self.approval_status}"
            if not self.is_active:
                return False, "Account deactivated"
        
        return True, "OK"
    
    def get_remaining_limits(self):
        """Get remaining usage limits based on subscription plan"""
        # Define limits for each plan
        limits = {
            'free': {
                'uploads': 10,
                'api_calls': 100,
                'ai_requests': 50,
                'video_minutes': 60
            },
            'basic': {
                'uploads': 100,
                'api_calls': 1000,
                'ai_requests': 500,
                'video_minutes': 600
            },
            'pro': {
                'uploads': 1000,
                'api_calls': 10000,
                'ai_requests': 5000,
                'video_minutes': 6000
            },
            'enterprise': {
                'uploads': float('inf'),
                'api_calls': float('inf'),
                'ai_requests': float('inf'),
                'video_minutes': float('inf')
            }
        }
        
        effective_plan = self.get_effective_plan()
        plan_limits = limits.get(effective_plan, limits['free'])
        
        return {
            'uploads_remaining': max(0, plan_limits['uploads'] - self.monthly_uploads_used),
            'api_calls_remaining': max(0, plan_limits['api_calls'] - self.monthly_api_calls_used),
            'ai_requests_remaining': max(0, plan_limits['ai_requests'] - self.monthly_ai_requests_used),
            'video_minutes_remaining': max(0, plan_limits['video_minutes'] - self.monthly_video_minutes_used),
            'uploads_limit': plan_limits['uploads'],
            'api_calls_limit': plan_limits['api_calls'],
            'ai_requests_limit': plan_limits['ai_requests'],
            'video_minutes_limit': plan_limits['video_minutes']
        }
    
    def reset_monthly_usage(self):
        """Reset monthly usage counters"""
        now = datetime.utcnow()
        if now.month != self.usage_reset_date.month or now.year != self.usage_reset_date.year:
            self.monthly_uploads_used = 0
            self.monthly_api_calls_used = 0
            self.monthly_ai_requests_used = 0
            self.monthly_video_minutes_used = 0
            self.usage_reset_date = now
            return True
        return False
    
    def get_effective_plan(self):
        """Get current effective plan (considering trial)"""
        # Check if trial is active
        if self.trial_ends_at and datetime.utcnow() < self.trial_ends_at:
            return self.trial_plan or 'pro'  # Default trial to pro
        
        # Check if subscription is active
        if self.subscription_status != 'active':
            return 'free'
        
        return self.subscription_plan or 'free'
    
    def is_trial_active(self):
        """Check if user is in trial period"""
        if not self.trial_ends_at:
            return False
        
        return datetime.utcnow() < self.trial_ends_at
    
    def get_pricing_info(self):
        """Get pricing info for user's country and plan"""
        # This assumes you have COUNTRY_PRICING configured in your app
        try:
            from app import COUNTRY_PRICING  # Import your pricing config
        except ImportError:
            # Default pricing if not configured
            COUNTRY_PRICING = {
                'default': {
                    'free': {'price': 0, 'currency': 'USD'},
                    'basic': {'price': 49, 'currency': 'USD'},
                    'pro': {'price': 99, 'currency': 'USD'},
                    'enterprise': {'price': 299, 'currency': 'USD'}
                }
            }
        
        country = self.country or 'default'
        plan = self.get_effective_plan()
        
        country_pricing = COUNTRY_PRICING.get(country, COUNTRY_PRICING['default'])
        return country_pricing.get(plan, country_pricing['free'])
    
    def can_access_feature(self, feature_name):
        """Check if user can access a specific feature"""
        # This assumes you have PLANS and PLAN_REQUIREMENTS configured
        try:
            from app import PLANS, PLAN_REQUIREMENTS  # Import your plans config
        except ImportError:
            # Default configuration if not set
            PLANS = {
                'free': {'limits': {'uploads_per_month': 10, 'api_calls_per_month': 100}},
                'basic': {'limits': {'uploads_per_month': 100, 'api_calls_per_month': 1000}},
                'pro': {'limits': {'uploads_per_month': 1000, 'api_calls_per_month': 10000}},
                'enterprise': {'limits': {}}
            }
            
            PLAN_REQUIREMENTS = {
                'ai_analysis': ('pro', 'ai_requests_per_month', 'AI analysis requires Pro plan'),
                'video_analysis': ('pro', 'video_analysis_minutes', 'Video analysis requires Pro plan'),
                'api_access': ('basic', 'api_calls_per_month', 'API access requires Basic plan'),
                'advanced_analytics': ('pro', None, 'Advanced analytics requires Pro plan'),
                'custom_integrations': ('enterprise', None, 'Custom integrations require Enterprise plan')
            }
        
        if not PLAN_REQUIREMENTS.get(feature_name):
            return True, None  # No restriction defined
        
        required_plan, limit_field, error_msg = PLAN_REQUIREMENTS[feature_name]
        effective_plan = self.get_effective_plan()
        
        # Check plan hierarchy
        plan_hierarchy = {'free': 0, 'basic': 1, 'pro': 2, 'enterprise': 3}
        user_level = plan_hierarchy.get(effective_plan, 0)
        required_level = plan_hierarchy.get(required_plan, 0)
        
        if user_level < required_level:
            return False, error_msg
        
        # Check usage limits if applicable
        if limit_field:
            plan_limits = PLANS.get(effective_plan, PLANS['free'])['limits']
            limit = plan_limits.get(limit_field)
            
            if limit and limit != "Unlimited":
                # Get current usage
                if limit_field == 'uploads_per_month':
                    used = self.monthly_uploads_used
                elif limit_field == 'api_calls_per_month':
                    used = self.monthly_api_calls_used
                elif limit_field == 'ai_requests_per_month':
                    used = self.monthly_ai_requests_used
                elif limit_field == 'video_analysis_minutes':
                    used = self.monthly_video_minutes_used
                else:
                    used = 0
                
                if used >= limit:
                    return False, f"Monthly limit for {limit_field} exceeded"
        
        return True, None
    
    def check_and_reset_usage(self):
        """Reset monthly usage counters if needed"""
        current_date = datetime.utcnow()
        
        # Reset on month change
        if current_date.month != self.usage_reset_date.month:
            self.monthly_uploads_used = 0
            self.monthly_api_calls_used = 0
            self.monthly_ai_requests_used = 0
            self.monthly_video_minutes_used = 0
            self.usage_reset_date = current_date
            return True
        return False
    
    def increment_usage(self, usage_type, amount=1):
        """Increment usage counter for a specific type"""
        self.check_and_reset_usage()  # Check if we need to reset first
        
        if usage_type == 'uploads':
            self.monthly_uploads_used += amount
        elif usage_type == 'api_calls':
            self.monthly_api_calls_used += amount
        elif usage_type == 'ai_requests':
            self.monthly_ai_requests_used += amount
        elif usage_type == 'video_minutes':
            self.monthly_video_minutes_used += amount
        
        return True
    
    def get_subscription_days_left(self):
        """Get number of days left in subscription/trial"""
        if self.is_trial_active() and self.trial_ends_at:
            from datetime import datetime
            days_left = (self.trial_ends_at - datetime.utcnow()).days
            return max(0, days_left)
        
        if self.subscription_ends_at and self.subscription_status == 'active':
            from datetime import datetime
            days_left = (self.subscription_ends_at - datetime.utcnow()).days
            return max(0, days_left)
        
        return 0
    
    @property
    def plan(self):
        """Backward compatibility property - returns subscription_plan"""
        return self.subscription_plan
    
    @plan.setter
    def plan(self, value):
        """Backward compatibility property setter"""
        self.subscription_plan = value
    
    def has_permission(self, permission_name):
        """Check if user has specific platform permission"""
        if not self.platform_permissions:
            return False
        
        # Platform owners have all permissions
        if self.is_platform_owner:
            return True
        
        # Check user-specific permissions
        return permission_name in self.platform_permissions


class SafetyViolation(db.Model):
    __tablename__ = 'safety_violations'
    
    id = db.Column(db.Integer, primary_key=True)
    camera_id = db.Column(db.String(128), nullable=False, index=True)
    violation_type = db.Column(db.String(128), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    frame_image = db.Column(db.String(256), nullable=False)
    department = db.Column(db.String(128))
    industry = db.Column(db.String(64))
    risk_level = db.Column(db.String(32))  # Low, Medium, High, Critical
    acknowledged = db.Column(db.Boolean, default=False)
    acknowledged_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    acknowledged_at = db.Column(db.DateTime)
    analysis_data = db.Column(db.Text)  # JSON string of detailed analysis
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)




# Add this SQLAlchemy model definition with your other models
class MedicalAnalysis(db.Model):
    __tablename__ = 'medical_analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    analysis_type = db.Column(db.String(50), nullable=False)  # chat, symptom_analysis, disease_prediction, etc.
    input_data = db.Column(db.Text)  # JSON string of input data
    output_data = db.Column(db.Text)  # JSON string of output data
    confidence_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('medical_analyses', lazy=True))


class APIUsage(db.Model):
    __tablename__ = 'api_usage'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True) 
    endpoint = db.Column(db.String(256), nullable=False)
    method = db.Column(db.String(16), nullable=False)  # GET, POST, PUT, DELETE
    ip_address = db.Column(db.String(64))
    user_agent = db.Column(db.Text)
    response_status = db.Column(db.Integer)
    processing_time = db.Column(db.Float)  # in seconds
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Additional tracking fields
    feature = db.Column(db.String(64))  # uploads, ai_requests, etc.
    resource_id = db.Column(db.Integer)  # ID of the created/modified resource
    request_metadata = db.Column(db.Text)  # JSON for additional data
    
    # Relationship
    user = db.relationship('User', backref=db.backref('api_usage', lazy=True))

class MonthlyUsageSummary(db.Model):
    __tablename__ = 'monthly_usage_summary'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)  # 1-12
    feature = db.Column(db.String(64), nullable=False)  # uploads, api_calls, ai_requests, etc.
    usage_count = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'year', 'month', 'feature', name='unique_monthly_usage'),)

class Verification(db.Model):
    __tablename__ = 'verifications'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, index=True)
    code = db.Column(db.String(16), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    purpose = db.Column(db.String(32), default='email_verification')  # email_verification, password_reset, etc.
    
    # ✅ Add expires_at field - default 10 minutes from creation
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=10))
    
    # Optional: add used flag to prevent reuse
    used = db.Column(db.Boolean, default=False)
    
    # Optional: track attempts
    attempts = db.Column(db.Integer, default=0)
    
    def is_expired(self):
        """Check if verification code has expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self):
        """Check if verification code is valid (not expired and not used)"""
        return not self.used and not self.is_expired()
    
    def __repr__(self):
        return f'<Verification {self.email} - {self.code} (expires: {self.expires_at})>'
class PasswordReset(db.Model):
    __tablename__ = 'password_resets'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, index=True)
    token = db.Column(db.String(128), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)

# models.py - Consolidated Upload File Model

class UploadedFile(db.Model):
    """Unified model for uploaded files - supports both local and cloud storage"""
    __tablename__ = 'uploaded_files'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # File information
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512))  # Local file path (if local storage)
    file_url = db.Column(db.String(500), nullable=False)  # Access URL
    
    # File metadata
    file_size = db.Column(db.Integer)  # in bytes
    mime_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    
    # Categorization
    upload_type = db.Column(db.String(64), default='document')  # document, image, video, audio, other
    category = db.Column(db.String(64))  # Safety, HSE, Medical, etc.
    folder = db.Column(db.String(100), default='general')
    
    # Storage settings
    storage_type = db.Column(db.String(50), default='local')  # backblaze_b2, local, aws_s3
    object_key = db.Column(db.String(500))  # Cloud storage object key
    is_public = db.Column(db.Boolean, default=False)
    
    # Grouping and metadata
    upload_session_id = db.Column(db.String(128))  # For grouping multiple files
    file_metadata = db.Column(db.JSON)  # Additional metadata as JSON
    
    # Timestamps
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('uploaded_files', lazy=True))
    
    # Indexes for performance
    __table_args__ = (
        db.Index('idx_uploaded_files_user_type', 'user_id', 'upload_type'),
        db.Index('idx_uploaded_files_uploaded_at', 'uploaded_at'),
        db.Index('idx_uploaded_files_category', 'category'),
    )
    
    def __repr__(self):
        return f'<UploadedFile {self.original_filename} (User: {self.user_id})>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'original_filename': self.original_filename,
            'stored_filename': self.stored_filename,
            'file_url': self.file_url,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'description': self.description,
            'upload_type': self.upload_type,
            'category': self.category,
            'folder': self.folder,
            'storage_type': self.storage_type,
            'is_public': self.is_public,
            'upload_session_id': self.upload_session_id,
            'file_metadata': self.file_metadata,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @property
    def file_extension(self):
        """Get file extension from original filename"""
        if self.original_filename:
            return self.original_filename.rsplit('.', 1)[-1].lower() if '.' in self.original_filename else ''
        return ''
    
    @property
    def is_image(self):
        """Check if file is an image"""
        return self.mime_type and self.mime_type.startswith('image/')
    
    @property
    def is_video(self):
        """Check if file is a video"""
        return self.mime_type and self.mime_type.startswith('video/')
    
    @property
    def is_document(self):
        """Check if file is a document"""
        document_types = ['application/pdf', 'application/msword', 
                         'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                         'text/plain', 'application/vnd.ms-excel',
                         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
        return self.mime_type in document_types
    

import json
from datetime import datetime
from sqlalchemy.exc import IntegrityError

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # ============================================================
    # BACKWARD COMPATIBILITY - Keep user_id for existing endpoints
    # ============================================================
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    analysis_result = db.Column(db.JSON, nullable=True, default=None)
    
    # ============================================================
    # NEW DOCUMENT MANAGEMENT FIELDS
    # ============================================================
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    content_hash = db.Column(db.String(255))
    document_type = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))
    module = db.Column(db.String(50), default='general')
    priority = db.Column(db.String(20), default='medium')
    status = db.Column(db.String(20), default='draft')
    version = db.Column(db.Integer, default=1)
    is_latest = db.Column(db.Boolean, default=True)
    file_url = db.Column(db.String(500))
    file_name = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    file_hash = db.Column(db.String(255))
    mime_type = db.Column(db.String(100))
    
    # ✅ FIXED: Store tags as JSON string in TEXT column
    tags = db.Column(db.Text, default='[]')
    
    # ============================================================
    # ✅ NEW: Editing Source — distinguishes where a doc came from
    #   'regular' — normal upload or modal-edited document
    #   'sidebar' — created/edited in standalone sidebar editor
    # ============================================================
    editing_source = db.Column(db.String(20), default='regular', index=True)
    
    is_confidential = db.Column(db.Boolean, default=False)
    requires_approval = db.Column(db.Boolean, default=True)
    approval_workflow = db.Column(db.String(50), default='simple')
    review_status = db.Column(db.String(20), default='never_reviewed')
    review_frequency = db.Column(db.String(20))
    review_date = db.Column(db.DateTime)
    next_review_date = db.Column(db.DateTime)
    last_reviewed_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    site_id = db.Column(db.Integer)
    parent_document_id = db.Column(db.Integer)
    
    # ============================================================
    # USER REFERENCES (Both for backward compatibility)
    # ============================================================
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # ============================================================
    # TIMESTAMPS
    # ============================================================
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    approved_at = db.Column(db.DateTime)
    published_at = db.Column(db.DateTime)
    archived_at = db.Column(db.DateTime)
    
    # ============================================================
    # RELATIONSHIPS
    # ============================================================
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('user_documents', lazy='dynamic'))
    
    creator = db.relationship('User', foreign_keys=[created_by], backref=db.backref('created_documents', lazy='dynamic'))
    updater = db.relationship('User', foreign_keys=[updated_by])
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    approver = db.relationship('User', foreign_keys=[approved_by])
    company = db.relationship('Company', foreign_keys=[company_id], backref=db.backref('company_documents', lazy='dynamic'))
    
    versions = db.relationship('DocumentVersion', foreign_keys='DocumentVersion.document_id', backref='doc_version', lazy='dynamic', cascade='all, delete-orphan')
    metadata_items = db.relationship('DocumentMetadata', foreign_keys='DocumentMetadata.document_id', backref='doc_metadata', lazy='dynamic', cascade='all, delete-orphan')
    comment_items = db.relationship('DocumentComment', foreign_keys='DocumentComment.document_id', backref='doc_comment', lazy='dynamic', cascade='all, delete-orphan')
    audit_logs = db.relationship('DocumentAuditLog', foreign_keys='DocumentAuditLog.document_id', backref='doc_audit', lazy='dynamic', cascade='all, delete-orphan')
    links = db.relationship('DocumentLink', foreign_keys='DocumentLink.document_id', backref='doc_link', lazy='dynamic', cascade='all, delete-orphan')
    review_history_items = db.relationship('ReviewHistory', foreign_keys='ReviewHistory.document_id', backref='doc_review', lazy='dynamic', cascade='all, delete-orphan')
    signatures = db.relationship('DocumentSignature', foreign_keys='DocumentSignature.document_id', backref='doc_signature', lazy='dynamic', cascade='all, delete-orphan')
    workflows = db.relationship('DocumentWorkflow', foreign_keys='DocumentWorkflow.document_id', backref='doc_workflow', lazy='dynamic', cascade='all, delete-orphan')
    
    __table_args__ = (
        db.Index('idx_documents_user_id', 'user_id'),
        db.Index('idx_documents_title', 'title'),
        db.Index('idx_documents_status', 'status'),
        db.Index('idx_documents_type', 'document_type'),
        db.Index('idx_documents_module', 'module'),
        db.Index('idx_documents_company', 'company_id'),
        db.Index('idx_documents_created_at', 'created_at'),
        db.Index('idx_documents_status_company', 'status', 'company_id'),
        db.Index('idx_documents_type_company', 'document_type', 'company_id'),
        # ✅ NEW: compound index for fast draft queries
        db.Index('idx_documents_editing_source', 'editing_source', 'company_id'),
    )
    
    def to_dict(self):
        """Convert document to dictionary with proper type handling"""
        
        # Parse tags from JSON string
        try:
            if self.tags:
                tags = json.loads(self.tags) if isinstance(self.tags, str) else self.tags
            else:
                tags = []
        except (json.JSONDecodeError, TypeError):
            if self.tags and isinstance(self.tags, str):
                tags = [t.strip() for t in self.tags.split(',') if t.strip()]
            else:
                tags = []
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'content_hash': self.content_hash,
            'document_type': self.document_type,
            'category': self.category,
            'module': self.module,
            'priority': self.priority,
            'status': self.status,
            'version': self.version,
            'is_latest': self.is_latest,
            'file_url': self.file_url,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'file_hash': self.file_hash,
            'mime_type': self.mime_type,
            'tags': tags,
            'editing_source': self.editing_source or 'regular',   # ✅ NEW
            'is_confidential': self.is_confidential,
            'requires_approval': self.requires_approval,
            'approval_workflow': self.approval_workflow,
            'review_status': self.review_status,
            'review_frequency': self.review_frequency,
            'review_date': self.review_date.isoformat() if self.review_date else None,
            'next_review_date': self.next_review_date.isoformat() if self.next_review_date else None,
            'last_reviewed_at': self.last_reviewed_at.isoformat() if self.last_reviewed_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'company_id': self.company_id,
            'site_id': self.site_id,
            'parent_document_id': self.parent_document_id,
            'created_by': self.created_by,
            'created_by_name': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_by': self.updated_by,
            'updated_by_name': self.updater.name if self.updater else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'reviewed_by': self.reviewed_by,
            'reviewed_by_name': self.reviewer.name if self.reviewer else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'approved_by': self.approved_by,
            'approved_by_name': self.approver.name if self.approver else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'archived_at': self.archived_at.isoformat() if self.archived_at else None,
            'versions_count': self.versions.count() if self.versions else 0,
            'comments_count': self.comment_items.count() if self.comment_items else 0,
            'signatures_count': self.signatures.count() if self.signatures else 0
        }
    
    def set_tags(self, tags_list):
        """Helper method to set tags from a list"""
        if isinstance(tags_list, list):
            self.tags = json.dumps(tags_list)
        elif isinstance(tags_list, str):
            try:
                json.loads(tags_list)
                self.tags = tags_list
            except json.JSONDecodeError:
                self.tags = json.dumps([t.strip() for t in tags_list.split(',') if t.strip()])
        else:
            self.tags = '[]'
    
    def get_tags(self):
        """Helper method to get tags as a list"""
        try:
            if self.tags:
                return json.loads(self.tags) if isinstance(self.tags, str) else self.tags
            return []
        except (json.JSONDecodeError, TypeError):
            if self.tags and isinstance(self.tags, str):
                return [t.strip() for t in self.tags.split(',') if t.strip()]
            return []

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # info, warning, error, success, critical
    priority = db.Column(db.String(16), default='medium')  # low, medium, high, critical
    category = db.Column(db.String(100))  # system, safety, compliance, training, project
    is_read = db.Column(db.Boolean, default=False)
    action_url = db.Column(db.String(512))  # URL for action button
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    
    def to_dict(self):
        return {
        'id': self.id,
        'user_id': self.user_id,
        'user_name': self.user.name if self.user else None,
        'title': self.title,
        'message': self.message,
        'type': self.type,
        'priority': self.priority,
        'category': self.category,
        'is_read': self.is_read,
        'action_url': self.action_url,
        'expires_at': self.expires_at.isoformat() if self.expires_at else None,
        'created_at': self.created_at.isoformat() if self.created_at else None
    }

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    members = db.relationship('TeamMember', backref='team', lazy=True, cascade='all, delete-orphan')
    invitations = db.relationship('TeamInvitation', backref='team', lazy=True, cascade='all, delete-orphan')

class TeamMember(db.Model):
    __tablename__ = 'team_members'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    role = db.Column(db.String(32), default='member')  # owner, admin, member, viewer
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    permissions = db.Column(db.Text)  # JSON string of permissions
    
    __table_args__ = (db.UniqueConstraint('team_id', 'user_id', name='unique_team_member'),)

class TeamInvitation(db.Model):
    __tablename__ = 'team_invitations'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Invited user
    email = db.Column(db.String(128), nullable=False)
    invited_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # User who sent invitation
    token = db.Column(db.String(128), unique=True, index=True)
    status = db.Column(db.String(32), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    role = db.Column(db.String(32), default='member')

    # Relationships with explicit foreign_keys
    
    invited_user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('received_team_invitations', lazy=True))
    inviting_user = db.relationship('User', foreign_keys=[invited_by], backref=db.backref('sent_team_invitations', lazy=True))

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    plan = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(32), default='active')  # active, canceled, expired, suspended
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    auto_renew = db.Column(db.Boolean, default=True)
    payment_method = db.Column(db.String(64))
    last_payment_date = db.Column(db.DateTime)
    next_payment_date = db.Column(db.DateTime)

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(16), nullable=False)
    plan = db.Column(db.String(32), nullable=False)
    duration = db.Column(db.String(32), nullable=False)  # 1_month, 6_month, 1_year
    payment_method = db.Column(db.String(64))
    status = db.Column(db.String(32), default='pending')  # pending, completed, failed, refunded
    transaction_id = db.Column(db.String(128), unique=True, index=True)
    paystack_reference = db.Column(db.String(128), index=True)
    payment_details = db.Column(db.Text)  # JSON string of payment details
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    completed_at = db.Column(db.DateTime)
    failure_reason = db.Column(db.Text)

class AdminAuditLog(db.Model):
    __tablename__ = 'admin_audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    action = db.Column(db.String(256), nullable=False)
    resource_type = db.Column(db.String(64))
    resource_id = db.Column(db.Integer)
    details = db.Column(db.Text)  # Add this field for JSON details
    ip_address = db.Column(db.String(64))
    user_agent = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship('User', backref=db.backref('admin_audit_logs', lazy=True))



class EditableDocument(db.Model):
    __tablename__ = 'editable_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, default="")
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    template_id = db.Column(db.Integer, db.ForeignKey('document_templates.id'))
    category = db.Column(db.String(64))
    status = db.Column(db.String(32), default='draft')  # draft, in_review, approved, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=1)
    last_modified_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class Workflow(db.Model):
    __tablename__ = 'workflows'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512))
    steps = db.Column(db.Text)  # JSON-encoded list of steps
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    industry = db.Column(db.String(64))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Referral(db.Model):
    __tablename__ = 'referrals'
    
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    referred_email = db.Column(db.String(128), nullable=False, index=True)
    status = db.Column(db.String(32), default='pending')  # pending, registered, rewarded
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reward_given = db.Column(db.Boolean, default=False)
    reward_amount = db.Column(db.Float)
    reward_type = db.Column(db.String(32))  # credit, discount, extended_trial

# ===== COMPUTER VISION & AI MODELS =====

class CameraFeed(db.Model):
    __tablename__ = 'camera_feeds'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(512), nullable=False)
    location = db.Column(db.String(256))
    department = db.Column(db.String(128))
    industry = db.Column(db.String(64), default='Healthcare')
    status = db.Column(db.String(32), default='inactive')  # inactive, active, error, maintenance
    monitor_id = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = db.Column(db.DateTime)
    resolution = db.Column(db.String(32))  # 720p, 1080p, 4K
    frame_rate = db.Column(db.Integer)  # FPS


class VideoAnalysis(db.Model):
    __tablename__ = 'video_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    video_path = db.Column(db.String(512), nullable=False)
    upload_file_id = db.Column(db.Integer, db.ForeignKey('uploaded_files.id'))   # ← FIXED
    analysis_results = db.Column(db.Text)
    duration = db.Column(db.Float)
    violations_count = db.Column(db.Integer, default=0)
    compliance_score = db.Column(db.Float)
    industry = db.Column(db.String(64))
    status = db.Column(db.String(32), default='completed')
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    processing_time = db.Column(db.Float)

class AIRequest(db.Model):
    __tablename__ = 'ai_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    request_type = db.Column(db.String(64), nullable=False)  # safety_analysis, compliance_check, incident_analysis, etc.
    user_input = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text)
    company_name = db.Column(db.String(256))
    company_logo = db.Column(db.String(512))
    include_logo = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(32), default='completed')  # pending, processing, completed, failed
    processing_time = db.Column(db.Float)  # in seconds
    tokens_used = db.Column(db.Integer)
    cost = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class PredictiveModel(db.Model):
    __tablename__ = 'predictive_models'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64))  # AirQuality, WaterQuality, IncidentPrediction, RiskAssessment
    version = db.Column(db.String(32))
    performance_metrics = db.Column(db.Text)  # JSON
    file_path = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SubscriptionHistory(db.Model):
    """Track subscription changes over time"""
    __tablename__ = 'subscription_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    old_plan = db.Column(db.String(50))
    new_plan = db.Column(db.String(50))
    billing_cycle = db.Column(db.String(20))
    country = db.Column(db.String(64))
    currency = db.Column(db.String(16))
    amount = db.Column(db.Float, nullable=True)
    
    change_type = db.Column(db.String(20))  # 'upgrade', 'downgrade', 'renewal', 'trial_start', 'trial_end'
    change_reason = db.Column(db.Text, nullable=True)
    
    effective_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PaymentHistory(db.Model):
    """Track all payments"""
    __tablename__ = 'payment_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    plan = db.Column(db.String(50))
    billing_cycle = db.Column(db.String(20))
    country = db.Column(db.String(64))
    currency = db.Column(db.String(16))
    amount = db.Column(db.Float, nullable=False)
    
    payment_method = db.Column(db.String(50))
    payment_gateway = db.Column(db.String(50))
    payment_id = db.Column(db.String(100), unique=True)
    
    status = db.Column(db.String(20), default='pending')  # 'pending', 'completed', 'failed', 'refunded'
    gateway_response = db.Column(db.JSON, nullable=True)
    
    invoice_url = db.Column(db.String(500), nullable=True)
    receipt_url = db.Column(db.String(500), nullable=True)
    
    paid_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ===== USER & AUTHENTICATION =====

from datetime import datetime



class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip_address = db.Column(db.String(50))
    activity_data = db.Column(db.JSON)  # CHANGED: Renamed from 'metadata' to 'activity_data'
    
    # Relationships
    user = db.relationship('User', backref=db.backref('activity_logs', lazy=True))
    
    # Indexes for better query performance
    __table_args__ = (
        db.Index('idx_activity_user_timestamp', 'user_id', 'timestamp'),
        db.Index('idx_activity_type', 'activity_type'),
        db.Index('idx_activity_user_type', 'user_id', 'activity_type'),
    )
    
    def __repr__(self):
        return f'<ActivityLog {self.id} - {self.activity_type}>'
    

def create_activity_log(user_id, activity_type, description, ip_address=None, metadata=None):
    """Create activity log entry"""
    try:
        # Create activity log
        activity_log = ActivityLog(
            user_id=user_id,
            activity_type=activity_type,
            description=description,
            ip_address=ip_address or request.remote_addr,
            activity_data=metadata or {}  # CHANGED: Use 'activity_data' instead of 'metadata'
        )
        db.session.add(activity_log)
        
        # Update user activity count
        user = User.query.get(user_id)
        if user:
            user.activity_count = (user.activity_count or 0) + 1
            user.last_activity = datetime.utcnow()
            db.session.add(user)
            
            # Update last activity in active session
            session = UserSession.query.filter_by(
                user_id=user_id,
                is_active=True
            ).order_by(UserSession.login_time.desc()).first()
            
            if session:
                session.last_activity = datetime.utcnow()
                db.session.add(session)
        
        db.session.commit()
        
        # Update performance score in background
        update_user_performance_score(user_id)
        
        logger.info(f"Activity tracked for user {user_id}: {activity_type} - {description}")
        
        return activity_log.id
        
    except Exception as e:
        logger.error(f"Failed to track activity for user {user_id}: {e}")
        db.session.rollback()
        return None

# ============== ADMIN APPROVAL LOG MODEL ==============
class AdminApprovalLog(db.Model):
    __tablename__ = 'admin_approval_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    approved_by = db.Column(db.Integer, nullable=False, index=True)
    action = db.Column(db.String(50), nullable=False)  # 'approved', 'rejected'
    notes = db.Column(db.Text)
    previous_status = db.Column(db.String(50))
    new_status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Additional metadata
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.Text)
    
    def __repr__(self):
        return f'<AdminApprovalLog {self.id}: {self.action} user {self.user_id}>'

# ============== LOGIN LOG MODEL ==============
class LoginLog(db.Model):
    __tablename__ = 'login_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    login_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    logout_time = db.Column(db.DateTime)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.Text)
    success = db.Column(db.Boolean, default=True)
    failure_reason = db.Column(db.Text)
    
    def __repr__(self):
        return f'<LoginLog {self.id}: user {self.user_id}>'


class Industry(db.Model):
    __tablename__ = 'industries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(50), nullable=False, unique=True)  # oil_gas, construction, healthcare, etc.
    description = db.Column(db.Text)
    risk_level = db.Column(db.String(20), nullable=False)  # low, medium, high, very_high
    color_code = db.Column(db.String(7))  # HEX color
    icon_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
        'id': self.id,
        'name': self.name,
        'code': self.code,
        'description': self.description,
        'risk_level': self.risk_level,
        'color_code': self.color_code,
        'icon_name': self.icon_name,
        'is_active': self.is_active,
        'created_at': self.created_at.isoformat() if self.created_at else None,
        'updated_at': self.updated_at.isoformat() if self.updated_at else None
    }

# ============== USER SESSION MODEL (for tracking active sessions) ==============

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=True)
    browser_notifications = db.Column(db.Boolean, default=True)
    notification_frequency = db.Column(db.String(32), default='realtime')
    categories = db.Column(db.Text, default='{}')  # JSON string
    quiet_hours = db.Column(db.Text, default='{}') # JSON string
    
    user = db.relationship('User', backref=db.backref('preferences', uselist=False))

# ===== INCIDENT MANAGEMENT =====

class Incident(db.Model):
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    incident_type = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='reported')
    location = db.Column(db.String(255))
    department = db.Column(db.String(100))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'))
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    
    # ✅ ADD project_id
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    
    date_occurred = db.Column(db.DateTime, nullable=False)
    date_reported = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    investigation_details = db.Column(db.Text)
    corrective_actions = db.Column(db.Text)
    root_cause = db.Column(db.Text)
    resolution_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ✅ RELATIONSHIPS - Use back_populates, NOT backref
    reporter = db.relationship('User', foreign_keys=[reported_by], backref=db.backref('reported_incidents', lazy=True))
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    department_rel = db.relationship('Department', backref=db.backref('incidents', lazy=True))
    industry = db.relationship('Industry')
    
    # Use back_populates to link to Company (NOT backref)
    company = db.relationship('Company', back_populates='incidents')
    
    # ✅ FIX: Use a unique name for the project relationship
    project = db.relationship('Project', back_populates='incidents_rel')
    
    attachments = db.relationship('IncidentAttachment', back_populates='incident', cascade='all, delete-orphan')
    actions = db.relationship('IncidentAction', back_populates='incident', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'incident_number': self.incident_number,
            'title': self.title,
            'description': self.description,
            'incident_type': self.incident_type,
            'severity': self.severity,
            'status': self.status,
            'location': self.location,
            'department': self.department,
            'industry_id': self.industry_id,
            'industry_name': self.industry.name if self.industry else None,
            'hospital_id': self.hospital_id,
            'department_id': self.department_id,
            'reported_by': self.reported_by,
            'reporter_name': self.reporter.name if self.reporter else None,
            'assigned_to': self.assigned_to,
            'assignee_name': self.assignee.name if self.assignee else None,
            'company_id': self.company_id,
            'project_id': self.project_id,
            'project_name': self.project.name if self.project else None,
            'date_occurred': self.date_occurred.isoformat() if self.date_occurred else None,
            'date_reported': self.date_reported.isoformat() if self.date_reported else None,
            'investigation_details': self.investigation_details,
            'corrective_actions': self.corrective_actions,
            'root_cause': self.root_cause,
            'resolution_date': self.resolution_date.isoformat() if self.resolution_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'attachments_count': len(self.attachments) if self.attachments else 0,
            'actions_count': len(self.actions) if self.actions else 0,
            'timeline_count': len(self.timeline_entries) if hasattr(self, 'timeline_entries') else 0,
            'notes_count': len(self.investigation_notes) if hasattr(self, 'investigation_notes') else 0
        }
    

# New model for Safety Tools
class SafetyTool(db.Model):
    __tablename__ = 'safety_tools'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # risk_assessment, inspection, incident, compliance
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=False)
    tool_type = db.Column(db.String(50))  # calculator, analyzer, generator, monitor
    status = db.Column(db.String(20), default='active')  # active, beta, maintenance
    configuration = db.Column(db.JSON)  # Tool-specific configuration
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    industry = db.relationship('Industry', backref=db.backref('safety_tools', lazy=True))
    creator = db.relationship('User', backref=db.backref('created_tools', lazy=True))

class IncidentAttachment(db.Model):
    __tablename__ = 'incident_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id', ondelete='CASCADE'), nullable=False)
    upload_file_id = db.Column(db.Integer, nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255))
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    file_type = db.Column(db.String(100))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    extra_data = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - FIXED: Use unique backref name
    incident = db.relationship('Incident', backref=db.backref('incident_attachments', lazy=True, cascade='all, delete-orphan'))
    uploader = db.relationship('User', backref=db.backref('uploaded_attachments', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'incident_id': self.incident_id,
            'upload_file_id': self.upload_file_id,
            'filename': self.filename,
            'stored_filename': self.stored_filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_size_formatted': self.format_file_size(),
            'mime_type': self.mime_type,
            'file_type': self.file_type or self.get_file_category(),
            'file_extension': self.get_file_extension(),
            'uploaded_by': self.uploaded_by,
            'uploaded_by_name': self.uploader.name if self.uploader else None,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'description': self.description,
            'extra_data': self.extra_data,
            'download_url': f'/api/attachments/{self.id}/download',
            'preview_url': self.get_preview_url(),
            'is_image': self.mime_type and self.mime_type.startswith('image/'),
            'is_video': self.mime_type and self.mime_type.startswith('video/'),
            'is_document': self.is_document(),
            'is_archive': self.is_archive()
        }
    
    def get_file_extension(self):
        if '.' in self.filename:
            return self.filename.rsplit('.', 1)[1].lower()
        return ''
    
    def get_file_category(self):
        if self.mime_type:
            if self.mime_type.startswith('image/'):
                return 'image'
            elif self.mime_type.startswith('video/'):
                return 'video'
            elif self.mime_type.startswith('audio/'):
                return 'audio'
            elif self.mime_type == 'application/pdf':
                return 'pdf'
            elif self.mime_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                return 'word'
            elif self.mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                return 'excel'
            elif self.mime_type in ['application/zip', 'application/x-rar-compressed']:
                return 'archive'
            elif self.mime_type.startswith('text/'):
                return 'text'
        
        ext = self.get_file_extension()
        image_exts = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg', 'ico'}
        video_exts = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm'}
        document_exts = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'}
        archive_exts = {'zip', 'rar', '7z', 'tar', 'gz'}
        
        if ext in image_exts:
            return 'image'
        elif ext in video_exts:
            return 'video'
        elif ext in document_exts:
            return 'document'
        elif ext in archive_exts:
            return 'archive'
        return 'other'
    
    def is_document(self):
        doc_types = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'text/plain',
            'text/csv'
        ]
        return self.mime_type in doc_types
    
    def is_archive(self):
        archive_types = [
            'application/zip',
            'application/x-zip-compressed',
            'application/x-rar-compressed',
            'application/x-7z-compressed',
            'application/x-tar',
            'application/gzip'
        ]
        return self.mime_type in archive_types or self.get_file_extension() in ['zip', 'rar', '7z', 'tar', 'gz']
    
    def format_file_size(self):
        size = self.file_size or 0
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"
    
    def get_preview_url(self):
        if self.mime_type and self.mime_type.startswith('image/'):
            return f'/api/attachments/{self.id}/preview'
        return None

class IncidentReportLog(db.Model):
    """Log of incident report actions"""
    __tablename__ = 'incident_report_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    plan = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    incident = db.relationship('Incident', backref=db.backref('report_logs', lazy=True, cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('incident_report_logs', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'incident_id': self.incident_id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'action': self.action,
            'details': self.details,
            'plan': self.plan,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class IncidentAction(db.Model):
    __tablename__ = 'incident_actions'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    action_type = db.Column(db.String(100), nullable=False)  # investigation, correction, prevention
    description = db.Column(db.Text, nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='pending')
    completed_date = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    incident = db.relationship('Incident', back_populates='actions')
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    creator = db.relationship('User', foreign_keys=[created_by])

    def to_dict(self):
        return {
        'id': self.id,
        'incident_id': self.incident_id,
        'action_type': self.action_type,
        'description': self.description,
        'assigned_to': self.assigned_to,
        'assignee_name': self.assignee.name if self.assignee else None,
        'due_date': self.due_date.isoformat() if self.due_date else None,
        'status': self.status,
        'completed_date': self.completed_date.isoformat() if self.completed_date else None,
        'created_by': self.created_by,
        'creator_name': self.creator.name if self.creator else None,
        'created_at': self.created_at.isoformat() if self.created_at else None,
        'updated_at': self.updated_at.isoformat() if self.updated_at else None
    }


class NearMiss(db.Model):
    __tablename__ = 'near_misses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    incident_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)  # slip_trip, equipment, chemical, electrical, etc.
    severity_potential = db.Column(db.String(50), nullable=False)  # low, medium, high, critical
    location = db.Column(db.String(255))
    department = db.Column(db.String(100))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_occurred = db.Column(db.DateTime, nullable=False)
    date_reported = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    immediate_cause = db.Column(db.Text)
    root_cause = db.Column(db.Text)
    corrective_actions = db.Column(db.Text)
    status = db.Column(db.String(50), default='reported')  # reported, investigating, closed
    risk_level = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reporter = db.relationship('User', foreign_keys=[reported_by])
    hospital = db.relationship('Hospital', backref=db.backref('near_misses', lazy=True))

class SafetyObservation(db.Model):
    """Safety observations - extended with company isolation and recognition."""
    __tablename__ = 'safety_observations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    observation_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(100), nullable=False)  # safe_behavior, unsafe_condition, positive_observation, at_risk_behavior, near_miss, good_practice, improvement, hazard
    category = db.Column(db.String(100))
    location = db.Column(db.String(255))
    department = db.Column(db.String(100))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    observed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_observed = db.Column(db.DateTime, nullable=False)
    risk_level = db.Column(db.String(50))
    immediate_action = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    status = db.Column(db.String(50), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ✅ NEW columns (add via ALTER TABLE)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    observed_person = db.Column(db.String(255))
    observed_person_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    positive_recognition = db.Column(db.Boolean, default=False)
    points_awarded = db.Column(db.Integer, default=0)
    photos = db.Column(db.Text, default='[]')
    closed_at = db.Column(db.DateTime)
    closed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    observer = db.relationship('User', foreign_keys=[observed_by])
    reporter = db.relationship('User', foreign_keys=[user_id])  # the user who created it
    hospital = db.relationship('Hospital', backref=db.backref('safety_observations', lazy=True))
    
    def to_dict(self):
        try:
            photos_list = json.loads(self.photos) if isinstance(self.photos, str) else (self.photos or [])
        except Exception:
            photos_list = []
        
        return {
            'id': self.id,
            'observation_number': self.observation_number,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            
            # Type (with alias for frontend compatibility)
            'type': self.type,
            'observation_type': self.type,  # alias
            
            'category': self.category,
            'risk_level': self.risk_level,
            
            # Actions
            'immediate_action': self.immediate_action,
            'corrective_action': self.immediate_action,  # alias
            'recommendation': self.recommendation,
            
            # Location
            'location': self.location,
            'department': self.department,
            'hospital_id': self.hospital_id,
            
            # People
            'user_id': self.user_id,
            'observed_by': self.observed_by,
            'observer': {
                'id': self.observer.id,
                'name': self.observer.name,
                'email': self.observer.email,
            } if self.observer else None,
            'observed_person': self.observed_person,
            'observed_person_id': self.observed_person_id,
            
            # Recognition
            'positive_recognition': self.positive_recognition,
            'points_awarded': self.points_awarded,
            
            # Media
            'photos': photos_list,
            
            # Ownership
            'company_id': self.company_id,
            
            # Dates
            'date_observed': self.date_observed.isoformat() if self.date_observed else None,
            'observation_date': self.date_observed.isoformat() if self.date_observed else None,  # alias
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None,
            'closed_by': self.closed_by,
        }
class BiohazardIncident(db.Model):
    __tablename__ = 'biohazard_incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    department_id = db.Column(db.Integer, db.ForeignKey('hospital_departments.id'), nullable=False)
    incident_type = db.Column(db.String(64))
    pathogen = db.Column(db.String(128))
    severity = db.Column(db.String(32))
    description = db.Column(db.Text)
    action_taken = db.Column(db.Text)
    follow_up_required = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reported_by = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ===== PERMIT MANAGEMENT =====

class Permit(db.Model):
    __tablename__ = 'permits'
    
    id = db.Column(db.Integer, primary_key=True)
    permit_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    permit_type = db.Column(db.String(100), nullable=False)  # hot_work, confined_space, electrical, etc.
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255), nullable=False)
    work_details = db.Column(db.Text)
    applicant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department = db.Column(db.String(100))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='draft')  # draft, submitted, approved, rejected, active, expired, closed
    risk_level = db.Column(db.String(50))  # low, medium, high, critical
    required_ppe = db.Column(db.Text)  # JSON array
    safety_precautions = db.Column(db.Text)
    emergency_procedures = db.Column(db.Text)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    rejection_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applicant = db.relationship('User', foreign_keys=[applicant_id])
    approver = db.relationship('User', foreign_keys=[approved_by])
    reviews = db.relationship('PermitReview', back_populates='permit', cascade='all, delete-orphan')

class PermitReview(db.Model):
    __tablename__ = 'permit_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    permit_id = db.Column(db.Integer, db.ForeignKey('permits.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    review_type = db.Column(db.String(50), nullable=False)  # safety, technical, environmental
    status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
    comments = db.Column(db.Text)
    reviewed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    permit = db.relationship('Permit', back_populates='reviews')
    reviewer = db.relationship('User')

# ===== TRAINING MANAGEMENT =====

class Training(db.Model):
    __tablename__ = 'trainings'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)  # safety, technical, compliance, soft_skills
    duration_minutes = db.Column(db.Integer, nullable=False)
    validity_months = db.Column(db.Integer)  # How long certification is valid
    is_required = db.Column(db.Boolean, default=False)
    required_roles = db.Column(db.Text)  # JSON array of roles that require this training
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    
    # ✅ Add project_id
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by])
    sessions = db.relationship('TrainingSession', back_populates='training', cascade='all, delete-orphan')
    records = db.relationship('TrainingRecord', back_populates='training', cascade='all, delete-orphan')
    
    # ✅ Add project relationship
    project = db.relationship('Project', back_populates='trainings')
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'duration_minutes': self.duration_minutes,
            'validity_months': self.validity_months,
            'is_required': self.is_required,
            'required_roles': json.loads(self.required_roles) if self.required_roles else [],
            'company_id': self.company_id,
            'project_id': self.project_id,  # ✅ ADD THIS
            'project_name': self.project.name if self.project else None,  # ✅ ADD THIS
            'created_by': self.created_by,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
class TrainingSession(db.Model):
    __tablename__ = 'training_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=False)
    session_code = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location = db.Column(db.String(255))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    max_attendees = db.Column(db.Integer)
    status = db.Column(db.String(50), default='scheduled')
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    training = db.relationship('Training', back_populates='sessions')
    instructor = db.relationship('User', foreign_keys=[instructor_id])
    creator = db.relationship('User', foreign_keys=[created_by])
    attendees = db.relationship('TrainingRecord', back_populates='session', cascade='all, delete-orphan')
    
    # ✅ FIX: Use back_populates instead of backref
    project = db.relationship('Project', back_populates='training_sessions_rel')
    company = db.relationship('Company', backref='training_sessions')

class TrainingRecord(db.Model):
    __tablename__ = 'training_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('training_sessions.id'))
    completion_date = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Float)
    status = db.Column(db.String(50), default='completed')
    certificate_url = db.Column(db.String(500))
    next_due_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='training_records')
    training = db.relationship('Training', back_populates='records')
    session = db.relationship('TrainingSession', back_populates='attendees')
    
    # ✅ Use back_populates with unique name
    project = db.relationship('Project', back_populates='training_records')
    company = db.relationship('Company', backref='training_records')

class SafetyTraining(db.Model):
    __tablename__ = 'safety_trainings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    assigned_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='assigned')
    score = db.Column(db.Float)
    certificate_url = db.Column(db.String(500))
    training_hours = db.Column(db.Float)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  
    # Relationships
    user = db.relationship('User', backref=db.backref('safety_trainings', lazy=True))
    training_master = db.relationship('Training', foreign_keys=[training_id])
    
    # ✅ Use back_populates with unique name
    project = db.relationship('Project', back_populates='safety_trainings')
    company = db.relationship('Company', backref='safety_trainings')

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    task_number = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='todo')  # todo, in_progress, review, done
    priority = db.Column(db.String(50), default='medium')
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    due_date = db.Column(db.DateTime)
    estimated_hours = db.Column(db.Float)
    actual_hours = db.Column(db.Float)
    completion_date = db.Column(db.DateTime)
    progress = db.Column(db.Float, default=0)  # 0-100
    
    # ✅ Add company_id if not already present
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', back_populates='tasks')
    assigned_to = db.relationship('User', back_populates='assigned_tasks', foreign_keys=[assigned_to_id])
    creator = db.relationship('User', foreign_keys=[created_by])
    company = db.relationship('Company', backref='tasks')

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    project_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='planning')
    priority = db.Column(db.String(50), default='medium')
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    actual_end_date = db.Column(db.DateTime)
    budget = db.Column(db.Numeric(12, 2))
    actual_cost = db.Column(db.Numeric(12, 2))
    department = db.Column(db.String(100))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    
    file_path = db.Column(db.String(256))
    file_size = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    completed_at = db.Column(db.DateTime)
    industry = db.Column(db.String(64))
    tags = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    created_by_user = db.relationship('User', foreign_keys=[created_by], backref=db.backref('created_projects', lazy=True))
    project_manager = db.relationship('User', foreign_keys=[project_manager_id])
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('uploaded_projects', lazy=True))
    tasks = db.relationship('Task', back_populates='project', cascade='all, delete-orphan')
    milestones = db.relationship('Milestone', back_populates='project', cascade='all, delete-orphan')
    company = db.relationship('Company', back_populates='projects')
    
    # PowerBI/Analytics relationships - ALL WITH UNIQUE NAMES
    manpower_rel = db.relationship('Manpower', back_populates='project')
    lti_rel = db.relationship('LTI', back_populates='project')
    manhours_rel = db.relationship('ManHours', back_populates='project')
    observations_rel = db.relationship('Observation', back_populates='project')
    severity_rel = db.relationship('Severity', back_populates='project')
    injuries_rel = db.relationship('Injury', back_populates='project')
    overdue_reports_rel = db.relationship('OverdueReport', back_populates='project')
    accidents_rel = db.relationship('Accident', back_populates='project')
    
    # ✅ FIX: Use unique name for incidents
    incidents_rel = db.relationship('Incident', back_populates='project')
    
    # Training relationships
    trainings = db.relationship('Training', back_populates='project')
    training_sessions_rel = db.relationship('TrainingSession', back_populates='project')
    training_records = db.relationship('TrainingRecord', back_populates='project')
    safety_trainings = db.relationship('SafetyTraining', back_populates='project')
    
    # KPI relationships
    safety_kpi_records = db.relationship('SafetyKPI', back_populates='project')
    safety_kpi_measurements = db.relationship('SafetyKPIMeasurement', back_populates='project')
    
    # Severity settings
    observation_severity_settings = db.relationship('ObservationSeverity', back_populates='project')
    
class Milestone(db.Model):
    __tablename__ = 'milestones'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=False)
    completed_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='pending')  # pending, achieved, delayed
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', back_populates='milestones')

class ProjectPhase(db.Model):
    __tablename__ = 'project_phases'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(32), default='not_started')
    sequence = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    progress = db.Column(db.Float, default=0)
    dependencies = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref='phases')

class ProjectTask(db.Model):
    __tablename__ = 'project_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    phase_id = db.Column(db.Integer, db.ForeignKey('project_phases.id'))
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(32), default='todo')
    priority = db.Column(db.String(32), default='medium')
    due_date = db.Column(db.DateTime)
    estimated_hours = db.Column(db.Float)
    actual_hours = db.Column(db.Float)
    completion_date = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref='project_tasks')
    phase = db.relationship('ProjectPhase', backref='tasks')
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    creator = db.relationship('User', foreign_keys=[created_by])

class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False, index=True)
    permission_key = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint to prevent duplicates
    __table_args__ = (
        db.UniqueConstraint('role', 'permission_key', name='unique_role_permission'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'permission_key': self.permission_key,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Role(db.Model):
    """Pre-defined roles in the system"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    label = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(20), default='employee')  # 'admin' or 'employee'
    description = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user_roles = db.relationship('UserRole', back_populates='role', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'label': self.label,
            'level': self.level,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class UserRole(db.Model):
    """User to Role mapping"""
    __tablename__ = 'user_roles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, index=True)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='user_roles')
    role = db.relationship('Role', back_populates='user_roles')
    assigner = db.relationship('User', foreign_keys=[assigned_by])
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'role_id', name='unique_user_role'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role_id': self.role_id,
            'role_name': self.role.name if self.role else None,
            'assigned_by': self.assigned_by,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None
        }

class ManualPayment(db.Model):
    __tablename__ = 'manual_payments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # ✅ Payment Reference (Unique)
    payment_reference = db.Column(db.String(100), unique=True, nullable=False)
    
    # ✅ Transaction Details
    transaction_id = db.Column(db.String(100), nullable=True)
    payment_method = db.Column(db.String(50), nullable=False)  # bank_transfer, mobile_money, wire_transfer
    
    # ✅ Payment Details
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='USD')
    plan = db.Column(db.String(50), nullable=False)  # basic, pro, enterprise, custom
    
    # ✅ Status Tracking
    status = db.Column(db.String(50), default='pending_verification')  # pending_verification, verified, rejected, expired
    duration = db.Column(db.String(20), default='1_month') 
    # ✅ Admin Fields
    admin_notes = db.Column(db.Text, nullable=True)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    rejected_at = db.Column(db.DateTime, nullable=True)
    
    # ✅ User Submitted Data
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_notes = db.Column(db.Text, nullable=True)  # User's notes about the payment
    
    # ✅ Expiry
    expires_at = db.Column(db.DateTime, nullable=True)  # Payment verification expiry (e.g., 7 days)
    
    # ✅ Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ✅ Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='manual_payments')
    verifier = db.relationship('User', foreign_keys=[verified_by])
    
    def to_dict(self):
        """Convert manual payment to dictionary"""
        return {
            'id': self.id,
            'payment_reference': self.payment_reference,
            'transaction_id': self.transaction_id,
            'payment_method': self.payment_method,
            'amount': self.amount,
            'currency': self.currency,
            'plan': self.plan,
            'duration': self.duration,
            'status': self.status,
            'admin_notes': self.admin_notes,
            'verified_by': self.verified_by,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'rejection_reason': self.rejection_reason,
            'rejected_at': self.rejected_at.isoformat() if self.rejected_at else None,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'user_notes': self.user_notes,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user': {
                'id': self.user.id,
                'name': self.user.name,
                'email': self.user.email
            } if self.user else None,
            'verifier': {
                'id': self.verifier.id,
                'name': self.verifier.name,
                'email': self.verifier.email
            } if self.verifier else None
        }
    
    def is_expired(self):
        """Check if payment verification has expired"""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    def can_verify(self):
        """Check if payment can be verified"""
        return self.status == 'pending_verification' and not self.is_expired()
    
    def verify(self, verifier_id):
        """Verify the payment"""
        self.status = 'verified'
        self.verified_by = verifier_id
        self.verified_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def reject(self, verifier_id, reason):
        """Reject the payment"""
        self.status = 'rejected'
        self.verified_by = verifier_id
        self.rejected_at = datetime.utcnow()
        self.rejection_reason = reason
        self.updated_at = datetime.utcnow()
        db.session.commit()

        # ==================== COMPLIANCE RECORD MODEL ====================

# ==================== COMPLIANCE RECORD MODEL ====================

class ComplianceRecord(db.Model):
    """Compliance records for tracking regulatory compliance"""
    __tablename__ = 'compliance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    
    # Basic info
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), default='general')
    
    # Compliance metrics
    score = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='pending')  # pending, completed, approved, rejected
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    
    # Dates
    due_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    submitted_at = db.Column(db.DateTime)
    
    # AI features
    ai_reviewed = db.Column(db.Boolean, default=False)
    ai_confidence = db.Column(db.Float, default=0.0)
    ai_suggestions = db.Column(db.Text)
    
    # ✅ FIXED: Renamed 'metadata' to 'extra_data'
    extra_data = db.Column(db.Text)  # JSON data
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='compliance_records')
    company = db.relationship('Company', foreign_keys=[company_id], backref='compliance_records')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'score': self.score,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'ai_reviewed': self.ai_reviewed,
            'ai_confidence': self.ai_confidence,
            'ai_suggestions': self.ai_suggestions,
            'extra_data': self.extra_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# ==================== ENVIRONMENTAL SCORE MODEL ====================

class EnvironmentalScore(db.Model):
    """Environmental impact scores"""
    __tablename__ = 'environmental_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    
    # Category and score
    category = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)
    target_score = db.Column(db.Integer, default=90)
    
    # Trend and impact
    trend = db.Column(db.String(20), default='stable')  # improving, stable, declining
    impact_level = db.Column(db.String(20), default='medium')  # low, medium, high
    
    # Description
    description = db.Column(db.Text)
    
    # AI features
    ai_confidence = db.Column(db.Float, default=0.85)
    ai_prediction = db.Column(db.Text)
    ai_recommendations = db.Column(db.Text)
    
    # ✅ FIXED: Renamed 'metadata' to 'extra_data'
    extra_data = db.Column(db.Text)  # JSON data
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='environmental_scores')
    company = db.relationship('Company', foreign_keys=[company_id], backref='environmental_scores')
    
    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'score': self.score,
            'target_score': self.target_score,
            'trend': self.trend,
            'impact_level': self.impact_level,
            'description': self.description,
            'ai_confidence': self.ai_confidence,
            'ai_prediction': self.ai_prediction,
            'extra_data': self.extra_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# ==================== ENVIRONMENTAL INITIATIVE MODEL ====================

class EnvironmentalInitiative(db.Model):
    """Environmental initiatives (used by scorecard)"""
    __tablename__ = 'environmental_initiatives'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    
    # Initiative details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    
    # Status
    status = db.Column(db.String(20), default='planned')  # planned, in_progress, completed, paused
    priority = db.Column(db.String(20), default='medium')
    
    # Metrics
    estimated_impact = db.Column(db.String(50))
    estimated_cost = db.Column(db.String(50))
    
    # Dates
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='environmental_initiatives')
    company = db.relationship('Company', foreign_keys=[company_id], backref='environmental_initiatives')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'status': self.status,
            'priority': self.priority,
            'estimated_impact': self.estimated_impact,
            'estimated_cost': self.estimated_cost,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# ==================== ENVIRONMENTAL METRIC MODEL ====================

class EnvironmentalMetric(db.Model):
    """Environmental metrics data (used by scorecard)"""
    __tablename__ = 'environmental_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    
    # Metric details
    metric_type = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    value = db.Column(db.Float, default=0)
    unit = db.Column(db.String(20))
    
    # Context
    location = db.Column(db.String(200))
    source = db.Column(db.String(100))
    
    # Thresholds
    threshold_min = db.Column(db.Float)
    threshold_max = db.Column(db.Float)
    is_alert = db.Column(db.Boolean, default=False)
    
    # Timestamps
    measured_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='environmental_metrics')
    company = db.relationship('Company', foreign_keys=[company_id], backref='environmental_metrics')
    
    def to_dict(self):
        return {
            'id': self.id,
            'metric_type': self.metric_type,
            'category': self.category,
            'value': self.value,
            'unit': self.unit,
            'location': self.location,
            'source': self.source,
            'threshold_min': self.threshold_min,
            'threshold_max': self.threshold_max,
            'is_alert': self.is_alert,
            'measured_at': self.measured_at.isoformat() if self.measured_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserEngagementEvent(db.Model):
    """Track user engagement events in real-time"""
    __tablename__ = 'user_engagement_events'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    event_type = db.Column(db.String(50), nullable=False)  # login, analysis, chat, view, share, export, etc.
    session_id = db.Column(db.String(128), nullable=True, index=True)
    # ❌ Rename 'metadata' to avoid conflict with SQLAlchemy reserved attribute
    event_data = db.Column(db.Text, nullable=True)  # JSON string with additional data (was 'metadata')
    duration_seconds = db.Column(db.Integer, default=0)
    ip_address = db.Column(db.String(64), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    hospital = db.relationship('Hospital', backref='engagement_events')
    user = db.relationship('User', backref='engagement_events')
    
    def to_dict(self):
        return {
            'id': self.id,
            'hospital_id': self.hospital_id,
            'user_id': self.user_id,
            'event_type': self.event_type,
            'session_id': self.session_id,
            'event_data': json.loads(self.event_data) if self.event_data else {},
            'duration_seconds': self.duration_seconds,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    @staticmethod
    def track_event(hospital_id, user_id, event_type, event_data=None, duration_seconds=0, session_id=None, ip_address=None, user_agent=None):
        """Track a user engagement event"""
        event = UserEngagementEvent(
            hospital_id=hospital_id,
            user_id=user_id,
            event_type=event_type,
            session_id=session_id,
            event_data=json.dumps(event_data) if event_data else None,
            duration_seconds=duration_seconds,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.utcnow()
        )
        db.session.add(event)
        db.session.commit()
        return event
    
    @staticmethod
    def get_engagement_stats(hospital_id, days=30, event_type=None):
        """Get engagement statistics for a hospital"""
        from datetime import timedelta
        from sqlalchemy import func
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = UserEngagementEvent.query.filter(
            UserEngagementEvent.hospital_id == hospital_id,
            UserEngagementEvent.created_at >= start_date
        )
        
        if event_type:
            query = query.filter(UserEngagementEvent.event_type == event_type)
        
        # Total events
        total_events = query.count()
        
        # Unique users
        unique_users = query.distinct(UserEngagementEvent.user_id).count()
        
        # Events by type
        events_by_type = db.session.query(
            UserEngagementEvent.event_type,
            func.count(UserEngagementEvent.id)
        ).filter(
            UserEngagementEvent.hospital_id == hospital_id,
            UserEngagementEvent.created_at >= start_date
        ).group_by(UserEngagementEvent.event_type).all()
        
        # Events by day
        events_by_day = db.session.query(
            func.date(UserEngagementEvent.created_at).label('date'),
            func.count(UserEngagementEvent.id).label('count')
        ).filter(
            UserEngagementEvent.hospital_id == hospital_id,
            UserEngagementEvent.created_at >= start_date
        ).group_by('date').order_by('date').all()
        
        return {
            'period_days': days,
            'total_events': total_events,
            'unique_users': unique_users,
            'events_by_type': {e[0]: e[1] for e in events_by_type},
            'events_by_day': [{'date': str(e[0]), 'count': e[1]} for e in events_by_day],
            'avg_events_per_user': round(total_events / unique_users, 1) if unique_users > 0 else 0
        }

class UserEngagementScore(db.Model):
    """Cached user engagement scores"""
    __tablename__ = 'user_engagement_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False, index=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    
    engagement_score = db.Column(db.Integer, default=0)  # 0-100
    sessions_count = db.Column(db.Integer, default=0)
    analyses_count = db.Column(db.Integer, default=0)
    chats_count = db.Column(db.Integer, default=0)
    last_active_days = db.Column(db.Integer, default=0)
    level = db.Column(db.String(20), default='low')  # low, medium, high
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='engagement_score')
    hospital = db.relationship('Hospital', backref='engagement_scores')
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'hospital_id': self.hospital_id,
            'engagement_score': self.engagement_score,
            'sessions_count': self.sessions_count,
            'analyses_count': self.analyses_count,
            'chats_count': self.chats_count,
            'last_active_days': self.last_active_days,
            'level': self.level,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def update_score(user_id, hospital_id):
        """Update or create engagement score for a user"""
        from sqlalchemy import func
        from models import User, MedicalAnalysis, UserSession
        
        # Get user data
        user = User.query.get(user_id)
        if not user:
            return None
        
        # Calculate sessions count
        sessions_count = UserSession.query.filter_by(user_id=user_id, is_active=True).count()
        
        # Calculate analyses count
        analyses_count = MedicalAnalysis.query.filter_by(user_id=user_id).count()
        
        # Calculate chats count
        chats_count = MedicalAnalysis.query.filter_by(user_id=user_id, analysis_type='chat').count()
        
        # Calculate last active days
        last_active = user.last_login or user.created_at
        last_active_days = (datetime.utcnow() - last_active).days
        
        # Calculate engagement score (0-100)
        score = min(100, int(
            (sessions_count * 2) +  # 20% weight (max 10 sessions = 20 points)
            (analyses_count * 3) +  # 30% weight (max 10 analyses = 30 points)
            (chats_count * 2) +     # 20% weight (max 10 chats = 20 points)
            (50 if last_active_days < 7 else 0)  # 30% weight
        ))
        
        # Determine level
        if score > 70:
            level = 'high'
        elif score > 40:
            level = 'medium'
        else:
            level = 'low'
        
        # Update or create score record
        score_record = UserEngagementScore.query.filter_by(user_id=user_id).first()
        
        if score_record:
            score_record.engagement_score = score
            score_record.sessions_count = sessions_count
            score_record.analyses_count = analyses_count
            score_record.chats_count = chats_count
            score_record.last_active_days = last_active_days
            score_record.level = level
            score_record.updated_at = datetime.utcnow()
        else:
            score_record = UserEngagementScore(
                user_id=user_id,
                hospital_id=hospital_id,
                engagement_score=score,
                sessions_count=sessions_count,
                analyses_count=analyses_count,
                chats_count=chats_count,
                last_active_days=last_active_days,
                level=level
            )
            db.session.add(score_record)
        
        db.session.commit()
        return score_record

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    specialty = db.Column(db.String(128))
    department = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patients = db.relationship('Patient', back_populates='doctor', foreign_keys='Patient.doctor_id', lazy=True)
    hospital = db.relationship('Hospital', foreign_keys=[hospital_id], backref='doctors', lazy=True)
    
    def __init__(self, **kwargs):
        super(Doctor, self).__init__(**kwargs)
        if 'password' in kwargs:
            self.set_password(kwargs['password'])
    
    def set_password(self, password):
        """Hash and set the password"""
        if not password or len(password) < 8:
            raise ValueError('Password must be at least 8 characters')
        # ✅ Use bcrypt directly
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def generate_auth_token(self):
        """Generate JWT token for doctor"""
        additional_claims = {
            'user_type': 'doctor',
            'hospital_id': self.hospital_id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'employee_id': self.employee_id
        }
        return create_access_token(identity=self.id, additional_claims=additional_claims)
    
    def generate_refresh_token(self):
        """Generate refresh token"""
        return create_refresh_token(identity=self.id)
    
    def to_dict(self):
        return {
            'id': self.id,
            'hospital_id': self.hospital_id,
            'employee_id': self.employee_id,
            'email': self.email,
            'name': self.name,
            'specialty': self.specialty,
            'department': self.department,
            'phone': self.phone,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'patient_count': len(self.patients) if self.patients else 0
        }


class SafetyIncident(db.Model):
    __tablename__ = 'safety_incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(20), default='Medium')
    department = db.Column(db.String(128))
    location = db.Column(db.String(255))
    status = db.Column(db.String(20), default='Reported')
    date = db.Column(db.DateTime, default=datetime.utcnow)
    investigator = db.Column(db.String(128))
    description = db.Column(db.Text)
    root_cause = db.Column(db.Text)
    corrective_actions = db.Column(db.Text)
    preventive_measures = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)

# ============================================================
# DOCUMENT CONTROL SYSTEM MODELS
# ============================================================

class DocumentVersion(db.Model):
    __tablename__ = 'document_versions'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False, index=True)
    version = db.Column(db.Integer, nullable=False)
    
    file_name = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    file_url = db.Column(db.String(500))
    file_hash = db.Column(db.String(255))
    changes = db.Column(db.Text)
    is_current = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # ============================================================
    # RELATIONSHIPS - FIXED (USE THE BACKREF FROM DOCUMENT)
    # ============================================================
    # This uses the backref 'doc_version' from Document.versions
    # DO NOT define another backref here
    document = db.relationship('Document', foreign_keys=[document_id], back_populates='versions')
    creator = db.relationship('User', foreign_keys=[created_by])
    
    __table_args__ = (
        db.UniqueConstraint('document_id', 'version', name='uq_document_version'),
        db.Index('idx_doc_versions_document', 'document_id'),
        db.Index('idx_doc_versions_created', 'created_at'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'version': self.version,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'file_url': self.file_url,
            'changes': self.changes,
            'is_current': self.is_current,
            'is_approved': self.is_approved,
            'created_by': self.created_by,
            'created_by_name': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DocumentMetadata(db.Model):
    __tablename__ = 'document_metadata'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False, index=True)
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ============================================================
    # RELATIONSHIPS - FIXED
    # ============================================================
    document = db.relationship('Document', foreign_keys=[document_id], back_populates='metadata_items')
    
    __table_args__ = (
        db.UniqueConstraint('document_id', 'key', name='uq_document_metadata'),
    )


class DocumentComment(db.Model):
    __tablename__ = 'document_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('document_comments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    content = db.Column(db.Text, nullable=False)
    is_private = db.Column(db.Boolean, default=False)
    is_archived = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ============================================================
    # RELATIONSHIPS - FIXED
    # ============================================================
    document = db.relationship('Document', foreign_keys=[document_id], back_populates='comment_items')
    user = db.relationship('User', foreign_keys=[user_id])
    replies = db.relationship('DocumentComment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    
    __table_args__ = (
        db.Index('idx_doc_comments_document', 'document_id'),
        db.Index('idx_doc_comments_user', 'user_id'),
        db.Index('idx_doc_comments_created', 'created_at'),
    )

class DocumentAuditLog(db.Model):
    __tablename__ = 'document_audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    action = db.Column(db.String(50), nullable=False)
    details = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # ============================================================
    # RELATIONSHIPS
    # ============================================================
    document = db.relationship('Document', foreign_keys=[document_id], back_populates='audit_logs')
    user = db.relationship('User', foreign_keys=[user_id])
    
    __table_args__ = (
        db.Index('idx_doc_audit_document', 'document_id'),
        db.Index('idx_doc_audit_user', 'user_id'),
        db.Index('idx_doc_audit_action', 'action'),
        db.Index('idx_doc_audit_created', 'created_at'),
    )
    
    def to_dict(self):
        """Convert audit log to dictionary"""
        return {
            'id': self.id,
            'document_id': self.document_id,
            'user_id': self.user_id,
            'action': self.action,
            'details': self.details,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_name': self.user.name if self.user else None,
            'document_title': self.document.title if self.document else None,
        }
    
    @classmethod
    def create_log(cls, document_id, user_id, action, details=None, ip_address=None, user_agent=None):
        """Helper method to create an audit log entry with integer ID"""
        # ✅ Generate integer ID
        audit_id = int(time.time() * 1000000) + random.randint(1000, 9999)
        
        # ✅ Ensure IDs are integers
        if isinstance(document_id, str) and document_id.isdigit():
            document_id = int(document_id)
        if isinstance(user_id, str) and user_id.isdigit():
            user_id = int(user_id)
        
        # ✅ Handle details
        if details and not isinstance(details, dict):
            try:
                details = json.loads(details) if isinstance(details, str) else {'data': str(details)}
            except json.JSONDecodeError:
                details = {'message': str(details)}
        
        audit_log = cls(
            id=audit_id,
            document_id=document_id,
            user_id=user_id,
            action=action,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.utcnow()
        )
        
        return audit_log


class DocumentLink(db.Model):
    __tablename__ = 'document_links'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False, index=True)
    target_type = db.Column(db.String(50), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    link_type = db.Column(db.String(50), default='related')
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # ============================================================
    # RELATIONSHIPS - FIXED
    # ============================================================
    document = db.relationship('Document', foreign_keys=[document_id], back_populates='links')
    creator = db.relationship('User', foreign_keys=[created_by])
    
    __table_args__ = (
        db.UniqueConstraint('document_id', 'target_type', 'target_id', name='uq_document_link'),
        db.Index('idx_doc_links_target', 'target_type', 'target_id'),
    )


class ReviewHistory(db.Model):
    __tablename__ = 'review_history'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False, index=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    action = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text)
    previous_review_date = db.Column(db.DateTime)
    new_review_date = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # ============================================================
    # RELATIONSHIPS - FIXED
    # ============================================================
    document = db.relationship('Document', foreign_keys=[document_id], back_populates='review_history_items')
    reviewer = db.relationship('User', foreign_keys=[reviewer_id])
    
    __table_args__ = (
        db.Index('idx_review_history_document', 'document_id'),
        db.Index('idx_review_history_reviewer', 'reviewer_id'),
        db.Index('idx_review_history_created', 'created_at'),
    )


class DocumentSignature(db.Model):
    __tablename__ = 'document_signatures'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False, index=True)
    signed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    signer_email = db.Column(db.String(255))
    signer_name = db.Column(db.String(255))
    signer_ip = db.Column(db.String(45))
    purpose = db.Column(db.String(50), default='approval')
    signature_type = db.Column(db.String(20), default='draw')
    signature_data = db.Column(db.JSON)
    signature_hash = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')
    comment = db.Column(db.Text)
    verified_at = db.Column(db.DateTime)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    verification_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    signed_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    
    # Relationships
    document = db.relationship('Document', foreign_keys=[document_id], back_populates='signatures')
    signer = db.relationship('User', foreign_keys=[signed_by])
    verifier = db.relationship('User', foreign_keys=[verified_by])
    
    __table_args__ = (
        db.Index('idx_doc_signatures_document', 'document_id'),
        db.Index('idx_doc_signatures_signer', 'signed_by'),
        db.Index('idx_doc_signatures_status', 'status'),
    )
    
    # ✅✅✅ ADD THIS METHOD
    def to_dict(self):
        """Convert signature to dictionary"""
        return {
            'id': self.id,
            'document_id': self.document_id,
            'signed_by': self.signed_by,
            'signer_name': self.signer_name,
            'signer_email': self.signer_email,
            'signer_ip': self.signer_ip,
            'purpose': self.purpose,
            'signature_type': self.signature_type,
            'signature_data': self.signature_data,
            'signature_hash': self.signature_hash,
            'status': self.status,
            'comment': self.comment,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'verified_by': self.verified_by,
            'verification_hash': self.verification_hash,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'signed_at': self.signed_at.isoformat() if self.signed_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'signer_name_display': self.signer.name if self.signer else self.signer_name,
            'verified_by_name': self.verifier.name if self.verifier else None
        }


class SignatureVerification(db.Model):
    """Records of signature verifications"""
    __tablename__ = 'signature_verifications'
    
    id = db.Column(db.Integer, primary_key=True)
    signature_id = db.Column(db.Integer, db.ForeignKey('document_signatures.id', ondelete='CASCADE'), nullable=False, index=True)
    
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    verification_type = db.Column(db.String(50))  # qr_code, manual, api
    status = db.Column(db.String(20))  # valid, invalid, revoked
    details = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    signature = db.relationship('DocumentSignature', foreign_keys=[signature_id], backref=db.backref('verifications', lazy='dynamic'))
    verifier = db.relationship('User', foreign_keys=[verified_by])
    
    __table_args__ = (
        db.Index('idx_sig_verifications_signature', 'signature_id'),
        db.Index('idx_sig_verifications_verifier', 'verified_by'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'signature_id': self.signature_id,
            'verified_by': self.verified_by,
            'verifier_name': self.verifier.name if self.verifier else None,
            'verification_type': self.verification_type,
            'status': self.status,
            'details': self.details,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SavedSearch(db.Model):
    """Saved searches for users"""
    __tablename__ = 'saved_searches'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    name = db.Column(db.String(255), nullable=False)
    filters = db.Column(db.JSON, nullable=False)  # Store all search parameters
    is_default = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'name', name='uq_user_search'),
        db.Index('idx_saved_searches_user', 'user_id'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'filters': self.filters,
            'is_default': self.is_default,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class SearchHistory(db.Model):
    """User search history"""
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    term = db.Column(db.String(255), nullable=False)
    filters = db.Column(db.JSON)
    result_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    
    __table_args__ = (
        db.Index('idx_search_history_user', 'user_id'),
        db.Index('idx_search_history_term', 'term'),
        db.Index('idx_search_history_created', 'created_at'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'term': self.term,
            'filters': self.filters,
            'result_count': self.result_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class DocumentWorkflow(db.Model):
    __tablename__ = 'document_workflows'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False, index=True)
    workflow_type = db.Column(db.String(50), nullable=False)
    current_state = db.Column(db.String(50))
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    due_date = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='active')
    
    # ============================================================
    # RELATIONSHIPS - FIXED
    # ============================================================
    document = db.relationship('Document', foreign_keys=[document_id], back_populates='workflows')
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    
    __table_args__ = (
        db.Index('idx_doc_workflows_document', 'document_id'),
        db.Index('idx_doc_workflows_assigned', 'assigned_to'),
        db.Index('idx_doc_workflows_status', 'status'),
    )


# ============================================================
# DOCUMENT TEMPLATE MODELS
# ============================================================

class DocumentTemplate(db.Model):
    __tablename__ = 'document_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    document_type = db.Column(db.String(50), nullable=False)
    module = db.Column(db.String(50), default='general')
    
    # Template content
    template_content = db.Column(db.Text)
    template_variables = db.Column(db.JSON)
    preview_image = db.Column(db.String(500))
    
    # Settings
    is_public = db.Column(db.Boolean, default=False)
    is_system = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    usage_count = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0)
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = db.relationship('Company', foreign_keys=[company_id])
    creator = db.relationship('User', foreign_keys=[created_by])
    categories = db.relationship('TemplateCategory', secondary='template_category_mapping')


class TemplateCategory(db.Model):
    __tablename__ = 'template_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    color = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'color': self.color,
            'is_active': self.is_active
        }


class TemplateCategoryMapping(db.Model):
    __tablename__ = 'template_category_mapping'
    
    template_id = db.Column(db.Integer, db.ForeignKey('document_templates.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('template_categories.id'), primary_key=True)



# ============================================================
# APPROVAL CHAIN MODELS
# ============================================================

class ApprovalChain(db.Model):
    __tablename__ = 'approval_chains'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    document_type = db.Column(db.String(50))
    module = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = db.relationship('Company', foreign_keys=[company_id])
    creator = db.relationship('User', foreign_keys=[created_by])
    steps = db.relationship('ApprovalStep', back_populates='chain', cascade='all, delete-orphan')
    approvals = db.relationship('DocumentApproval', back_populates='chain')
    
    __table_args__ = (
        db.Index('idx_approval_chains_company', 'company_id'),
        db.Index('idx_approval_chains_active', 'is_active'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'document_type': self.document_type,
            'module': self.module,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_by_name': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'steps': [step.to_dict() for step in self.steps] if self.steps else [],
            'steps_count': len(self.steps) if self.steps else 0
        }


class ApprovalStep(db.Model):
    __tablename__ = 'approval_steps'
    
    id = db.Column(db.Integer, primary_key=True)
    chain_id = db.Column(db.Integer, db.ForeignKey('approval_chains.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Approval type
    approval_type = db.Column(db.String(50), default='sequential')
    
    # Assignee
    assignee_type = db.Column(db.String(50), default='role')
    assignee_id = db.Column(db.Integer)
    assignee_name = db.Column(db.String(255))
    
    # Settings
    requires_comment = db.Column(db.Boolean, default=False)
    timeout_days = db.Column(db.Integer, default=7)
    escalation_days = db.Column(db.Integer)
    escalation_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_mandatory = db.Column(db.Boolean, default=True)
    
    # Conditions
    condition_type = db.Column(db.String(50))
    condition_value = db.Column(db.Text)
    can_skip = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chain = db.relationship('ApprovalChain', back_populates='steps')
    escalation_user = db.relationship('User', foreign_keys=[escalation_user_id])
    approvals = db.relationship('ApprovalStepStatus', back_populates='step')
    
    __table_args__ = (
        db.Index('idx_approval_steps_chain', 'chain_id'),
        db.UniqueConstraint('chain_id', 'step_number', name='uq_step_number'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'chain_id': self.chain_id,
            'step_number': self.step_number,
            'name': self.name,
            'description': self.description,
            'approval_type': self.approval_type,
            'assignee_type': self.assignee_type,
            'assignee_id': self.assignee_id,
            'assignee_name': self.assignee_name,
            'requires_comment': self.requires_comment,
            'timeout_days': self.timeout_days,
            'escalation_days': self.escalation_days,
            'escalation_user_id': self.escalation_user_id,
            'escalation_user_name': self.escalation_user.name if self.escalation_user else None,
            'is_mandatory': self.is_mandatory,
            'condition_type': self.condition_type,
            'condition_value': self.condition_value
        }


class DocumentApproval(db.Model):
    __tablename__ = 'document_approvals'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    chain_id = db.Column(db.Integer, db.ForeignKey('approval_chains.id'), nullable=False)
    
    status = db.Column(db.String(20), default='pending')
    current_step = db.Column(db.Integer, default=0)
    
    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    approved_at = db.Column(db.DateTime)
    rejected_at = db.Column(db.DateTime)
    
    # Metadata
    submitted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    document = db.relationship('Document', backref=db.backref('approval', uselist=False))
    chain = db.relationship('ApprovalChain', back_populates='approvals')
    submitter = db.relationship('User', foreign_keys=[submitted_by])
    step_statuses = db.relationship('ApprovalStepStatus', back_populates='approval', cascade='all, delete-orphan')
    
    __table_args__ = (
        db.Index('idx_doc_approvals_document', 'document_id'),
        db.Index('idx_doc_approvals_status', 'status'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'document_title': self.document.title if self.document else None,
            'chain_id': self.chain_id,
            'chain_name': self.chain.name if self.chain else None,
            'status': self.status,
            'current_step': self.current_step,
            'total_steps': len(self.chain.steps) if self.chain else 0,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'rejected_at': self.rejected_at.isoformat() if self.rejected_at else None,
            'submitted_by': self.submitted_by,
            'submitter_name': self.submitter.name if self.submitter else None,
            'notes': self.notes,
            'step_statuses': [step.to_dict() for step in self.step_statuses] if self.step_statuses else [],
            'progress': self.get_progress(),
            'is_completed': self.status in ['approved', 'rejected', 'cancelled']
        }
    
    def get_progress(self):
        if not self.chain or not self.chain.steps:
            return 0
        total = len(self.chain.steps)
        completed = len([s for s in self.step_statuses if s.status == 'approved'])
        return round((completed / total) * 100) if total > 0 else 0


class ApprovalStepStatus(db.Model):
    __tablename__ = 'approval_step_statuses'
    
    id = db.Column(db.Integer, primary_key=True)
    approval_id = db.Column(db.Integer, db.ForeignKey('document_approvals.id'), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey('approval_steps.id'), nullable=False)
    
    status = db.Column(db.String(20), default='pending')
    comment = db.Column(db.Text)
    
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_to_name = db.Column(db.String(255))
    
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    escalated_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    approval = db.relationship('DocumentApproval', back_populates='step_statuses')
    step = db.relationship('ApprovalStep', back_populates='approvals')
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    
    __table_args__ = (
        db.Index('idx_step_status_approval', 'approval_id'),
        db.Index('idx_step_status_step', 'step_id'),
        db.Index('idx_step_status_status', 'status'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'approval_id': self.approval_id,
            'step_id': self.step_id,
            'step_name': self.step.name if self.step else None,
            'step_number': self.step.step_number if self.step else None,
            'status': self.status,
            'comment': self.comment,
            'assigned_to': self.assigned_to,
            'assigned_to_name': self.assigned_to_name or (self.assignee.name if self.assignee else None),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'escalated_at': self.escalated_at.isoformat() if self.escalated_at else None,
            'is_pending': self.status == 'pending',
            'is_completed': self.status in ['approved', 'rejected']
        }


# ============================================================
# DOCUMENT EXPIRATION MODELS
# ============================================================

class DocumentExpiration(db.Model):
    __tablename__ = 'document_expirations'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    
    # Expiration settings
    expires_at = db.Column(db.DateTime, nullable=False)
    review_date = db.Column(db.DateTime)
    warning_days = db.Column(db.Integer, default=30)
    
    # Status tracking
    status = db.Column(db.String(20), default='active')  # active, expired, extended, renewed
    
    # Notification tracking
    notifications_sent = db.Column(db.JSON, default=[])
    last_notification_sent = db.Column(db.DateTime)
    
    # Workflow
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    review_notes = db.Column(db.Text)
    extension_reason = db.Column(db.Text)
    new_expiry_date = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    document = db.relationship('Document', foreign_keys=[document_id], backref=db.backref('expiration', uselist=False))
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    
    __table_args__ = (
        db.Index('idx_expiration_document', 'document_id'),
        db.Index('idx_expiration_status', 'status'),
        db.Index('idx_expiration_date', 'expires_at'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'document_title': self.document.title if self.document else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'review_date': self.review_date.isoformat() if self.review_date else None,
            'warning_days': self.warning_days,
            'status': self.status,
            'notifications_sent': self.notifications_sent,
            'last_notification_sent': self.last_notification_sent.isoformat() if self.last_notification_sent else None,
            'assigned_to': self.assigned_to,
            'assignee_name': self.assignee.name if self.assignee else None,
            'review_notes': self.review_notes,
            'extension_reason': self.extension_reason,
            'new_expiry_date': self.new_expiry_date.isoformat() if self.new_expiry_date else None,
            'days_until_expiry': self.get_days_until_expiry(),
            'is_expired': self.is_expired(),
            'is_expiring_soon': self.is_expiring_soon(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def get_days_until_expiry(self):
        if not self.expires_at:
            return None
        now = datetime.utcnow()
        delta = self.expires_at - now
        return delta.days
    
    def is_expired(self):
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    def is_expiring_soon(self):
        if not self.expires_at:
            return False
        days = self.get_days_until_expiry()
        if days is None:
            return False
        return 0 < days <= self.warning_days
    
    def get_status_display(self):
        if self.is_expired():
            return 'Expired'
        elif self.is_expiring_soon():
            return 'Expiring Soon'
        elif self.status == 'extended':
            return 'Extended'
        elif self.status == 'renewed':
            return 'Renewed'
        elif self.status == 'completed':
            return 'Completed'
        else:
            return 'Active'


class ExpirationNotificationLog(db.Model):
    __tablename__ = 'expiration_notification_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    expiration_id = db.Column(db.Integer, db.ForeignKey('document_expirations.id'), nullable=False)
    
    notification_type = db.Column(db.String(50))  # warning, critical, expired, review_reminder
    sent_to = db.Column(db.String(255))
    sent_via = db.Column(db.String(20))  # email, system, push
    subject = db.Column(db.String(255))
    content = db.Column(db.Text)
    status = db.Column(db.String(20), default='sent')  # sent, failed
    
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    expiration = db.relationship('DocumentExpiration', backref=db.backref('notification_logs', lazy='dynamic'))
    
    __table_args__ = (
        db.Index('idx_exp_notification_expiration', 'expiration_id'),
        db.Index('idx_exp_notification_sent_at', 'sent_at'),
    )

class DocumentCategory(db.Model):
    """Document categories for organization and filtering"""
    __tablename__ = 'document_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    color = db.Column(db.String(20))
    
    # Hierarchy (for nested categories)
    parent_id = db.Column(db.Integer, db.ForeignKey('document_categories.id'))
    
    # Settings
    is_active = db.Column(db.Boolean, default=True)
    is_system = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    
    # Company scope (null = global)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    
    # Metadata
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    parent = db.relationship('DocumentCategory', remote_side=[id], backref='children')
    company = db.relationship('Company', foreign_keys=[company_id])
    creator = db.relationship('User', foreign_keys=[created_by])
    
    __table_args__ = (
        db.Index('idx_doc_categories_company', 'company_id'),
        db.Index('idx_doc_categories_parent', 'parent_id'),
        db.Index('idx_doc_categories_active', 'is_active'),
        db.UniqueConstraint('name', 'company_id', name='uq_category_name_company'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'color': self.color,
            'parent_id': self.parent_id,
            'is_active': self.is_active,
            'is_system': self.is_system,
            'sort_order': self.sort_order,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_by_name': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'child_count': len(self.children) if self.children else 0,
            'children': [child.to_dict() for child in self.children] if self.children else []
        }
    
    def get_full_path(self):
        """Get full category path (e.g., 'Safety / PPE / Gloves')"""
        path = [self.name]
        parent = self.parent
        while parent:
            path.insert(0, parent.name)
            parent = parent.parent
        return ' / '.join(path)

# models.py

# ============================================================
# COMPLIANCE FRAMEWORK MODELS
# ============================================================

# models.py

# ============================================================
# COMPLIANCE FRAMEWORK MODELS - FIXED
# ============================================================

class ComplianceFramework(db.Model):
    """Compliance Framework - defines compliance standards and requirements"""
    __tablename__ = 'compliance_frameworks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    version = db.Column(db.String(20))
    category = db.Column(db.String(50))
    
    is_active = db.Column(db.Boolean, default=True)
    is_required = db.Column(db.Boolean, default=False)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ✅ FIXED: Use unique backref names
    company = db.relationship('Company', foreign_keys=[company_id])
    creator = db.relationship('User', foreign_keys=[created_by])
    
    # ✅ Use 'compliance_framework_requirements' as backref
    requirements = db.relationship('ComplianceRequirement', backref='compliance_framework_requirements', lazy='dynamic', cascade='all, delete-orphan')
    
    # ✅ Use 'compliance_framework_links' as backref
    document_links = db.relationship('DocumentComplianceLink', backref='compliance_framework_links', lazy='dynamic', cascade='all, delete-orphan')
    
    __table_args__ = (
        db.Index('idx_compliance_frameworks_code', 'code'),
        db.Index('idx_compliance_frameworks_category', 'category'),
        db.Index('idx_compliance_frameworks_company', 'company_id'),
        db.Index('idx_compliance_frameworks_active', 'is_active'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'version': self.version,
            'category': self.category,
            'is_active': self.is_active,
            'is_required': self.is_required,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_by_name': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'requirements_count': self.requirements.count() if self.requirements else 0,
            'document_links_count': self.document_links.count() if self.document_links else 0
        }


class ComplianceRequirement(db.Model):
    """Individual compliance requirement within a framework"""
    __tablename__ = 'compliance_requirements'
    
    id = db.Column(db.Integer, primary_key=True)
    framework_id = db.Column(db.Integer, db.ForeignKey('compliance_frameworks.id', ondelete='CASCADE'), nullable=False)
    
    requirement_id = db.Column(db.String(50))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    category = db.Column(db.String(50))
    priority = db.Column(db.String(20), default='medium')
    
    is_mandatory = db.Column(db.Boolean, default=True)
    requires_evidence = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ✅ FIXED: Use the same backref name as defined above
    # The backref is 'compliance_framework_requirements' from ComplianceFramework.requirements
    
    __table_args__ = (
        db.Index('idx_compliance_requirements_framework', 'framework_id'),
        db.Index('idx_compliance_requirements_category', 'category'),
        db.Index('idx_compliance_requirements_priority', 'priority'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'framework_id': self.framework_id,
            'requirement_id': self.requirement_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'is_mandatory': self.is_mandatory,
            'requires_evidence': self.requires_evidence,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class DocumentComplianceLink(db.Model):
    """Link between documents and compliance frameworks"""
    __tablename__ = 'document_compliance_links'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False)
    framework_id = db.Column(db.Integer, db.ForeignKey('compliance_frameworks.id', ondelete='CASCADE'), nullable=False)
    
    status = db.Column(db.String(20), default='pending')
    compliance_score = db.Column(db.Integer, default=0)
    target_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    linked_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_checked = db.Column(db.DateTime)
    checked_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ✅ FIXED: Use unique backref names
    document = db.relationship('Document', foreign_keys=[document_id])
    # Use 'compliance_framework_links' as backref (from ComplianceFramework.document_links)
    compliance_framework = db.relationship('ComplianceFramework', foreign_keys=[framework_id])
    
    linker = db.relationship('User', foreign_keys=[linked_by])
    checker = db.relationship('User', foreign_keys=[checked_by])
    
    __table_args__ = (
        db.Index('idx_compliance_links_document', 'document_id'),
        db.Index('idx_compliance_links_framework', 'framework_id'),
        db.Index('idx_compliance_links_status', 'status'),
        db.UniqueConstraint('document_id', 'framework_id', name='uq_doc_framework'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'document_title': self.document.title if self.document else None,
            'framework_id': self.framework_id,
            'framework_name': self.compliance_framework.name if self.compliance_framework else None,
            'framework_code': self.compliance_framework.code if self.compliance_framework else None,
            'status': self.status,
            'compliance_score': self.compliance_score,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'notes': self.notes,
            'linked_by': self.linked_by,
            'linked_by_name': self.linker.name if self.linker else None,
            'last_checked': self.last_checked.isoformat() if self.last_checked else None,
            'checked_by': self.checked_by,
            'checked_by_name': self.checker.name if self.checker else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ComplianceAuditLog(db.Model):
    """Audit log for compliance activities"""
    __tablename__ = 'compliance_audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False)
    framework_id = db.Column(db.Integer, db.ForeignKey('compliance_frameworks.id', ondelete='CASCADE'), nullable=True)
    
    action = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20))
    description = db.Column(db.Text)
    details = db.Column(db.JSON)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    document = db.relationship('Document', foreign_keys=[document_id])
    compliance_framework = db.relationship('ComplianceFramework', foreign_keys=[framework_id])
    user = db.relationship('User', foreign_keys=[user_id])
    
    __table_args__ = (
        db.Index('idx_compliance_audit_document', 'document_id'),
        db.Index('idx_compliance_audit_framework', 'framework_id'),
        db.Index('idx_compliance_audit_action', 'action'),
        db.Index('idx_compliance_audit_created', 'created_at'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'document_title': self.document.title if self.document else None,
            'framework_id': self.framework_id,
            'framework_name': self.compliance_framework.name if self.compliance_framework else None,
            'action': self.action,
            'status': self.status,
            'description': self.description,
            'details': self.details,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DocumentPermission(db.Model):
    """Per-document access control entries"""
    __tablename__ = 'document_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False, index=True)
    
    principal_type = db.Column(db.String(20), nullable=False)  # user/group/role/department/organization/public
    principal_id = db.Column(db.String(100), nullable=False, index=True)
    principal_name = db.Column(db.String(255))
    
    access_level = db.Column(db.String(20), default='view')  # none/view/comment/edit/full
    permissions = db.Column(db.Text, default='[]')  # JSON array
    
    expires_at = db.Column(db.DateTime)
    ip_whitelist = db.Column(db.Text, default='[]')  # JSON array
    notes = db.Column(db.Text)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    granted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    document = db.relationship('Document', foreign_keys=[document_id], backref=db.backref('permissions', lazy='dynamic', cascade='all, delete-orphan'))
    grantor = db.relationship('User', foreign_keys=[granted_by])
    
    __table_args__ = (
        db.Index('idx_doc_perm_doc', 'document_id'),
        db.Index('idx_doc_perm_principal', 'principal_type', 'principal_id'),
        db.Index('idx_doc_perm_company', 'company_id'),
    )
    
    def to_dict(self):
        try:
            perms = json.loads(self.permissions) if isinstance(self.permissions, str) else (self.permissions or [])
        except:
            perms = []
        try:
            ips = json.loads(self.ip_whitelist) if isinstance(self.ip_whitelist, str) else (self.ip_whitelist or [])
        except:
            ips = []
        
        return {
            'id': self.id,
            'document_id': self.document_id,
            'principal_type': self.principal_type,
            'principal_id': self.principal_id,
            'principal_name': self.principal_name,
            'access_level': self.access_level,
            'permissions': perms,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'ip_whitelist': ips,
            'notes': self.notes,
            'company_id': self.company_id,
            'granted_by': self.granted_by,
            'created_by_name': self.grantor.name if self.grantor else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class DocumentSecurity(db.Model):
    """Per-document security settings"""
    __tablename__ = 'document_security'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False, unique=True, index=True)
    
    sensitivity = db.Column(db.String(20), default='internal')  # public/internal/confidential/restricted/top_secret
    masking_rule = db.Column(db.String(20), default='none')  # none/partial/full/custom
    masking_config = db.Column(db.Text, default='{}')
    
    inherit_from_parent = db.Column(db.Boolean, default=True)
    
    download_restricted = db.Column(db.Boolean, default=False)
    print_restricted = db.Column(db.Boolean, default=False)
    watermark_enabled = db.Column(db.Boolean, default=False)
    
    expiry_enabled = db.Column(db.Boolean, default=False)
    expiry_date = db.Column(db.DateTime)
    
    ip_restrictions = db.Column(db.Text, default='[]')
    time_restrictions = db.Column(db.Text, default='{}')
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    document = db.relationship('Document', foreign_keys=[document_id], backref=db.backref('security_settings', uselist=False, cascade='all, delete-orphan'))
    
    def to_dict(self):
        def parse_json(val, default):
            try:
                return json.loads(val) if isinstance(val, str) else (val or default)
            except:
                return default
        
        return {
            'id': self.id,
            'document_id': self.document_id,
            'sensitivity': self.sensitivity,
            'masking_rule': self.masking_rule,
            'masking_config': parse_json(self.masking_config, {}),
            'inherit_from_parent': self.inherit_from_parent,
            'download_restricted': self.download_restricted,
            'print_restricted': self.print_restricted,
            'watermark_enabled': self.watermark_enabled,
            'expiry_enabled': self.expiry_enabled,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'ip_restrictions': parse_json(self.ip_restrictions, []),
            'time_restrictions': parse_json(self.time_restrictions, {}),
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AccessAuditLog(db.Model):
    """Access-specific audit trail"""
    __tablename__ = 'access_audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), index=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    user_name = db.Column(db.String(255))
    user_email = db.Column(db.String(255))
    
    action = db.Column(db.String(50), nullable=False, index=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    actor_name = db.Column(db.String(255))
    description = db.Column(db.Text)
    
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    document = db.relationship('Document', foreign_keys=[document_id])
    user = db.relationship('User', foreign_keys=[user_id])
    actor = db.relationship('User', foreign_keys=[actor_id])
    
    __table_args__ = (
        db.Index('idx_access_audit_doc', 'document_id'),
        db.Index('idx_access_audit_user', 'user_id'),
        db.Index('idx_access_audit_action', 'action'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'document_title': self.document.title if self.document else None,
            'user_id': self.user_id,
            'user_name': self.user_name or (self.user.name if self.user else None),
            'user_email': self.user_email,
            'action': self.action,
            'actor_id': self.actor_id,
            'actor_name': self.actor_name or (self.actor.name if self.actor else None),
            'description': self.description,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ============================================================
# GROUP 2: RETENTION (3 models)
# ============================================================

class RetentionPolicy(db.Model):
    """Retention policy definitions"""
    __tablename__ = 'retention_policies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=True, index=True)
    
    schedule = db.Column(db.String(20), default='years_7')
    custom_days = db.Column(db.Integer)
    regulatory_framework = db.Column(db.String(30))
    retention_start_event = db.Column(db.String(30), default='created_at')
    
    auto_archive = db.Column(db.Boolean, default=True)
    auto_dispose = db.Column(db.Boolean, default=False)
    disposal_method = db.Column(db.String(30), default='secure_delete')
    
    notify_before_days = db.Column(db.Integer, default=30)
    notification_emails = db.Column(db.Text, default='[]')
    require_approval = db.Column(db.Boolean, default=True)
    enable_legal_hold = db.Column(db.Boolean, default=True)
    
    lifecycle_stage = db.Column(db.String(30), default='active')
    notes = db.Column(db.Text)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    document = db.relationship('Document', foreign_keys=[document_id], backref=db.backref('retention_policy', uselist=False))
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        try:
            emails = json.loads(self.notification_emails) if isinstance(self.notification_emails, str) else (self.notification_emails or [])
        except:
            emails = []
        
        return {
            'id': self.id,
            'name': self.name,
            'document_id': self.document_id,
            'schedule': self.schedule,
            'custom_days': self.custom_days,
            'regulatory_framework': self.regulatory_framework,
            'retention_start_event': self.retention_start_event,
            'auto_archive': self.auto_archive,
            'auto_dispose': self.auto_dispose,
            'disposal_method': self.disposal_method,
            'notify_before_days': self.notify_before_days,
            'notification_emails': emails,
            'require_approval': self.require_approval,
            'enable_legal_hold': self.enable_legal_hold,
            'lifecycle_stage': self.lifecycle_stage,
            'notes': self.notes,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class LegalHold(db.Model):
    """Legal holds preventing disposal"""
    __tablename__ = 'legal_holds'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # ⚠️ KEEP JSON for backward compat AND fast "list all doc IDs"
    document_ids = db.Column(db.Text, default='[]')
    document_count = db.Column(db.Integer, default=0)
    
    case_number = db.Column(db.String(100), index=True)
    reason = db.Column(db.Text)
    custodian = db.Column(db.String(255))
    expected_duration = db.Column(db.String(50))
    
    status = db.Column(db.String(20), default='active', index=True)
    
    applied_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    applied_by_name = db.Column(db.String(255))
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    released_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    released_at = db.Column(db.DateTime)
    release_reason = db.Column(db.Text)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    applier = db.relationship('User', foreign_keys=[applied_by])
    releaser = db.relationship('User', foreign_keys=[released_by])
    
    # ✅ NEW: Junction relationship
    hold_documents = db.relationship(
        'LegalHoldDocument',
        foreign_keys='LegalHoldDocument.hold_id',
        backref='hold',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def to_dict(self):
        try:
            doc_ids = json.loads(self.document_ids) if isinstance(self.document_ids, str) else (self.document_ids or [])
        except:
            doc_ids = []
        
        return {
            'id': self.id,
            'document_ids': doc_ids,
            'case_number': self.case_number,
            'reason': self.reason,
            'custodian': self.custodian,
            'expected_duration': self.expected_duration,
            'status': self.status,
            'document_count': self.document_count,
            'applied_by': self.applied_by,
            'applied_by_name': self.applied_by_name or (self.applier.name if self.applier else None),
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'released_by': self.released_by,
            'released_at': self.released_at.isoformat() if self.released_at else None,
            'release_reason': self.release_reason,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class LegalHoldDocument(db.Model):
    """✅ NEW: Junction table for LegalHold ↔ Document"""
    __tablename__ = 'legal_hold_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    hold_id = db.Column(
        db.Integer,
        db.ForeignKey('legal_holds.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    document_id = db.Column(
        db.Integer,
        db.ForeignKey('documents.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    document = db.relationship('Document', foreign_keys=[document_id])
    adder = db.relationship('User', foreign_keys=[added_by])
    
    __table_args__ = (
        db.UniqueConstraint('hold_id', 'document_id', name='uq_hold_document'),
        db.Index('idx_hold_doc_company', 'company_id'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'hold_id': self.hold_id,
            'document_id': self.document_id,
            'document_title': self.document.title if self.document else None,
            'company_id': self.company_id,
            'added_at': self.added_at.isoformat() if self.added_at else None
        }


class DispositionCertificate(db.Model):
    """Proof of document disposal"""
    __tablename__ = 'disposition_certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    certificate_number = db.Column(db.String(100), unique=True, index=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), index=True)
    document_title = db.Column(db.String(255))
    
    disposal_method = db.Column(db.String(30))
    disposal_reason = db.Column(db.Text)
    disposed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    disposed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    disposed_by_name = db.Column(db.String(255))
    witnessed_by = db.Column(db.String(255))
    
    metadata_json = db.Column(db.Text, default='{}')
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    document = db.relationship('Document', foreign_keys=[document_id])
    disposer = db.relationship('User', foreign_keys=[disposed_by])
    
    def to_dict(self):
        try:
            meta = json.loads(self.metadata_json) if isinstance(self.metadata_json, str) else (self.metadata_json or {})
        except:
            meta = {}
        
        return {
            'id': self.id,
            'certificate_number': self.certificate_number,
            'document_id': self.document_id,
            'document_title': self.document_title,
            'disposal_method': self.disposal_method,
            'disposal_reason': self.disposal_reason,
            'disposed_at': self.disposed_at.isoformat() if self.disposed_at else None,
            'disposed_by': self.disposed_by,
            'disposed_by_name': self.disposed_by_name or (self.disposer.name if self.disposer else None),
            'witnessed_by': self.witnessed_by,
            'metadata': meta,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ============================================================
# GROUP 3: WATERMARKING (2 models)
# ============================================================

class WatermarkSettings(db.Model):
    """Watermark configuration per document"""
    __tablename__ = 'watermark_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False, unique=True, index=True)
    
    enabled = db.Column(db.Boolean, default=False)
    watermark_type = db.Column(db.String(30), default='diagonal')
    template = db.Column(db.String(30), default='confidential')
    
    text = db.Column(db.Text)
    color = db.Column(db.String(20), default='#f5222d')
    opacity = db.Column(db.Float, default=0.15)
    font_size = db.Column(db.Integer, default=60)
    rotation = db.Column(db.Integer, default=-45)
    position = db.Column(db.String(30), default='center')
    font_family = db.Column(db.String(50), default='Arial')
    font_weight = db.Column(db.String(20), default='bold')
    tile_spacing = db.Column(db.Integer, default=100)
    
    image_url = db.Column(db.String(500))
    
    apply_to_pages = db.Column(db.String(20), default='all')
    page_range = db.Column(db.Text, default='{}')
    
    apply_on_view = db.Column(db.Boolean, default=True)
    apply_on_download = db.Column(db.Boolean, default=True)
    apply_on_print = db.Column(db.Boolean, default=True)
    apply_on_share = db.Column(db.Boolean, default=True)
    dynamic_user_tracking = db.Column(db.Boolean, default=True)
    include_qr_code = db.Column(db.Boolean, default=False)
    include_barcode = db.Column(db.Boolean, default=False)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    document = db.relationship('Document', foreign_keys=[document_id], backref=db.backref('watermark_settings', uselist=False, cascade='all, delete-orphan'))
    
    def to_dict(self):
        try:
            pr = json.loads(self.page_range) if isinstance(self.page_range, str) else (self.page_range or {})
        except:
            pr = {}
        
        return {
            'id': self.id,
            'document_id': self.document_id,
            'enabled': self.enabled,
            'watermark_type': self.watermark_type,
            'template': self.template,
            'text': self.text,
            'color': self.color,
            'opacity': self.opacity,
            'font_size': self.font_size,
            'rotation': self.rotation,
            'position': self.position,
            'font_family': self.font_family,
            'font_weight': self.font_weight,
            'tile_spacing': self.tile_spacing,
            'image_url': self.image_url,
            'apply_to_pages': self.apply_to_pages,
            'page_range': pr,
            'apply_on_view': self.apply_on_view,
            'apply_on_download': self.apply_on_download,
            'apply_on_print': self.apply_on_print,
            'apply_on_share': self.apply_on_share,
            'dynamic_user_tracking': self.dynamic_user_tracking,
            'include_qr_code': self.include_qr_code,
            'include_barcode': self.include_barcode,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class WatermarkLog(db.Model):
    """Watermark application history"""
    __tablename__ = 'watermark_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), index=True)
    watermark_template = db.Column(db.String(50))
    
    action = db.Column(db.String(30))
    target = db.Column(db.String(30))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_name = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    document = db.relationship('Document', foreign_keys=[document_id])
    user = db.relationship('User', foreign_keys=[user_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'document_title': self.document.title if self.document else None,
            'watermark_template': self.watermark_template,
            'action': self.action,
            'target': self.target,
            'user_id': self.user_id,
            'user_name': self.user_name or (self.user.name if self.user else None),
            'ip_address': self.ip_address,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ============================================================
# GROUP 4: WORKFLOW BUILDER
# NOTE: Workflow already exists in your models. Skipping.
# You need to add ONE new model:
# ============================================================

class WorkflowExecution(db.Model):
    """Workflow run instances"""
    __tablename__ = 'workflow_executions'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False, index=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), index=True)
    
    status = db.Column(db.String(20), default='running', index=True)
    current_node_id = db.Column(db.String(100))
    
    context = db.Column(db.Text, default='{}')
    execution_log = db.Column(db.Text, default='[]')
    
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    
    workflow = db.relationship('Workflow', foreign_keys=[workflow_id], backref=db.backref('executions', lazy='dynamic'))
    document = db.relationship('Document', foreign_keys=[document_id])
    
    def to_dict(self):
        def pj(val, default):
            try:
                return json.loads(val) if isinstance(val, str) else (val or default)
            except:
                return default
        
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'workflow_name': self.workflow.name if self.workflow else None,
            'document_id': self.document_id,
            'status': self.status,
            'current_node_id': self.current_node_id,
            'context': pj(self.context, {}),
            'execution_log': pj(self.execution_log, []),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'company_id': self.company_id
        }


# ============================================================
# GROUP 5: COMPLIANCE REPORTS (3 models)
# ============================================================

class DocumentComplianceAssessment(db.Model):
    """Document compliance assessments (new feature)"""
    __tablename__ = 'document_compliance_assessments'   # ← renamed
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), index=True)
    framework_id = db.Column(db.String(50), nullable=False, index=True)
    requirement_id = db.Column(db.String(100))
    requirement = db.Column(db.Text)
    
    status = db.Column(db.String(30), default='not_assessed')
    score = db.Column(db.Integer, default=0)
    
    gap_description = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    evidence_count = db.Column(db.Integer, default=0)
    
    last_assessed = db.Column(db.DateTime)
    assessed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    document = db.relationship('Document', foreign_keys=[document_id])
    assessor = db.relationship('User', foreign_keys=[assessed_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'framework_id': self.framework_id,
            'requirement_id': self.requirement_id,
            'requirement': self.requirement,
            'status': self.status,
            'score': self.score,
            'gap_description': self.gap_description,
            'recommendation': self.recommendation,
            'evidence_count': self.evidence_count,
            'last_assessed': self.last_assessed.isoformat() if self.last_assessed else None,
            'assessed_by': self.assessed_by,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class DocumentComplianceReport(db.Model):
    """Generated document compliance reports (new feature)"""
    __tablename__ = 'document_compliance_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    report_type = db.Column(db.String(50), default='compliance_status')
    
    frameworks = db.Column(db.Text, default='[]')
    format = db.Column(db.String(20), default='pdf')
    
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)
    
    include_charts = db.Column(db.Boolean, default=True)
    include_evidence = db.Column(db.Boolean, default=True)
    include_recommendations = db.Column(db.Boolean, default=True)
    
    notes = db.Column(db.Text)
    download_url = db.Column(db.String(500))
    file_size = db.Column(db.Integer)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    generated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    generator = db.relationship('User', foreign_keys=[generated_by])
    
    def to_dict(self):
        try:
            fw = json.loads(self.frameworks) if isinstance(self.frameworks, str) else (self.frameworks or [])
        except:
            fw = []
        
        return {
            'id': self.id,
            'title': self.title,
            'report_type': self.report_type,
            'frameworks': fw,
            'format': self.format,
            'date_from': self.date_from.isoformat() if self.date_from else None,
            'date_to': self.date_to.isoformat() if self.date_to else None,
            'include_charts': self.include_charts,
            'include_evidence': self.include_evidence,
            'include_recommendations': self.include_recommendations,
            'notes': self.notes,
            'download_url': self.download_url,
            'file_size': self.file_size,
            'company_id': self.company_id,
            'generated_by': self.generated_by,
            'generated_by_name': self.generator.name if self.generator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class DocumentComplianceSchedule(db.Model):
    """Scheduled document compliance reports"""
    __tablename__ = 'document_compliance_schedules'   # ← renamed
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    report_config = db.Column(db.Text, default='{}')
    
    frequency = db.Column(db.String(20), default='monthly')
    recipients = db.Column(db.Text, default='[]')
    
    enabled = db.Column(db.Boolean, default=True)
    last_sent_at = db.Column(db.DateTime)
    next_send_at = db.Column(db.DateTime)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        def pj(val, default):
            try:
                return json.loads(val) if isinstance(val, str) else (val or default)
            except:
                return default
        
        return {
            'id': self.id,
            'name': self.name,
            'report_config': pj(self.report_config, {}),
            'frequency': self.frequency,
            'recipients': pj(self.recipients, []),
            'enabled': self.enabled,
            'last_sent_at': self.last_sent_at.isoformat() if self.last_sent_at else None,
            'next_send_at': self.next_send_at.isoformat() if self.next_send_at else None,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ============================================================
# GROUP 6: DOCUMENT BUNDLES (2 models)
# ============================================================

class DocumentBundle(db.Model):
    """Case files / bundles"""
    __tablename__ = 'document_bundles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), default='custom')
    description = db.Column(db.Text)
    tags = db.Column(db.Text, default='[]')
    
    is_confidential = db.Column(db.Boolean, default=False)
    is_locked = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime)
    
    status = db.Column(db.String(20), default='draft', index=True)
    
    document_count = db.Column(db.Integer, default=0)
    total_size = db.Column(db.Integer, default=0)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by_name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    bundle_documents = db.relationship('BundleDocument', foreign_keys='BundleDocument.bundle_id', backref='bundle', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        try:
            tg = json.loads(self.tags) if isinstance(self.tags, str) else (self.tags or [])
        except:
            tg = []
        
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'tags': tg,
            'is_confidential': self.is_confidential,
            'is_locked': self.is_locked,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'status': self.status,
            'document_count': self.document_count,
            'total_size': self.total_size,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_by_name': self.created_by_name or (self.creator.name if self.creator else None),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class BundleDocument(db.Model):
    """Many-to-many link between bundles and documents"""
    __tablename__ = 'bundle_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    bundle_id = db.Column(db.Integer, db.ForeignKey('document_bundles.id'), nullable=False, index=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False, index=True)
    
    position = db.Column(db.Integer, default=0)
    
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    document = db.relationship('Document', foreign_keys=[document_id])
    adder = db.relationship('User', foreign_keys=[added_by])
    
    __table_args__ = (
        db.UniqueConstraint('bundle_id', 'document_id', name='uq_bundle_document'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'bundle_id': self.bundle_id,
            'document_id': self.document_id,
            'document_title': self.document.title if self.document else None,
            'position': self.position,
            'added_by': self.added_by,
            'added_at': self.added_at.isoformat() if self.added_at else None
        }


# ============================================================
# GROUP 7: SHARE PORTAL (2 models)
# ============================================================

class Share(db.Model):
    """External share links"""
    __tablename__ = 'shares'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), index=True)
    bundle_id = db.Column(db.Integer, db.ForeignKey('document_bundles.id'), index=True)
    
    share_type = db.Column(db.String(20), default='link')  # link/email/portal/nda
    access_level = db.Column(db.String(20), default='view')  # view/comment/download/sign/edit
    
    recipient = db.Column(db.String(255))
    recipient_email = db.Column(db.String(255))
    recipients = db.Column(db.Text, default='[]')  # JSON array
    
    share_url = db.Column(db.String(500))
    share_token = db.Column(db.String(100), unique=True, index=True)
    
    expires_at = db.Column(db.DateTime, index=True)
    expiry_days = db.Column(db.Integer)
    max_downloads = db.Column(db.Integer)
    
    has_password = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(255))
    
    require_nda = db.Column(db.Boolean, default=False)
    require_email = db.Column(db.Boolean, default=True)
    send_notification = db.Column(db.Boolean, default=True)
    custom_message = db.Column(db.Text)
    
    watermark = db.Column(db.Boolean, default=True)
    allow_print = db.Column(db.Boolean, default=False)
    
    status = db.Column(db.String(20), default='active', index=True)  # active/expired/revoked/pending
    
    view_count = db.Column(db.Integer, default=0)
    download_count = db.Column(db.Integer, default=0)
    unique_users = db.Column(db.Integer, default=0)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    document = db.relationship('Document', foreign_keys=[document_id])
    bundle = db.relationship('DocumentBundle', foreign_keys=[bundle_id])
    creator = db.relationship('User', foreign_keys=[created_by])
    activities = db.relationship(
        'ShareActivity',
        foreign_keys='ShareActivity.share_id',
        backref='share',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    # ✅ NEW: CHECK constraint — exactly one of document_id or bundle_id must be set
    __table_args__ = (
        db.CheckConstraint(
            '(document_id IS NOT NULL AND bundle_id IS NULL) OR '
            '(document_id IS NULL AND bundle_id IS NOT NULL)',
            name='ck_share_exactly_one_target'
        ),
        db.Index('idx_share_document', 'document_id'),
        db.Index('idx_share_bundle', 'bundle_id'),
        db.Index('idx_share_token', 'share_token'),
        db.Index('idx_share_status', 'status'),
        db.Index('idx_share_company', 'company_id'),
        db.Index('idx_share_expires', 'expires_at'),
    )
    
    def to_dict(self):
        try:
            rec = json.loads(self.recipients) if isinstance(self.recipients, str) else (self.recipients or [])
        except:
            rec = []
        
        return {
            'id': self.id,
            'document_id': self.document_id,
            'document_title': self.document.title if self.document else None,
            'bundle_id': self.bundle_id,
            'bundle_name': self.bundle.name if self.bundle else None,
            'share_type': self.share_type,
            'access_level': self.access_level,
            'recipient': self.recipient,
            'recipient_email': self.recipient_email,
            'recipients': rec,
            'share_url': self.share_url,
            'share_token': self.share_token,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'expiry_days': self.expiry_days,
            'max_downloads': self.max_downloads,
            'has_password': self.has_password,
            'require_nda': self.require_nda,
            'require_email': self.require_email,
            'send_notification': self.send_notification,
            'custom_message': self.custom_message,
            'watermark': self.watermark,
            'allow_print': self.allow_print,
            'status': self.status,
            'view_count': self.view_count,
            'download_count': self.download_count,
            'unique_users': self.unique_users,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_by_name': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ShareActivity(db.Model):
    """Track share access"""
    __tablename__ = 'share_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    share_id = db.Column(db.Integer, db.ForeignKey('shares.id'), nullable=False, index=True)
    
    user_email = db.Column(db.String(255))
    action = db.Column(db.String(30), index=True)
    allowed = db.Column(db.Boolean, default=True)
    
    ip_address = db.Column(db.String(45))
    device = db.Column(db.String(20))
    user_agent = db.Column(db.String(500))
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'share_id': self.share_id,
            'user_email': self.user_email,
            'action': self.action,
            'allowed': self.allowed,
            'ip_address': self.ip_address,
            'device': self.device,
            'user_agent': self.user_agent,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ============================================================
# GROUP 8: SMART INTAKE (2 models)
# ============================================================

class IntakeQueueItem(db.Model):
    """AI-powered document processing queue"""
    __tablename__ = 'intake_queue_items'
    
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    file_url = db.Column(db.String(500))
    
    status = db.Column(db.String(30), default='uploading', index=True)
    stage = db.Column(db.String(30), default='uploading')
    progress = db.Column(db.Integer, default=0)
    
    predicted_type = db.Column(db.String(50))
    confidence = db.Column(db.Float, default=0.0)
    
    extracted_data = db.Column(db.Text, default='{}')
    suggested_tags = db.Column(db.Text, default='[]')
    ocr_text = db.Column(db.Text)
    
    duplicate_found = db.Column(db.Boolean, default=False)
    duplicate_title = db.Column(db.String(255))
    
    review_reason = db.Column(db.String(255))
    needs_review = db.Column(db.Boolean, default=False)
    
    error = db.Column(db.Text)
    message = db.Column(db.String(500))
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    processed_at = db.Column(db.DateTime)
    
    uploader = db.relationship('User', foreign_keys=[uploaded_by])
    
    def to_dict(self):
        def pj(val, default):
            try:
                return json.loads(val) if isinstance(val, str) else (val or default)
            except:
                return default
        
        return {
            'id': self.id,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'file_url': self.file_url,
            'status': self.status,
            'stage': self.stage,
            'progress': self.progress,
            'predicted_type': self.predicted_type,
            'confidence': self.confidence,
            'extracted_data': pj(self.extracted_data, {}),
            'suggested_tags': pj(self.suggested_tags, []),
            'ocr_text': self.ocr_text,
            'duplicate_found': self.duplicate_found,
            'duplicate_title': self.duplicate_title,
            'review_reason': self.review_reason,
            'needs_review': self.needs_review,
            'error': self.error,
            'message': self.message,
            'company_id': self.company_id,
            'uploaded_by': self.uploaded_by,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }


class IntakeStats(db.Model):
    """Aggregate intake statistics"""
    __tablename__ = 'intake_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True, unique=True)
    
    total_processed = db.Column(db.Integer, default=0)
    auto_approved = db.Column(db.Integer, default=0)
    needs_review = db.Column(db.Integer, default=0)
    duplicates_found = db.Column(db.Integer, default=0)
    avg_confidence = db.Column(db.Float, default=0.0)
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'total_processed': self.total_processed,
            'auto_approved': self.auto_approved,
            'needs_review': self.needs_review,
            'duplicates_found': self.duplicates_found,
            'avg_confidence': self.avg_confidence,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# ============================================================
# GROUP 9: ADVANCED SEARCH
# NOTE: SavedSearch & SearchHistory already exist in your models.
# Skipping both.
# ============================================================

class SearchAlert(db.Model):
    """Scheduled search notifications"""
    __tablename__ = 'search_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    query = db.Column(db.Text)
    mode = db.Column(db.String(20), default='fulltext')
    filters = db.Column(db.Text, default='{}')
    
    frequency = db.Column(db.String(20), default='daily')
    recipients = db.Column(db.Text, default='[]')
    
    enabled = db.Column(db.Boolean, default=True)
    last_sent_at = db.Column(db.DateTime)
    next_send_at = db.Column(db.DateTime)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        def pj(val, default):
            try:
                return json.loads(val) if isinstance(val, str) else (val or default)
            except:
                return default
        
        return {
            'id': self.id,
            'name': self.name,
            'query': self.query,
            'mode': self.mode,
            'filters': pj(self.filters, {}),
            'frequency': self.frequency,
            'recipients': pj(self.recipients, []),
            'enabled': self.enabled,
            'last_sent_at': self.last_sent_at.isoformat() if self.last_sent_at else None,
            'next_send_at': self.next_send_at.isoformat() if self.next_send_at else None,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ============================================================
# GROUP 10: AI ASSISTANT (2 models)
# ============================================================

class AssistantConversation(db.Model):
    """AI chat sessions"""
    __tablename__ = 'assistant_conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255), default='Untitled')
    message_count = db.Column(db.Integer, default=0)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id])
    messages = db.relationship('AssistantMessage', foreign_keys='AssistantMessage.conversation_id', backref='conversation', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message_count': self.message_count,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AssistantMessage(db.Model):
    """Individual chat messages"""
    __tablename__ = 'assistant_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey('assistant_conversations.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # ✅ NEW: Direct scope for query speed
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text)
    sources = db.Column(db.Text, default='[]')
    suggestions = db.Column(db.Text, default='[]')
    tokens_used = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        db.Index('idx_assistant_msg_user', 'user_id'),
        db.Index('idx_assistant_msg_company', 'company_id'),
    )
    
    def to_dict(self):
        def pj(val, default):
            try:
                return json.loads(val) if isinstance(val, str) else (val or default)
            except:
                return default
        
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'user_id': self.user_id,
            'company_id': self.company_id,
            'role': self.role,
            'content': self.content,
            'sources': pj(self.sources, []),
            'suggestions': pj(self.suggestions, []),
            'tokens_used': self.tokens_used,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ============================================================
# GROUP 11: BUSINESS INTELLIGENCE (2 models)
# ============================================================

class BIDashboard(db.Model):
    """Custom BI dashboards"""
    __tablename__ = 'bi_dashboards'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    widgets = db.Column(db.Text, default='[]')
    is_public = db.Column(db.Boolean, default=False)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        try:
            wg = json.loads(self.widgets) if isinstance(self.widgets, str) else (self.widgets or [])
        except:
            wg = []
        
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'widgets': wg,
            'is_public': self.is_public,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class BIDashboardShare(db.Model):
    """BI dashboard sharing"""
    __tablename__ = 'bi_dashboard_shares'
    
    id = db.Column(db.Integer, primary_key=True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('bi_dashboards.id'), nullable=False, index=True)
    recipients = db.Column(db.Text, default='[]')
    
    shared_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    shared_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    
    dashboard = db.relationship('BIDashboard', foreign_keys=[dashboard_id])
    sharer = db.relationship('User', foreign_keys=[shared_by])
    
    def to_dict(self):
        try:
            rec = json.loads(self.recipients) if isinstance(self.recipients, str) else (self.recipients or [])
        except:
            rec = []
        
        return {
            'id': self.id,
            'dashboard_id': self.dashboard_id,
            'recipients': rec,
            'shared_by': self.shared_by,
            'shared_at': self.shared_at.isoformat() if self.shared_at else None,
            'company_id': self.company_id
        }


# ============================================================
# GROUP 12: ANOMALY DETECTION (3 models)
# ============================================================

class Anomaly(db.Model):
    """Detected anomalies"""
    __tablename__ = 'anomalies'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False, index=True)
    severity = db.Column(db.String(20), nullable=False, index=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    user_name = db.Column(db.String(255))
    user_email = db.Column(db.String(255))
    
    description = db.Column(db.Text)
    risk_score = db.Column(db.Integer, default=0)
    
    status = db.Column(db.String(30), default='new', index=True)
    
    ip_address = db.Column(db.String(45))
    location = db.Column(db.String(255))
    device_info = db.Column(db.String(255))
    detection_method = db.Column(db.String(50))
    related_events = db.Column(db.Text, default='[]')
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship('User', foreign_keys=[user_id])
    resolver = db.relationship('User', foreign_keys=[resolved_by])
    
    def to_dict(self):
        try:
            re = json.loads(self.related_events) if isinstance(self.related_events, str) else (self.related_events or [])
        except:
            re = []
        
        return {
            'id': self.id,
            'type': self.type,
            'severity': self.severity,
            'user_id': self.user_id,
            'user_name': self.user_name or (self.user.name if self.user else None),
            'user_email': self.user_email,
            'description': self.description,
            'risk_score': self.risk_score,
            'status': self.status,
            'ip_address': self.ip_address,
            'location': self.location,
            'device_info': self.device_info,
            'detection_method': self.detection_method,
            'related_events': re,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolved_by': self.resolved_by
        }


class DetectionRule(db.Model):
    """Custom anomaly detection rules"""
    __tablename__ = 'detection_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50))
    severity = db.Column(db.String(20), default='medium')
    
    condition = db.Column(db.Text)
    actions = db.Column(db.Text, default='[]')
    
    enabled = db.Column(db.Boolean, default=True)
    triggered_count = db.Column(db.Integer, default=0)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        try:
            ac = json.loads(self.actions) if isinstance(self.actions, str) else (self.actions or [])
        except:
            ac = []
        
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'severity': self.severity,
            'condition': self.condition,
            'actions': ac,
            'enabled': self.enabled,
            'triggered_count': self.triggered_count,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class UserBaseline(db.Model):
    """User behavior baselines"""
    __tablename__ = 'user_baselines'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    user_name = db.Column(db.String(255))
    user_email = db.Column(db.String(255))
    
    typical_hours = db.Column(db.String(100))
    common_locations = db.Column(db.Text, default='[]')
    avg_daily_downloads = db.Column(db.Float, default=0.0)
    
    baseline_score = db.Column(db.Integer, default=100)
    risk_level = db.Column(db.String(20), default='low')
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id])
    
    def to_dict(self):
        try:
            cl = json.loads(self.common_locations) if isinstance(self.common_locations, str) else (self.common_locations or [])
        except:
            cl = []
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user_name or (self.user.name if self.user else None),
            'user_email': self.user_email,
            'typical_hours': self.typical_hours,
            'common_locations': cl,
            'avg_daily_downloads': self.avg_daily_downloads,
            'baseline_score': self.baseline_score,
            'risk_level': self.risk_level,
            'company_id': self.company_id,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# ============================================================
# GROUP 13: CUSTOM REPORTS (1 model)
# ============================================================

class CustomReport(db.Model):
    """User-built reports"""
    __tablename__ = 'custom_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    data_source = db.Column(db.String(50), default='documents')
    
    fields = db.Column(db.Text, default='[]')
    group_by = db.Column(db.Text, default='[]')
    aggregations = db.Column(db.Text, default='[]')
    filters = db.Column(db.Text, default='[]')
    sort_by = db.Column(db.Text, default='[]')
    limit = db.Column(db.Integer, default=100)
    
    visualization_type = db.Column(db.String(30), default='table')
    chart_config = db.Column(db.Text, default='{}')
    
    is_public = db.Column(db.Boolean, default=False)
    schedule = db.Column(db.Text, default='{}')
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        def pj(val, default):
            try:
                return json.loads(val) if isinstance(val, str) else (val or default)
            except:
                return default
        
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'data_source': self.data_source,
            'fields': pj(self.fields, []),
            'group_by': pj(self.group_by, []),
            'aggregations': pj(self.aggregations, []),
            'filters': pj(self.filters, []),
            'sort_by': pj(self.sort_by, []),
            'limit': self.limit,
            'visualization_type': self.visualization_type,
            'chart_config': pj(self.chart_config, {}),
            'is_public': self.is_public,
            'schedule': pj(self.schedule, {}),
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# ============================================================
# GROUP 14: PREDICTIVE ANALYTICS (2 models)
# NOTE: PredictiveModel already exists in your models.
# ============================================================



class PredictiveAlert(db.Model):
    """Predictive analytics alerts"""
    __tablename__ = 'predictive_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    prediction_type = db.Column(db.String(50))
    threshold = db.Column(db.Float, default=0.0)
    recipients = db.Column(db.Text, default='[]')
    enabled = db.Column(db.Boolean, default=True)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        try:
            rec = json.loads(self.recipients) if isinstance(self.recipients, str) else (self.recipients or [])
        except:
            rec = []
        
        return {
            'id': self.id,
            'name': self.name,
            'prediction_type': self.prediction_type,
            'threshold': self.threshold,
            'recipients': rec,
            'enabled': self.enabled,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ============================================================
# GROUP 15: QUALITY MANAGEMENT (4 models)
# ============================================================

class QualityRecord(db.Model):
    """CAPA/NCR/Deviation/Change Request records"""
    __tablename__ = 'quality_records'
    
    id = db.Column(db.Integer, primary_key=True)
    record_number = db.Column(db.String(50), unique=True, index=True)
    type = db.Column(db.String(30), nullable=False, index=True)
    
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20), default='minor', index=True)
    
    department = db.Column(db.String(100))
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_to_name = db.Column(db.String(255))
    due_date = db.Column(db.DateTime, index=True)
    source = db.Column(db.String(100))
    
    attachments = db.Column(db.Text, default='[]')
    rca = db.Column(db.Text, default='{}')
    
    status = db.Column(db.String(30), default='draft', index=True)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    creator = db.relationship('User', foreign_keys=[created_by])
    actions = db.relationship('QualityAction', foreign_keys='QualityAction.record_id', backref='record', lazy='dynamic', cascade='all, delete-orphan')
    timeline = db.relationship('QualityTimeline', foreign_keys='QualityTimeline.record_id', backref='quality_record', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        def pj(val, default):
            try:
                return json.loads(val) if isinstance(val, str) else (val or default)
            except:
                return default
        
        return {
            'id': self.id,
            'record_number': self.record_number,
            'type': self.type,
            'title': self.title,
            'description': self.description,
            'severity': self.severity,
            'department': self.department,
            'assigned_to': self.assigned_to,
            'assigned_to_name': self.assigned_to_name or (self.assignee.name if self.assignee else None),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'source': self.source,
            'attachments': pj(self.attachments, []),
            'rca': pj(self.rca, {}),
            'status': self.status,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }



class QualityAction(db.Model):
    """Action items per quality record"""
    __tablename__ = 'quality_actions'
    
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(
        db.Integer,
        db.ForeignKey('quality_records.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # ✅ NEW: Direct scope for query speed
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    
    action_type = db.Column(db.String(30), default='corrective')
    description = db.Column(db.Text)
    
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_to_name = db.Column(db.String(255))
    due_date = db.Column(db.DateTime, index=True)
    priority = db.Column(db.String(20), default='medium')
    
    status = db.Column(db.String(30), default='pending', index=True)
    
    completed_at = db.Column(db.DateTime)
    verified_at = db.Column(db.DateTime)
    verification_notes = db.Column(db.Text)
    effectiveness_score = db.Column(db.Integer)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    
    __table_args__ = (
        db.Index('idx_quality_action_company', 'company_id'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'record_id': self.record_id,
            'company_id': self.company_id,
            'action_type': self.action_type,
            'description': self.description,
            'assigned_to': self.assigned_to,
            'assigned_to_name': self.assigned_to_name or (self.assignee.name if self.assignee else None),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority,
            'status': self.status,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'verification_notes': self.verification_notes,
            'effectiveness_score': self.effectiveness_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class QualityTimeline(db.Model):
    """Activity log for quality records"""
    __tablename__ = 'quality_timeline'
    
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(
        db.Integer,
        db.ForeignKey('quality_records.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # ✅ NEW: Direct scope
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    
    action = db.Column(db.String(100))
    description = db.Column(db.Text)
    type = db.Column(db.String(30))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_name = db.Column(db.String(255))
    
    action_metadata = db.Column(db.Text, default='{}')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    user = db.relationship('User', foreign_keys=[user_id])
    
    __table_args__ = (
        db.Index('idx_quality_timeline_company', 'company_id'),
    )
    
    def to_dict(self):
        try:
            md = json.loads(self.action_metadata) if isinstance(self.action_metadata, str) else (self.action_metadata or {})
        except:
            md = {}
        
        return {
            'id': self.id,
            'record_id': self.record_id,
            'company_id': self.company_id,
            'action': self.action,
            'description': self.description,
            'type': self.type,
            'user_id': self.user_id,
            'user_name': self.user_name or (self.user.name if self.user else None),
            'metadata': md,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class QualityMetrics(db.Model):
    """Aggregate QMS metrics"""
    __tablename__ = 'quality_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    period = db.Column(db.String(30))
    
    avg_resolution_days = db.Column(db.Float, default=0.0)
    closure_rate = db.Column(db.Float, default=0.0)
    on_time_rate = db.Column(db.Float, default=0.0)
    recurrence_rate = db.Column(db.Float, default=0.0)
    capa_effectiveness = db.Column(db.Float, default=0.0)
    first_time_right = db.Column(db.Float, default=0.0)
    response_sla = db.Column(db.Float, default=0.0)
    doc_accuracy = db.Column(db.Float, default=0.0)
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'period': self.period,
            'avg_resolution_days': self.avg_resolution_days,
            'closure_rate': self.closure_rate,
            'on_time_rate': self.on_time_rate,
            'recurrence_rate': self.recurrence_rate,
            'capa_effectiveness': self.capa_effectiveness,
            'first_time_right': self.first_time_right,
            'response_sla': self.response_sla,
            'doc_accuracy': self.doc_accuracy,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# ============================================================
# GROUP 16: OFFLINE MANAGER (4 models)
# ============================================================

class OfflineDocument(db.Model):
    """Cached documents for offline access"""
    __tablename__ = 'offline_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False, index=True)
    
    cached_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_accessed = db.Column(db.DateTime)
    
    file_size = db.Column(db.Integer)
    hash_value = db.Column(db.String(255))
    
    sync_status = db.Column(db.String(20), default='synced', index=True)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    
    user = db.relationship('User', foreign_keys=[user_id])
    document = db.relationship('Document', foreign_keys=[document_id])
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'document_id', name='uq_user_offline_doc'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'document_id': self.document_id,
            'document_title': self.document.title if self.document else None,
            'cached_at': self.cached_at.isoformat() if self.cached_at else None,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'file_size': self.file_size,
            'hash': self.hash_value,
            'sync_status': self.sync_status,
            'company_id': self.company_id
        }


class SyncQueueItem(db.Model):
    """Pending offline changes"""
    __tablename__ = 'sync_queue_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), index=True)
    
    action = db.Column(db.String(30), index=True)
    description = db.Column(db.Text)
    payload = db.Column(db.Text, default='{}')
    
    status = db.Column(db.String(20), default='pending', index=True)
    retry_count = db.Column(db.Integer, default=0)
    error = db.Column(db.Text)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id])
    document = db.relationship('Document', foreign_keys=[document_id])
    
    def to_dict(self):
        try:
            pl = json.loads(self.payload) if isinstance(self.payload, str) else (self.payload or {})
        except:
            pl = {}
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'document_id': self.document_id,
            'document_title': self.document.title if self.document else None,
            'action': self.action,
            'description': self.description,
            'payload': pl,
            'status': self.status,
            'retry_count': self.retry_count,
            'error': self.error,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class SyncConflict(db.Model):
    """Sync conflicts between local and remote"""
    __tablename__ = 'sync_conflicts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), index=True)
    document_title = db.Column(db.String(255))
    
    conflict_type = db.Column(db.String(50))
    local_content = db.Column(db.Text)
    remote_content = db.Column(db.Text)
    local_modified = db.Column(db.DateTime)
    remote_modified = db.Column(db.DateTime)
    
    resolved = db.Column(db.Boolean, default=False, index=True)
    resolution = db.Column(db.String(20))
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id])
    resolver = db.relationship('User', foreign_keys=[resolved_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'document_id': self.document_id,
            'document_title': self.document_title,
            'conflict_type': self.conflict_type,
            'local_content': self.local_content,
            'remote_content': self.remote_content,
            'local_modified': self.local_modified.isoformat() if self.local_modified else None,
            'remote_modified': self.remote_modified.isoformat() if self.remote_modified else None,
            'resolved': self.resolved,
            'resolution': self.resolution,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolved_by': self.resolved_by,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class OfflineSettings(db.Model):
    """Per-user offline preferences"""
    __tablename__ = 'offline_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    
    cache_strategy = db.Column(db.String(30), default='recent')
    auto_sync = db.Column(db.Boolean, default=True)
    sync_interval = db.Column(db.Integer, default=15)
    wifi_only = db.Column(db.Boolean, default=True)
    max_cache_size = db.Column(db.Integer, default=500)
    encrypt_cache = db.Column(db.Boolean, default=True)
    auto_download = db.Column(db.Boolean, default=True)
    
    last_sync_at = db.Column(db.DateTime)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'cache_strategy': self.cache_strategy,
            'auto_sync': self.auto_sync,
            'sync_interval': self.sync_interval,
            'wifi_only': self.wifi_only,
            'max_cache_size': self.max_cache_size,
            'encrypt_cache': self.encrypt_cache,
            'auto_download': self.auto_download,
            'last_sync_at': self.last_sync_at.isoformat() if self.last_sync_at else None,
            'company_id': self.company_id,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# ============================================================
# GROUP 17: INTEGRATION HUB (4 models)
# ============================================================

class Integration(db.Model):
    """Connected external integrations"""
    __tablename__ = 'integrations'
    
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.String(50), nullable=False, index=True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(30))
    
    config = db.Column(db.Text, default='{}')
    
    status = db.Column(db.String(20), default='disconnected', index=True)
    
    connected_at = db.Column(db.DateTime)
    last_sync_at = db.Column(db.DateTime)
    documents_synced = db.Column(db.Integer, default=0)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    connected_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    connector = db.relationship('User', foreign_keys=[connected_by])
    
    def to_dict(self):
        try:
            cf = json.loads(self.config) if isinstance(self.config, str) else (self.config or {})
        except:
            cf = {}
        
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'name': self.name,
            'category': self.category,
            'config': cf,
            'status': self.status,
            'connected_at': self.connected_at.isoformat() if self.connected_at else None,
            'last_sync_at': self.last_sync_at.isoformat() if self.last_sync_at else None,
            'documents_synced': self.documents_synced,
            'company_id': self.company_id,
            'connected_by': self.connected_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Webhook(db.Model):
    """User-defined webhooks"""
    __tablename__ = 'webhooks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    
    events = db.Column(db.Text, default='[]')
    secret = db.Column(db.String(255))
    
    enabled = db.Column(db.Boolean, default=True, index=True)
    last_triggered_at = db.Column(db.DateTime)
    trigger_count = db.Column(db.Integer, default=0)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        try:
            ev = json.loads(self.events) if isinstance(self.events, str) else (self.events or [])
        except:
            ev = []
        
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'events': ev,
            'enabled': self.enabled,
            'last_triggered_at': self.last_triggered_at.isoformat() if self.last_triggered_at else None,
            'trigger_count': self.trigger_count,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class APIKey(db.Model):
    """API access keys"""
    __tablename__ = 'api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    key_hash = db.Column(db.String(255), nullable=False)
    prefix = db.Column(db.String(20))
    
    scopes = db.Column(db.Text, default='[]')
    
    expires_at = db.Column(db.DateTime)
    last_used_at = db.Column(db.DateTime)
    
    revoked = db.Column(db.Boolean, default=False, index=True)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        try:
            sc = json.loads(self.scopes) if isinstance(self.scopes, str) else (self.scopes or [])
        except:
            sc = []
        
        return {
            'id': self.id,
            'name': self.name,
            'prefix': self.prefix,
            'scopes': sc,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'revoked': self.revoked,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class IntegrationActivity(db.Model):
    """Integration activity log"""
    __tablename__ = 'integration_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    integration_id = db.Column(db.String(50), index=True)
    integration_name = db.Column(db.String(255))
    
    action = db.Column(db.String(100))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='success', index=True)
    duration = db.Column(db.Integer)
    error_message = db.Column(db.Text)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'integration_id': self.integration_id,
            'integration_name': self.integration_name,
            'action': self.action,
            'description': self.description,
            'status': self.status,
            'duration': self.duration,
            'error_message': self.error_message,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ============================================================
# GROUP 18: REALTIME COLLABORATION (2 models)
# ============================================================

class CollaborationSession(db.Model):
    """Active real-time editing sessions"""
    __tablename__ = 'collaboration_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    user_name = db.Column(db.String(255))
    user_color = db.Column(db.String(20))
    
    socket_id = db.Column(db.String(100), index=True)
    cursor_position = db.Column(db.Integer, default=0)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    document = db.relationship('Document', foreign_keys=[document_id])
    user = db.relationship('User', foreign_keys=[user_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'user_id': self.user_id,
            'user_name': self.user_name or (self.user.name if self.user else None),
            'user_color': self.user_color,
            'socket_id': self.socket_id,
            'cursor_position': self.cursor_position,
            'company_id': self.company_id,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None
        }


class DocumentLock(db.Model):
    """Document locks during editing"""
    __tablename__ = 'document_locks'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False, unique=True, index=True)
    
    locked_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    locked_by_name = db.Column(db.String(255))
    locked_at = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.String(255))
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    
    document = db.relationship('Document', foreign_keys=[document_id])
    locker = db.relationship('User', foreign_keys=[locked_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'document_title': self.document.title if self.document else None,
            'locked_by': self.locked_by,
            'locked_by_name': self.locked_by_name or (self.locker.name if self.locker else None),
            'locked_at': self.locked_at.isoformat() if self.locked_at else None,
            'reason': self.reason,
            'company_id': self.company_id
        }

# ============================================================
# GROUP 4: WORKFLOW BUILDER (2 models) — RENAMED
# ============================================================

class DocumentWorkflowDefinition(db.Model):
    """Custom document workflow definitions (visual builder)"""
    __tablename__ = 'document_workflow_definitions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='general')
    
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)
    applicable_to = db.Column(db.Text, default='[]')  # JSON array
    
    nodes = db.Column(db.Text, default='[]')  # JSON array of node objects
    connections = db.Column(db.Text, default='[]')  # JSON array of edges
    
    version = db.Column(db.Integer, default=1)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    executions = db.relationship(
        'DocumentWorkflowExecution',
        foreign_keys='DocumentWorkflowExecution.workflow_id',
        backref='workflow',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    __table_args__ = (
        db.Index('idx_doc_workflow_company', 'company_id'),
        db.Index('idx_doc_workflow_active', 'is_active'),
    )
    
    def to_dict(self):
        def pj(val, default):
            try:
                return json.loads(val) if isinstance(val, str) else (val or default)
            except:
                return default
        
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'applicable_to': pj(self.applicable_to, []),
            'nodes': pj(self.nodes, []),
            'connections': pj(self.connections, []),
            'version': self.version,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_by_name': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class DocumentWorkflowExecution(db.Model):
    """Runs of a document workflow definition"""
    __tablename__ = 'document_workflow_executions'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(
        db.Integer,
        db.ForeignKey('document_workflow_definitions.id'),
        nullable=False,
        index=True
    )
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), index=True)
    
    status = db.Column(db.String(20), default='running', index=True)  # running/completed/failed/cancelled
    current_node_id = db.Column(db.String(100))
    
    context = db.Column(db.Text, default='{}')  # JSON
    execution_log = db.Column(db.Text, default='[]')  # JSON array
    
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    
    document = db.relationship('Document', foreign_keys=[document_id])
    
    def to_dict(self):
        def pj(val, default):
            try:
                return json.loads(val) if isinstance(val, str) else (val or default)
            except:
                return default
        
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'workflow_name': self.workflow.name if self.workflow else None,
            'document_id': self.document_id,
            'document_title': self.document.title if self.document else None,
            'status': self.status,
            'current_node_id': self.current_node_id,
            'context': pj(self.context, {}),
            'execution_log': pj(self.execution_log, []),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'company_id': self.company_id
        }


# ============================================================
# GROUP 14: PREDICTIVE ANALYTICS — RENAMED
# ============================================================

class MLPredictiveModel(db.Model):
    """Machine learning model registry for predictive analytics"""
    __tablename__ = 'ml_predictive_models'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50))  # time_series/regression/ml_model/neural_network
    
    accuracy = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='inactive', index=True)  # active/training/inactive
    
    model_metadata = db.Column(db.Text, default='{}')  # JSON
    
    trained_at = db.Column(db.DateTime)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        try:
            md = json.loads(self.model_metadata) if isinstance(self.model_metadata, str) else (self.model_metadata or {})
        except:
            md = {}
        
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'accuracy': self.accuracy,
            'status': self.status,
            'metadata': md,
            'trained_at': self.trained_at.isoformat() if self.trained_at else None,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Prediction(db.Model):
    """Generated predictions"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    type = db.Column(db.String(50), index=True)  # document_volume/compliance_risk/expiry_risk/etc
    description = db.Column(db.Text)
    
    value = db.Column(db.Float, default=0.0)
    unit = db.Column(db.String(30))
    timeframe = db.Column(db.String(50))
    confidence = db.Column(db.Float, default=0.0)
    risk_score = db.Column(db.Integer, default=0)
    
    # ✅ UPDATED FK — points to the new renamed model
    model_id = db.Column(
        db.Integer,
        db.ForeignKey('ml_predictive_models.id'),
        index=True
    )
    supporting_data = db.Column(db.Text, default='[]')  # JSON
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    model = db.relationship('MLPredictiveModel', foreign_keys=[model_id])
    
    def to_dict(self):
        try:
            sd = json.loads(self.supporting_data) if isinstance(self.supporting_data, str) else (self.supporting_data or [])
        except:
            sd = []
        
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'description': self.description,
            'value': self.value,
            'unit': self.unit,
            'timeframe': self.timeframe,
            'confidence': self.confidence,
            'risk_score': self.risk_score,
            'model_id': self.model_id,
            'model': self.model.name if self.model else None,
            'supporting_data': sd,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
