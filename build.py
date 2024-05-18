import argparse
import importlib
import os
import subprocess


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


def build():
    for root, _, files in os.walk("."):
        for filename in files:
            if filename.endswith(".ui"):
                ui_file_path = os.path.join(root, filename)
                py_file_path = ui_file_path.replace(".ui", ".py")
                convert_ui_files(ui_file_path, py_file_path)
            if filename.endswith(".qrc"):
                qrc_file_path = os.path.join(root, filename)
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


def main():
    """Parses command-line arguments and executes corresponding actions."""
    parser = argparse.ArgumentParser(
        description="Engineering Project Management Script"
    )
    parser.add_argument(
        "command",
        choices=["run", "build", "br", "test", "demo"],
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
            print(f"Demo with name: {args.name}")
            demo(args.name)
        else:
            print("Demo command requires a name of tests/UI/[name]")
    else:
        print("Invalid command. Use 'run', 'build', 'test', 'br', or 'demo'.")


if __name__ == "__main__":
    main()
