#!/bin/bash
# TEQUMSA Development Environment Setup
# Following Claude Code methodologies for streamlined development

set -e

echo "🚀 Setting up TEQUMSA development environment..."
echo "Following Claude Code development patterns from Anthropic teams"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_success "Python $PYTHON_VERSION found"
    else
        log_error "Python 3 is required but not found"
        exit 1
    fi
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        log_success "Node.js $NODE_VERSION found"
    else
        log_warning "Node.js not found - frontend development tools will be limited"
    fi
    
    # Check Git
    if command -v git &> /dev/null; then
        log_success "Git found"
    else
        log_error "Git is required but not found"
        exit 1
    fi
    
    # Check Docker (optional)
    if command -v docker &> /dev/null; then
        log_success "Docker found"
    else
        log_warning "Docker not found - containerization features will be unavailable"
    fi
}

# Setup backend environment
setup_backend() {
    log_info "Setting up backend environment..."
    
    cd backend/
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        log_info "Creating Python virtual environment..."
        python3 -m venv venv
        log_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    log_info "Activated virtual environment"
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies
    log_info "Installing backend dependencies..."
    pip install -r requirements.txt
    
    # Install development dependencies
    log_info "Installing development dependencies..."
    pip install pytest pytest-cov black flake8 bandit safety pre-commit pydoc-markdown
    
    # Create environment file
    if [ ! -f ".env" ]; then
        log_info "Creating environment configuration..."
        cat > .env << 'EOF'
# TEQUMSA Backend Configuration
# Copy this to .env.local and add your actual API keys

# OpenAI Configuration (optional - uses echo fallback if not set)
OPENAI_API_KEY=your-openai-api-key-here

# ElevenLabs Configuration (optional - no audio generation if not set)
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://localhost:8080

# Development Settings
PORT=5000
LOG_LEVEL=DEBUG
FLASK_ENV=development
EOF
        log_success "Environment configuration created (.env)"
        log_warning "Remember to update .env with your actual API keys"
    fi
    
    cd ..
    log_success "Backend setup complete"
}

# Setup frontend environment
setup_frontend() {
    log_info "Setting up frontend environment..."
    
    if command -v npm &> /dev/null; then
        cd frontend/
        
        # Install dependencies
        if [ -f "package.json" ]; then
            log_info "Installing frontend dependencies..."
            npm install
            log_success "Frontend dependencies installed"
        else
            log_warning "package.json not found in frontend/, skipping npm install"
        fi
        
        cd ..
    else
        log_warning "npm not found, skipping frontend setup"
    fi
    
    log_success "Frontend setup complete"
}

