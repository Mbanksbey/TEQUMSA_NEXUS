#!/usr/bin/env python3
"""
Optimization Report Generator
Combines all optimization analysis results into comprehensive reports
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

class OptimizationReportGenerator:
    """Generate comprehensive optimization reports from all analysis results"""
    
    def __init__(self):
        self.repo_root = Path.cwd()
        self.artifacts_dir = Path('.')
        self.reports = {
            'health': None,
            'dependencies': None,
            'git_cleanup': None,
            'performance': None
        }
    
    def load_analysis_reports(self) -> Dict[str, Any]:
        """Load all available analysis reports"""
        print("📊 Loading analysis reports...")
        
        # Try to load each report type
        report_files = {
            'health': 'repo_health_report.json',
            'dependencies': 'dependency_analysis_report.json',
            'git_cleanup': 'git_cleanup_report.json',
            'performance': 'performance_analysis_report.json'
        }
        
        loaded_reports = {}
        
        for report_type, filename in report_files.items():
            try:
                # Check in current directory first
                report_path = self.repo_root / filename
                if not report_path.exists():
                    # Check in artifacts directory
                    report_path = self.artifacts_dir / filename
                
                if report_path.exists():
                    with open(report_path, 'r') as f:
                        loaded_reports[report_type] = json.load(f)
                    print(f"✅ Loaded {report_type} report")
                else:
                    print(f"⚠️  {report_type} report not found: {filename}")
                    
            except Exception as e:
                print(f"❌ Error loading {report_type} report: {e}")
        
        return loaded_reports
    
    def calculate_overall_optimization_score(self, reports: Dict[str, Any]) -> int:
        """Calculate comprehensive optimization score"""
        scores = []
        weights = {
            'health': 0.3,
            'dependencies': 0.25,
            'performance': 0.25,
            'git_cleanup': 0.2
        }
        
        for report_type, weight in weights.items():
            if report_type in reports:
                report = reports[report_type]
                
                if report_type == 'health':
                    score = report.get('health_score', 0)
                elif report_type == 'dependencies':
                    score = report.get('optimization_score', 0)
                elif report_type == 'performance':
                    score = report.get('overall_performance_score', 0)
                elif report_type == 'git_cleanup':
                    # Calculate score based on cleanup needs
                    summary = report.get('summary', {})
                    score = 100
                    score -= min(30, summary.get('large_files_count', 0) * 3)
                    score -= min(20, summary.get('stale_branches_count', 0) * 2)
                    score -= min(10, summary.get('potential_duplicates', 0))
                    score = max(0, score)
                
                scores.append(score * weight)
        
        return int(sum(scores)) if scores else 0
    
    def consolidate_recommendations(self, reports: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Consolidate recommendations from all reports"""
        all_recommendations = []
        
        # Priority mapping
        priority_scores = {'high': 3, 'medium': 2, 'low': 1}
        
        for report_type, report in reports.items():
            recommendations = report.get('recommendations', [])
            
            for rec in recommendations:
                # Standardize recommendation format
                standardized_rec = {
                    'source': report_type,
                    'category': rec.get('category', rec.get('type', 'General')),
                    'description': rec.get('description', ''),
                    'priority': rec.get('priority', 'medium'),
                    'priority_score': priority_scores.get(rec.get('priority', 'medium'), 2),
                    'impact': rec.get('impact', rec.get('suggestion', 'Unknown')),
                    'actions': rec.get('actions', [])
                }
                
                # Add source-specific context
                if report_type == 'health':
                    standardized_rec['context'] = 'Repository Health'
                elif report_type == 'dependencies':
                    standardized_rec['context'] = 'Dependency Management'
                elif report_type == 'performance':
                    standardized_rec['context'] = 'Performance Optimization'
                elif report_type == 'git_cleanup':
                    standardized_rec['context'] = 'Repository Cleanup'
                
                all_recommendations.append(standardized_rec)
        
        # Sort by priority and impact
        all_recommendations.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return all_recommendations
    
    def generate_executive_summary(self, reports: Dict[str, Any], overall_score: int, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate executive summary of optimization status"""
        
        # Count recommendations by priority
        priority_counts = {'high': 0, 'medium': 0, 'low': 0}
        for rec in recommendations:
            priority_counts[rec['priority']] += 1
        
        # Gather key metrics
        metrics = {}
        
        if 'health' in reports:
            health = reports['health']
            metrics['repository_health'] = {
                'score': health.get('health_score', 0),
                'total_files': health.get('summary', {}).get('total_files', 0),
                'test_coverage': health.get('summary', {}).get('test_coverage', 0)
            }
        
        if 'dependencies' in reports:
            deps = reports['dependencies']
            metrics['dependencies'] = {
                'total_dependencies': deps.get('summary', {}).get('total_dependencies', 0),
                'outdated_packages': deps.get('summary', {}).get('outdated_packages', 0),
                'security_vulnerabilities': deps.get('summary', {}).get('security_vulnerabilities', 0)
            }
        
        if 'performance' in reports:
            perf = reports['performance']
            metrics['performance'] = {
                'score': perf.get('overall_performance_score', 0),
                'optimization_opportunities': perf.get('summary', {}).get('optimization_opportunities', 0)
            }
        
        if 'git_cleanup' in reports:
            cleanup = reports['git_cleanup']
            metrics['repository_cleanup'] = {
                'large_files': cleanup.get('summary', {}).get('large_files_count', 0),
                'stale_branches': cleanup.get('summary', {}).get('stale_branches_count', 0)
            }
        
        return {
            'overall_score': overall_score,
            'status': self.get_status_from_score(overall_score),
            'priority_breakdown': priority_counts,
            'key_metrics': metrics,
            'top_concerns': [rec for rec in recommendations if rec['priority'] == 'high'][:3],
            'quick_wins': [rec for rec in recommendations if rec['priority'] == 'low' and 'cleanup' in rec['description'].lower()][:3]
        }
    
    def get_status_from_score(self, score: int) -> str:
        """Convert score to status description"""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Fair"
        elif score >= 60:
            return "Needs Attention"
        else:
            return "Requires Immediate Action"
    
    def generate_markdown_report(self, summary: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> str:
        """Generate markdown optimization report"""
        
        report_md = f"""# Repository Optimization Report

**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Executive Summary

**Overall Optimization Score:** {summary['overall_score']}/100 ({summary['status']})

### Key Findings

"""
        
        # Add metrics summary
        if 'key_metrics' in summary:
            metrics = summary['key_metrics']
            
            if 'repository_health' in metrics:
                health = metrics['repository_health']
                report_md += f"- **Repository Health:** {health['score']}/100\n"
                report_md += f"  - Total Files: {health['total_files']}\n"
                report_md += f"  - Test Coverage: {health['test_coverage']:.1f}%\n\n"
            
            if 'dependencies' in metrics:
                deps = metrics['dependencies']
                report_md += f"- **Dependencies:** {deps['total_dependencies']} total\n"
                report_md += f"  - Outdated: {deps['outdated_packages']}\n"
                report_md += f"  - Security Issues: {deps['security_vulnerabilities']}\n\n"
            
            if 'performance' in metrics:
                perf = metrics['performance']
                report_md += f"- **Performance:** {perf['score']}/100\n"
                report_md += f"  - Optimization Opportunities: {perf['optimization_opportunities']}\n\n"
        
        # Priority breakdown
        priority_counts = summary['priority_breakdown']
        report_md += f"""### Recommendations Summary

- **High Priority:** {priority_counts['high']} items
- **Medium Priority:** {priority_counts['medium']} items  
- **Low Priority:** {priority_counts['low']} items

"""
        
        # Top concerns
        if summary.get('top_concerns'):
            report_md += "### 🚨 Top Concerns (High Priority)\n\n"
            for i, concern in enumerate(summary['top_concerns'], 1):
                report_md += f"{i}. **{concern['category']}** ({concern['source']})\n"
                report_md += f"   {concern['description']}\n\n"
        
        # Quick wins
        if summary.get('quick_wins'):
            report_md += "### ⚡ Quick Wins\n\n"
            for i, win in enumerate(summary['quick_wins'], 1):
                report_md += f"{i}. **{win['category']}** - {win['description']}\n"
        
        # Detailed recommendations
        report_md += "\n## Detailed Recommendations\n\n"
        
        current_priority = None
        for rec in recommendations:
            if rec['priority'] != current_priority:
                current_priority = rec['priority']
                report_md += f"### {current_priority.title()} Priority\n\n"
            
            report_md += f"#### {rec['category']} ({rec['context']})\n"
            report_md += f"{rec['description']}\n\n"
            
            if rec['actions']:
                report_md += "**Recommended Actions:**\n"
                for action in rec['actions']:
                    report_md += f"- {action}\n"
                report_md += "\n"
        
        # Next steps
        report_md += """## Next Steps

1. **Address High Priority Items** - Focus on security and critical performance issues
2. **Plan Medium Priority Tasks** - Schedule optimization work in upcoming sprints  
3. **Automate Monitoring** - Set up regular optimization analysis
4. **Track Progress** - Monitor improvements in future reports

## Automation Features

This report was generated by the repository optimization automation system, which includes:

- ✅ Repository health monitoring
- ✅ Dependency analysis and security scanning
- ✅ Git repository cleanup recommendations
- ✅ Performance analysis and optimization suggestions
- ✅ Automated reporting and issue creation

The optimization analysis runs weekly and can be triggered manually for immediate insights.

---

*Report generated by TEQUMSA Repository Optimization Automation*
"""
        
        return report_md
    
    def run_report_generation(self) -> Dict[str, Any]:
        """Run complete optimization report generation"""
        print("📊 Generating comprehensive optimization report...")
        
        # Load all analysis reports
        reports = self.load_analysis_reports()
        
        if not reports:
            print("❌ No analysis reports found")
            return {}
        
        # Calculate overall optimization score
        overall_score = self.calculate_overall_optimization_score(reports)
        
        # Consolidate recommendations
        recommendations = self.consolidate_recommendations(reports)
        
        # Generate executive summary
        summary = self.generate_executive_summary(reports, overall_score, recommendations)
        
        # Create comprehensive report
        final_report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'repository_path': str(self.repo_root),
            'summary': summary,
            'recommendations': recommendations[:20],  # Top 20 recommendations
            'detailed_analysis': reports,
            'optimization_score': overall_score
        }
        
        # Generate markdown report
        markdown_report = self.generate_markdown_report(summary, recommendations)
        
        # Save reports
        with open('optimization_summary.json', 'w') as f:
            json.dump(final_report, f, indent=2)
        
        with open('optimization_report.md', 'w') as f:
            f.write(markdown_report)
        
        print(f"✅ Optimization report generation complete! Overall score: {overall_score}/100")
        return final_report

def main():
    """Main execution function"""
    generator = OptimizationReportGenerator()
    report = generator.run_report_generation()
    
    if report:
        # Print summary
        print("\n📊 Optimization Report Summary:")
        print("=" * 40)
        print(f"Overall Score: {report['optimization_score']}/100")
        print(f"Status: {report['summary']['status']}")
        print(f"High Priority Items: {report['summary']['priority_breakdown']['high']}")
        print(f"Total Recommendations: {len(report['recommendations'])}")
        
        print(f"\n📁 Reports generated:")
        print(f"- optimization_summary.json (machine-readable)")
        print(f"- optimization_report.md (human-readable)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())