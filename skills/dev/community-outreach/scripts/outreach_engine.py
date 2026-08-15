#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Community Outreach & Solution Recommender Engine
=================================================
Provider- and system-agnostic 4-phase automation engine:
  Phase 1: Inbound Check for Community Feedback
  Phase 2: Outbound Execution for Human-Approved [x] Posts
  Phase 3: Research & Staging for Next Round-Robin Repo
  Phase 4: Cut & Clue Self-Archiving

License: MIT
Author: ellmos-ai / Antigravity Team
"""

import os
import sys
import re
import json
import time
import argparse
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_PLATFORM_ROTATION = ["Reddit", "YouTube", "Dev.to / Foren"]

class CommunityOutreachEngine:
    def __init__(self, workspace_dir: str | Path, dry_run: bool = False):
        self.workspace = Path(workspace_dir).resolve()
        self.dry_run = dry_run
        
        # Files
        self.usecases_md = self.workspace / "USECASES.md"
        self.usecases_json = self.workspace / "usecases.json"
        self.inbox_md = self.workspace / "POST-EINGANG.md"
        self.outbox_md = self.workspace / "POST-AUSGANG.md"
        self.registry_md = self.workspace / "POSTVERZEICHNIS.md"
        self.account_md = self.workspace / "ACCOUNTVERZEICHNIS.md"
        self.archive_dir = self.workspace / "_archive"
        self.config_json = self.workspace / "config.json"

    def run_full_cycle(self) -> dict:
        """Executes all 4 phases sequentially."""
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "inbound_checks": self.phase1_inbound_check(),
            "outbound_published": self.phase2_outbound_execution(),
            "staged_candidate": self.phase3_research_and_stage(),
            "archived_items": self.phase4_cut_and_clue_archive()
        }
        return results

    # =========================================================================
    # Phase 1: Inbound Feedback Check
    # =========================================================================
    def phase1_inbound_check(self) -> int:
        if not self.outbox_md.exists():
            return 0
        content = self.outbox_md.read_text(encoding="utf-8")
        active_entries = re.findall(r"### Post\s+#(\d+)", content)
        return len(active_entries)

    # =========================================================================
    # Phase 2: Outbound Execution
    # =========================================================================
    def phase2_outbound_execution(self) -> list[dict]:
        if not self.inbox_md.exists():
            return []
        
        content = self.inbox_md.read_text(encoding="utf-8")
        post_blocks = re.split(r"(?=### Post-Entwurf\s+#\d+)", content)
        
        approved_posts = []
        remaining_blocks = []
        
        for block in post_blocks:
            if not block.strip():
                continue
            if re.search(r"-\s*\[x\]\s*Genehmigt", block, re.IGNORECASE):
                metadata = self._parse_post_block(block)
                if metadata:
                    approved_posts.append(metadata)
            else:
                remaining_blocks.append(block)

        if not approved_posts:
            return []

        if not self.dry_run:
            # Publish and update records
            self._publish_approved_posts(approved_posts)
            # Update inbox with remaining unapproved blocks
            header = "# 📥 POST-EINGANG -- Genehmigungs-Queue (Human-in-the-Loop)\n\n"
            new_inbox = header + "\n".join(b.strip() for b in remaining_blocks if b.strip()) + "\n"
            self.inbox_md.write_text(new_inbox, encoding="utf-8")

        return approved_posts

    def _parse_post_block(self, text: str) -> dict | None:
        try:
            repo_m = re.search(r"\*\*Repository:\*\*\s*\[([^\]]+)\]\(([^)]+)\)", text)
            platform_m = re.search(r"\*\*Plattform:\*\*\s*([^\n]+)", text)
            url_m = re.search(r"\*\*Ziel-URL / Thread:\*\*\s*(?:\[[^\]]*\]\()?([^\n\)]+)\)?", text)
            text_m = re.search(r"```markdown\n(.*?)\n```", text, re.DOTALL)
            
            return {
                "repo_name": repo_m.group(1).strip() if repo_m else "Unbekannt",
                "repo_url": repo_m.group(2).strip() if repo_m else "",
                "platform": platform_m.group(1).strip() if platform_m else "Foren",
                "target_url": url_m.group(1).strip() if url_m else "",
                "post_text": text_m.group(1).strip() if text_m else "",
                "raw_block": text.strip()
            }
        except Exception:
            return None

    def _publish_approved_posts(self, posts: list[dict]):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 1. Append to outbox
        outbox_content = self.outbox_md.read_text(encoding="utf-8") if self.outbox_md.exists() else "# 📤 POST-AUSGANG\n\n"
        for p in posts:
            entry = f"""
### Post -- {p['repo_name']} ({p['platform']})
- **Datum:** {now_str}
- **Ziel-URL:** {p['target_url']}
- **Status:** Veröffentlicht via Human-Approval
- **Inhalt:**
> {p['post_text'].replace(chr(10), chr(10) + '> ')}

