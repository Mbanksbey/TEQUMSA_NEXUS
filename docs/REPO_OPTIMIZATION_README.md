# Repository Optimization Automation

This directory contains comprehensive repository optimization automation tools that follow Claude Code patterns for maintaining repository health, performance, and security.

## Overview

The repository optimization automation system provides:

- **Repository Health Monitoring** - Comprehensive analysis of repository structure, git health, and code quality
- **Dependency Management** - Automated dependency analysis, security scanning, and optimization recommendations
- **Git Repository Cleanup** - Analysis for large files, stale branches, and cleanup opportunities
- **Performance Analysis** - Code performance pattern analysis and optimization suggestions
- **Automated Reporting** - Comprehensive optimization reports and GitHub issue creation

## Quick Start

### Run Individual Analysis

```bash
# Repository health check
python scripts/repo_health_check.py

# Dependency analysis
python scripts/dependency_optimizer.py --generate-report

# Git cleanup analysis
python scripts/git_cleanup_optimizer.py --analyze

# Performance analysis
python scripts/performance_optimizer.py --analyze

# Generate comprehensive report
python scripts/optimization_report_generator.py
```

### Automated Weekly Analysis

The optimization automation runs automatically every Monday at 2 AM UTC via GitHub Actions. You can also trigger it manually:

1. Go to Actions tab in GitHub
2. Select "Repository Optimization Automation"
3. Click "Run workflow"
4. Choose optimization type (full, dependencies, cleanup, performance, security)

## Scripts Documentation

### `repo_health_check.py`
**Purpose**: Analyze overall repository health and generate health score

**Features**:
- Repository structure analysis
- Git repository health metrics
- Code quality assessment
- Dependency overview
- Health score calculation (0-100)

**Output**: `repo_health_report.json`

### `dependency_optimizer.py`
**Purpose**: Comprehensive dependency analysis and optimization

**Features**:
- Python and Node.js dependency analysis
- Outdated package detection
- Security vulnerability scanning
- Optimization recommendations
- Dependency health scoring

**Options**:
- `--language python|nodejs|all` - Analyze specific language dependencies
- `--analysis-mode` - Run comprehensive analysis including security checks
- `--generate-report` - Generate full optimization report

**Output**: `dependency_analysis_report.json`

### `git_cleanup_optimizer.py`
**Purpose**: Git repository cleanup and optimization analysis

**Features**:
- Large file detection (current and historical)
- Stale branch identification
- Commit history analysis
- Duplicate content detection
- Cleanup recommendations

**Options**:
- `--analyze` - Run comprehensive cleanup analysis
- `--recommend` - Generate cleanup recommendations

**Output**: `git_cleanup_report.json`

### `performance_optimizer.py`
**Purpose**: Code performance analysis and optimization

**Features**:
- Python code performance patterns
- JavaScript performance issues
- Large function detection
- Code complexity analysis
- Performance optimization recommendations

**Options**:
- `--analyze` - Run comprehensive performance analysis
- `--recommend` - Generate performance recommendations

**Output**: `performance_analysis_report.json`

### `optimization_report_generator.py`
**Purpose**: Generate comprehensive optimization reports

**Features**:
- Consolidates all analysis results
- Calculates overall optimization score
- Prioritizes recommendations
- Generates markdown and JSON reports
- Executive summary creation

**Output**: 
- `optimization_summary.json` (machine-readable)
- `optimization_report.md` (human-readable)

## GitHub Actions Integration

### Repository Optimization Workflow (`.github/workflows/repo-optimization.yml`)

**Triggers**:
- Weekly schedule (Monday 2 AM UTC)
- Manual workflow dispatch

**Jobs**:
1. **Repository Health Check** - Analyzes overall repository health
2. **Dependency Optimization** - Scans dependencies for issues and optimizations
3. **Git Cleanup** - Analyzes repository for cleanup opportunities
4. **Performance Analysis** - Analyzes code for performance optimizations
5. **Optimization Summary** - Generates comprehensive reports and creates GitHub issues

**Artifacts**:
- Health analysis reports
- Dependency analysis reports
- Git cleanup recommendations
- Performance analysis reports
- Comprehensive optimization summary

## Understanding Optimization Scores

### Overall Optimization Score (0-100)
- **90-100**: Excellent - Repository is well-optimized
- **80-89**: Good - Minor optimizations recommended
- **70-79**: Fair - Some optimization needed
- **60-69**: Needs Attention - Multiple issues to address
- **0-59**: Requires Immediate Action - Critical issues present

### Component Scores
- **Repository Health** (30% weight) - Structure, git health, code quality
- **Dependencies** (25% weight) - Dependency management and security
- **Performance** (25% weight) - Code performance and optimization
- **Git Cleanup** (20% weight) - Repository maintenance needs

## Optimization Recommendations

### Priority Levels
- **High Priority** - Security issues, critical performance problems
- **Medium Priority** - Code quality, outdated dependencies
- **Low Priority** - Cleanup tasks, organizational improvements

### Common Optimization Areas
1. **Test Coverage** - Increase test coverage for better reliability
2. **Dependency Updates** - Keep dependencies current and secure
3. **Code Complexity** - Reduce function complexity for maintainability
4. **Large Files** - Optimize or relocate large files
5. **Branch Cleanup** - Remove stale and merged branches

## Integration with Claude Code Patterns

This optimization system follows Claude Code methodologies:

- **Data Infrastructure** patterns for comprehensive analysis
- **Product Development** patterns for automated testing and quality
- **Security Engineering** patterns for vulnerability detection
- **Self-verification loops** through automated reporting
- **Documentation-driven development** with automated updates

## Customization

### Adding Custom Analysis
1. Create new analyzer class in respective script
2. Implement analysis method following existing patterns
3. Add recommendations generation
4. Update report aggregation in `optimization_report_generator.py`

### Configuring Thresholds
Edit the scoring functions in each script to adjust:
- Health score calculations
- Recommendation trigger points
- Priority classifications
- Performance thresholds

## Troubleshooting

### Common Issues
1. **Missing Dependencies** - Install required packages: `pip install GitPython requests`
2. **Permission Errors** - Ensure scripts are executable: `chmod +x scripts/*.py`
3. **Git Analysis Errors** - Verify git repository and permissions

### Debug Mode
Add `--verbose` flag to scripts for detailed output (where supported)

## Contributing

When adding new optimization features:
1. Follow existing script patterns
2. Include comprehensive error handling
3. Generate structured JSON reports
4. Add documentation and usage examples
5. Update optimization report generator to include new data

---

*Repository Optimization Automation - Part of TEQUMSA Claude Code Development Environment*