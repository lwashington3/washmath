from setuptools import setup

with open("README.md", 'r') as f:
	long_description = f.read()


project_name = "washmath"
git_url = "https://github.com/lwashington3/washmath"


setup(
	name=project_name,
	version="2.1.2",
	author="Len Washington III",
	author_email="l.washingtoniii.27@gmail.com",
	description="Custom mathematics module",
	include_package_data=True,
	long_description=long_description,
	long_description_content_type="test/markdown",
	url=git_url,
	project_urls={
		"Bug Tracker": f"{git_url}/issues"
	},
	license="MIT",
	packages=[project_name],
	install_requires=["matplotlib", "numpy", "pandas", "tabulate", "colors @ git+https://github.com/lwashington3/colors.git"]
)
