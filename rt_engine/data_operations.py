

from re import S


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

        self.tabs_stack: list = []
        self.__count_of_stack_framess = 10
        self.__current_indent = 4

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

    def tabs_child(self, parrent):
        self.__count_of_stack_framess -= 1

        child_datas = []
        for child_item in parrent:
            for item_frame in child_item.child:
                child_datas.append(item_frame)

        self.__current_indent += 4
        self.tabs_stack.append([child_datas, self.__current_indent])

        if self.__count_of_stack_framess > 0:
            self.tabs_child(child_datas)

    def show_tabs(self, layer=None):
        self.__count_of_stack_framess -= 1

        new_layer: list = []
        for child_item in layer.child:
            new_layer.append(child_item)
        
        self.tabs_stack.append([new_layer, self.__current_indent])
        self.tabs_child(new_layer)


class Writer:
    def __init__(self, first_parrent, data, tabs_stack):
        self.write(first_parrent, data, tabs_stack)

    def write(self, first_parrent, data, tabs_stack):
        file_ = open("test.html", "w")

        file_.write("<!DOCTYPE html>\n<html>\n")


        for html_item in data:
            for html_frame in tabs_stack:
                is_break = False
                for frame in html_frame[0]:
                    if html_item == frame.value:
                        file_.write(f"{' '*html_frame[1]}{html_item}\n")

                        is_break = True
                        break
                    elif html_item == frame.close_value:
                        file_.write(f"{' '*html_frame[1]}{html_item}\n")

                        is_break = True
                        break
                if is_break:
                    break

        file_.write("</html>\n")

        file_.close()
