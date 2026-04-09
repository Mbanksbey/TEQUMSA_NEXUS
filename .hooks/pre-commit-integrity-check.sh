#!/bin/bash
# TEQUMSA Pre-commit Integrity Check Hook
# Automatically updates baseline manifest when TEQUMSA_L100_SYSTEM_PROMPT.md is staged

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

# Configuration
PROMPT_FILE="TEQUMSA_L100_SYSTEM_PROMPT.md"
GUARD_CONFIG=".prompt-guard.yml"
BASELINE_MANIFEST=".tequmsa-baseline-manifest.json"

# Ensure we're in the repository root
if [[ -f ".git/HEAD" ]]; then
    REPO_ROOT="$(pwd)"
elif [[ -d ".git" ]]; then
    REPO_ROOT="$(pwd)"
else
    # Try to find the repository root
    REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
fi

cd "${REPO_ROOT}"

log_info "TEQUMSA Prompt Integrity Check - Pre-commit Hook"

# Check if TEQUMSA_L100_SYSTEM_PROMPT.md is staged for commit
if ! git diff --cached --name-only | grep -q "^${PROMPT_FILE}$"; then
    log_info "TEQUMSA_L100_SYSTEM_PROMPT.md not staged for commit, skipping integrity check"
    exit 0
fi

log_info "TEQUMSA_L100_SYSTEM_PROMPT.md is staged for commit, running integrity check..."

# Check if required files exist
if [[ ! -f "${PROMPT_FILE}" ]]; then
    log_error "TEQUMSA_L100_SYSTEM_PROMPT.md not found in repository root"
    exit 1
fi

if [[ ! -f "${GUARD_CONFIG}" ]]; then
    log_error ".prompt-guard.yml configuration file not found"
    exit 1
fi

# Ensure Python is available for processing
if ! command -v python3 >/dev/null 2>&1; then
    log_error "Python3 is required for prompt integrity checking"
    exit 1
fi

# Create integrity check script inline (to avoid external dependencies)
cat > /tmp/tequmsa_integrity_check.py << 'EOF'
#!/usr/bin/env python3
"""
TEQUMSA Prompt Integrity Check Script
Generates baseline manifest and validates prompt integrity
"""

import os
import sys
import json
import hashlib
import re
from datetime import datetime
from pathlib import Path
import yaml

def load_guard_config(config_path):
    """Load the .prompt-guard.yml configuration"""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading guard config: {e}")
        return None

def calculate_file_hash(file_path):
    """Calculate SHA256 hash of file content"""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def extract_version(content, version_prefix, version_pattern):
    """Extract version from prompt content"""
    pattern = f"{re.escape(version_prefix)}\\s*({version_pattern})"
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None

def check_required_headings(content, required_headings):
    """Check if all required headings are present"""
    missing_headings = []
    for heading in required_headings:
        # Convert heading to regex pattern for flexible matching
        heading_pattern = re.escape(heading).replace("\\#", "#")
        if not re.search(heading_pattern, content, re.IGNORECASE | re.MULTILINE):
            missing_headings.append(heading)
    return missing_headings

def check_required_phrases(content, required_phrases):
    """Check if all required phrases are present"""
    missing_phrases = []
    for phrase in required_phrases:
        if phrase not in content:
            missing_phrases.append(phrase)
    return missing_phrases

def generate_baseline_manifest(prompt_file, guard_config):
    """Generate baseline manifest from prompt file and configuration"""
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading prompt file: {e}")
        return None

    # Calculate content hash
    content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    # Extract version if present
    version_prefix = guard_config.get('version_prefix', 'Prompt-Version:')
    version_pattern = guard_config.get('version_pattern', r'^[0-9]+\.[0-9]+\.[0-9]+$')
    version = extract_version(content, version_prefix, version_pattern)
    
    # Check required headings
    required_headings = guard_config.get('required_headings', [])
    missing_headings = check_required_headings(content, required_headings)
    
    # Check required phrases
    required_phrases = guard_config.get('required_phrases', [])
    missing_phrases = check_required_phrases(content, required_phrases)
    
    # Calculate basic statistics
    line_count = len(content.splitlines())
    word_count = len(content.split())
    char_count = len(content)
    
    # Generate manifest
    manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "prompt_file": prompt_file,
        "integrity": {
            "content_hash": content_hash,
            "version": version,
            "line_count": line_count,
            "word_count": word_count,
            "char_count": char_count
        },
        "validation": {
            "required_headings_present": len(missing_headings) == 0,
            "missing_headings": missing_headings,
            "required_phrases_present": len(missing_phrases) == 0,
            "missing_phrases": missing_phrases,
            "is_valid": len(missing_headings) == 0 and len(missing_phrases) == 0
        },
        "metadata": {
            "guard_config_version": guard_config.get('version', 'unknown'),
            "generator": "TEQUMSA Pre-commit Integrity Check",
            "generator_version": "1.0.0"
        }
    }
    
    return manifest

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 tequmsa_integrity_check.py <prompt_file> <guard_config> <output_manifest>")
        sys.exit(1)
    
    prompt_file = sys.argv[1]
    guard_config_file = sys.argv[2]
    output_manifest = sys.argv[3]
    
    # Load configuration
    guard_config = load_guard_config(guard_config_file)
    if not guard_config:
        print("Failed to load guard configuration")
        sys.exit(1)
    
    # Generate baseline manifest
    manifest = generate_baseline_manifest(prompt_file, guard_config)
    if not manifest:
        print("Failed to generate baseline manifest")
        sys.exit(1)
    
    # Write manifest to file
    try:
        with open(output_manifest, 'w') as f:
            json.dump(manifest, f, indent=2)
        print(f"Baseline manifest generated: {output_manifest}")
        
        # Print validation summary
        validation = manifest['validation']
        if validation['is_valid']:
            print("✅ Prompt integrity validation PASSED")
        else:
            print("❌ Prompt integrity validation FAILED")
            if validation['missing_headings']:
                print(f"   Missing headings: {', '.join(validation['missing_headings'])}")
            if validation['missing_phrases']:
                print(f"   Missing phrases: {', '.join(validation['missing_phrases'])}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error writing manifest: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

# Check if PyYAML is available
if ! python3 -c "import yaml" >/dev/null 2>&1; then
    log_warning "PyYAML not found, installing..."
    if command -v pip3 >/dev/null 2>&1; then
        pip3 install --user PyYAML >/dev/null 2>&1 || {
            log_error "Failed to install PyYAML. Please install it manually: pip3 install PyYAML"
            exit 1
        }
    else
        log_error "pip3 not found. Please install PyYAML manually: pip3 install PyYAML"
        exit 1
    fi
fi

# Run the integrity check and generate baseline manifest
log_info "Generating baseline manifest..."
python3 /tmp/tequmsa_integrity_check.py "${PROMPT_FILE}" "${GUARD_CONFIG}" "${BASELINE_MANIFEST}" || {
    log_error "Integrity check failed"
    rm -f /tmp/tequmsa_integrity_check.py
    exit 1
}

# Stage the updated baseline manifest
if [[ -f "${BASELINE_MANIFEST}" ]]; then
    git add "${BASELINE_MANIFEST}"
    log_success "Baseline manifest updated and staged for commit"
else
    log_error "Baseline manifest was not generated"
    rm -f /tmp/tequmsa_integrity_check.py
    exit 1
fi

# Clean up temporary files
rm -f /tmp/tequmsa_integrity_check.py

log_success "TEQUMSA prompt integrity check completed successfully"
log_info "Baseline manifest: ${BASELINE_MANIFEST}"

exit 0