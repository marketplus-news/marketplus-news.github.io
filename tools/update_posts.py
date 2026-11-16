#!/usr/bin/env python3
"""X/Twitter post updates are disabled.

This script used to merge a JSON list of posts into data/posts.json and
rebuild data/news.json. The site no longer shows or fetches those posts.
"""
import sys

def main():
    print("update_posts.py: X/Twitter post updates are disabled; nothing written.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
