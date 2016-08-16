# Changelog

## [0.2.0] - [unreleased]
### Added
- Added possibility to create an object by dictionary
(pass `__dictionary` argument)
- Added `BooleanField`

### Changed
- Changed `__to_dict` method to public method `to_dict`
- Changed `Schema` to `cls` when calling `get_handler`

### Fixed
- Fixed `drop_collection` on MongoDB
- Fixed `convert_ids` to handle operators on `_id`

## [0.1.0] - 2016-08-12
### Added
- Added Changelog
- Added abstraction layer for database handling
- Added MongoDB support
- Added MongoDB configuration example

### Changed
- Changed `find_one`: use find with limit 1
- Changed imports: use relative paths
- *BREAKING*: Changed configuration - See README.md

### Removed
- Debug output

## [0.0.2] - 2016-05-22
### Added
- Added possibility to sort by class `@property`
- Added missing fields and validators
- Added unit tests
- Added `StringMinValidator`
- Added `StringMaxValidator`
- Added post processor
- Added `PasswordField`
- Added ordering in `find` method
- Added `DateField`
- Added `distinct` method

### Removed
- Removed irrelevant arguments

### Fixed
- Fixed `update` method (save)
- Fixed password `MaxLength`

## [0.0.1] - 2016-05-20
- Initial release