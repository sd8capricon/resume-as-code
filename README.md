# Resume As Code

I built this out of pure frustration after struggling (and failing) to get LaTeX running locally. I just wanted a simple, open, lightweight yet powerful way to update my resume without constantly wrestling with messy Word formatting and can be versioned with git.

A flexible, template-based resume generator that converts YAML resume data into beautifully formatted HTML documents, ready to be exported as a single page A4 pdf directly from the browser.

It’s designed to be easily extendable — customize or create your own YAML structure, css styling, and Jinja templates.

## Features

- **Data-Driven Design**: Store resume data in clean YAML format
- **Template-Based**: Use Jinja2 templates for customizable resume layouts
- **HTML Output**: Generate professional HTML resumes
- **Styled**: Includes CSS styling for polished results
- **Modular Templates**: Organized template sections for easy customization

## Project Structure

```
.
├── build.py              # Main build script for generating resumes
├── data/
│   └── resume.yaml       # Resume data in YAML format
├── templates/
│   ├── resume.html.jinja # Main HTML template
│   └── sections/         # Reusable template sections
├── styles/
│   └── style.css         # CSS stylesheet
└── dist/                 # Output directory for generated files
```

## Prerequisites

- Python 3.13+
- `uv` package manager (recommended) or `pip`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies:
```bash
uv sync
```

Or with pip:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Generate a resume with default settings:

```bash
uv run build.py
```

This will:
- Read resume data from `data/resume.yaml`
- Apply the `resume.html.jinja` template
- Output the result to `dist/resume.html`
- Copy `styles/style.css` to `dist/style.css`

### Custom YAML and Template

Specify custom data and template files:

```bash
uv run build.py path/to/resume.yaml path/to/template.jinja
```

### Custom Output Location

Specify where to save the generated resume:

```bash
uv run build.py -o dist/my-resume.html
# or
uv run build.py --output dist/my-resume.html
```

## Resume Data Format

The `data/resume.yaml` file contains your resume information:

```yaml
about:
  name: Your Name
  email: your.email@example.com
  website: yourwebsite.com
  github:
    username: yourusername
    link: https://github.com/yourusername
  description: Brief professional description

education:
  - institution: University Name
    degree: Your Degree
    start: "2020"
    end: "2024"
    cgpa: "8.83/10"

experience:
  - company: Company Name
    location: City
    link: https://company.com
    roles:
      - title: Job Title
        start: "2024"
        end: "Present"
        highlights:
          - Achievement or responsibility
          - Another achievement

projects:
  - name: Project Name
    link: https://github.com/...
    description: Brief description
    highlights:
      - Key feature or achievement
      - Technology used

accomplishments:
  - title: Award or Recognition
    issuer: Organization
    highlights:
      - Details about the accomplishment

publications:
  - publication: Full citation
    link: https://doi.org/...
```

## Dependencies

- **jinja2**: Template engine for rendering resume layouts
- **pyyaml**: YAML parsing for resume data
- **weasyprint**: PDF generation support (WIP)

## Development

To modify the templates or styling:

1. Edit template files in `templates/` (using Jinja2 syntax)
2. Update CSS in `styles/style.css`
3. Run `python build.py` to regenerate

Template variables are exposed from the YAML file, making it easy to access resume data in your templates.

## Author

Created by Siddharth Dhaigude
