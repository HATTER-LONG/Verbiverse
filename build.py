import argparse
import importlib
import os
import re
import subprocess

from verbiverse.Functions.Log import get_logger

logger = get_logger("project")

# Main cfg
PROJECT_ROOT_PATH = "./verbiverse"

# Translate file cfg
NEED_TRANSLATE_FILE_PATH_LIST = [
    "./verbiverse/MainWindow.py",
    "./verbiverse/UI/SettingInterface.py",
    "./verbiverse/UI/HomeInterface.py",
    "./verbiverse/UI/ChatWidget.ui",
    "./verbiverse/UI/ReadAndChatWidget.ui",
    "./verbiverse/CustomWidgets/CContexMenu.py",
    "./verbiverse/CustomWidgets/CWebView.py",
    "./verbiverse/Functions/ErrorString.py",
]
TRANSLATE_RESOURCE_PATH = "./verbiverse/resources/i18n/"
TRANSLATE_RESULT_FILE = "./verbiverse/resources/i18n/verbiverse.zh_CN"

# optimize prompt cfg
PROMPT_RESOURCE_PATH = "./verbiverse/resources/prompt/"
PROMPT_TASK_LIST = {
    "chat_prompt.txt": "help me to improve a new language skill by chat",
    "explain_prompt.txt": "explain the new language input data mean and output structed data",
    "explain_chinese.txt": "explain the new language input data mean and output structed data",
    "explain_sentence_prompt.txt": "explain the new language input data mean and output structed data",
    "explain_sentence_chinese.txt": "explain the new language input data mean and output structed data",
    "check_prompt.txt": "Check the input sentence for errors and output the result in the format",
    "check_chinese.txt": "Check the input sentence for errors and output the result in the format",
}


def convert_ui_files(ui_file_path, py_file_path):
    """Converts a UI file (.ui) to a Python file (.py) using pyside6-uic."""
    command = ["pyside6-uic", ui_file_path, "-o", py_file_path]
    try:
        subprocess.run(command, check=True)
        print(f"Successfully converted {ui_file_path} to {py_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {ui_file_path}: {e.output}")


def convert_qrc_files(qrc_file_path, py_file_path):
    """Converts a qrc file (.qrc) to a Python file (.py) using pyside6-rcc."""
    command = ["pyside6-rcc", qrc_file_path, "-o", py_file_path]
    try:
        subprocess.run(command, check=True)
        print(f"Successfully converted {qrc_file_path} to {py_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {qrc_file_path}: {e.output}")


def convert_qm_files(ts_file_path, qm_file_path):
    """Converts a qm file (.qm) to a .ts file (.ts) using lrelease."""
    command = ["pyside6-lrelease", ts_file_path, "-qm", qm_file_path]
    try:
        subprocess.run(command, check=True)
        print(f"Successfully converted {ts_file_path} to {qm_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {qm_file_path}: {e.output}")


def update_py_to_ts(py_file_path: list[str], prefix: str, resource_path: str):
    for py_file in py_file_path:
        command = ""
        if py_file.endswith(".py"):
            ts_file_path = py_file.replace(".py", f".TMP.{prefix}.ts")
        elif py_file.endswith(".ui"):
            ts_file_path = py_file.replace(".ui", f".TMP.{prefix}.ts")
        try:
            ts_file_path = resource_path + os.path.basename(ts_file_path)
            command = ["pyside6-lupdate", py_file, "-ts", ts_file_path]
            subprocess.run(command, check=True)
            print(f"Successfully converted {py_file} to {ts_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {py_file}: {e.output}")


def py_translate_ts():
    update_py_to_ts(NEED_TRANSLATE_FILE_PATH_LIST, "zh_CN", TRANSLATE_RESOURCE_PATH)


def build():
    py_translate_ts()
    convert_all_ts_to_one()
    qrc_file_path = []
    for root, _, files in os.walk(PROJECT_ROOT_PATH):
        for filename in files:
            if filename.endswith(".ui"):
                ui_file_path = os.path.join(root, filename)
                py_file_path = ui_file_path.replace(".ui", "_ui.py")
                convert_ui_files(ui_file_path, py_file_path)
            if filename.endswith(".qrc"):
                qrc_file_path.append(os.path.join(root, filename))
    for qrc_file_path in qrc_file_path:
        py_file_path = qrc_file_path.replace(".qrc", "_rc.py")
        convert_qrc_files(qrc_file_path, py_file_path)


def get_directory_names(directory):
    """Returns a list of directory names in the given directory."""
    return [
        name
        for name in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, name))
    ]


def check_directory_existence(directory, name):
    """Checks if the given name exists in the directory."""
    directory_names = get_directory_names(directory)
    return name in directory_names


