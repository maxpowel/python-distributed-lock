from setuptools import setup

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name='distributed-lock',
    packages=['distributed_lock'],
    version='1.0',
    description='Distributed lock',
    author='Álvaro García',
    author_email='maxpowel@gmail.com',
    url='https://github.com/maxpowel/python-distributed-lock',
    download_url='https://github.com/maxpowel/python-distributed-lock/archive/master.zip',
    keywords=['redis', 'distributed', 'lock'],
    classifiers=['Topic :: Adaptive Technologies', 'Topic :: Software Development', 'Topic :: System',
                 'Topic :: Utilities'],
    install_requires=install_requires
)