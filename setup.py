from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='gyropalm_control',
    version='1.0.1',
    description='GyroPalm Python SDK for Robotic Control using Gestures',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['gyropalm_control'],
    install_requires=[
        'websockets>=7.0',
    ],
    data_files=[('examples', ['gyropalm_control/examples/realtime_test.py', 'gyropalm_control/examples/driving_test.py'])],
    project_urls={
        'Source': 'https://github.com/GyroPalm/GyroPalm-Python-SDK',
    },
    # other package metadata
)
