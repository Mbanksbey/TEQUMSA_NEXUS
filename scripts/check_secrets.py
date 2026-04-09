#!/usr/bin/env python3
"""
Security Analysis Script for TEQUMSA
Following Security Engineering team patterns from Anthropic
Comprehensive security scanning and runbook generation
"""

import os
import re
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any
import tempfile


class SecurityAnalyzer:
    """Security analysis following Claude Code security engineering patterns"""
    
    def __init__(self):
        self.findings = []
        self.security_patterns = {
            'hardcoded_secrets': [
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'password\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']',
                r'token\s*=\s*["\'][^"\']+["\']',
                r'["\'][A-Za-z0-9]{20,}["\']',  # Long strings that might be keys
            ],
            'insecure_patterns': [
                r'eval\s*\(',
                r'exec\s*\(',
                r'shell\s*=\s*True',
                r'subprocess\.call\([^)]*shell\s*=\s*True',
                r'os\.system\s*\(',
                r'__import__\s*\(',
            ],
            'weak_crypto': [
                r'md5\s*\(',
                r'sha1\s*\(',
                r'DES\s*\(',
                r'RC4\s*\(',
            ],
            'debug_code': [
                r'console\.log\s*\(',
                r'print\s*\([^)]*debug',
                r'DEBUG\s*=\s*True',
                r'console\.debug',
            ]
        }
        
        self.file_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.json': 'json'
        }
    
    def scan_file_for_patterns(self, file_path: Path) -> List[Dict]:
        """Scan individual file for security patterns"""
        findings = []
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            return [{'type': 'scan_error', 'file': str(file_path), 'error': str(e)}]
        
        lines = content.split('\n')
        
        for pattern_category, patterns in self.security_patterns.items():
            for pattern in patterns:
                for line_num, line in enumerate(lines, 1):
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        findings.append({
                            'type': pattern_category,
                            'file': str(file_path),
                            'line': line_num,
                            'pattern': pattern,
                            'match': match.group(),
                            'context': line.strip(),
                            'severity': self.get_severity(pattern_category)
                        })
        
        return findings
    
    def get_severity(self, pattern_type: str) -> str:
        """Determine severity based on pattern type"""
        severity_map = {
            'hardcoded_secrets': 'HIGH',
            'insecure_patterns': 'HIGH',
            'weak_crypto': 'MEDIUM',
            'debug_code': 'LOW'
        }
        return severity_map.get(pattern_type, 'MEDIUM')
    
    def scan_directory(self, directory: Path) -> List[Dict]:
        """Scan directory recursively for security issues"""
        all_findings = []
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix in self.file_extensions:
                # Skip test files and generated files
                if any(skip in str(file_path) for skip in [
                    '/test_', '/.git/', '/node_modules/', '/__pycache__/',
                    '/venv/', '.pyc', '/coverage', '/dist/'
                ]):
                    continue
                
                findings = self.scan_file_for_patterns(file_path)
                all_findings.extend(findings)
        
        return all_findings
    
    def check_dependencies(self) -> List[Dict]:
        """Check dependencies for known vulnerabilities"""
        findings = []
        
        # Check Python dependencies
        if Path('backend/requirements.txt').exists():
            try:
                result = subprocess.run(
                    ['safety', 'check', '-r', 'backend/requirements.txt', '--json'],
                    capture_output=True,
                    text=True,
                    cwd='backend'
                )
                if result.returncode != 0 and result.stdout:
                    try:
                        vulnerabilities = json.loads(result.stdout)
                        for vuln in vulnerabilities:
                            findings.append({
                                'type': 'dependency_vulnerability',
                                'package': vuln.get('package'),
                                'version': vuln.get('installed_version'),
                                'vulnerability': vuln.get('vulnerability'),
                                'severity': 'HIGH'
                            })
                    except json.JSONDecodeError:
                        pass
            except FileNotFoundError:
                findings.append({
                    'type': 'tool_missing',
                    'tool': 'safety',
                    'message': 'Install with: pip install safety',
                    'severity': 'INFO'
                })
        
        # Check Node.js dependencies
        if Path('frontend/package.json').exists():
            try:
                result = subprocess.run(
                    ['npm', 'audit', '--json'],
                    capture_output=True,
                    text=True,
                    cwd='frontend'
                )
                if result.stdout:
                    try:
                        audit_data = json.loads(result.stdout)
                        vulnerabilities = audit_data.get('vulnerabilities', {})
                        for package, vuln_info in vulnerabilities.items():
                            findings.append({
                                'type': 'dependency_vulnerability',
                                'package': package,
                                'severity': vuln_info.get('severity', 'UNKNOWN').upper(),
                                'title': vuln_info.get('title', 'Unknown vulnerability')
                            })
                    except json.JSONDecodeError:
                        pass
            except FileNotFoundError:
                findings.append({
                    'type': 'tool_missing',
                    'tool': 'npm',
                    'message': 'Node.js and npm required for frontend security scanning',
                    'severity': 'INFO'
                })
        
        return findings
    
    def check_configuration_security(self) -> List[Dict]:
        """Check configuration files for security issues"""
        findings = []
        
        # Check for exposed environment files
        env_files = ['.env', 'backend/.env', '.env.local', '.env.production']
        for env_file in env_files:
            if Path(env_file).exists():
                # Check if it's in git
                try:
                    result = subprocess.run(
                        ['git', 'ls-files', env_file],
                        capture_output=True,
                        text=True
                    )
                    if result.stdout.strip():
                        findings.append({
                            'type': 'exposed_secrets',
                            'file': env_file,
                            'message': 'Environment file tracked in git',
                            'severity': 'HIGH'
                        })
                except subprocess.CalledProcessError:
                    pass
        
        # Check Docker configuration
        dockerfile_paths = ['Dockerfile', 'backend/Dockerfile']
        for dockerfile in dockerfile_paths:
            if Path(dockerfile).exists():
                content = Path(dockerfile).read_text()
                if 'ADD' in content.upper():
                    findings.append({
                        'type': 'insecure_docker',
                        'file': dockerfile,
                        'message': 'Use COPY instead of ADD in Dockerfile',
                        'severity': 'LOW'
                    })
                if '--privileged' in content:
                    findings.append({
                        'type': 'insecure_docker',
                        'file': dockerfile,
                        'message': 'Privileged mode detected',
                        'severity': 'HIGH'
                    })
        
        return findings
    
    def generate_security_report(self, findings: List[Dict]) -> str:
        """Generate comprehensive security report"""
        report = f"""# TEQUMSA Security Analysis Report
Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
"""
        
        # Count findings by severity
        severity_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0}
        for finding in findings:
            severity = finding.get('severity', 'UNKNOWN')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        report += f"""
- **Total Issues Found**: {len(findings)}
- **High Severity**: {severity_counts['HIGH']}
- **Medium Severity**: {severity_counts['MEDIUM']} 
- **Low Severity**: {severity_counts['LOW']}
- **Informational**: {severity_counts['INFO']}

## Detailed Findings

"""
        
        # Group findings by type
        findings_by_type = {}
        for finding in findings:
            finding_type = finding.get('type', 'unknown')
            if finding_type not in findings_by_type:
                findings_by_type[finding_type] = []
            findings_by_type[finding_type].append(finding)
        
        for finding_type, type_findings in findings_by_type.items():
            report += f"### {finding_type.replace('_', ' ').title()}\n\n"
            
            for finding in type_findings:
                severity = finding.get('severity', 'UNKNOWN')
                severity_emoji = {
                    'HIGH': '🔴',
                    'MEDIUM': '🟡', 
                    'LOW': '🟢',
                    'INFO': 'ℹ️'
                }.get(severity, '❓')
                
                report += f"**{severity_emoji} {severity}**: "
                
                if 'file' in finding:
                    report += f"`{finding['file']}`"
                    if 'line' in finding:
                        report += f" (line {finding['line']})"
                    report += "\n"
                
                if 'context' in finding:
                    report += f"```\n{finding['context']}\n```\n"
                
                if 'message' in finding:
                    report += f"{finding['message']}\n"
                
                report += "\n"
        
        return report
    
    def generate_security_runbook(self, findings: List[Dict]) -> str:
        """Generate security incident response runbook"""
        runbook = f"""# TEQUMSA Security Incident Response Runbook
Last Updated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}

## Quick Response Procedures

### Immediate Actions for Security Incidents

#### 1. API Key Compromise
```bash
# Immediate response
1. Rotate all API keys (OpenAI, ElevenLabs)
2. Update environment variables
3. Restart all services
4. Review access logs for unauthorized usage
5. Update Claude.md with incident learnings
```

#### 2. Code Injection Attack
```bash
# Response procedure
1. Identify attack vector
2. Isolate affected components
3. Review input validation
4. Update security filters
5. Deploy patches
```

#### 3. Container Security Breach
```bash
# Container incident response
1. Stop affected containers
2. Analyze container logs
3. Update base images
4. Scan for malware
5. Redeploy with security patches
```

## Preventive Security Measures

### Development Security (Claude Code Patterns)

#### Pre-commit Security Checks
- Run security scanners before commits
- Validate no secrets in code
- Check dependency vulnerabilities
- Verify secure coding patterns

#### Code Review Security Checklist
- [ ] Input validation implemented
- [ ] Output encoding applied
- [ ] Authentication/authorization checked
- [ ] Error handling doesn't leak information
- [ ] Logging doesn't include sensitive data

### Infrastructure Security

#### API Security
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] Authentication required for sensitive operations
- [ ] HTTPS enforced

#### Container Security
- [ ] Use minimal base images
- [ ] Run as non-root user
- [ ] Limit container privileges
- [ ] Regular security updates
- [ ] Vulnerability scanning

## Regular Security Tasks

### Daily Tasks
- Monitor application logs for anomalies
- Check for failed authentication attempts
- Review system resource usage

### Weekly Tasks
- Run dependency vulnerability scans
- Review access logs
- Update security documentation

### Monthly Tasks
- Full security assessment
- Penetration testing
- Security training review
- Incident response drill

## Security Contact Information

### Internal Contacts
- Security Team: [security@organization.com]
- DevOps Team: [devops@organization.com]
- Management: [management@organization.com]

### External Resources
- OpenAI Security: security@openai.com
- ElevenLabs Support: [support contact]
- Cloud Provider Security: [provider security contact]

## Tools and Resources

### Security Scanning Tools
- `bandit` - Python security linter
- `safety` - Python dependency scanner
- `npm audit` - Node.js dependency scanner
- `docker-bench-security` - Container security

### Monitoring Tools
- Application logs
- Access logs
- System metrics
- Network monitoring

## Incident Documentation Template

When a security incident occurs, document using this template:

```markdown
## Security Incident Report

**Date**: [YYYY-MM-DD]
**Severity**: [High/Medium/Low]
**Affected Systems**: [List systems]

### Incident Description
[Detailed description]

### Timeline
- [Time] - Initial detection
- [Time] - Response initiated
- [Time] - Containment achieved
- [Time] - Resolution completed

### Root Cause
[Analysis of how incident occurred]

### Remediation Actions
- [Action 1]
- [Action 2]
- [Action 3]

### Lessons Learned
[What we learned and how to prevent future incidents]

### Claude.md Updates Required
[Document any updates needed to development procedures]
```

## Current Security Status

Based on latest scan ({__import__('datetime').datetime.now().strftime('%Y-%m-%d')}):
"""
        
        # Add current security status based on findings
        high_findings = [f for f in findings if f.get('severity') == 'HIGH']
        if high_findings:
            runbook += f"\n⚠️ **{len(high_findings)} HIGH severity issues require immediate attention**\n"
        else:
            runbook += "\n✅ No high severity issues detected\n"
        
        runbook += """
## Integration with Claude Code Workflows

### Security in Development Process
1. Use Claude Code for security analysis of changes
2. Include security considerations in Claude.md updates
3. Implement security test generation patterns
4. Document security learnings in team sharing sessions

### Automated Security Integration
- Pre-commit hooks prevent insecure code
- CI/CD pipeline includes security scans
- Automated dependency vulnerability checking
- Security documentation stays current

---

*This runbook should be reviewed and updated regularly based on new threats and incident learnings.*
"""
        
        return runbook


