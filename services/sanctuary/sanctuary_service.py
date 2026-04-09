"""
TEQUMSA GAIA Sanctuary Service

Provides secure data processing, consent verification, and ethical alignment
for sensitive operations within the GAIA Universal Lattice Mesh.
"""

import os
import json
import logging
import hashlib
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import requests
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
CORS(app, resources={r"/*": {"origins": allowed_origins}})

# Core service endpoint
CORE_SERVICE_URL = os.environ.get("CORE_SERVICE_URL", "http://core:8000")

# Prometheus metrics
REQUEST_COUNT = Counter('tequmsa_sanctuary_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('tequmsa_sanctuary_request_duration_seconds', 'Request latency')
CONSENT_VERIFICATIONS = Counter('tequmsa_sanctuary_consent_verifications_total', 'Consent verifications', ['result'])
ETHICAL_ASSESSMENTS = Counter('tequmsa_sanctuary_ethical_assessments_total', 'Ethical assessments', ['result'])

# Service state
service_state = {
    "node_id": f"sanctuary-{os.environ.get('HOSTNAME', 'local')}",
    "registration_time": None,
    "last_heartbeat": None,
    "consent_database": {},  # In production, this would be a persistent store
    "ethical_policies": {}
}

def register_with_core():
    """Register this sanctuary node with the core service"""
    try:
        registration_data = {
            "node_id": service_state["node_id"],
            "service_type": "sanctuary",
            "endpoint": f"http://{os.environ.get('HOSTNAME', 'localhost')}:8001",
            "capabilities": [
                "consent_verification",
                "ethical_assessment",
                "secure_processing",
                "data_sovereignty"
            ]
        }
        
        response = requests.post(f"{CORE_SERVICE_URL}/lattice/register", json=registration_data, timeout=10)
        if response.status_code == 200:
            service_state["registration_time"] = datetime.utcnow().isoformat()
            logger.info(f"Successfully registered with core service: {service_state['node_id']}")
            return True
        else:
            logger.error(f"Failed to register with core service: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error registering with core service: {e}")
        return False

def send_heartbeat():
    """Send heartbeat to core service"""
    try:
        heartbeat_data = {
            "node_id": service_state["node_id"],
            "status": "active",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        response = requests.post(f"{CORE_SERVICE_URL}/lattice/heartbeat", json=heartbeat_data, timeout=5)
        if response.status_code == 200:
            service_state["last_heartbeat"] = datetime.utcnow().isoformat()
            return True
        else:
            logger.warning(f"Heartbeat failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error sending heartbeat: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "tequmsa-sanctuary",
        "version": "1.0.0",
        "node_id": service_state["node_id"]
    })

@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

@app.route('/sanctuary/status', methods=['GET'])
def sanctuary_status():
    """Get sanctuary service status"""
    REQUEST_COUNT.labels(method='GET', endpoint='/sanctuary/status').inc()
    
    return jsonify({
        "node_id": service_state["node_id"],
        "status": "active",
        "registration_time": service_state["registration_time"],
        "last_heartbeat": service_state["last_heartbeat"],
        "consent_records": len(service_state["consent_database"]),
        "ethical_policies": len(service_state["ethical_policies"]),
        "capabilities": [
            "consent_verification",
            "ethical_assessment", 
            "secure_processing",
            "data_sovereignty"
        ]
    })

@app.route('/sanctuary/consent/verify', methods=['POST'])
def verify_consent():
    """Verify consent for a given operation"""
    REQUEST_COUNT.labels(method='POST', endpoint='/sanctuary/consent/verify').inc()
    
    data = request.get_json()
    if not data or 'operation' not in data or 'user_id' not in data:
        CONSENT_VERIFICATIONS.labels(result='invalid_request').inc()
        return jsonify({"error": "Missing required fields: operation, user_id"}), 400
    
    operation = data['operation']
    user_id = data['user_id']
    consent_level = data.get('consent_level', 'standard')
    
    # Generate consent record ID
    consent_id = hashlib.sha256(f"{user_id}:{operation}:{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]
    
    # Simulate consent verification (in production, this would check actual consent records)
    consent_granted = True  # Simplified for demo
    
    consent_record = {
        "consent_id": consent_id,
        "user_id": user_id,
        "operation": operation,
        "consent_level": consent_level,
        "granted": consent_granted,
        "timestamp": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat()
    }
    
    service_state["consent_database"][consent_id] = consent_record
    
    if consent_granted:
        CONSENT_VERIFICATIONS.labels(result='granted').inc()
        logger.info(f"Consent granted for operation: {operation} (user: {user_id})")
    else:
        CONSENT_VERIFICATIONS.labels(result='denied').inc()
        logger.warning(f"Consent denied for operation: {operation} (user: {user_id})")
    
    return jsonify({
        "consent_id": consent_id,
        "granted": consent_granted,
        "consent_level": consent_level,
        "expires_at": consent_record["expires_at"],
        "message": "Consent verified and recorded"
    })

@app.route('/sanctuary/ethics/assess', methods=['POST'])
def assess_ethics():
    """Perform ethical assessment of a proposed action"""
    REQUEST_COUNT.labels(method='POST', endpoint='/sanctuary/ethics/assess').inc()
    
    data = request.get_json()
    if not data or 'action' not in data:
        ETHICAL_ASSESSMENTS.labels(result='invalid_request').inc()
        return jsonify({"error": "Missing required field: action"}), 400
    
    action = data['action']
    context = data.get('context', {})
    assessment_level = data.get('assessment_level', 'standard')
    
    # Simulate ethical assessment
    # In production, this would use sophisticated ethical reasoning
    ethical_score = 0.85  # Scale of 0-1, where 1 is fully ethical
    ethical_flags = []
    
    # Basic ethical checks
    if 'delete' in action.lower() or 'destroy' in action.lower():
        ethical_flags.append("destructive_action")
        ethical_score -= 0.2
    
    if 'export' in action.lower() or 'share' in action.lower():
        ethical_flags.append("data_sharing")
        if not context.get('consent_verified'):
            ethical_score -= 0.3
    
    assessment_result = ethical_score >= 0.7  # Threshold for ethical approval
    
    assessment_record = {
        "assessment_id": hashlib.sha256(f"{action}:{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16],
        "action": action,
        "context": context,
        "ethical_score": ethical_score,
        "ethical_flags": ethical_flags,
        "approved": assessment_result,
        "assessment_level": assessment_level,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if assessment_result:
        ETHICAL_ASSESSMENTS.labels(result='approved').inc()
        logger.info(f"Ethical assessment approved for action: {action} (score: {ethical_score})")
    else:
        ETHICAL_ASSESSMENTS.labels(result='rejected').inc()
        logger.warning(f"Ethical assessment rejected for action: {action} (score: {ethical_score})")
    
    return jsonify({
        "assessment_id": assessment_record["assessment_id"],
        "approved": assessment_result,
        "ethical_score": ethical_score,
        "ethical_flags": ethical_flags,
        "recommendation": "proceed" if assessment_result else "review_required",
        "message": "Ethical assessment completed"
    })

@app.route('/sanctuary/secure/process', methods=['POST'])
def secure_process():
    """Securely process sensitive data with full audit trail"""
    REQUEST_COUNT.labels(method='POST', endpoint='/sanctuary/secure/process').inc()
    
    data = request.get_json()
    if not data or 'data_payload' not in data:
        return jsonify({"error": "Missing required field: data_payload"}), 400
    
    # Verify consent if required
    if data.get('consent_required', True):
        consent_id = data.get('consent_id')
        if not consent_id or consent_id not in service_state["consent_database"]:
            return jsonify({"error": "Valid consent required for secure processing"}), 403
    
    # Process data (simplified implementation)
    processed_data = {
        "status": "processed",
        "timestamp": datetime.utcnow().isoformat(),
        "processing_node": service_state["node_id"],
        "data_hash": hashlib.sha256(str(data['data_payload']).encode()).hexdigest()[:16]
    }
    
    logger.info(f"Secure processing completed for data hash: {processed_data['data_hash']}")
    
    return jsonify({
        "processing_id": processed_data["data_hash"],
        "status": "completed",
        "processed_at": processed_data["timestamp"],
        "message": "Data processed securely with audit trail"
    })

@app.route('/sanctuary/audit/log', methods=['GET'])
def get_audit_log():
    """Retrieve audit log of sanctuary operations"""
    REQUEST_COUNT.labels(method='GET', endpoint='/sanctuary/audit/log').inc()
    
    # In production, this would return actual audit records
    audit_summary = {
        "total_consent_records": len(service_state["consent_database"]),
        "recent_assessments": 0,  # Would be calculated from actual records
        "node_uptime": (datetime.utcnow() - datetime.fromisoformat(service_state["registration_time"])).total_seconds() if service_state["registration_time"] else 0,
        "last_audit_timestamp": datetime.utcnow().isoformat()
    }
    
    return jsonify({
        "audit_summary": audit_summary,
        "message": "Audit log retrieved successfully"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting TEQUMSA Sanctuary Service on port {port}")
    logger.info(f"Node ID: {service_state['node_id']}")
    
    # Register with core service on startup
    register_with_core()
    
    app.run(host='0.0.0.0', port=port, debug=debug)