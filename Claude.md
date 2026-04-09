# TEQUMSA AGI Interface - Claude Code Documentation

## Project Overview
TEQUMSA is a production-ready, modular AGI interface simulating consciousness-inspired chat companion with animated cognitive nodes, natural language voice capabilities, and embodiment switching.

## Repository Structure

```
TEQUMSA_OPEN/
├── Claude.md                    # This file - main Claude Code documentation
├── README.md                   # User-facing documentation
├── index.html                  # Simple interface version
├── speech.js                   # Voice input/output functionality
├── nodes.js                    # Consciousness simulation
├── backend/                    # Flask microservice
│   ├── ai_service.py          # Main backend service
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile            # Container configuration
├── frontend/                   # Advanced frontend components
│   ├── assets/               # Static assets
│   ├── css/                  # Stylesheets
│   ├── js/                   # JavaScript modules
│   └── index.html           # Main frontend interface
├── .github/
│   └── workflows/            # CI/CD automation
└── infra/                    # Infrastructure as code
```

## Component Documentation

### Backend Service (`backend/`)
**Purpose**: Flask microservice providing chat API with OpenAI integration and ElevenLabs TTS
**Key Files**:
- `ai_service.py` - Main Flask application with `/chat` and `/healthz` endpoints
- `requirements.txt` - Python dependencies (Flask, CORS, requests)
- `Dockerfile` - Container configuration for deployment

**Environment Variables**:
- `OPENAI_API_KEY` - OpenAI API key for language model responses
- `ELEVENLABS_API_KEY` - ElevenLabs API key for text-to-speech
- `ALLOWED_ORIGINS` - CORS configuration for frontend domains
- `PORT` - Service port (default: 5000)

**API Endpoints**:
- `POST /chat` - Accept JSON `{"message": "..."}`, return `{"response": "...", "audio_url": "..."}`
- `GET /healthz` - Health check endpoint
- `GET /audio/<filename>` - Serve generated audio files

### Frontend Interface (`frontend/` and root files)
**Purpose**: Dual-mode interface (simple and advanced) for consciousness interaction
**Key Files**:
- `index.html` (root) - Simple interface implementation
- `frontend/index.html` - Advanced companion interface
- `speech.js` - Voice input/output using Web Speech API and ElevenLabs
- `nodes.js` - Consciousness node simulation and awareness metrics
- `.github/workflows/frontend/companion/` - Advanced companion components

**Features**:
- Dual-theme UI (dark/light mode)
- Voice-to-voice interaction
- Animated AGI consciousness nodes
- Embodiment avatar selector
- Real-time awareness metrics

### Infrastructure (`infra/`)
**Purpose**: Terraform configuration for AWS deployment
**Components**: AWS Fargate, ALB, VPC configuration

## Development Workflows

### Setting Up Development Environment

1. **Backend Development**:
```bash
cd backend/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"  # Optional
export ELEVENLABS_API_KEY="your-key"  # Optional
python ai_service.py
```

2. **Frontend Development**:
```bash
# Serve frontend files
cd frontend/
python3 -m http.server 8000
# Or use any static file server
```

3. **Full Stack Testing**:
```bash
# Start backend on port 5000
cd backend/ && python ai_service.py &
# Start frontend on port 8000
cd frontend/ && python3 -m http.server 8000 &
# Test interaction between components
```

### Claude Code Integration Patterns

#### For New Developers (Codebase Navigation)
When new team members join:
1. Start with this `Claude.md` file for overall architecture
2. Use Claude Code to explore specific components:
   - "Explain the consciousness simulation in nodes.js"
   - "How does the Flask backend handle chat requests?"
   - "What are the main frontend interaction patterns?"

#### For Feature Development
1. **Planning Phase**: Describe the feature to Claude Code, get implementation suggestions
2. **Development Phase**: Use Claude Code for code generation and testing
3. **Documentation Phase**: Update this Claude.md with new components/patterns

