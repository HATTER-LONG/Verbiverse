import argparse
import importlib
import os
import re
import subprocess

from verbiverse.Functions.Log import get_logger

logger = get_logger("project")


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


def build():
    qrc_file_path = []
    for root, _, files in os.walk("."):
        for filename in files:
            if filename.endswith(".ui"):
                ui_file_path = os.path.join(root, filename)
                py_file_path = ui_file_path.replace(".ui", "_ui.py")
                convert_ui_files(ui_file_path, py_file_path)
            # if filename.endswith(".ts") and ".TMP." not in filename:
            #     ts_file_path = os.path.join(root, filename)
            #     qm_file_path = ts_file_path.replace(".ts", ".qm")
            #     convert_qm_files(ts_file_path, qm_file_path)
            if filename.endswith(".qrc"):
                qrc_file_path.append(os.path.join(root, filename))
    convert_all_ts_to_one()
    for qrc_file_path in qrc_file_path:
        py_file_path = qrc_file_path.replace(".qrc", "_rc.py")
        convert_qrc_files(qrc_file_path, py_file_path)


def run_app():
    """Runs the main application."""
    try:
        import main

        main.main()
    except Exception as e:
        print(f"Error running application: {e}")


def demo(module_name):
    """Runs the demo application."""
    try:
        import resources  # noqa: F401

        module = importlib.import_module(f"tests.UI.{module_name}.demo")
        function = getattr(module, "main")
        function()
    except Exception as e:
        print(f"Error running demo: {e}")


def test():
    """use pytest to run unit tests"""
    subprocess.run(["pytest"])


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


def update_py_to_ts(py_file_path: list[str], prefix: str, resource_path: str):
    for py_file in py_file_path:
        if py_file.endswith(".py"):
            ts_file_path = py_file.replace(".py", f".TMP.{prefix}.ts")
            ts_file_path = resource_path + os.path.basename(ts_file_path)
            command = ["pyside6-lupdate", py_file, "-ts", ts_file_path]
            try:
                subprocess.run(command, check=True)
                print(f"Successfully converted {py_file} to {ts_file_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting {py_file}: {e.output}")


def get_tmp_files(path):
    tmp_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if ".TMP." in file:
                tmp_files.append(os.path.join(root, file))
    return tmp_files


def extract_context_tags(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r"<TS(.*?)>(.*?)</TS>"
    matches = re.findall(pattern, content, flags=re.DOTALL)[0][1]
    return matches


def convert_all_ts_to_one():
    files = get_tmp_files("./verbiverse/resources")
    firstfile = ""
    content = ""
    firstcontext = ""

    with open(files[0], "r", encoding="utf-8") as f:
        firstfile = f.read()
        firstcontext = extract_context_tags(files[0])

    for file in files:
        content = content + extract_context_tags(file)

    result = firstfile.replace(firstcontext, content)

    with open(
        "./verbiverse/resources/i18n/verbiverse.zh_CN.ts", "w", encoding="utf-8"
    ) as f:
        f.seek(0)
        f.truncate()
        f.write(result)

    convert_qm_files(
        "./verbiverse/resources/i18n/verbiverse.zh_CN.ts",
        "./verbiverse/resources/i18n/verbiverse.zh_CN.qm",
    )


def optimize_prompt(promptPath, task):
    import datetime

    from tools.prompt_maker import promptMaker

    logger.info(f"prompt path: {promptPath}, task: {task}")

    res = ""
    with open(promptPath, "r+", encoding="utf-8") as f:
        content = f.read()
        res = promptMaker(content, task).strip()
        logger.info(f"res: \n\n{res}\n\n")
        if input("overwrite the prompt? y/n:").lower() == "y":
            time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            with open(f"{promptPath}_{time}.bak", "w", encoding="utf-8") as bak:
                bak.write(content)
                logger.info(f"already backup to {promptPath}_{time}.bak")
            f.truncate(0)
            f.seek(0)
            f.write(res)
        f.flush()
    logger.info("prompt optimization done")


def main():
    """Parses command-line arguments and executes corresponding actions."""
    parser = argparse.ArgumentParser(
        description="Engineering Project Management Script"
    )
    parser.add_argument(
        "command",
        choices=["run", "build", "br", "test", "demo", "pyts", "prompt"],
        help="Command to execute",
    )
    parser.add_argument("name", nargs="?", default=None, help="Name for demo")

    args = parser.parse_args()

    if args.command == "build":
        build()
    elif args.command == "run":
        run_app()
    elif args.command == "br":
        build()
        run_app()
    elif args.command == "test":
        test()
    elif args.command == "demo":
        tests_directory = "./tests/UI/"
        if check_directory_existence(tests_directory, args.name):
            logger.info(f"Demo with name: {args.name}")
            demo(args.name)
        else:
            logger.error("Demo command requires a name of tests/UI/[name]")
    elif args.command == "pyts":
        # cn_ts_file_path = "./resources/i18n/verbiverse.zh_CN.ts"
        # hk_ts_file_path = "./resources/i18n/verbiverse.zh_HK.ts"
        py_file_path = ["./verbiverse/UI/SettingInterface.py", "./verbiverse/main.py"]
        resource_path = "./verbiverse/resources/i18n/"
        update_py_to_ts(py_file_path, "zh_CN", resource_path)
        # update_py_to_ts(py_file_path, "zh_HK", resource_path)
    elif args.command == "prompt":
        if not args.name:
            logger.error("Please specify the name of the prompt.")
        else:
            logger.info(f"optimize prompt: {args.name}")

            promptPrefix = "./verbiverse/resources/prompt/"
            promptList = [
                {
                    "name": "chat_prompt",
                    "task": "help me to improve a new language skill by chat",
                },
                {
                    "name": "explain_prompt",
                    "task": "explain the new language input data mean and output structed data",
                },
            ]
            for prompt in promptList:
                if prompt["name"] == args.name:
                    optimize_prompt(
                        promptPrefix + prompt["name"] + ".txt", prompt["task"]
                    )
    else:
        logger.error("Invalid command. Use 'run', 'build', 'test', 'br', or 'demo'.")


if __name__ == "__main__":
    main()
