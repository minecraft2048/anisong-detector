# anisong-detector

## Demo
https://www.reddit.com/r/Python/comments/f68eo9/change_wallpaper_to_the_currently_playing_anime/ 

## System requirements

- Python 3.8
- Linux with KDE Plasma desktop environment
  
## Installation

1. Install these dependencies using `pip` or your package manager:
   - [python-parse](https://pypi.org/project/parse/)
   - sklearn
   - [Plasma Integration for Firefox](https://addons.mozilla.org/en-US/firefox/addon/plasma-integration/)
   - [fuzzywuzzy](https://pypi.org/project/fuzzywuzzy/)
   - [sparse-dot-topn](https://github.com/ing-bank/sparse_dot_topn)
2. Download some anime wallpaper and put it in wallpaper folder
3. Rename the wallpapers to the anime title that is in MyAnimeList website. For example for a Bleach wallpaper, name it `Bleach.jpg`


## Usage

- Run `python identify_anisong.py`

## TODO

- [ ] Complete the `anisong.db` database by extracting data from Kaggle MyAnimeList data dump
- [ ] Evaluate which string fuzzy matching function is the fastest and uses the lowest amount of RAM
- [ ] Find an online wallpaper provider  


