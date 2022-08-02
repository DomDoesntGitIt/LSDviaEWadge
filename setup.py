import setuptools


setuptools.setup(
    name='LSD',
    version='0.0.1',
    author='Elliot Wadge',
    author_email='ewadge@sfu.ca',
    description='Package for making level schemes',
    url='https://github.com/Elliot-Wadge/LSD',
    license='MIT',
    packages=["lsd"],
    install_requires=['numpy', 'plotly'],
)
