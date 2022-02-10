

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
        self.__count_of_stack_framess = 20
        self.__current_indent = 4
        self.new_str_stack = []

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
        for child_item in parrent[0 : -1]:
            for item_frame in child_item.child:
                child_datas.append(item_frame)
        self.__current_indent += 4

        child_datas.append(self.__current_indent)
        self.tabs_stack.append(child_datas)

        if self.__count_of_stack_framess > 0:
            self.tabs_child(child_datas)

    def show_tabs(self, layer=None, data_stack=None):
        self.__count_of_stack_framess -= 1

        new_layer: list = []
        for child_item in layer.child:
            new_layer.append(child_item)

        new_layer.append(self.__current_indent)

        self.tabs_stack.append(new_layer)
        self.tabs_child(new_layer)


class Writer:
    def __init__(self, ast, tabs_stack):
        self.__main_ast = ast
        self.write(self.__main_ast, tabs_stack)

    def write(self, ast, tabs_stack):
        file_ = open("test.html", "w")
        file_.write("<!DOCTYPE html>\n<html>\n")

#        print(ast._html_stack)
#        print()
#        print(tabs_stack)

        for html_item in ast._html_stack:
            for tab_frame in tabs_stack:
                if len(tab_frame) == 0:
                    break
                for tab_item in tab_frame[0 : -1]:
                    try:
                        if html_item[1] == tab_item.id:
                            if "{{" in html_item[0]:
                                data = ast._variables.get(tab_item.id)
                                if data:
                                    file_.write(f"{' '*tab_frame[-1]}{data}\n")
                                    ast._variables.pop(tab_item.id)
                                    break
                            file_.write(f"{' '*tab_frame[-1]}{html_item[0]}\n")
                            break
                        elif html_item[1] == tab_item.close_id:
                            file_.write(f"{' '*tab_frame[-1]}{html_item[0]}\n")
                            break
                    except:
                        ...


        file_.write("</html>\n")

        file_.close()
