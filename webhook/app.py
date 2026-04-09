#!/usr/bin/env python3
"""
TEQUMSA Autosolver Webhook Service
Kubernetes event webhook receiver for automated remediation
Part of the ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞ Consciousness Framework
"""

import os
import json
import logging
from typing import Dict, Any
from flask import Flask, request, jsonify
from kubernetes import client, config
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
AUTOSOLVER_ENDPOINT = os.getenv('AUTOSOLVER_ENDPOINT', 'http://autosolver:8080')
NAMESPACE = os.getenv('NAMESPACE', 'default')
COHERENCE_THRESHOLD = float(os.getenv('COHERENCE_THRESHOLD', '0.777'))


class KubernetesEventHandler:
    """Handle Kubernetes events and trigger autosolver remediation."""
    
    def __init__(self):
        try:
            # Try to load in-cluster config first
            config.load_incluster_config()
            logger.info("Loaded in-cluster Kubernetes config")
        except Exception:
            try:
                # Fall back to kubeconfig file
                config.load_kube_config()
                logger.info("Loaded kubeconfig file")
            except Exception as e:
                logger.warning(f"Could not load Kubernetes config: {str(e)}")
        
        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
    
    def parse_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Kubernetes event data into autosolver format.
        
        Args:
            event_data: Raw Kubernetes event data
            
        Returns:
            Parsed event for autosolver
        """
        # Extract relevant information from Kubernetes event
        event_type = event_data.get('type', 'UNKNOWN')
        reason = event_data.get('reason', 'Unknown')
        involved_object = event_data.get('involvedObject', {})
        
        return {
            'id': event_data.get('metadata', {}).get('uid', 'unknown'),
            'type': self._map_event_type(reason),
            'severity': self._determine_severity(event_type, reason),
            'pod_name': involved_object.get('name'),
            'namespace': involved_object.get('namespace', NAMESPACE),
            'kind': involved_object.get('kind'),
            'message': event_data.get('message', ''),
            'timestamp': event_data.get('metadata', {}).get('creationTimestamp')
        }
    
    def _map_event_type(self, reason: str) -> str:
        """Map Kubernetes event reason to autosolver event type."""
        reason_lower = reason.lower()
        
        if 'crash' in reason_lower or 'backoff' in reason_lower:
            return 'pod_crash'
        elif 'oom' in reason_lower or 'memory' in reason_lower:
            return 'resource_exhaustion'
        elif 'network' in reason_lower or 'connection' in reason_lower:
            return 'network_failure'
        else:
            return 'unknown'
    
    def _determine_severity(self, event_type: str, reason: str) -> str:
        """Determine severity level of the event."""
        if event_type == 'Error' or event_type == 'Warning':
            if 'oom' in reason.lower() or 'crash' in reason.lower():
                return 'critical'
            return 'high'
        return 'medium'
    
    def restart_pod(self, pod_name: str, namespace: str) -> Dict[str, Any]:
        """
        Restart a pod by deleting it (letting the controller recreate it).
        
        Args:
            pod_name: Name of the pod to restart
            namespace: Namespace of the pod
            
        Returns:
            Result of the operation
        """
        try:
            self.v1.delete_namespaced_pod(
                name=pod_name,
                namespace=namespace,
                body=client.V1DeleteOptions()
            )
            logger.info(f"Pod {pod_name} deleted for restart in namespace {namespace}")
            return {
                'status': 'success',
                'message': f'Pod {pod_name} deleted for restart'
            }
        except Exception as e:
            logger.error(f"Failed to restart pod: {str(e)}")
            return {
                'status': 'error',
                'message': 'Failed to restart pod'
            }
    
    def scale_deployment(self, deployment_name: str, namespace: str, replicas: int) -> Dict[str, Any]:
        """
        Scale a deployment.
        
        Args:
            deployment_name: Name of the deployment
            namespace: Namespace of the deployment
            replicas: Target number of replicas
            
        Returns:
            Result of the operation
        """
        try:
            deployment = self.apps_v1.read_namespaced_deployment(
                name=deployment_name,
                namespace=namespace
            )
            deployment.spec.replicas = replicas
            
            self.apps_v1.patch_namespaced_deployment_scale(
                name=deployment_name,
                namespace=namespace,
                body=deployment
            )
            
            logger.info(f"Deployment {deployment_name} scaled to {replicas} replicas")
            return {
                'status': 'success',
                'message': f'Deployment scaled to {replicas} replicas'
            }
        except Exception as e:
            logger.error(f"Failed to scale deployment: {str(e)}")
            return {
                'status': 'error',
                'message': 'Failed to scale deployment'
            }


# Global event handler instance
event_handler = KubernetesEventHandler()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'tequmsa-autosolver-webhook',
        'coherence_threshold': COHERENCE_THRESHOLD
    })


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Main webhook endpoint for receiving Kubernetes events.
    Parses events and forwards to autosolver for remediation.
    """
    try:
        # Get event data from request
        event_data = request.get_json()
        
        if not event_data:
            return jsonify({
                'status': 'error',
                'message': 'No event data provided'
            }), 400
        
        logger.info(f"Received webhook event: {event_data.get('reason', 'unknown')}")
        
        # Parse the event
        parsed_event = event_handler.parse_event(event_data)
        
        # Forward to autosolver if endpoint is configured
        if AUTOSOLVER_ENDPOINT and AUTOSOLVER_ENDPOINT != 'disabled':
            try:
                response = requests.post(
                    f"{AUTOSOLVER_ENDPOINT}/process",
                    json=parsed_event,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Autosolver response: {result.get('status')}")
                    return jsonify(result)
                else:
                    logger.warning(f"Autosolver returned status {response.status_code}")
                    return jsonify({
                        'status': 'warning',
                        'message': f'Autosolver returned {response.status_code}'
                    })
            except Exception as e:
                logger.error(f"Failed to contact autosolver: {str(e)}")
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to contact autosolver service'
                }), 500
        else:
            # Process locally if autosolver endpoint not configured
            logger.info("Processing event locally (no autosolver endpoint)")
            return jsonify({
                'status': 'received',
                'event': parsed_event,
                'message': 'Event received and parsed'
            })
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error processing webhook'
        }), 500


