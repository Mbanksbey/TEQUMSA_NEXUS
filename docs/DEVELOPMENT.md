# TEQUMSA Development Environment Setup

This guide will help you set up your development environment following Claude Code methodologies for enhanced productivity and collaboration.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Life-Ambassadors-International/TEQUMSA_OPEN.git
cd TEQUMSA_OPEN

# Run the setup script
./scripts/setup-dev-env.sh

# Start development
./scripts/start-dev.sh
```

## Manual Setup

### Prerequisites

- **Python 3.9+** - Backend development
- **Node.js 18+** - Frontend tooling and testing
- **Docker** - Containerization and deployment testing
- **Git** - Version control

### Backend Setup

```bash
cd backend/

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 bandit safety pre-commit

# Set up environment variables
cp .env.example .env  # Edit with your API keys
```

### Frontend Setup

```bash
cd frontend/

# Install dependencies
npm install

# Install development tools globally (optional)
npm install -g http-server eslint prettier
```

### Development Tools Installation

```bash
# Install pre-commit hooks
pre-commit install

# Install Claude Code automation tools
pip install pydoc-markdown diagrams

# Install testing tools
npm install -g lighthouse artillery pa11y-ci

# Optional: Install TEQUMSA prompt integrity check hook
./.hooks/install-integrity-check.sh install
```

### TEQUMSA Prompt Integrity Check (Optional)

The repository includes an optional pre-commit hook that validates the integrity of `TEQUMSA_L100_SYSTEM_PROMPT.md`:

```bash
# Check hook status
./.hooks/install-integrity-check.sh status

# Install the hook (optional but recommended)
./.hooks/install-integrity-check.sh install

# Test the hook manually
git add TEQUMSA_L100_SYSTEM_PROMPT.md
./.hooks/pre-commit-integrity-check.sh
```

This hook provides:
- Automatic validation of prompt structure and required content
- Generation of baseline manifest for integrity tracking
- Local safety net before commits reach the repository

## Claude Code Development Patterns

### 1. Documentation-Driven Development (Data Infrastructure Pattern)

Always start by updating `Claude.md` with your planned changes:

```bash
# Before starting development
vim Claude.md  # Document your approach

# Use Claude Code to help plan implementation
# Ask: "How should I implement [feature] following the patterns in Claude.md?"
```

### 2. Test-First Development (Security Engineering Pattern)

Generate comprehensive tests before writing code:

```bash
# Generate test templates
python scripts/generate_tests.py --component backend/ai_service.py

# Run tests to see them fail
pytest backend/test_ai_service.py -v

# Implement functionality to make tests pass
```

### 3. Auto-Accept Development Mode (Product Development Pattern)

For non-critical features, use autonomous development with checkpoints:

```bash
# Start with clean git state
git status  # Ensure working tree is clean
git checkout -b feature/autonomous-development

# Use Claude Code with auto-accept for rapid prototyping
# Set up verification loops
npm run test:watch &  # Continuous testing
python -m pytest --watch &  # Backend test watching

# Commit frequently for easy rollback
git add . && git commit -m "Checkpoint: Initial implementation"
```

### 4. Self-Verification Loops

Set up automated verification for your development workflow:

```bash
# Backend verification loop
cd backend/
while true; do
  python -m pytest --cov=. --cov-report=term-missing
  python -m flake8 .
  python -m black --check .
  sleep 30
done &

# Frontend verification loop
cd frontend/
npm run lint:watch &
npm run test:watch &
```

## Development Workflows

### Starting New Feature Development

```bash
# 1. Review Claude.md for relevant patterns
cat Claude.md | grep -A 10 -B 10 "relevant_keyword"

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Update documentation first
vim Claude.md  # Add your feature to appropriate section

# 4. Generate tests
python scripts/generate_tests.py --feature your-feature-name

# 5. Start development with appropriate pattern
# - Synchronous: Real-time development with testing
# - Autonomous: Auto-accept mode with checkpoints
# - Hybrid: Mix of both approaches
```

### Code Quality Workflow

```bash
# Run full quality check
./scripts/quality-check.sh

# Format code
black backend/
npm run format

# Run security checks
bandit -r backend/
npm audit

# Generate coverage reports
pytest --cov=backend --cov-report=html
open htmlcov/index.html
```

### Testing Workflow

```bash
# Backend testing
cd backend/
pytest -v                          # Run all tests
pytest --cov=. --cov-report=html   # With coverage
pytest --watch                     # Continuous testing

# Frontend testing
cd frontend/
npm run test                       # All frontend tests
npm run test:accessibility         # Accessibility tests
npm run lint                       # Code quality

