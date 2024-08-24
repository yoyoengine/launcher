# yoyoengine hub

The hub is a proposed central manager of yoyoengine versions.

## Usage

The hub will provide a gui to see and manage yoyoeditor installs.

Each yoyoeditor install has its own folder in a managed location, and its own list of projects to sandbox and seperate projects across your versions.

## Distribution

The hub will be built by pyinstaller, and distributed as a single executable file.

## Considerations

- add version tracking into the yoyoengine projects themselves
- add concrete version checking functions into editor (build X.X)

## Development

Build final output:

```bash
pyinstaller --onefile --collect-data sv_ttk src/main.py
```

## stipulations

yoyoeditor build releases are expected to have a yoyoeditor**.tar.gz file in the assets, which is what should be actually installed into the new directory.

yoyoeditor builds are not nested in a subdir, if you extract, yoyoeditor is at the root

## todo

add settings page to cleanup all installs
some kinda menu that shows during install, uninstall to show progress
maybe replace the hub update available since its trash
add github cicd to build hub
