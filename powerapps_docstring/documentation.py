import os
from mdutils.mdutils import MdUtils
from powerapps_docstring.parser import Parser

# https://mdutils.readthedocs.io/en/latest/examples/Example_Python.html


class Docstring():
    def __init__(self, source, output, config) -> None:
        self.source_path = source
        self.output_path = output
        self.parser = Parser(self.source_path)
        self.config = config
        self.relevant_objects = self.config["RelevantObjects"]
        self.relevant_object_keys = [f" As {x}" for x in self.relevant_objects.keys()]

    def _extract_parts_from_propperty(self, propperty) -> tuple:
        """Extracts the parts from a propperty.

        Parts can be:
        - docstring
        - function

        Args:
            propperty (str): The string representation of the propperty

        Returns:
            tuple: bool for contains docstring, docstring, function
        """
        print(propperty[:3])
        if propperty[:3] == "=/*":
            start = propperty.find("/*") + len("/*")
            end = propperty.find("*/")
            docstring = propperty[start:end]
            func = propperty[end+2:]
            return True, docstring, func.strip()
        else:
            return False, None, propperty[1:]

    def _extract_screen_content_to_markdown(self, screen_objects) -> None:
        self.md_file.new_header(level=2, title=screen_objects[0])
        self.md_file.new_line("---")

        def _recursive(key, value):
            # check for object
            rel_obj_key = None

            for rel_obj in self.relevant_objects.keys():
                if f" As {rel_obj}" in key:
                    rel_obj_key = rel_obj
                    break

            if rel_obj_key != None:
                # we found a header
                self.md_file.new_header(level=3, title=key)

                for sub_dict_key, sub_dict_item in value.items():
                    if sub_dict_key in self.relevant_objects.get(rel_obj_key):
                        self.md_file.new_header(level=4, title=sub_dict_key)
                        self.md_file.insert_code(str(sub_dict_item))

                    elif type(sub_dict_item) == dict:
                        # we found another dict so start over
                        for new_key, new_value in sub_dict_item.items():
                            _recursive(new_key, new_value)

        for key, value in screen_objects[1].items():
            _recursive(key, value)

    
    def create_documentation(self, format=None):
        if format == None:
            self.format = "markdown"
        else:
            self.format = format

        # instantiate the md file
        # TODO: get title from docstring variable
        app_name = self.parser.get_app_name()
        self.md_file = MdUtils(file_name=self.output_path +
                          f'/{app_name}-doc', title='Power App Documentation')

        # # APP # #
        # get contents from App.fx.yaml
        app_screen = self.parser.get_screen_objects("App.fx.yaml")
        on_start = app_screen[1]["App As appinfo"].get("OnStart")

        # create heading for app info
        self.md_file.new_line("")
        self.md_file.new_line("")
        self.md_file.new_header(level=1, title=app_name)
        # write app info
        if on_start != None:
            appinfo = self._extract_parts_from_propperty(on_start)
            self.md_file.new_paragraph(appinfo[1], )
            self.md_file.new_line("")
            self.md_file.new_header(level=2, title="OnStart")
            self.md_file.insert_code(appinfo[2])
            
        # # Connections # #
        # writing connections header
        self.md_file.new_header(level=1, title="Connections")
        connections = self.parser.get_connections()
        if len(connections) > 0:
            for connection in connections.items():

                self.md_file.new_line(connection[1]["connectionRef"]["displayName"] +
                                 f" ({connection[1]['connectionRef']['apiTier']})", "b")    # Header
                self.md_file.new_line("")

                for parameter in connection[1]["connectionParameters"].items():
                    self.md_file.new_line(f"{parameter[0]}: {parameter[1]}")
                
                self.md_file.new_line("")
                self.md_file.new_line("With following datasources:")
                self.md_file.new_line("")
                self.md_file.new_list([x for x in connection[1]["dataSources"]])
                self.md_file.new_line("")

        # # Screen # #
        self.md_file.new_header(level=1, title="Screens")
        # TODO: add screenflow visualization

        # loop thru all screens and create markdown
        screens_path = self.source_path + "/Src/"
        for file in os.listdir(screens_path):
            if os.path.isfile(screens_path + file) & file.endswith(".yaml"):
                if file != "App.fx.yaml":
                    screen_objects = self.parser.get_screen_objects(file)
                    self._extract_screen_content_to_markdown(screen_objects)
        
        # write toc + file
        self.md_file.new_table_of_contents(table_title='Contents', depth=2)
        self.md_file.create_md_file()
