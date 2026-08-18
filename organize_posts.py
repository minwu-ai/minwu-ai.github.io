#!/usr/bin/env python3
"""
organize_posts.py — file posts into posts/published/ and posts/unpublished/
according to their `published:` frontmatter flag.

The FRONTMATTER IS THE SOURCE OF TRUTH, always. The folders are a convenience
view so you can see at a glance what has gone live; moving a file between them
does NOT publish or unpublish it. Flip `published:` in the file, then run this
to re-file it.

    python3 organize_posts.py            # show what would move
    python3 organize_posts.py --apply    # actually move (uses git mv when possible)

Filenames are unchanged, and a post's URL comes from its slug, not its folder,
so re-filing never changes a live URL.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
STATES = {True: "published", False: "unpublished"}


def is_published(path):
    """Read the `published:` flag. Absent means published, matching build_site."""
    text = path.read_text(errors="replace")[:4000]
    m = re.search(r"^published:\s*(\S+)", text, re.M)
    if not m:
        return True
    return m.group(1).strip().strip('"\'').lower() != "false"


def git_mv(src, dst):
    """Prefer git mv so history follows the file; fall back to a plain move."""
    try:
        subprocess.run(["git", "mv", str(src), str(dst)], cwd=ROOT,
                       check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        os.replace(src, dst)
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true",
                    help="perform the moves (default is a dry run)")
    args = ap.parse_args()

    moves, counts = [], {"published": 0, "unpublished": 0}
    for path in sorted(POSTS_DIR.rglob("*.md")):
        state = STATES[is_published(path)]
        counts[state] += 1
        target_dir = POSTS_DIR / state
        if path.parent != target_dir:
            moves.append((path, target_dir / path.name))

    print("{} published, {} unpublished".format(
        counts["published"], counts["unpublished"]))

    if not moves:
        print("Everything is already filed correctly.")
        return 0

    # Refuse to clobber: same filename already sitting in the destination.
    clashes = [(s, d) for s, d in moves if d.exists()]
    if clashes:
        print("\nERROR: a file with that name already exists in the destination:")
        for s, d in clashes:
            print("  {} -> {}".format(s.relative_to(ROOT), d.relative_to(ROOT)))
        print("Rename one of them, then re-run.")
        return 1

    print("\n{} file(s) to move:".format(len(moves)))
    for src, dst in moves:
        print("  {}  ->  posts/{}/".format(src.relative_to(POSTS_DIR), dst.parent.name))

    if not args.apply:
        print("\nDry run. Re-run with --apply to move them.")
        return 0

    for state in STATES.values():
        (POSTS_DIR / state).mkdir(parents=True, exist_ok=True)
    tracked = 0
    for src, dst in moves:
        if git_mv(src, dst):
            tracked += 1
    print("\nMoved {} file(s) ({} via git mv).".format(len(moves), tracked))
    return 0


if __name__ == "__main__":
    sys.exit(main())
