@echo off
echo Cleaning old build files...
rmdir /s /q build dist zhige_tools.egg-info

echo Building package...
python setup.py sdist bdist_wheel

echo Uploading to PyPI...
for /f "tokens=2 delims==" %%a in ('findstr "token" pypi.conf') do (
    twine upload dist/* -u __token__ -p %%a
)