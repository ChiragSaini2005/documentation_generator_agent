"""
utils/prompts.py
All prompt templates used by the agent nodes.
"""

# ── Node 2: analyze_code ──────────────────────────────────────────────────────

REPO_OVERVIEW_PROMPT = """\
You are a senior software engineer. Analyze the following repository file tree
and selected source files, then write a concise technical overview.

Project title      : {title}
Project description: {description}
Repository URL     : {repo_url}

File tree (all paths):
{file_tree}

Selected file contents:
{file_contents}

Write a 3-5 paragraph technical overview covering:
1. What the project does and its main purpose
2. The overall architecture and code organization
3. Key technologies, frameworks, and dependencies
4. Notable design patterns or architectural decisions

Be precise and technical. Output only the overview text, no headers.
"""

MODULE_SUMMARY_PROMPT = """\
You are a senior software engineer reviewing a source file.

File path: {file_path}

Content:
{content}

Write a concise summary (3-6 sentences) covering:
- What this file/module does
- Key classes, functions, or exports it defines
- Any important dependencies or side effects

Output only the summary, no headers or file path prefix.
"""

# ── Node 3: generate_docs ─────────────────────────────────────────────────────

GENERATE_DOCS_PROMPT = """\
You are a technical writer creating professional documentation for a software project.

Project title      : {title}
Project description: {description}
Repository URL     : {repo_url}

Technical overview:
{repo_overview}

Module summaries:
{module_summaries}

Generate comprehensive, well-structured documentation in Markdown format.
Include the following sections (use ## for section headers):

## Overview
A clear, engaging description of what the project does and who it's for.

## Features
Bullet list of the main features and capabilities.

## Architecture
How the project is structured, main components, and how they interact.
Include a brief description of the key files/modules.

## Installation
Step-by-step installation instructions. Infer the package manager and
setup steps from the file tree and config files you've seen.

## Usage
How to run and use the project. Include example commands or code snippets
where appropriate, wrapped in ```language fenced blocks.

## API Reference
(If applicable) Document key public functions, classes, or endpoints.
Use ### subheadings for each item.

## Configuration
(If applicable) Document environment variables, config files, or settings.

## Contributing
Brief guidelines for contributors.

## License
If a license file was found, mention it. Otherwise note it's not specified.

Rules:
- Use proper Markdown: ## headers, **bold**, `code`, ``` fenced code blocks
- Be specific and technical — use actual file names, function names, etc.
- Keep it professional but readable
- Do NOT invent features — only document what you actually observed in the code
- Output ONLY the markdown content, starting directly with ## Overview
"""