# Integration testing
./scripts/integration-test.sh      # Full stack testing
```

## Environment Configuration

### Environment Variables

Create `.env` files for different environments:

```bash
# backend/.env.development
OPENAI_API_KEY=your-dev-key
ELEVENLABS_API_KEY=your-dev-key
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
LOG_LEVEL=DEBUG

# backend/.env.testing
OPENAI_API_KEY=test-key
ELEVENLABS_API_KEY=test-key
ALLOWED_ORIGINS=*
LOG_LEVEL=INFO

# backend/.env.production
OPENAI_API_KEY=${OPENAI_API_KEY}
ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
ALLOWED_ORIGINS=${ALLOWED_ORIGINS}
LOG_LEVEL=WARNING
```

### Docker Development

```bash
# Build development image
docker build -t tequmsa:dev -f Dockerfile.dev .

# Run with development settings
docker run -p 5000:5000 -v $(pwd):/app tequmsa:dev

# Docker Compose for full stack
docker-compose -f docker-compose.dev.yml up
```

## Claude Code Integration Tips

### 1. Codebase Navigation

Use Claude Code to quickly understand components:

```bash
# Common Claude Code queries for this project:
# "Explain the consciousness simulation in nodes.js"
# "How does the Flask backend handle chat requests?"
# "What are the frontend interaction patterns?"
# "Show me the data flow from user input to response"
```

### 2. Debugging Workflows

When encountering issues:

```bash
# Collect debugging information
./scripts/collect-debug-info.sh > debug_info.txt

# Use Claude Code for diagnosis:
# "Here's my error log and stack trace: [paste debug_info.txt]"
# "The API is returning 500 errors with this configuration: [paste config]"
```

### 3. Documentation Synthesis

Use Claude Code to maintain documentation:

```bash
# Generate documentation updates
python scripts/sync_documentation.py

# Use Claude Code to:
# "Review my Claude.md and suggest improvements"
# "Create troubleshooting guide for common issues"
# "Generate API documentation from code comments"
```

## Performance Monitoring

### Development Performance

```bash
# Monitor backend performance
python scripts/monitor_performance.py &

# Monitor frontend performance
lighthouse http://localhost:8000 --watch

# Database/API monitoring
artillery quick --count 10 --num 2 http://localhost:5000/chat
```

### Memory and Resource Monitoring

```bash
# Monitor resource usage
./scripts/monitor-resources.sh

# Python memory profiling
python -m memory_profiler backend/ai_service.py

# Node.js performance monitoring
node --inspect frontend/js/performance_test.js
```

## Troubleshooting Common Issues

### Backend Issues

```bash
# Port conflicts
lsof -i :5000  # Check what's using port 5000
export PORT=5001  # Use different port

# Virtual environment issues
deactivate && source venv/bin/activate  # Restart venv
pip install --upgrade pip setuptools    # Update tools
```

### Frontend Issues

```bash
# Node modules issues
rm -rf node_modules package-lock.json
npm install

# Browser compatibility
npx browserslist  # Check supported browsers
npm run build     # Test build process
```

### Integration Issues

```bash
# CORS problems
export ALLOWED_ORIGINS="http://localhost:3000,http://localhost:8000"

# API connectivity
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"test"}'
```

## Team Collaboration

### Sharing Development Patterns

```bash
# Document your workflow
./scripts/document_workflow.sh > workflows/my_workflow.md

# Share Claude Code insights
git add workflows/ && git commit -m "docs: Add workflow documentation"
```

### Code Review Preparation

```bash
# Prepare for code review
./scripts/pre_review_check.sh

# Generate review summary
python scripts/generate_review_summary.py > review_summary.md
```

## Advanced Development

### Custom MCP Server Setup

For sensitive data operations, set up MCP servers instead of direct CLI access:

```bash
# Set up MCP server for database access
python scripts/setup_mcp_server.py --service database

# Configure Claude Code to use MCP server
# Instead of direct SQL access, use controlled MCP endpoints
```

### Continuous Integration

```bash
# Test CI pipeline locally
act  # Run GitHub Actions locally

# Validate workflow files
python scripts/validate_workflows.py
```

---

## Getting Help

1. **Check Claude.md** for component-specific guidance
2. **Review workflows** in `.github/workflows/` for automation patterns
3. **Run diagnostics** with `./scripts/diagnose.sh`
4. **Use Claude Code** for specific technical questions
5. **Create an issue** using the enhanced issue template

Remember: The goal is to use Claude Code methodologies to accelerate development while maintaining high code quality and comprehensive documentation.