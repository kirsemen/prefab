copy_path = "мессанджер_vt/test/copy_file.py"
paste_path = "мессанджер_vt/test/servers/{}/main.py"
def copy(name: str):
    _paste_path = paste_path.format(name)
    mes = {}
    try:
        open(_paste_path)
        mes["answer"] = "server is already done"
    except:
        paste_file = open(_paste_path, "w")
        copy_file_text = open(copy_path).read()
        paste_file.write(copy_file_text)
        paste_file.close()
        mes["answer"] = "server made"
    return mes

