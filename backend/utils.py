import zipfile


def flatten(dct: dict, sub_dct_key_name: str, prefix: str = None) -> dict:
    """
    Сводит вложенный к невложенному по ключу sub_dct_key_name
    """
    prefix = prefix or f"{sub_dct_key_name}."
    sub_dct = dct.pop(sub_dct_key_name) or {}
    for k, v in sub_dct.items():
        dct[f"{prefix}{k}"] = v
    return dct


def unflatten(dct: dict, sub_dct_key_name: str, prefix: str = None) -> dict:
    prefix = prefix or f"{sub_dct_key_name}."
    new_dct = {sub_dct_key_name: {}}
    for k, v in dct.items():
        if k.startswith(prefix):
            new_k = k[len(prefix):]
            new_dct[sub_dct_key_name][new_k] = v
        else:
            new_dct[k] = v
    return new_dct


def unzip_file(file_path: str, dest_dir: str) -> None:
    """
    Разархивирует файл file_path в директорию dest_dir
    """
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(dest_dir)
