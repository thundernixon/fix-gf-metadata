# Notes on fixing the metadata in the google/fonts repo

In trying to address the Google Fonts issue [Check all families that have latin-ext glyphs enable it](https://github.com/google/fonts/issues/187), it is necessary to check all fonts in the [google/fonts repo](https://github.com/google/fonts) for the presence of glyphs considered to be in the [`latin-ext` glyphset](https://github.com/googlefonts/gftools/blob/master/Lib/gftools/encodings/latin-ext_unique-glyphs.nam). 

This is a bigger project than it may seem at first, in that it involves about 1,000 fonts across a diverse range of languages, genres, and complexity. Luckily, there are existing tools that will help, but these are not perfect.

In order to work through this methodically, I will use this repo to store working notes, existing error logs, and other data that comes up.

## Process

I've made the following bash script to run `gftools add-font` to all directories of a directory that is passed in. Then, I've added it to the `bin` directory of my virtual environment.

```
#!/bin/bash

set -e # uncomment to stop on errors

# get args
dirOfFontDirs="$1"

dirs=$(ls $dirOfFontDirs)

for fontdir in $dirs; do
    echo ====================================
    echo $fontdir
    gftools add-font $dirOfFontDirs/$fontdir --min_pct_ext 0.1
done
```

I can then run it on a given directory, such as `ofl` if I'm in my local `google/fonts` directory, and pipe errors into a text file:

```
add-gf ofl 2>> errors.txt
```

I am adding these errors to the [add-font-errors](/add-font-errors) directory of this repo.