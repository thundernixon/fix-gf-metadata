# Metadata differences

Running `gftools add-font` on the entire google/fonts collection results in changes to more than just subset metadata. In this document, I'll make notes of what other metadata has been affected, by looking at Git diffs.

## Script

I've used `check-diffs.py` to compile a list of all the git diffs from running `gftools add-font` on all fonts. This has not only compiled a handy list of all the changes, but in turn, this has *also* helped me to see what differences have been made.

## Differences

Basically all differences are to font names, copyright strings, and (as hoped for) subsets.

- URLs (e.g. in Copyright strings) are now unescaped with `\r`
- Designer Names
  - Protobuf is forming non-ASCII characters with unicodes, so what was "Huerta Tipogr\xc3\xa1fica" is now "Huerta Tipogr\\303\\241fica"
- Font Names
  - camelcased names like ABeeZee and KoHo have gained incorrect spaces (not great)
  - some names gained "Regular" in their `full_name`, like Cabin or librebarcode39extended
- Copyrights
  - Quite a few copyright strings have had updates, like emails being replaced with just URLs (e.g. `www.impallari.com impallari@gmail.com` is now just `www.impallari.com`). I'm not sure exactly why ... probably, these were formerly made by hand, and are now being generated from the font files. 
- Subsets
  - "latin-ext" has been added to many fonts
  - the "menu" subset has changed to the last-listed subset

**Other changes**
  - adobe blank has incorrectly had the designer and category changed to defaults (I had deleted its former metadata file before running add-font)


## Suspect updates

**Escaping issues in copyright strings:**
```
alikeangular
    '-  copyright: "Copyright (c) 2011, Cyreal (www.cyreal.org) with Reserved Font Name \\"Alike\\" and \\"Alike Angular\\"."'
    '+  copyright: "Copyright (c) 2011, Cyreal (www.cyreal.org)\\rwith Reserved Font Name \\"Alike\\" and \\"Alike Angular\\"."'
```

```
amiri
    '-  copyright: "Copyright (c) 2010-2016, Khaled Hosny <khaledhosny@eglug.org>. Portions copyright (c) 2010, Sebastian Kosch <sebastian@aldusleaf.org>."'
    '+  copyright: "Copyright (c) 2010-2016, Khaled Hosny <khaledhosny@eglug.org>.\\nPortions copyright (c) 2010, Sebastian Kosch <sebastian@aldusleaf.org>."'
```

```
antonio
    '-  copyright: "Copyright (c) 2011-12, vernon adams (vern@newtypography.co.uk), with Reserved Font Names \'Antonio\'"'
    '+  copyright: "Copyright (c) 2011-12, vernon adams (vern@newtypography.co.uk), with Reserved Font Names \\\'Antonio\\\'"'
```

```
blackopsone
    '-  copyright: "Copyright (c) 2011-2012, Sorkin Type Co (www.sorkintype.com) with Reserved Font Names \\"Black Ops\\" and \\"Black Ops One\\"."'
    '+  copyright: "Copyright (c) 2011-2012, Sorkin Type Co (www.sorkintype.com)\\rwith Reserved Font Names \\"Black Ops\\" and \\"Black Ops One\\"."'
```

```
    '+  copyright: "Copyright (c) 2011, Sorkin Type Co. (www.sorkintype.com)\\rwith Reserved Font Name \\"Hammersmith\\".\\r\\rThis Font Software is licensed under the SIL Open Font License,\\rVersion 1.1. This license is available with a FAQ at:\\rhttp://scripts.sil.org/OFL"'
```

```
    '-  copyright: "Copyright (c) 2004 Alejandro Paul (sudtipos@sudtipos.com), with Reserved Font Name \\"Herr Von Mullerhoff\\""'
    '+  copyright: "Copyright (c) 2004 Alejandro Paul (sudtipos@sudtipos.com),\\rwith Reserved Font Name \\"Herr Von Mullerhoff\\""'
```

(There are lots more in the diff logs).

**Should "Mathieu Reguer" lack diacritics in the copyright string?**

```
biryani
    '-designer: "Dan Reynolds, Mathieu R\xc3\xa9guer"'
    '+designer: "Dan Reynolds, Mathieu R\\303\\251guer"'
    '-  copyright: "Copyright (c) 2015 Dan Reynolds. Copyright (c) 2015 Mathieu R\xc3\xa9guer."'
    '+  copyright: "Copyright (c) 2015 Dan Reynolds. Copyright (c) 2015 Mathieu Reguer"'
```



**Is it okay (or good?) if `cyrillic-ext` subset is added?**
```
baumans
    '+subsets: "cyrillic-ext"'
```

Should Gamja have lost its Korean subset?
```
gamjaflower
    '-subsets: "korean"'
    '+subsets: "latin-ext"'
```

## Next Steps
- [ ] start with fresh batch of fonts repo, then re-build metadata files (without deleting any, first)
- [ ] re-run diff checks
- [ ] check into suspect updates
- [ ] check with Marc on a few suspect updates if they aren't clearly good or bad
- [ ] (maybe) find a way to render the copyright strings (containing `+  copyright` in the diffs), to tell more easily what escapes are good/bad
- [ ] find way to get a specific read on percentages met by certain subsets (e.g. how much korean is in Gamja Flower?)
- [ ] find list of known camel-cased names (in FontBakery?) and correct those in add-font, or at least in the metadata

