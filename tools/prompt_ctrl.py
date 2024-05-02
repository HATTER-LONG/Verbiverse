from langchain import hub
from langchain_core import load


def get_prompt_template(prompt_name: str) -> dict:
    """
    Fetch a prompt template from the Hub by its name.

    Args:
        prompt_name (str): The name of the prompt template to retrieve.

    Returns:
        dict: The retrieved prompt template in JSON format.
    """
    return hub.pull(prompt_name)


def dump_prompt_template_to_file(template: dict, file_path: str) -> None:
    """
    Write a prompt template to a file in JSON format with proper indentation.

    Args:
        template (dict): The template data to be saved.
        file_path (str): The path where the template will be written.

    """
    prompt_json = load.dumps(template, indent=4)
    with open(file_path, "w") as file:
        file.write(prompt_json)


def load_prompt_template_from_file(file_path: str) -> dict:
    """
    Load a prompt template from a JSON file and return the parsed dictionary.

    Args:
        file_path (str): The path of the file containing the template.

    Returns:
        dict: The loaded template as a Python dictionary.
    """
    with open(file_path, "r") as file:
        template_json = file.read()
        return load.loads(template_json)
