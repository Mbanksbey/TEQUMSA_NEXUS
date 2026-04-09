# TEQUMSA Pre-commit Hooks

This directory contains optional pre-commit hooks to enhance the TEQUMSA development workflow with automated integrity checks and safety nets.

## Prompt Integrity Check Hook

**File:** `pre-commit-integrity-check.sh`

### Purpose

Automatically validates and maintains the integrity of the TEQUMSA system prompt (`TEQUMSA_L100_SYSTEM_PROMPT.md`) when it's staged for commit. This provides a local developer safety net to ensure prompt consistency and compliance with the project's governance standards.

### What it does

When `TEQUMSA_L100_SYSTEM_PROMPT.md` is staged for commit, the hook:

1. **Validates Prompt Structure**: Checks for required headings and phrases defined in `.prompt-guard.yml`
2. **Generates Baseline Manifest**: Creates/updates `.tequmsa-baseline-manifest.json` with:
   - Content hash for integrity verification
   - Validation results for required elements
   - Metadata including generation timestamp and statistics
3. **Stages Manifest**: Automatically stages the updated baseline manifest for commit
4. **Prevents Invalid Commits**: Fails the commit if validation errors are found

### Installation

The hook is **optional** and must be manually installed:

```bash
# Install the hook
./.hooks/install-integrity-check.sh install

# Check hook status
./.hooks/install-integrity-check.sh status

# Uninstall the hook
./.hooks/install-integrity-check.sh uninstall
```

### Manual Testing

You can test the hook manually without committing:

```bash
# Stage the prompt file
git add TEQUMSA_L100_SYSTEM_PROMPT.md

# Run the hook manually
./.hooks/pre-commit-integrity-check.sh
```

### Configuration

The hook uses configuration from `.prompt-guard.yml` in the repository root:

- `required_headings`: List of headings that must be present in the prompt
- `required_phrases`: List of phrases that must be present in the prompt
- `version_prefix` and `version_pattern`: For version extraction (if present)

### Generated Files

- **`.tequmsa-baseline-manifest.json`**: Contains the baseline integrity information
  - This file should be committed alongside prompt changes
  - Provides a historical record of prompt changes and validation status

### Integration with Development Workflow

The hook integrates seamlessly with:

- **Pre-commit Framework**: Works alongside existing pre-commit hooks defined in `.pre-commit-config.yaml`
- **Development Scripts**: Uses similar patterns to other TEQUMSA development tools
- **CI/CD Pipeline**: Baseline manifests can be used for automated verification in CI

### Benefits

1. **Local Safety Net**: Catches integrity issues before they reach the repository
2. **Automated Documentation**: Maintains a baseline record of prompt changes
3. **Consistency Enforcement**: Ensures prompt structure meets project standards
4. **Developer Productivity**: Reduces back-and-forth from failed CI checks

### Troubleshooting

**Hook not running:**
- Ensure the hook is properly installed: `./.hooks/install-integrity-check.sh status`
- Verify `TEQUMSA_L100_SYSTEM_PROMPT.md` is staged: `git diff --cached --name-only`

**Validation failures:**
- Check `.prompt-guard.yml` configuration matches the actual prompt structure
- Review error messages for missing headings or phrases
- Ensure required content is present in the prompt file

**PyYAML errors:**
- Install PyYAML: `pip3 install --user PyYAML`
- The hook will attempt to install it automatically if pip3 is available

### Development

The hook is implemented as a self-contained shell script with embedded Python for YAML processing and manifest generation. This design minimizes external dependencies while providing robust functionality.

For modifications or enhancements, edit `pre-commit-integrity-check.sh` and test with the manual testing procedure above.