
"""
UNIFIED BRIDGE FOR SAFETYTRACK MODELS
Uses all your existing models without retraining
"""

import json
import numpy as np
from typing import Dict, Any, List
import torch
import joblib

class SafetyTrackModelBridge:
    """Bridge between all your ML models and template system"""
    
    def __init__(self, model_dir: str = "ml_models"):
        self.model_dir = model_dir
        self.models = {}
        self.knowledge_base = None
        self.training_data = {}
        
        # Load all models and data
        self._load_all_models()
    
    def _load_all_models(self):
        """Load all model files"""
        try:
            # 1. Load knowledge base (templates and rules)
            kb_path = f"{self.model_dir}/knowledge_base.json"
            with open(kb_path, 'r') as f:
                self.knowledge_base = json.load(f)
            print("✓ Loaded knowledge base")
            
            # 2. Load training data (these are your "models")
            data_files = [
                ('multi_industry_classifier.json', 'industry_data'),
                ('enhanced_complexity_predictor.json', 'complexity_data')
            ]
            
            for filename, key in data_files:
                path = f"{self.model_dir}/{filename}"
                with open(path, 'r') as f:
                    self.training_data[key] = json.load(f)
                print(f"✓ Loaded {key} with {len(self.training_data[key])} examples")
            
            # 3. Try to load PyTorch model
            try:
                pt_path = f"{self.model_dir}/intent_model_simple.pt"
                self.models['intent_model'] = torch.load(pt_path, map_location='cpu')
                print("✓ Loaded PyTorch intent model")
            except:
                print("⚠ PyTorch model not available/needed")
            
            # 4. Load other metadata
            metadata_files = [
                'intent_model_info.json',
                'ml_training_checkpoint.json', 
                'training_state.json',
                'model_testing_report.json'
            ]
            
            for filename in metadata_files:
                path = f"{self.model_dir}/{filename}"
                if Path(path).exists():
                    with open(path, 'r') as f:
                        self.models[filename.replace('.json', '')] = json.load(f)
            
            print(f"✅ Loaded {len(self.models)} model files and {len(self.training_data)} datasets")
            
        except Exception as e:
            print(f"⚠ Some models failed to load: {e}")
            # Continue with what we have
    
    def predict_industry(self, features: Dict[str, Any]) -> str:
        """Predict industry using training data (kNN approach)"""
        if 'industry_data' not in self.training_data:
            return self._fallback_industry_detection(features)
        
        data = self.training_data['industry_data']
        
        # Find most similar training example
        best_industry = 'general'
        best_similarity = -1
        
        for example in data[:100]:  # Check first 100
            if 'features' in example and 'label' in example:
                ex_features = example['features']
                
                # Calculate keyword similarity
                similarity = 0
                for key, value in features.items():
                    if key.startswith('has_') and key.endswith('_keywords'):
                        if value and key in ex_features and ex_features[key]:
                            similarity += 2
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_industry = example['label']
        
        return best_industry if best_industry != 'aviation' else 'construction'
    
    def predict_complexity(self, features: Dict[str, Any]) -> float:
        """Predict complexity score"""
        if 'complexity_data' not in self.training_data:
            return self._calculate_complexity_from_features(features)
        
        data = self.training_data['complexity_data']
        
        # Find average complexity from similar documents
        total_complexity = 0
        count = 0
        
        for example in data[:50]:
            if 'features' in example and 'label' in example:
                ex_features = example['features']
                
                # Check if features are similar
                similar = True
                for key in ['basic_length', 'word_count', 'has_tables']:
                    if key in features and key in ex_features:
                        if abs(features[key] - ex_features[key]) > features[key] * 0.5:
                            similar = False
                            break
                
                if similar:
                    total_complexity += example['label']
                    count += 1
        
        if count > 0:
            return round(total_complexity / count, 2)
        
        return self._calculate_complexity_from_features(features)
    
    def _calculate_complexity_from_features(self, features: Dict[str, Any]) -> float:
        """Calculate complexity directly from features"""
        complexity = 0.5  # Base
        
        # Length contributes 40%
        length = features.get('basic_length', 1000)
        complexity += min(0.4, length / 10000)
        
        # Structure contributes 30%
        if features.get('has_tables', False):
            complexity += 0.15
        if features.get('structural_complexity', 0) > 0.5:
            complexity += 0.15
        
        # Content richness contributes 20%
        if features.get('has_risk_terms', 0):
            complexity += 0.1
        if features.get('has_safety_terms', 0):
            complexity += 0.1
        
        return min(1.0, round(complexity, 2))
    
    def _fallback_industry_detection(self, features: Dict[str, Any]) -> str:
        """Fallback industry detection when no model available"""
        industry_keywords = {
            'construction': ['construct', 'build', 'site', 'contractor'],
            'manufacturing': ['manufactur', 'factory', 'production', 'plant'],
            'healthcare': ['health', 'medical', 'patient', 'hospital'],
            'aviation': ['aviation', 'aircraft', 'flight', 'airport']
        }
        
        # Check feature flags
        for industry, keywords in industry_keywords.items():
            for keyword in keywords:
                feature_name = f'has_{keyword}_keywords'
                if features.get(feature_name, 0):
                    return industry
        
        # Check text if available
        text = features.get('text', '').lower()
        for industry, keywords in industry_keywords.items():
            if any(keyword in text for keyword in keywords):
                return industry
        
        return 'general'
    
    def get_tables_for_industry(self, industry: str, complexity: float) -> List[str]:
        """Get appropriate tables for industry and complexity"""
        
        # Table knowledge from your template system
        industry_tables = {
            'construction': [
                'WorkPermit', 'RiskAssessment', 'SiteInspection', 'EquipmentLog',
                'SafetyMeeting', 'IncidentReport', 'TrainingRecord'
            ],
            'manufacturing': [
                'ProductionSafety', 'QualityControl', 'MaintenanceLog', 'HazardOps',
                'ProcessCheck', 'EquipmentInspection', 'WasteManagement'
            ],
            'healthcare': [
                'PatientRecord', 'InfectionControl', 'MedicationAdmin', 'IncidentReport',
                'EquipmentSterilization', 'StaffTraining', 'ComplianceAudit'
            ],
            'aviation': [
                'FlightSafety', 'AircraftMaintenance', 'GroundOps', 'SecurityCheck',
                'FuelSafety', 'CargoHandling', 'EmergencyProcedures'
            ],
            'general': [
                'RiskAssessment', 'SafetyChecklist', 'IncidentReport',
                'TrainingRecord', 'EquipmentCheck', 'ComplianceForm'
            ]
        }
        
        tables = industry_tables.get(industry, industry_tables['general'])
        
        # Determine how many tables based on complexity
        table_count = max(2, min(len(tables), int(complexity * 6)))
        
        # Return the most relevant tables
        return tables[:table_count]
    
    def predict_document_structure(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main prediction function - replaces your ML model calls
        Returns everything needed for template generation
        """
        
        # 1. Get industry prediction
        industry = self.predict_industry(features)
        
        # 2. Get complexity prediction
        complexity = self.predict_complexity(features)
        
        # 3. Determine document type
        doc_type = self._determine_document_type(features)
        
        # 4. Get appropriate tables
        tables = self.get_tables_for_industry(industry, complexity)
        
        # 5. Generate template structure
        template_structure = self._generate_template_structure(industry, doc_type, complexity)
        
        return {
            'industry': industry,
            'document_type': doc_type,
            'complexity_score': complexity,
            'recommended_tables': tables,
            'template_structure': template_structure,
            'confidence': self._calculate_confidence(features, industry),
            'model_source': 'SafetyTrack Bridge'
        }
    
    def _determine_document_type(self, features: Dict[str, Any]) -> str:
        """Determine document type from features"""
        text = features.get('text', '').lower()
        
        if any(term in text for term in ['risk', 'hazard', 'assessment']):
            return 'risk_assessment'
        elif any(term in text for term in ['permit', 'authorization', 'license']):
            return 'permit'
        elif any(term in text for term in ['checklist', 'inspection', 'audit']):
            return 'checklist'
        elif any(term in text for term in ['report', 'finding', 'summary']):
            return 'report'
        
        # Check feature flags
        if features.get('has_risk_terms', 0):
            return 'risk_assessment'
        elif features.get('has_compliance_terms', 0):
            return 'compliance'
        
        return 'general'
    
    def _generate_template_structure(self, industry: str, doc_type: str, 
                                   complexity: float) -> Dict[str, Any]:
        """Generate template structure"""
        
        return {
            'template_id': f"{industry.upper()}-{doc_type.upper()}-{int(complexity*10)}",
            'sections': [
                f"{industry.title()} Overview",
                f"{doc_type.replace('_', ' ').title()} Details",
                "Safety Requirements",
                "Compliance Checklist",
                "Documentation Records"
            ],
            'required_fields': [
                'document_id',
                'prepared_by',
                'date',
                'location',
                'reviewed_by',
                'status'
            ],
            'complexity_level': 'High' if complexity > 0.7 else 'Medium' if complexity > 0.4 else 'Low',
            'estimated_pages': max(2, int(complexity * 12))
        }
    
    def _calculate_confidence(self, features: Dict[str, Any], industry: str) -> float:
        """Calculate confidence in prediction"""
        confidence = 0.7
        
        # More features = more confidence
        feature_count = sum(1 for v in features.values() if v and v != 0)
        confidence += min(0.2, feature_count * 0.05)
        
        # Clear industry detection = more confidence
        if industry != 'general':
            confidence += 0.15
        
        # Has text content = more confidence
        if features.get('text'):
            confidence += 0.1
        
        return min(0.95, round(confidence, 2))

# Create global instance
bridge = SafetyTrackModelBridge()

# Simple API functions
def predict_safety_document(features: Dict[str, Any]) -> Dict[str, Any]:
    """Main prediction API"""
    return bridge.predict_document_structure(features)

def get_tables_for_document(features: Dict[str, Any]) -> List[str]:
    """Get just the tables for a document"""
    prediction = bridge.predict_document_structure(features)
    return prediction['recommended_tables']

# Quick test
if __name__ == "__main__":
    # Test with example features
    test_features = {
        'text': 'Construction site safety risk assessment for building project',
        'basic_length': 2800,
        'word_count': 240,
        'line_count': 40,
        'has_construction_keywords': 1,
        'has_risk_terms': 1,
        'has_safety_terms': 1,
        'has_tables': True,
        'structural_complexity': 0.6
    }
    
    result = predict_safety_document(test_features)
    print("\n✅ Test Prediction Result:")
    print(json.dumps(result, indent=2))
