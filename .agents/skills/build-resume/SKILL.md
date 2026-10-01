---
name: build-resume
description: Build a resume from a project YAML data file as HTML, PDF, or both. Use when the user wants this repository's resume renderer to produce output.
---

# Build a Resume

Render the requested resume YAML with this repository's `build.py` and its default Jinja template.

## Inputs

- Require the resume YAML filename and output format (`html`, `pdf`, or `both`). If either is missing, ask for it before running the build.
- If the user has not provided an output destination, ask where to save the generated file. They may give a filename, relative path, or absolute path.
- Preserve the requested destination and format. Do not silently substitute another YAML file or format.

## Build

Run `uv run build.py <yaml-file> --format <format> --output <destination>` from the repository root. The template defaults to `templates/resume.html.jinja`.

`build.py` resolves relative YAML paths beneath `data/`. It resolves relative output destinations beneath `dist/`; absolute output paths are used directly. The output extension is replaced to match the format. `html` also writes a stylesheet beside the HTML file; `pdf` writes only the PDF; `both` writes HTML, CSS, and PDF. For PDF output, the project needs Playwright Chromium installed.

Report the actual output path or paths when the command succeeds. If the build fails, give the relevant error and do not claim an output was produced.
