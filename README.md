# (Slowed + Reverb)

Create slowed and reverb songs with python.

Fork of a now [unsupported project](https://github.com/JustCoww/slowedreverb)

## **Installation**

```shell
pip install slowrevpy
```

## **Dependencies**

For the conversions to formats, other that wav, you would want to install ffmpeg

For windows:

```powershell
winget install ffmpeg
```

For Linux:

```shell
sudo apt-get install ffmpeg
```

## Usage

It's possible to use this package on files and folders.

```shell
python -m slowrevpy -f <file-format | default: mp3>  -s <speed-coefficient | default: 0.65> -o <output-filename | works only if you select a single file> <path to audiofile>
```

## Known problem

- Impossible to convert to `.flac` format
