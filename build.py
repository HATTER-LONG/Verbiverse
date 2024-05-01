import argparse
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


def build():
    for root, _, files in os.walk("."):
        for filename in files:
            if filename.endswith(".ui"):
                ui_file_path = os.path.join(root, filename)
                py_file_path = ui_file_path.replace(".ui", ".py")
                convert_ui_files(ui_file_path, py_file_path)


def run_app():
    """Runs the main application (__init__.py)."""
    try:
        import verbiverse  # Assuming the main application is in __init__.py

        verbiverse.MainWindow.main()
    except Exception as e:
        print(f"Error running application: {e}")


def main():
    """Parses command-line arguments and executes corresponding actions."""
    parser = argparse.ArgumentParser(
        description="Engineering Project Management Script"
    )
    parser.add_argument(
        "command", choices=["run", "build", "br"], help="Command to execute"
    )

    args = parser.parse_args()

    if args.command == "build":
        build()
    elif args.command == "run":
        run_app()
    elif args.command == "br":
        build()
        run_app()
    else:
        print("Invalid command. Use 'run', 'build' or 'br'.")


if __name__ == "__main__":
    main()