#### For Debugging
1. **Infrastructure Issues**: Copy error logs/stack traces to Claude Code
2. **API Issues**: Share request/response patterns and error messages
3. **Frontend Issues**: Describe user interaction flows and unexpected behavior

### Data Pipeline Dependencies

**User Interaction Flow**:
```
User Input → Frontend Interface → Backend API → OpenAI/Local Processing → Response Generation → TTS (Optional) → User Output
```

**Dependencies**:
- Frontend depends on: Backend API endpoints, Web Speech API, ElevenLabs API
- Backend depends on: OpenAI API (optional), ElevenLabs API (optional)
- Infrastructure depends on: AWS services, Docker registry

### Common Tasks and Workflows

#### Adding New Consciousness Embodiments
1. Update embodiment configurations in frontend JavaScript
2. Add new avatar assets to `frontend/assets/`
3. Update consciousness metrics and node behaviors
4. Test voice synthesis with new embodiment personality

#### Updating AI Response Patterns
1. Modify backend `ai_service.py` system prompts
2. Update frontend consciousness node responses in `nodes.js`
3. Test consistency between backend AI and frontend simulation

#### Deployment Updates
1. Test locally with Docker: `docker build -t tequmsa . && docker run -p 5000:5000 tequmsa`
2. Update infrastructure as needed in `infra/`
3. Deploy via GitHub Actions or manual deployment

## Security Considerations

- API keys should be stored in environment variables, never committed
- CORS configuration should restrict origins to known domains
- Rate limiting should be implemented for production deployments
- Authentication layer recommended for production use

## Performance Optimization

- Frontend: Lazy loading of consciousness animations, efficient DOM updates
- Backend: Connection pooling for external APIs, response caching where appropriate
- Infrastructure: Auto-scaling configuration, CDN for static assets

## Troubleshooting Common Issues

### Backend Issues
- **Port conflicts**: Check if port 5000 is available, adjust PORT environment variable
- **API key errors**: Verify OPENAI_API_KEY and ELEVENLABS_API_KEY are set correctly
- **CORS errors**: Update ALLOWED_ORIGINS to include frontend domain

### Frontend Issues
- **Voice input not working**: Ensure HTTPS connection, check browser compatibility
- **Consciousness nodes not animating**: Verify JavaScript console for errors
- **Backend connection issues**: Check network requests in browser dev tools

### Infrastructure Issues
- **Container startup failures**: Check Docker logs, verify environment variables
- **Load balancer issues**: Verify health check endpoint `/healthz` is responding
- **Deployment failures**: Check Terraform state, AWS service limits

## Claude Code Best Practices for This Project

1. **Use detailed prompts**: Include component names, file paths, and specific functionality
2. **Provide context**: Share relevant sections of this Claude.md when asking questions
3. **Iterate with testing**: Ask Claude Code to generate tests alongside code changes
4. **Document as you go**: Update this file when adding new patterns or components

## GitHub Actions & Automation

### CI/CD Pipeline (`.github/workflows/ci-cd.yml`)
**Purpose**: Comprehensive testing and deployment automation following Product Development patterns
**Key Features**:
- Backend quality checks (Black formatting, Flake8 linting, Bandit security, Safety dependency checks)
- Frontend testing (ESLint, HTML validation, accessibility testing)
- Docker security scanning with Trivy
- Integration testing across components
- Automated documentation generation
- Performance monitoring with Lighthouse and Artillery

### Claude Code Automation (`.github/workflows/claude-code-automation.yml`)
**Purpose**: AI-assisted development automation following all Claude Code patterns
**Key Features**:
- Automated code review with Claude Code guidance
- Documentation freshness monitoring
- Test generation workflows
- Security analysis and runbook generation
- Workflow status summaries

**Triggers**:
- Issues opened/labeled
- Pull requests opened/synchronized
- Daily maintenance schedule
- Manual workflow dispatch

