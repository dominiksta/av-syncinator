Changelog
======================================================================

`0.0.3` - _[unreleased]_
----------------------------------------------------------------------

### Changed

- Default parameter values in CLI now adjusted to the same values as in GUI
- `.csv` files from CLI now are named based on the input filename instead of a
  generic `out.csv`


`0.0.2` - _2021-07-05_
----------------------------------------------------------------------

### Added

- Ability to save to `.csv` (results + some metadata)
- By default, AV-Syncinator now attempts to ignore audio stutters to not distort
  measured asynchronicity for timestamps after the stutter. Can be disabled by
  either a checkbox in the GUI or the new `--no-try-match` flag in the CLI.

### Fixed

- Require a minimum distance between two audio timestamps to not record too many
  timestamps when volume is around threshold

### Changed

- New default values for `audio_threshold` and `audio_interval`
- `testvid.mp4` is now slightly more accurate
- `data/example/local.mkv` reflects new `testvid.mp4`
- CLI now outputs `.csv` files by default (can be changed with the `-f` flag)
- CLI now uses the current directory as default (so `-o` needs to be specified
  in less situations)

`0.0.1` - _2021-06-14_
----------------------------------------------------------------------

- Initial Release