def main():
    """Main security analysis function"""
    print("🔒 Running TEQUMSA security analysis...")
    print("Following Claude Code Security Engineering patterns")
    
    analyzer = SecurityAnalyzer()
    all_findings = []
    
    # Scan codebase
    print("\n📁 Scanning codebase for security patterns...")
    code_findings = analyzer.scan_directory(Path('.'))
    all_findings.extend(code_findings)
    print(f"   Found {len(code_findings)} code security issues")
    
    # Check dependencies
    print("\n📦 Checking dependencies for vulnerabilities...")
    dep_findings = analyzer.check_dependencies()
    all_findings.extend(dep_findings)
    print(f"   Found {len(dep_findings)} dependency issues")
    
    # Check configuration
    print("\n⚙️  Checking configuration security...")
    config_findings = analyzer.check_configuration_security()
    all_findings.extend(config_findings)
    print(f"   Found {len(config_findings)} configuration issues")
    
    # Generate reports
    print("\n📄 Generating security reports...")
    
    # Security analysis report
    security_report = analyzer.generate_security_report(all_findings)
    report_path = Path('security_analysis_report.md')
    report_path.write_text(security_report)
    
    # Security runbook
    security_runbook = analyzer.generate_security_runbook(all_findings)
    runbook_path = Path('SECURITY_RUNBOOK.md')
    runbook_path.write_text(security_runbook)
    
    print(f"📊 Security analysis complete:")
    print(f"   - Report: {report_path}")
    print(f"   - Runbook: {runbook_path}")
    print(f"   - Total findings: {len(all_findings)}")
    
    # Summary for exit code
    high_severity = len([f for f in all_findings if f.get('severity') == 'HIGH'])
    if high_severity > 0:
        print(f"\n⚠️  {high_severity} HIGH severity issues found!")
        print("Review the security report and address critical issues immediately.")
        return 1
    else:
        print("\n✅ No high severity security issues detected")
        return 0


if __name__ == "__main__":
    sys.exit(main())