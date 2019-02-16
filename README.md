# Notes on fixing the metadata in the google/fonts repo

In trying to address the Google Fonts issue [Check all families that have latin-ext glyphs enable it](https://github.com/google/fonts/issues/187), it is necessary to check all fonts in the [google/fonts repo](https://github.com/google/fonts) for the presence of glyphs considered to be in the [`latin-ext` glyphset](https://github.com/googlefonts/gftools/blob/master/Lib/gftools/encodings/latin-ext_unique-glyphs.nam). 

This is a bigger project than it may seem at first, in that it involves about 1,000 fonts across a diverse range of languages, genres, and complexity. Luckily, there are existing tools that will help, but these are not perfect.

In order to work through this methodically, I will use this repo to store working notes, existing error logs, and other data that comes up.

## Process

**Basic Plan**
1. verify that `gftools add-font` accurately labels subsets – assigning `latin-ext` when any `latin-ext` characters are present in a font
2. run `gftools add-font` on every folder in the google/fonts repo. 
3. Make a PR with the changed `METADATA.pb` files

My assumption is that if we run `gftools add-font` on all families in the google/fonts repo, it will not only will their subset labels be updated, but (hopefully) all of their other metadata will be improved, as well.

### Modifying gftools to apply `latin-ext` label at a lower bar

Based on `gftools-add-font.py` at line 65, it appears that fonts currently must have at least 10% of an `ext` glyphset in order to be labeled with that subset:

```
    flags.DEFINE_integer('min_pct_ext', 10,
                         'What percentage of subset codepoints have to be supported'
                         ' for a -ext subset.')
```

However, based on Dave’s response to my question, this is incorrect.

Me:

> Are you saying that the `latin-ext` subset should be enabled if there are any characters inside that range?

Dave:

> Yes

Based on this, I think that the flag should be set as low as possible without causing an error. I’ll try setting it to `0.01` (Currently, latin-ext_unique-glyphs.nam contains 810 glyphs, so 0.01% (1 in 10,000) is low enough that even a single glyph will be qualifying (and leaves plenty of room in case we ever decide that `latin-ext` should be a significantly larger category). Of course, `0.1` isn’t an integer, so this may break the check. …aaand sure enough, when I run `add-font` I get this:


```
    absl.flags._exceptions.IllegalFlagValueError: flag --min_pct_ext=0.1: Expect argument to be a string or int, found <class 'float'>
```

However, when I update the type in the flag, it works!

gftools-add-font.py, line 65

```
    flags.DEFINE_float('min_pct_ext', 0.01,
```

This is better than editing line 121 to not pass in any argument for `min_pct_ext`, because `SubsetsInFont()` (lines 382–416 of gftools/Lib/gftools/util/google_fonts.py) will default the arg to `None`, and it will not check for this subset or apply this label.



### Looping add-font through font directories in bulk, and saving the errors

I've made the following bash script to run `gftools add-font` to all directories of a directory that is passed in. Then, I've added it to the `bin` directory of my virtual environment. (The venv I'm using is in a central location, rather than in my local google/fonts directory, as I don't want to add any code there).

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

### Pip installing latest protobuf to handle non-ASCII characters in metadata

Initially, protobuf was getting hung up on non-ASCII characters in metadata. This was resolved by updating to the latest, pre-release version with:

```
pip install protobuf==3.7.0rc2
```

## Results so far

The current errors being logged in this method are saved in the [add-font-errors](/add-font-errors) directory of this repo.

There are a bunch of errors like `no cp file for batak found at /batak_unique-glyphs.nam` for most font families.

It is also tripping on VF fonts.

These errors are making me question whether `add-font` is really the best way forward, or if I should make a tool to _only_ check the glyph set and add the `latin-ext` label if needed. If I go in this route, I would basically duplicate the `add-font` script, but gut it to only apply the `latin-ext` subset if needed. This might be slightly faster, but would basically only really be a one-time gain.

I want to talk to Dave, Felipe, and Marc to ask what they recommend.

## Possible next steps

If I do move forward using `add-font` to generate this metadata, I'll need to make improvements to it.

PR `add-font` to:
- [ ] prevent issue of `no cp file for...` errors
- [ ] correctly take the designer name from font nameID 8 or 9
- [ ] handle exceptional font names, probably by getting them from font nameIDs 16 or 1, minus the possible style name
- [ ] handle VF names


---

As suggested by Marc, I will test out [modifying add-font to check nameIDs for better font names](https://github.com/googlefonts/gftools/issues/122#issuecomment-463562083), rather than parsing file names:
```
nametable = font['name']

family_name = None
typographic_name = nametable.getName(16, 3, 1, 1033)
if typographic_name:
    family_name = typographic_name.toUnicode()
else:
    family_name = nametable.getName(1, 3, 1, 1033).toUnicode()
```