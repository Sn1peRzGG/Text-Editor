import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("Untitled - Text Editor")
root.geometry("620x420")

saved_path = None

notepad = tk.Text(root, undo=True)
notepad.pack(fill="both", expand=True)

word_count_label = tk.Label(root, text="Words Count: 0")
word_count_label.pack(side="bottom")

def open_file():
	file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
	if file_path:
		save_file()
		notepad.delete("1.0", "end")
		with open(file_path, "r") as file:
			notepad.insert("1.0", file.read())
		root.title(f"{file_path} - Text Editor")
		count_words()

def save_file(event=None):
	global saved_path
	if saved_path:
		with open(saved_path, "w") as file:
			file.write(notepad.get("1.0", "end"))
		root.title(f"{saved_path} - Text Editor")
	else:
		file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")], initialfile="Doc1.txt")
		if file_path:
			with open(file_path, "w") as file:
				file.write(notepad.get("1.0", "end"))
			root.title(f"{file_path} - Text Editor")
			saved_path = file_path

def undo(event=None):
	try:
		notepad.edit_undo()
	except tk.TclError:
		pass
	count_words()

def redo(event=None):
	try:
		notepad.edit_redo()
	except tk.TclError:
		pass
	count_words()

def quit(event=None):
	save_file()
	root.destroy()

def cut(event=None):
	notepad.event_generate("<<Cut>>")
	count_words()

def copy(event=None):
	notepad.event_generate("<<Copy>>")

def paste(event=None):
	notepad.event_generate("<<Paste>>")
	count_words()

def select_all(event=None):
	notepad.tag_add("sel", "1.0", "end")

def count_words(event=None):
	text = notepad.get("1.0", "end-1c")
	word_count = len(text.split())
	word_count_label.config(text=f"Words Count: {word_count}")

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
edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

root.config(menu=menu_bar)

root.bind("<Control-c>", copy)
root.bind("<Control-v>", paste)
root.bind("<Control-x>", cut)
root.bind("<Control-a>", select_all)
root.bind("<Control-s>", save_file)
root.bind("<Control-z>", undo)
root.bind("<Control-y>", redo)
root.bind("<Control-q>", quit)
root.bind("<KeyRelease>", count_words)

root.protocol("WM_DELETE_WINDOW", quit)

root.mainloop()
