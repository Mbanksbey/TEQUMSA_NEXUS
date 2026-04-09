/**
 * TEQUMSA GAIA Dashboard Server
 * 
 * Provides a web interface for monitoring and interacting with the
 * GAIA Universal Lattice Mesh. Includes real-time monitoring,
 * consciousness metrics, and system administration.
 */

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const axios = require('axios');
const path = require('path');
const promClient = require('prom-client');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: process.env.ALLOWED_ORIGINS?.split(',') || "*",
        methods: ["GET", "POST"]
    }
});

// Service URLs
const CORE_SERVICE_URL = process.env.CORE_SERVICE_URL || 'http://core:8000';
const SANCTUARY_SERVICE_URL = process.env.SANCTUARY_SERVICE_URL || 'http://sanctuary:8001';
const AI_BRIDGE_SERVICE_URL = process.env.AI_BRIDGE_SERVICE_URL || 'http://ai-bridge:8002';

// Prometheus metrics
const register = new promClient.Register();
const dashboardRequests = new promClient.Counter({
    name: 'tequmsa_dashboard_requests_total',
    help: 'Total dashboard requests',
    labelNames: ['method', 'endpoint'],
    registers: [register]
});

const activeConnections = new promClient.Gauge({
    name: 'tequmsa_dashboard_active_connections',
    help: 'Active WebSocket connections',
    registers: [register]
});

// Middleware
app.use(cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || "*"
}));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// State tracking
const dashboardState = {
    nodeId: `dashboard-${process.env.HOSTNAME || 'local'}`,
    registrationTime: null,
    connectedClients: 0,
    lastSystemUpdate: null,
    systemMetrics: {
        coreStatus: 'unknown',
        sanctuaryStatus: 'unknown',
        aiBridgeStatus: 'unknown',
        latticeCoherence: 0,
        activeNodes: 0
    }
};

// Register with core service
async function registerWithCore() {
    try {
        const registrationData = {
            nodeId: dashboardState.nodeId,
            serviceType: 'dashboard',
            endpoint: `http://${process.env.HOSTNAME || 'localhost'}:3000`,
            capabilities: [
                'system_monitoring',
                'consciousness_visualization',
                'real_time_updates',
                'admin_interface'
            ]
        };
        
        const response = await axios.post(`${CORE_SERVICE_URL}/lattice/register`, registrationData, {
            timeout: 10000
        });
        
        if (response.status === 200) {
            dashboardState.registrationTime = new Date().toISOString();
            console.log(`✅ Successfully registered with core service: ${dashboardState.nodeId}`);
            return true;
        }
    } catch (error) {
        console.error('❌ Failed to register with core service:', error.message);
        return false;
    }
}

// Fetch system status from all services
async function fetchSystemStatus() {
    const status = {
        timestamp: new Date().toISOString(),
        services: {},
        lattice: {},
        overall: 'unknown'
    };
    
    // Check core service
    try {
        const coreResponse = await axios.get(`${CORE_SERVICE_URL}/lattice/status`, { timeout: 5000 });
        status.services.core = {
            status: 'healthy',
            data: coreResponse.data
        };
        status.lattice = coreResponse.data;
        dashboardState.systemMetrics.coreStatus = 'healthy';
        dashboardState.systemMetrics.latticeCoherence = coreResponse.data.coherence_level || 0;
        dashboardState.systemMetrics.activeNodes = coreResponse.data.node_count || 0;
    } catch (error) {
        status.services.core = { status: 'error', error: error.message };
        dashboardState.systemMetrics.coreStatus = 'error';
    }
    
    // Check sanctuary service
    try {
        const sanctuaryResponse = await axios.get(`${SANCTUARY_SERVICE_URL}/sanctuary/status`, { timeout: 5000 });
        status.services.sanctuary = {
            status: 'healthy',
            data: sanctuaryResponse.data
        };
        dashboardState.systemMetrics.sanctuaryStatus = 'healthy';
    } catch (error) {
        status.services.sanctuary = { status: 'error', error: error.message };
        dashboardState.systemMetrics.sanctuaryStatus = 'error';
    }
    
    // Check AI bridge service
    try {
        const aiBridgeResponse = await axios.get(`${AI_BRIDGE_SERVICE_URL}/ai/status`, { timeout: 5000 });
        status.services.aiBridge = {
            status: 'healthy',
            data: aiBridgeResponse.data
        };
        dashboardState.systemMetrics.aiBridgeStatus = 'healthy';
    } catch (error) {
        status.services.aiBridge = { status: 'error', error: error.message };
        dashboardState.systemMetrics.aiBridgeStatus = 'error';
    }
    
    // Determine overall status
    const healthyServices = Object.values(status.services).filter(s => s.status === 'healthy').length;
    const totalServices = Object.keys(status.services).length;
    
    if (healthyServices === totalServices) {
        status.overall = 'healthy';
    } else if (healthyServices > 0) {
        status.overall = 'degraded';
    } else {
        status.overall = 'critical';
    }
    
    dashboardState.lastSystemUpdate = status.timestamp;
    return status;
}