def optimize_prompts():
    prompts = []
    for root, _, files in os.walk(PROMPT_RESOURCE_PATH):
        for file in files:
            if file in PROMPT_TASK_LIST:
                prompts.append(file)

    print("Select prompt you want to optimize:")
    for index, file in enumerate(prompts):
        print(f"{index} -> {file}")
    index = int(input("Please input index: "))

    logger.info(f"optimize prompt: {prompts[index]}")
    optimizationPrompt(
        PROMPT_RESOURCE_PATH + prompts[index], PROMPT_TASK_LIST[prompts[index]]
    )


def extract_context_tags(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r"<TS(.*?)>(.*?)</TS>"
    matches = re.findall(pattern, content, flags=re.DOTALL)[0][1]
    return matches


def convert_all_ts_to_one():
    """
    Merges multiple temporary translation files into a single translation file.
    This function searches for temporary translation files (`*.TMP.ts`) in the `TRANSLATE_RESOURCE_PATH` directory and its subdirectories. It reads the content of the first temporary file, extracts the context tags using the `extract_context_tags()` function, and stores them in the `firstcontext` variable.
    Then, it iterates over the remaining temporary files and appends their context tags to the `content` variable.
    Finally, it replaces the context tags in the `firstfile` with the `content` and writes the result to the `TRANSLATE_RESULT_FILE.ts` file.
    After that, it calls the `convert_qm_files()` function to convert the merged translation file to a QM file (`TRANSLATE_RESULT_FILE.qm`).
    """
    ts_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(TRANSLATE_RESOURCE_PATH)
        for file in files
        if ".TMP." in file
    ]

    firstfile = ""
    content = ""
    firstcontext = ""

    with open(ts_files[0], "r", encoding="utf-8") as f:
        firstfile = f.read()
        firstcontext = extract_context_tags(ts_files[0])

    content = "".join(extract_context_tags(file) for file in ts_files)
    result = firstfile.replace(firstcontext, content)

    with open(f"{TRANSLATE_RESULT_FILE}.ts", "w", encoding="utf-8") as f:
        f.seek(0)
        f.truncate()
        f.write(result)

    convert_qm_files(
        f"{TRANSLATE_RESULT_FILE}.ts",
        f"{TRANSLATE_RESULT_FILE}.qm",
    )


def optimizationPrompt(prompt_path, task):
    """
    Optimizes a prompt file by generating an optimized prompt and asking for user confirmation to overwrite the original prompt.

    Args:
        prompt_path (str): The path to the prompt file.
        task (str): The task associated with the prompt.

    Returns:
        None
    """
    import datetime

    from tools.prompt_maker import promptMaker

    # Read the content of the prompt file
    with open(prompt_path, "r", encoding="utf-8") as f:
        content = f.read()

    logger.info(
        f"start optimize prompt, please wait. -> path: {prompt_path}, task: {task}"
    )

    # Generate the optimized prompt
    optimized_prompt = promptMaker(content, task).strip()
    # Ask user for confirmation to overwrite the prompt
    if input("Overwrite the prompt? (y/n): ").lower() == "y":
        # Create a backup of the original prompt
        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        with open(f"{prompt_path}_{time}.bak", "w", encoding="utf-8") as bak:
            bak.write(content)
            logger.info(f"Backup created at {prompt_path}_{time}.bak")

        # Write the optimized prompt back to the original file
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(optimized_prompt)

        logger.info("Prompt optimization completed and saved.")
    else:
        logger.info("Prompt optimization canceled.")


def demo(module_name):
    """Runs the demo application."""
    try:
        import resources  # noqa: F401

        module = importlib.import_module(f"tests.UI.{module_name}.demo")
        function = getattr(module, "main")
        function()
    except Exception as e:
        print(f"Error running demo: {e}")


def main():
    """Parses command-line arguments and executes corresponding actions."""
    parser = argparse.ArgumentParser(description="Project Management Script")
    parser.add_argument(
        "command",
        choices=["build", "pyts", "prompt", "demo"],
        help="Command to execute",
    )
    parser.add_argument("name", nargs="?", default=None, help="Name for demo")

    args = parser.parse_args()

    if args.command == "build":
        build()
    elif args.command == "pyts":
        py_translate_ts()
    elif args.command == "prompt":
        optimize_prompts()
    elif args.command == "demo":
        tests_directory = "./tests/UI/"
        if check_directory_existence(tests_directory, args.name):
            logger.info(f"Demo with name: {args.name}")
            demo(args.name)
        else:
            logger.error("Demo command requires a name of tests/UI/[name]")
    else:
        logger.error("Invalid command.")


if __name__ == "__main__":
    main()
