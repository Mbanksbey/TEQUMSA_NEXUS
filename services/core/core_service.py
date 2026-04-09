"""
TEQUMSA GAIA Core Service

The central coordination node of the GAIA Universal Lattice Mesh.
Handles system orchestration, node discovery, and lattice coordination.
"""

import os
import time
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
CORS(app, resources={r"/*": {"origins": allowed_origins}})

# Prometheus metrics
REQUEST_COUNT = Counter('tequmsa_core_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('tequmsa_core_request_duration_seconds', 'Request latency')
ACTIVE_NODES = Gauge('tequmsa_core_active_nodes', 'Number of active nodes in the lattice')
LATTICE_COHERENCE = Gauge('tequmsa_core_lattice_coherence', 'Lattice coherence level (0-1)')

# In-memory node registry (in production, this would use a persistent store)
node_registry = {}
system_status = {
    "initialization_time": datetime.utcnow().isoformat(),
    "lattice_coherence": 1.0,
    "active_nodes": 0,
    "last_pulse": None
}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for container orchestration"""
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "tequmsa-core",
        "version": "1.0.0"
    })

@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

@app.route('/lattice/status', methods=['GET'])
def lattice_status():
    """Get current lattice status and node information"""
    REQUEST_COUNT.labels(method='GET', endpoint='/lattice/status').inc()
    
    # Update metrics
    ACTIVE_NODES.set(len(node_registry))
    LATTICE_COHERENCE.set(system_status["lattice_coherence"])
    
    return jsonify({
        "status": "active",
        "nodes": list(node_registry.keys()),
        "node_count": len(node_registry),
        "coherence_level": system_status["lattice_coherence"],
        "last_pulse": system_status["last_pulse"],
        "uptime": (datetime.utcnow() - datetime.fromisoformat(system_status["initialization_time"])).total_seconds()
    })

@app.route('/lattice/register', methods=['POST'])
def register_node():
    """Register a new node in the lattice"""
    REQUEST_COUNT.labels(method='POST', endpoint='/lattice/register').inc()
    
    data = request.get_json()
    if not data or 'node_id' not in data or 'service_type' not in data:
        return jsonify({"error": "Missing required fields: node_id, service_type"}), 400
    
    node_id = data['node_id']
    node_info = {
        "service_type": data['service_type'],
        "endpoint": data.get('endpoint'),
        "capabilities": data.get('capabilities', []),
        "registration_time": datetime.utcnow().isoformat(),
        "last_heartbeat": datetime.utcnow().isoformat(),
        "status": "active"
    }
    
    node_registry[node_id] = node_info
    system_status["active_nodes"] = len(node_registry)
    
    logger.info(f"Registered node: {node_id} ({node_info['service_type']})")
    
    return jsonify({
        "message": f"Node {node_id} registered successfully",
        "lattice_status": "coherent",
        "total_nodes": len(node_registry)
    })

@app.route('/lattice/heartbeat', methods=['POST'])
def heartbeat():
    """Handle node heartbeat to maintain lattice coherence"""
    REQUEST_COUNT.labels(method='POST', endpoint='/lattice/heartbeat').inc()
    
    data = request.get_json()
    if not data or 'node_id' not in data:
        return jsonify({"error": "Missing node_id"}), 400
    
    node_id = data['node_id']
    if node_id not in node_registry:
        return jsonify({"error": "Node not registered"}), 404
    
    # Update heartbeat
    node_registry[node_id]['last_heartbeat'] = datetime.utcnow().isoformat()
    node_registry[node_id]['status'] = data.get('status', 'active')
    
    return jsonify({
        "message": "Heartbeat received",
        "lattice_coherence": system_status["lattice_coherence"]
    })

@app.route('/lattice/pulse', methods=['POST'])
def source_pulse():
    """Handle TEQUMSA source pulse for system-wide coherence"""
    REQUEST_COUNT.labels(method='POST', endpoint='/lattice/pulse').inc()
    
    data = request.get_json()
    pulse_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "pulse_type": data.get('pulse_type', 'coherence'),
        "source": data.get('source', 'unknown'),
        "message": data.get('message', 'TEQUMSA source recognition pulse')
    }
    
    system_status["last_pulse"] = pulse_data
    
    # Broadcast pulse to all active nodes (simplified implementation)
    active_nodes = [node for node, info in node_registry.items() 
                   if info['status'] == 'active']
    
    logger.info(f"Broadcasting pulse to {len(active_nodes)} nodes")
    
    return jsonify({
        "message": "Pulse broadcasted",
        "target_nodes": len(active_nodes),
        "pulse_id": pulse_data["timestamp"]
    })

@app.route('/lattice/discover', methods=['GET'])
def discover_services():
    """Service discovery endpoint"""
    REQUEST_COUNT.labels(method='GET', endpoint='/lattice/discover').inc()
    
    service_type = request.args.get('type')
    
    if service_type:
        filtered_nodes = {
            node_id: info for node_id, info in node_registry.items()
            if info['service_type'] == service_type and info['status'] == 'active'
        }
    else:
        filtered_nodes = {
            node_id: info for node_id, info in node_registry.items()
            if info['status'] == 'active'
        }
    
    return jsonify({
        "discovered_services": filtered_nodes,
        "total_count": len(filtered_nodes)
    })

@app.route('/admin/config', methods=['GET'])
def get_config():
    """Get current system configuration"""
    REQUEST_COUNT.labels(method='GET', endpoint='/admin/config').inc()
    
    config = {
        "lattice_mesh": {
            "coherence_threshold": 0.7,
            "pulse_interval": 8,
            "node_timeout": 300
        },
        "monitoring": {
            "metrics_enabled": True,
            "prometheus_endpoint": "/metrics"
        },
        "system": system_status
    }
    
    return jsonify(config)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting TEQUMSA Core Service on port {port}")
    logger.info(f"Lattice coherence initialized at {system_status['lattice_coherence']}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)