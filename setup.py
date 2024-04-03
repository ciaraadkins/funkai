from setuptools import setup, find_packages

setup(
    name="funkai",
    version="0.6",
    packages=find_packages(),
    install_requires=[
        "openai",  'llmonitor'
    ],
    author="Ciara Adkins",
    author_email="adkins.ciara@gmail.com.com",
    description="Easily create and deploy placeholder functions powered by OpenAI for rapid prototyping, diverse linguistic tasks, and quick insights.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ciaraadkins/funkai",
)
