import shutil

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

# Check which editors are installed
installed_editors = {name: cmd for name, cmd in editors.items() if shutil.which(cmd)}

# Print the available editors
if installed_editors:
    print("Installed Editors:")
    for name, cmd in installed_editors.items():
        print(f"- {name} ({cmd})")
else:
    print("No known editors found on this system.")
