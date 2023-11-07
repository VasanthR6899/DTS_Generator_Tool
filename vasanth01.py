from tkinter import *
from tkinter import filedialog

root = Tk()

# Display the dialog for browsing files.
filename = filedialog.askopenfilename()
# Print the selected file path.

clicked = StringVar()
clicked1 = StringVar()
clicked2 = StringVar()

clicked.set(filename)
clicked1.set("r u late to office today ")
clicked2.set('r u working from home')

def print_selected_value():
    #selected_value = clicked.get()
    #print("Selected Value:", selected_value)
    
    if(clicked1=="yes"):
        data_to_write = "the person is late to the office"
        file_path = filename
        with open(file_path, 'a') as file:
            file.write(data_to_write)
    else:
        data_to_write = "the person is on time to the office"
        file_path = filename
        with open(file_path, 'a') as file:
            file.write(data_to_write)
        
    

optionsyn = [
    "yes",
    "no"]


drop1 = OptionMenu(root,clicked1,*optionsyn)
drop1.pack()

drop2 = OptionMenu(root,clicked2,*optionsyn)
drop2.pack()

print_button = Button(root, text="submit", command=print_selected_value)
print_button.pack()

root.mainloop()
