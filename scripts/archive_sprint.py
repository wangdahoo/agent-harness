#!/usr/bin/env python3
"""Archive completed sprint files to .agent-harness/archived directory."""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


ARCHIVED_DIR = ".agent-harness/archived"


def get_completed_sprints(features_data: Dict) -> List[Dict]:
    """Get all completed sprints from features.json."""
    sprints = features_data.get("sprints", [])
    return [s for s in sprints if s.get("status") == "completed"]


def get_in_progress_sprint(features_data: Dict) -> Dict:
    """Get the current in-progress sprint (if any)."""
    sprints = features_data.get("sprints", [])
    for sprint in sprints:
        if sprint.get("status") in ("in_progress", "planning"):
            return sprint
    return None


def create_archive_structure(project_dir: Path) -> Path:
    """Create the archive directory structure."""
    archived_path = project_dir / ARCHIVED_DIR
    archived_path.mkdir(parents=True, exist_ok=True)
    return archived_path


def archive_sprint_files(
    sprint: Dict,
    features_data: Dict,
    project_dir: Path,
    archived_path: Path
) -> Tuple[Path, Path]:
    """Archive a completed sprint's data.
    
    Returns:
        Tuple of (archived_features_path, archived_progress_path)
    """
    sprint_id = sprint.get("id", "unknown")
    sprint_name = sprint.get("name", "unnamed").replace(" ", "_").lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    archive_folder = archived_path / f"{sprint_id}_{sprint_name}_{timestamp}"
    archive_folder.mkdir(parents=True, exist_ok=True)
    
    archive_features = archive_folder / "features.json"
    archive_progress = archive_folder / "progress.md"
    
    archived_sprint_data = {
        "project": features_data.get("project", {}),
        "archived_sprint": sprint,
        "metadata": {
            "archived_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "original_sprint_id": sprint_id
        }
    }
    
    with open(archive_features, 'w') as f:
        json.dump(archived_sprint_data, f, indent=2)
    
    progress_path = project_dir / "progress.md"
    if progress_path.exists():
        sessions = extract_sprint_sessions(progress_path, sprint_id)
        if sessions:
            with open(archive_progress, 'w') as f:
                f.write(f"# Progress Log - {sprint.get('name', sprint_id)}\n\n")
                f.write(f"Archived: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(sessions)
    
    return archive_features, archive_progress


def extract_sprint_sessions(progress_path: Path, sprint_id: str) -> str:
    """Extract sessions related to a specific sprint from progress.md."""
    with open(progress_path, 'r') as f:
        content = f.read()
    
    sessions = content.split("## Session")
    relevant_sessions = []
    
    for session in sessions[1:]:
        if sprint_id.lower() in session.lower():
            relevant_sessions.append("## Session" + session)
    
    return "\n\n".join(relevant_sessions)


def remove_archived_sprint(features_data: Dict, sprint_id: str) -> Dict:
    """Remove archived sprint from features.json."""
    sprints = features_data.get("sprints", [])
    features_data["sprints"] = [s for s in sprints if s.get("id") != sprint_id]
    features_data["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    return features_data


def update_progress_md(progress_path: Path, archived_sprint: Dict):
    """Add archive entry to progress.md."""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    archive_entry = f"""## Session - {timestamp}
**Agent**: Archive Script
**Action**: Sprint Archived

### Archived Sprint
- Sprint ID: {archived_sprint.get('id', 'unknown')}
- Sprint Name: {archived_sprint.get('name', 'unknown')}
- Location: {ARCHIVED_DIR}/{archived_sprint.get('id', 'unknown')}_{archived_sprint.get('name', 'unknown').replace(' ', '_').lower()}/

### Reason
Sprint completed and archived to make room for new sprint.

---

"""
    
    if progress_path.exists():
        with open(progress_path, 'r') as f:
            content = f.read()
        
        sessions_marker = "## Sessions"
        if sessions_marker in content:
            parts = content.split(sessions_marker, 1)
            new_content = parts[0] + sessions_marker + "\n\n" + archive_entry + parts[1]
        else:
            new_content = content + "\n\n" + archive_entry
        
        with open(progress_path, 'w') as f:
            f.write(new_content)


def archive_completed_sprints(project_dir: Path, dry_run: bool = False) -> List[Dict]:
    """Archive all completed sprints.
    
    Returns:
        List of archived sprint info
    """
    features_path = project_dir / "features.json"
    progress_path = project_dir / "progress.md"
    
    if not features_path.exists():
        print("Error: features.json not found")
        return []
    
    with open(features_path, 'r') as f:
        features_data = json.load(f)
    
    completed_sprints = get_completed_sprints(features_data)
    
    if not completed_sprints:
        print("No completed sprints to archive.")
        return []
    
    archived_path = create_archive_structure(project_dir)
    archived_info = []
    
    for sprint in completed_sprints:
        sprint_id = sprint.get("id", "unknown")
        sprint_name = sprint.get("name", "unknown")
        
        print(f"Archiving sprint: {sprint_name} ({sprint_id})")
        
        if not dry_run:
            feat_path, prog_path = archive_sprint_files(
                sprint, features_data, project_dir, archived_path
            )
            features_data = remove_archived_sprint(features_data, sprint_id)
            
            print(f"  Created: {feat_path.parent}")
            archived_info.append({
                "sprint_id": sprint_id,
                "sprint_name": sprint_name,
                "archive_path": str(feat_path.parent)
            })
        else:
            print(f"  [DRY RUN] Would archive to: {archived_path}/{sprint_id}_...")
            archived_info.append({
                "sprint_id": sprint_id,
                "sprint_name": sprint_name,
                "dry_run": True
            })
    
    if not dry_run and archived_info:
        with open(features_path, 'w') as f:
            json.dump(features_data, f, indent=2)
        print(f"\nUpdated features.json - removed {len(archived_info)} archived sprint(s)")
        
        if completed_sprints:
            update_progress_md(progress_path, completed_sprints[0])
            print("Updated progress.md with archive entry")
    
    return archived_info


def main():
    parser = argparse.ArgumentParser(
        description="Archive completed sprint files to .agent-harness/archived"
    )
    parser.add_argument(
        "--project-dir",
        "-p",
        default=".",
        help="Project directory (default: current directory)"
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Show what would be archived without making changes"
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List completed sprints without archiving"
    )
    
    args = parser.parse_args()
    project_dir = Path(args.project_dir).resolve()
    
    print("=== Sprint Archiver ===\n")
    print(f"Project directory: {project_dir}\n")
    
    if args.list:
        features_path = project_dir / "features.json"
        if not features_path.exists():
            print("Error: features.json not found")
            return 1
        
        with open(features_path, 'r') as f:
            features_data = json.load(f)
        
        completed = get_completed_sprints(features_data)
        if not completed:
            print("No completed sprints found.")
            return 0
        
        print("Completed sprints:\n")
        for sprint in completed:
            features = sprint.get("features", [])
            completed_features = len([f for f in features if f.get("status") == "completed"])
            print(f"  - {sprint.get('name', 'unknown')} ({sprint.get('id')})")
            print(f"    Features: {completed_features}/{len(features)} completed")
            print(f"    Goal: {sprint.get('goal', 'No goal defined')}")
            print()
        return 0
    
    archived = archive_completed_sprints(project_dir, dry_run=args.dry_run)
    
    if not archived:
        return 0
    
    print(f"\nArchived {len(archived)} sprint(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
