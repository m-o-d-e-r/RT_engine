from ..data_operations import Reader, AstReader, Writer
import re



class AstSyntax:
    PATTERNS = {
        "START_HTML_PATTERN": r"<[a-zA-Z-_'\"\s=]*>",
        "VAR_PATTERN": r"{{\s*\D[a-zA-Z]*\s*}}",
        "START_BLOCK_PATTERN": r"{%\s*\D[a-zA-Z0-9_]*\s*%}",
        "END_BLOCK_PATTERN": r"{%\s*end\s*\D[a-zA-Z_]*\s*%}",
        "END_HTML_PATTERN": r"</[a-zA-Z]*>"
    }


class AstNode:
    def __init__(self, value, close_value=None):
        self.value = value
        self.close_value = close_value
        self.child = []
    
    def add_child(self, chld):
        self.child.append(chld)

    def __repr__(self) -> str:
        return f"Parrent: {self.value}"


class AstQueue:
    def __init__(self):
        self.queue: list = []

    def push(self, item):
        self.queue.append(item)
        return item

    def pop(self):
        del self.queue[-1]
        return self.queue

    @property
    def get(self):
        return self.queue


class Ast:
    def __init__(self, tokens):
        self.__tokens = tokens
        self._current_parrent = None
        self._first_parrent = None
        self.__raw_wood_temp = None

        self.__queue = AstQueue()
        self.__queue_tree_item = AstQueue()

    def __generate_raw_wood(self):
        raw_wood = []

        for line in self.__tokens:
            line_temlates = []
            for key in AstSyntax.PATTERNS.keys():
                finded = re.findall(AstSyntax.PATTERNS[key], line)
                if finded:
                    line_temlates.append((finded, key))
            if line_temlates:
                raw_wood.append(line_temlates)

        return raw_wood

    def generate_tree(self, args):
        self.__raw_wood_temp = self.__generate_raw_wood()

        for wood in self.__raw_wood_temp:
            for item_wood in wood:
                for item in item_wood[0]:
                    if item_wood[1] == "START_HTML_PATTERN":
                        if self._first_parrent is None:
                            self._first_parrent = AstNode(item)
                            self._current_parrent = self._first_parrent
                            self.__queue.push(self._first_parrent)
                            self.__queue_tree_item.push(self._first_parrent.value)
                        else:
                            new_node = AstNode(item)
                            self._current_parrent.add_child(new_node)
                            self._current_parrent = new_node
                            self.__queue.push(new_node)
                            self.__queue_tree_item.push(new_node.value)
                    elif item_wood[1] == "VAR_PATTERN":
                        self.__queue_tree_item.push(args["".join(re.findall(r"[a-zA-Z_]*", item))])
                    elif item_wood[1] == "END_HTML_PATTERN":
                        self._current_parrent.close_value = item
                        self.__queue_tree_item.push(item)

                        self.__queue.pop()
                        try:
                            self._current_parrent = self.__queue.get[-1]
                        except:
                            pass


        return (self._first_parrent, self.__queue_tree_item, self.__raw_wood_temp)


class AstTemplate:
    def __init__(self, path, **kwargs):
        html_data = Reader(path)
        main_ast = Ast(html_data.tokens)
        ast_reader = AstReader(main_ast.generate_tree(kwargs))

        ast_reader.show_tabs(main_ast._first_parrent)

        print()
        print("\n\t\tStack:\t", ast_reader.tabs_stack)
        print("="*100)
#        print(ast_reader.show())
#        print()
#        print(main_ast._first_parrent.value, main_ast._first_parrent.close_value)


        Writer(main_ast._first_parrent, ast_reader.show(), ast_reader.tabs_stack)
