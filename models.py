
# models.py
from datetime import datetime
import json

# Flask extensions (from your extensions.py)
from datetime import datetime, timedelta
from flask import current_app
# SQLAlchemy utilities (if needed for specific column types)
from sqlalchemy import Text, Float, Integer, String, Boolean, DateTime, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from extensions import db
# Optional: If you use any JSON fields
from sqlalchemy.dialects.sqlite import JSON

from usermodels import (
    User,
    SafetyViolation,
    UploadedFile,
    
    MedicalAnalysis,
    APIUsage,
    MonthlyUsageSummary,
    Verification,
    PasswordReset,
    Document,
    DocumentTemplate,
    TemplateCategory,
    EditableDocument,
    Notification,
    Team,
    TeamMember,
    TeamInvitation,
    Subscription,
    Payment,
    SubscriptionHistory,
    PaymentHistory,
    AdminAuditLog,
    AdminApprovalLog,
    Workflow,
    Referral,
    CameraFeed,
    VideoAnalysis,
    AIRequest,
    PredictiveModel,
    ActivityLog,
    LoginLog,
    UserPreferences,
    Industry,
    Incident,
    IncidentAttachment,
    IncidentReportLog,
    IncidentAction,
    NearMiss,
    SafetyObservation,
    BiohazardIncident,
    Permit,
    PermitReview,
    Training,
    TrainingSession,
    TrainingRecord,
    SafetyTraining,
    Project,
    Task,
    Milestone,
    ProjectPhase,
    ProjectTask,
    SafetyTool,
    Permission,
    Role,
    UserRole,
    ManualPayment,
    ComplianceRecord,
    EnvironmentalMetric,
    EnvironmentalScore,
    EnvironmentalInitiative,
    UserEngagementEvent,
    UserEngagementScore,
    Doctor,
    SafetyIncident,
    DocumentVersion,
    DocumentMetadata,
    DocumentComment,
    DocumentAuditLog,
    DocumentLink,
    ReviewHistory,
    DocumentSignature,
    SignatureVerification,
    SavedSearch,
    SearchHistory,
    DocumentWorkflow,
    DocumentCategory,
    ApprovalChain,
    ApprovalStep,
    TemplateCategoryMapping,
    DocumentApproval,
    ApprovalStepStatus,
    DocumentExpiration,
    ExpirationNotificationLog,
    ComplianceFramework,
    ComplianceRequirement,
    ComplianceAuditLog,
    DocumentComplianceLink,






)
# ===== HOSPITAL MANAGEMENT =====

class Hospital(db.Model):
    __tablename__ = 'hospitals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(128))
    country = db.Column(db.String(128))
    type = db.Column(db.String(128))  # General, Specialty, Teaching, etc.
    beds = db.Column(db.Integer)
    accreditation = db.Column(db.String(128))
    contact_email = db.Column(db.String(128))
    contact_phone = db.Column(db.String(32))
    status = db.Column(db.String(32), default='active')
    rating = db.Column(db.Float, default=0)
    established_date = db.Column(db.DateTime)
    emergency_services = db.Column(db.Boolean, default=True)
    teaching_hospital = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True, index=True)
    
    
    company = db.relationship('Company', foreign_keys=[company_id], backref='hospitals', lazy=True)
    # NO RELATIONSHIPS HERE - they cause mapper initialization errors
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'type': self.type,
            'beds': self.beds,
            'accreditation': self.accreditation,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'status': self.status,
            'rating': self.rating,
            'established_date': self.established_date.isoformat() if self.established_date else None,
            'emergency_services': self.emergency_services,
            'teaching_hospital': self.teaching_hospital,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    # ===== HELPER METHODS FOR RELATED DATA =====
    
    def get_departments(self):
        """Get departments for this hospital"""
        from models import Department
        return Department.query.filter_by(hospital_id=self.id).all()
    
    def get_employees(self):
        """Get employees (users) for this hospital"""
        from models import User
        return User.query.filter_by(hospital_id=self.id).all()
    
    def get_patients(self):
        """Get patients for this hospital"""
        from models import Patient
        return Patient.query.filter_by(hospital_id=self.id).all()
    
    def get_beds(self):
        """Get beds for this hospital"""
        from models import Bed
        return Bed.query.filter_by(hospital_id=self.id).all()
    
    def get_incidents(self):
        """Get incidents for this hospital"""
        from models import Incident
        return Incident.query.filter_by(hospital_id=self.id).all()
    
    def get_safety_incidents(self):
        """Get safety incidents for this hospital"""
        try:
            from models import SafetyIncident
            return SafetyIncident.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_risk_assessments(self):
        """Get risk assessments for this hospital"""
        try:
            from models import RiskAssessment
            return RiskAssessment.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_emergency_plans(self):
        """Get emergency plans for this hospital"""
        try:
            from models import EmergencyPlan
            return EmergencyPlan.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_emergency_drills(self):
        """Get emergency drills for this hospital"""
        try:
            from models import EmergencyDrill
            return EmergencyDrill.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_compliances(self):
        """Get compliances for this hospital"""
        try:
            from models import Compliance
            return Compliance.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_safety_inspections(self):
        """Get safety inspections for this hospital"""
        try:
            from models import SafetyInspection
            return SafetyInspection.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_safety_equipment(self):
        """Get safety equipment for this hospital"""
        try:
            from models import SafetyEquipment
            return SafetyEquipment.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_safety_trainings(self):
        """Get safety trainings for this hospital"""
        try:
            from models import SafetyTraining
            return SafetyTraining.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_lab_safety(self):
        """Get lab safety records for this hospital"""
        try:
            from models import LabSafety
            return LabSafety.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_accreditations(self):
        """Get accreditations for this hospital"""
        try:
            from models import Accreditation
            return Accreditation.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_quality_indicators(self):
        """Get quality indicators for this hospital"""
        try:
            from models import QualityIndicator
            return QualityIndicator.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_patient_safety_goals(self):
        """Get patient safety goals for this hospital"""
        try:
            from models import PatientSafetyGoal
            return PatientSafetyGoal.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_adverse_events(self):
        """Get adverse events for this hospital"""
        try:
            from models import AdverseEvent
            return AdverseEvent.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_staff_competencies(self):
        """Get staff competencies for this hospital"""
        try:
            from models import StaffCompetency
            return StaffCompetency.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_medical_analyses(self):
        """Get medical analyses for this hospital"""
        try:
            from models import MedicalAnalysis
            return MedicalAnalysis.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_medical_chats(self):
        """Get medical chats for this hospital"""
        try:
            from models import MedicalChat
            return MedicalChat.query.filter_by(hospital_id=self.id).all()
        except (ImportError, AttributeError):
            return []
    
    def get_stats(self):
        """Get hospital statistics"""
        return {
            'department_count': len(self.get_departments()),
            'employee_count': len(self.get_employees()),
            'patient_count': len(self.get_patients()),
            'bed_count': len(self.get_beds()),
            'incident_count': len(self.get_incidents()),
            'safety_incident_count': len(self.get_safety_incidents()),
            'safety_inspection_count': len(self.get_safety_inspections()),
            'compliance_count': len(self.get_compliances()),
            'emergency_plan_count': len(self.get_emergency_plans()),
            'risk_assessment_count': len(self.get_risk_assessments()),
            'total_beds': self.beds or 0,
            'occupied_beds': sum(1 for bed in self.get_beds() if bed.status == 'occupied'),
            'available_beds': sum(1 for bed in self.get_beds() if bed.status == 'available'),
            'utilization_rate': self.get_utilization_rate()
        }
    
    def get_utilization_rate(self):
        """Calculate bed utilization rate"""
        total_beds = self.beds or 0
        if total_beds == 0:
            return 0
        occupied = sum(1 for bed in self.get_beds() if bed.status == 'occupied')
        return round((occupied / total_beds) * 100, 1)
    
    def get_department_stats(self):
        """Get statistics by department"""
        departments = self.get_departments()
        stats = []
        for dept in departments:
            stats.append({
                'id': dept.id,
                'name': dept.name,
                'employee_count': len(self.get_employees_by_department(dept.id)),
                'patient_count': len(self.get_patients_by_department(dept.id)),
                'incident_count': len(self.get_incidents_by_department(dept.id))
            })
        return stats
    
    def get_employees_by_department(self, department_id):
        """Get employees in a specific department"""
        from models import User
        return User.query.filter_by(hospital_id=self.id, department_id=department_id).all()
    
    def get_patients_by_department(self, department_id):
        """Get patients in a specific department"""
        from models import Patient
        return Patient.query.filter_by(hospital_id=self.id, department_id=department_id).all()
    
    def get_incidents_by_department(self, department_id):
        """Get incidents in a specific department"""
        from models import Incident
        return Incident.query.filter_by(hospital_id=self.id, department_id=department_id).all()
    
    def to_dict_with_stats(self):
        """Convert hospital to dictionary with statistics"""
        data = self.to_dict()
        data['stats'] = self.get_stats()
        data['department_stats'] = self.get_department_stats()
        return data
    
class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    
    # ✅ Use back_populates to link to Company
    company = db.relationship('Company', back_populates='departments')
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    head_of_department = db.Column(db.String(128))
    location = db.Column(db.String(256))
    risk_level = db.Column(db.String(32), default='Low')
    staff_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(32), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    hazards = db.relationship('Hazard', backref='department', lazy=True, cascade='all, delete-orphan')
    equipment = db.relationship('Equipment', backref='department', lazy=True, cascade='all, delete-orphan')
    risk_assessments = db.relationship('RiskAssessment', back_populates='department')
    emergency_plans = db.relationship('EmergencyPlan', back_populates='department')
    emergency_drills = db.relationship('EmergencyDrill', back_populates='department')
    waste_disposals = db.relationship('WasteDisposal', back_populates='department')
    patient_safety_incidents = db.relationship('PatientSafetyIncident', back_populates='department')
    fall_risk_assessments = db.relationship('FallRiskAssessment', back_populates='department')
    indoor_air_quality = db.relationship('IndoorAirQuality', back_populates='department')
    surface_sanitation = db.relationship('SurfaceSanitation', back_populates='department')
    workplace_ergonomics = db.relationship('WorkplaceErgonomics', back_populates='department')
    safety_kpis = db.relationship('SafetyKPI', back_populates='department')
    safety_documents = db.relationship('SafetyDocument', back_populates='department')
    improvement_initiatives = db.relationship('ImprovementInitiative', back_populates='department')
    corrective_actions = db.relationship('CorrectiveAction', back_populates='department')
    
    def to_dict(self):
        return {
            'id': self.id,
            'hospital_id': self.hospital_id,
            'company_id': self.company_id,
            'name': self.name,
            'description': self.description,
            'head_of_department': self.head_of_department,
            'location': self.location,
            'risk_level': self.risk_level,
            'staff_count': self.staff_count,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
# ============================================
# PATIENT FLOW MODELS
# ============================================

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=True, index=True)
    mrn = db.Column(db.String(50), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(20))
    dob = db.Column(db.DateTime)
    age = db.Column(db.Integer)
    blood_type = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.String(128))
    emergency_phone = db.Column(db.String(20))
    admission_date = db.Column(db.DateTime, default=datetime.utcnow)
    discharge_date = db.Column(db.DateTime)
    status = db.Column(db.String(32), default='Admitted', index=True)
    department = db.Column(db.String(128))
    ward = db.Column(db.String(64))
    bed_number = db.Column(db.Integer)
    diagnosis = db.Column(db.String(512))
    diagnoses = db.Column(db.JSON, default=list)
    doctor_name = db.Column(db.String(128))  # ✅ Renamed from 'doctor' to 'doctor_name'
    medical_history = db.Column(db.Text)
    allergies = db.Column(db.JSON, default=list)
    medications = db.Column(db.JSON, default=list)
    current_medications = db.Column(db.JSON, default=list)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)
    
    # Relationships
    timeline_events = db.relationship('PatientTimeline', backref='patient', lazy=True, cascade='all, delete-orphan')
    
    # ✅ Relationship to Doctor - using back_populates instead of backref
    doctor = db.relationship('Doctor', back_populates='patients', foreign_keys=[doctor_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'hospital_id': self.hospital_id,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else self.doctor_name,
            'mrn': self.mrn,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'gender': self.gender,
            'dob': self.dob.isoformat() if self.dob else None,
            'age': self.age,
            'blood_type': self.blood_type,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'emergency_contact': self.emergency_contact,
            'emergency_phone': self.emergency_phone,
            'admission_date': self.admission_date.isoformat() if self.admission_date else None,
            'discharge_date': self.discharge_date.isoformat() if self.discharge_date else None,
            'status': self.status,
            'department': self.department,
            'ward': self.ward,
            'bed_number': self.bed_number,
            'diagnosis': self.diagnosis,
            'diagnoses': self.diagnoses or [],
            'doctor_name': self.doctor_name,
            'medical_history': self.medical_history,
            'allergies': self.allergies or [],
            'medications': self.medications or [],
            'current_medications': self.current_medications or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Bed(db.Model):
    __tablename__ = 'beds'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    number = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(128), nullable=False)
    ward = db.Column(db.String(64))
    status = db.Column(db.String(32), default='available')
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'hospital_id': self.hospital_id,
            'number': self.number,
            'department': self.department,
            'ward': self.ward,
            'status': self.status,
            'patient_id': self.patient_id,
            'patient_name': self.patient.full_name if self.patient else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PatientVital(db.Model):
    __tablename__ = 'patient_vitals'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)
    blood_pressure = db.Column(db.String(16))
    heart_rate = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    oxygen_saturation = db.Column(db.Float)
    respiratory_rate = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    bmi = db.Column(db.Float)
    notes = db.Column(db.Text)
    recorded_by = db.Column(db.String(128))
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'blood_pressure': self.blood_pressure,
            'heart_rate': self.heart_rate,
            'temperature': self.temperature,
            'oxygen_saturation': self.oxygen_saturation,
            'respiratory_rate': self.respiratory_rate,
            'weight': self.weight,
            'height': self.height,
            'bmi': self.bmi,
            'notes': self.notes,
            'recorded_by': self.recorded_by,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ClinicalNote(db.Model):
    __tablename__ = 'clinical_notes'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)
    type = db.Column(db.String(64))
    summary = db.Column(db.String(256))
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(128))
    attachments = db.Column(db.JSON, default=list)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'type': self.type,
            'summary': self.summary,
            'content': self.content,
            'author': self.author,
            'attachments': self.attachments,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class LabResult(db.Model):
    __tablename__ = 'lab_results'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)
    test_name = db.Column(db.String(128), nullable=False)
    ordered_by = db.Column(db.String(128))
    ordered_date = db.Column(db.DateTime, default=datetime.utcnow)
    performed_date = db.Column(db.DateTime)
    status = db.Column(db.String(32), default='Pending')
    results = db.Column(db.JSON, default=list)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'test_name': self.test_name,
            'ordered_by': self.ordered_by,
            'ordered_date': self.ordered_date.isoformat() if self.ordered_date else None,
            'performed_date': self.performed_date.isoformat() if self.performed_date else None,
            'status': self.status,
            'results': self.results,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ImagingStudy(db.Model):
    __tablename__ = 'imaging_studies'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)
    study_type = db.Column(db.String(128), nullable=False)
    modality = db.Column(db.String(64))
    ordered_by = db.Column(db.String(128))
    ordered_date = db.Column(db.DateTime, default=datetime.utcnow)
    performed_date = db.Column(db.DateTime)
    status = db.Column(db.String(32), default='Scheduled')
    findings = db.Column(db.Text)
    impressions = db.Column(db.Text)
    images = db.Column(db.JSON, default=list)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'study_type': self.study_type,
            'modality': self.modality,
            'ordered_by': self.ordered_by,
            'ordered_date': self.ordered_date.isoformat() if self.ordered_date else None,
            'performed_date': self.performed_date.isoformat() if self.performed_date else None,
            'status': self.status,
            'findings': self.findings,
            'impressions': self.impressions,
            'images': self.images,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)
    medication = db.Column(db.String(128), nullable=False)
    dosage = db.Column(db.String(64))
    frequency = db.Column(db.String(64))
    route = db.Column(db.String(64))
    prescribed_by = db.Column(db.String(128))
    prescribed_date = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(32), default='Active')
    notes = db.Column(db.Text)
    is_high_alert = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'medication': self.medication,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'route': self.route,
            'prescribed_by': self.prescribed_by,
            'prescribed_date': self.prescribed_date.isoformat() if self.prescribed_date else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'notes': self.notes,
            'is_high_alert': self.is_high_alert,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PatientTimeline(db.Model):
    __tablename__ = 'patient_timelines'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)
    event_type = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'event_type': self.event_type,
            'description': self.description,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ============================================
# SAFETY DEPARTMENT MODELS
# ============================================

class SafetyEquipment(db.Model):
    __tablename__ = 'safety_equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    location = db.Column(db.String(256))
    quantity = db.Column(db.Integer, default=0)
    status = db.Column(db.String(32), default='Good')
    last_inspection_date = db.Column(db.DateTime)
    next_inspection_date = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime)
    manufacturer = db.Column(db.String(128))
    model_number = db.Column(db.String(64))
    serial_number = db.Column(db.String(64))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    department = db.relationship('Department')


