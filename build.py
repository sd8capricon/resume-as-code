import argparse
import shutil
import sys
import tempfile
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

# base directory for project
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"

# output directory for generated files
DIST_DIR = BASE_DIR / "dist"
DIST_DIR.mkdir(exist_ok=True)


def load_yaml(path: Path):
    """Load YAML file (absolute or relative to data/)"""
    if not path.is_absolute():
        path = DATA_DIR / path

    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def create_env(template_dir: Path):
    return Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_template(yaml_path: Path, template_path: Path) -> str:
    """Render given template using given YAML"""

    # Resolve YAML
    data = load_yaml(yaml_path)

    # Resolve template location
    if not template_path.is_absolute():
        template_path = TEMPLATES_DIR / template_path

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    env = create_env(template_path.parent)

    template = env.get_template(template_path.name)

    # expose yaml as `resume`
    return template.render(data)


def render_pdf(html_path: Path, pdf_path: Path):
    """Print the rendered HTML to an A4 PDF using headless Chromium"""
    # imported lazily so HTML-only builds don't need playwright
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.resolve().as_uri())
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
        )
        browser.close()


def main():
    parser = argparse.ArgumentParser(
        description="Render resume from YAML + Jinja template"
    )

    parser.add_argument(
        "yaml",
        nargs="?",
        default="resume.yaml",
        help="YAML data file (default: resume.yaml)",
    )

    parser.add_argument(
        "template",
        nargs="?",
        default="resume.html.jinja",
        help="Jinja template file (default: resume.html.jinja)",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="resume.html",
        help="Output filename (default: dist/resume.html; extension follows --format)",
    )

    parser.add_argument(
        "--format",
        choices=("html", "pdf", "both"),
        default="both",
        help="Output format: html, pdf, or both (default: both)",
    )

    parser.add_argument(
        "--no-pdf",
        action="store_true",
        help="Skip generating the A4 PDF next to the HTML output",
    )

    args = parser.parse_args()

    if args.no_pdf:
        if args.format == "pdf":
            parser.error("--no-pdf cannot be combined with --format pdf")
        args.format = "html"

    output_html = render_template(Path(args.yaml), Path(args.template))

    out_path = Path(args.output)
    if not out_path.is_absolute():
        out_path = DIST_DIR / out_path

    output_format = args.format
    if output_format == "pdf":
        pdf_path = out_path.with_suffix(".pdf")
        html_path = None
    else:
        html_path = out_path.with_suffix(".html")
        pdf_path = html_path.with_suffix(".pdf")

    DIST_DIR.mkdir(exist_ok=True)
    if html_path is not None:
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(output_html, encoding="utf-8")

        # Copy stylesheet beside the HTML output.
        css_src = BASE_DIR / "styles" / "style.css"
        css_dest = html_path.parent / "style.css"
        if css_src.exists():
            shutil.copy2(css_src, css_dest)
        else:
            sys.stderr.write(f"warning: stylesheet {css_src} not found\n")

        print(f"wrote resume to {html_path}")
        if css_dest.exists():
            print(f"copied stylesheet to {css_dest}")

    if output_format in ("pdf", "both"):
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        if html_path is not None:
            render_pdf(html_path, pdf_path)
        else:
            # Chromium prints a local HTML file, so stage it with its stylesheet.
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir = Path(temp_dir)
                temp_html = temp_dir / "resume.html"
                temp_html.write_text(output_html, encoding="utf-8")
                css_src = BASE_DIR / "styles" / "style.css"
                if css_src.exists():
                    shutil.copy2(css_src, temp_dir / "style.css")
                render_pdf(temp_html, pdf_path)
        print(f"wrote pdf to {pdf_path}")


if __name__ == "__main__":
    main()
