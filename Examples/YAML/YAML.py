import os
import yaml

import importlib


def example(aws, module_name, function_name = None, param = None, result = None):
    """ 'Example' run """

    if function_name == None:
        function_name = module_name

    try:
        module = importlib.import_module(f"Examples." + module_name + "." + module_name)
        importlib.reload(module)

        if not hasattr(module, function_name):
            return None

        func = getattr(module, function_name)

        params = {
            "aws" : aws,
            "param" : param,
        }
        if function_name != module_name:
            params["result"] = result
        res = func(**params)

        return res
                
    except Exception as e:
        print(f"Example: An exception occurred: {type(e).__name__} - {e}")


def read_yaml_tuples(file_path):
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
    except Exception as e:
        return []
    
    if not (isinstance(data, list) and all(isinstance(item, dict) for item in data)):
        return []
    
    return data


def write_yaml_tuples(file_path, tuples_list):
    try:
        with open(file_path, 'w') as file:
            yaml.safe_dump(tuples_list, file)
    except Exception as e:
        print(f"Failed to write to {file_path}: {e}")
        
def doYAML(aws, filename, param, result = None):
    print(f"{{ YAML ({filename}) [{param if param != None else 'run'}] ---")

    file_path = f'./Data/{filename}.yaml'
    ex_list = read_yaml_tuples(file_path)

    to_iterate = ex_list if param != "clean" else reversed(ex_list)

    for ex in to_iterate:
        do_ignore = ex["Ignore"] if "Ignore" in ex else False
        if do_ignore: continue

        it_exists = ex["Status"] if "Status" in ex else False
        res = ex["Result"] if "Result" in ex else None

        do_create = ex["Create"] if "Create" in ex else True
        do_update = ex["Update"] if "Update" in ex else True
        do_delete = ex["Delete"] if "Delete" in ex else True

        if   param == None: # create
            if not do_create or     it_exists: continue
        elif param == "update":
            if not do_update : continue
            if not it_exists and do_create:
                res = example(aws, ex["Example"], None, ex["Param"], res)
                ex["Result"] = res
            if it_exists and not do_create:
                example(aws, ex["Example"], "clean", ex["Param"], res)
                ex["Result"] = None
                continue
        elif param == "clean":
            if not do_delete or not it_exists: continue

        print(f"{ex["Example"]} ({ex["Param"]}) [{param if param != None else 'run'}]")

        res = example(aws, ex["Example"], param, ex["Param"], res)

        if param == None or (param == "update" and res != None):
            ex["Result"] = res
        if param == "clean":
            ex["Result"] = None

        ex["Status"] = param != "clean"
    
    write_yaml_tuples(file_path, ex_list)

    print("--- YAML }")

def YAML(aws, param):
    doYAML(aws, param, None)

def update(aws, param, result = None):
    doYAML(aws, param, "update", result)

def clean(aws, param, result = None):
    doYAML(aws, param, "clean", result)