class LabSafety(db.Model):
    __tablename__ = 'lab_safety'
    
    id = db.Column(db.Integer, primary_key=True)
    lab_safety_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    category = db.Column(db.String(64), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    location = db.Column(db.String(256))
    status = db.Column(db.String(32), default='Compliant')
    inspection_date = db.Column(db.DateTime)
    next_inspection_date = db.Column(db.DateTime)
    findings = db.Column(db.Text)
    corrective_actions = db.Column(db.Text)
    chemicals = db.Column(db.Text)
    safety_equipment = db.Column(db.Text)
    risk_level = db.Column(db.String(32))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    department = db.relationship('Department')


# ============================================
# ACCREDITATION & QUALITY MODELS
# ============================================

class Accreditation(db.Model):
    __tablename__ = 'accreditations'
    
    id = db.Column(db.Integer, primary_key=True)
    accreditation_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    standard = db.Column(db.String(128), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    status = db.Column(db.String(32), default='Pending')
    score = db.Column(db.Float)
    requirements_total = db.Column(db.Integer)
    requirements_completed = db.Column(db.Integer)
    audit_date = db.Column(db.DateTime)
    next_audit_date = db.Column(db.DateTime)
    last_audit_date = db.Column(db.DateTime)
    auditor = db.Column(db.String(128))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QualityIndicator(db.Model):
    __tablename__ = 'quality_indicators'
    
    id = db.Column(db.Integer, primary_key=True)
    indicator_code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(64))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    target = db.Column(db.Float)
    current_value = db.Column(db.Float)
    benchmark = db.Column(db.Float)
    trend = db.Column(db.String(32))
    unit = db.Column(db.String(32))
    measurement_frequency = db.Column(db.String(32))
    last_updated = db.Column(db.DateTime)
    department = db.Column(db.String(128))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================
# PATIENT SAFETY GOALS
# ============================================

class PatientSafetyGoal(db.Model):
    __tablename__ = 'patient_safety_goals'
    
    id = db.Column(db.Integer, primary_key=True)
    goal_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    goal = db.Column(db.Text, nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    department = db.Column(db.String(128))
    compliance_rate = db.Column(db.Float)
    target_rate = db.Column(db.Float)
    status = db.Column(db.String(32))
    last_audit_date = db.Column(db.DateTime)
    next_audit_date = db.Column(db.DateTime)
    responsible_person = db.Column(db.String(128))
    actions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AdverseEvent(db.Model):
    __tablename__ = 'adverse_events'
    
    id = db.Column(db.Integer, primary_key=True)
    event_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    type = db.Column(db.String(64), nullable=False)
    severity = db.Column(db.String(32))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    description = db.Column(db.Text)
    status = db.Column(db.String(32), default='Under Investigation')
    event_date = db.Column(db.DateTime, nullable=False)
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    root_cause = db.Column(db.Text)
    corrective_actions = db.Column(db.Text)
    preventive_measures = db.Column(db.Text)
    resolved_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    reporter = db.relationship('User', foreign_keys=[reported_by])
    department = db.relationship('Department')
    patient = db.relationship('Patient')


# ============================================
# STAFF COMPETENCY
# ============================================

class StaffCompetency(db.Model):
    __tablename__ = 'staff_competencies'
    
    id = db.Column(db.Integer, primary_key=True)
    competency_code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    department = db.Column(db.String(128))
    staff_member_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    compliance_rate = db.Column(db.Float)
    status = db.Column(db.String(32))
    date_obtained = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime)
    next_renewal_date = db.Column(db.DateTime)
    last_training_date = db.Column(db.DateTime)
    training_provider = db.Column(db.String(128))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    staff_member = db.relationship('User', foreign_keys=[staff_member_id])



class HospitalDepartment(db.Model):
    __tablename__ = 'hospital_departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64))
    risk_level = db.Column(db.String(32))
    location = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class InfectionControlProtocol(db.Model):
    __tablename__ = 'infection_control_protocols'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('hospital_departments.id'), nullable=False)
    standard_precautions = db.Column(db.Text)
    transmission_precautions = db.Column(db.Text)
    ppe_requirements = db.Column(db.Text)
    cleaning_procedures = db.Column(db.Text)
    compliance_rate = db.Column(db.Float)
    last_audit_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Hazard(db.Model):
    __tablename__ = 'hazards'
    
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False, index=True)
    name = db.Column(db.String(256), nullable=False)
    type = db.Column(db.String(64))  # Biological, Chemical, Physical, etc.
    risk_level = db.Column(db.String(32))  # Low, Medium, High, Critical
    description = db.Column(db.Text)
    location = db.Column(db.String(256))
    control_measures = db.Column(db.Text)
    last_assessment = db.Column(db.DateTime)
    next_assessment = db.Column(db.DateTime)
    status = db.Column(db.String(32), default='active')  # active, mitigated, eliminated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False, index=True)
    name = db.Column(db.String(256), nullable=False)
    type = db.Column(db.String(128))
    model = db.Column(db.String(128))
    serial_number = db.Column(db.String(128))
    status = db.Column(db.String(32), default='Operational')  # Operational, Maintenance, Out of Service
    last_maintenance = db.Column(db.DateTime)
    next_maintenance = db.Column(db.DateTime)
    calibration_due = db.Column(db.DateTime)
    warranty_expiry = db.Column(db.DateTime)
    purchase_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Compliance(db.Model):
    __tablename__ = 'compliances'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    standard = db.Column(db.String(128))  # ISO, JCIA, etc.
    requirement = db.Column(db.String(256))
    status = db.Column(db.String(32))  # Compliant, Non-Compliant, Partial
    evidence = db.Column(db.Text)
    last_audit = db.Column(db.DateTime)
    next_audit = db.Column(db.DateTime)
    auditor = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AirQualitySensor(db.Model):
    __tablename__ = 'air_quality_sensors'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(64), unique=True, nullable=False, index=True)
    
    # New fields
    name = db.Column(db.String(100), nullable=True)
    sensor_type = db.Column(db.String(50), default='air_quality')
    min_range = db.Column(db.Float, default=0)
    max_range = db.Column(db.Float, default=500)
    unit = db.Column(db.String(20), default='AQI')
    compliance_score = db.Column(db.Float, default=100.0)
    
    # Existing fields
    location = db.Column(db.String(128))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    installation_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(32), default='active')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    department = db.Column(db.String(64))
    calibration_data = db.Column(db.Text)
    last_calibration = db.Column(db.DateTime)
    next_calibration = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ✅ ADD THIS - company_id for scoping
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True, index=True)
    
    # Relationships
    user = db.relationship('User', backref='air_quality_sensors')
    company = db.relationship('Company', backref='air_quality_sensors')
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'name': self.name,
            'sensor_type': self.sensor_type,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'min_range': self.min_range,
            'max_range': self.max_range,
            'unit': self.unit,
            'compliance_score': self.compliance_score,
            'status': self.status,
            'department': self.department,
            'installation_date': self.installation_date.isoformat() if self.installation_date else None,
            'last_calibration': self.last_calibration.isoformat() if self.last_calibration else None,
            'next_calibration': self.next_calibration.isoformat() if self.next_calibration else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_id': self.user_id,
            'company_id': self.company_id  # ✅ Added
        }

class AirQualityReading(db.Model):
    __tablename__ = 'air_quality_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('air_quality_sensors.id'), nullable=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    pm2_5 = db.Column(db.Float)
    pm10 = db.Column(db.Float)
    co = db.Column(db.Float)
    no2 = db.Column(db.Float)
    o3 = db.Column(db.Float)
    so2 = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    aqi = db.Column(db.Integer)
    aqi_category = db.Column(db.String(32))
    raw_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WaterSamplingSite(db.Model):
    __tablename__ = 'water_sampling_sites'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(256))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    water_type = db.Column(db.String(64))  # drinking, waste, surface, ground
    frequency = db.Column(db.String(32))  # daily, weekly, monthly
    
    # ✅ ADD company_id
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='water_sampling_sites')
    company = db.relationship('Company', backref='water_sampling_sites')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'water_type': self.water_type,
            'frequency': self.frequency,
            'user_id': self.user_id,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
class WaterSample(db.Model):
    __tablename__ = 'water_samples'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # ✅ Make site_id nullable (allow NULL)
    site_id = db.Column(db.Integer, db.ForeignKey('water_sampling_sites.id'), nullable=True, index=True)
    site_name = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    sample_type = db.Column(db.String(50), default='water')
    
    collection_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    analysis_time = db.Column(db.DateTime)
    collected_by = db.Column(db.String(128))
    
    # Water quality parameters
    temperature = db.Column(db.Float)
    ph = db.Column(db.Float)
    turbidity = db.Column(db.Float)
    conductivity = db.Column(db.Float)
    tds = db.Column(db.Float)
    dissolved_oxygen = db.Column(db.Float)
    bod = db.Column(db.Float)
    cod = db.Column(db.Float)
    lead = db.Column(db.Float)
    mercury = db.Column(db.Float)
    arsenic = db.Column(db.Float)
    coliform_count = db.Column(db.Float)
    e_coli = db.Column(db.Boolean)
    
    # Compliance
    compliant = db.Column(db.Boolean, default=True)
    violations = db.Column(db.Text)
    lab_report_url = db.Column(db.String(256))
    notes = db.Column(db.Text)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='water_samples')
    company = db.relationship('Company', backref='water_samples')
    site = db.relationship('WaterSamplingSite', backref='water_samples')
    
    def to_dict(self):
        return {
            'id': self.id,
            'site_id': self.site_id,
            'site_name': self.site_name,
            'location': self.location,
            'sample_type': self.sample_type,
            'collection_time': self.collection_time.isoformat() if self.collection_time else None,
            'analysis_time': self.analysis_time.isoformat() if self.analysis_time else None,
            'collected_by': self.collected_by,
            'temperature': self.temperature,
            'ph': self.ph,
            'turbidity': self.turbidity,
            'conductivity': self.conductivity,
            'tds': self.tds,
            'dissolved_oxygen': self.dissolved_oxygen,
            'bod': self.bod,
            'cod': self.cod,
            'lead': self.lead,
            'mercury': self.mercury,
            'arsenic': self.arsenic,
            'coliform_count': self.coliform_count,
            'e_coli': self.e_coli,
            'compliant': self.compliant,
            'violations': self.violations,
            'lab_report_url': self.lab_report_url,
            'notes': self.notes,
            'user_id': self.user_id,
            'company_id': self.company_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
class MonitoringStation(db.Model):
    __tablename__ = 'monitoring_stations'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64))  # Air, Water, Surface, Radiation
    location = db.Column(db.String(256))
    description = db.Column(db.Text)
    status = db.Column(db.String(32), default='Active')  # Active, Inactive, Maintenance
    parameters = db.Column(db.Text)  # JSON list of parameters measured
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MonitoringReading(db.Model):
    __tablename__ = 'monitoring_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('monitoring_stations.id'), nullable=False, index=True)
    parameter = db.Column(db.String(64), nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MonitoringAlert(db.Model):
    __tablename__ = 'monitoring_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('monitoring_stations.id'), nullable=False, index=True)
    parameter = db.Column(db.String(64))
    value = db.Column(db.Float)
    threshold = db.Column(db.Float)
    severity = db.Column(db.String(32))  # Warning, Alert, Critical
    message = db.Column(db.Text)
    status = db.Column(db.String(32), default='Active')  # Active, Acknowledged, Resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    acknowledged_at = db.Column(db.DateTime)
    acknowledged_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolved_at = db.Column(db.DateTime)

# ===== SAFETY & COMPLIANCE =====


class InspectionItem(db.Model):
    __tablename__ = 'inspection_items'
    
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('safety_inspections.id'), nullable=False, index=True)
    item_number = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirement = db.Column(db.Text)
    compliance_status = db.Column(db.String(50), default='not_assessed')  # compliant, non_compliant, not_applicable
    findings = db.Column(db.Text)
    risk_level = db.Column(db.String(50))
    corrective_action = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(50), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assignee = db.relationship('User', foreign_keys=[assigned_to])

class CompliancePolicy(db.Model):
    __tablename__ = 'compliance_policies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    policy_number = db.Column(db.String(64))
    category = db.Column(db.String(64))
    version = db.Column(db.String(32))
    effective_date = db.Column(db.DateTime)
    review_date = db.Column(db.DateTime)
    content = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('hospital_departments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ComplianceChecklist(db.Model):
    __tablename__ = 'compliance_checklists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    frequency = db.Column(db.String(32))  # daily, weekly, monthly, quarterly
    department_id = db.Column(db.Integer, db.ForeignKey('hospital_departments.id'))
    items = db.Column(db.Text)  # JSON string of checklist items
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChecklistResponse(db.Model):
    __tablename__ = 'checklist_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.Integer, db.ForeignKey('compliance_checklists.id'), nullable=False, index=True)
    responses = db.Column(db.Text)  # JSON string of responses
    completed_by = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('hospital_departments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    score = db.Column(db.Float)
    status = db.Column(db.String(32))  # passed, failed, needs_improvement

class AuditFinding(db.Model):
    __tablename__ = 'audit_findings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(32))
    standard_reference = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('hospital_departments.id'))
    due_date = db.Column(db.DateTime)
    resolved = db.Column(db.Boolean, default=False)
    resolution_notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditActionPlan(db.Model):
    __tablename__ = 'audit_action_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    finding_id = db.Column(db.Integer, db.ForeignKey('audit_findings.id'), nullable=False, index=True)
    action = db.Column(db.Text)
    responsible_person = db.Column(db.String(128))
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(32))  # not_started, in_progress, completed, overdue
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



