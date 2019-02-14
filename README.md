# Notes on fixing the metadata in the google/fonts repo

In trying to address the Google Fonts issue [Check all families that have latin-ext glyphs enable it](https://github.com/google/fonts/issues/187), it is necessary to check all fonts in the [google/fonts repo](https://github.com/google/fonts) for the presence of glyphs considered to be in the [`latin-ext` glyphset](https://github.com/googlefonts/gftools/blob/master/Lib/gftools/encodings/latin-ext_unique-glyphs.nam). 

This is a bigger project than it may seem at first, in that it involves about 1,000 fonts across a diverse range of languages, genres, and complexity. Luckily, there are existing tools that will help, but these are not perfect.

In order to work through this methodically, I will use this repo to store working notes, existing error logs, and other data that comes up.

