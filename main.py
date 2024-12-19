from ttkbootstrap import Window, Label, Entry, Button, LabelFrame, Treeview, Frame, PRIMARY, DANGER, OUTLINE, Notebook, \
    SUCCESS, WARNING, INFO, LIGHT
from ttkbootstrap.dialogs import Messagebox
from datetime import datetime
from pathlib import Path
import os
import shutil

window = Window(title="Desktop Explorer", themename="cyborg", iconphoto="image/filepic.png")
window.grid_rowconfigure(2, weight=1)
window.grid_columnconfigure(1, weight=1)

path_label = Label(window, text="Path", padding=10, bootstyle=PRIMARY)
path_label.grid(row=0, column=0, sticky="w")

path_entry = Entry(window)
path_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")

item_list = []


def explor_path():
    path = path_entry.get()
    for item in item_list:
        explore_treeview.delete(item)
    item_list.clear()

    row_number = 1
    path_lib = Path(path)
    for windows_path in path_lib.iterdir():
        entry_type = "File"
        entry_size = ""

        information = windows_path.stat()
        if windows_path.is_dir():
            entry_type = "Folder"
        else:
            entry_size = information.st_size // 1024

        date_created = datetime.fromtimestamp(information.st_ctime)
        date_modified = datetime.fromtimestamp(information.st_mtime)
        date_accessed = datetime.fromtimestamp(information.st_atime)

        item = explore_treeview.insert("", "end", iid=str(windows_path), text=str(row_number),
                                       values=(
                                           windows_path.name, entry_type, entry_size, date_created, date_modified,
                                           date_accessed))
        item_list.append(item)
        row_number += 1


button_frame = LabelFrame(window, text="Buttons")
button_frame.grid(row=0, column=2, pady=10, padx=(0, 10))

explor_button = Button(button_frame, text="Explor", command=explor_path)
explor_button.grid(row=0, column=0, padx=10, pady=(0, 10))


def open_folder():
    full_path = explore_treeview.selection()[0]
    path_entry.delete(0, "end")
    path_entry.insert(0, full_path)
    explor_path()


open_button = Button(button_frame, text="Open", bootstyle=OUTLINE + PRIMARY, command=open_folder)
open_button.grid(row=0, column=1, padx=(0, 10), pady=(0, 10))

notebook = Notebook(window, bootstyle=WARNING)
notebook.grid(row=1, column=1, columnspan=3, pady=(0, 10), padx=10, sticky="nsew")
frame1 = Frame(notebook)
frame2 = Frame(notebook)
frame3 = Frame(notebook)
frame4= Frame(notebook)
notebook.add(frame1, text="Search")
notebook.add(frame2, text="New Folder")
notebook.add(frame3, text="Select Path(copy,move)")
notebook.add(frame4,text="Download Manager")
frame1.grid_columnconfigure(1, weight=1)
frame2.grid_columnconfigure(1, weight=1)
frame3.grid_columnconfigure(1, weight=1)


def search():
    term = search_entry.get()
    path = path_entry.get()

    for item in item_list:
        explore_treeview.delete(item)
    item_list.clear()

    row_number = 1

    for main_folder, folder_list, file_list in os.walk(path):
        for file in file_list:
            if file.endswith(term) or file.startswith(term):
                full_path = os.path.join(main_folder, file)

                path_lib = Path(full_path)
                entry_type = "File"
                entry_size = ""
                if path_lib.is_dir():
                    entry_type = "Folder"
                else:
                    entry_size = path_lib.stat().st_size // 1024

                date_created = datetime.fromtimestamp(path_lib.stat().st_ctime)
                date_modified = datetime.fromtimestamp(path_lib.stat().st_mtime)
                date_accessed = datetime.fromtimestamp(path_lib.stat().st_atime)

                item = explore_treeview.insert("", "end", iid=str(path_lib), text=str(row_number),
                                               values=(path_lib.name, entry_type, entry_size, date_created,
                                                       date_modified,
                                                       date_accessed))
                item_list.append(item)
                row_number += 1


search_label = Label(frame1, text="Search by extension", padding=10, bootstyle=PRIMARY)
search_label.grid(row=0, column=0, sticky="w")
search_entry = Entry(frame1)
search_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")
search_button = Button(frame1, text="Search", bootstyle=OUTLINE + PRIMARY, command=search)
search_button.grid(row=0, column=2, padx=10)


def create_folder():
    new_folder = new_folder_entry.get()
    path_lib = Path(new_folder)
    if path_lib.exists():
        Messagebox.show_error(title="Exists", message="Cannot create a file when that file already exists pleas")
    else:
        path_lib.mkdir()
        Messagebox.show_info(title="Info", message="Has been created folder.")


