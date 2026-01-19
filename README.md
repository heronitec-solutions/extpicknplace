# KiPart  

This [KiCad EDA](https://www.kicad.org/) plugin extends the fabrication ouput for pick and place machines.

## Installation

### Automated, via KiCad plugin manager

The KiPart plugin is part of the official KiCad repository. You can install it via the Plugin an Content Manager in KiCad.

The get updates early use the Heronitec Solutions Plugin repository: ```https://kicad.heronitec-solutions.de/repository.json```

### Manual, most current version

To get the most current version of the plugin, clone the repo in the plugin directory of your KiCad installtion:

```bash
# Linux (KiCad from Ubuntu PPA)
# TODO
# Linux (KiCad 9 from FlatPak)
cd <HOME>/.var/app/org.kicad.KiCad/data/kicad/9.0/3rdparty/plugins
# Windows
cd C:\Users\<USERNAME>\Documents\KiCad\9.0\3rdparty\plugins
# Mac
cd <HOME>/Documents/KiCad/9.0/3rdparty/plugins

# then clone the repo main branch
git clone --depth 1 https://github.com/heronitec-solutions/extpicknplace
```

Restart KiCad and it should be visiable.

## Manual, latest stable release

Same as above, but instead cloning the main branch, clone the realease branch:

```bash
# clone the repo tag
git clone --depth 1 --branch release https://github.com/heronitec-solutions/extpicknplace
```

### Manual, older version

Same as above, but instead cloning the main branch, clone the desired tag:

```bash
# clone the repo tag
git clone --depth 1 --branch v1.6.0 https://github.com/heronitec-solutions/extpicknplace
```
