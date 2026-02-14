from flask import Flask, render_template, request, abort, jsonify
import os
import requests
from functools import lru_cache
import json
import base64
import re
from dotenv import load_dotenv
import markdown

load_dotenv()

# Configuration via .env (optional): GITHUB_TOKEN for higher rate limits
SITE_NAME = os.getenv("SITE_NAME", "Joan Fernando González García")
SITE_SUBTITLE = os.getenv("SITE_SUBTITLE", "Proyectos seleccionados")
# Optional: split the displayed title into an accent (blue) part and the remaining title.
# You can set these in your .env: SITE_ACCENT and SITE_TITLE. If not set, the code will
# attempt to split SITE_NAME into first word (accent) + rest.
SITE_ACCENT = os.getenv("SITE_ACCENT")
SITE_TITLE = os.getenv("SITE_TITLE")

app = Flask(__name__)


def github_headers():
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


@lru_cache(maxsize=128)
def fetch_repos_for_user(username: str):
    """Fetch public repos for a GitHub user (simplified list)."""
    url = f"https://api.github.com/users/{username}/repos"
    params = {"sort": "updated", "per_page": 100}
    resp = requests.get(url, params=params, headers=github_headers(), timeout=10)
    resp.raise_for_status()
    data = resp.json()
    repos = []
    for r in data:
        repos.append({
            "owner": r.get("owner", {}).get("login"),
            "name": r.get("name"),
            "html_url": r.get("html_url"),
            "description": r.get("description"),
            "language": r.get("language"),
            "updated_at": r.get("updated_at"),
            "stargazers_count": r.get("stargazers_count"),
            "forks_count": r.get("forks_count"),
        })
    return repos


def extract_image_from_readme(readme_content_b64: str, owner: str, repo: str):
    try:
        content = base64.b64decode(readme_content_b64).decode('utf-8', errors='ignore')
    except Exception:
        return None
    # markdown image
    md_img = re.search(r"!\[[^\]]*\]\(([^)]+)\)", content)
    if md_img:
        url = md_img.group(1).strip()
        if url.startswith('http'):
            return url
        for branch in ('main', 'master'):
            return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{url.lstrip('./')}"
    # html image
    html_img = re.search(r"<img[^>]+src=[\'\"]([^\'\"]+)[\'\"]", content)
    if html_img:
        url = html_img.group(1).strip()
        if url.startswith('http'):
            return url
    return None


@lru_cache(maxsize=256)
def fetch_repo(owner: str, repo: str):
    """Fetch metadata for a single repo and try to obtain a preview image."""
    base = f"https://api.github.com/repos/{owner}/{repo}"
    r = requests.get(base, headers=github_headers(), timeout=10)
    r.raise_for_status()
    data = r.json()
    preview = None
    try:
        rr = requests.get(base + "/readme", headers=github_headers(), timeout=10)
        if rr.status_code == 200:
            rd = rr.json()
            if rd.get('content'):
                preview = extract_image_from_readme(rd['content'], owner, repo)
    except Exception:
        preview = None
    repo_info = {
        "owner": owner,
        "name": data.get("name"),
        "html_url": data.get("html_url"),
        "description": data.get("description"),
        "language": data.get("language"),
        "updated_at": data.get("updated_at"),
        "stargazers_count": data.get("stargazers_count"),
        "forks_count": data.get("forks_count"),
        "homepage": data.get("homepage"),
        "preview": preview,
    }
    return repo_info


def load_featured():
    path = os.path.join(os.path.dirname(__file__), 'featured.json')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


@app.route('/')
def index():
    """Home page: displays featured projects (preferred) or user repos as fallback."""
    featured = load_featured()
    projects = []
    error = None
    try:
        if featured:
            for item in featured:
                owner = item.get('owner')
                repo = item.get('repo')
                if not owner or not repo:
                    continue
                info = fetch_repo(owner, repo)
                # allow fields override
                if item.get('title'):
                    info['title'] = item.get('title')
                if item.get('description'):
                    info['description'] = item.get('description')
                if item.get('image'):
                    info['preview'] = item.get('image')
                # allow setting a demo/homepage URL from featured.json (e.g. GitHub Pages)
                if item.get('homepage'):
                    info['homepage'] = item.get('homepage')
                elif item.get('demo'):
                    info['homepage'] = item.get('demo')
                info['tags'] = item.get('tags', [])
                projects.append(info)
        else:
            # If no featured.json, try to use GITHUB_USER env var
            username = os.getenv('GITHUB_USER')
            if username:
                repos = fetch_repos_for_user(username)
                # convert to project shape
                for r in repos:
                    projects.append(r)
            else:
                error = 'No hay `featured.json` y no se ha configurado GITHUB_USER. Crea `featured.json` para seleccionar proyectos o añade GITHUB_USER en `.env`.'
    except requests.HTTPError as e:
        error = f'GitHub API error: {e}'
    except Exception as e:
        error = str(e)
    # Prepare title pieces for the templates
    # Use only SITE_ACCENT (blue part). The header always shows "<SITE_ACCENT> Portfolio".
    site_accent = SITE_ACCENT if SITE_ACCENT and SITE_ACCENT.strip() != '' else 'Mi'
    site_title = 'Portfolio'
    return render_template('index.html', site_accent=site_accent, site_title=site_title, site_name=SITE_NAME, site_subtitle=SITE_SUBTITLE, projects=projects, error=error)


@app.route('/project/<owner>/<repo>')
def project_detail(owner: str, repo: str):
    try:
        info = fetch_repo(owner, repo)
    except requests.HTTPError:
        abort(404)
    readme_html = ''
    try:
        rr = requests.get(f'https://api.github.com/repos/{owner}/{repo}/readme', headers=github_headers(), timeout=10)
        if rr.status_code == 200:
            rd = rr.json()
            content = base64.b64decode(rd.get('content', '')).decode('utf-8', errors='ignore')
            # render markdown to HTML
            readme_html = markdown.markdown(content, extensions=['extra'])
    except Exception:
        readme_html = ''
    return render_template('project.html', project=info, readme_html=readme_html)


@app.route('/api/project/<owner>/<repo>')
def api_project(owner: str, repo: str):
    """Return JSON with project metadata and rendered README (for modal)."""
    try:
        info = fetch_repo(owner, repo)
    except requests.HTTPError:
        return jsonify({'error': 'not found'}), 404
    readme_html = ''
    try:
        rr = requests.get(f'https://api.github.com/repos/{owner}/{repo}/readme', headers=github_headers(), timeout=10)
        if rr.status_code == 200:
            rd = rr.json()
            content = base64.b64decode(rd.get('content', '')).decode('utf-8', errors='ignore')
            readme_html = markdown.markdown(content, extensions=['extra'])
    except Exception:
        readme_html = ''
    return jsonify({'project': info, 'readme_html': readme_html})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