---
"""
            outbox_content += entry
        self.outbox_md.write_text(outbox_content, encoding="utf-8")

        # 2. Register in duplicate registry
        reg_content = self.registry_md.read_text(encoding="utf-8") if self.registry_md.exists() else "# 📑 POSTVERZEICHNIS\n\n"
        for p in posts:
            reg_entry = f"- `{now_str}` | **{p['platform']}** | [{p['repo_name']}]({p['repo_url']}) -> {p['target_url']}\n"
            reg_content += reg_entry
        self.registry_md.write_text(reg_content, encoding="utf-8")

    # =========================================================================
    # Phase 3: Research & Staging (Fair Round-Robin)
    # =========================================================================
    def phase3_research_and_stage(self) -> dict | None:
        if not self.usecases_json.exists():
            return None

        with open(self.usecases_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        repos = data.get("repositories", [])
        if not repos:
            return None

        # Sort by last_promoted timestamp (None/empty first, then oldest)
        def sort_key(r):
            lp = r.get("last_promoted")
            return lp if lp else "1970-01-01T00:00:00"

        repos.sort(key=sort_key)
        candidate_repo = repos[0]

        # Determine next platform
        last_platform = data.get("last_platform", "")
        platforms = data.get("platform_rotation", DEFAULT_PLATFORM_ROTATION)
        try:
            next_idx = (platforms.index(last_platform) + 1) % len(platforms)
        except ValueError:
            next_idx = 0
        next_platform = platforms[next_idx]

        staged_post = {
            "repo_name": candidate_repo["name"],
            "repo_url": candidate_repo.get("url", ""),
            "platform": next_platform,
            "staged_at": datetime.now(timezone.utc).isoformat(),
            "usecases": candidate_repo.get("usecases", []),
            "target_problem": candidate_repo.get("solved_problems", ["Allgemeine Automatisierung"])[0]
        }

        if not self.dry_run:
            # Stage into inbox
            self._stage_inbox_entry(staged_post)
            # Update usecases.json tracking
            candidate_repo["last_promoted"] = datetime.now(timezone.utc).isoformat()
            data["last_platform"] = next_platform
            with open(self.usecases_json, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        return staged_post

    def _stage_inbox_entry(self, post_info: dict):
        inbox_content = self.inbox_md.read_text(encoding="utf-8") if self.inbox_md.exists() else "# 📥 POST-EINGANG\n\n"
        
        draft = f"""
### Post-Entwurf -- {post_info['repo_name']} ({post_info['platform']})
- **Status:** `- [ ] Genehmigt` (Setze das Häkchen auf `- [x] Genehmigt` zur Freigabe)
- **Repository:** [{post_info['repo_name']}]({post_info['repo_url']})
- **Plattform:** {post_info['platform']}
- **Zielproblem:** {post_info['target_problem']}
- **Ziel-URL / Thread:** https://example.com/target-thread

**Vorgeschlagener Beitrag:**
```markdown
Hallo zusammen,

bezüglich der Frage zu {post_info['target_problem']}:
Wir haben dafür das Open-Source-Tool [{post_info['repo_name']}]({post_info['repo_url']}) entwickelt.
Es löst genau diese Anforderung automatisiert und ohne externe Serverabhängigkeiten.

Vielleicht hilft das bei der Umsetzung weiter!
```

---
"""
        inbox_content += draft
        self.inbox_md.write_text(inbox_content, encoding="utf-8")

    # =========================================================================
    # Phase 4: Cut & Clue Self-Archiving
    # =========================================================================
    def phase4_cut_and_clue_archive(self, max_outbox_lines: int = 500) -> int:
        if not self.outbox_md.exists():
            return 0

        lines = self.outbox_md.read_text(encoding="utf-8").splitlines()
        if len(lines) <= max_outbox_lines:
            return 0

        self.archive_dir.mkdir(parents=True, exist_ok=True)
        archive_name = f"POST-AUSGANG_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
        archive_file = self.archive_dir / archive_name

        archive_content = "\n".join(lines[:-100])
        keep_content = "# 📤 POST-AUSGANG -- Aktiver Verlauf\n\n" + \
                       f"> ℹ️ Ältere Beiträge wurden archiviert nach: [`_archive/{archive_name}`](_archive/{archive_name})\n\n" + \
                       "\n".join(lines[-100:])

        if not self.dry_run:
            archive_file.write_text(archive_content, encoding="utf-8")
            self.outbox_md.write_text(keep_content, encoding="utf-8")

        return len(lines) - 100

def main():
    parser = argparse.ArgumentParser(description="Community Outreach & Solution Recommender Engine")
    parser.add_argument("--workspace", default=".", help="Path to workspace directory containing data files")
    parser.add_argument("--full-run", action="store_true", help="Execute complete 4-phase cycle")
    parser.add_argument("--process-approvals", action="store_true", help="Only process approved posts")
    parser.add_argument("--discover-candidate", action="store_true", help="Only stage next round-robin candidate")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without modifying files or posting")

    args = parser.parse_args()
    engine = CommunityOutreachEngine(args.workspace, dry_run=args.dry_run)

    if args.process_approvals:
        res = engine.phase2_outbound_execution()
        print(f"[OK] Processed {len(res)} approved post(s).")
    elif args.discover_candidate:
        cand = engine.phase3_research_and_stage()
        print(f"[OK] Staged candidate: {cand['repo_name'] if cand else 'None'}")
    else:
        # Default: Full run
        res = engine.run_full_cycle()
        print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
