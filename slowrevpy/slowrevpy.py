import soundfile as sf
import subprocess
import platform
import sys
import os
import getpass
from pedalboard import Pedalboard, Reverb, Resample

# from pedalboard.io import get_supported_read_formats, AudioFile

# To check: https://github.com/asherchok/snr/blob/main/snr-generator.ipynb


start_bold = "\033[1m"
end_bold = "\033[0m"


def __check_ffmpeg():
    if not __is_ffmpeg_installed():
        __ffmpeg_noninstalled()


def __is_ffmpeg_installed():
    """Проверяет наличие FFmpeg в системе"""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def __print_command(command: list):
    """Выводит команду для пользователя перед выполнением"""
    print(f"{start_bold}Выполняется команда:{end_bold}")
    print(" ".join(command))
    # sys.stdout.flush()


def __check_choice(choice: str):
    if choice not in ("", "y", "yes"):
        return False
    return True


def __run_command(command: list, shell=False) -> bool:
    """Выполняет команду с выводом в реальном времени"""
    __print_command(command)
    try:
        return subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            shell=shell,
        ).returncode == 0
        # process = subprocess.Popen(
        #     command,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.STDOUT,
        #     universal_newlines=True,
        #     shell=shell,
        #     bufsize=1,
        #     check=True
        # )

        # # Выводим вывод команды в реальном времени
        # for line in process.stdout:
        #     print(line, end="")

        # process.wait()

    except Exception as e:
        print(f"\n\033[31mОшибка выполнения команды: {e}\033[0m")
        return False


def __install_ffmpeg_windows():
    """Установка FFmpeg для Windows"""
    print("\n\033[1mБудет выполнена следующая команда:\033[0m")
    print("winget install --id Gyan.FFmpeg -e --source winget\n")

    choice = (
        input(f"Продолжить установку? [{start_bold}Y{end_bold}/n]: ").strip().lower()
    )
    if not __check_choice(choice):
        return False

    return __run_command(
        ["winget", "install", "--id", "Gyan.FFmpeg", "-e", "--source", "winget"],
        shell=True,
    )


def __install_ffmpeg_linux():
    """Установка FFmpeg для Linux с подтверждением"""
    print("\n\033[1mДля установки FFmpeg потребуются права администратора\033[0m")
    print("Будут выполнены следующие команды:")
    print("1. sudo apt update - обновление списка пакетов")
    print("2. sudo apt install ffmpeg - установка FFmpeg\n")

    choice = (
        input(f"Продолжить установку? [{start_bold}Y{end_bold}/n]: ").strip().lower()
    )
    if not __check_choice(choice):
        return False

    # Проверка доступности sudo
    if __run_command(["sudo", "-n", "true"]) and getpass.getuser() != "root":
        print("\n\033[33mВнимание: Команды будут выполняться через sudo")
        print("При необходимости введите пароль при запросе\033[0m\n")

    success = True
    success &= __run_command(["sudo", "apt", "update"])
    success &= __run_command(["sudo", "apt", "install", "-y", "ffmpeg"])
    return success


def __ffmpeg_noninstalled():
    print("\nFFmpeg не найден в системе!")
    choice = (
        input(
            f"Хотите выполнить автоматическую установку? [{start_bold}Y{end_bold}/n]: "
        )
        .strip()
        .lower()
    )

    if not __check_choice(choice):
        print(
            "❌ FFmpeg необходим для конвертации выходных файлов в формат, отличный от .wav"
        )
        sys.exit(1)
    system = platform.system()
    try:
        if system == "Windows":
            __install_ffmpeg_windows()
        elif system == "Linux":
            __install_ffmpeg_linux()
        else:
            print("❌ Автоматическая установка для вашей ОС не поддерживается")
            sys.exit(1)

        # Повторная проверка после установки
        if __is_ffmpeg_installed():
            print("✅ FFmpeg успешно установлен")
        else:
            print("⚠️ Установка завершена, но FFmpeg не найден в PATH")
            print("Добавьте FFmpeg в переменные среды или перезапустите терминал")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Ошибка установки: {str(e)}")
        print("Установите FFmpeg вручную:")
        print("- Windows: winget install Gyan.FFmpeg")
        print("- Linux: sudo apt install ffmpeg")
        sys.exit(1)


def slowrevpy(audio: str, ext: str, output_filename: str, speed: float) -> None:
    """
    Замедляет и накладывает реверберации на аудиофайл

    Args:
        audio (str): Путь к аудиофайлу.
        ext (str): Расширение выходного файла.
        output_filename (str): Выходное имя файла + расширение.
        speed (float): Коэффициент выходной скорости от исходной.

    Returns:
        None: Генерирует замедленный аудиофайл с наложенными реверберациями.
        Сохранение происходит в корневой папке.

    """

    print("Импорт аудио...")
    audio, sample_rate = sf.read(audio)

    pedals = []

    sample_rate_2 = int(sample_rate * speed)

    print("Замедление аудио...")
    pedals.append(
        Resample(
            target_sample_rate=sample_rate_2, quality=Resample.Quality.WindowedSinc
        )
    )

    # speed = 0.85 & reverb = 0.10

    print("Добавление ревербераций...")
    pedals.append(Reverb(room_size=0.75, damping=0.5, wet_level=0.08, dry_level=0.2))
    board = Pedalboard(pedals)

    effected = board(audio, sample_rate)

    if ext != "wav":
        # Before exporting, convert to {ext} using ffmpeg
        from ffmpeg import FFmpeg

        __check_ffmpeg()

        tmp_dir = "tmp"
        os.makedirs(tmp_dir, exist_ok=True)
        temp_output = os.path.join(
            tmp_dir, f"temp_output_{output_filename}.wav"
        )  # Temporary WAV file

        print("Exporting temp audio as WAV...")
        sf.write(temp_output, effected, sample_rate_2)

        print(f"Конвертация аудио в {ext}...")
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(temp_output)
            .output(
                output_filename, acodec="libmp3lame", ar="44100", ac=2, ab="192k"
            )  #! Скорее всего, flac ломается из-за этих параметров
        )

        try:
            ffmpeg.execute()
        except Exception as e:
            print(
                f"Ошибка при обработке {output_filename} на стадии конвертации:\n"
                + str(e)
            )
            return
        # ffmpeg -i '.\07. Re Beautiful Morning _slowedreverb_0.65.wav' -vn -ar 44100 -ac 2 -b:a 192k output.mp3

        os.remove(temp_output)
    else:
        sf.write(output_filename, effected, sample_rate_2)

    print(f"Готово! Выходной файл: {output_filename}")
    print()
