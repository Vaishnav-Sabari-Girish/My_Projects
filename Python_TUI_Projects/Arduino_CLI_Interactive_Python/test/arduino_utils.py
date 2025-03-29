import os
import subprocess
import json
import shutil


def list_arduino_boards(output_file="boards.json"):
    """
    Runs 'arduino-cli board listall' and saves the board details as JSON.

    Parameters:
    - output_file (str): Path to the JSON file where board details are stored.

    Returns:
    - list: A list of dictionaries containing board names and their FQBNs.
    """
    command_list_boards = ["arduino-cli", "board", "listall"]
    try:
        # Run the command and capture output
        result = subprocess.run(
            command_list_boards, capture_output=True, text=True, check=True
        )

        # Process output into structured data
        boards = []
        for line in result.stdout.splitlines()[1:]:  # Skip header line
            parts = line.split()  # Split by spaces
            if len(parts) >= 2:
                board_name = " ".join(
                    parts[:-1]
                )  # Everything except last part is board name
                fqbn = parts[-1]  # Last part is fqbn
                boards.append({"name": board_name, "fqbn": fqbn})

        # Save to JSON file
        with open(output_file, "w") as json_file:
            json.dump(boards, json_file, indent=4)
        return boards
    except subprocess.CalledProcessError as e:
        print("Error listing boards")
        print(e.stderr)
        return []


def search_boards(search_query, output_file="boards.json"):
    """
    Searches for Arduino boards by name or FQBN.

    Parameters:
    - search_query (str): The search term to filter boards.
    - output_file (str): JSON file containing board details.

    Returns:
    - list: A list of matching boards.
    """
    try:
        # Load boards from the JSON file
        with open(output_file, "r") as json_file:
            boards = json.load(json_file)

        # Filter boards that match the search query (case insensitive)
        matching_boards = [
            board
            for board in boards
            if search_query.lower() in board["name"].lower()
            or search_query.lower() in board["fqbn"].lower()
        ]

        # Display matching boards
        if matching_boards:
            print("\nMatching Boards:")
            for board in matching_boards:
                print(f" - {board['name']} ({board['fqbn']})")
        else:
            print("No matching boards found.")

        return matching_boards

    except FileNotFoundError:
        print(f"Error: {output_file} not found. Run list_arduino_boards() first.")
        return []


def create_new_sketch(filename):
    """
    Runs "arduino-cli sketch new <filename>" and creates a new arduino sketch.

    Parameters:
    - output_file (str): Path to the ino file.

    Returns:
    - PATH: Path to the .ino file .

    """

    command_sketch = ["arduino-cli", "sketch", "new", f"{filename}"]

    try:
        sketch_file = subprocess.run(
            command_sketch, capture_output=True, text=True, check=True
        )

        print(f"Sketch created with filename {filename}")
        return sketch_file.stdout

    except subprocess.CalledProcessError as e:
        print("Error executing command")
        print(e.stderr)
        return []


def edit_sketch():
    # List of common code editors and their command-line names
    editors = {
        "Notepad": "notepad.exe",
        "VS Code": "code",
        "VSCodium": "codium",
        "Neovim": "nvim",
        "Vim": "vim",
        "Nano": "nano",
        "Micro": "micro",
        "Emacs": "emacs",
        "Sublime Text": "subl",
        "Kate": "kate",
        "Gedit": "gedit",
        "Notepad++": "notepad++",
        "Atom": "atom",
        "Geany": "geany",
    }

    # Find installed editors
    installed_editors = {
        name: cmd for name, cmd in editors.items() if shutil.which(cmd)
    }

    # Check if there are any installed editors
    if not installed_editors:
        print("No known editors found on this system.")
        exit()

    # Display available editors
    print("\nAvailable Editors:")
    for i, name in enumerate(installed_editors.keys(), 1):
        print(f"{i}. {name}")

    # Ask user to choose an editor
    while True:
        try:
            choice = int(input("\nSelect an editor (Enter number): ")) - 1
            if 0 <= choice < len(installed_editors):
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Get selected editor
    selected_editor = list(installed_editors.keys())[choice]
    editor_cmd = installed_editors[selected_editor]

    # Ask for the file to edit
    file_path = input("\nEnter the file path to edit: ").strip()

    # Ensure the file exists (create it if it doesn't)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            pass  # Create an empty file

    # Open the selected editor
    print(f"\nOpening {selected_editor} to edit {file_path}...")
    subprocess.run([editor_cmd, file_path])
    return []


def compile_sketch(filename, fqbn):
    command_compile = [
        "arduino-cli",
        "compile",
        "--fqbn",
        f"{fqbn}",
        f"{filename}",
        "-v",
    ]

    try:
        compile_output = subprocess.Popen(
            command_compile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        for line in compile_output.stdout:
            print(line, end=" ")

        for line in compile_output.stderr:
            print(line, end=" ")

        print(f"Compiled for {fqbn}")
        return compile_output.stdout

    except subprocess.CalledProcessError as e:
        print("Error Compiling Code")
        print(e.stderr)
        return []


def upload_code(filename, fqbn, port):
    command_upload = [
        "arduino-cli",
        "upload",
        "-p",
        f"{port}",
        "--fqbn",
        f"{fqbn}",
        f"{filename}",
    ]

    try:
        upload_output = subprocess.Popen(
            command_upload, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
    except subprocess.CalledProcessError as e:
        print("Upload failed")
        print(e.stderr)
        return []

    for line in upload_output.stdout:
        print(line, end="")
    for line in upload_output.stderr:
        print(line, end="")
