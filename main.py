import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("Text Editor")
root.geometry("620x420")

saved_path = None

text_widget = tk.Text(root)
text_widget.pack(fill="both", expand=True)

def open_file():
	file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
	if file_path:
		save_file()
		text_widget.delete("1.0", "end")
		with open(file_path, "r") as file:
			text_widget.insert("1.0", file.read())
		root.title(f"{file_path} - Text Editor")

def save_file(event=None):
	global saved_path
	if saved_path:
		with open(saved_path, "w") as file:
			file.write(text_widget.get("1.0", "end"))
	else:
		file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")], initialfile="Doc1.txt")
		if file_path:
			with open(file_path, "w") as file:
				file.write(text_widget.get("1.0", "end"))
			saved_path = file_path
			root.title(f"{file_path} - Text Editor")

def cut(event=None):
	text_widget.event_generate("<<Cut>>")

def copy(event=None):
	text_widget.event_generate("<<Copy>>")

def paste(event=None):
	text_widget.event_generate("<<Paste>>")

def select_all(event=None):
	text_widget.tag_add("sel", "1.0", "end")

def quit():
	save_file()
	root.quit()

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit)
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

root.config(menu=menu_bar)

root.bind("<Control-c>", copy)
root.bind("<Control-v>", paste)
root.bind("<Control-x>", cut)
root.bind("<Control-a>", select_all)
root.bind("<Control-s>", save_file)

root.mainloop()