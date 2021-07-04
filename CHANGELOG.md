Changelog
======================================================================

`0.0.2` - _[unreleased]_
----------------------------------------------------------------------

### Added

- Ability to save to `.csv` (results + some metadata)

### Fixed

- Require a minimum distance between two audio timestamps to not record too many
  timestamps when volume is around threshold

### Changed

- New default values for `audio_threshold` and `audio_interval`
- CLI now outputs `.csv` files by default (can be changed with the `-f` flag)
- `testvid.mp4` is now slightly more accurate
- `data/example/local.mkv` reflects new `testvid.mp4`

`0.0.1` - _2021-06-14_
----------------------------------------------------------------------

- Initial Release