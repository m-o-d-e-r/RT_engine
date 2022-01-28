

class Reader:
    def __init__(self, path: str):
        self.__data = ""
        with open(path, "r") as file_:
            self.__data = file_.read()

    @property
    def tokens(self):
        return self.__data.split("\n")


class AstReader:
    def __init__(self, ast: str):
        self.__ast = ast
        self.__tree = []

    def __return_child(self, parrent):
        for child in parrent.child:
            self.__tree.append(child.value)
            self.__return_child(child)

    def show(self):
        self.__tree.append(self.__ast[0].value)
        for parrent in self.__ast[0].child:
            self.__tree.append(parrent.value)
            self.__return_child(parrent)

        return self.__ast[1].queue


class Writer:
    def __init__(self, data):
        self.__data = data
    
    def write(self):
        with open("test.html", "a") as file_:
            file_.write("<!DOCTYPE html>\n")
            for item in self.__data:
                file_.write(item + "\n")
