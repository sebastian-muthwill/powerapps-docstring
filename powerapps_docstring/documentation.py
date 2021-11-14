import os
import re
from mdutils.mdutils import MdUtils
from powerapps_docstring.parser import Parser

# https://mdutils.readthedocs.io/en/latest/examples/Example_Python.html


class Docstring():
    def __init__(self, source, output, config) -> None:
        self.source_path = os.path.normpath(source)
        self.output_path = os.path.normpath(output)
        self.parser = Parser(self.source_path)
        self.config = config
        self.manifest_file = self.parser.get_canvas_manifest()
        self.relevant_objects = self.config["RelevantObjects"]
        self.relevant_object_keys = [f" As {x}" for x in self.relevant_objects.keys()]

    def _get_screen_files(self):
        screen_files = []
        screens_path = os.path.join(self.source_path, "Src")

        # read screen order from manifest and check if files exists
        screen_order = self.manifest_file["ScreenOrder"]
        for screen in screen_order:
            screen_file_name = screen + ".fx.yaml"
            if screen_file_name in os.listdir(screens_path):
                if screen_file_name != "App.fx.yaml":
                    screen_files.append(screen_file_name)
        
        return screen_files

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
        if propperty.startswith("=/*"):
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
        
        # add variables to screen if enabled in config
        if self.config["ScreenFlow"]["ShowVariables"]:
            # find variable with regex pattern
            global_variables = re.findall(r"Set\((.[^,]*)", str(screen_objects[1]))
            global_variables = list(set(global_variables))
            self.md_file.new_header(level=3, title="Global variables")
            self.md_file.new_line("Following variables have been created / or updated on this screen")
            self.md_file.new_list(global_variables)
            

        def _recursive(key, value):
            # check for object
            rel_obj_key = None

            for rel_obj in self.relevant_objects.keys():
                if f" As {rel_obj}" in key:
                    rel_obj_key = rel_obj
                    break

            # key is header
            if rel_obj_key != None:
                # we found a header
                self.md_file.new_header(level=3, title=key)

                # check if value has content (deals with blank screens)
                if not value:
                    return

                for sub_dict_key, sub_dict_item in value.items():
                    if sub_dict_key in self.relevant_objects.get(rel_obj_key):
                        if sub_dict_key == "OnVisible":
                            screen_docstring = self._extract_parts_from_propperty(sub_dict_item)
                            # check if docstring exists then add screen docstring
                            if screen_docstring[0]:
                                self.md_file.new_paragraph(screen_docstring[1])
                                sub_dict_item = screen_docstring[2]
                        if sub_dict_item != "":
                            self.md_file.new_header(level=4, title=sub_dict_key)
                            self.md_file.insert_code(str(sub_dict_item))

                    elif type(sub_dict_item) == dict:
                        # we found another dict so start over
                        for new_key, new_value in sub_dict_item.items():
                            _recursive(new_key, new_value)

        for key, value in screen_objects[1].items():
            _recursive(key, value)

    def _create_mermaid_screenflow(self):

        # from https://stackoverflow.com/a/20254842
        def get_recursively(search_dict, field):
            """
            Takes a dict with nested lists and dicts,
            and searches all dicts for a key of the field
            provided.
            """
            fields_found = []

            for key, value in search_dict.items():

                if key == field:
                    fields_found.append(value)

                elif isinstance(value, dict):
                    results = get_recursively(value, field)
                    for result in results:
                        fields_found.append(result)

                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            more_results = get_recursively(item, field)
                            for another_result in more_results:
                                fields_found.append(another_result)

            return fields_found

        # create header for mermaid graph
        screenflow_list = [self.config["MermaidPrefix"]]
        screenflow_list.append("graph LR")

        screen_files = self._get_screen_files()

        for screen in screen_files:
            # check if screen has been excluded
            if screen.replace(".fx.yaml", "") not in self.config["ScreenFlow"]["ExcludeScreens"]:
                screen_obj = self.parser.get_screen_objects(screen)
                from_screen = screen_obj[0]
                list_of_onselects = get_recursively(screen_obj[1], "OnSelect")

                for item in list_of_onselects:
                    if "Navigate(" in item:

                        item = item.strip().replace("\n", "").replace("\t", "")
                        navigate_occurences = [m.start() for m in re.finditer('Navigate\(', item)]

                        for occurence in navigate_occurences:
                            #print(occurence)
                            start = occurence + len("Navigate(")
                            #print(start)
                            end = item[start:].find(",")
                            if end == -1:
                                end = item[start:].find(")")
                            end = end + start
                            to_screen = item[start:end]
                            to_screen = to_screen.replace("\n", "").replace("\t", "").replace(")", "").replace("'", "")
                            if to_screen != None and to_screen != "" and not to_screen.startswith("[@") and to_screen not in self.config["ScreenFlow"]["ExcludeScreens"]:
                                screenflow_list.append(
                                            "".join(from_screen.split()) + "(" + from_screen + ")" + 
                                            " --> " + 
                                            "".join(to_screen.split()) + "(" + to_screen + ")"
                                            )
                
        screenflow_list.append(self.config["MermaidSuffix"])

        # to avoid double entrys in the graph
        # the doubled items are removed by convertig to dict and back to list
        screenflow_list = list(dict.fromkeys(screenflow_list))

        return screenflow_list  #"\n".join(screenflow_list)

    def _create_chapter_app(self, app_name):
        # # APP # #
        # get contents from App.fx.yaml
        app_screen = self.parser.get_screen_objects("App.fx.yaml")
        
        # read StartScreen and OnStart propperties from App
        start_screen = app_screen[1]["App As appinfo"].get("StartScreen")
        on_start = app_screen[1]["App As appinfo"].get("OnStart")
        
        # create heading for app info
        self.md_file.new_line("")
        self.md_file.new_line("")
        self.md_file.new_header(level=1, title=app_name)
        
        # write app info
        if start_screen != None:
            appinfo = self._extract_parts_from_propperty(start_screen)
            self.md_file.new_line("")
            self.md_file.new_header(level=2, title="StartScreen")
            self.md_file.insert_code(appinfo[2],language='typescript')
            self.md_file.new_line("")
        
        if on_start != None:
            appinfo = self._extract_parts_from_propperty(on_start)
            if appinfo[1] != None:
                self.md_file.new_paragraph(appinfo[1])
            self.md_file.new_line("")
            self.md_file.new_header(level=2, title="OnStart")
            self.md_file.insert_code(appinfo[2])

    
    def _create_chapter_connections(self):
        # # Connections # #
        # writing connections header
        self.md_file.new_header(level=1, title="Connections")
        connections = self.parser.get_connections()
        if len(connections) > 0:
            for connection in connections.items():
                # not all connections have an apiTier
                try:
                    api_tier = f" ({connection[1]['connectionRef']['apiTier']})"
                except KeyError:
                    api_tier = ""

                self.md_file.new_line(connection[1]["connectionRef"]["displayName"] +
                                 api_tier, "b")    # Header
                self.md_file.new_line("")

                for parameter in connection[1]["connectionParameters"].items():
                    self.md_file.new_line(f"{parameter[0]}: {parameter[1]}")
                
                self.md_file.new_line("")
                self.md_file.new_line("With following datasources:")
                self.md_file.new_line("")
                self.md_file.new_list([x for x in connection[1]["dataSources"]])
                self.md_file.new_line("")


    def _create_chapter_screens(self):
        # # Screen # #
        self.md_file.new_header(level=1, title="Screens")
        # TODO: add screenflow visualization

        #self.md_file.new_paragraph(self._create_mermaid_screenflow())
        for scr_flow in self._create_mermaid_screenflow():
            self.md_file.new_line(scr_flow)

        # loop thru all screens and create markdown
        for file in self._get_screen_files():
            screen_objects = self.parser.get_screen_objects(file)
            self._extract_screen_content_to_markdown(screen_objects)
            
    
    def _create_global_variables(self):
        screen_set_variables = {}
        screen_use_variables = {}
        
        for file in self._get_screen_files():
            # check on which screen variables are set
            screen_objects = self.parser.get_screen_objects(file)
            global_variables_on_screen = re.findall(r"Set\((.[^,]*)", str(screen_objects[1]))
            global_variables_on_screen = list(set(global_variables_on_screen))
            screen_set_variables[screen_objects[0]] = global_variables_on_screen    

        # get all set global variables
        all_global_variables = [item for sublist in screen_set_variables.values() for item in sublist]
        all_global_variables = list(set(all_global_variables))
        
        for file in self._get_screen_files():
            screen_objects = self.parser.get_screen_objects(file)
            used_variables_on_screen = []
            
            # check if variables are used on this screen
            for variable in all_global_variables:
                used_variables_on_screen = used_variables_on_screen + re.findall(f"(?<!Set\(){variable}", str(screen_objects[1]))
            
            # remove duplicates
            used_variables_on_screen = list(set(used_variables_on_screen))
            screen_use_variables[screen_objects[0]] = used_variables_on_screen
            
        # create mermaid for each variable (where set and where used)
        self.md_file.new_header(level=1, title="Global Variables")
        self.md_file.new_line("Usage of global variables is shown based on the screen(s) where this variable is set and the screen(s) where it is used. ")
        
        for variable in all_global_variables:
            variable_mermaid = [self.config["MermaidPrefix"]]
            variable_mermaid.append("graph LR")
            
            for key, value in screen_set_variables.items():
                if variable in value:
                    variable_mermaid.append(
                        "Set" + "".join(key.split()) + r"(" + key + r")" +
                        "-- set -->" +
                        "".join(variable.split()) + r"[/" + variable + r"/]"
                    )
            
            for key, value in screen_use_variables.items():
                if variable in value:
                    variable_mermaid.append(
                        "".join(variable.split()) + r"[/" + variable + r"/]" +
                        "-. use .->" +
                        "Use" + "".join(key.split()) + r"(" + key + r")"
                    )

            variable_mermaid.append(self.config["MermaidSuffix"])
        
            variable_mermaid = list(dict.fromkeys(variable_mermaid))
            
            if len(variable_mermaid) > 2:
                self.md_file.new_header(level=2, title=variable)
            
                for line in variable_mermaid:
                    self.md_file.new_line(line)

    def _create_global_collects(self):
        screen_set_variables = {}
        screen_use_variables = {}

        for file in self._get_screen_files():
            # check on which screen variables are set
            screen_objects = self.parser.get_screen_objects(file)
            global_variables_on_screen = re.findall(
                r"Collect\((.[^,]*)", str(screen_objects[1]))
            global_variables_on_screen = list(set(global_variables_on_screen))
            screen_set_variables[screen_objects[0]
                                 ] = global_variables_on_screen

        # get all set global variables
        all_global_variables = [
            item for sublist in screen_set_variables.values() for item in sublist]
        all_global_variables = list(set(all_global_variables))

        for file in self._get_screen_files():
            screen_objects = self.parser.get_screen_objects(file)
            used_variables_on_screen = []

            # check if variables are used on this screen
            for variable in all_global_variables:
                used_variables_on_screen = used_variables_on_screen + \
                    re.findall(f"(?<!Collect\(){variable}", str(screen_objects[1]))

            # remove duplicates
            used_variables_on_screen = list(set(used_variables_on_screen))
            screen_use_variables[screen_objects[0]] = used_variables_on_screen

        # create mermaid for each variable (where set and where used)
        self.md_file.new_header(level=1, title="Global Collects")
        self.md_file.new_line(
            "Usage of global collects is shown based on the screen(s) where this collect is set and the screen(s) where it is used. ")

        for variable in all_global_variables:
            variable_mermaid = [self.config["MermaidPrefix"]]
            variable_mermaid.append("graph LR")

            for key, value in screen_set_variables.items():
                if variable in value:
                    variable_mermaid.append(
                        "Set" + "".join(key.split()) + r"(" + key + r")" +
                        "-- set -->" +
                        "".join(variable.split()) + r"[/" + variable + r"/]"
                    )

            for key, value in screen_use_variables.items():
                if variable in value:
                    variable_mermaid.append(
                        "".join(variable.split()) + r"[/" + variable + r"/]" +
                        "-. use .->" +
                        "Use" + "".join(key.split()) + r"(" + key + r")"
                    )

            variable_mermaid.append(self.config["MermaidSuffix"])

            variable_mermaid = list(dict.fromkeys(variable_mermaid))

            if len(variable_mermaid) > 2:
                self.md_file.new_header(level=2, title=variable)

                for line in variable_mermaid:
                    self.md_file.new_line(line)


    def create_documentation(self, format=None):
        if format == None:
            self.format = "markdown"
        else:
            self.format = format

        # instantiate the md file
        # TODO: get title from docstring variable
        app_name = self.manifest_file["PublishInfo"]["AppName"]
        output_file = os.path.join(self.output_path, f'{app_name}-doc')
        self.md_file = MdUtils(file_name=output_file, title='Power App Documentation')

        for chapter in self.config["DocumentStructure"]:
            if chapter == "App":
                self._create_chapter_app(app_name=app_name)
            elif chapter == "Connections":
                self._create_chapter_connections()
            elif chapter == "Screens":
                self._create_chapter_screens()
            elif chapter == "GlobalVariables":
                self._create_global_variables()
            elif chapter == "GlobalCollects":
                self._create_global_collects()

        # write toc + file
        self.md_file.new_table_of_contents(table_title='Contents', depth=2)
        self.md_file.create_md_file()

        return output_file + ".md"
