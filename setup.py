from setuptools import setup, find_packages

setup(
    name="funkai",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",  # Assuming you're using the openai package
        # Add other dependencies if needed
    ],
    author="Your Name",
    author_email="adkins.ciara@gmail.com.com",
    description="A library to create placeholder functions using the OpenAI API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ciaraadkins/funkai",  # Link to the repository or library's website
)
