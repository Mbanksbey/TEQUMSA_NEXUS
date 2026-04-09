#!/usr/bin/env python3
"""
Repository Health Check Script
Comprehensive analysis of repository health following Claude Code patterns
"""

import os
import json
import subprocess
import datetime
from pathlib import Path
from typing import Dict, List, Any
import sys

class RepositoryHealthAnalyzer:
    """Analyze repository health metrics and optimization opportunities"""
    
    def __init__(self):
        self.repo_root = Path.cwd()
        self.health_metrics = {
            'score': 0,
            'issues': [],
            'recommendations': [],
            'metrics': {}
        }
    
    def analyze_repository_structure(self) -> Dict[str, Any]:
        """Analyze repository structure and organization"""
        print("🏗️  Analyzing repository structure...")
        
        structure_metrics = {
            'total_files': 0,
            'code_files': 0,
            'documentation_files': 0,
            'config_files': 0,
            'large_files': [],
            'orphaned_files': [],
            'directory_structure_score': 0
        }
        
        # Count files by type
        for file_path in self.repo_root.rglob('*'):
            if file_path.is_file() and '.git' not in str(file_path):
                structure_metrics['total_files'] += 1
                
                # Categorize files
                suffix = file_path.suffix.lower()
                if suffix in ['.py', '.js', '.html', '.css', '.ts', '.jsx', '.tsx']:
                    structure_metrics['code_files'] += 1
                elif suffix in ['.md', '.txt', '.rst', '.doc']:
                    structure_metrics['documentation_files'] += 1
                elif suffix in ['.yml', '.yaml', '.json', '.toml', '.cfg', '.ini']:
                    structure_metrics['config_files'] += 1
                
                # Check for large files (>1MB)
                if file_path.stat().st_size > 1024 * 1024:
                    structure_metrics['large_files'].append({
                        'path': str(file_path),
                        'size_mb': round(file_path.stat().st_size / (1024 * 1024), 2)
                    })
        
        # Check for standard directories
        expected_dirs = ['backend', 'frontend', 'scripts', 'docs', 'tests', '.github']
        existing_dirs = [d.name for d in self.repo_root.iterdir() if d.is_dir()]
        
        structure_score = 0
        for expected in expected_dirs:
            if expected in existing_dirs:
                structure_score += 1
        
        structure_metrics['directory_structure_score'] = (structure_score / len(expected_dirs)) * 100
        
        # Add recommendations
        if structure_metrics['directory_structure_score'] < 80:
            self.health_metrics['recommendations'].append({
                'category': 'Repository Structure',
                'description': 'Consider organizing code into standard directories (backend, frontend, docs, tests)',
                'priority': 'medium',
                'impact': 'maintainability'
            })
        
        if len(structure_metrics['large_files']) > 0:
            self.health_metrics['recommendations'].append({
                'category': 'File Size',
                'description': f'Found {len(structure_metrics["large_files"])} large files. Consider using Git LFS or optimization.',
                'priority': 'low',
                'impact': 'performance'
            })
        
        return structure_metrics
    
    def analyze_git_health(self) -> Dict[str, Any]:
        """Analyze Git repository health"""
        print("🔄 Analyzing Git repository health...")
        
        git_metrics = {
            'commit_frequency': 0,
            'branch_count': 0,
            'active_branches': 0,
            'last_commit_days': 0,
            'commit_message_quality': 0,
            'merge_conflicts_potential': 0
        }
        
        try:
            # Get commit count in last 30 days
            result = subprocess.run([
                'git', 'rev-list', '--count', '--since=30.days.ago', 'HEAD'
            ], capture_output=True, text=True)
            if result.returncode == 0:
                git_metrics['commit_frequency'] = int(result.stdout.strip())
            
            # Get branch count
            result = subprocess.run([
                'git', 'branch', '-r'
            ], capture_output=True, text=True)
            if result.returncode == 0:
                git_metrics['branch_count'] = len(result.stdout.strip().split('\n'))
            
            # Get last commit date
            result = subprocess.run([
                'git', 'log', '-1', '--format=%ct'
            ], capture_output=True, text=True)
            if result.returncode == 0:
                last_commit_timestamp = int(result.stdout.strip())
                now = datetime.datetime.now().timestamp()
                git_metrics['last_commit_days'] = int((now - last_commit_timestamp) / 86400)
            
            # Analyze recent commit messages
            result = subprocess.run([
                'git', 'log', '--oneline', '-10'
            ], capture_output=True, text=True)
            if result.returncode == 0:
                commit_messages = result.stdout.strip().split('\n')
                quality_score = 0
                for message in commit_messages:
                    # Basic quality check: length > 10, has meaningful words
                    if len(message) > 10 and any(word in message.lower() for word in ['add', 'fix', 'update', 'remove', 'refactor']):
                        quality_score += 1
                git_metrics['commit_message_quality'] = (quality_score / len(commit_messages)) * 100
            
        except Exception as e:
            print(f"Git analysis error: {e}")
        
        # Add recommendations based on metrics
        if git_metrics['commit_frequency'] < 5:
            self.health_metrics['recommendations'].append({
                'category': 'Git Activity',
                'description': 'Low commit frequency. Consider more frequent, smaller commits.',
                'priority': 'low',
                'impact': 'collaboration'
            })
        
        if git_metrics['last_commit_days'] > 7:
            self.health_metrics['recommendations'].append({
                'category': 'Git Activity',
                'description': f'Last commit was {git_metrics["last_commit_days"]} days ago. Repository may be stale.',
                'priority': 'medium',
                'impact': 'maintenance'
            })
        
        return git_metrics
    
    def analyze_code_quality(self) -> Dict[str, Any]:
        """Analyze code quality metrics"""
        print("🔍 Analyzing code quality...")
        
        quality_metrics = {
            'python_files': 0,
            'javascript_files': 0,
            'test_coverage_estimated': 0,
            'documentation_coverage': 0,
            'complexity_score': 0
        }
        
        # Count code files
        python_files = list(self.repo_root.rglob('*.py'))
        js_files = list(self.repo_root.rglob('*.js')) + list(self.repo_root.rglob('*.ts'))
        
        quality_metrics['python_files'] = len(python_files)
        quality_metrics['javascript_files'] = len(js_files)
        
        # Estimate test coverage based on test file ratio
        test_files = list(self.repo_root.rglob('test_*.py')) + list(self.repo_root.rglob('*_test.py')) + list(self.repo_root.rglob('*.test.js'))
        total_code_files = len(python_files) + len(js_files)
        
        if total_code_files > 0:
            quality_metrics['test_coverage_estimated'] = (len(test_files) / total_code_files) * 100
        
        # Check documentation coverage
        doc_files = list(self.repo_root.rglob('*.md')) + list(self.repo_root.rglob('*.rst'))
        if total_code_files > 0:
            quality_metrics['documentation_coverage'] = min(100, (len(doc_files) / total_code_files) * 200)
        
        # Analyze complexity (basic line count analysis)
        total_lines = 0
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                    total_lines += lines
            except:
                continue
        
        if len(python_files) > 0:
            avg_file_size = total_lines / len(python_files)
            # Score based on average file size (smaller is better)
            if avg_file_size < 100:
                quality_metrics['complexity_score'] = 100
            elif avg_file_size < 300:
                quality_metrics['complexity_score'] = 80
            elif avg_file_size < 500:
                quality_metrics['complexity_score'] = 60
            else:
                quality_metrics['complexity_score'] = 40
        
        # Add recommendations
        if quality_metrics['test_coverage_estimated'] < 50:
            self.health_metrics['recommendations'].append({
                'category': 'Testing',
                'description': 'Low test coverage detected. Consider adding more tests.',
                'priority': 'high',
                'impact': 'reliability'
            })
        
        if quality_metrics['documentation_coverage'] < 30:
            self.health_metrics['recommendations'].append({
                'category': 'Documentation',
                'description': 'Limited documentation. Consider adding more README files and code comments.',
                'priority': 'medium',
                'impact': 'maintainability'
            })
        
        return quality_metrics
    
    def analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze dependency health"""
        print("📦 Analyzing dependencies...")
        
        dep_metrics = {
            'python_dependencies': 0,
            'node_dependencies': 0,
            'outdated_dependencies': [],
            'security_vulnerabilities': 0,
            'dependency_health_score': 100
        }
        
        # Analyze Python dependencies
        requirements_file = self.repo_root / 'backend' / 'requirements.txt'
        if requirements_file.exists():
            with open(requirements_file, 'r') as f:
                deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                dep_metrics['python_dependencies'] = len(deps)
        
        # Analyze Node.js dependencies
        package_json = self.repo_root / 'frontend' / 'package.json'
        if package_json.exists():
            try:
                import json as json_lib
                with open(package_json, 'r') as f:
                    package_data = json_lib.load(f)
                    deps = package_data.get('dependencies', {})
                    dev_deps = package_data.get('devDependencies', {})
                    dep_metrics['node_dependencies'] = len(deps) + len(dev_deps)
            except:
                pass
        
        # Add recommendations
        if dep_metrics['python_dependencies'] > 50:
            self.health_metrics['recommendations'].append({
                'category': 'Dependencies',
                'description': 'High number of Python dependencies. Consider dependency cleanup.',
                'priority': 'low',
                'impact': 'performance'
            })
        
        return dep_metrics
    
    def calculate_overall_score(self, metrics: Dict[str, Any]) -> int:
        """Calculate overall repository health score"""
        score_components = []
        
        # Structure score (20%)
        if 'structure' in metrics:
            score_components.append(metrics['structure']['directory_structure_score'] * 0.2)
        
        # Git health score (25%)
        if 'git' in metrics:
            git_score = 100
            if metrics['git']['last_commit_days'] > 30:
                git_score -= 30
            if metrics['git']['commit_frequency'] < 2:
                git_score -= 20
            score_components.append(git_score * 0.25)
        
        # Code quality score (35%)
        if 'quality' in metrics:
            quality_score = (
                min(100, metrics['quality']['test_coverage_estimated']) * 0.4 +
                metrics['quality']['documentation_coverage'] * 0.3 +
                metrics['quality']['complexity_score'] * 0.3
            )
            score_components.append(quality_score * 0.35)
        
        # Dependency health score (20%)
        if 'dependencies' in metrics:
            score_components.append(metrics['dependencies']['dependency_health_score'] * 0.2)
        
        return int(sum(score_components)) if score_components else 0
    
    def run_analysis(self) -> Dict[str, Any]:
        """Run complete repository health analysis"""
        print("🔍 Starting repository health analysis...")
        
        # Run all analysis components
        structure_metrics = self.analyze_repository_structure()
        git_metrics = self.analyze_git_health()
        quality_metrics = self.analyze_code_quality()
        dependency_metrics = self.analyze_dependencies()
        
        # Combine all metrics
        all_metrics = {
            'structure': structure_metrics,
            'git': git_metrics,
            'quality': quality_metrics,
            'dependencies': dependency_metrics
        }
        
        # Calculate overall score
        overall_score = self.calculate_overall_score(all_metrics)
        
        # Generate final report
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'repository_path': str(self.repo_root),
            'health_score': overall_score,
            'metrics': all_metrics,
            'recommendations': self.health_metrics['recommendations'],
            'summary': {
                'total_files': all_metrics['structure']['total_files'],
                'code_files': all_metrics['structure']['code_files'],
                'test_coverage': all_metrics['quality']['test_coverage_estimated'],
                'commit_frequency': all_metrics['git']['commit_frequency'],
                'last_commit_days': all_metrics['git']['last_commit_days']
            }
        }
        
        print(f"✅ Analysis complete! Repository health score: {overall_score}/100")
        return report

def main():
    """Main execution function"""
    analyzer = RepositoryHealthAnalyzer()
    report = analyzer.run_analysis()
    
    # Save report to file
    with open('repo_health_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n📊 Repository Health Summary:")
    print("=" * 40)
    print(f"Overall Score: {report['health_score']}/100")
    print(f"Total Files: {report['summary']['total_files']}")
    print(f"Code Files: {report['summary']['code_files']}")
    print(f"Estimated Test Coverage: {report['summary']['test_coverage']:.1f}%")
    print(f"Commits (30 days): {report['summary']['commit_frequency']}")
    print(f"Days since last commit: {report['summary']['last_commit_days']}")
    
    if report['recommendations']:
        print(f"\n💡 Top Recommendations ({len(report['recommendations'])}):")
        for i, rec in enumerate(report['recommendations'][:5], 1):
            print(f"{i}. {rec['category']}: {rec['description']}")
    
    print(f"\n📁 Full report saved to: repo_health_report.json")
    return 0

if __name__ == "__main__":
    sys.exit(main())