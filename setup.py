from setuptools import setup

setup(
    name='MRSS to Facebook Video',
    version='0.0.0',
    description='MRSS to Facebook Video',
    author='Fusion',
    author_email='tech@fusion.net',
    url='https://github.com/fusioneng/mrss-to-facebook-video-app',
    py_modules=['script', 'oauth', 'utils'],
    entry_points={
        'console_scripts': [
            'mtfv=script:cli'
        ]
    }
)
