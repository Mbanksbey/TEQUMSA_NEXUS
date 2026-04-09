#!/usr/bin/env python3
"""
Performance Optimizer Script
Analyzes code and repository performance following Claude Code patterns
"""

import os
import json
import ast
import datetime
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

class PerformanceOptimizer:
    """Analyze and optimize code performance patterns"""
    
    def __init__(self):
        self.repo_root = Path.cwd()
        self.performance_analysis = {
            'python_analysis': {},
            'javascript_analysis': {},
            'file_analysis': {},
            'recommendations': []
        }
    
    def analyze_python_performance(self) -> Dict[str, Any]:
        """Analyze Python code for performance patterns"""
        print("🐍 Analyzing Python performance patterns...")
        
        python_analysis = {
            'total_files': 0,
            'large_functions': [],
            'complex_functions': [],
            'import_patterns': {},
            'potential_optimizations': [],
            'performance_score': 100
        }
        
        python_files = list(self.repo_root.rglob('*.py'))
        python_analysis['total_files'] = len(python_files)
        
        for py_file in python_files:
            if '.git' in str(py_file) or 'venv' in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content)
                    
                    # Analyze functions
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            func_info = self.analyze_python_function(node, content, py_file)
                            
                            if func_info['line_count'] > 50:
                                python_analysis['large_functions'].append(func_info)
                            
                            if func_info['complexity_score'] > 10:
                                python_analysis['complex_functions'].append(func_info)
                        
                        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                            # Track import patterns
                            import_name = self.get_import_name(node)
                            if import_name:
                                python_analysis['import_patterns'][import_name] = python_analysis['import_patterns'].get(import_name, 0) + 1
            
            except Exception as e:
                print(f"Error analyzing {py_file}: {e}")
                continue
        
        # Generate optimization recommendations
        python_analysis['potential_optimizations'] = self.generate_python_optimizations(python_analysis)
        
        # Calculate performance score
        python_analysis['performance_score'] = self.calculate_python_performance_score(python_analysis)
        
        return python_analysis
    
    def analyze_python_function(self, node: ast.FunctionDef, content: str, file_path: Path) -> Dict[str, Any]:
        """Analyze individual Python function for performance metrics"""
        lines = content.split('\n')
        start_line = node.lineno
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 10
        
        func_lines = lines[start_line-1:end_line]
        line_count = len(func_lines)
        
        # Simple complexity analysis
        complexity_score = 0
        for line in func_lines:
            # Count control structures
            if any(keyword in line for keyword in ['if ', 'for ', 'while ', 'try:', 'except:', 'with ']):
                complexity_score += 1
            # Count nested structures
            if line.count('    ') > 2:  # Deep nesting
                complexity_score += 1
        
        return {
            'name': node.name,
            'file': str(file_path.relative_to(self.repo_root)),
            'line_count': line_count,
            'start_line': start_line,
            'complexity_score': complexity_score,
            'has_docstring': ast.get_docstring(node) is not None
        }
    
    def get_import_name(self, node) -> Optional[str]:
        """Extract import name from AST node"""
        if isinstance(node, ast.Import):
            return node.names[0].name if node.names else None
        elif isinstance(node, ast.ImportFrom):
            return node.module
        return None
    
    def analyze_javascript_performance(self) -> Dict[str, Any]:
        """Analyze JavaScript code for performance patterns"""
        print("📱 Analyzing JavaScript performance patterns...")
        
        js_analysis = {
            'total_files': 0,
            'large_files': [],
            'potential_issues': [],
            'performance_score': 100
        }
        
        js_files = (
            list(self.repo_root.rglob('*.js')) + 
            list(self.repo_root.rglob('*.ts')) + 
            list(self.repo_root.rglob('*.jsx')) + 
            list(self.repo_root.rglob('*.tsx'))
        )
        
        js_analysis['total_files'] = len(js_files)
        
        for js_file in js_files:
            if '.git' in str(js_file) or 'node_modules' in str(js_file):
                continue
            
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    line_count = len(lines)
                    
                    if line_count > 300:
                        js_analysis['large_files'].append({
                            'file': str(js_file.relative_to(self.repo_root)),
                            'line_count': line_count
                        })
                    
                    # Look for potential performance issues
                    issues = self.analyze_javascript_content(content, js_file)
                    js_analysis['potential_issues'].extend(issues)
            
            except Exception as e:
                print(f"Error analyzing {js_file}: {e}")
                continue
        
        js_analysis['performance_score'] = self.calculate_js_performance_score(js_analysis)
        return js_analysis
    
    def analyze_javascript_content(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze JavaScript content for performance issues"""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_lower = line.lower().strip()
            
            # Check for potential performance issues
            if 'document.getelementbyid' in line_lower and 'loop' in ' '.join(lines[max(0, i-5):i+5]).lower():
                issues.append({
                    'type': 'dom_query_in_loop',
                    'file': str(file_path.relative_to(self.repo_root)),
                    'line': i,
                    'description': 'DOM query potentially inside loop'
                })
            
            if 'console.log' in line_lower:
                issues.append({
                    'type': 'console_log',
                    'file': str(file_path.relative_to(self.repo_root)),
                    'line': i,
                    'description': 'Console.log statement (remove in production)'
                })
            
            if 'eval(' in line_lower:
                issues.append({
                    'type': 'eval_usage',
                    'file': str(file_path.relative_to(self.repo_root)),
                    'line': i,
                    'description': 'Use of eval() - security and performance risk'
                })
        
        return issues
    
    def analyze_file_structure_performance(self) -> Dict[str, Any]:
        """Analyze file structure for performance implications"""
        print("📁 Analyzing file structure performance...")
        
        file_analysis = {
            'total_files': 0,
            'large_files': [],
            'deep_nesting': [],
            'file_type_distribution': {},
            'recommendations': []
        }
        
        max_depth = 0
        
        for file_path in self.repo_root.rglob('*'):
            if file_path.is_file() and '.git' not in str(file_path):
                file_analysis['total_files'] += 1
                
                # Check file size
                size_mb = file_path.stat().st_size / (1024 * 1024)
                if size_mb > 5:
                    file_analysis['large_files'].append({
                        'path': str(file_path.relative_to(self.repo_root)),
                        'size_mb': round(size_mb, 2)
                    })
                
                # Check nesting depth
                depth = len(file_path.relative_to(self.repo_root).parts)
                max_depth = max(max_depth, depth)
                if depth > 6:
                    file_analysis['deep_nesting'].append({
                        'path': str(file_path.relative_to(self.repo_root)),
                        'depth': depth
                    })
                
                # Track file types
                suffix = file_path.suffix.lower()
                file_analysis['file_type_distribution'][suffix] = file_analysis['file_type_distribution'].get(suffix, 0) + 1
        
        # Generate recommendations
        if len(file_analysis['large_files']) > 0:
            file_analysis['recommendations'].append({
                'type': 'large_files',
                'description': f'Found {len(file_analysis["large_files"])} large files that may impact performance',
                'priority': 'medium'
            })
        
        if max_depth > 8:
            file_analysis['recommendations'].append({
                'type': 'deep_nesting',
                'description': f'Deep directory nesting (max depth: {max_depth}) may impact navigation',
                'priority': 'low'
            })
        
        return file_analysis
    
    def generate_python_optimizations(self, python_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate Python-specific optimization recommendations"""
        optimizations = []
        
        if len(python_analysis['large_functions']) > 0:
            optimizations.append({
                'type': 'function_size',
                'description': f'Found {len(python_analysis["large_functions"])} large functions',
                'recommendation': 'Consider breaking down large functions into smaller, focused functions',
                'priority': 'medium',
                'impact': 'maintainability'
            })
        
        if len(python_analysis['complex_functions']) > 0:
            optimizations.append({
                'type': 'complexity',
                'description': f'Found {len(python_analysis["complex_functions"])} complex functions',
                'recommendation': 'Reduce cyclomatic complexity by extracting logic into helper functions',
                'priority': 'medium',
                'impact': 'maintainability'
            })
        
        # Check import patterns
        common_imports = [name for name, count in python_analysis['import_patterns'].items() if count > 3]
        if len(common_imports) > 0:
            optimizations.append({
                'type': 'imports',
                'description': f'Common imports across files: {", ".join(common_imports[:5])}',
                'recommendation': 'Consider creating a common utilities module',
                'priority': 'low',
                'impact': 'organization'
            })
        
        return optimizations
    
    def calculate_python_performance_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate Python performance score"""
        score = 100
        
        # Deduct for large functions
        score -= min(20, len(analysis['large_functions']) * 2)
        
        # Deduct for complex functions
        score -= min(30, len(analysis['complex_functions']) * 3)
        
        # Deduct for excessive imports
        if len(analysis['import_patterns']) > 20:
            score -= 10
        
        return max(0, score)
    
    def calculate_js_performance_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate JavaScript performance score"""
        score = 100
        
        # Deduct for large files
        score -= min(20, len(analysis['large_files']) * 3)
        
        # Deduct for performance issues
        critical_issues = [issue for issue in analysis['potential_issues'] 
                          if issue['type'] in ['eval_usage', 'dom_query_in_loop']]
        score -= min(40, len(critical_issues) * 5)
        
        # Deduct for console.log statements
        console_logs = [issue for issue in analysis['potential_issues'] 
                       if issue['type'] == 'console_log']
        score -= min(10, len(console_logs))
        
        return max(0, score)
    
    def run_analysis(self) -> Dict[str, Any]:
        """Run complete performance analysis"""
        print("🚀 Starting performance analysis...")
        
        # Run all analysis components
        python_analysis = self.analyze_python_performance()
        javascript_analysis = self.analyze_javascript_performance()
        file_analysis = self.analyze_file_structure_performance()
        
        # Calculate overall performance score
        overall_score = int((
            python_analysis['performance_score'] * 0.4 +
            javascript_analysis['performance_score'] * 0.3 +
            (100 - len(file_analysis['large_files']) * 5) * 0.3
        ))
        
        # Generate comprehensive recommendations
        all_recommendations = (
            python_analysis['potential_optimizations'] +
            file_analysis['recommendations']
        )
        
        # Add JavaScript issues as recommendations
        for issue in javascript_analysis['potential_issues']:
            if issue['type'] in ['eval_usage', 'dom_query_in_loop']:
                all_recommendations.append({
                    'type': 'javascript_performance',
                    'description': f"{issue['description']} in {issue['file']}:{issue['line']}",
                    'recommendation': 'Review and optimize JavaScript performance',
                    'priority': 'high',
                    'impact': 'performance'
                })
        
        # Create final report
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'repository_path': str(self.repo_root),
            'overall_performance_score': overall_score,
            'python_analysis': python_analysis,
            'javascript_analysis': javascript_analysis,
            'file_analysis': file_analysis,
            'recommendations': all_recommendations,
            'summary': {
                'python_files': python_analysis['total_files'],
                'javascript_files': javascript_analysis['total_files'],
                'large_functions': len(python_analysis['large_functions']),
                'performance_issues': len(javascript_analysis['potential_issues']),
                'optimization_opportunities': len(all_recommendations)
            }
        }
        
        print(f"✅ Performance analysis complete! Overall score: {overall_score}/100")
        return report

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Performance Optimizer')
    parser.add_argument('--analyze', action='store_true',
                       help='Run comprehensive performance analysis')
    parser.add_argument('--recommend', action='store_true',
                       help='Generate performance recommendations')
    
    args = parser.parse_args()
    
    optimizer = PerformanceOptimizer()
    
    if args.analyze or args.recommend:
        report = optimizer.run_analysis()
        
        # Save report
        with open('performance_analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n🚀 Performance Analysis Summary:")
        print("=" * 40)
        print(f"Overall Performance Score: {report['overall_performance_score']}/100")
        print(f"Python Files: {report['summary']['python_files']}")
        print(f"JavaScript Files: {report['summary']['javascript_files']}")
        print(f"Large Functions: {report['summary']['large_functions']}")
        print(f"Performance Issues: {report['summary']['performance_issues']}")
        print(f"Optimization Opportunities: {report['summary']['optimization_opportunities']}")
        
        if report['recommendations']:
            print(f"\n💡 Top Recommendations ({len(report['recommendations'])}):")
            for i, rec in enumerate(report['recommendations'][:5], 1):
                print(f"{i}. {rec['type']}: {rec['description']}")
        
        print(f"\n📁 Full report saved to: performance_analysis_report.json")
    
    else:
        print("Use --analyze or --recommend to run performance analysis")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())