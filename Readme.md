# Japanese Wikipedia Word Fequency

This repository contains code to automatically download and process all
japanese wikipedia pages, parse it and build a frequency list of the japanese
words.

MeCab is used to parse japanese texts.

The script does everything automatically. However, to make things faster
it is possible to download
[this](https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2),
extract it and rename to `data.xml`. The code detect that the files exists and
uses it instead of downloading and extracting again.

# TODO

- [ ] Properly parse the XML file
- [x] Fix decompression not working
- [ ] Fix download progress bar to show ETA and %%s
- [ ] Fix decompression progress bar to show the actual progress (instead of whatever it is showing right now)
- [ ] Fix processing progress bar to show the actual progress (instead of whatever it is showing right now)
- [ ] Support resuming partial downloads
- [ ] Support resuming decompression
- [ ] Support resuming parsing and progression
- [ ] Make output compatible with yomichan's
- [ ] Make it not terribly slow

# LICENSE

See [LICENSE](LICENSE)
