from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize
from threading import Thread


def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path):
    # Создаем папку для архивов
    target_folder.mkdir(exist_ok=True, parents=True)
    #  Создаем папку куда распаковываем архив
    # Берем суффикс у файла и убираем replace(filename.suffix, '')
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    #  создаем папку для архива с именем файла
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Обман - это не архив {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Не удалось удалить папку {folder}')


def main(folder: Path):
    # parser.scan(folder)
    tread_scan = Thread(target=parser.scan, args=(folder, ))
    tread_scan.start()
    tread_scan.join()

    # images

    for file in parser.JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')

    # audio

    for file in parser.MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in parser.OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in parser.WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in parser.AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')
    for file in parser.OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')

        # video

    for file in parser.AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in parser.MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in parser.MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in parser.MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')

    # documents

    for file in parser.DOC_FILES:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in parser.DOCX_FILES:
        handle_media(file, folder / 'documents' / 'DOCX')
    for file in parser.TXT_FILES:
        handle_media(file, folder / 'documents' / 'TXT')
    for file in parser.PDF_FILES:
        handle_media(file, folder / 'documents' / 'PDF')
    for file in parser.XLSX_FILES:
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in parser.PPT_FILES:
        handle_media(file, folder / 'documents' / 'PPT')
    for file in parser.PPTX_FILES:
        handle_media(file, folder / 'documents' / 'PPTX')

        # some other

    for file in parser.SOME:
        handle_other(file, folder / 'Unsorted')

    # archives

    for file in parser.ARCHIVES:
        thread_archive = Thread(target=handle_archive, args=(file, folder / 'archives'))
        thread_archive.start()


    # Выполняем реверс списка для того, чтобы все папки удалить.
    for folder in parser.FOLDERS[::-1]:
        thread_folder = Thread(target=handle_folder, args=(folder, ))
        thread_folder.start()
        thread_folder.join()


if __name__ == '__main__':
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())
