from setuptools import setup, find_packages

setup(
    name='system-analyzer',
    version='2.0.0', 
    author='OWUSU ANSAH KWADWO',
    author_email='guidemelearn.info@gmail.com',
    description='System Analyzer Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/quarj0/system-analyzer',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    python_requires='>=3.8',  
    install_requires=[
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
            'system-analyzer=system_analyzer.main:main',
        ],
    },
)
