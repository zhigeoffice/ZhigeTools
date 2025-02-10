# Development Guide

## Environment Setup

1. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

## PyPI Upload Configuration

To upload packages to PyPI:

1. Copy `pypi.conf.example` to `pypi.conf`:
```bash
cp pypi.conf.example pypi.conf  # Linux/Mac
# or
copy pypi.conf.example pypi.conf  # Windows
```

2. Get your PyPI API token:
   - Go to https://pypi.org/manage/account/token/
   - Create a new token with scope "Upload packages"
   - Copy the token (starts with `pypi-`)

3. Edit `pypi.conf` and replace `your-pypi-token-here` with your actual PyPI token

4. The `pypi.conf` file is ignored by git to keep your token secure

## Building and Publishing

1. Update version in `setup.py`

2. Build and upload to PyPI:
```bash
./setup.bat  # Windows
# or
sh setup.sh  # Linux/Mac
```

## Development Workflow

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and add tests if needed

3. Run tests:
```bash
python -m pytest
```

4. Update documentation:
   - Update README.md and README-zh.md
   - Add example code if needed
   - Update version changelog

5. Commit your changes:
```bash
git add .
git commit -m "feat: your feature description"
```

6. Create pull request

## Project Structure

```
ZhigeTools/
├── setup.py           # Package configuration
├── setup.bat          # Windows build script
├── setup.sh           # Linux/Mac build script
├── requirements.txt   # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── README.md         # English documentation
├── README-zh.md      # Chinese documentation
├── DEVELOPMENT.md    # Development guide
├── LICENSE          # MIT license
├── pypi.conf.example # PyPI configuration template
├── zhige_tools/     # Main package
│   ├── __init__.py
│   ├── base_converter.py
│   ├── ini_reader.py
│   ├── snowflake.py
│   └── examples/    # Example code
│       ├── __init__.py
│       ├── base_converter_example.py
│       ├── ini_reader_example.py
│       └── snowflake_example.py
└── tools_test/     # Test cases
    ├── __init__.py
    ├── test_base_converter.py
    ├── test_ini_reader.py
    └── test_snowflake.py
```

## Coding Standards

1. Follow PEP 8 style guide
2. Add type hints to all functions
3. Write docstrings for all modules, classes and functions
4. Include examples in docstrings
5. Add tests for new features
6. Keep both English and Chinese documentation updated

## Release Process

1. Update version number in `setup.py`
2. Update changelog in README.md and README-zh.md
3. Run all tests
4. Build and upload to PyPI
5. Create git tag for the release
6. Push changes and tag to GitHub

## Questions and Support

If you have any questions about the development process, please:
1. Check existing documentation
2. Search in issues
3. Create new issue if needed

## License

This project is licensed under the MIT License - see the LICENSE file for details. 