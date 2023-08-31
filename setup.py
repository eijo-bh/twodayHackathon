
# NOTE --> REMEMBER TO INSTALL SETUPTOOLS IF YOU HAVE NOT DONE SO ALREADY

# Install with command: pip install .
from setuptools import find_packages
from setuptools import setup
setup(
    name="src",
    version="0.0.1",
    maintainer="thbm@kapacity",
    python_requires='==3.10.11',
    description="Application for hackathon",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "annoy==1.17.3",
        "pandas==2.0.2",
        "numpy==1.24.3",
        "openai==0.27.7",
        "tiktoken==0.4.0",
        "langchain==0.0.244",
        "llama-index===0.7.13",
        "streamlit==1.22.0",
        "streamlit_chat==0.0.2.2",
        "streamlit-option-menu==0.3.6"
    ],
)