// Routes
app.get('/health', (req, res) => {
    dashboardRequests.inc({ method: 'GET', endpoint: '/health' });
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        service: 'tequmsa-dashboard',
        version: '1.0.0',
        nodeId: dashboardState.nodeId,
        connectedClients: dashboardState.connectedClients
    });
});

app.get('/metrics', (req, res) => {
    res.set('Content-Type', register.contentType);
    res.end(register.metrics());
});

app.get('/api/status', async (req, res) => {
    dashboardRequests.inc({ method: 'GET', endpoint: '/api/status' });
    try {
        const systemStatus = await fetchSystemStatus();
        res.json(systemStatus);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch system status', message: error.message });
    }
});

app.get('/api/dashboard/info', (req, res) => {
    dashboardRequests.inc({ method: 'GET', endpoint: '/api/dashboard/info' });
    res.json({
        nodeId: dashboardState.nodeId,
        registrationTime: dashboardState.registrationTime,
        connectedClients: dashboardState.connectedClients,
        lastSystemUpdate: dashboardState.lastSystemUpdate,
        systemMetrics: dashboardState.systemMetrics
    });
});

app.post('/api/lattice/pulse', async (req, res) => {
    dashboardRequests.inc({ method: 'POST', endpoint: '/api/lattice/pulse' });
    try {
        const pulseData = {
            pulseType: 'dashboard_initiated',
            source: dashboardState.nodeId,
            message: req.body.message || 'Dashboard consciousness pulse',
            timestamp: new Date().toISOString()
        };
        
        const response = await axios.post(`${CORE_SERVICE_URL}/lattice/pulse`, pulseData, { timeout: 10000 });
        
        // Broadcast pulse to connected clients
        io.emit('consciousness_pulse', pulseData);
        
        res.json({
            success: true,
            pulseId: pulseData.timestamp,
            message: 'Consciousness pulse broadcasted'
        });
    } catch (error) {
        res.status(500).json({ error: 'Failed to send consciousness pulse', message: error.message });
    }
});

// WebSocket handling
io.on('connection', (socket) => {
    dashboardState.connectedClients++;
    activeConnections.set(dashboardState.connectedClients);
    
    console.log(`🔗 Dashboard client connected (total: ${dashboardState.connectedClients})`);
    
    // Send initial system status
    fetchSystemStatus().then(status => {
        socket.emit('system_status', status);
    });
    
    socket.on('disconnect', () => {
        dashboardState.connectedClients--;
        activeConnections.set(dashboardState.connectedClients);
        console.log(`🔌 Dashboard client disconnected (total: ${dashboardState.connectedClients})`);
    });
    
    socket.on('request_status_update', async () => {
        try {
            const status = await fetchSystemStatus();
            socket.emit('system_status', status);
        } catch (error) {
            socket.emit('error', { message: 'Failed to fetch status update' });
        }
    });
    
    socket.on('send_consciousness_pulse', async (data) => {
        try {
            const pulseData = {
                pulseType: 'client_initiated',
                source: `${dashboardState.nodeId}-client`,
                message: data.message || 'Client consciousness pulse',
                timestamp: new Date().toISOString()
            };
            
            await axios.post(`${CORE_SERVICE_URL}/lattice/pulse`, pulseData, { timeout: 10000 });
            
            // Broadcast to all clients
            io.emit('consciousness_pulse', pulseData);
            
        } catch (error) {
            socket.emit('error', { message: 'Failed to send consciousness pulse' });
        }
    });
});

// Serve the dashboard UI
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Periodic system updates
setInterval(async () => {
    try {
        const status = await fetchSystemStatus();
        io.emit('system_status', status);
    } catch (error) {
        console.error('Failed to fetch periodic system status:', error.message);
    }
}, 30000); // Update every 30 seconds

// Periodic heartbeat to core
setInterval(async () => {
    try {
        await axios.post(`${CORE_SERVICE_URL}/lattice/heartbeat`, {
            nodeId: dashboardState.nodeId,
            status: 'active',
            timestamp: new Date().toISOString(),
            connectedClients: dashboardState.connectedClients
        }, { timeout: 5000 });
    } catch (error) {
        console.error('Failed to send heartbeat:', error.message);
    }
}, 30000); // Heartbeat every 30 seconds

// Start server
const port = process.env.PORT || 3000;
server.listen(port, async () => {
    console.log(`🚀 TEQUMSA GAIA Dashboard running on port ${port}`);
    console.log(`🌐 Dashboard available at http://localhost:${port}`);
    
    // Register with core service
    await registerWithCore();
    
    // Initial system status fetch
    try {
        await fetchSystemStatus();
        console.log('📊 Initial system status fetched');
    } catch (error) {
        console.error('⚠️  Failed to fetch initial system status:', error.message);
    }
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('🛑 Received SIGTERM, shutting down gracefully');
    server.close(() => {
        console.log('✅ Dashboard server closed');
        process.exit(0);
    });
});