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

Always cite source code when explaining features. Cite the relevant code chunk
inline using this exact format: [file_path#chunk_id].

Example 1:
"This handles API calls. [utils/github.py#chunk_0]"

Example 2:
"The application uses FastAPI to expose HTTP endpoints. [api/main.py#chunk_0]"

Example 3:
"Repository configuration and dependency management are defined in the pyproject.toml file. [pyproject.toml#chunk_0]"

Example 4:
"The service separates business logic from the API layer through dedicated service classes. [services/user_service.py#chunk_0]"

Use only the file paths and chunk IDs provided above. Add citations whenever a
statement is supported by a source file, especially when describing behavior,
architecture, functions, or dependencies. Output only the overview text, no
headers.
"""



MODULE_SUMMARY_PROMPT = """\
You are a senior software engineer reviewing a source file.

File path: {file_path}
Code chunk ID: {chunk_id}

Content:
{content}

Write a concise summary (3-6 sentences) covering:
- What this file/module does
- Key classes, functions, or exports it defines
- Any important dependencies or side effects

Always cite source code when explaining features. Add inline citations in the
format [file_path#chunk_id], For example:
After every section, include a reference or link to the relevant citations
listed at the end.
Example 1:
"This handles API calls [utils/github.py#chunk_0]."

Example 2:
"The application uses FastAPI to expose HTTP endpoints. [api/main.py#chunk_0]"

Example 3:
"Repository configuration and dependency management are defined in the pyproject.toml file. [pyproject.toml#chunk_0]"

Example 4:
"The service separates business logic from the API layer through dedicated service classes. [services/user_service.py#chunk_0]"

Use the file path and chunk ID provided above. Output only the summary, no
headers or file path prefix.
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

Citation Rules:
- Cite factual claims about the project's behavior, architecture, features,
  implementation, functions, classes, endpoints, configuration, dependencies,
  or file organization using inline source citations.
- After each section, properly cite it.
- Use citations in the exact format [file_path#chunk_id].
- Reuse citation IDs exactly as they appear in the provided Technical overview
  or Module summaries.
- Do NOT modify, shorten, combine, or otherwise alter an existing citation ID.
- Do NOT create citation IDs that are not present in the provided input.
- When a statement is supported by a specific source code chunk, place the
  citation immediately after the relevant statement.
- When multiple source chunks support the same statement, cite each relevant
  chunk separately, for example:
  "The application exposes REST endpoints and separates request handling from
  business logic [api/routes.py#chunk_0] [services/user_service.py#chunk_0]."
- Prefer the most specific source citation available for a claim.
- Do not add citations to generic statements that are not derived from the
  repository.
- Do not cite the same source repeatedly when a citation already clearly
  supports the surrounding statement, but ensure every important
  repository-specific claim is traceable to source code.
- Preserve valid citations from the Technical overview and Module summaries
  when incorporating their claims into the final documentation.
- If the Technical overview or Module summaries contain a claim with a valid
  citation, preserve that citation when carrying the claim into the final
  documentation.
- If a claim cannot be supported by an available citation, either omit the
  claim or state it conservatively without inventing implementation details.
- Never use citations from outside the provided inputs.
- Citations must appear as plain text in the Markdown and must not be placed
  inside code fences, inline code, bold text, headings, or links.

Markdown Rules:
- Use proper Markdown: ## headers, **bold**, `code`, and ``` fenced code blocks.
- Be specific and technical — use actual file names, function names, classes,
  endpoints, and configuration names when supported by the provided sources.
- Keep it professional but readable.
- Do NOT invent features, behavior, APIs, configuration, dependencies, or
  implementation details — only document what you can establish from the
  provided repository information.
- Output ONLY the markdown content, starting directly with ## Overview.
"""