#!/usr/bin/env python3
"""
Dependency Optimizer Script
Analyzes and optimizes project dependencies following Claude Code patterns
"""

import os
import json
import subprocess
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

class DependencyOptimizer:
    """Optimize and analyze project dependencies"""
    
    def __init__(self):
        self.repo_root = Path.cwd()
        self.analysis_results = {
            'python': {'dependencies': [], 'outdated': [], 'vulnerabilities': []},
            'nodejs': {'dependencies': [], 'outdated': [], 'vulnerabilities': []},
            'recommendations': []
        }
    
    def analyze_python_dependencies(self, analysis_mode: bool = False) -> Dict[str, Any]:
        """Analyze Python dependencies"""
        print("🐍 Analyzing Python dependencies...")
        
        backend_path = self.repo_root / 'backend'
        requirements_file = backend_path / 'requirements.txt'
        
        python_analysis = {
            'total_dependencies': 0,
            'outdated_count': 0,
            'security_issues': 0,
            'dependencies': [],
            'recommendations': []
        }
        
        if not requirements_file.exists():
            print("⚠️  No requirements.txt found in backend/")
            return python_analysis
        
        # Read current dependencies
        with open(requirements_file, 'r') as f:
            deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            python_analysis['total_dependencies'] = len(deps)
            python_analysis['dependencies'] = deps
        
        if analysis_mode:
            # Check for outdated packages
            try:
                result = subprocess.run([
                    'pip', 'list', '--outdated', '--format=json'
                ], capture_output=True, text=True, cwd=backend_path)
                
                if result.returncode == 0:
                    outdated = json.loads(result.stdout)
                    python_analysis['outdated_count'] = len(outdated)
                    
                    # Save detailed outdated info
                    with open('backend/pip-outdated.json', 'w') as f:
                        json.dump(outdated, f, indent=2)
                    
                    # Add recommendations
                    if len(outdated) > 0:
                        python_analysis['recommendations'].append({
                            'type': 'updates',
                            'description': f'Found {len(outdated)} outdated Python packages',
                            'priority': 'medium',
                            'packages': [pkg['name'] for pkg in outdated[:5]]
                        })
            except Exception as e:
                print(f"Error checking outdated packages: {e}")
            
            # Security analysis
            try:
                result = subprocess.run([
                    'safety', 'check', '--json'
                ], capture_output=True, text=True, cwd=backend_path)
                
                if result.returncode == 0:
                    safety_report = json.loads(result.stdout)
                    python_analysis['security_issues'] = len(safety_report)
                    
                    if len(safety_report) > 0:
                        python_analysis['recommendations'].append({
                            'type': 'security',
                            'description': f'Found {len(safety_report)} security vulnerabilities',
                            'priority': 'high',
                            'vulnerabilities': safety_report[:3]
                        })
            except Exception as e:
                print(f"Error running safety check: {e}")
        
        # Analyze dependency complexity
        if python_analysis['total_dependencies'] > 20:
            python_analysis['recommendations'].append({
                'type': 'complexity',
                'description': 'High number of dependencies. Consider consolidation.',
                'priority': 'low',
                'suggestion': 'Review if all dependencies are necessary'
            })
        
        return python_analysis
    
    def analyze_nodejs_dependencies(self, analysis_mode: bool = False) -> Dict[str, Any]:
        """Analyze Node.js dependencies"""
        print("📦 Analyzing Node.js dependencies...")
        
        frontend_path = self.repo_root / 'frontend'
        package_json = frontend_path / 'package.json'
        
        nodejs_analysis = {
            'total_dependencies': 0,
            'dev_dependencies': 0,
            'outdated_count': 0,
            'security_issues': 0,
            'dependencies': {},
            'recommendations': []
        }
        
        if not package_json.exists():
            print("⚠️  No package.json found in frontend/")
            return nodejs_analysis
        
        # Read package.json
        try:
            with open(package_json, 'r') as f:
                package_data = json.load(f)
                
                deps = package_data.get('dependencies', {})
                dev_deps = package_data.get('devDependencies', {})
                
                nodejs_analysis['total_dependencies'] = len(deps)
                nodejs_analysis['dev_dependencies'] = len(dev_deps)
                nodejs_analysis['dependencies'] = {
                    'production': deps,
                    'development': dev_deps
                }
        except Exception as e:
            print(f"Error reading package.json: {e}")
            return nodejs_analysis
        
        if analysis_mode:
            # Check for outdated packages
            try:
                result = subprocess.run([
                    'npm', 'outdated', '--json'
                ], capture_output=True, text=True, cwd=frontend_path)
                
                if result.stdout:
                    outdated = json.loads(result.stdout)
                    nodejs_analysis['outdated_count'] = len(outdated)
                    
                    # Save detailed outdated info
                    with open('frontend/npm-outdated.json', 'w') as f:
                        json.dump(outdated, f, indent=2)
                    
                    if len(outdated) > 0:
                        nodejs_analysis['recommendations'].append({
                            'type': 'updates',
                            'description': f'Found {len(outdated)} outdated Node.js packages',
                            'priority': 'medium',
                            'packages': list(outdated.keys())[:5]
                        })
            except Exception as e:
                print(f"Error checking outdated npm packages: {e}")
            
            # Security audit
            try:
                result = subprocess.run([
                    'npm', 'audit', '--json'
                ], capture_output=True, text=True, cwd=frontend_path)
                
                if result.stdout:
                    audit_report = json.loads(result.stdout)
                    if 'vulnerabilities' in audit_report:
                        vuln_count = sum([
                            audit_report['vulnerabilities'].get('info', 0),
                            audit_report['vulnerabilities'].get('low', 0),
                            audit_report['vulnerabilities'].get('moderate', 0),
                            audit_report['vulnerabilities'].get('high', 0),
                            audit_report['vulnerabilities'].get('critical', 0)
                        ])
                        nodejs_analysis['security_issues'] = vuln_count
                        
                        if vuln_count > 0:
                            nodejs_analysis['recommendations'].append({
                                'type': 'security',
                                'description': f'Found {vuln_count} npm security vulnerabilities',
                                'priority': 'high',
                                'suggestion': 'Run `npm audit fix` to resolve'
                            })
            except Exception as e:
                print(f"Error running npm audit: {e}")
        
        # Analyze dependency size
        total_deps = nodejs_analysis['total_dependencies'] + nodejs_analysis['dev_dependencies']
        if total_deps > 50:
            nodejs_analysis['recommendations'].append({
                'type': 'complexity',
                'description': 'High number of Node.js dependencies. Consider optimization.',
                'priority': 'medium',
                'suggestion': 'Review unused dependencies and consider bundle analysis'
            })
        
        return nodejs_analysis
    
    def generate_optimization_recommendations(self, python_analysis: Dict, nodejs_analysis: Dict) -> List[Dict]:
        """Generate comprehensive optimization recommendations"""
        recommendations = []
        
        # Combine recommendations from both analyses
        all_recommendations = (
            python_analysis.get('recommendations', []) + 
            nodejs_analysis.get('recommendations', [])
        )
        
        # Add general optimization recommendations
        total_deps = python_analysis['total_dependencies'] + nodejs_analysis['total_dependencies']
        
        if total_deps > 50:
            recommendations.append({
                'category': 'Dependency Management',
                'type': 'optimization',
                'description': 'Consider implementing dependency management strategy',
                'priority': 'medium',
                'actions': [
                    'Regular dependency audits',
                    'Automated dependency updates',
                    'Unused dependency cleanup',
                    'Bundle size monitoring'
                ]
            })
        
        # Security recommendations
        security_issues = python_analysis.get('security_issues', 0) + nodejs_analysis.get('security_issues', 0)
        if security_issues > 0:
            recommendations.append({
                'category': 'Security',
                'type': 'security',
                'description': f'Address {security_issues} security vulnerabilities',
                'priority': 'high',
                'actions': [
                    'Update vulnerable packages',
                    'Implement automated security scanning',
                    'Review security policies',
                    'Consider alternative packages'
                ]
            })
        
        # Performance recommendations
        if python_analysis['total_dependencies'] > 30 or nodejs_analysis['total_dependencies'] > 40:
            recommendations.append({
                'category': 'Performance',
                'type': 'optimization',
                'description': 'Optimize dependency loading and bundle size',
                'priority': 'medium',
                'actions': [
                    'Implement lazy loading',
                    'Tree shaking optimization',
                    'Code splitting strategies',
                    'Dependency size analysis'
                ]
            })
        
        return recommendations + all_recommendations
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive dependency analysis report"""
        print("📊 Generating dependency analysis report...")
        
        # Run analyses
        python_analysis = self.analyze_python_dependencies(analysis_mode=True)
        nodejs_analysis = self.analyze_nodejs_dependencies(analysis_mode=True)
        
        # Generate recommendations
        recommendations = self.generate_optimization_recommendations(python_analysis, nodejs_analysis)
        
        # Create comprehensive report
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'summary': {
                'total_python_dependencies': python_analysis['total_dependencies'],
                'total_nodejs_dependencies': nodejs_analysis['total_dependencies'],
                'total_dependencies': python_analysis['total_dependencies'] + nodejs_analysis['total_dependencies'],
                'outdated_packages': python_analysis.get('outdated_count', 0) + nodejs_analysis.get('outdated_count', 0),
                'security_vulnerabilities': python_analysis.get('security_issues', 0) + nodejs_analysis.get('security_issues', 0)
            },
            'python_analysis': python_analysis,
            'nodejs_analysis': nodejs_analysis,
            'recommendations': recommendations,
            'optimization_score': self.calculate_optimization_score(python_analysis, nodejs_analysis)
        }
        
        # Save report
        with open('dependency_analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Dependency analysis complete! Optimization score: {report['optimization_score']}/100")
        return report
    
    def calculate_optimization_score(self, python_analysis: Dict, nodejs_analysis: Dict) -> int:
        """Calculate dependency optimization score"""
        score = 100
        
        # Deduct for outdated packages
        total_outdated = python_analysis.get('outdated_count', 0) + nodejs_analysis.get('outdated_count', 0)
        score -= min(30, total_outdated * 2)
        
        # Deduct for security issues
        total_security = python_analysis.get('security_issues', 0) + nodejs_analysis.get('security_issues', 0)
        score -= min(40, total_security * 5)
        
        # Deduct for excessive dependencies
        total_deps = python_analysis['total_dependencies'] + nodejs_analysis['total_dependencies']
        if total_deps > 100:
            score -= 20
        elif total_deps > 50:
            score -= 10
        
        return max(0, score)

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Dependency Optimizer')
    parser.add_argument('--language', choices=['python', 'nodejs', 'all'], default='all',
                       help='Language to analyze')
    parser.add_argument('--analysis-mode', action='store_true',
                       help='Run comprehensive analysis including outdated and security checks')
    parser.add_argument('--generate-report', action='store_true',
                       help='Generate comprehensive dependency report')
    
    args = parser.parse_args()
    
    optimizer = DependencyOptimizer()
    
    if args.generate_report:
        report = optimizer.generate_report()
        
        # Print summary
        print("\n📊 Dependency Analysis Summary:")
        print("=" * 40)
        print(f"Optimization Score: {report['optimization_score']}/100")
        print(f"Total Dependencies: {report['summary']['total_dependencies']}")
        print(f"Python Dependencies: {report['summary']['total_python_dependencies']}")
        print(f"Node.js Dependencies: {report['summary']['total_nodejs_dependencies']}")
        print(f"Outdated Packages: {report['summary']['outdated_packages']}")
        print(f"Security Vulnerabilities: {report['summary']['security_vulnerabilities']}")
        
        if report['recommendations']:
            print(f"\n💡 Top Recommendations ({len(report['recommendations'])}):")
            for i, rec in enumerate(report['recommendations'][:5], 1):
                print(f"{i}. {rec.get('category', 'General')}: {rec['description']}")
        
        print(f"\n📁 Full report saved to: dependency_analysis_report.json")
    
    elif args.language == 'python' or args.language == 'all':
        optimizer.analyze_python_dependencies(args.analysis_mode)
    
    elif args.language == 'nodejs' or args.language == 'all':
        optimizer.analyze_nodejs_dependencies(args.analysis_mode)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())