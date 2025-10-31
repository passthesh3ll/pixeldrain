# Pixeldrain
![image](https://i.postimg.cc/50y4ydnf/image.png)

A python Pixeldrain client. You can upload files or entire folders to Pixeldrain (using your api), providing a simple command-line interface with progress tracking and optional logging of download links.

## Dependencies

- `requests`
- `requests_toolbelt`
- `tqdm`
- `colorama`

```bash
pip install requests requests-toolbelt tqdm colorama
```

## Example

Upload a file:

```bash
python pixeldrain.py /path/to/file.txt --api-key <API-KEY>
```

Upload a folder:

```bash
python pixeldrain.py /path/to/dir/ --api-key <API-KEY>
```
![image](https://i.postimg.cc/J0dB05NC/2.png)

## Help

```bash
usage: pixeldrain.py [-h] [--log] --api-key API_KEY path

Upload files or folders to Pixeldrain

positional arguments:
  path               Path to the file or folder to upload

options:
  -h, --help         show this help message and exit
  --log              Save upload links to individual <filename>_links.txt files
  --api-key API_KEY  Pixeldrain API key
```