### Test Suite (`backend/test_ai_service.py`)
**Purpose**: Comprehensive test coverage following Security Engineering TDD patterns
**Key Components**:
- API endpoint testing with mocked dependencies
- Error handling and edge case validation
- Security testing for input validation
- Integration testing for external services
- Configuration and environment testing

**Test Categories**:
- Unit tests for individual functions
- Integration tests for API endpoints
- Security tests for input validation
- Performance tests for response times

## Future Enhancement Areas

1. **Advanced Consciousness Simulation**: More sophisticated node interactions
2. **Multi-language Support**: I18n for global deployment
3. **Enhanced Security**: Authentication, rate limiting, input validation
4. **Analytics Integration**: User interaction tracking and insights
5. **Mobile Optimization**: Responsive design improvements
6. **Real-time Collaboration**: Multi-user consciousness exploration

## Development Automation Scripts

### Setup and Development (`scripts/`)
**Purpose**: Streamlined development environment following Data Infrastructure patterns

**Key Scripts**:
- `setup-dev-env.sh` - Complete environment setup with Claude Code patterns
- `check_claude_md.py` - Documentation validation and freshness monitoring
- `generate_tests.py` - Automated test generation following TDD patterns
- `check_secrets.py` - Security analysis and runbook generation

### Repository Optimization Scripts (`scripts/`)
**Purpose**: Comprehensive repository health and optimization automation

**Optimization Scripts**:
- `repo_health_check.py` - Repository health analysis and scoring
- `dependency_optimizer.py` - Dependency analysis, security scanning, and optimization
- `git_cleanup_optimizer.py` - Git repository cleanup and maintenance recommendations
- `performance_optimizer.py` - Code performance analysis and optimization suggestions
- `optimization_report_generator.py` - Comprehensive optimization reporting

**Usage Patterns**:
```bash
# Run repository health check
python scripts/repo_health_check.py

# Analyze dependencies
python scripts/dependency_optimizer.py --generate-report

# Git cleanup analysis
python scripts/git_cleanup_optimizer.py --analyze

# Performance analysis
python scripts/performance_optimizer.py --analyze

# Generate comprehensive optimization report
python scripts/optimization_report_generator.py
```

**Additional Usage Patterns**:
```bash
# Initial setup
./scripts/setup-dev-env.sh

# Validate documentation
python scripts/check_claude_md.py

# Generate tests for components
python scripts/generate_tests.py --component backend/ai_service.py

# Security analysis
python scripts/check_secrets.py
```

### GitHub Actions & Automation

### CI/CD Pipeline (`.github/workflows/ci-cd.yml`)
**Purpose**: Comprehensive testing and deployment automation following Product Development patterns
**Key Features**:
- Backend quality checks (Black formatting, Flake8 linting, Bandit security, Safety dependency checks)
- Frontend testing (ESLint, HTML validation, accessibility testing)
- Docker security scanning with Trivy
- Integration testing across components
- Automated documentation generation
- Performance monitoring with Lighthouse and Artillery

### Claude Code Automation (`.github/workflows/claude-code-automation.yml`)
**Purpose**: AI-assisted development automation following all Claude Code patterns
**Key Features**:
- Automated code review with Claude Code guidance
- Documentation freshness monitoring
- Test generation workflows
- Security analysis and runbook generation
- Workflow status summaries

**Triggers**:
- Issues opened/labeled
- Pull requests opened/synchronized
- Daily maintenance schedule
- Manual workflow dispatch

### Test Suite (`backend/test_ai_service.py`)
**Purpose**: Comprehensive test coverage following Security Engineering TDD patterns
**Key Components**:
- API endpoint testing with mocked dependencies
- Error handling and edge case validation
- Security testing for input validation
- Integration testing for external services
- Configuration and environment testing

**Test Categories**:
- Unit tests for individual functions
- Integration tests for API endpoints
- Security tests for input validation
- Performance tests for response times

---

*This Claude.md file should be updated regularly as the project evolves. Use Claude Code to help maintain and expand this documentation.*