new_folder_label = Label(frame2, text="New Folder", padding=10, bootstyle=SUCCESS)
new_folder_label.grid(row=0, column=0, sticky="w")
new_folder_entry = Entry(frame2, bootstyle=SUCCESS)
new_folder_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")
create_button = Button(frame2, text="Create", bootstyle=OUTLINE + SUCCESS, command=create_folder)
create_button.grid(row=0, column=2, padx=10)

button_menu = LabelFrame(window, text="Button Menu")
button_menu.grid(row=1, column=0, pady=10, padx=(10, 0), sticky="nsew")


def select_source_path():
    source_paths = explore_treeview.selection()[0]
    source_paths_entry.delete(0, "end")
    source_paths_entry.insert(0, source_paths)


def select_destination_path():
    destination_paths = explore_treeview.selection()[0]
    destination_entry.delete(0, "end")
    destination_entry.insert(0, destination_paths)


def copy():
    path = source_paths_entry.get()
    path_lib = Path(path)
    if path_lib.iterdir():
        shutil.copy2(source_paths_entry.get(), destination_entry.get())
    else:
        shutil.copytree(source_paths_entry.get(), destination_entry.get())


copy_button = Button(button_menu, text="Copy", bootstyle=OUTLINE + SUCCESS, command=copy)
copy_button.grid(row=0, column=0, pady=(0, 10), padx=(10, 0))

def move():
    shutil.move(source_paths_entry.get(), destination_entry.get())

move_button = Button(button_menu, text="Move", bootstyle=OUTLINE + WARNING,command=move)
move_button.grid(row=1, column=0, pady=(0, 10), padx=(10, 0))


def delete():
    delete_path = explore_treeview.selection()
    for path in delete_path:
        path_lib = Path(path)
        if path_lib.is_dir():
            fullpath = str(path_lib)
            shutil.rmtree(fullpath)
        else:
            path_lib.unlink(missing_ok=True)


delete_button = Button(button_menu, text="Delete", bootstyle=OUTLINE + DANGER, command=delete)
delete_button.grid(row=0, column=1, pady=(0, 10), padx=(10, 0),sticky="w")

def rename():
    path_lib = Path(source_paths_entry.get())
    path_lib.rename(destination_entry.get())

rename_button = Button(button_menu, text="Rename", bootstyle=OUTLINE + INFO,command=rename)
rename_button.grid(row=1, column=1, pady=(0, 10), padx=(10, 0),sticky="w")

source_paths_label = Label(frame3, text="Source Paths", padding=10, bootstyle=WARNING)
source_paths_label.grid(row=0, column=0, sticky="w")
source_paths_entry = Entry(frame3, bootstyle=LIGHT)
source_paths_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")
create_button = Button(frame3, text="Select", bootstyle=OUTLINE + WARNING, command=select_source_path)
create_button.grid(row=0, column=2, padx=10)

destination_label = Label(frame3, text="Destination Path", padding=10, bootstyle=PRIMARY)
destination_label.grid(row=1, column=0, sticky="w")
destination_entry = Entry(frame3, bootstyle=LIGHT)
destination_entry.grid(row=1, column=1, padx=(0, 10), sticky="ew")
create_button = Button(frame3, text="Select", bootstyle=OUTLINE + PRIMARY, command=select_destination_path)
create_button.grid(row=1, column=2, padx=10)

# def load_file_to_treeview(treeview):
#     path = "C:\\Program Files"
#     for item in item_list:
#         explore_treeview.delete(item)
#     item_list.clear()
#
#     row_number = 1
#     path_lib = Path(path)
#     for windows_path in path_lib.iterdir():
#         item = treeview.insert("", "end", iid=str(windows_path), text=str(row_number))
#         item_list.append(item)
#         row_number += 1


main_treeview = Treeview(window, bootstyle=PRIMARY)
main_treeview.grid(row=2, column=0, pady=(0, 10), sticky="ns")
# load_file_to_treeview(main_treeview)

explore_treeview = Treeview(window, columns=("name", "type", "size", "created", "modified", "accessed"))
explore_treeview.grid(row=2, column=1, columnspan=3, pady=(0, 10), padx=10, sticky="nsew")

explore_treeview.heading("#0", text="#")
explore_treeview.heading("#1", text="Name")
explore_treeview.heading("#2", text="Type")
explore_treeview.heading("#3", text="Size(KB)")
explore_treeview.heading("#4", text="Date Created")
explore_treeview.heading("#5", text="Date Modified")
explore_treeview.heading("#6", text="Date Accessed")
explore_treeview.column("#0", width=50)

window.mainloop()
