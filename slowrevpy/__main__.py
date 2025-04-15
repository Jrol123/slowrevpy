import argparse as prs
import os.path
from .slowrevpy import slowrevpy

DEFAULT_SPEED_COEFFICIENT = 0.65
DEFAULT_FILE_FORMAT = "mp3"

parser = prs.ArgumentParser(
    prog="slowrevpy",
    description="Python module that helps creating slowed and reverbed audio",
    epilog="For the examples of how to use it check the repository: https://github.com/Jrol123/slowedreverb_main",
)
parser.add_argument("audio", type=str, help="destination")
parser.add_argument(
    "-s",
    "--speed",
    nargs="?",
    dest="speed_coefficient",
    type=float,
    default=DEFAULT_SPEED_COEFFICIENT,
    help="Speed coefficient",
)
parser.add_argument(
    "-o",
    "--output",
    nargs="?",
    dest="output_filename",
    type=str,
    default=None,
    help="Name of the output file(s)",
)
parser.add_argument(
    "-f",
    "--format",
    nargs="?",
    dest="file_format",
    type=str,
    default=DEFAULT_FILE_FORMAT,
    help="Format of the output file(s). Applies only when name is None",
)
# parser.add_argument('-s', dest='silent_mode', help='NoAdditionalInfo')


def __file_processing(
    filename: str,
    speed_coefficient: float,
    output_filename: str | None,
    ext_global: str,
):
    """
    Обработка файлов

    Args:
        filename (str): Название файла
        speed_coefficient (float): Коэффициент выходной скорости от исходной.
        output_filename (str | None): Выходное имя файла.
        ext_global (str): Формат файла
    """
    print(f"Now processing {filename}")

    if output_filename is None:
        ext = ext_global
        output_filename = (
            ".".join(filename.split("\\")[-1].split(".")[:-1])
            + "_slowedreverb_"
            + str(speed_coefficient)
            + "."
            + ext
        )
    else:
        ext = output_filename.split(".")[-1]
    print(f"Трэк будет сохранён в формате {ext} В файл {output_filename}")

    slowrevpy(filename, ext, output_filename, speed_coefficient)


def __dir_processing(dir: str, *args):
    """
    Обработка папок

    Args:
        dir (str): Путь к папке.
    """
    for item in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, item)):
            # При впихивании папки output_filename не работает.
            print("Processing: " + item)
            try:
                # TODO: Обрабатывать только муз файлы
                __file_processing(os.path.join(dir, item), *args)
            except Exception as e:
                print(f"Error happened while processing file {item}: \n" + str(e))
            finally:
                print("Done\n")
        else:
            __dir_processing(os.path.join(dir, item), *args)


def main_processing(
    audio_path: str,
    speed_coefficient: float = DEFAULT_SPEED_COEFFICIENT,
    output_filename: str = None,
    file_format: str = DEFAULT_FILE_FORMAT,
) -> None:
    """
    Обработчик объектов

    Обрабатывает сами музыкальные объекты и находящиеся внутри них файлы

    Args:
        audio_path (str): Путь к файлу или папке.
        speed_coefficient (float, optional): Коэффициент выходной скорости от исходной. Defaults to 0.65.
        output_filename (_type_, optional): Выходное имя файла. Не работает для папок. Defaults to None.
        file_format (str, optional): Формат выходного файла. Defaults to 'wav'.

    Returns:
        None: Сохраняет обработанные файлы рядом с их исходниками.
    """
    if os.path.isdir(audio_path):
        __dir_processing(audio_path, speed_coefficient, None, file_format)
    else:
        __file_processing(audio_path, speed_coefficient, output_filename, file_format)


# TODO: Добавить возможность кастомизировать реверберации
if __name__ == "__main__":
    args = parser.parse_args()
    main_processing(
        args.audio, args.speed_coefficient, args.output_filename, args.file_format
    )
