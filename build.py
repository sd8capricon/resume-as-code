import yaml
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

# base directory for project
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"

# output directory for generated files
DIST_DIR = BASE_DIR / "dist"

# ensure dist exists when script is run
DIST_DIR.mkdir(exist_ok=True)


def load_yaml(path: Path):
    """Load a single YAML file and return the parsed value.

    ``path`` may be either a full path or a filename relative to the
    `data` directory.  This is a thin wrapper around :func:`yaml.safe_load`.
    """

    if not path.is_absolute():
        path = DATA_DIR / path

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


about = load_yaml(DATA_DIR / "about.yaml")
accomplishments = load_yaml(DATA_DIR / "accomplishments.yaml")
education = load_yaml(DATA_DIR / "education.yaml")
experience = load_yaml(DATA_DIR / "experience.yaml")
publications = load_yaml(DATA_DIR / "publications.yaml")
projects = load_yaml(DATA_DIR / "projects.yaml")


env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_resume() -> str:
    """Render the top-level resume template with the loaded YAML data.

    Returns the generated HTML string; callers can print it, write it to
    a file, or pass it to a converter (e.g. pandoc) to produce LaTeX/PDF.

    The context keys mirror the YAML filenames so they are available in
    templates by name.
    """

    context: dict = {
        "about": about,
        "accomplishments": accomplishments,
        "education": education,
        "experience": experience,
        "publications": publications,
        "projects": projects,
    }

    template = env.get_template("resume.html.jinja")
    return template.render(**context)


if __name__ == "__main__":
    # simple CLI: write output to stdout or file
    import sys
    import shutil

    output = render_resume()

    # ensure dist directory exists before writing files
    DIST_DIR.mkdir(exist_ok=True)

    # determine target html path; if user passed one it is treated as filename
    if len(sys.argv) > 1:
        out_path = Path(sys.argv[1])
        # if user provided just a name, put it inside dist
        if not out_path.is_absolute():
            out_path = DIST_DIR / out_path
    else:
        out_path = DIST_DIR / "resume.html"

    out_path.write_text(output, encoding="utf-8")

    # copy stylesheet into dist
    css_src = BASE_DIR / "styles" / "style.css"
    css_dest = DIST_DIR / "style.css"
    if css_src.exists():
        shutil.copy2(css_src, css_dest)
    else:
        sys.stderr.write(f"warning: stylesheet {css_src} not found\n")

    # also inform the user of what was written
    print(f"wrote resume to {out_path}")
    if css_dest.exists():
        print(f"copied stylesheet to {css_dest}")
