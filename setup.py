from setuptools import setup

try:
    import pypandoc

    long_description = pypandoc.convert_file('README.md', 'rst')
except (ImportError, OSError, RuntimeError):
    long_description = 'Usage available at http://github.com/giantas/pyconfigreader'

setup(
    name='secretive',
    version='0.1.1',
    description='A password generator',
    long_description=long_description,
    url='http://github.com/giantas/passwordgen',
    author='Aswa Paul',
    license='MIT',
    packages=[
        'secretive'
    ],
    entry_points={
        'console_scripts': [
            'secretfrom=secretive.command_line:password_from',
            'secretgen=secretive.command_line:password_gen',
        ]
    },
    install_requires=[
        'click',
    ],
    include_package_data=True,
    zip_safe=False,
    python_requires='>2.7, >3.5, <3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.6",
    ],
    keywords='password generator secret random'
)
