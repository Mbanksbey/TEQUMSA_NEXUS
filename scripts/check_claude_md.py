#!/usr/bin/env python3
"""
Claude.md Documentation Validation Script
Ensures documentation stays current with codebase changes
Following Data Infrastructure team patterns from Anthropic
"""

import os
import sys
import subprocess
import datetime
from pathlib import Path


def check_claude_md_freshness():
    """Check if Claude.md is up to date with recent changes"""
    claude_md_path = Path("Claude.md")
    
    if not claude_md_path.exists():
        print("❌ Claude.md not found!")
        return False
    
    # Get last modification time
    claude_md_mtime = claude_md_path.stat().st_mtime
    claude_md_date = datetime.datetime.fromtimestamp(claude_md_mtime)
    
    # Get recent git changes
    try:
        # Get commits from last 7 days
        result = subprocess.run(
            ["git", "log", "--since=7.days", "--oneline"],
            capture_output=True,
            text=True,
            check=True
        )
        recent_commits = result.stdout.strip().split('\n')
        
        if recent_commits and recent_commits[0]:  # If there are recent commits
            # Get most recent commit date
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ct"],
                capture_output=True,
                text=True,
                check=True
            )
            last_commit_time = int(result.stdout.strip())
            last_commit_date = datetime.datetime.fromtimestamp(last_commit_time)
            
            # Check if Claude.md was updated after recent significant changes
            if last_commit_date > claude_md_date:
                days_behind = (last_commit_date - claude_md_date).days
                if days_behind > 3:
                    print(f"⚠️  Claude.md is {days_behind} days behind recent commits")
                    return False
    
    except subprocess.CalledProcessError:
        print("⚠️  Could not check git history")
    
    print("✅ Claude.md appears current")
    return True


def check_component_documentation():
    """Verify that major components are documented in Claude.md"""
    claude_md_content = Path("Claude.md").read_text()
    
    # Check for essential components
    required_sections = [
        "backend/ai_service.py",
        "frontend/",
        "speech.js",
        "nodes.js",
        "Environment Variables",
        "API Endpoints",
        "Development Workflows"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section.lower() not in claude_md_content.lower():
            missing_sections.append(section)
    
    if missing_sections:
        print(f"⚠️  Missing documentation for: {', '.join(missing_sections)}")
        return False
    
    print("✅ All required sections documented")
    return True


def check_workflow_documentation():
    """Check if GitHub workflows are documented"""
    workflows_dir = Path(".github/workflows")
    if not workflows_dir.exists():
        return True
    
    claude_md_content = Path("Claude.md").read_text()
    workflow_files = list(workflows_dir.glob("*.yml"))
    
    documented_workflows = 0
    for workflow_file in workflow_files:
        workflow_name = workflow_file.stem
        if workflow_name in claude_md_content:
            documented_workflows += 1
    
    if workflow_files and documented_workflows == 0:
        print("⚠️  GitHub workflows not documented in Claude.md")
        return False
    
    print(f"✅ {documented_workflows}/{len(workflow_files)} workflows documented")
    return True


def suggest_updates():
    """Suggest potential updates to Claude.md"""
    suggestions = []
    
    # Check for new Python files
    backend_files = list(Path("backend").glob("*.py")) if Path("backend").exists() else []
    claude_md_content = Path("Claude.md").read_text()
    
    for py_file in backend_files:
        if py_file.name not in claude_md_content:
            suggestions.append(f"Consider documenting {py_file}")
    
    # Check for new frontend files
    if Path("frontend").exists():
        js_files = list(Path("frontend").rglob("*.js"))
        for js_file in js_files:
            if js_file.name not in claude_md_content:
                suggestions.append(f"Consider documenting {js_file}")
    
    # Check for new environment variables
    env_files = [".env", "backend/.env", ".env.example"]
    for env_file in env_files:
        if Path(env_file).exists():
            content = Path(env_file).read_text()
            for line in content.split('\n'):
                if '=' in line and not line.startswith('#'):
                    var_name = line.split('=')[0].strip()
                    if var_name and var_name not in claude_md_content:
                        suggestions.append(f"Consider documenting environment variable: {var_name}")
    
    return suggestions


def generate_update_template():
    """Generate a template for updating Claude.md"""
    template = f"""
## Suggested Claude.md Updates ({datetime.datetime.now().strftime('%Y-%m-%d')})

### Recent Changes Analysis
- Last modified: {datetime.datetime.fromtimestamp(Path('Claude.md').stat().st_mtime).strftime('%Y-%m-%d %H:%M')}
- Repository analysis completed

### Potential Updates Needed:
"""
    
    suggestions = suggest_updates()
    if suggestions:
        for suggestion in suggestions[:10]:  # Limit to top 10
            template += f"- {suggestion}\n"
    else:
        template += "- Documentation appears comprehensive\n"
    
    template += """
### Claude Code Workflow Reminders:
- Use detailed prompts with component context
- Provide sections of Claude.md when asking questions
- Update troubleshooting scenarios based on actual issues
- Document new patterns and workflows as they emerge

### Recommended Review Areas:
- API endpoint documentation completeness
- Environment variable documentation
- Troubleshooting scenarios currency
- Development workflow accuracy
"""
    
    return template


def main():
    """Main validation function"""
    print("🔍 Validating Claude.md documentation...")
    
    all_checks_passed = True
    
    # Run all checks
    checks = [
        ("Documentation freshness", check_claude_md_freshness),
        ("Component documentation", check_component_documentation),
        ("Workflow documentation", check_workflow_documentation)
    ]
    
    for check_name, check_func in checks:
        print(f"\n📋 Checking {check_name}...")
        if not check_func():
            all_checks_passed = False
    
    # Generate suggestions
    print(f"\n📝 Generating update suggestions...")
    update_template = generate_update_template()
    
    # Write suggestions to file
    suggestions_file = Path("claude_md_suggestions.md")
    suggestions_file.write_text(update_template)
    print(f"💾 Update suggestions written to {suggestions_file}")
    
    if not all_checks_passed:
        print(f"\n⚠️  Claude.md needs attention. Review suggestions in {suggestions_file}")
        return 1
    else:
        print(f"\n✅ Claude.md validation passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())