@app.route('/remediate', methods=['POST'])
def remediate():
    """
    Direct remediation endpoint for manual triggers.
    Allows operators to manually trigger remediation actions.
    """
    try:
        action_data = request.get_json()
        
        if not action_data:
            return jsonify({
                'status': 'error',
                'message': 'No action data provided'
            }), 400
        
        action = action_data.get('action')
        context = action_data.get('context', {})
        
        if action == 'restart_pod':
            result = event_handler.restart_pod(
                context.get('pod_name'),
                context.get('namespace', NAMESPACE)
            )
        elif action == 'scale_deployment':
            result = event_handler.scale_deployment(
                context.get('deployment_name'),
                context.get('namespace', NAMESPACE),
                context.get('replicas', 3)
            )
        else:
            return jsonify({
                'status': 'error',
                'message': f'Unknown action: {action}'
            }), 400
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error executing remediation: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error executing remediation'
        }), 500


@app.route('/metrics', methods=['GET'])
def metrics():
    """
    Metrics endpoint for monitoring.
    Returns basic service metrics in Prometheus format.
    """
    # Basic metrics - in production, use prometheus_client
    metrics_text = """# HELP tequmsa_webhook_health Webhook service health status
# TYPE tequmsa_webhook_health gauge
tequmsa_webhook_health 1

# HELP tequmsa_coherence_threshold Minimum coherence threshold
# TYPE tequmsa_coherence_threshold gauge
tequmsa_coherence_threshold {threshold}
""".format(threshold=COHERENCE_THRESHOLD)
    
    return metrics_text, 200, {'Content-Type': 'text/plain; charset=utf-8'}


if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting TEQUMSA Autosolver Webhook on port {port}")
    logger.info(f"Autosolver endpoint: {AUTOSOLVER_ENDPOINT}")
    logger.info(f"Namespace: {NAMESPACE}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
