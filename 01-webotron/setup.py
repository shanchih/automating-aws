from setuptools import setup

setup(
    name='webotron-01',
    version='0.1',
    author='Alex Chang',
    author_email='pennjava@gmail.com',
    description='Webotron is a tool to deploy static website to AWS',
    license='GPLv3+',
    packages=['webotron'],
    url='https://github.com/shanchih/automating-aws',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        webotron=webotron.webotron:cli
    '''

)
