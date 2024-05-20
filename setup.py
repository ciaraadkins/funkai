from setuptools import setup, find_packages

setup(
    name="funkai",
    version="1.1",
    packages=find_packages(),
    install_requires=[
        "openai",  'llmonitor', 'anthropic'
    ],
    author="Ciara Adkins",
    author_email="adkins.ciara@gmail.com.com",
    description="Easily create and deploy placeholder functions powered by OpenAI and Anthropic (Claude) for rapid prototyping, diverse linguistic tasks, and quick insights.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ciaraadkins/funkai",
)
