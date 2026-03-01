import yaml
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

# base directory for project
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"


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


env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_resume() -> str:
    """Render the top-level resume template with the loaded YAML data.

    Returns the generated Markdown string; callers can print it, write it to
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
    }

    template = env.get_template("resume.md.jinja")
    return template.render(**context)


if __name__ == "__main__":
    # simple CLI: write output to stdout or file
    import sys

    output = render_resume()
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(output, encoding="utf-8")
    else:
        print(output)
