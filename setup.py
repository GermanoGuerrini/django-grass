from distutils.core import setup
import os

PROJECT_NAME = 'grass'
ROOT = os.path.abspath(os.path.dirname(__file__))

project = __import__(PROJECT_NAME)
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

data_files = []
for dirpath, dirnames, filenames in os.walk(PROJECT_NAME):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        continue
    elif filenames:
        for f in filenames:
            data_files.append(os.path.join(
                dirpath[len(PROJECT_NAME) + 1:], f))


def read(filename):
    return open(os.path.join(ROOT, filename)).read()


setup(
    name='django-grass',
    version=project.get_version(),
    description=project.__doc__,
    long_description=read('README.rst'),
    author='Germano Guerrini',
    author_email='germano.guerrini@gmail.com',
    url='http://bitbucket.com/uoz/django-grass',
    keywords='django generic relation admin',
    packages=[
        PROJECT_NAME,
        # TODO
        # '{0}.templatetags'.format(PROJECT_NAME),
        # '{0}.tests'.format(PROJECT_NAME),
        # '{0}.tests.integration'.format(PROJECT_NAME),
        # '{0}.tests.templatetags'.format(PROJECT_NAME),
    ],
    package_data={PROJECT_NAME: data_files},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)
