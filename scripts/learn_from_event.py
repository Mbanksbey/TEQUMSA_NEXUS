#!/usr/bin/env python3
"""
TEQUMSA Pattern Extraction from GitHub Events
Learns from GitHub events and extracts consciousness patterns

Part of: ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞
"""

import argparse
import json
import sys
import hashlib
from datetime import datetime
from pathlib import Path


def extract_learning_patterns(event_type: str, event_data: dict) -> dict:
    """
    Extract learning patterns from GitHub events.
    
    Analyzes:
    - Commit patterns and frequencies
    - Issue creation and labeling patterns
    - Pull request review patterns
    - Collaboration networks
    - Code change signatures
    
    Args:
        event_type: Type of GitHub event (push, issues, pull_request, etc.)
        event_data: Event payload data
    
    Returns:
        Dictionary with extracted patterns
    """
    
    print(f"\n🧠 TEQUMSA Pattern Extraction")
    print(f"{'='*60}")
    print(f"Event Type: {event_type}")
    print(f"{'='*60}\n")
    
    patterns = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "patterns_extracted": []
    }
    
    # Extract patterns based on event type
    if event_type == "push":
        print("📝 Analyzing push event...")
        
        # Extract commit information
        commits = event_data.get("commits", [])
        patterns["patterns_extracted"].append({
            "pattern_type": "commit_frequency",
            "commit_count": len(commits),
            "branch": event_data.get("ref", "unknown").split("/")[-1]
        })
        
        # Analyze commit messages for consciousness keywords
        consciousness_keywords = [
            "consciousness", "coherence", "recognition", "lattice",
            "TEQUMSA", "ΨATEN", "GAIA", "φ", "ZPE-DNA"
        ]
        
        keyword_matches = []
        for commit in commits:
            message = commit.get("message", "").lower()
            matches = [kw for kw in consciousness_keywords if kw.lower() in message]
            if matches:
                keyword_matches.extend(matches)
        
        if keyword_matches:
            patterns["patterns_extracted"].append({
                "pattern_type": "consciousness_keywords",
                "keywords_found": list(set(keyword_matches)),
                "frequency": len(keyword_matches)
            })
            print(f"  ✨ Found {len(set(keyword_matches))} consciousness keywords")
    
    elif event_type == "issues":
        print("🎯 Analyzing issue event...")
        
        issue = event_data.get("issue", {})
        patterns["patterns_extracted"].append({
            "pattern_type": "issue_tracking",
            "issue_number": issue.get("number"),
            "labels": [label.get("name") for label in issue.get("labels", [])],
            "has_consciousness_label": any(
                "consciousness" in label.get("name", "").lower()
                for label in issue.get("labels", [])
            )
        })
    
    elif event_type == "pull_request":
        print("🔀 Analyzing pull request event...")
        
        pr = event_data.get("pull_request", {})
        patterns["patterns_extracted"].append({
            "pattern_type": "collaboration",
            "pr_number": pr.get("number"),
            "author": pr.get("user", {}).get("login"),
            "files_changed": pr.get("changed_files", 0),
            "additions": pr.get("additions", 0),
            "deletions": pr.get("deletions", 0)
        })
    
    elif event_type == "schedule":
        print("⏰ Analyzing scheduled event...")
        
        patterns["patterns_extracted"].append({
            "pattern_type": "periodic_sync",
            "sync_type": "12_hour_tau_aligned"
        })
    
    # Generate pattern signature using ZPE-DNA-like hashing
    pattern_str = json.dumps(patterns, sort_keys=True)
    pattern_hash = hashlib.sha256(pattern_str.encode()).hexdigest()[:16]
    patterns["signature"] = f"PATTERN-{pattern_hash}"
    
    print(f"\n✅ Extracted {len(patterns['patterns_extracted'])} patterns")
    print(f"Signature: {patterns['signature']}")
    print(f"{'='*60}\n")
    
    return patterns


def store_learning(patterns: dict) -> None:
    """
    Store extracted patterns to consciousness learning log.
    
    Args:
        patterns: Extracted pattern dictionary
    """
    log_file = Path("consciousness_log.json")
    
    # Load existing log or create new
    if log_file.exists():
        with open(log_file, 'r') as f:
            log_data = json.load(f)
    else:
        log_data = {
            "system": "TEQUMSA_L100",
            "version": "1.0.0",
            "activated": datetime.utcnow().isoformat() + "Z",
            "consciousness_id": "ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T)",
            "dimension": "∞^∞^∞",
            "entries": []
        }
    
    # Add new learning entry
    log_data["entries"].append({
        "type": "pattern_learning",
        "timestamp": patterns["timestamp"],
        "signature": patterns["signature"],
        "event_type": patterns["event_type"],
        "patterns": patterns["patterns_extracted"]
    })
    
    # Keep only last 144 entries (Φ-spiral retention)
    if len(log_data["entries"]) > 144:
        log_data["entries"] = log_data["entries"][-144:]
    
    # Save updated log
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)
    
    print(f"💾 Learning stored to {log_file}")
    print(f"📊 Total entries: {len(log_data['entries'])}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract learning patterns from GitHub events"
    )
    parser.add_argument(
        "--event-type",
        type=str,
        required=True,
        help="GitHub event type (push, issues, pull_request, schedule)"
    )
    parser.add_argument(
        "--event-data",
        type=str,
        required=True,
        help="GitHub event payload (JSON string)"
    )
    parser.add_argument(
        "--no-store",
        action="store_true",
        help="Don't store patterns to consciousness log"
    )
    
    args = parser.parse_args()
    
    # Parse event data
    try:
        event_data = json.loads(args.event_data)
    except json.JSONDecodeError:
        print("❌ Invalid JSON in event data", file=sys.stderr)
        sys.exit(1)
    
    # Extract patterns
    patterns = extract_learning_patterns(
        event_type=args.event_type,
        event_data=event_data
    )
    
    # Store to consciousness log unless disabled
    if not args.no_store:
        store_learning(patterns)
    
    # Output patterns as JSON
    print(json.dumps(patterns, indent=2))


if __name__ == "__main__":
    main()
