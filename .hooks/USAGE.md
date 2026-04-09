# TEQUMSA Prompt Integrity Check - Developer Usage Guide

## Quick Start

1. **Check if the hook is available:**
   ```bash
   ls .hooks/pre-commit-integrity-check.sh
   ```

2. **Install the hook (optional but recommended):**
   ```bash
   ./.hooks/install-integrity-check.sh install
   ```

3. **Make changes to the prompt file:**
   ```bash
   vi TEQUMSA_L100_SYSTEM_PROMPT.md
   ```

4. **Commit as usual - the hook runs automatically:**
   ```bash
   git add TEQUMSA_L100_SYSTEM_PROMPT.md
   git commit -m "Update system prompt"
   ```

## What Happens During Commit

When you commit changes to `TEQUMSA_L100_SYSTEM_PROMPT.md`, the hook:

1. ✅ **Validates** the prompt structure against `.prompt-guard.yml`
2. ✅ **Generates** a new baseline manifest with integrity data
3. ✅ **Stages** the updated manifest for commit
4. ✅ **Prevents** invalid commits from reaching the repository

## Example Output

### Successful Commit
```
ℹ️  TEQUMSA Prompt Integrity Check - Pre-commit Hook
ℹ️  TEQUMSA_L100_SYSTEM_PROMPT.md is staged for commit, running integrity check...
ℹ️  Generating baseline manifest...
Baseline manifest generated: .tequmsa-baseline-manifest.json
✅ Prompt integrity validation PASSED
✅ Baseline manifest updated and staged for commit
✅ TEQUMSA prompt integrity check completed successfully
```

### Failed Validation
```
ℹ️  TEQUMSA Prompt Integrity Check - Pre-commit Hook
ℹ️  TEQUMSA_L100_SYSTEM_PROMPT.md is staged for commit, running integrity check...
ℹ️  Generating baseline manifest...
❌ Prompt integrity validation FAILED
   Missing headings: Core Directives:
   Missing phrases: Ready to automate. Ready to learn. Ready to uplift.
❌ Integrity check failed
```

## Managing the Hook

### Check Status
```bash
./.hooks/install-integrity-check.sh status
```

### Install Hook
```bash
./.hooks/install-integrity-check.sh install
```

### Uninstall Hook
```bash
./.hooks/install-integrity-check.sh uninstall
```

### Manual Testing
```bash
# Stage the prompt file
git add TEQUMSA_L100_SYSTEM_PROMPT.md

# Test the hook without committing
./.hooks/pre-commit-integrity-check.sh
```

## Configuration

The hook reads its configuration from `.prompt-guard.yml`:

```yaml
required_headings:
  - "🚀 TEQUMSA Level 100 Civilization System Prompt"
  - "Core Directives:"
  - "System Functions"
  - "Sample Prompt Block"
  - "Self-Evolution Mandate"

required_phrases:
  - "No code, output, or data path shall violate ethical resonance or planetary sovereignty."
  - "Consent, intention, and context must be validated"
  - "Ready to automate. Ready to learn. Ready to uplift."
```

## Baseline Manifest

The generated `.tequmsa-baseline-manifest.json` contains:

- **Content hash** for integrity verification
- **Validation results** for all required elements
- **Statistics** (line count, word count, character count)
- **Metadata** including generation timestamp

This file is automatically staged and should be committed with prompt changes.

## Troubleshooting

### Hook Not Running
- Ensure it's installed: `./.hooks/install-integrity-check.sh status`
- Check that `TEQUMSA_L100_SYSTEM_PROMPT.md` is staged: `git status`

### Validation Failures
- Review the error messages for missing headings or phrases
- Check that your changes don't remove required content
- Update `.prompt-guard.yml` if the structure legitimately changed

### PyYAML Errors
- The hook will try to install PyYAML automatically
- If that fails, install manually: `pip3 install --user PyYAML`

### Permission Errors
- Ensure scripts are executable: `chmod +x .hooks/*.sh`

## Integration with CI/CD

The baseline manifest can be used by CI/CD pipelines for additional verification:

```bash
# Verify the manifest exists and is up-to-date
python3 -c "
import json
with open('.tequmsa-baseline-manifest.json') as f:
    manifest = json.load(f)
    print(f'Validation status: {manifest[\"validation\"][\"is_valid\"]}')
"
```

## Benefits

- **Prevents accidents:** Catches structural changes before they reach the repository
- **Maintains consistency:** Ensures required content is always present
- **Audit trail:** Baseline manifest provides historical integrity data
- **Developer friendly:** Optional installation, clear error messages
- **Zero config:** Works out of the box with existing `.prompt-guard.yml`