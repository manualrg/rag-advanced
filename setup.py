from setuptools import setup, find_packages

setup(
    name="src",                     # Name of the package
    version="0.1",                         # Version number
    packages=find_packages(),              # Automatically find and include your packages
    install_requires=[                     # Dependencies
        # Example: 'numpy>=1.19.0',
    ],
    author="manualrg",
    description="A short description of your project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/my_project",  # Your project URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",      # Example license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',               # Specify the Python versions supported
)