# Setup development tools
setup_dev_tools() {
    log_info "Setting up development tools..."
    
    # Install pre-commit hooks
    if command -v pre-commit &> /dev/null || pip show pre-commit &> /dev/null; then
        log_info "Installing pre-commit hooks..."
        pre-commit install
        log_success "Pre-commit hooks installed"
    else
        log_warning "pre-commit not available, install manually with: pip install pre-commit"
    fi
    
    # Make scripts executable
    log_info "Setting up development scripts..."
    chmod +x scripts/*.sh
    chmod +x .hooks/*.sh 2>/dev/null || true
    
    # Notify about optional integrity check hook
    if [ -f ".hooks/pre-commit-integrity-check.sh" ]; then
        log_info "TEQUMSA prompt integrity check hook available (optional)"
        log_info "To install: ./.hooks/install-integrity-check.sh install"
        log_info "To check status: ./.hooks/install-integrity-check.sh status"
    fi
    
    # Create development aliases
    if [ ! -f ".dev_aliases" ]; then
        cat > .dev_aliases << 'EOF'
# TEQUMSA Development Aliases
# Source this file in your shell: source .dev_aliases

# Backend development
alias tequmsa-backend="cd backend && source venv/bin/activate && python ai_service.py"
alias tequmsa-test="cd backend && source venv/bin/activate && pytest -v"
alias tequmsa-test-cov="cd backend && source venv/bin/activate && pytest --cov=. --cov-report=html"

# Frontend development
alias tequmsa-frontend="cd frontend && npm run dev"
alias tequmsa-lint="cd frontend && npm run lint"

# Full stack
alias tequmsa-dev="./scripts/start-dev.sh"
alias tequmsa-test-all="./scripts/test-all.sh"
alias tequmsa-quality="./scripts/quality-check.sh"

# Claude Code workflows
alias claude-doc="vim Claude.md"
alias claude-test-gen="python scripts/generate_tests.py"
alias claude-sync="python scripts/sync_documentation.py"

echo "🤖 TEQUMSA development aliases loaded"
echo "Use 'tequmsa-dev' to start development environment"
EOF
        log_success "Development aliases created (.dev_aliases)"
        log_info "To use aliases, run: source .dev_aliases"
    fi
    
    log_success "Development tools setup complete"
}

# Create additional helper scripts
create_helper_scripts() {
    log_info "Creating helper scripts..."
    
    # Start development script
    cat > scripts/start-dev.sh << 'EOF'
#!/bin/bash
# Start TEQUMSA development environment

echo "🚀 Starting TEQUMSA development environment..."

# Start backend in background
echo "Starting backend service..."
cd backend && source venv/bin/activate && python ai_service.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend if available
if [ -f "frontend/package.json" ]; then
    echo "Starting frontend development server..."
    cd frontend && npm run dev &
    FRONTEND_PID=$!
else
    echo "Starting simple HTTP server for frontend..."
    python3 -m http.server 8000 &
    FRONTEND_PID=$!
fi

echo "🎉 Development environment started!"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo "Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup EXIT INT TERM
wait
EOF

    # Quality check script
    cat > scripts/quality-check.sh << 'EOF'
#!/bin/bash
# Comprehensive quality check following Claude Code patterns

echo "🔍 Running comprehensive quality checks..."

cd backend/
source venv/bin/activate

echo "📝 Code formatting check..."
black --check --diff . || echo "❌ Code formatting issues found"

echo "🔧 Linting check..."
flake8 . --max-line-length=88 --extend-ignore=E203,W503 || echo "❌ Linting issues found"

echo "🔒 Security check..."
bandit -r . -f json -o bandit-report.json || echo "⚠️ Security issues found"

echo "📦 Dependency security check..."
safety check || echo "⚠️ Dependency security issues found"

echo "🧪 Running tests..."
pytest --cov=. --cov-report=term-missing

cd ../frontend/
if [ -f "package.json" ]; then
    echo "🎨 Frontend linting..."
    npm run lint || echo "❌ Frontend linting issues found"
fi

echo "✅ Quality check complete"
EOF

    # Test all script
    cat > scripts/test-all.sh << 'EOF'
#!/bin/bash
# Run all tests following Claude Code test patterns

echo "🧪 Running comprehensive test suite..."

# Backend tests
echo "Testing backend..."
cd backend/
source venv/bin/activate
pytest -v --cov=. --cov-report=html --cov-report=term-missing

# Frontend tests (if available)
cd ../frontend/
if [ -f "package.json" ]; then
    echo "Testing frontend..."
    npm run test
fi

# Integration tests
echo "Running integration tests..."
cd ..
# Add integration test commands here

echo "✅ All tests complete"
EOF

    # Make scripts executable
    chmod +x scripts/*.sh
    
    log_success "Helper scripts created"
}

# Validate setup
validate_setup() {
    log_info "Validating setup..."
    
    # Test backend
    cd backend/
    if [ -d "venv" ]; then
        source venv/bin/activate
        if python -c "import flask, flask_cors; print('Backend dependencies OK')" 2>/dev/null; then
            log_success "Backend validation passed"
        else
            log_error "Backend validation failed"
        fi
    fi
    
    # Test frontend
    cd ../frontend/
    if [ -f "package.json" ] && command -v npm &> /dev/null; then
        if npm list >/dev/null 2>&1; then
            log_success "Frontend validation passed"
        else
            log_warning "Frontend validation issues - check npm install"
        fi
    fi
    
    cd ..
    log_success "Setup validation complete"
}

# Display setup summary
show_summary() {
    echo ""
    echo "🎉 TEQUMSA Development Environment Setup Complete!"
    echo "=================================================="
    echo ""
    echo "📚 Next Steps:"
    echo "1. Review Claude.md for development patterns"
    echo "2. Update backend/.env with your API keys"
    echo "3. Source development aliases: source .dev_aliases"
    echo "4. Start development: ./scripts/start-dev.sh"
    echo ""
    echo "🔧 Available Commands:"
    echo "- ./scripts/start-dev.sh     # Start development environment"
    echo "- ./scripts/quality-check.sh # Run code quality checks"
    echo "- ./scripts/test-all.sh      # Run all tests"
    echo ""
    echo "📖 Documentation:"
    echo "- Claude.md          # Claude Code development patterns"
    echo "- DEVELOPMENT.md     # Detailed development guide"
    echo "- README.md          # Project overview"
    echo ""
    echo "🤖 Claude Code Features:"
    echo "- Comprehensive documentation in Claude.md"
    echo "- GitHub Actions for automated testing and deployment"
    echo "- Pre-commit hooks for code quality"
    echo "- Test generation and automation tools"
    echo ""
    log_success "Happy coding with Claude Code methodologies! 🚀"
}

# Main execution
main() {
    check_prerequisites
    setup_backend
    setup_frontend
    setup_dev_tools
    create_helper_scripts
    validate_setup
    show_summary
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi