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
    # User relationships (backward compatibility)
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('user_documents', lazy='dynamic'))
    
    # New relationships
    creator = db.relationship('User', foreign_keys=[created_by], backref=db.backref('created_documents', lazy='dynamic'))
    updater = db.relationship('User', foreign_keys=[updated_by])
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    approver = db.relationship('User', foreign_keys=[approved_by])
    company = db.relationship('Company', foreign_keys=[company_id], backref=db.backref('company_documents', lazy='dynamic'))
    
    # Document Control System Relationships
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
    )
    
    def to_dict(self):
        """Convert document to dictionary with proper type handling"""
        
        # ✅ FIXED: Parse tags from JSON string properly
        try:
            if self.tags:
                tags = json.loads(self.tags) if isinstance(self.tags, str) else self.tags
            else:
                tags = []
        except (json.JSONDecodeError, TypeError):
            # Fallback: if it's a comma-separated string
            if self.tags and isinstance(self.tags, str):
                tags = [t.strip() for t in self.tags.split(',') if t.strip()]
            else:
                tags = []
        
        return {
            'id': self.id,
            'user_id': self.user_id,  # Keep for backward compatibility
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
            'tags': tags,  # ✅ Now properly parsed as a list
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
                # If it's already a JSON string, validate it
                json.loads(tags_list)
                self.tags = tags_list
            except json.JSONDecodeError:
                # If it's a comma-separated string, convert to list
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
    upload_file_id = db.Column(db.Integer, db.ForeignKey('upload_files.id'))
    analysis_results = db.Column(db.Text)  # JSON string of analysis results
    duration = db.Column(db.Float)  # in seconds
    violations_count = db.Column(db.Integer, default=0)
    compliance_score = db.Column(db.Float)
    industry = db.Column(db.String(64))
    status = db.Column(db.String(32), default='completed')  # processing, completed, failed
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    processing_time = db.Column(db.Float)  # in seconds

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
    __tablename__ = 'safety_observations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    observation_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(100), nullable=False)  # safe_behavior, unsafe_condition, positive_observation
    category = db.Column(db.String(100))  # ppe, procedures, equipment, housekeeping, etc.
    location = db.Column(db.String(255))
    department = db.Column(db.String(100))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    observed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_observed = db.Column(db.DateTime, nullable=False)
    risk_level = db.Column(db.String(50))
    immediate_action = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    status = db.Column(db.String(50), default='open')  # open, in_progress, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    observer = db.relationship('User', foreign_keys=[observed_by])
    hospital = db.relationship('Hospital', backref=db.backref('safety_observations', lazy=True))

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