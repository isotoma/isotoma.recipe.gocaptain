from setuptools import setup, find_packages

version = '0.0.5'

setup(
    name = 'isotoma.recipe.gocaptain',
    version = version,
    description = "Starting and stopping daemons",
    long_description = open("README.rst").read() + "\n" + \
                       open("CHANGES.txt").read(),
    classifiers = [
        "Framework :: Buildout",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
    ],
    package_data = {
        '': ['README.rst', 'CHANGES.txt'],
        'isotoma.recipe.gocaptain': ['lsb.tmpl', 'simple.tmpl']
    },
    keywords = "buildout",
    author = "Doug Winter",
    author_email = "doug.winter@isotoma.com",
    url = 'http://pypi.python.org/pypi/isotoma.recipe.gocaptain',
    license="Apache Software License",
    packages = find_packages(exclude=['ez_setup']),
    namespace_packages = ['isotoma', 'isotoma.recipe'],
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
        'zc.buildout',
        'Cheetah',
    ],
    entry_points = {
        "zc.buildout": [
            "default = isotoma.recipe.gocaptain:AutomaticBuildout",
            "simple = isotoma.recipe.gocaptain:SimpleBuildout",
            "ubuntu = isotoma.recipe.gocaptain:LinuxStandardBaseBuildout",
        ],
    }
)
