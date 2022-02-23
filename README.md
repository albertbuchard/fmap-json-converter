### JSON IntendedFor converter

Assumes the JSON files and the nii.gz files are in the same folder.

Clone the repository:
```bash
git clone https://github.com/albertbuchard/fmap-json-converter.git
```

To call the converter:
```
python main.py -d=<directory> -o=<output_directory>
```

If the output directory is not specified, the output will overwrite the files.
```
python main.py -d=<directory>
```

The directory is relative to the current working directory where the script is called.
You can also move the `main.py` script to a different directory if it is easier.