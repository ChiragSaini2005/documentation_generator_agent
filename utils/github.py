"""
utils/github.py
Fetch file tree and selected file contents from a public GitHub repo
using the GitHub REST API (no cloning needed).
"""
import os
import re
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

# Extensions worth reading for documentation purposes
READABLE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".java", ".go", ".rs", ".rb", ".php",
    ".cpp", ".c", ".h", ".cs", ".swift",
    ".md", ".mdx", ".rst", ".txt",
    ".yaml", ".yml", ".toml", ".json",
    ".sh", ".bash", ".zsh",
    ".dockerfile", ".env.example",
}

# Files/dirs to always skip
SKIP_PATTERNS = {
    "node_modules", ".git", "__pycache__", ".pytest_cache",
    "dist", "build", ".next", "venv", ".venv", "env",
    "*.min.js", "*.min.css", "*.lock", "package-lock.json",
    "yarn.lock", "poetry.lock", ".DS_Store",
}

MAX_FILES  = int(os.getenv("MAX_FILES_TO_READ", 20))
MAX_CHARS  = int(os.getenv("MAX_FILE_CHARS",    8000))


def _parse_owner_repo(url: str) -> tuple[str, str]:
    """Extract owner and repo name from a GitHub URL."""
    url = url.rstrip("/")
    match = re.search(r"github\.com[/:]([^/]+)/([^/\s]+?)(?:\.git)?$", url)
    if not match:
        raise ValueError(f"Cannot parse GitHub URL: {url}")
    return match.group(1), match.group(2)


def _github_headers() -> dict:
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _get_tree(owner: str, repo: str) -> list[dict]:
    """Return the full recursive file tree via the Git Trees API."""
    # First get the default branch
    repo_url = f"https://api.github.com/repos/{owner}/{repo}"
    r = requests.get(repo_url, headers=_github_headers(), timeout=15)
    r.raise_for_status()
    default_branch = r.json().get("default_branch", "main")

    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
    r = requests.get(tree_url, headers=_github_headers(), timeout=20)
    r.raise_for_status()
    return r.json().get("tree", [])


def _should_skip(path: str) -> bool:
    parts = path.replace("\\", "/").split("/")
    for part in parts:
        if part in SKIP_PATTERNS:
            return True
    return False


def _get_file_content(owner: str, repo: str, path: str) -> str:
    """Fetch a single file's content via the Contents API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    r = requests.get(url, headers=_github_headers(), timeout=15)
    if r.status_code != 200:
        return ""
    data = r.json()
    if data.get("encoding") == "base64":
        try:
            content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
            return content[:MAX_CHARS]
        except Exception:
            return ""
    return ""


def fetch_repository(repo_url: str) -> tuple[list[str], dict[str, str]]:
    """
    Main entry point.  Returns:
      file_tree      – list of all file paths
      file_contents  – dict of path → content for the most relevant files
    """
    owner, repo = _parse_owner_repo(repo_url)
    tree_items  = _get_tree(owner, repo)

    file_paths = [
        item["path"]
        for item in tree_items
        if item["type"] == "blob" and not _should_skip(item["path"])
    ]

    # Priority scoring: README and root-level config files first,
    # then source files, then everything else
    def priority(path: str) -> int:
        name = path.split("/")[-1].lower()
        ext  = "." + name.rsplit(".", 1)[-1] if "." in name else ""
        if name.startswith("readme"):                     return 0
        if path.count("/") == 0 and ext in READABLE_EXTENSIONS: return 1
        if ext in {".py", ".js", ".ts", ".go", ".rs"}:   return 2
        if ext in READABLE_EXTENSIONS:                    return 3
        return 99

    readable = sorted(
        [p for p in file_paths if "." + p.rsplit(".", 1)[-1] in READABLE_EXTENSIONS
         or p.split("/")[-1].lower().startswith("readme")],
        key=priority,
    )[:MAX_FILES]

    file_contents: dict[str, str] = {}
    for path in readable:
        content = _get_file_content(owner, repo, path)
        if content.strip():
            file_contents[path] = content

    return file_paths, file_contents