# Contribution Guidelines

## Development

### Installation

> Requirements: `nvm`

```sh
git clone git@github.com:wagtail/wagtail-react-streamfield.git
cd wagtail-react-streamfield/
# Use the correct Node version.
nvm use
# Run the static files’ build.
npm run build
```

## Releases

- Update the [CHANGELOG](https://github.com/wagtail/wagtail-react-streamfield/CHANGELOG.rst).
- Update the version number in `wagtail-react-streamfield/__init__.py`.
- Commit
- `rm dist/* ; python setup.py sdist bdist_wheel; twine upload dist/*`
- Finally, go to GitHub and create a release and a tag for the new version.
- Done!
