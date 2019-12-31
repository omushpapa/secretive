from setuptools import setup

try:
    import pypandoc

    long_description = pypandoc.convert_file('README.md', 'rst')
except (ImportError, OSError, RuntimeError):
    long_description = 'Usage available at http://github.com/giantas/pyconfigreader'

setup(
    name='passwordgen',
    version='0.1.0',
    description='A password generator',
    long_description=long_description,
    url='http://github.com/giantas/passwordgen',
    author='Aswa Paul',
    license='MIT',
    packages=[
        'passwordgen'
    ],
    entry_points={
        'console_scripts': [
            'passwordfrom=passwordgen.command_line:password_from',
            'passwordgen=passwordgen.command_line:password_gen',
        ]
    },
    install_requires=[
        'click',
    ],
    include_package_data=True,
    zip_safe=False,
    python_requires='>2.7, >3.5, <3.7',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
    keywords='password generator secret random'
)