class RiskAssessment(db.Model):
    __tablename__ = 'risk_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'))
    assessed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_date = db.Column(db.DateTime, nullable=False)
    next_assessment_date = db.Column(db.DateTime)
    overall_risk_level = db.Column(db.String(50))
    status = db.Column(db.String(50), default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Existing relationships
    assessor = db.relationship('User', foreign_keys=[assessed_by])
    department = db.relationship('Department')
    hospital = db.relationship('Hospital')
    industry = db.relationship('Industry')
    items = db.relationship('RiskAssessmentItem', back_populates='assessment', cascade='all, delete-orphan')
    
    # ADD THESE NEW RELATIONSHIPS:
    attachments = db.relationship('RiskAssessmentAttachment', back_populates='assessment', cascade='all, delete-orphan')
    comments = db.relationship('RiskAssessmentComment', back_populates='assessment', cascade='all, delete-orphan')
    history = db.relationship('RiskAssessmentHistory', back_populates='assessment', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'assessment_number': self.assessment_number,
            'title': self.title,
            'description': self.description,
            'department_id': self.department_id,
            'hospital_id': self.hospital_id,
            'industry_id': self.industry_id,
            'assessed_by': self.assessed_by,
            'assessment_date': self.assessment_date.isoformat() if self.assessment_date else None,
            'next_assessment_date': self.next_assessment_date.isoformat() if self.next_assessment_date else None,
            'overall_risk_level': self.overall_risk_level,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Include relationships
            'items': [item.to_dict() for item in self.items],
            'attachment_count': len(self.attachments) if hasattr(self, 'attachments') else 0,
            'comment_count': len(self.comments) if hasattr(self, 'comments') else 0,
            'assessor_name': self.assessor.name if self.assessor else None,
            'department_name': self.department.name if self.department else None
        }
    


class RiskAssessmentAttachment(db.Model):
    __tablename__ = 'risk_assessment_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('risk_assessments.id'), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    file_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    assessment = db.relationship('RiskAssessment', back_populates='attachments')
    uploader = db.relationship('User', foreign_keys=[uploaded_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'filename': self.filename,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'description': self.description,
            'uploaded_by': self.uploaded_by,
            'uploader_name': self.uploader.name if self.uploader else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'download_url': f'/api/risk-assessments/{self.assessment_id}/attachments/{self.id}/download'
        }

class RiskAssessmentComment(db.Model):
    __tablename__ = 'risk_assessment_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('risk_assessments.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    assessment = db.relationship('RiskAssessment', back_populates='comments')
    user = db.relationship('User', foreign_keys=[user_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class RiskAssessmentHistory(db.Model):
    __tablename__ = 'risk_assessment_history'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('risk_assessments.id'), nullable=False, index=True)
    action = db.Column(db.String(100), nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    change_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    assessment = db.relationship('RiskAssessment', back_populates='history')
    changer = db.relationship('User', foreign_keys=[changed_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'action': self.action,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'changed_by': self.changed_by,
            'changer_name': self.changer.name if self.changer else None,
            'change_reason': self.change_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class RiskAssessmentTemplate(db.Model):
    __tablename__ = 'risk_assessment_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    template_data = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    industry = db.relationship('Industry')
    department = db.relationship('Department')
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'industry_id': self.industry_id,
            'department_id': self.department_id,
            'industry_name': self.industry.name if self.industry else None,
            'department_name': self.department.name if self.department else None,
            'template_data': self.template_data,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'created_by': self.created_by,
            'creator_name': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class SafetyInspection(db.Model):
    __tablename__ = 'safety_inspections'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    inspection_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100), nullable=False)  # routine, scheduled, special, audit
    area = db.Column(db.String(255))
    department = db.Column(db.String(100))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'))  # NEW FIELD
    conducted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    inspection_date = db.Column(db.DateTime, nullable=False)
    next_inspection_date = db.Column(db.DateTime)
    total_items = db.Column(db.Integer, default=0)
    compliant_items = db.Column(db.Integer, default=0)
    non_compliant_items = db.Column(db.Integer, default=0)
    compliance_rate = db.Column(db.Float)
    overall_rating = db.Column(db.String(50))  # excellent, good, fair, poor
    findings_summary = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    status = db.Column(db.String(50), default='draft')  # draft, in_progress, completed, approved
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inspector = db.relationship('User', foreign_keys=[conducted_by])
    hospital = db.relationship('Hospital', backref=db.backref('safety_inspections', lazy=True))
    industry = db.relationship('Industry')  # NEW RELATIONSHIP
    items = db.relationship('InspectionItem', backref='inspection', lazy=True, cascade='all, delete-orphan')



class RiskAssessmentItem(db.Model):
    __tablename__ = 'risk_assessment_items'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('risk_assessments.id'), nullable=False, index=True)
    hazard_description = db.Column(db.Text, nullable=False)
    existing_controls = db.Column(db.Text)
    likelihood = db.Column(db.String(50))  # rare, unlikely, possible, likely, almost_certain
    severity = db.Column(db.String(50))  # insignificant, minor, moderate, major, catastrophic
    risk_level = db.Column(db.String(50))  # low, medium, high, extreme
    recommended_actions = db.Column(db.Text)
    responsible_person = db.Column(db.String(128))
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    assessment = db.relationship('RiskAssessment', back_populates='items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'hazard_description': self.hazard_description,
            'existing_controls': self.existing_controls,
            'likelihood': self.likelihood,
            'severity': self.severity,
            'risk_level': self.risk_level,
            'recommended_actions': self.recommended_actions,
            'responsible_person': self.responsible_person,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
# ===== EMERGENCY PREPAREDNESS MODELS =====

class EmergencyPlan(db.Model):
    __tablename__ = 'emergency_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    emergency_type = db.Column(db.String(100), nullable=False)  # fire, earthquake, flood, etc.
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    version = db.Column(db.String(32))
    effective_date = db.Column(db.DateTime)
    review_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='draft')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User')
    department = db.relationship('Department')
    hospital = db.relationship('Hospital')
    procedures = db.relationship('EmergencyProcedure', back_populates='plan', cascade='all, delete-orphan')

class EmergencyProcedure(db.Model):
    __tablename__ = 'emergency_procedures'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('emergency_plans.id'), nullable=False, index=True)
    step_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    responsible_role = db.Column(db.String(128))
    estimated_time = db.Column(db.Integer)  # in minutes
    critical = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    plan = db.relationship('EmergencyPlan', back_populates='procedures')

class EmergencyDrill(db.Model):
    __tablename__ = 'emergency_drills'
    
    id = db.Column(db.Integer, primary_key=True)
    drill_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    emergency_type = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    drill_date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer)
    participants_count = db.Column(db.Integer)
    coordinator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    objectives = db.Column(db.Text)
    outcomes = db.Column(db.Text)
    score = db.Column(db.Float)  # 0-100
    status = db.Column(db.String(50), default='completed')  # scheduled, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    coordinator = db.relationship('User', foreign_keys=[coordinator_id])
    department = db.relationship('Department')
    hospital = db.relationship('Hospital')

# ===== WASTE MANAGEMENT MODELS =====

class WasteCategory(db.Model):
    __tablename__ = 'waste_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.Text)
    color_code = db.Column(db.String(32))
    disposal_method = db.Column(db.Text)
    hazard_level = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    company_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    
    # Subscription
    plan = db.Column(db.String(50), nullable=False, default='free')
    subscription_status = db.Column(db.String(50), default='active')
    subscription_starts_at = db.Column(db.DateTime, default=datetime.utcnow)
    subscription_ends_at = db.Column(db.DateTime, nullable=True)
    trial_ends_at = db.Column(db.DateTime, nullable=True)
    trial_plan = db.Column(db.String(32), nullable=True)
    billing_cycle = db.Column(db.String(20), default='1_month')
    payment_method = db.Column(db.String(50), nullable=True)
    payment_gateway = db.Column(db.String(50), nullable=True)
    payment_id = db.Column(db.String(100), nullable=True)
    last_payment_date = db.Column(db.DateTime, nullable=True)
    next_payment_date = db.Column(db.DateTime, nullable=True)
    
    # Company details
    industry = db.Column(db.String(100), nullable=True)
    company_size = db.Column(db.String(50), default='small')
    employee_count = db.Column(db.Integer, default=0)
    country = db.Column(db.String(64), default='default')
    currency = db.Column(db.String(16), default='USD')
    timezone = db.Column(db.String(64), default='UTC')
    address = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    logo_url = db.Column(db.String(512), nullable=True)
    
    # Features & limits
    features = db.Column(db.Text, nullable=True)
    custom_limits = db.Column(db.Text, nullable=True)
    
    # Usage tracking
    monthly_api_calls_used = db.Column(db.Integer, default=0)
    monthly_ai_requests_used = db.Column(db.Integer, default=0)
    monthly_uploads_used = db.Column(db.Integer, default=0)
    monthly_video_minutes_used = db.Column(db.Integer, default=0)
    monthly_incidents_reported = db.Column(db.Integer, default=0)
    usage_reset_date = db.Column(db.DateTime, default=datetime.utcnow)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=True, index=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_trial = db.Column(db.Boolean, default=False)
    is_enterprise = db.Column(db.Boolean, default=False)
    is_suspended = db.Column(db.Boolean, default=False)
    
    # Admin & ownership
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Metadata
    description = db.Column(db.Text, nullable=True)
    tags = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ✅ RELATIONSHIPS with foreign_keys specified
    users = db.relationship('User', foreign_keys='User.company_id', back_populates='company', lazy=True)
    departments = db.relationship('Department', foreign_keys='Department.company_id', back_populates='company', lazy=True, cascade='all, delete-orphan')
    projects = db.relationship('Project', foreign_keys='Project.company_id', back_populates='company', lazy=True, cascade='all, delete-orphan')
    incidents = db.relationship('Incident', foreign_keys='Incident.company_id', back_populates='company', lazy=True, cascade='all, delete-orphan')
    
    # These reference User but are separate relationships
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_companies')
    updater = db.relationship('User', foreign_keys=[updated_by])
    owner = db.relationship('User', foreign_keys=[owner_id], backref='owned_companies')
    hospital = db.relationship('Hospital', foreign_keys=[hospital_id], backref='companies', lazy=True)
    subscription_history = db.relationship('CompanySubscriptionHistory', backref='company', lazy=True, cascade='all, delete-orphan')
    
    
    def to_dict(self):
        """Convert company to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'company_number': self.company_number,
            'email': self.email,
            'phone': self.phone,
            'plan': self.plan,
            'subscription_status': self.subscription_status,
            'subscription_starts_at': self.subscription_starts_at.isoformat() if self.subscription_starts_at else None,
            'subscription_ends_at': self.subscription_ends_at.isoformat() if self.subscription_ends_at else None,
            'trial_ends_at': self.trial_ends_at.isoformat() if self.trial_ends_at else None,
            'trial_plan': self.trial_plan,
            'billing_cycle': self.billing_cycle,
            'payment_method': self.payment_method,
            'payment_gateway': self.payment_gateway,
            'last_payment_date': self.last_payment_date.isoformat() if self.last_payment_date else None,
            'next_payment_date': self.next_payment_date.isoformat() if self.next_payment_date else None,
            'industry': self.industry,
            'company_size': self.company_size,
            'employee_count': self.employee_count,
            'country': self.country,
            'currency': self.currency,
            'timezone': self.timezone,
            'address': self.address,
            'website': self.website,
            'logo_url': self.logo_url,
            'features': json.loads(self.features) if self.features else [],
            'custom_limits': json.loads(self.custom_limits) if self.custom_limits else {},
            'is_active': self.is_active,
            'is_trial': self.is_trial,
            'is_enterprise': self.is_enterprise,
            'is_suspended': self.is_suspended,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_count': len(self.users) if self.users else 0,
            'department_count': len(self.departments) if self.departments else 0,
            'project_count': len(self.projects) if self.projects else 0,
            'incident_count': len(self.incidents) if self.incidents else 0,
            'usage': {
                'api_calls_used': self.monthly_api_calls_used,
                'ai_requests_used': self.monthly_ai_requests_used,
                'uploads_used': self.monthly_uploads_used,
                'video_minutes_used': self.monthly_video_minutes_used,
                'incidents_reported': self.monthly_incidents_reported,
                'usage_reset_date': self.usage_reset_date.isoformat() if self.usage_reset_date else None
            }
        }
    
    def get_plan_limits(self):
        """Get limits based on plan"""
        limits = {
            'free': {
                'max_users': 5,
                'max_projects': 10,
                'max_departments': 3,
                'max_incidents': 50,
                'api_calls_per_month': 100,
                'ai_requests_per_month': 10,
                'uploads_per_month': 50,
                'video_minutes_per_month': 60,
                'max_storage_mb': 100,
                'features': ['basic_analytics', 'incident_reporting']
            },
            'basic': {
                'max_users': 20,
                'max_projects': 50,
                'max_departments': 10,
                'max_incidents': 200,
                'api_calls_per_month': 1000,
                'ai_requests_per_month': 100,
                'uploads_per_month': 500,
                'video_minutes_per_month': 300,
                'max_storage_mb': 500,
                'features': ['basic_analytics', 'incident_reporting', 'document_upload', 'team_management']
            },
            'pro': {
                'max_users': 100,
                'max_projects': 200,
                'max_departments': 20,
                'max_incidents': 500,
                'api_calls_per_month': 5000,
                'ai_requests_per_month': 500,
                'uploads_per_month': 2000,
                'video_minutes_per_month': 1000,
                'max_storage_mb': 2000,
                'features': ['basic_analytics', 'incident_reporting', 'document_upload', 'team_management',
                           'advanced_analytics', 'ai_predictions', 'custom_reports', 'api_access', 
                           'video_analysis', 'real_time_monitoring']
            },
            'enterprise': {
                'max_users': -1,  # Unlimited
                'max_projects': -1,
                'max_departments': -1,
                'max_incidents': -1,
                'api_calls_per_month': -1,
                'ai_requests_per_month': -1,
                'uploads_per_month': -1,
                'video_minutes_per_month': -1,
                'max_storage_mb': -1,
                'features': ['all']
            }
        }
        
        # If there are custom limits, merge them
        plan_limits = limits.get(self.plan, limits['free']).copy()
        if self.custom_limits:
            custom = json.loads(self.custom_limits) if isinstance(self.custom_limits, str) else self.custom_limits
            plan_limits.update(custom)
        
        return plan_limits
    
    def get_remaining_limits(self):
        """Get remaining usage limits"""
        plan_limits = self.get_plan_limits()
        
        def get_remaining(limit, used):
            if limit == -1:  # Unlimited
                return float('inf')
            return max(0, limit - used)
        
        return {
            'api_calls_remaining': get_remaining(plan_limits.get('api_calls_per_month', 0), self.monthly_api_calls_used),
            'ai_requests_remaining': get_remaining(plan_limits.get('ai_requests_per_month', 0), self.monthly_ai_requests_used),
            'uploads_remaining': get_remaining(plan_limits.get('uploads_per_month', 0), self.monthly_uploads_used),
            'video_minutes_remaining': get_remaining(plan_limits.get('video_minutes_per_month', 0), self.monthly_video_minutes_used),
            'incidents_remaining': get_remaining(plan_limits.get('max_incidents', 0), self.monthly_incidents_reported)
        }
    
    def has_feature(self, feature_name):
        """Check if company has a specific feature"""
        plan_limits = self.get_plan_limits()
        features = plan_limits.get('features', [])
        
        if 'all' in features:
            return True
        return feature_name in features
    
    def reset_monthly_usage(self):
        """Reset monthly usage counters"""
        now = datetime.utcnow()
        if now.month != self.usage_reset_date.month or now.year != self.usage_reset_date.year:
            self.monthly_api_calls_used = 0
            self.monthly_ai_requests_used = 0
            self.monthly_uploads_used = 0
            self.monthly_video_minutes_used = 0
            self.monthly_incidents_reported = 0
            self.usage_reset_date = now
            return True
        return False
    
    def increment_usage(self, usage_type, amount=1):
        """Increment usage counter"""
        self.reset_monthly_usage()
        
        if usage_type == 'api_calls':
            self.monthly_api_calls_used += amount
        elif usage_type == 'ai_requests':
            self.monthly_ai_requests_used += amount
        elif usage_type == 'uploads':
            self.monthly_uploads_used += amount
        elif usage_type == 'video_minutes':
            self.monthly_video_minutes_used += amount
        elif usage_type == 'incidents':
            self.monthly_incidents_reported += amount
        
        return True
    
    def is_trial_active(self):
        """Check if company is in trial period"""
        if not self.is_trial or not self.trial_ends_at:
            return False
        return datetime.utcnow() < self.trial_ends_at
    
    def can_add_user(self):
        """Check if company can add more users"""
        plan_limits = self.get_plan_limits()
        max_users = plan_limits.get('max_users', 0)
        if max_users == -1:  # Unlimited
            return True
        current_users = len(self.users) if self.users else 0
        return current_users < max_users
    
    def get_subscription_days_left(self):
        """Get days left in subscription"""
        if self.subscription_ends_at and self.subscription_status == 'active':
            days_left = (self.subscription_ends_at - datetime.utcnow()).days
            return max(0, days_left)
        return 0
    
    def is_expired(self):
        """Check if company subscription is expired"""
        if self.subscription_status == 'expired':
            return True
        if self.subscription_ends_at and datetime.utcnow() > self.subscription_ends_at:
            return True
        return False

class CompanySubscriptionHistory(db.Model):
    """Track company subscription changes"""
    __tablename__ = 'company_subscription_history'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    old_plan = db.Column(db.String(50), nullable=True)
    new_plan = db.Column(db.String(50), nullable=False)
    old_status = db.Column(db.String(50), nullable=True)
    new_status = db.Column(db.String(50), nullable=False)
    
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='company_subscription_changes')

class WasteDisposal(db.Model):
    __tablename__ = 'waste_disposals'
    
    id = db.Column(db.Integer, primary_key=True)
    disposal_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('waste_categories.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    weight_kg = db.Column(db.Float, nullable=False)
    volume_liters = db.Column(db.Float)
    disposal_date = db.Column(db.DateTime, nullable=False)
    disposed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    disposal_method = db.Column(db.String(128))
    disposal_company = db.Column(db.String(128))
    certificate_number = db.Column(db.String(128))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    category = db.relationship('WasteCategory')
    department = db.relationship('Department')
    disposer = db.relationship('User', foreign_keys=[disposed_by])

# ===== PATIENT SAFETY MODELS =====

class PatientSafetyIncident(db.Model):
    __tablename__ = 'patient_safety_incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    patient_id = db.Column(db.String(64))  # Pseudonymized patient identifier
    patient_age = db.Column(db.Integer)
    patient_gender = db.Column(db.String(20))
    incident_type = db.Column(db.String(100), nullable=False)  # fall, medication_error, etc.
    severity = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_occurred = db.Column(db.DateTime, nullable=False)
    date_reported = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    immediate_action = db.Column(db.Text)
    root_cause_analysis = db.Column(db.Text)
    preventive_measures = db.Column(db.Text)
    status = db.Column(db.String(50), default='reported')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reporter = db.relationship('User', foreign_keys=[reported_by])
    department = db.relationship('Department')

class FallRiskAssessment(db.Model):
    __tablename__ = 'fall_risk_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    patient_id = db.Column(db.String(64))
    patient_age = db.Column(db.Integer)
    patient_gender = db.Column(db.String(20))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    assessed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_date = db.Column(db.DateTime, nullable=False)
    risk_score = db.Column(db.Integer, nullable=False)
    risk_level = db.Column(db.String(50), nullable=False)  # low, medium, high
    factors = db.Column(db.Text)  # JSON of risk factors
    interventions = db.Column(db.Text)  # JSON of preventive interventions
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    assessor = db.relationship('User', foreign_keys=[assessed_by])
    department = db.relationship('Department')

# ===== MEDICATION SAFETY MODELS =====

class MedicationSafetyCheck(db.Model):
    __tablename__ = 'medication_safety_checks'
    
    id = db.Column(db.Integer, primary_key=True)
    check_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    patient_id = db.Column(db.String(64))
    medication_name = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(128))
    frequency = db.Column(db.String(128))
    route = db.Column(db.String(64))
    prescribed_by = db.Column(db.String(128))
    administered_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    check_type = db.Column(db.String(100))  # prescription, administration, reconciliation
    check_result = db.Column(db.String(50))  # passed, warning, error
    issues_found = db.Column(db.Text)
    corrective_action = db.Column(db.Text)
    check_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    administrator = db.relationship('User', foreign_keys=[administered_by])

# ===== ENVIRONMENTAL HEALTH MODELS =====

class IndoorAirQuality(db.Model):
    __tablename__ = 'indoor_air_quality'
    
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    measurement_date = db.Column(db.DateTime, nullable=False, index=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    co2_ppm = db.Column(db.Float)
    pm2_5 = db.Column(db.Float)
    pm10 = db.Column(db.Float)
    tvoc = db.Column(db.Float)  # Total Volatile Organic Compounds
    formaldehyde = db.Column(db.Float)
    air_exchange_rate = db.Column(db.Float)
    overall_rating = db.Column(db.String(50))
    measured_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    department = db.relationship('Department')
    measurer = db.relationship('User', foreign_keys=[measured_by])

class SurfaceSanitation(db.Model):
    __tablename__ = 'surface_sanitation'
    
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    surface_type = db.Column(db.String(128))
    test_date = db.Column(db.DateTime, nullable=False, index=True)
    atp_level = db.Column(db.Float)  # Adenosine Triphosphate level
    bacterial_count = db.Column(db.Float)
    cleaning_status = db.Column(db.String(50))  # clean, needs_cleaning, contaminated
    cleaning_agent = db.Column(db.String(128))
    tested_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    department = db.relationship('Department')
    tester = db.relationship('User', foreign_keys=[tested_by])

# ===== OCCUPATIONAL HEALTH MODELS =====

class EmployeeHealthScreening(db.Model):
    __tablename__ = 'employee_health_screenings'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    screening_type = db.Column(db.String(100), nullable=False)  # pre_employment, periodic, return_to_work
    screening_date = db.Column(db.DateTime, nullable=False, index=True)
    next_screening_date = db.Column(db.DateTime)
    blood_pressure = db.Column(db.String(32))
    heart_rate = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    bmi = db.Column(db.Float)
    vision_test = db.Column(db.String(128))
    hearing_test = db.Column(db.String(128))
    respiratory_test = db.Column(db.String(128))
    vaccination_status = db.Column(db.Text)  # JSON of vaccination records
    fitness_assessment = db.Column(db.String(50))  # fit, unfit, fit_with_restrictions
    restrictions = db.Column(db.Text)
    conducted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    employee = db.relationship('User', foreign_keys=[employee_id])
    conductor = db.relationship('User', foreign_keys=[conducted_by])

class WorkplaceErgonomics(db.Model):
    __tablename__ = 'workplace_ergonomics'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    workstation_id = db.Column(db.String(128), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    assessed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_date = db.Column(db.DateTime, nullable=False)
    posture_rating = db.Column(db.String(50))  # excellent, good, fair, poor
    equipment_rating = db.Column(db.String(50))
    lighting_rating = db.Column(db.String(50))
    noise_level = db.Column(db.String(50))
    recommendations = db.Column(db.Text)
    status = db.Column(db.String(50), default='assessed')  # assessed, implemented, verified
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = db.relationship('Department')
    assessor = db.relationship('User', foreign_keys=[assessed_by])

# ===== SAFETY PERFORMANCE MODELS =====

class SafetyKPI(db.Model):
    __tablename__ = 'safety_kpis'
    
    id = db.Column(db.Integer, primary_key=True)
    kpi_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    target_value = db.Column(db.Float)
    unit = db.Column(db.String(50))
    frequency = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    is_active = db.Column(db.Boolean, default=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = db.relationship('Department')
    creator = db.relationship('User')
    company = db.relationship('Company', backref='safety_kpis')
    
    # ✅ FIX: Use a unique name for the project relationship
    project = db.relationship('Project', back_populates='safety_kpi_records')

class SafetyKPIMeasurement(db.Model):
    __tablename__ = 'safety_kpi_measurements'
    
    id = db.Column(db.Integer, primary_key=True)
    kpi_id = db.Column(db.Integer, db.ForeignKey('safety_kpis.id'), nullable=False, index=True)
    period_start = db.Column(db.DateTime, nullable=False, index=True)
    period_end = db.Column(db.DateTime, nullable=False)
    measured_value = db.Column(db.Float, nullable=False)
    achievement_percentage = db.Column(db.Float)
    status = db.Column(db.String(50))
    notes = db.Column(db.Text)
    measured_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    kpi = db.relationship('SafetyKPI')
    measurer = db.relationship('User', foreign_keys=[measured_by])
    company = db.relationship('Company', backref='kpi_measurements')
    
    # ✅ FIX: Use a unique name for the project relationship
    project = db.relationship('Project', back_populates='safety_kpi_measurements')

# ===== DOCUMENT MANAGEMENT MODELS =====

class SafetyDocument(db.Model):
    __tablename__ = 'safety_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    document_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    version = db.Column(db.String(32), nullable=False)
    effective_date = db.Column(db.DateTime, nullable=False)
    review_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='draft')
    file_path = db.Column(db.String(512))
    
    # Use UploadedFile model (which exists)
    upload_file_id = db.Column(db.Integer, db.ForeignKey('uploaded_files.id'))
    upload_file = db.relationship('UploadedFile', foreign_keys=[upload_file_id], backref=db.backref('safety_documents', lazy='dynamic'))
    
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = db.relationship('Department', foreign_keys=[department_id])
    creator = db.relationship('User', foreign_keys=[created_by])
    approver = db.relationship('User', foreign_keys=[approved_by])
    upload_file = db.relationship('UploadedFile', foreign_keys=[upload_file_id])

class DocumentReview(db.Model):
    __tablename__ = 'document_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('safety_documents.id'), nullable=False, index=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    review_date = db.Column(db.DateTime, nullable=False)
    review_status = db.Column(db.String(50), default='pending')  # pending, reviewed, approved
    comments = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    next_review_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    document = db.relationship('SafetyDocument')
    reviewer = db.relationship('User', foreign_keys=[reviewer_id])

# Update the UserDocument model relationships
class UserDocument(db.Model):
    __tablename__ = 'user_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    document_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    
    # Status
    status = db.Column(db.String(20), default='pending')
    verification_notes = db.Column(db.Text)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    verified_at = db.Column(db.DateTime)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # FIXED: Use unique backref names to avoid conflicts
    user = db.relationship('User', foreign_keys=[user_id], backref='uploaded_documents')  # Changed backref name
    verifier = db.relationship('User', foreign_keys=[verified_by], backref='verified_user_documents')  # Changed backref name
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'document_type': self.document_type,
            'document_name': self.document_name,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'status': self.status,
            'verification_notes': self.verification_notes,
            'verified_by': self.verified_by,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# Update the UserNote model relationships
class UserNote(db.Model):
    __tablename__ = 'user_notes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note_type = db.Column(db.String(50), default='general')
    content = db.Column(db.Text, nullable=False)
    
    # Who created/updated
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Visibility
    is_internal = db.Column(db.Boolean, default=True)
    priority = db.Column(db.String(20), default='normal')
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # FIXED: Use unique backref names
    user = db.relationship('User', foreign_keys=[user_id], backref='profile_notes')  # Changed backref name
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_profile_notes')  # Changed backref name
    updater = db.relationship('User', foreign_keys=[updated_by], backref='updated_profile_notes')  # Changed backref name
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'note_type': self.note_type,
            'content': self.content,
            'created_by': self.created_by,
            'created_by_name': self.creator.name if self.creator else None,
            'updated_by': self.updated_by,
            'updated_by_name': self.updater.name if self.updater else None,
            'is_internal': self.is_internal,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'time_ago': get_time_ago(self.created_at) if self.created_at else None
        }


# Update the RequiredDocument model (no relationships to fix here)
class RequiredDocument(db.Model):
    __tablename__ = 'required_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Which user types need this document
    required_for_types = db.Column(db.JSON, default=list)
    
    # Which subscription plans need this document
    required_for_plans = db.Column(db.JSON, default=list)
    
    # Country-specific requirements
    countries = db.Column(db.JSON, default=list)
    
    # Requirements
    is_required = db.Column(db.Boolean, default=True)
    is_verification_required = db.Column(db.Boolean, default=True)
    
    # File requirements
    allowed_formats = db.Column(db.JSON, default=['pdf', 'jpg', 'jpeg', 'png'])
    max_file_size = db.Column(db.Integer, default=10*1024*1024)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_type': self.document_type,
            'display_name': self.display_name,
            'description': self.description,
            'required_for_types': self.required_for_types,
            'required_for_plans': self.required_for_plans,
            'countries': self.countries,
            'is_required': self.is_required,
            'is_verification_required': self.is_verification_required,
            'allowed_formats': self.allowed_formats,
            'max_file_size': self.max_file_size,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AISmartQueryLog(db.Model):
    """Log for smart AI queries"""
    __tablename__ = 'ai_smart_query_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message_length = db.Column(db.Integer, default=0)
    intent = db.Column(db.String(50))
    industry = db.Column(db.String(50))
    has_context = db.Column(db.Boolean, default=False)
    system_team_bypass = db.Column(db.Boolean, default=False)  # Add this field
    plan = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='ai_smart_queries')

class ApprovalNotification(db.Model):
    __tablename__ = 'approval_notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_type = db.Column(db.String(50), default='approval_confirmation')  # approval_confirmation, rejection_notice, etc.
    sent_via = db.Column(db.String(50), default='email')  # email, sms, push, in_app
    status = db.Column(db.String(20), default='pending')  # pending, sent, failed, delivered, read
    notes = db.Column(db.Text, nullable=True)
    email_subject = db.Column(db.String(255), nullable=True)
    email_content = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    read_at = db.Column(db.DateTime, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='approval_notifications')
    admin = db.relationship('User', foreign_keys=[admin_id], backref='sent_approval_notifications')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'admin_id': self.admin_id,
            'notification_type': self.notification_type,
            'sent_via': self.sent_via,
            'status': self.status,
            'notes': self.notes,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'error_message': self.error_message
        }
# ===== CONTINUOUS IMPROVEMENT MODELS =====

class ImprovementInitiative(db.Model):
    __tablename__ = 'improvement_initiatives'
    
    id = db.Column(db.Integer, primary_key=True)
    initiative_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # safety, quality, efficiency, cost
    priority = db.Column(db.String(50), default='medium')
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    proposed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    proposed_date = db.Column(db.DateTime, nullable=False)
    target_completion_date = db.Column(db.DateTime)
    actual_completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='proposed')  # proposed, approved, in_progress, completed
    benefits = db.Column(db.Text)
    challenges = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = db.relationship('Department')
    proposer = db.relationship('User', foreign_keys=[proposed_by])

class CorrectiveAction(db.Model):
    __tablename__ = 'corrective_actions'
    
    id = db.Column(db.Integer, primary_key=True)
    action_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    source_type = db.Column(db.String(100))  # incident, audit, inspection, risk_assessment
    source_id = db.Column(db.Integer)  # ID of the source record
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='open')  # open, in_progress, completed, overdue
    effectiveness = db.Column(db.String(50))  # effective, partially_effective, not_effective
    verification_date = db.Column(db.DateTime)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = db.relationship('Department')
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    verifier = db.relationship('User', foreign_keys=[verified_by])

class LoginAttempt(db.Model):
    __tablename__ = 'login_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, index=True)
    ip_address = db.Column(db.String(64), nullable=False, index=True)
    user_agent = db.Column(db.Text)
    success = db.Column(db.Boolean, default=False)
    failure_reason = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # FIXED: 'users.id'
    
    # Relationship
    user = db.relationship('User', backref=db.backref('login_attempts', lazy=True))

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)  # FIXED: 'users.id'
    session_id = db.Column(db.String(128), unique=True, nullable=False, index=True)
    ip_address = db.Column(db.String(64))
    user_agent = db.Column(db.Text)
    device_fingerprint = db.Column(db.String(255))
    location = db.Column(db.String(255))
    login_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    logout_time = db.Column(db.DateTime)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))

class SecuritySetting(db.Model):
    __tablename__ = 'security_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)  # FIXED: 'users.id'
    max_login_attempts = db.Column(db.Integer, default=5)
    lockout_duration_minutes = db.Column(db.Integer, default=30)
    require_2fa = db.Column(db.Boolean, default=False)
    session_timeout_minutes = db.Column(db.Integer, default=60)
    allow_concurrent_sessions = db.Column(db.Boolean, default=False)
    notify_on_new_device = db.Column(db.Boolean, default=True)
    last_password_change = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('security_settings', uselist=False))

class TemplateMarketplace(db.Model):
    __tablename__ = 'template_marketplace'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    price = db.Column(db.Float, default=0.0)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    download_count = db.Column(db.Integer, default=0)
    file_url = db.Column(db.String(500))
    preview_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref=db.backref('marketplace_templates', lazy=True))

# ===== AI LOGGING MODELS =====

class AIDocumentGeneration(db.Model):
    """Log for AI document generations (updated)"""
    __tablename__ = 'ai_document_generations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    document_type = db.Column(db.String(50))
    industry = db.Column(db.String(50))
    quality_level = db.Column(db.String(20))
    output_format = db.Column(db.String(20))
    generation_mode = db.Column(db.String(20))
    style = db.Column(db.String(50), default='professional')  # ADD THIS
    template_used = db.Column(db.Boolean, default=False)  # ADD THIS
    tokens_used = db.Column(db.Integer, default=0)
    cost_units = db.Column(db.Float, default=0.0)
    plan = db.Column(db.String(20))
    system_team_bypass = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='ai_document_generations')


class AIChatMessage(db.Model):
    """Log for AI chat messages"""
    __tablename__ = 'ai_chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    session_id = db.Column(db.String(100), index=True)
    message = db.Column(db.Text)
    response = db.Column(db.Text)
    industry = db.Column(db.String(50))
    query_type = db.Column(db.String(50))
    response_length = db.Column(db.Integer, default=0)
    tokens_used = db.Column(db.Integer, default=0)
    plan = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('ai_chat_messages', lazy=True))

class AIQueryLog(db.Model):
    """Log for AI queries (basic and advanced)"""
    __tablename__ = 'ai_query_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    query_type = db.Column(db.String(50))  # basic, advanced, smart
    industry = db.Column(db.String(50))
    message_length = db.Column(db.Integer, default=0)
    tokens_used = db.Column(db.Integer, default=0)
    uses_universal_knowledge = db.Column(db.Boolean, default=False)
    plan = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('ai_query_logs', lazy=True))


class AIHTMLPreview(db.Model):
    """Log for HTML previews"""
    __tablename__ = 'ai_html_previews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    document_type = db.Column(db.String(50))
    industry = db.Column(db.String(50))
    style = db.Column(db.String(50))
    preview_size = db.Column(db.Integer, default=0)
    plan = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('ai_html_previews', lazy=True))

class AIOptimizationLog(db.Model):
    """Log for AI optimizations"""
    __tablename__ = 'ai_optimization_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    optimization_type = db.Column(db.String(50))  # universal_training, model_update, etc.
    status = db.Column(db.String(20))  # started, completed, failed
    pre_optimization_data = db.Column(db.Text)
    post_optimization_data = db.Column(db.Text)
    estimated_duration_minutes = db.Column(db.Float, default=15.0)
    duration_minutes = db.Column(db.Float)
    error_message = db.Column(db.Text)
    plan = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    user = db.relationship('User', backref=db.backref('ai_optimization_logs', lazy=True))

class AIRiskAnalysisLog(db.Model):
    """Log for AI risk analyses"""
    __tablename__ = 'ai_risk_analysis_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    industry = db.Column(db.String(50))
    risk_level = db.Column(db.String(20))
    scenario_length = db.Column(db.Integer, default=0)
    plan = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('ai_risk_analyses', lazy=True))

class AIConsultationSession(db.Model):
    """Log for AI consultation sessions"""
    __tablename__ = 'ai_consultation_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    session_id = db.Column(db.String(100), unique=True, index=True)
    industry = db.Column(db.String(50))
    message_count = db.Column(db.Integer, default=0)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Float)
    plan = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('ai_consultation_sessions', lazy=True))

# Models for Monitoring System
class Camera(db.Model):
    __tablename__ = 'cameras'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    feed_url = db.Column(db.String(500))
    status = db.Column(db.String(20), default='active')  # active, inactive, maintenance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('cameras', lazy=True))

class ExportProgress(db.Model):
    __tablename__ = 'export_progress'
    id = db.Column(db.Integer, primary_key=True)
    export_job_id = db.Column(db.Integer, db.ForeignKey('export_jobs.id'), nullable=False)
    current_step = db.Column(db.String(100), nullable=False)
    total_steps = db.Column(db.Integer, nullable=False)
    current_step_number = db.Column(db.Integer, nullable=False)
    progress_percentage = db.Column(db.Float, default=0.0)
    status_message = db.Column(db.String(500))
    estimated_remaining = db.Column(db.Integer)  # seconds
    data_processed = db.Column(db.Integer)  # records processed
    total_data = db.Column(db.Integer)  # total records to process
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    export_job = db.relationship('ExportJob', backref=db.backref('progress', lazy=True))

class ProgressEvent(db.Model):
    __tablename__ = 'progress_events'
    id = db.Column(db.Integer, primary_key=True)
    progress_id = db.Column(db.Integer, db.ForeignKey('export_progress.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # step_started, step_completed, error, warning
    message = db.Column(db.Text)
    data = db.Column(db.JSON)  # Additional event data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    progress = db.relationship('ExportProgress', backref=db.backref('events', lazy=True))

class ExportJob(db.Model):
    __tablename__ = 'export_jobs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='pending')
    filters = db.Column(db.JSON)
    file_path = db.Column(db.String(500))
    file_size = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    download_count = db.Column(db.Integer, default=0)
    last_downloaded_at = db.Column(db.DateTime)
    last_downloaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Progress tracking fields
    progress_channel = db.Column(db.String(100))  # WebSocket channel for real-time updates
    current_progress = db.Column(db.Float, default=0.0)  # Cached progress for quick access
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('exports', lazy=True))
    downloader = db.relationship('User', foreign_keys=[last_downloaded_by])

class ExportDownloadLog(db.Model):
    __tablename__ = 'export_download_logs'
    id = db.Column(db.Integer, primary_key=True)
    export_id = db.Column(db.Integer, db.ForeignKey('export_jobs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    downloaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_agent = db.Column(db.Text)
    ip_address = db.Column(db.String(45))  # Support IPv6
    download_successful = db.Column(db.Boolean, default=True)

class FileAccessLog(db.Model):
    __tablename__ = 'file_access_logs'
    id = db.Column(db.Integer, primary_key=True)
    export_id = db.Column(db.Integer, db.ForeignKey('export_jobs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    accessed_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    bytes_served = db.Column(db.Integer)

# Add these to your models.py

# models.py

class EnvironmentalIncident(db.Model):
    __tablename__ = 'environmental_incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='reported')
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    impact = db.Column(db.Text)
    action_required = db.Column(db.Text)
    reported_by = db.Column(db.String(100), nullable=False)
    reported_date = db.Column(db.DateTime, default=datetime.utcnow)
    estimated_completion = db.Column(db.DateTime)
    actual_completion = db.Column(db.DateTime)
    department = db.Column(db.String(100))
    cost_estimate = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships (optional)
    company = db.relationship('Company', backref='environmental_incidents')
    user = db.relationship('User', backref='environmental_incidents')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'severity': self.severity,
            'status': self.status,
            'location': self.location,
            'description': self.description,
            'impact': self.impact,
            'action_required': self.action_required,
            'reported_by': self.reported_by,
            'reported_date': self.reported_date.isoformat() if self.reported_date else None,
            'estimated_completion': self.estimated_completion.isoformat() if self.estimated_completion else None,
            'actual_completion': self.actual_completion.isoformat() if self.actual_completion else None,
            'department': self.department,
            'cost_estimate': self.cost_estimate,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'company_id': self.company_id,
            'user_id': self.user_id
        }

# models.py - Add this model

class ComplianceViolation(db.Model):
    __tablename__ = 'compliance_violations'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    status = db.Column(db.String(20), default='open')     # open, investigating, resolved, closed
    category = db.Column(db.String(50))                   # environmental, safety, quality, etc.
    regulation = db.Column(db.String(100))                # OSHA, EPA, ISO, etc.
    location = db.Column(db.String(200))
    reported_by = db.Column(db.String(100))
    reported_date = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_date = db.Column(db.DateTime)
    resolution_notes = db.Column(db.Text)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = db.relationship('Company', backref='compliance_violations')
    user = db.relationship('User', backref='compliance_violations')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'severity': self.severity,
            'status': self.status,
            'category': self.category,
            'regulation': self.regulation,
            'location': self.location,
            'reported_by': self.reported_by,
            'reported_date': self.reported_date.isoformat() if self.reported_date else None,
            'resolved_date': self.resolved_date.isoformat() if self.resolved_date else None,
            'resolution_notes': self.resolution_notes,
            'company_id': self.company_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class SustainabilityGoal(db.Model):
    __tablename__ = 'sustainability_goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    
    goal = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    target = db.Column(db.String(500))
    current_value = db.Column(db.Float, default=0)
    target_value = db.Column(db.Float, default=100)
    unit = db.Column(db.String(20), default='%')
    progress = db.Column(db.Float, default=0)
    
    # ✅ This can now accept None (NULL)
    deadline = db.Column(db.DateTime, nullable=True)
    
    category = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')
    priority = db.Column(db.String(20), default='medium')
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='sustainability_goals')
    company = db.relationship('Company', backref='sustainability_goals')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_id': self.company_id,
            'goal': self.goal,
            'description': self.description,
            'target': self.target,
            'current_value': self.current_value,
            'target_value': self.target_value,
            'unit': self.unit,
            'progress_percentage': self.progress,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'category': self.category,
            'status': self.status,
            'priority': self.priority,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ComplianceReport(db.Model):
    __tablename__ = 'compliance_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(100), nullable=False)
    period = db.Column(db.String(50), nullable=False)  # "January 2024", "Q1 2024", etc.
    status = db.Column(db.String(20), nullable=False)  # draft, submitted, under_review, approved, rejected
    submitted_date = db.Column(db.DateTime)
    agency = db.Column(db.String(100), nullable=False)
    compliance_score = db.Column(db.Float, nullable=False)
    findings_count = db.Column(db.Integer, nullable=False, default=0)
    next_submission = db.Column(db.DateTime, nullable=False)
    file_path = db.Column(db.String(500))  # Path to uploaded report file
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# ===== DATABASE MODELS FOR ENVIRONMENTAL DATA =====

class EnvironmentalAlert(db.Model):
    __tablename__ = 'environmental_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    suggested_action = db.Column(db.Text)
    confidence_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged = db.Column(db.Boolean, default=False)
    acknowledged_at = db.Column(db.DateTime)
    acknowledged_by = db.Column(db.String(100))
    category = db.Column(db.String(50))
    location = db.Column(db.String(100))
    sensor_id = db.Column(db.String(100))
    trigger_value = db.Column(db.Float)
    threshold_value = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True, index=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=True, index=True)


class ComplianceAutomationSettings(db.Model):
    __tablename__ = 'compliance_automation_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    auto_reporting_enabled = db.Column(db.Boolean, default=True)
    ai_review_enabled = db.Column(db.Boolean, default=True)
    alert_thresholds = db.Column(db.Text)  # JSON string
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ComplianceDeadline(db.Model):
    __tablename__ = 'compliance_deadlines'
    
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    assigned_to = db.Column(db.String(100))

class EnergyConsumption(db.Model):
    __tablename__ = 'energy_consumption'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    consumption_kwh = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100))
    source = db.Column(db.String(50))  # electricity, gas, etc.

class TransportationLog(db.Model):
    __tablename__ = 'transportation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    distance_km = db.Column(db.Float, nullable=False)
    vehicle_type = db.Column(db.String(50))
    purpose = db.Column(db.String(100))





class ConstructionDocument(db.Model):
    """Construction-specific documents"""
    __tablename__ = 'construction_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    site_id = db.Column(db.Integer, db.ForeignKey('construction_sites.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    document_type = db.Column(db.String(100), nullable=False)  # 'safety_plan', 'inspection', 'permit', 'report'
    file_path = db.Column(db.String(500))
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    status = db.Column(db.String(50), default='draft')  # 'draft', 'submitted', 'approved', 'rejected'
    version = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'site_id': self.site_id,
            'title': self.title,
            'description': self.description,
            'document_type': self.document_type,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'status': self.status,
            'version': self.version,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class SafetyMetric(db.Model):
    """Safety performance metrics"""
    __tablename__ = 'safety_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    site_id = db.Column(db.Integer, db.ForeignKey('construction_sites.id'))
    metric_date = db.Column(db.Date, nullable=False)
    incidents_reported = db.Column(db.Integer, default=0)
    safety_inspections = db.Column(db.Integer, default=0)
    training_completions = db.Column(db.Integer, default=0)
    compliance_rate = db.Column(db.Float)  # 0.0 - 1.0
    equipment_uptime = db.Column(db.Float)  # 0.0 - 1.0
    risk_index = db.Column(db.Float)  # 0.0 - 1.0
    ai_insights = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'site_id': self.site_id,
            'metric_date': self.metric_date.isoformat(),
            'incidents_reported': self.incidents_reported,
            'safety_inspections': self.safety_inspections,
            'training_completions': self.training_completions,
            'compliance_rate': self.compliance_rate,
            'equipment_uptime': self.equipment_uptime,
            'risk_index': self.risk_index,
            'ai_insights': self.ai_insights,
            'created_at': self.created_at.isoformat()
        }

class SafetyBulletin(db.Model):
    """Safety communications"""
    __tablename__ = 'safety_bulletins'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    bulletin_type = db.Column(db.String(100))  # 'alert', 'update', 'reminder', 'policy'
    priority = db.Column(db.String(50), default='normal')  # 'low', 'normal', 'high', 'critical'
    target_audience = db.Column(db.String(255))  # 'all', 'management', 'workers', 'specific_team'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'bulletin_type': self.bulletin_type,
            'priority': self.priority,
            'target_audience': self.target_audience,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ReportTemplate(db.Model):
    """Report templates for construction"""
    __tablename__ = 'report_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    template_type = db.Column(db.String(100))  # 'incident', 'inspection', 'risk_assessment'
    content = db.Column(db.Text)  # Template content or structure
    file_path = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'template_type': self.template_type,
            'content': self.content,
            'file_path': self.file_path,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class SystemSettings(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(255), unique=True, nullable=False, index=True)
    setting_value = db.Column(db.Text, nullable=False)
    data_type = db.Column(db.String(50), nullable=False, default='string')  # string, integer, boolean, json, float
    category = db.Column(db.String(100), nullable=False, default='general')
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False)
    is_encrypted = db.Column(db.Boolean, default=False)
    min_value = db.Column(db.String(100))  # For validation
    max_value = db.Column(db.String(100))  # For validation
    allowed_values = db.Column(db.Text)  # JSON array of allowed values
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    updater = db.relationship('User', backref=db.backref('updated_settings', lazy=True))
    
class SystemLog(db.Model):
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    level = db.Column(db.String(20), nullable=False, default='info')
    module = db.Column(db.String(100), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    action = db.Column(db.String(200), nullable=False)
    resource_type = db.Column(db.String(100))
    resource_id = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    request_method = db.Column(db.String(10))
    request_path = db.Column(db.String(500))
    status_code = db.Column(db.Integer)
    response_time = db.Column(db.Float)
    error_message = db.Column(db.Text)
    stack_trace = db.Column(db.Text)
    additional_data = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('system_logs', lazy=True))
    
    @staticmethod
    def create_log(level, module, action, description, user_id=None, **kwargs):
        """
        Create a new system log entry
        
        Args:
            level (str): debug, info, warning, error, critical
            module (str): Module name (e.g., 'camera', 'video_analysis', 'ai_analysis')
            action (str): Action performed (e.g., 'analyze_frame', 'start_session')
            description (str): Human-readable description
            user_id (int): User ID (if available)
            **kwargs: Additional fields:
                - resource_type (str): Type of resource
                - resource_id (int): ID of the resource
                - ip_address (str): Client IP
                - user_agent (str): Browser/device info
                - request_method (str): HTTP method
                - request_path (str): API endpoint
                - status_code (int): HTTP status code
                - response_time (float): Response time in ms
                - error_message (str): Error message
                - stack_trace (str): Stack trace
                - additional_data (dict): Extra context data
        """
        try:
            # Convert additional_data to JSON string if dict
            additional_data = kwargs.get('additional_data')
            if isinstance(additional_data, dict):
                additional_data = json.dumps(additional_data)
            
            log = SystemLog(
                level=level,
                module=module,
                action=action,
                description=description,
                user_id=user_id,
                resource_type=kwargs.get('resource_type'),
                resource_id=kwargs.get('resource_id'),
                ip_address=kwargs.get('ip_address'),
                user_agent=kwargs.get('user_agent'),
                request_method=kwargs.get('request_method'),
                request_path=kwargs.get('request_path'),
                status_code=kwargs.get('status_code'),
                response_time=kwargs.get('response_time'),
                error_message=kwargs.get('error_message'),
                stack_trace=kwargs.get('stack_trace'),
                additional_data=additional_data
            )
            
            db.session.add(log)
            db.session.commit()
            return log
            
        except Exception as e:
            print(f"❌ Failed to create system log: {str(e)}")
            db.session.rollback()
            return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'level': self.level,
            'module': self.module,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'description': self.description,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'request_method': self.request_method,
            'request_path': self.request_path,
            'status_code': self.status_code,
            'response_time': self.response_time,
            'error_message': self.error_message,
            'stack_trace': self.stack_trace,
            'additional_data': json.loads(self.additional_data) if self.additional_data else None
        }

class DocumentVerificationLog(db.Model):
    __tablename__ = 'document_verification_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'pending', 'verified', 'rejected'
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='document_verifications')
    verifier = db.relationship('User', foreign_keys=[verified_by], backref='document_verifications_made')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'verified_by': self.verified_by,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_name': self.user.name if self.user else None,
            'verifier_name': self.verifier.name if self.verifier else None
        }

# ============================================================================
# 1. CONSTRUCTION SITE MODEL (Define FIRST)
# ============================================================================

class ConstructionSite(db.Model):
    """Construction site management"""
    __tablename__ = 'construction_sites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    location_coordinates = db.Column(db.String(100))  # lat,long
    site_type = db.Column(db.String(100))  # 'residential', 'commercial', 'industrial', 'infrastructure'
    project_manager = db.Column(db.String(255))
    safety_officer = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    estimated_completion = db.Column(db.Date)
    status = db.Column(db.String(50), default='active')  # 'planning', 'active', 'completed', 'on_hold'
    safety_score = db.Column(db.Float)  # 0-100
    compliance_status = db.Column(db.String(50), default='compliant')
    safety_plan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'location_coordinates': self.location_coordinates,
            'site_type': self.site_type,
            'project_manager': self.project_manager,
            'safety_officer': self.safety_officer,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'estimated_completion': self.estimated_completion.isoformat() if self.estimated_completion else None,
            'status': self.status,
            'safety_score': self.safety_score,
            'compliance_status': self.compliance_status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


# ============================================================================
# 2. SAFETY TREND DATA (Define AFTER ConstructionSite)
# ============================================================================

class SafetyTrendData(db.Model):
    __tablename__ = 'safety_trend_data'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    metric_name = db.Column(db.String(100), nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('construction_sites.id'))
    department = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    site = db.relationship('ConstructionSite', backref=db.backref('trend_data', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'site_id': self.site_id,
            'department': self.department,
            'created_at': self.created_at.isoformat()
        }


# ============================================================================
# 3. SAFETY PERFORMANCE TARGET (Define AFTER ConstructionSite AND User)
# ============================================================================

class SafetyPerformanceTarget(db.Model):
    __tablename__ = 'safety_performance_targets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # leading, lagging, process, outcome
    current_value = db.Column(db.Float)
    target_value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50))
    period = db.Column(db.String(50))  # daily, weekly, monthly, quarterly, annual
    site_id = db.Column(db.Integer, db.ForeignKey('construction_sites.id'))
    department = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    site = db.relationship('ConstructionSite', backref=db.backref('safety_targets', lazy=True))
    creator = db.relationship('User', backref=db.backref('created_safety_targets', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'current_value': self.current_value,
            'target_value': self.target_value,
            'unit': self.unit,
            'period': self.period,
            'site_id': self.site_id,
            'site_name': self.site.name if self.site else 'All Sites',
            'department': self.department,
            'is_active': self.is_active,
            'performance_percentage': (self.current_value / self.target_value * 100) if self.current_value and self.target_value else 0,
            'status': 'exceeded' if self.current_value and self.current_value >= self.target_value else 'on_track' if self.current_value and (self.current_value / self.target_value) >= 0.9 else 'needs_improvement',
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# ============================================================================
# HEAT & COOL MONITORING DATABASE MODELS
# ============================================================================

class ThermalComfortLog(db.Model):
    """Log of thermal comfort measurements and calculations"""
    __tablename__ = 'thermal_comfort_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.String(100), nullable=False)
    location_name = db.Column(db.String(200))
    building_zone = db.Column(db.String(100))
    
    # Temperature measurements
    air_temperature = db.Column(db.Float)  # Celsius
    radiant_temperature = db.Column(db.Float)  # Celsius
    surface_temperature = db.Column(db.Float)  # Celsius
    
    # Humidity
    relative_humidity = db.Column(db.Float)  # Percentage
    absolute_humidity = db.Column(db.Float)  # g/m³
    
    # Air movement
    air_velocity = db.Column(db.Float)  # m/s
    
    # Calculated indices
    heat_index = db.Column(db.Float)  # Feels like temperature
    wet_bulb_temperature = db.Column(db.Float)
    dew_point = db.Column(db.Float)
    predicted_mean_vote = db.Column(db.Float)  # -3 to +3
    predicted_percentage_dissatisfied = db.Column(db.Float)  # 0-100%
    discomfort_index = db.Column(db.Float)  # 0-100
    
    # Comfort level classification
    comfort_level = db.Column(db.String(50))  # Comfortable, Warm, Cool, etc.
    thermal_sensation = db.Column(db.String(50))  # Very Cold to Very Hot
    
    # Metadata
    measurement_time = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    recorded_by = db.Column(db.String(100))  # User or system
    data_source = db.Column(db.String(50))  # 'sensor', 'satellite', 'calculated'
    
    # Foreign keys
    sensor_id = db.Column(db.String(100))
    analysis_id = db.Column(db.Integer, db.ForeignKey('thermal_analysis_results.id'))
    
    # Indexes for better query performance
    __table_args__ = (
        db.Index('idx_thermal_comfort_location_time', 'location_id', 'measurement_time'),
        db.Index('idx_thermal_comfort_level', 'comfort_level'),
    )


class ThermalAnalysisResult(db.Model):
    """Results of thermal analysis from satellite or sensors"""
    __tablename__ = 'thermal_analysis_results'
    
    id = db.Column(db.Integer, primary_key=True)
    analysis_type = db.Column(db.String(50))  # 'satellite', 'sensor_fusion', 'predictive'
    location_id = db.Column(db.String(100), nullable=False)
    location_name = db.Column(db.String(200))
    
    # Temperature statistics
    min_temperature = db.Column(db.Float)
    max_temperature = db.Column(db.Float)
    mean_temperature = db.Column(db.Float)
    median_temperature = db.Column(db.Float)
    std_deviation_temperature = db.Column(db.Float)
    
    # Thermal patterns
    thermal_gradient = db.Column(db.Float)  # Max - Min
    thermal_inertia = db.Column(db.Float)
    
    # Hot spots
    hot_spot_count = db.Column(db.Integer)
    hot_spot_percentage = db.Column(db.Float)
    hot_spot_mean_temp = db.Column(db.Float)
    hot_spot_areas = db.Column(db.JSON)  # Store coordinates/regions
    
    # Cool zones
    cool_zone_count = db.Column(db.Integer)
    cool_zone_percentage = db.Column(db.Float)
    cool_zone_mean_temp = db.Column(db.Float)
    cool_zone_areas = db.Column(db.JSON)  # Store coordinates/regions
    
    # Analysis metadata
    image_path = db.Column(db.String(500))
    resolution = db.Column(db.String(50))
    cloud_coverage = db.Column(db.Float)  # Percentage
    analysis_time = db.Column(db.DateTime, default=datetime.utcnow)
    processing_time_ms = db.Column(db.Integer)
    
    # Relationships
    comfort_logs = db.relationship('ThermalComfortLog', backref='analysis', lazy=True)
    heat_island_records = db.relationship('UrbanHeatIslandRecord', backref='analysis', lazy=True)
    
    __table_args__ = (
        db.Index('idx_thermal_analysis_location', 'location_id'),
        db.Index('idx_thermal_analysis_time', 'analysis_time'),
    )


class UrbanHeatIslandRecord(db.Model):
    """Records of urban heat island effect measurements"""
    __tablename__ = 'urban_heat_island_records'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.String(100), nullable=False)
    city_area = db.Column(db.String(200))
    
    # Temperature measurements
    urban_core_temperature = db.Column(db.Float)
    rural_reference_temperature = db.Column(db.Float)
    heat_island_intensity = db.Column(db.Float)  # Temperature difference
    
    # Risk assessment
    risk_level = db.Column(db.String(50))  # Critical, High, Moderate, Low, None
    affected_population_estimate = db.Column(db.Integer)
    affected_area_sqkm = db.Column(db.Float)
    
    # Contributing factors
    impervious_surface_percentage = db.Column(db.Float)
    vegetation_coverage = db.Column(db.Float)
    albedo_mean = db.Column(db.Float)  # Average reflectivity
    
    # Hot spots
    hot_spot_count = db.Column(db.Integer)
    hot_spot_intensity = db.Column(db.Float)  # Average temperature above threshold
    
    # Mitigation
    cooling_effect_needed = db.Column(db.Float)  # Temperature reduction needed
    mitigation_priority = db.Column(db.String(50))
    
    # Metadata
    measurement_date = db.Column(db.DateTime, default=datetime.utcnow)
    season = db.Column(db.String(20))  # Summer, Winter, etc.
    time_of_day = db.Column(db.String(20))  # Day, Night, Dawn, Dusk
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    analysis_id = db.Column(db.Integer, db.ForeignKey('thermal_analysis_results.id'))
    
    __table_args__ = (
        db.Index('idx_uhi_location', 'location_id'),
        db.Index('idx_uhi_intensity', 'heat_island_intensity'),
    )


class CoolingRequirement(db.Model):
    """Cooling requirements and predictions"""
    __tablename__ = 'cooling_requirements'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.String(100), nullable=False)
    building_id = db.Column(db.String(100))
    zone = db.Column(db.String(100))
    
    # Current conditions
    current_temperature = db.Column(db.Float)
    target_temperature = db.Column(db.Float)
    cooling_needed = db.Column(db.Boolean, default=False)
    
    # Cooling load
    estimated_cooling_load = db.Column(db.Float)  # kW
    estimated_energy_consumption = db.Column(db.Float)  # kWh
    estimated_cost = db.Column(db.Float)  # Currency
    
    # Peak demand
    peak_demand_time = db.Column(db.String(50))
    peak_factor = db.Column(db.Float)
    
    # Recommendations
    recommended_setpoint = db.Column(db.Float)
    efficiency_suggestions = db.Column(db.JSON)
    
    # System status
    hvac_efficiency = db.Column(db.Float)  # 0-100%
    filter_status = db.Column(db.String(50))  # Clean, Dirty, Needs Replacement
    refrigerant_level = db.Column(db.String(50))  # Normal, Low, Critical
    
    # Predictive
    predicted_duration_hours = db.Column(db.Float)
    confidence_score = db.Column(db.Float)
    
    # Metadata
    calculation_time = db.Column(db.DateTime, default=datetime.utcnow)
    valid_until = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    thermal_analysis_id = db.Column(db.Integer, db.ForeignKey('thermal_analysis_results.id'))
    
    __table_args__ = (
        db.Index('idx_cooling_location', 'location_id'),
        db.Index('idx_cooling_load', 'estimated_cooling_load'),
    )


class HeatingRequirement(db.Model):
    """Heating requirements and predictions"""
    __tablename__ = 'heating_requirements'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.String(100), nullable=False)
    building_id = db.Column(db.String(100))
    zone = db.Column(db.String(100))
    
    # Current conditions
    current_temperature = db.Column(db.Float)
    target_temperature = db.Column(db.Float)
    heating_needed = db.Column(db.Boolean, default=False)
    
    # Heating load
    estimated_heating_load = db.Column(db.Float)  # kW
    estimated_energy_consumption = db.Column(db.Float)  # kWh
    estimated_cost = db.Column(db.Float)  # Currency
    
    # Peak demand
    peak_demand_time = db.Column(db.String(50))
    peak_factor = db.Column(db.Float)
    
    # Recommendations
    recommended_setpoint = db.Column(db.Float)
    efficiency_suggestions = db.Column(db.JSON)
    
    # System status
    system_efficiency = db.Column(db.Float)  # 0-100%
    insulation_status = db.Column(db.String(50))  # Good, Fair, Poor
    duct_status = db.Column(db.String(50))  # Sealed, Needs Inspection
    
    # Predictive
    predicted_duration_hours = db.Column(db.Float)
    confidence_score = db.Column(db.Float)
    
    # Metadata
    calculation_time = db.Column(db.DateTime, default=datetime.utcnow)
    valid_until = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    thermal_analysis_id = db.Column(db.Integer, db.ForeignKey('thermal_analysis_results.id'))
    
    __table_args__ = (
        db.Index('idx_heating_location', 'location_id'),
        db.Index('idx_heating_load', 'estimated_heating_load'),
    )


class ThermalAnomaly(db.Model):
    """Detected thermal anomalies"""
    __tablename__ = 'thermal_anomalies'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.String(100), nullable=False)
    anomaly_type = db.Column(db.String(50))  # 'extreme_heat', 'extreme_cold', 'heat_island', 'temperature_spike'
    
    # Anomaly details
    current_value = db.Column(db.Float)
    expected_value = db.Column(db.Float)
    deviation = db.Column(db.Float)
    deviation_percentage = db.Column(db.Float)
    
    # Severity classification
    severity = db.Column(db.String(20))  # 'critical', 'high', 'medium', 'low'
    severity_score = db.Column(db.Float)  # 0-100
    
    # Impact assessment
    affected_area = db.Column(db.Float)  # sq meters
    affected_population = db.Column(db.Integer)
    infrastructure_risk = db.Column(db.String(50))  # High, Medium, Low
    health_risk = db.Column(db.String(50))  # High, Medium, Low
    
    # Detection
    detection_method = db.Column(db.String(50))  # 'satellite', 'sensor', 'statistical'
    detection_time = db.Column(db.DateTime, default=datetime.utcnow)
    confidence = db.Column(db.Float)
    
    # Status
    status = db.Column(db.String(20), default='active')  # 'active', 'investigating', 'resolved'
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.String(100))
    
    # Recommendations
    recommended_actions = db.Column(db.JSON)
    priority = db.Column(db.Integer)  # 1-5, 1 being highest
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Foreign keys
    thermal_analysis_id = db.Column(db.Integer, db.ForeignKey('thermal_analysis_results.id'))
    
    __table_args__ = (
        db.Index('idx_anomaly_location', 'location_id'),
        db.Index('idx_anomaly_type', 'anomaly_type'),
        db.Index('idx_anomaly_severity', 'severity'),
    )


class ThermalRecommendation(db.Model):
    """Recommendations based on thermal analysis"""
    __tablename__ = 'thermal_recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.String(100), nullable=False)
    
    # Recommendation details
    category = db.Column(db.String(50))  # 'cooling', 'heating', 'insulation', 'ventilation', 'urban_planning'
    priority = db.Column(db.String(20))  # 'high', 'medium', 'low'
    action = db.Column(db.Text, nullable=False)
    
    # Impact estimates
    estimated_impact = db.Column(db.String(200))
    estimated_cost = db.Column(db.String(100))
    estimated_temperature_reduction = db.Column(db.Float)  # For cooling
    estimated_energy_savings = db.Column(db.Float)  # kWh or percentage
    estimated_roi_months = db.Column(db.Integer)
    
    # Implementation
    timeframe = db.Column(db.String(50))  # 'immediate', '24h', '1 week', '1 month', 'long-term'
    implementation_difficulty = db.Column(db.String(50))  # 'easy', 'medium', 'hard'
    required_resources = db.Column(db.JSON)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'implemented', 'rejected'
    implemented_at = db.Column(db.DateTime)
    implemented_by = db.Column(db.String(100))
    
    # Effectiveness tracking
    actual_temperature_reduction = db.Column(db.Float)
    actual_energy_savings = db.Column(db.Float)
    effectiveness_score = db.Column(db.Float)  # 0-100
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(100))
    source_analysis_id = db.Column(db.Integer, db.ForeignKey('thermal_analysis_results.id'))
    
    __table_args__ = (
        db.Index('idx_rec_location', 'location_id'),
        db.Index('idx_rec_priority', 'priority'),
        db.Index('idx_rec_category', 'category'),
    )


class BuildingThermalProfile(db.Model):
    """Thermal profiles for buildings"""
    __tablename__ = 'building_thermal_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.String(100), unique=True, nullable=False)
    building_name = db.Column(db.String(200))
    building_type = db.Column(db.String(50))  # 'residential', 'commercial', 'industrial', 'institutional'
    
    # Location
    address = db.Column(db.String(500))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    climate_zone = db.Column(db.String(50))
    
    # Building characteristics
    year_built = db.Column(db.Integer)
    total_area_sqft = db.Column(db.Float)
    num_floors = db.Column(db.Integer)
    window_to_wall_ratio = db.Column(db.Float)
    
    # Thermal properties
    insulation_rating = db.Column(db.String(50))  # 'excellent', 'good', 'fair', 'poor'
    insulation_effectiveness = db.Column(db.Float)  # 0-100%
    
    # Facade temperatures (different orientations)
    facade_temp_north = db.Column(db.Float)
    facade_temp_south = db.Column(db.Float)
    facade_temp_east = db.Column(db.Float)
    facade_temp_west = db.Column(db.Float)
    roof_temperature = db.Column(db.Float)
    
    # Internal zones
    internal_zones = db.Column(db.JSON)  # Zone name -> temperature mapping
    
    # HVAC
    hvac_system_type = db.Column(db.String(100))
    hvac_efficiency = db.Column(db.Float)  # 0-100%
    hvac_last_maintenance = db.Column(db.DateTime)
    hvac_next_maintenance = db.Column(db.DateTime)
    
    # Thermal bridges
    thermal_bridges = db.Column(db.JSON)  # List of thermal bridge locations
    
    # Energy performance
    energy_star_rating = db.Column(db.Integer)  # 1-100
    predicted_cooling_load = db.Column(db.Float)  # kW
    predicted_heating_load = db.Column(db.Float)  # kW
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    last_analyzed = db.Column(db.DateTime)
    
    __table_args__ = (
        db.Index('idx_building_type', 'building_type'),
        db.Index('idx_building_climate', 'climate_zone'),
    )


class ThermalSensorReading(db.Model):
    """Real-time thermal sensor readings"""
    __tablename__ = 'thermal_sensor_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(100), nullable=False)
    sensor_type = db.Column(db.String(50))  # 'air', 'surface', 'infrared', 'humidity'
    location_id = db.Column(db.String(100))
    
    # Readings
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    air_flow = db.Column(db.Float)
    
    # Quality
    battery_level = db.Column(db.Float)  # Percentage
    signal_strength = db.Column(db.Integer)  # dBm
    accuracy = db.Column(db.Float)  # 0-100%
    
    # Timestamps
    reading_time = db.Column(db.DateTime, default=datetime.utcnow)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Status
    status = db.Column(db.String(20), default='active')  # 'active', 'offline', 'error'
    error_code = db.Column(db.String(50))
    
    __table_args__ = (
        db.Index('idx_sensor_reading_time', 'reading_time'),
        db.Index('idx_sensor_location', 'location_id'),
    )

# models.py - Add these models to your existing models file



# ============================================================================
# ENUMERATIONS FOR CONSISTENCY
# ============================================================================

class ThermalComfortLevel:
    COMFORTABLE = 'Comfortable'
    SLIGHTLY_WARM = 'Slightly Warm'
    WARM = 'Warm'
    HOT = 'Hot'
    VERY_HOT = 'Very Hot'
    SLIGHTLY_COOL = 'Slightly Cool'
    COOL = 'Cool'
    COLD = 'Cold'
    VERY_COLD = 'Very Cold'
    
    @classmethod
    def get_all(cls):
        return [
            cls.VERY_COLD, cls.COLD, cls.COOL, cls.SLIGHTLY_COOL,
            cls.COMFORTABLE,
            cls.SLIGHTLY_WARM, cls.WARM, cls.HOT, cls.VERY_HOT
        ]


class ThermalAnomalyType:
    EXTREME_HEAT = 'extreme_heat'
    EXTREME_COLD = 'extreme_cold'
    HEAT_ISLAND = 'heat_island'
    TEMPERATURE_SPIKE = 'temperature_spike'
    TEMPERATURE_DROP = 'temperature_drop'
    THERMAL_INVERSION = 'thermal_inversion'
    
    @classmethod
    def get_all(cls):
        return [
            cls.EXTREME_HEAT, cls.EXTREME_COLD, cls.HEAT_ISLAND,
            cls.TEMPERATURE_SPIKE, cls.TEMPERATURE_DROP, cls.THERMAL_INVERSION
        ]


class UHIRiskLevel:
    CRITICAL = 'Critical'
    HIGH = 'High'
    MODERATE = 'Moderate'
    LOW = 'Low'
    NONE = 'None'
    
    @classmethod
    def get_all(cls):
        return [cls.CRITICAL, cls.HIGH, cls.MODERATE, cls.LOW, cls.NONE]




class ProgressTracker:
    def __init__(self, export_job_id):
        self.export_job_id = export_job_id
        self.progress = None
        self.current_step = 0
        self.total_steps = 0
        self.step_weights = {}  # Custom weights for different steps
        
    def initialize_progress(self, total_steps, step_weights=None):
        """Initialize progress tracking for a new export"""
        with db.session() as session:
            # Create progress record
            self.progress = ExportProgress(
                export_job_id=self.export_job_id,
                current_step="Initializing",
                total_steps=total_steps,
                current_step_number=0,
                progress_percentage=0.0,
                status_message="Starting export process...",
                data_processed=0,
                total_data=0
            )
            session.add(self.progress)
            session.commit()
            
            # Set step weights (default equal weighting)
            self.total_steps = total_steps
            self.step_weights = step_weights or {i: 1.0/total_steps for i in range(total_steps)}
            
            # Generate progress channel for real-time updates
            export_job = session.query(ExportJob).get(self.export_job_id)
            export_job.progress_channel = f"export_progress_{self.export_job_id}"
            session.commit()
            
            self._emit_progress_event('progress_initialized', {
                'total_steps': total_steps,
                'step_weights': self.step_weights
            })
    
    def start_step(self, step_name, step_number, total_items=0, step_weight=None):
        """Start a new processing step"""
        with db.session() as session:
            self.progress = session.query(ExportProgress).filter_by(
                export_job_id=self.export_job_id
            ).first()
            
            if not self.progress:
                logger.error(f"Progress tracking not initialized for export {self.export_job_id}")
                return
            
            self.current_step = step_number
            self.progress.current_step = step_name
            self.progress.current_step_number = step_number
            self.progress.total_data = total_items
            self.progress.data_processed = 0
            self.progress.status_message = f"Processing {step_name}..."
            self.progress.updated_at = datetime.utcnow()
            
            # Calculate progress based on completed steps
            completed_weight = sum(
                self.step_weights.get(i, 0) 
                for i in range(step_number)
            )
            self.progress.progress_percentage = completed_weight * 100
            
            session.commit()
            
            self._emit_progress_event('step_started', {
                'step_name': step_name,
                'step_number': step_number,
                'total_items': total_items
            })
    
    def update_step_progress(self, items_processed, status_message=None, custom_percentage=None):
        """Update progress within the current step"""
        with db.session() as session:
            self.progress = session.query(ExportProgress).filter_by(
                export_job_id=self.export_job_id
            ).first()
            
            if not self.progress:
                return
            
            # Update processed items
            if items_processed > self.progress.data_processed:
                self.progress.data_processed = items_processed
            
            # Update status message if provided
            if status_message:
                self.progress.status_message = status_message
            
            # Calculate progress percentage
            if custom_percentage is not None:
                step_progress = custom_percentage
            elif self.progress.total_data > 0:
                step_progress = self.progress.data_processed / self.progress.total_data
            else:
                step_progress = 0
            
            # Calculate overall progress
            completed_weight = sum(
                self.step_weights.get(i, 0) 
                for i in range(self.current_step)
            )
            current_step_weight = self.step_weights.get(self.current_step, 0)
            current_step_contribution = current_step_weight * step_progress
            
            overall_progress = (completed_weight + current_step_contribution) * 100
            
            self.progress.progress_percentage = overall_progress
            self.progress.updated_at = datetime.utcnow()
            
            # Update cached progress in export job
            export_job = session.query(ExportJob).get(self.export_job_id)
            export_job.current_progress = overall_progress
            
            session.commit()
            
            self._emit_progress_event('progress_updated', {
                'items_processed': items_processed,
                'total_items': self.progress.total_data,
                'step_progress': step_progress * 100,
                'overall_progress': overall_progress,
                'status_message': status_message
            })
    
    def complete_step(self, step_name, items_processed=None):
        """Mark a step as completed"""
        with db.session() as session:
            self.progress = session.query(ExportProgress).filter_by(
                export_job_id=self.export_job_id
            ).first()
            
            if not self.progress:
                return
            
            # Ensure step is marked as 100% complete
            completed_weight = sum(
                self.step_weights.get(i, 0) 
                for i in range(self.current_step + 1)
            )
            self.progress.progress_percentage = completed_weight * 100
            self.progress.current_step = f"Completed: {step_name}"
            self.progress.status_message = f"Completed {step_name}"
            self.progress.updated_at = datetime.utcnow()
            
            # Update cached progress
            export_job = session.query(ExportJob).get(self.export_job_id)
            export_job.current_progress = completed_weight * 100
            
            session.commit()
            
            self._emit_progress_event('step_completed', {
                'step_name': step_name,
                'step_number': self.current_step,
                'items_processed': items_processed or self.progress.data_processed,
                'overall_progress': completed_weight * 100
            })
    
    def record_error(self, error_message, error_data=None):
        """Record an error in the progress tracking"""
        with db.session() as session:
            self._emit_progress_event('error_occurred', {
                'error_message': error_message,
                'error_data': error_data,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Log error event
            error_event = ProgressEvent(
                progress_id=self.progress.id,
                event_type='error',
                message=error_message,
                data=error_data or {}
            )
            session.add(error_event)
            session.commit()
    
    def complete_export(self, file_path, file_size):
        """Mark export as completed"""
        with db.session() as session:
            self.progress = session.query(ExportProgress).filter_by(
                export_job_id=self.export_job_id
            ).first()
            
            if not self.progress:
                return
            
            # Mark as 100% complete
            self.progress.progress_percentage = 100.0
            self.progress.current_step = "Export Complete"
            self.progress.status_message = "Export successfully completed"
            self.progress.updated_at = datetime.utcnow()
            
            # Update export job
            export_job = session.query(ExportJob).get(self.export_job_id)
            export_job.status = 'completed'
            export_job.file_path = file_path
            export_job.file_size = file_size
            export_job.completed_at = datetime.utcnow()
            export_job.current_progress = 100.0
            
            session.commit()
            
            self._emit_progress_event('export_completed', {
                'file_path': file_path,
                'file_size': file_size,
                'completed_at': datetime.utcnow().isoformat()
            })
    
    def _emit_progress_event(self, event_type, data):
        """Emit progress event via WebSocket"""
        try:
            event_data = {
                'export_id': self.export_job_id,
                'event_type': event_type,
                'timestamp': datetime.utcnow().isoformat(),
                'data': data
            }
            
            # Emit via WebSocket if available
            if hasattr(app, 'socketio'):
                channel = f"export_progress_{self.export_job_id}"
                app.socketio.emit('progress_update', event_data, room=channel)
            
            # Also store in database for audit
            with db.session() as session:
                progress = session.query(ExportProgress).filter_by(
                    export_job_id=self.export_job_id
                ).first()
                
                if progress:
                    event = ProgressEvent(
                        progress_id=progress.id,
                        event_type=event_type,
                        message=f"{event_type} event",
                        data=data
                    )
                    session.add(event)
                    session.commit()
                    
        except Exception as e:
            logger.error(f"Failed to emit progress event: {str(e)}")

# Add these relationships to the User class

def allowed_file(filename):
    """Check if file extension is allowed"""
    allowed_extensions = {
        'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv',
        'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff',
        'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm',
        'zip', 'rar', '7z'
    }
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

class NotificationPreferences(db.Model):
    __tablename__ = 'notification_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Channel preferences
    email_enabled = db.Column(db.Boolean, default=True)
    push_enabled = db.Column(db.Boolean, default=True)
    sms_enabled = db.Column(db.Boolean, default=False)
    in_app_enabled = db.Column(db.Boolean, default=True)
    
    # Category preferences
    incident_alerts = db.Column(db.Boolean, default=True)
    status_updates = db.Column(db.Boolean, default=True)
    assignment_notifications = db.Column(db.Boolean, default=True)
    overdue_alerts = db.Column(db.Boolean, default=True)
    daily_digest = db.Column(db.Boolean, default=False)
    weekly_report = db.Column(db.Boolean, default=False)
    safety_updates = db.Column(db.Boolean, default=True)
    compliance_alerts = db.Column(db.Boolean, default=True)
    
    # Priority filters
    low_priority = db.Column(db.Boolean, default=True)
    medium_priority = db.Column(db.Boolean, default=True)
    high_priority = db.Column(db.Boolean, default=True)
    urgent_priority = db.Column(db.Boolean, default=True)
    
    # Quiet hours
    quiet_hours_enabled = db.Column(db.Boolean, default=False)
    quiet_hours_start = db.Column(db.Time, default=None)
    quiet_hours_end = db.Column(db.Time, default=None)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'email_enabled': self.email_enabled,
            'push_enabled': self.push_enabled,
            'sms_enabled': self.sms_enabled,
            'in_app_enabled': self.in_app_enabled,
            'incident_alerts': self.incident_alerts,
            'status_updates': self.status_updates,
            'assignment_notifications': self.assignment_notifications,
            'overdue_alerts': self.overdue_alerts,
            'daily_digest': self.daily_digest,
            'weekly_report': self.weekly_report,
            'safety_updates': self.safety_updates,
            'compliance_alerts': self.compliance_alerts,
            'low_priority': self.low_priority,
            'medium_priority': self.medium_priority,
            'high_priority': self.high_priority,
            'urgent_priority': self.urgent_priority,
            'quiet_hours_enabled': self.quiet_hours_enabled,
            'quiet_hours_start': self.quiet_hours_start.isoformat() if self.quiet_hours_start else None,
            'quiet_hours_end': self.quiet_hours_end.isoformat() if self.quiet_hours_end else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
class BatchProcess(db.Model):
    __tablename__ = 'batch_processes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    batch_id = db.Column(db.String(100), unique=True, nullable=False)
    process_type = db.Column(db.String(50), nullable=False)
    total_files = db.Column(db.Integer, default=0)
    processed_files = db.Column(db.Integer, default=0)
    failed_files = db.Column(db.Integer, default=0)
    skipped_files = db.Column(db.Integer, default=0)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='processing')
    total_size = db.Column(db.BigInteger, default=0)
    batch_metadata = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ✅ KEEP relationship but add lazy='select' and explicit primaryjoin
    user = db.relationship(
        'User', 
        backref=db.backref('batches', lazy='select'), 
        lazy='select',
        primaryjoin='BatchProcess.user_id == User.id'
    )
    
    def __repr__(self):
        return f'<BatchProcess {self.batch_id}>'

class NotificationTemplate(db.Model):
    __tablename__ = 'notification_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=False)  # incident_report, status_update, assignment, etc.
    category = db.Column(db.String(50), nullable=False)  # safety, compliance, system, etc.
    title_template = db.Column(db.String(255), nullable=False)
    message_template = db.Column(db.Text, nullable=False)
    default_priority = db.Column(db.String(16), default='medium')
    is_active = db.Column(db.Boolean, default=True)
    variables = db.Column(db.JSON)  # Available template variables
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'category': self.category,
            'title_template': self.title_template,
            'message_template': self.message_template,
            'default_priority': self.default_priority,
            'is_active': self.is_active,
            'variables': self.variables,
            'created_by': self.created_by,
            'creator_name': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }   

# ANALYTICS MODELS - Add after your User model
class AnalyticsExport(db.Model):
    __tablename__ = 'analytics_exports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    export_type = db.Column(db.String(20), nullable=False)  # pdf, excel, csv, json
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    analytics_types = db.Column(db.String(500))  # Comma-separated list
    date_range = db.Column(db.String(50))
    file_size = db.Column(db.Integer)  # in bytes
    status = db.Column(db.String(20), default='processing')  # processing, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    downloaded_at = db.Column(db.DateTime)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('analytics_exports', lazy=True))

class MedicalChat(db.Model):
    __tablename__ = 'medical_chats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=True)
    messages = db.Column(db.Text, nullable=False)  # JSON string
    response = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_test_data = db.Column(db.Boolean, default=False)
    plan_used = db.Column(db.String(50), default='free')
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    hospital = db.relationship('Hospital', foreign_keys=[hospital_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'hospital_id': self.hospital_id,
            'messages': json.loads(self.messages) if self.messages else [],
            'response': json.loads(self.response) if self.response else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_test_data': self.is_test_data,
            'plan_used': self.plan_used
        }

class AnalyticsDashboard(db.Model):
    __tablename__ = 'analytics_dashboards'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    layout_config = db.Column(db.JSON)  # Widget layout and positions
    data_config = db.Column(db.JSON)  # Data sources, filters, time ranges
    filters = db.Column(db.JSON)  # Saved filters
    is_shared = db.Column(db.Boolean, default=False)
    is_default = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    shared_token = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('analytics_dashboards', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'layout_config': self.layout_config,
            'data_config': self.data_config,
            'filters': self.filters,
            'is_shared': self.is_shared,
            'is_default': self.is_default,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AnalyticsCache(db.Model):
    __tablename__ = 'analytics_cache'
    
    id = db.Column(db.Integer, primary_key=True)
    cache_key = db.Column(db.String(255), unique=True, nullable=False, index=True)
    data = db.Column(db.JSON)
    expires_at = db.Column(db.DateTime, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cache_key': self.cache_key,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AnalyticsWidget(db.Model):
    __tablename__ = 'analytics_widgets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))  # 'chart', 'table', 'metric', 'list'
    category = db.Column(db.String(50))  # 'risk', 'compliance', 'safety', 'operations'
    config_template = db.Column(db.JSON)  # Default configuration
    is_system = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'category': self.category,
            'config_template': self.config_template,
            'is_system': self.is_system,
            'is_active': self.is_active
        }

class UserSignature(db.Model):
    """Store user signatures for certificates"""
    __tablename__ = 'user_signatures'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    signature_image = db.Column(db.String(500))
    signature_text = db.Column(db.String(200))
    signature_type = db.Column(db.String(20), default='image')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('signature', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'signature_image': self.signature_image,
            'signature_text': self.signature_text,
            'signature_type': self.signature_type,
            'is_active': self.is_active
        }


class AIExamGeneration(db.Model):
    """Track AI exam generation"""
    __tablename__ = 'ai_exam_generations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False, default='intermediate')
    num_questions = db.Column(db.Integer, nullable=False, default=10)
    industry = db.Column(db.String(100), nullable=False, default='general')
    exam_id = db.Column(db.String(100), nullable=True)
    plan = db.Column(db.String(50), nullable=False, default='free')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('ai_exam_generations', lazy=True))

class AICertificateGeneration(db.Model):
    """Track AI certificate generation"""
    __tablename__ = 'ai_certificate_generations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient = db.Column(db.String(200), nullable=False)
    course = db.Column(db.String(200), nullable=False)
    completion_date = db.Column(db.String(50), nullable=False)
    certificate_id = db.Column(db.String(100), nullable=True)
    certificate_pdf_path = db.Column(db.String(500), nullable=True)  # NEW: Store PDF file path
    certificate_html = db.Column(db.Text, nullable=True)  # NEW: Store HTML for regeneration
    plan = db.Column(db.String(50), nullable=False, default='free')
    downloaded = db.Column(db.Boolean, default=False)  # NEW: Track if downloaded
    downloaded_at = db.Column(db.DateTime, nullable=True)  # NEW: Track download time
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('ai_certificate_generations', lazy=True))
    
class AIExamSubmission(db.Model):
    """Track exam submissions for grading"""
    __tablename__ = 'ai_exam_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exam_id = db.Column(db.String(100), nullable=False)
    answers = db.Column(db.JSON, nullable=True)
    score = db.Column(db.Float, nullable=True)
    passed = db.Column(db.Boolean, nullable=True)
    graded_at = db.Column(db.DateTime, nullable=True)
    plan = db.Column(db.String(50), nullable=False, default='free')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('ai_exam_submissions', lazy=True))

# Add these to your models.py file

# ===== CORRECTED PDF MODELS FOR SQLALCHEMY =====

class AIPDFDocument(db.Model):
    __tablename__ = 'ai_pdf_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), default='general')
    template_id = db.Column(db.String(100))
    file_path = db.Column(db.String(500))
    file_size = db.Column(db.Integer)  # in bytes
    includes_signature = db.Column(db.Boolean, default=False)
    has_watermark = db.Column(db.Boolean, default=False)
    quality_level = db.Column(db.String(50), default='high')
    generation_id = db.Column(db.Integer, db.ForeignKey('ai_document_generations.id'))
    current_version_id = db.Column(db.Integer, db.ForeignKey('ai_pdf_versions.id'))
    plan = db.Column(db.String(50), default='free')
    system_team_bypass = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('pdf_documents', lazy='dynamic'))
    generation = db.relationship('AIDocumentGeneration', backref=db.backref('pdf_document', uselist=False))
    
    # Corrected version relationship with explicit foreign_keys
    current_version = db.relationship('AIPDFVersion', 
                                     foreign_keys=[current_version_id],
                                     post_update=True)
    
    versions = db.relationship('AIPDFVersion',
                              foreign_keys='AIPDFVersion.pdf_document_id',
                              backref=db.backref('document', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')


class AIPDFVersion(db.Model):
    __tablename__ = 'ai_pdf_versions'
    
    id = db.Column(db.Integer, primary_key=True)
    pdf_document_id = db.Column(db.Integer, 
                               db.ForeignKey('ai_pdf_documents.id', ondelete='CASCADE'), 
                               nullable=False)
    version_number = db.Column(db.String(50), nullable=False)
    version_notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_path = db.Column(db.String(500))
    file_size = db.Column(db.Integer)
    is_major_version = db.Column(db.Boolean, default=False)
    parent_version_id = db.Column(db.Integer, db.ForeignKey('ai_pdf_versions.id'))
    is_active = db.Column(db.Boolean, default=True)
    plan = db.Column(db.String(50), default='free')
    system_team_bypass = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships with explicit foreign_keys
    creator = db.relationship('User', foreign_keys=[created_by])
    
    # Self-referential relationship for parent version
    parent_version = db.relationship('AIPDFVersion', 
                                    remote_side=[id],
                                    foreign_keys=[parent_version_id],
                                    backref=db.backref('child_versions', lazy='dynamic'))
    
    # Indexes for better performance
    __table_args__ = (
        db.Index('idx_pdf_versions_document', 'pdf_document_id'),
        db.Index('idx_pdf_versions_created_by', 'created_by'),
        db.Index('idx_pdf_versions_parent', 'parent_version_id'),
        db.UniqueConstraint('pdf_document_id', 'version_number', name='uq_document_version')
    )


class AIPDFGeneration(db.Model):
    __tablename__ = 'ai_pdf_generations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pdf_document_id = db.Column(db.Integer, db.ForeignKey('ai_pdf_documents.id'))
    document_type = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    template_id = db.Column(db.String(100))
    file_size = db.Column(db.Integer)
    plan = db.Column(db.String(50), default='free')
    system_team_bypass = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('pdf_generations', lazy='dynamic'))
    document = db.relationship('AIPDFDocument', 
                              foreign_keys=[pdf_document_id],
                              backref=db.backref('generations', lazy='dynamic'))
    

class AIPDFTemplate(db.Model):
    __tablename__ = 'ai_pdf_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    template_name = db.Column(db.String(200), nullable=False)
    template_html = db.Column(db.Text, nullable=False)
    template_css = db.Column(db.Text, default='')
    industry = db.Column(db.String(100), default='general')
    document_type = db.Column(db.String(100), default='custom')
    is_public = db.Column(db.Boolean, default=False)
    is_system_template = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    usage_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    plan = db.Column(db.String(50), default='free')
    system_team_bypass = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime)
    
    user = db.relationship('User', backref=db.backref('pdf_templates', lazy='dynamic'))


class AIPDFDownload(db.Model):
    __tablename__ = 'ai_pdf_downloads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pdf_document_id = db.Column(db.Integer, db.ForeignKey('ai_pdf_documents.id'))
    download_format = db.Column(db.String(50), default='pdf')
    file_size = db.Column(db.Integer)
    plan = db.Column(db.String(50), default='free')
    system_team_bypass = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('pdf_downloads', lazy='dynamic'))
    document = db.relationship('AIPDFDocument', 
                              foreign_keys=[pdf_document_id],
                              backref=db.backref('downloads', lazy='dynamic'))


class AIPDFAnalysis(db.Model):
    __tablename__ = 'ai_pdf_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pdf_document_id = db.Column(db.Integer, db.ForeignKey('ai_pdf_documents.id'))
    analysis_type = db.Column(db.String(50), default='comprehensive')
    analysis_data = db.Column(db.JSON)  # Store analysis results as JSON
    file_size = db.Column(db.Integer)
    plan = db.Column(db.String(50), default='free')
    system_team_bypass = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('pdf_analyses', lazy='dynamic'))
    document = db.relationship('AIPDFDocument', 
                              foreign_keys=[pdf_document_id],
                              backref=db.backref('analyses', lazy='dynamic'))


class AIPDFBatch(db.Model):
    __tablename__ = 'ai_pdf_batches'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    batch_name = db.Column(db.String(200), nullable=False)
    total_documents = db.Column(db.Integer, default=0)
    successful_count = db.Column(db.Integer, default=0)
    failed_count = db.Column(db.Integer, default=0)
    template_id = db.Column(db.String(100))
    status = db.Column(db.String(50), default='pending')
    error_message = db.Column(db.Text)
    plan = db.Column(db.String(50), default='free')
    system_team_bypass = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    user = db.relationship('User', backref=db.backref('pdf_batches', lazy='dynamic'))
    
    # Relationship to batch documents
    documents = db.relationship('AIPDFBatchDocument', 
                               backref='batch', 
                               lazy='dynamic',
                               cascade='all, delete-orphan')


class AIPDFBatchDocument(db.Model):
    __tablename__ = 'ai_pdf_batch_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('ai_pdf_batches.id', ondelete='CASCADE'), nullable=False)
    document_index = db.Column(db.Integer)
    document_type = db.Column(db.String(100))
    requirements = db.Column(db.Text)
    industry = db.Column(db.String(100))
    company_info = db.Column(db.JSON)
    status = db.Column(db.String(50), default='pending')
    generated_document_id = db.Column(db.Integer, db.ForeignKey('ai_pdf_documents.id'))
    error_message = db.Column(db.Text)
    estimated_size = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    generated_document = db.relationship('AIPDFDocument', 
                                        foreign_keys=[generated_document_id],
                                        backref=db.backref('batch_document', uselist=False))


class AIPDFExport(db.Model):
    __tablename__ = 'ai_pdf_exports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    export_format = db.Column(db.String(50), default='zip')
    document_count = db.Column(db.Integer, default=0)
    include_metadata = db.Column(db.Boolean, default=True)
    compression_level = db.Column(db.String(50), default='normal')
    status = db.Column(db.String(50), default='pending')
    file_path = db.Column(db.String(500))
    file_size = db.Column(db.Integer)
    error_message = db.Column(db.Text)
    plan = db.Column(db.String(50), default='free')
    system_team_bypass = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    user = db.relationship('User', backref=db.backref('pdf_exports', lazy='dynamic'))


class AIPDFGenerationError(db.Model):
    __tablename__ = 'ai_pdf_generation_errors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    document_type = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    error_type = db.Column(db.String(100))
    error_message = db.Column(db.Text)
    stack_trace = db.Column(db.Text)
    plan = db.Column(db.String(50), default='free')
    system_team_bypass = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('pdf_generation_errors', lazy='dynamic'))


class AIStatisticsCache(db.Model):
    __tablename__ = 'ai_statistics_cache'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    statistic_type = db.Column(db.String(100), nullable=False)
    statistic_key = db.Column(db.String(200), nullable=False)
    statistic_value = db.Column(db.JSON, nullable=False)
    time_range = db.Column(db.String(50))
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    plan = db.Column(db.String(50), default='free')
    
    user = db.relationship('User', backref=db.backref('statistics_cache', lazy='dynamic'))
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'statistic_type', 'statistic_key', 'time_range', 
                           name='uq_statistics_cache'),
        db.Index('idx_statistics_cache_expires', 'expires_at'),
    )


class AIUsageAnalytics(db.Model):
    __tablename__ = 'ai_usage_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    feature_type = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    document_type = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    file_size = db.Column(db.Integer)
    duration_ms = db.Column(db.Integer)
    tokens_used = db.Column(db.Integer)
    cost_units = db.Column(db.Float)
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)
    usage_metadata = db.Column(db.JSON)
    plan = db.Column(db.String(50), default='free')
    system_team_bypass = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('usage_analytics', lazy='dynamic'))
    
    __table_args__ = (
        db.Index('idx_usage_analytics_feature', 'feature_type'),
        db.Index('idx_usage_analytics_created', 'created_at'),
        db.Index('idx_usage_analytics_success', 'success'),
    )

class Manpower(db.Model):
    __tablename__ = 'powerbi_manpower'
    
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, index=True)
    department_id = db.Column(db.Integer, nullable=True)
    department_name = db.Column(db.String(100))
    notes = db.Column(db.Text)
    company_id = db.Column(db.Integer, nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ✅ FIX: Use back_populates with a unique name
    project = db.relationship('Project', back_populates='manpower_rel')

class LTI(db.Model):
    __tablename__ = 'powerbi_lti'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    value = db.Column(db.Float, nullable=False)
    department_id = db.Column(db.Integer, nullable=True)
    department_name = db.Column(db.String(100))
    incident_count = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    company_id = db.Column(db.Integer, nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ FIX: Use back_populates with a unique name
    project = db.relationship('Project', back_populates='lti_rel')

class ManHours(db.Model):
    __tablename__ = 'powerbi_manhours'
    
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100), nullable=False)
    hours = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, index=True)
    department_id = db.Column(db.Integer, nullable=True)
    department_name = db.Column(db.String(100))
    project = db.Column(db.String(200))
    activity = db.Column(db.String(200))
    company_id = db.Column(db.Integer, nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ FIX: Use back_populates with a unique name
    project = db.relationship('Project', back_populates='manhours_rel')

class Observation(db.Model):
    __tablename__ = 'powerbi_observations'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, index=True)
    location = db.Column(db.String(200))
    observed_by = db.Column(db.String(200))
    description = db.Column(db.Text)
    company_id = db.Column(db.Integer, nullable=False, index=True)
    severity_id = db.Column(db.Integer, db.ForeignKey('observation_severities.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    severity = db.relationship('ObservationSeverity', back_populates='observations')
    
    # ✅ FIX: Use back_populates with a unique name
    project = db.relationship('Project', back_populates='observations_rel')

class Severity(db.Model):
    __tablename__ = 'powerbi_severity'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    value = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50))
    description = db.Column(db.Text)
    company_id = db.Column(db.Integer, nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ FIX: Use back_populates with a unique name
    project = db.relationship('Project', back_populates='severity_rel')

class Injury(db.Model):
    __tablename__ = 'powerbi_injuries'
    
    id = db.Column(db.Integer, primary_key=True)
    body_part = db.Column(db.String(100), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False, index=True)
    injury_type = db.Column(db.String(100))
    severity = db.Column(db.String(50))
    company_id = db.Column(db.Integer, nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ FIX: Use back_populates with a unique name
    project = db.relationship('Project', back_populates='injuries_rel')
class OverdueReport(db.Model):
    __tablename__ = 'powerbi_overdue_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20), nullable=False)
    on_time = db.Column(db.Integer, nullable=False, default=0)
    late = db.Column(db.Integer, nullable=False, default=0)
    report_type = db.Column(db.String(100))
    department_id = db.Column(db.Integer, nullable=True)
    department_name = db.Column(db.String(100))
    responsible_person = db.Column(db.String(200))
    company_id = db.Column(db.Integer, nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ FIX: Use back_populates with a unique name
    project = db.relationship('Project', back_populates='overdue_reports_rel')

class DashboardConfig(db.Model):
    __tablename__ = 'powerbi_dashboard_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    config = db.Column(db.Text)  # JSON string of widgets
    date_range = db.Column(db.Text)  # JSON string of date range
    department_id = db.Column(db.Integer, nullable=True)
    project_id = db.Column(db.Integer, nullable=True)
    company_id = db.Column(db.Integer, nullable=False, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ObservationSeverity(db.Model):
    __tablename__ = 'observation_severities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    level = db.Column(db.Integer, nullable=False)
    color_code = db.Column(db.String(7), default='#FF0000')
    description = db.Column(db.Text)
    requires_immediate_action = db.Column(db.Boolean, default=False)
    requires_supervisor_review = db.Column(db.Boolean, default=False)
    response_time_hours = db.Column(db.Integer, default=24)
    
    # Company and creator
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # ✅ Add project_id
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Relationships
    observations = db.relationship('Observation', back_populates='severity', lazy=True)
    company = db.relationship('Company', backref=db.backref('observation_severities', lazy=True))
    creator = db.relationship('User', foreign_keys=[created_by], backref=db.backref('created_severities', lazy=True))
    
    # ✅ FIX: Use back_populates with a unique name instead of backref
    project = db.relationship('Project', back_populates='observation_severity_settings')
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ObservationSeverity {self.name} (Level {self.level})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'color_code': self.color_code,
            'description': self.description,
            'requires_immediate_action': self.requires_immediate_action,
            'requires_supervisor_review': self.requires_supervisor_review,
            'response_time_hours': self.response_time_hours,
            'is_active': self.is_active,
            'company_id': self.company_id,
            'project_id': self.project_id,
            'project_name': self.project.name if self.project else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_default_severities():
        """Get default severity levels"""
        return [
            {
                'name': 'Critical',
                'level': 5,
                'color_code': '#FF0000',
                'description': 'Immediate danger to life or property',
                'requires_immediate_action': True,
                'requires_supervisor_review': True,
                'response_time_hours': 1
            },
            {
                'name': 'High',
                'level': 4,
                'color_code': '#FF6B6B',
                'description': 'Serious risk requiring prompt attention',
                'requires_immediate_action': True,
                'requires_supervisor_review': True,
                'response_time_hours': 4
            },
            {
                'name': 'Medium',
                'level': 3,
                'color_code': '#FFD93D',
                'description': 'Moderate risk requiring attention',
                'requires_immediate_action': False,
                'requires_supervisor_review': False,
                'response_time_hours': 24
            },
            {
                'name': 'Low',
                'level': 2,
                'color_code': '#6BCB77',
                'description': 'Minor risk, can be addressed in regular workflow',
                'requires_immediate_action': False,
                'requires_supervisor_review': False,
                'response_time_hours': 48
            },
            {
                'name': 'Negligible',
                'level': 1,
                'color_code': '#4ECDC4',
                'description': 'Minimal to no risk',
                'requires_immediate_action': False,
                'requires_supervisor_review': False,
                'response_time_hours': 72
            }
        ]

class OverdueReportDashboardConfig(db.Model):
    """Configuration settings for overdue reports dashboard"""
    __tablename__ = 'overdue_report_dashboard_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Dashboard configuration
    widgets_config = db.Column(db.JSON, default=list)  # JSON array of widget configurations
    layout_config = db.Column(db.JSON, default=dict)  # JSON object for layout settings
    filters_config = db.Column(db.JSON, default=dict)  # Default filters
    
    # Display settings
    refresh_interval = db.Column(db.Integer, default=300)  # seconds
    default_date_range = db.Column(db.String(50), default='last_30_days')
    items_per_page = db.Column(db.Integer, default=20)
    
    # Color coding
    critical_threshold = db.Column(db.Integer, default=30)  # days overdue for critical status
    warning_threshold = db.Column(db.Integer, default=15)   # days overdue for warning status
    
    # Notification settings
    enable_notifications = db.Column(db.Boolean, default=True)
    notification_frequency = db.Column(db.String(50), default='daily')  # daily, weekly, realtime
    notification_recipients = db.Column(db.JSON, default=list)  # List of user IDs or emails
    
    # Export settings
    default_export_format = db.Column(db.String(20), default='excel')  # excel, pdf, csv
    include_charts_in_export = db.Column(db.Boolean, default=True)
    
    # User association
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    
    # Sharing
    is_public = db.Column(db.Boolean, default=False)
    shared_with = db.Column(db.JSON, default=list)  # List of user IDs with access
    
    # Metadata
    is_default = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_accessed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('overdue_report_dashboards', lazy=True))
    
    def __repr__(self):
        return f'<OverdueReportDashboardConfig {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'widgets_config': self.widgets_config,
            'layout_config': self.layout_config,
            'filters_config': self.filters_config,
            'refresh_interval': self.refresh_interval,
            'default_date_range': self.default_date_range,
            'items_per_page': self.items_per_page,
            'critical_threshold': self.critical_threshold,
            'warning_threshold': self.warning_threshold,
            'enable_notifications': self.enable_notifications,
            'notification_frequency': self.notification_frequency,
            'notification_recipients': self.notification_recipients,
            'default_export_format': self.default_export_format,
            'include_charts_in_export': self.include_charts_in_export,
            'user_id': self.user_id,
            'company_id': self.company_id,
            'is_public': self.is_public,
            'shared_with': self.shared_with,
            'is_default': self.is_default,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_accessed_at': self.last_accessed_at.isoformat() if self.last_accessed_at else None
        }
    
    @staticmethod
    def get_default_config(user_id, company_id=None):
        """Get or create default dashboard config for user"""
        config = OverdueReportDashboardConfig.query.filter_by(
            user_id=user_id,
            is_default=True,
            is_active=True
        ).first()
        
        if not config:
            config = OverdueReportDashboardConfig(
                name="Default Overdue Reports Dashboard",
                description="Default dashboard configuration for overdue reports",
                user_id=user_id,
                company_id=company_id,
                is_default=True,
                widgets_config=[
                    {
                        'id': 'overdue_trend',
                        'type': 'line_chart',
                        'title': 'Overdue Reports Trend',
                        'position': {'x': 0, 'y': 0, 'w': 6, 'h': 4}
                    },
                    {
                        'id': 'overdue_by_department',
                        'type': 'bar_chart',
                        'title': 'Overdue Reports by Department',
                        'position': {'x': 6, 'y': 0, 'w': 6, 'h': 4}
                    },
                    {
                        'id': 'overdue_summary',
                        'type': 'kpi_cards',
                        'title': 'Overdue Summary',
                        'position': {'x': 0, 'y': 4, 'w': 12, 'h': 2}
                    }
                ],
                layout_config={
                    'theme': 'light',
                    'show_grid': True,
                    'allow_dragging': True,
                    'allow_resizing': True
                },
                filters_config={
                    'department': 'all',
                    'report_type': 'all',
                    'date_range': 'last_30_days'
                }
            )
            db.session.add(config)
            db.session.commit()
        
        return config

class Accident(db.Model):
    __tablename__ = 'powerbi_accidents'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    rate = db.Column(db.Float, nullable=False)
    per_10k_hours = db.Column(db.Float, nullable=False)
    severity = db.Column(db.String(50))
    description = db.Column(db.Text)
    company_id = db.Column(db.Integer, nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ FIX: Use back_populates with a unique name
    project = db.relationship('Project', back_populates='accidents_rel')
    
class ThermalSensor(db.Model):
    """Thermal sensor device model"""
    __tablename__ = 'thermal_sensors'
    
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    type = db.Column(db.String(50))  # indoor, outdoor, industrial, hvac
    status = db.Column(db.String(20), default='active')  # active, inactive, maintenance
    min_temp = db.Column(db.Float, default=-10)
    max_temp = db.Column(db.Float, default=50)
    installation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_calibration = db.Column(db.DateTime)
    battery_level = db.Column(db.Integer, default=100)
    
    # Relationships
    readings = db.relationship('ThermalReading', backref='sensor', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('ThermalAlert', backref='sensor', lazy=True)
    readings = db.relationship('ThermalReading', 
                              backref='sensor', 
                              lazy=True, 
                              cascade='all, delete-orphan')
    
    alerts = db.relationship('ThermalAlert', 
                            backref='sensor', 
                            lazy=True, 
                            cascade='all, delete-orphan')


    def to_dict(self):
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'name': self.name,
            'location': self.location,
            'type': self.type,
            'status': self.status,
            'min_temp': self.min_temp,
            'max_temp': self.max_temp,
            'installation_date': self.installation_date.isoformat() if self.installation_date else None,
            'last_calibration': self.last_calibration.isoformat() if self.last_calibration else None,
            'battery_level': self.battery_level,
            'current_temperature': self.get_current_temperature()
        }
    
    def get_current_temperature(self):
        """Get the most recent temperature reading"""
        latest = ThermalReading.query.filter_by(sensor_id=self.sensor_id)\
            .order_by(ThermalReading.reading_time.desc()).first()
        return latest.temperature if latest else None


class ThermalReading(db.Model):
    """Thermal sensor readings"""
    __tablename__ = 'thermal_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(50), db.ForeignKey('thermal_sensors.sensor_id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float)
    battery_level = db.Column(db.Integer)
    reading_time = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'battery_level': self.battery_level,
            'reading_time': self.reading_time.isoformat() if self.reading_time else None
        }



class ThermalAlert(db.Model):
    """Thermal alerts for abnormal conditions"""
    __tablename__ = 'thermal_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(50), db.ForeignKey('thermal_sensors.sensor_id'), nullable=False)
    alert_type = db.Column(db.String(50))  # high_temp, low_temp, rapid_change, battery_low
    severity = db.Column(db.String(20))  # info, warning, critical
    message = db.Column(db.Text)
    temperature = db.Column(db.Float)
    threshold = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged = db.Column(db.Boolean, default=False)
    acknowledged_at = db.Column(db.DateTime)
    acknowledged_by = db.Column(db.String(100))
    resolved = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'message': self.message,
            'temperature': self.temperature,
            'threshold': self.threshold,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'acknowledged': self.acknowledged
        }


class ThermalAnalysis(db.Model):
    """Thermal analysis results from satellite or sensors"""
    __tablename__ = 'thermal_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.String(100))
    analysis_type = db.Column(db.String(50))  # satellite, sensor_fusion, predictive
    mean_temperature = db.Column(db.Float)
    min_temperature = db.Column(db.Float)
    max_temperature = db.Column(db.Float)
    hot_spot_percentage = db.Column(db.Float)
    cool_zone_percentage = db.Column(db.Float)
    thermal_gradient = db.Column(db.Float)
    analysis_time = db.Column(db.DateTime, default=datetime.utcnow)
    data = db.Column(db.JSON)  # Store additional analysis data
    
    def to_dict(self):
        return {
            'id': self.id,
            'location_id': self.location_id,
            'analysis_type': self.analysis_type,
            'mean_temperature': self.mean_temperature,
            'min_temperature': self.min_temperature,
            'max_temperature': self.max_temperature,
            'hot_spot_percentage': self.hot_spot_percentage,
            'cool_zone_percentage': self.cool_zone_percentage,
            'thermal_gradient': self.thermal_gradient,
            'analysis_time': self.analysis_time.isoformat() if self.analysis_time else None
        }


class IncidentTimeline(db.Model):
    __tablename__ = 'incident_timeline'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id', ondelete='CASCADE'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    data = db.Column(db.JSON, default={})
    
    # Relationships - FIXED
    incident = db.relationship('Incident', backref=db.backref('timeline_entries', lazy=True, cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('timeline_entries', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'incident_id': self.incident_id,
            'action': self.action,
            'details': self.details,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'data': self.data
        }


class InvestigationNote(db.Model):
    __tablename__ = 'investigation_notes'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    note_type = db.Column(db.String(50), default='general')
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - FIXED
    incident = db.relationship('Incident', backref=db.backref('investigation_notes', lazy=True, cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('investigation_notes', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'incident_id': self.incident_id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'note': self.note,
            'note_type': self.note_type,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class SDSDocument(db.Model):
    """Safety Data Sheet Document"""
    __tablename__ = 'sds_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    chemical_name = db.Column(db.String(255), nullable=False)
    cas_number = db.Column(db.String(50), nullable=False, unique=True)
    manufacturer = db.Column(db.String(255))
    classification = db.Column(db.String(100))
    hazard_codes = db.Column(db.String(255))
    file_url = db.Column(db.String(500))
    file_name = db.Column(db.String(255))
    revision_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='draft')
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_sds_cas_number', 'cas_number'),
        db.Index('idx_sds_chemical_name', 'chemical_name'),
        db.Index('idx_sds_company', 'company_id'),
        db.Index('idx_sds_status', 'status'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'chemical_name': self.chemical_name,
            'cas_number': self.cas_number,
            'manufacturer': self.manufacturer,
            'classification': self.classification,
            'hazard_codes': self.hazard_codes,
            'file_url': self.file_url,
            'file_name': self.file_name,
            'revision_date': self.revision_date.isoformat() if self.revision_date else None,
            'status': self.status,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
class PTWDocument(db.Model):
    __tablename__ = 'ptw_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    permit_type = db.Column(db.String(50), default='hot_work')
    location = db.Column(db.String(255))
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    
    status = db.Column(db.String(20), default='draft')
    priority = db.Column(db.String(20), default='medium')
    
    # ✅ Additional PTW fields
    assigned_to = db.Column(db.String(255))
    department = db.Column(db.String(255))
    risk_assessment = db.Column(db.Text)
    isolation_requirements = db.Column(db.Text)
    ppe_requirements = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    file_url = db.Column(db.String(500))
    file_name = db.Column(db.String(255))
    
    approved_at = db.Column(db.DateTime)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approval_comment = db.Column(db.Text)
    
    rejected_at = db.Column(db.DateTime)
    rejected_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    rejection_reason = db.Column(db.Text)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = db.relationship('Company', foreign_keys=[company_id])
    creator = db.relationship('User', foreign_keys=[created_by])
    updater = db.relationship('User', foreign_keys=[updated_by])
    approver = db.relationship('User', foreign_keys=[approved_by])
    rejector = db.relationship('User', foreign_keys=[rejected_by])
    
    __table_args__ = (
        db.Index('idx_ptw_status', 'status'),
        db.Index('idx_ptw_type', 'permit_type'),
        db.Index('idx_ptw_company', 'company_id'),
        db.Index('idx_ptw_dates', 'start_date', 'end_date'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'permit_type': self.permit_type,
            'location': self.location,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'priority': self.priority,
            'assigned_to': self.assigned_to,
            'department': self.department,
            'risk_assessment': self.risk_assessment,
            'isolation_requirements': self.isolation_requirements,
            'ppe_requirements': self.ppe_requirements,
            'notes': self.notes,
            'file_url': self.file_url,
            'file_name': self.file_name,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'approved_by': self.approved_by,
            'approved_by_name': self.approver.name if self.approver else None,
            'approval_comment': self.approval_comment,
            'rejected_at': self.rejected_at.isoformat() if self.rejected_at else None,
            'rejected_by': self.rejected_by,
            'rejected_by_name': self.rejector.name if self.rejector else None,
            'rejection_reason': self.rejection_reason,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'created_by_name': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# models.py

# ============================================================
# DISEASE SURVEILLANCE
# ============================================================

class DiseaseSurveillance(db.Model):
    """Disease surveillance tracking for hospitals"""
    __tablename__ = 'disease_surveillance'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    
    disease_name = db.Column(db.String(255), nullable=False)
    disease_code = db.Column(db.String(50))
    category = db.Column(db.String(100))
    
    # Tracking metrics
    cases = db.Column(db.Integer, default=0)
    deaths = db.Column(db.Integer, default=0)
    recovered = db.Column(db.Integer, default=0)
    active_cases = db.Column(db.Integer, default=0)
    
    # Status and reporting
    status = db.Column(db.String(50), default='active')
    severity = db.Column(db.String(20), default='medium')
    reported_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Reporting
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    hospital = db.relationship('Hospital', foreign_keys=[hospital_id])
    reporter = db.relationship('User', foreign_keys=[reported_by])
    
    __table_args__ = (
        db.Index('idx_disease_surveillance_hospital', 'hospital_id'),
        db.Index('idx_disease_surveillance_status', 'status'),
        db.Index('idx_disease_surveillance_disease', 'disease_name'),
        db.Index('idx_disease_surveillance_date', 'reported_date'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'hospital_id': self.hospital_id,
            'disease_name': self.disease_name,
            'disease_code': self.disease_code,
            'category': self.category,
            'cases': self.cases,
            'deaths': self.deaths,
            'recovered': self.recovered,
            'active_cases': self.active_cases,
            'status': self.status,
            'severity': self.severity,
            'reported_date': self.reported_date.isoformat() if self.reported_date else None,
            'reported_by': self.reported_by,
            'reporter_name': self.reporter.name if self.reporter else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# ============================================================
# EMERGENCY
# ============================================================

class Emergency(db.Model):
    __tablename__ = 'emergencies'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    emergency_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    department_id = db.Column(db.Integer, db.ForeignKey('hospital_departments.id'))
    
    status = db.Column(db.String(50), default='active')
    severity = db.Column(db.String(20), default='medium')
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    injuries = db.Column(db.Integer, default=0)
    fatalities = db.Column(db.Integer, default=0)
    
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reported_date = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_date = db.Column(db.DateTime)
    
    actions_taken = db.Column(db.Text)
    root_cause = db.Column(db.Text)
    preventive_measures = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    hospital = db.relationship('Hospital', foreign_keys=[hospital_id])
    department = db.relationship('HospitalDepartment', foreign_keys=[department_id])
    patient = db.relationship('Patient', foreign_keys=[patient_id])
    reporter = db.relationship('User', foreign_keys=[reported_by])
    
    __table_args__ = (
        db.Index('idx_emergencies_hospital', 'hospital_id'),
        db.Index('idx_emergencies_status', 'status'),
        db.Index('idx_emergencies_type', 'type'),
        db.Index('idx_emergencies_date', 'reported_date'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'emergency_number': self.emergency_number,
            'hospital_id': self.hospital_id,
            'title': self.title,
            'type': self.type,
            'description': self.description,
            'location': self.location,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'status': self.status,
            'severity': self.severity,
            'patient_id': self.patient_id,
            'patient_name': self.patient.name if self.patient else None,
            'injuries': self.injuries,
            'fatalities': self.fatalities,
            'reported_by': self.reported_by,
            'reporter_name': self.reporter.name if self.reporter else None,
            'reported_date': self.reported_date.isoformat() if self.reported_date else None,
            'resolved_date': self.resolved_date.isoformat() if self.resolved_date else None,
            'actions_taken': self.actions_taken,
            'root_cause': self.root_cause,
            'preventive_measures': self.preventive_measures,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class EmergencyPreparedness(db.Model):
    __tablename__ = 'emergency_preparedness'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    plan_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    status = db.Column(db.String(50), default='active')
    severity = db.Column(db.String(20), default='medium')
    
    department_id = db.Column(db.Integer, db.ForeignKey('hospital_departments.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    hospital = db.relationship('Hospital', foreign_keys=[hospital_id])
    department = db.relationship('HospitalDepartment', foreign_keys=[department_id])
    creator = db.relationship('User', foreign_keys=[created_by])
    
    __table_args__ = (
        db.Index('idx_emergency_preparedness_hospital', 'hospital_id'),
        db.Index('idx_emergency_preparedness_status', 'status'),
        db.Index('idx_emergency_preparedness_type', 'type'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'plan_number': self.plan_number,
            'hospital_id': self.hospital_id,
            'title': self.title,
            'type': self.type,
            'description': self.description,
            'status': self.status,
            'severity': self.severity,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'created_by': self.created_by,
            'creator_name': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


__all__ = [
    # Core models
    'Industry',
    'Accident',
    'Incident',
    'ObservationSeverity',
    'IncidentAttachment',
    'OverdueReportDashboardConfig',
    'IncidentAction',
    'User',
    'UserPreferences',
    'UserDocument',
    'UserNote',
    'UserSession',
    'VideoAnalysis',
    'SafetyViolation',
    'UploadedFile',
    'DocumentVersion',
    'Company',
    'Department',
    'Hospital',
    'HospitalDepartment',
    'InvestigationNote',
    'IncidentTimeline',
    # AI Related
    'AIRequest',
    'AIChatMessage',
    'AIDocumentGeneration',
    'AIExamGeneration',
    'AIExamSubmission',
    'AICertificateGeneration',
    'AIHTMLPreview',
    'AISmartQueryLog',
    'AIQueryLog',
    'AIOptimizationLog',
    'AIRiskAnalysisLog',
    'AIConsultationSession',
    'AIStatisticsCache',
    'AIUsageAnalytics',
    
    # PDF Related
    'AIPDFDocument',
    'AIPDFGeneration',
    'AIPDFTemplate',
    'AIPDFDownload',
    'AIPDFAnalysis',
    'AIPDFBatch',
    'AIPDFBatchDocument',
    'AIPDFExport',
    'AIPDFVersion',
    'AIPDFGenerationError',
    
    # Safety & Risk
    'SafetyInspection',
    'SafetyObservation',
    'SafetyBulletin',
    'SafetyTraining',
    'SafetyDocument',
    'SafetyMetric',
    'SafetyKPI',
    'SafetyKPIMeasurement',
    'SafetyPerformanceTarget',
    'SafetyTrendData',
    'SafetyTool',
    'NearMiss',
    'Hazard',
    'RiskAssessment',
    'RiskAssessmentItem',
    'RiskAssessmentComment',
    'RiskAssessmentAttachment',
    'RiskAssessmentHistory',
    'RiskAssessmentTemplate',
    'AuditFinding',
    'AuditActionPlan',
    'CorrectiveAction',
    'ImprovementInitiative',
    'Permit',
    'PermitReview',
    'InspectionItem',
    
    # Emergency
    'EmergencyPlan',
    'EmergencyProcedure',
    'EmergencyDrill',
    
    # Environmental
    'EnvironmentalIncident',
    'EnvironmentalAlert',
    'WasteCategory',
    'WasteDisposal',
    'WaterSample',
    'WaterSamplingSite',
    'AirQualitySensor',
    'AirQualityReading',
    'IndoorAirQuality',
    'EnergyConsumption',
    'SustainabilityGoal',
    
    # Healthcare
    'Patient',
    'Bed',
    'PatientVital',
    'ClinicalNote',
    'LabResult',
    'ImagingStudy',
    'PatientSafetyIncident',
    'Prescription',
    'PatientTimeline',
    'LabSafety',
    'Accreditation',
    'QualityIndicator',
    

    'BiohazardIncident',
    'PatientSafetyGoal',
    'InfectionControlProtocol',
    'MedicationSafetyCheck',
    'EmployeeHealthScreening',
    'WorkplaceErgonomics',
    'FallRiskAssessment',
    'SurfaceSanitation',
    
    'MedicalChat',
    'MedicalAnalysis',
    
    # Equipment/Inventory
    'Equipment',
    
    
    
    # Construction
    'ConstructionSite',
    'ConstructionDocument',
    
    # Monitoring
    'MonitoringStation',
    'MonitoringReading',
    'MonitoringAlert',
    'Camera',
    'CameraFeed',
    
    # Analytics
    'AnalyticsDashboard',
    'AnalyticsWidget',
    'AnalyticsExport',
    'AnalyticsCache',
    'ReportTemplate',
    'ExportJob',
    'ExportProgress',
    'ExportDownloadLog',
    
    # Team/Project
    'Team',
    'TeamMember',
    'TeamInvitation',
    'Project',
    'ProjectPhase',
    'ProjectTask',
    'Milestone',
    'ProgressEvent',
    'ProgressTracker',
    'Task',
    'Workflow',
    'Referral',
    
    # Compliance
    'Compliance',
    'CompliancePolicy',
    'ComplianceChecklist',
    'ComplianceDeadline',
    'ComplianceReport',
    'ComplianceAutomationSettings',
    'ChecklistResponse',
    
    # Training
    'Training',
    'TrainingRecord',
    'TrainingSession',
    
    # Documents
    'Document',
    'DocumentTemplate',
    'DocumentReview',
    'DocumentVerificationLog',
    'EditableDocument',
    'RequiredDocument',
    
    # Notifications
    'Notification',
    'NotificationTemplate',
    'NotificationPreferences',
    'ApprovalNotification',
    
    # System
    'SystemLog',
    'SystemSettings',
    'ActivityLog',
    'LoginLog',
    'LoginAttempt',
    'AdminApprovalLog',
    'AdminAuditLog',
    'FileAccessLog',
    'SecuritySetting',
    'APIUsage',
    
    # Payment/Subscription
    'Subscription',
    'SubscriptionHistory',
    'Payment',
    'PaymentHistory',
    'MonthlyUsageSummary',
    
    # Marketplace
    'TemplateMarketplace',
    
    # Batch Processing
    'BatchProcess',
    
    # Predictive
    'PredictiveModel',
    
    # Verification
    'Verification',
    
    # Password
    'PasswordReset',
    'Manpower',
    'LTI',
    'ManHours',
    'Observation',
    'Severity',
    'Injury',
    'OverdueReport',
    'DashboardConfig',
    
    # Thermal Monitoring Models
    'ThermalComfortLog',
    'ThermalAnalysisResult',
    'UrbanHeatIslandRecord',
    'CoolingRequirement',
    'HeatingRequirement',
    'ThermalAnomaly',
    'ThermalRecommendation',
    'BuildingThermalProfile',
    'ThermalSensorReading',
    'ThermalComfortLevel',
    'ThermalAnomalyType',
    'UHIRiskLevel',
    'ThermalSensor',
    'IncidentReportLog',
    'ThermalReading',
    'ThermalAlert',
    'ThermalAnalysis',
    'UserSignature',
    'Permission',
    'Role',
    'UserRole',
    'ManualPayment',
    'ComplianceRecord',
    'EnvironmentalMetric',
    'EnvironmentalScore',
    'EnvironmentalInitiative',
    'UserEngagementEvent',
    'UserEngagementScore',
    'Doctor',
    'SafetyIncident',
    'SafetyEquipment',
    'DocumentMetadata',
    'DocumentComment',
    'DocumentAuditLog',
    'DocumentLink',
    'ReviewHistory',
    'DocumentSignature',
    'SignatureVerification',
    'SavedSearch',
    'SearchHistory',
    'DocumentWorkflow',
    'DocumentCategory',
    'ApprovalChain',
    'ApprovalStep',
    'TemplateCategoryMapping',
    'DocumentApproval',
    'ApprovalStepStatus',
    'DocumentExpiration',
    'ExpirationNotificationLog',
    'TemplateCategory',
    'ComplianceViolation',
    'SDSDocument',
    'PTWDocument',
    'ComplianceFramework',
    'ComplianceRequirement',
    'ComplianceAuditLog',
    'DocumentComplianceLink',
    'Emergency',
    'DiseaseSurveillance',
    'EmergencyPreparedness',

    
]

print(f"✅ Models.py loaded with {len(__all__)} models")
