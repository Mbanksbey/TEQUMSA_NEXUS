#!/usr/bin/env python3
"""
Git Cleanup Optimizer Script
Analyzes git repository for cleanup opportunities following Claude Code patterns
"""

import os
import json
import subprocess
import datetime
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

class GitCleanupOptimizer:
    """Analyze and optimize Git repository structure and history"""
    
    def __init__(self):
        self.repo_root = Path.cwd()
        self.cleanup_analysis = {
            'large_files': [],
            'unused_branches': [],
            'old_commits': [],
            'duplicate_files': [],
            'recommendations': []
        }
    
    def analyze_large_files(self) -> List[Dict[str, Any]]:
        """Analyze large files in repository history"""
        print("📊 Analyzing large files in repository...")
        
        large_files = []
        
        try:
            # Find large files in current working directory
            for file_path in self.repo_root.rglob('*'):
                if file_path.is_file() and '.git' not in str(file_path):
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    if size_mb > 1:  # Files larger than 1MB
                        large_files.append({
                            'path': str(file_path.relative_to(self.repo_root)),
                            'size_mb': round(size_mb, 2),
                            'type': 'current'
                        })
            
            # Find large files in git history
            result = subprocess.run([
                'git', 'rev-list', '--objects', '--all'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # This is a simplified analysis - for production, consider using git-filter-repo
                objects = result.stdout.strip().split('\n')
                
                # Get file sizes for recent objects (simplified approach)
                for obj_line in objects[:1000]:  # Limit to recent objects
                    if ' ' in obj_line:
                        obj_hash, path = obj_line.split(' ', 1)
                        try:
                            size_result = subprocess.run([
                                'git', 'cat-file', '-s', obj_hash
                            ], capture_output=True, text=True)
                            
                            if size_result.returncode == 0:
                                size_bytes = int(size_result.stdout.strip())
                                size_mb = size_bytes / (1024 * 1024)
                                
                                if size_mb > 5:  # Historical files larger than 5MB
                                    large_files.append({
                                        'path': path,
                                        'size_mb': round(size_mb, 2),
                                        'type': 'historical',
                                        'object_hash': obj_hash
                                    })
                        except:
                            continue
        
        except Exception as e:
            print(f"Error analyzing large files: {e}")
        
        # Sort by size
        large_files.sort(key=lambda x: x['size_mb'], reverse=True)
        return large_files[:20]  # Top 20 largest files
    
    def analyze_branches(self) -> Dict[str, Any]:
        """Analyze branch structure and identify cleanup opportunities"""
        print("🌿 Analyzing branch structure...")
        
        branch_analysis = {
            'total_branches': 0,
            'active_branches': [],
            'stale_branches': [],
            'merged_branches': [],
            'recommendations': []
        }
        
        try:
            # Get all branches with last commit info
            result = subprocess.run([
                'git', 'for-each-ref', '--format=%(refname:short)|%(committerdate:unix)|%(authorname)',
                'refs/heads/', 'refs/remotes/'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                branches = []
                now = datetime.datetime.now().timestamp()
                
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            branch_name = parts[0]
                            last_commit_time = int(parts[1])
                            author = parts[2]
                            days_old = int((now - last_commit_time) / 86400)
                            
                            branches.append({
                                'name': branch_name,
                                'days_old': days_old,
                                'author': author,
                                'last_commit_time': last_commit_time
                            })
                
                branch_analysis['total_branches'] = len(branches)
                
                # Categorize branches
                for branch in branches:
                    if branch['days_old'] <= 30:
                        branch_analysis['active_branches'].append(branch)
                    elif branch['days_old'] > 90:
                        branch_analysis['stale_branches'].append(branch)
                
                # Check for merged branches
                try:
                    merged_result = subprocess.run([
                        'git', 'branch', '--merged', 'main'
                    ], capture_output=True, text=True)
                    
                    if merged_result.returncode == 0:
                        merged_branches = [
                            line.strip().replace('* ', '') 
                            for line in merged_result.stdout.strip().split('\n')
                            if line.strip() and line.strip() != 'main'
                        ]
                        branch_analysis['merged_branches'] = merged_branches
                
                except:
                    pass
        
        except Exception as e:
            print(f"Error analyzing branches: {e}")
        
        # Generate recommendations
        if len(branch_analysis['stale_branches']) > 0:
            branch_analysis['recommendations'].append({
                'type': 'stale_branches',
                'description': f'Found {len(branch_analysis["stale_branches"])} stale branches (>90 days old)',
                'priority': 'medium',
                'action': 'Consider removing stale branches after verification'
            })
        
        if len(branch_analysis['merged_branches']) > 5:
            branch_analysis['recommendations'].append({
                'type': 'merged_branches',
                'description': f'Found {len(branch_analysis["merged_branches"])} merged branches',
                'priority': 'low',
                'action': 'Consider cleaning up merged branches'
            })
        
        return branch_analysis
    
    def analyze_commit_history(self) -> Dict[str, Any]:
        """Analyze commit history for optimization opportunities"""
        print("📜 Analyzing commit history...")
        
        commit_analysis = {
            'total_commits': 0,
            'recent_commits': 0,
            'large_commits': [],
            'commit_frequency': {},
            'recommendations': []
        }
        
        try:
            # Get total commit count
            result = subprocess.run([
                'git', 'rev-list', '--count', 'HEAD'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                commit_analysis['total_commits'] = int(result.stdout.strip())
            
            # Get recent commits (last 30 days)
            result = subprocess.run([
                'git', 'rev-list', '--count', '--since=30.days.ago', 'HEAD'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                commit_analysis['recent_commits'] = int(result.stdout.strip())
            
            # Analyze commit sizes (simplified)
            result = subprocess.run([
                'git', 'log', '--oneline', '--stat', '-20'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Parse for large commits (simplified analysis)
                lines = result.stdout.strip().split('\n')
                large_commits = []
                
                for line in lines:
                    if 'insertions' in line and 'deletions' in line:
                        # Extract numbers for basic analysis
                        if '++' in line and len(line) > 50:
                            large_commits.append(line)
                
                commit_analysis['large_commits'] = large_commits[:10]
        
        except Exception as e:
            print(f"Error analyzing commit history: {e}")
        
        # Generate recommendations
        if commit_analysis['total_commits'] > 1000:
            commit_analysis['recommendations'].append({
                'type': 'history_size',
                'description': f'Large commit history ({commit_analysis["total_commits"]} commits)',
                'priority': 'low',
                'action': 'Consider shallow clones for CI/CD'
            })
        
        if commit_analysis['recent_commits'] == 0:
            commit_analysis['recommendations'].append({
                'type': 'activity',
                'description': 'No commits in the last 30 days',
                'priority': 'medium',
                'action': 'Repository may be stale'
            })
        
        return commit_analysis
    
    def analyze_duplicate_content(self) -> List[Dict[str, Any]]:
        """Analyze for potential duplicate files"""
        print("🔍 Analyzing for duplicate content...")
        
        duplicates = []
        file_hashes = {}
        
        try:
            # Simple duplicate detection based on file size and name patterns
            for file_path in self.repo_root.rglob('*'):
                if file_path.is_file() and '.git' not in str(file_path):
                    size = file_path.stat().st_size
                    name = file_path.name.lower()
                    
                    # Look for potential duplicates by size and similar names
                    key = f"{size}_{name}"
                    if key in file_hashes:
                        file_hashes[key].append(str(file_path.relative_to(self.repo_root)))
                    else:
                        file_hashes[key] = [str(file_path.relative_to(self.repo_root))]
            
            # Find actual duplicates
            for key, paths in file_hashes.items():
                if len(paths) > 1:
                    size = int(key.split('_')[0])
                    if size > 1024:  # Only consider files > 1KB
                        duplicates.append({
                            'size_bytes': size,
                            'files': paths,
                            'potential_savings_kb': (size * (len(paths) - 1)) / 1024
                        })
        
        except Exception as e:
            print(f"Error analyzing duplicates: {e}")
        
        return sorted(duplicates, key=lambda x: x['potential_savings_kb'], reverse=True)[:10]
    
    def generate_cleanup_recommendations(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate comprehensive cleanup recommendations"""
        recommendations = []
        
        # Large files recommendations
        if analysis_results.get('large_files'):
            large_count = len(analysis_results['large_files'])
            total_size = sum(f['size_mb'] for f in analysis_results['large_files'])
            
            recommendations.append({
                'category': 'Storage Optimization',
                'type': 'large_files',
                'description': f'Found {large_count} large files totaling {total_size:.1f}MB',
                'priority': 'medium' if total_size > 50 else 'low',
                'actions': [
                    'Consider using Git LFS for large files',
                    'Move large assets to external storage',
                    'Compress or optimize large files',
                    'Remove unnecessary large files'
                ]
            })
        
        # Branch cleanup recommendations
        if analysis_results.get('branches'):
            stale_count = len(analysis_results['branches'].get('stale_branches', []))
            merged_count = len(analysis_results['branches'].get('merged_branches', []))
            
            if stale_count > 0 or merged_count > 5:
                recommendations.append({
                    'category': 'Branch Management',
                    'type': 'branch_cleanup',
                    'description': f'Found {stale_count} stale and {merged_count} merged branches',
                    'priority': 'medium' if stale_count > 5 else 'low',
                    'actions': [
                        'Remove stale branches after verification',
                        'Clean up merged feature branches',
                        'Implement branch protection rules',
                        'Set up automated branch cleanup'
                    ]
                })
        
        # Duplicate content recommendations
        if analysis_results.get('duplicates'):
            dup_count = len(analysis_results['duplicates'])
            potential_savings = sum(d['potential_savings_kb'] for d in analysis_results['duplicates'])
            
            if dup_count > 0:
                recommendations.append({
                    'category': 'Content Deduplication',
                    'type': 'duplicates',
                    'description': f'Found {dup_count} potential duplicates, {potential_savings:.1f}KB savings possible',
                    'priority': 'low',
                    'actions': [
                        'Review and remove duplicate files',
                        'Implement pre-commit hooks to prevent duplicates',
                        'Use symlinks for shared content',
                        'Organize assets in shared directories'
                    ]
                })
        
        return recommendations
    
    def run_analysis(self) -> Dict[str, Any]:
        """Run complete git cleanup analysis"""
        print("🧹 Starting Git cleanup analysis...")
        
        # Run all analysis components
        large_files = self.analyze_large_files()
        branch_analysis = self.analyze_branches()
        commit_analysis = self.analyze_commit_history()
        duplicates = self.analyze_duplicate_content()
        
        # Combine results
        analysis_results = {
            'large_files': large_files,
            'branches': branch_analysis,
            'commits': commit_analysis,
            'duplicates': duplicates
        }
        
        # Generate recommendations
        recommendations = self.generate_cleanup_recommendations(analysis_results)
        
        # Create final report
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'repository_path': str(self.repo_root),
            'analysis': analysis_results,
            'recommendations': recommendations,
            'summary': {
                'large_files_count': len(large_files),
                'stale_branches_count': len(branch_analysis.get('stale_branches', [])),
                'total_commits': commit_analysis.get('total_commits', 0),
                'potential_duplicates': len(duplicates)
            }
        }
        
        print(f"✅ Git cleanup analysis complete!")
        return report

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Git Cleanup Optimizer')
    parser.add_argument('--analyze', action='store_true',
                       help='Run comprehensive cleanup analysis')
    parser.add_argument('--recommend', action='store_true',
                       help='Generate cleanup recommendations')
    
    args = parser.parse_args()
    
    optimizer = GitCleanupOptimizer()
    
    if args.analyze or args.recommend:
        report = optimizer.run_analysis()
        
        # Save report
        with open('git_cleanup_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n🧹 Git Cleanup Analysis Summary:")
        print("=" * 40)
        print(f"Large Files: {report['summary']['large_files_count']}")
        print(f"Stale Branches: {report['summary']['stale_branches_count']}")
        print(f"Total Commits: {report['summary']['total_commits']}")
        print(f"Potential Duplicates: {report['summary']['potential_duplicates']}")
        
        if report['recommendations']:
            print(f"\n💡 Cleanup Recommendations ({len(report['recommendations'])}):")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"{i}. {rec['category']}: {rec['description']}")
        
        print(f"\n📁 Full report saved to: git_cleanup_report.json")
    
    else:
        print("Use --analyze or --recommend to run cleanup analysis")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())