# (Slowed + Reverb)

Create slowed and reverb songs with python.

Fork of a now [unsupported project](https://github.com/JustCoww/slowedreverb)

## **Installation**

```shell
pip install slowrevpy
```

## **Dependencies**

### FFmpeg
For the conversions to formats, other that `.wav`, you would want to install ffmpeg

#### Auto install

You can use autoinstaller from the module, which whill automatically install ffmpeg for your OS.
When you will start to transform your audio, the module will automatically check if the ffmpeg is installed, and if not, then it will try to autoinstall it.

#### Manial install

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
