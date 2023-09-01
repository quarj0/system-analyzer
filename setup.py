from setuptools import setup, find_packages

setup(
    name='system-response-analyzer',
    version='1.1.0',
    author='OWUSU ANSAH K.',
    author_email='owusuansahkwadwo24@email.com',
    description='System Response Analyzer Tool',
    long_description='A tool to measure system response time and check for OS updates.',
    url='https://github.com/qu4r0/system-response-analyzer',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        
    ],
    python_requires='>=3.6',
    install_requires=[
        'psutil',
        'requests',
        'tabulate',
    ],
    entry_points={
        'console_scripts': [
            'system-response-analyzer=system_response_analyzer:main',
        ],
    },
)
