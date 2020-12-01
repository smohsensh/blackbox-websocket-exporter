import os.path
from setuptools import setup

current_dir = os.path.abspath(os.path.dirname(__file__))

# Requirements
with open(os.path.join(current_dir, 'requirements.txt'), 'r') as f:
    requirements = [l.strip() for l in f]

# Metadata
metadata = {}
with open(os.path.join(current_dir, 'websocket_exporter', '__init__.py'), 'r') as f:
    exec(f.read(), metadata)

setup(
    name='websocket-exporter',
    version=metadata['__version__'],
    author=metadata['__author__'],
    license=metadata['__license__'],
    description=metadata['__description__'],
    install_requires=requirements,
    packages=['websocket_exporter'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring'
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['websocket_exporter = websocket_exporter.websocket_exporter:main']
    }
)
