import platform


def iswindows(path):
    os = platform.system()
    if os == 'Linux':
        return path
    if os == 'Windows':
        newpath = []
        for letter in path:
            if letter != '/':
                newpath.append(letter)
            else:
                newpath.append('\\')
        rpath = "".join(newpath)
        return rpath


if __name__ == "__main__":
    pass
