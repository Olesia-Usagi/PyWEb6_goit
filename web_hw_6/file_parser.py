import sys
from pathlib import Path

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_FILES = []
DOCX_FILES = []
TXT_FILES = []
PDF_FILES = []
XLSX_FILES = []
PPT_FILES = []
PPTX_FILES = []
SOME = []
ARCHIVES = []

REGISTER_EXTENSIONS = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'DOC': DOC_FILES,
    'DOCX': DOCX_FILES,
    'TXT': TXT_FILES,
    'PDF': PDF_FILES,
    'XLSX': XLSX_FILES,
    'PPT': PPT_FILES,
    'PPTX': PPTX_FILES,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extention(filename: str) -> str:
    # Перетворюємо розширення файлу на назву файлу
    return Path(filename).suffix[1:].upper()


async def scan(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_dir():
            # перевіряємо щоб папка не була тією в яку ми скидаємо вже файли
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'some'):
                FOLDERS.append(item)
                # рекурсія
                await scan(item)
            continue

        # Работа з файлом
        ext = get_extention(item.name)  # взяти розширення
        fullname = folder / item.name  # повний шлях файлу
        if not ext:  # нема розширення - до невідомого
            SOME.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSIONS[ext]
                EXTENSIONS.add(ext)
                container.append(fullname)
            except KeyError:
                # Якщо не в REGISTER_EXTENSIONS, то додати в Other
                UNKNOWN.add(ext)
                SOME.append(fullname)


if __name__ == '__main__':
    folder_for_scan = sys.argv[1]
    print(f'Start in folder {folder_for_scan}')

    scan(Path(folder_for_scan))
    print(f'Images jpeg: {JPEG_IMAGES}')
    print(f'Images jpg: {JPG_IMAGES}')
    print(f'Images svg: {SVG_IMAGES}')
    print(f'Audio mp3: {MP3_AUDIO}')
    print(f'Archives: {ARCHIVES}')

    print(f'Types of files in folder: {EXTENSIONS}')
    print(f'Unknown files of types: {UNKNOWN}')

    print(FOLDERS[::-1])
