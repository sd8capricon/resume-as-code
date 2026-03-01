import argparse
import shutil
import sys
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
        help="Output HTML filename (default: dist/resume.html)",
    )

    args = parser.parse_args()

    output_html = render_template(Path(args.yaml), Path(args.template))

    out_path = Path(args.output)
    if not out_path.is_absolute():
        out_path = DIST_DIR / out_path

    DIST_DIR.mkdir(exist_ok=True)
    out_path.write_text(output_html, encoding="utf-8")

    # copy stylesheet into dist
    css_src = BASE_DIR / "styles" / "style.css"
    css_dest = DIST_DIR / "style.css"
    if css_src.exists():
        shutil.copy2(css_src, css_dest)
    else:
        sys.stderr.write(f"warning: stylesheet {css_src} not found\n")

    print(f"wrote resume to {out_path}")
    if css_dest.exists():
        print(f"copied stylesheet to {css_dest}")


if __name__ == "__main__":
    main()
