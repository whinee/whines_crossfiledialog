# Bump Version

## Semantic Versioning

This project uses the [Semantic Versioning](https://semver.org). According to the site:

Given a version number MAJOR.MINOR.PATCH, increment the:

- MAJOR version when you make incompatible API changes
- MINOR version when you add functionality in a backward compatible manner
- PATCH version when you make backward compatible bug fixes

## How to Bump

The table below illustrates the effect of the `just bump` subcommands on the following version strings:

|subcommand|before|after|
|:---:|:---:|:---:|
|`major`|1.3.0|2.0.0|
|`minor`|2.1.4|2.2.0|
|`patch`|4.1.1|4.1.2|
|`premajor`|1.0.2|2.0.0a0|
|`preminor`|1.0.2|1.1.0a0|
|`prepatch`|1.0.2|1.0.3a0|
|`prerelease`|1.0.2|1.0.3a0|
|`prerelease`|1.0.3a0|1.0.3a1|
|`prerelease`|1.0.3b0|1.0.3b1|

The option `--next-phase` allows the increment of prerelease phase versions.

|subcommand|before|after|
|:---:|:---:|:---:|
|`prerelease –-next-phase`|1.0.3a0|1.0.3b0|
|`prerelease –-next-phase`|1.0.3b0|1.0.3rc0|
|`prerelease –-next-phase`|1.0.3rc0|1.0.3|
