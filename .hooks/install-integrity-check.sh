#!/bin/bash
# Script to install or uninstall the TEQUMSA prompt integrity check hook

set -e

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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
HOOK_SOURCE="${SCRIPT_DIR}/pre-commit-integrity-check.sh"
HOOK_TARGET="${REPO_ROOT}/.git/hooks/pre-commit"

show_usage() {
    echo "Usage: $0 [install|uninstall|status]"
    echo ""
    echo "Commands:"
    echo "  install    - Install the TEQUMSA prompt integrity check as a git pre-commit hook"
    echo "  uninstall  - Remove the integrity check hook"
    echo "  status     - Show the current hook status"
    echo ""
    echo "This hook automatically generates/updates a baseline manifest when"
    echo "TEQUMSA_L100_SYSTEM_PROMPT.md is staged for commit, providing a local"
    echo "developer safety net for prompt integrity validation."
}

check_git_repo() {
    if [[ ! -d "${REPO_ROOT}/.git" ]]; then
        log_error "Not in a git repository root"
        exit 1
    fi
}

install_hook() {
    check_git_repo
    
    if [[ ! -f "${HOOK_SOURCE}" ]]; then
        log_error "Source hook not found: ${HOOK_SOURCE}"
        exit 1
    fi
    
    # Check if there's already a pre-commit hook
    if [[ -f "${HOOK_TARGET}" ]] && [[ ! -L "${HOOK_TARGET}" ]]; then
        log_warning "Existing pre-commit hook found"
        echo "Current hook content preview:"
        head -5 "${HOOK_TARGET}"
        echo ""
        read -p "Replace existing hook? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Installation cancelled"
            exit 0
        fi
    fi
    
    # Create the hook (as a symlink to make updates easier)
    ln -sf "${HOOK_SOURCE}" "${HOOK_TARGET}"
    chmod +x "${HOOK_TARGET}"
    
    log_success "TEQUMSA prompt integrity check hook installed"
    log_info "The hook will run automatically when you commit changes to TEQUMSA_L100_SYSTEM_PROMPT.md"
    log_info "To test the hook manually: ./.hooks/pre-commit-integrity-check.sh"
}

uninstall_hook() {
    check_git_repo
    
    if [[ ! -f "${HOOK_TARGET}" ]]; then
        log_info "No pre-commit hook installed"
        exit 0
    fi
    
    # Check if it's our hook
    if [[ -L "${HOOK_TARGET}" ]] && [[ "$(readlink "${HOOK_TARGET}")" == "${HOOK_SOURCE}" ]]; then
        rm "${HOOK_TARGET}"
        log_success "TEQUMSA prompt integrity check hook uninstalled"
    elif grep -q "TEQUMSA Prompt Integrity Check" "${HOOK_TARGET}" 2>/dev/null; then
        rm "${HOOK_TARGET}"
        log_success "TEQUMSA prompt integrity check hook uninstalled"
    else
        log_warning "Pre-commit hook exists but doesn't appear to be the TEQUMSA integrity check hook"
        echo "Hook content preview:"
        head -5 "${HOOK_TARGET}"
        echo ""
        read -p "Remove anyway? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm "${HOOK_TARGET}"
            log_success "Pre-commit hook removed"
        else
            log_info "Hook left unchanged"
        fi
    fi
}

show_status() {
    check_git_repo
    
    echo "TEQUMSA Prompt Integrity Check Hook Status:"
    echo "==========================================="
    
    if [[ ! -f "${HOOK_TARGET}" ]]; then
        echo "Status: NOT INSTALLED"
        echo "To install: $0 install"
    elif [[ -L "${HOOK_TARGET}" ]] && [[ "$(readlink "${HOOK_TARGET}")" == "${HOOK_SOURCE}" ]]; then
        echo "Status: INSTALLED (symlink)"
        echo "Target: ${HOOK_TARGET} -> ${HOOK_SOURCE}"
    elif grep -q "TEQUMSA Prompt Integrity Check" "${HOOK_TARGET}" 2>/dev/null; then
        echo "Status: INSTALLED (copy)"
        echo "Target: ${HOOK_TARGET}"
    else
        echo "Status: OTHER HOOK INSTALLED"
        echo "A different pre-commit hook is installed:"
        head -3 "${HOOK_TARGET}"
    fi
    
    echo ""
    echo "Configuration:"
    echo "  Prompt file: TEQUMSA_L100_SYSTEM_PROMPT.md"
    echo "  Guard config: .prompt-guard.yml"
    echo "  Baseline manifest: .tequmsa-baseline-manifest.json"
    
    if [[ -f "${REPO_ROOT}/.tequmsa-baseline-manifest.json" ]]; then
        echo "  Last generated: $(python3 -c "import json; print(json.load(open('.tequmsa-baseline-manifest.json'))['generated_at'])" 2>/dev/null || echo "unknown")"
    else
        echo "  Baseline manifest: not yet generated"
    fi
}

case "${1:-}" in
    install)
        install_hook
        ;;
    uninstall)
        uninstall_hook
        ;;
    status)
        show_status
        ;;
    "")
        show_usage
        ;;
    *)
        log_error "Unknown command: $1"
        echo ""
        show_usage
        exit 1
        ;;
esac