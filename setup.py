import setuptools

with open("README.md", "r") as f:
        long_description = f.read()

        setuptools.setup(
                name="am-research",
                version="1.0",
                author="William O'Brien",
                author_email="william.obrien@columbia.edu",
                description="LPBF research predictive models",
                long_description=long_description,
                long_description_content_type="text/markdown",
                url="https://github.com/wgobrien/am-research",
                packages=setuptools.find_packages(),
                classifiers=[
                             "Programming Language :: Python :: 3",
                             "Operating System :: OS Independent",
                            ],
                python_requires='>=3.5',

        )
