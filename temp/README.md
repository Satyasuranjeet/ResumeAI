# Python Virtual Environment

This directory contains the Python virtual environment for the Resume Analyzer project.

## Contents

- `Scripts/` - Python executable and activation scripts
- `Lib/` - Installed Python packages and dependencies
- `Include/` - Python header files
- `pyvenv.cfg` - Virtual environment configuration

## Purpose

This virtual environment ensures:
- Isolated Python dependencies
- Consistent package versions
- No conflicts with system Python packages

## Usage

### Activation (Windows)
```bash
temp\Scripts\activate
```

### Activation (Unix/MacOS)
```bash
source temp/bin/activate
```

### Deactivation
```bash
deactivate
```

## Important Notes

⚠️ **Do not delete this folder while working on the project**

- This folder is excluded from Vercel deployment via `.vercelignore`
- Contains all required dependencies from `requirements.txt`
- Git tracking ensures consistent development environment

## Dependencies

This environment includes:
- Flask 3.0.0
- PyPDF2 3.0.1
- Werkzeug 3.0.1
- And other required packages

To recreate this environment:
```bash
python -m venv temp
temp\Scripts\activate  # Windows
pip install -r requirements.txt
```
