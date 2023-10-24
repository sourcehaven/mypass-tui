from setuptools import setup


setup(
    name="mypass-tui",
    version="0.0.1-dev",
    description="Text-based user interface for MyPass using Textual.",
    author="ricky :) (: skyzip",
    license="MIT",
    packages=["mypass_tui"],
    package_dir={"mypass_tui": "mypass_tui"},
    install_requires=["textual", "pyperclip"],
    package_data={"": ["license"]},
)
