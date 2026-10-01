# Repository Guidelines

Keep `AGENTS.md` and `CLAUDE.md` in sync: when editing guidance in either file, make the same change to the other.

## Project Structure

`build.py` is the rendering entry point. Resume content lives in `data/resume.yaml`; the main Jinja template is `templates/resume.html.jinja`, with reusable section templates in `templates/sections/`. Styling and print layout are in `styles/style.css`. The build writes generated HTML and a CSS copy to `dist/`, which is output rather than source. There is no separate test directory.

## Build and Review

- `uv sync` installs the dependencies (Python 3.13+); `pip install -r requirements.txt` is the pip alternative. PDF output needs a one-time `uv run playwright install chromium`.
- `uv run build.py` renders the default YAML and template to `dist/resume.html` and `dist/resume.pdf`; use `--format html`, `--format pdf`, or `--format both` to choose outputs, and `--no-pdf` remains an alias for HTML only.
- `uv run build.py other.yaml other.jinja -o preview.html` renders custom inputs. Relative YAML and template paths resolve under `data/` and `templates/`; a relative output path resolves under `dist/`.

There is no automated test, formatter, or linter configured. After changes, rebuild and inspect `dist/resume.html` in a browser, including print preview; the CSS targets a single A4 page, so check for overflow or an extra page.

## Content, Templates, and Style

Keep resume entries and personal details in YAML rather than hard-coding them in templates. Top-level YAML keys are exposed directly to Jinja templates. Add a section by defining its data, creating `templates/sections/<name>.html.jinja`, and including it in `templates/resume.html.jinja` in the desired display order.

Use clear, lowercase filenames with underscores where needed. Follow the existing Python style: four-space indentation, descriptive `snake_case` names, and standard-library imports before third-party imports. Preserve the HTML autoescaping and whitespace settings in `build.py`. Keep CSS changes mindful of the compact print layout.

## Commits and Pull Requests

Recent commits use short, informal summaries (for example, `Added skills`, `update resume`, and `cleanup build`); keep summaries brief and focused on one change. A pull request should explain the user-visible or layout change, list any relevant build command run, and include a screenshot or print-preview image when visual output changes. Note any YAML schema changes so existing custom resume data can be updated.

## Generated Files and Privacy

Do not commit `dist/` output unless a change explicitly requires a generated artifact. Resume YAML can contain personal information; avoid copying real contact details into examples, logs, or screenshots shared publicly.
