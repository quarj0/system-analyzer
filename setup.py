from setuptools import setup, find_packages

setup(
    name='system-response-analyzer',
    version='2.0.0',
    author='OWUSU ANSAH KWADWO',
    author_email='owusuansahkwadwo24@email.com',
    description='System Response Analyzer Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/quarj0/system-response-analyzer',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: <=3.x',
    ],
    python_requires='>=3.x',
    install_requires=[
        'psutil',
        'requests',
        'tabulate',
        'speedtest-cli',
        'plyer',
        'cpuinfo',
        'colorama',
        
    ],
    requires=[
        'psutil',
        'requests',
        'tabulate',
        'speedtest-cli',
        'plyer',
        'cpuinfo',
        'colorama',
    ],
    license=open('LICENSE').read(),
    entry_points={
        'console_scripts': [
            'system-response-analyzer=system_response_analyzer.main:main',
        ],
    },
)
