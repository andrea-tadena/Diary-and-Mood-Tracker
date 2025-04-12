from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from time import strftime
from datetime import datetime
from tkcalendar import Calendar
import random
import os

background = "#feafde"
default_font = "MS Sans Serif"
button_color = "#d0aad3"

root = Tk()
root.title("Diary and Mood Tracker")
root.geometry("600x700")
root.config(bg="#feafde")

daytime = Image.open("daytime.png")
afternoon = Image.open("afternoon.png")
nighttime = Image.open("nighttime.png")
daytime_image = ImageTk.PhotoImage(daytime)
afternoon_image = ImageTk.PhotoImage(afternoon)
nighttime_image = ImageTk.PhotoImage(nighttime)

current_time = strftime('%H:%M:%S %p')
current_date = strftime("%Y-%m-%d")

extra_day = ["Hope the day is as bright as you are.",
             "Rise and shine, my sunshine.",
             "I'm still asleep, please don't wake me up yet."]

extra_afternoon = ["*yawns* Oh it's you. I was having a little nap.",
                   "Is the day still going well for you?",
                   "Remember to keep taking care of yourself, my friend."]

extra_night = ["The moon is cheese. You just haven't looked well enough.",
               "And just like that-another day has come to an end.",
               "If you feel lonely, look at the sky. \nChances are someone's looking at it too."]

emotions = [
    "Happy", "Playful", "Contented", "Interested", "Thankful",
    "Lonely", "Vulnerable", "Despair", "Jealous", "Humiliated", "Bitter",
    "Excited", "Confident", "Proud", "Grateful", "Curious",
    "Anxious", "Worried", "Stressed", "Overwhelmed", "Fearful",
    "Angry", "Frustrated", "Irritated", "Resentful", "Enraged",
    "Sad", "Disappointed", "Hurt", "Regretful", "Hopeless",
    "Peaceful", "Relaxed", "Satisfied", "Secure", "Loved",
    "Ashamed", "Embarrassed", "Guilty", "Insecure", "Rejected",
    "Nostalgic", "Surprised", "Hopeful", "Inspired", "Determined"
    ]

selected_emotions = []
rating = StringVar(value=" ")
var_dict = {emotion: IntVar() for emotion in emotions}

now = datetime.now()
current_hour = now.hour

canvas = Canvas(root, width=200, height=95)
canvas.place(x=20, y=190)

script_dir = os.path.dirname(os.path.abspath(__file__))
file_name = str(current_date) + ".txt"
folder = "Entries"

file_path = os.path.join(script_dir, folder, file_name)

def update_text_based_on_time():
    if 6 <= current_hour < 12:
        time_of_day = "Good Morning"
    elif 12 <= current_hour < 18:
        time_of_day = "Good Afternoon"
    else:
        time_of_day = "Good Evening"
    greeting.config(text=time_of_day)

def update_extra():
    daytime_extra = random.choice(extra_day)
    afternoon_extra = random.choice(extra_afternoon)
    nighttime_extra = random.choice(extra_night)

    if 6 <= current_hour < 12:
        extra_quote = daytime_extra
    elif 12 <= current_hour < 18:
        extra_quote = afternoon_extra
    else:
        extra_quote = nighttime_extra
        
    extra.config(text=extra_quote)

def update_icon():
    if 6 <= current_hour < 12:
        icon = daytime_image
    elif 12 <= current_hour < 18:
        icon = afternoon_image
    else:
        icon = nighttime_image
    
    time_icon.config(image=icon)
    root.iconphoto(True, icon)

def update_time():
    current_time = strftime("%H:%M:%S %p")
    current_date = strftime("%A, %B %d, %Y")
    display_text = f"How are you? It is {current_date} {current_time}"
    how_are_you.config(text=display_text, font=(default_font, 12, "bold"), fg="purple")
    how_are_you.after(1000, update_time)

def load_icon():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")]
    )
    if file_path:
        image = Image.open(file_path)
        image = image.resize((100, 100))  
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(100, 50, image=photo, anchor=CENTER)
        canvas.image = photo  
        canvas.original_image_path = file_path

def copy_image():
    if hasattr(canvas, 'original_image_path'):
        original_img = Image.open(canvas.original_image_path)
        copied_img = original_img.copy()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        new_file_name = f"{current_date}.png"
        new_file_path = os.path.join(script_dir, "Details", new_file_name)
        copied_img.save(new_file_path)

def add_emotions():
    selected_emotions.clear() 
    for emotion, var in var_dict.items():
        if var.get():  
            selected_emotions.append(emotion)
            
    tags_entry.config(state=NORMAL) 
    tags_entry.delete(1.0, END)  
    tags_entry.insert(END, "\n".join(selected_emotions))  
    tags_entry.config(state=DISABLED)  

def open_new_window():
    emotions_window = Toplevel(root)
    emotions_window.title("You can never have too many emotions")
    emotions_window.geometry("500x600")
    emotions_window.config(bg=background)
    
    max_per_row = 5
    for index, emotion in enumerate(emotions):
        row = index // max_per_row
        col = index % max_per_row
        checkbox = Checkbutton(emotions_window, text=emotion, bg=background, variable=var_dict[emotion])
        checkbox.grid(row=row, column=col, padx=5, pady=5)

    add_button = Button(emotions_window, text="Add Emotions", command=add_emotions)
    add_button.grid(row=row + 1, column=0, columnspan=max_per_row, pady=10)
    
def get_rating():
    selected_rating = rating.get()

def save_details():
    details = str(get_rating) + "\n" + str(selected_emotions)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = str(current_date) + "-Details.txt"
    file_path = os.path.join(script_dir, "Details", file_name)
    with open(file_path, "w") as file:
        file.write(details)

def save_entry():
    try:
        content = entry.get("1.0", END).strip()
        if not content: 
            messagebox.askquestion("Warning", "Entry is empty. Do you want to proceed?")
        else:
            with open(file_path, 'w') as file:
                file.write(content)
                save_details()
            copy_image()
            messagebox.showinfo("Saved", "Entry saved")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")

def view_entries():
    entries_window = Toplevel(root)
    entries_window.title("You can never have too many emotions")
    entries_window.geometry("600x450")
    entries_window.config(bg=background)
    entries_window.title("View Entries")
    
    directory = os.path.dirname(os.path.abspath(__file__))

    canvas = Canvas(entries_window, width=200, height=95)
    canvas.place(x=300, y=110)
    
    entry = Text(entries_window, width=79, height=10, borderwidth=1, font=(default_font, 10), wrap="word", state=DISABLED)
    entry.place(x=20, y=270)
    
    def edit_entry():
        if entry.get("1.0", END).strip():
            entry.config(state=NORMAL)
            messagebox.showinfo("Editing", "Currently editing entry")
        else:
            messagebox.showerror("Error", "No selected entry")
    
    edit_button = Button(entries_window, text="Edit Entry", width=10, height=1, font=(default_font, 10), fg="darkgray", command=edit_entry, relief=SUNKEN, state=DISABLED)
    edit_button.place(x=20, y=230)
    
    try:
        cal = Calendar(entries_window, width=12, background="pink", foreground='white', borderwidth=2, font=(default_font, 10), date_pattern="yyyy-mm-dd")
        cal.place(x=20, y=20)
    except:
        print("Cannot open calendar")
        entries_window.quit()
    
    dates_path = os.path.join(directory, "Entries")
    
    def get_dates_from_files(dates_path):
        files = os.listdir(dates_path)
        dates = []
        for file in files:
            if file.endswith(".txt"):
                try:
                    date_str = file[:-4] 
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    dates.append(date)
                except ValueError:
                    continue  
        return dates
    
    def color_dates(cal, dates):
        for date in dates:
            cal.calevent_create(date, 'Event', 'date')
            cal.tag_config('date', background='#ae8fc4', foreground='black')
            
    def refresh_calendar():
        cal.calevent_remove('all')
        dates = get_dates_from_files(dates_path)
        color_dates(cal, dates)
    
    refresh_calendar()
    cal.bind("<<CalendarSelected>>")
    
    def view_entry():
        try:
            get_date = cal.get_date()
            get_date_txt = f"{get_date}.txt"
            path = os.path.join(directory, "Entries", get_date_txt)
            print(get_date_txt)
            entry.config(state=NORMAL)
            with open(path, "r") as file:
                    text = file.read()
                    entry.delete(1.0, END)  
                    entry.insert(END, text)  
                    entry.config(state=DISABLED)
                    edit_button.config(relief=RAISED, fg="black", state=NORMAL)
        except:
            messagebox.showerror("Error", "No entry for this date.")
        
        get_image_date = f"{get_date}.png"
        image_path = os.path.join(directory, "Details", get_image_date)
        print(get_image_date)
        if os.path.exists(image_path):
            image = Image.open(image_path)
            resized_image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(resized_image)
            canvas.create_image(100, 50, image=photo, anchor=CENTER, tags=image)
            canvas.image = photo
        else:
            pass  

    def edit_icon():
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")]
        )
        if file_path:
            image = Image.open(file_path)
            resized_image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(resized_image)
            canvas.create_image(100, 50, image=photo, anchor=CENTER, tags=image)
            canvas.image = photo  
    
    edit_icon_button = Button(entries_window, text="Edit icon", width=10, height=1, font=(default_font, 10), command=edit_icon)
    edit_icon_button.place(x=220, y=230)

    def delete_entry():
        get_date = cal.get_date()
        get_date_txt = f"{get_date}.txt"
        get_date_details_txt = f"{get_date}-Details.txt"
        get_date_picture = f"{get_date}.png"
        path_entry = os.path.join(directory, folder, get_date_txt)
        path_details = os.path.join(directory, "Details", get_date_details_txt)
        path_picture = os.path.join(directory, "Details", get_date_picture)
        if os.path.exists(path_entry):
            try:
                os.remove(path_entry)
                entry.config(state=NORMAL)
                entry.delete(1.0, END)
                entry.config(state=DISABLED)
                canvas.delete("image")
                canvas.image = None
                messagebox.showinfo("Success", f"Entry deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while deleting the file: {e}")
        else:
            messagebox.showerror("Error", f"File '{get_date_txt}' does not exist.")
        if os.path.exists(path_details):
            try:
                os.remove(path_details)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while deleting the file: {e}")
        else:
            messagebox.showerror("Error", f"File '{get_date_details_txt}' does not exist.")
        if os.path.exists(path_picture):
            try:
                os.remove(path_picture)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while deleting the file: {e}")
        else:
            pass   
    
    delete_button = Button(entries_window, text="Delete", width=10, height=1, font=(default_font, 10), command=delete_entry)
    delete_button.place(x=320, y=230)    
                
    view_entry_button = Button(entries_window, text="View Entry", width=10, height=1, font=(default_font, 10), command=view_entry)
    view_entry_button.place(x=120, y=230)


how_are_you = Label(root, bg=background)
update_time()
how_are_you.place(x=100, y=60)

greeting = Label(root, text="", font=(default_font, 20, "bold"), bg=background)
update_text_based_on_time()
greeting.place(x=100, y=20)

time_icon = Label(root)
time_icon.place(x=20, y=20)
update_icon()

rate_your_day = Label(root, text="Rate your current mood", font=(default_font, 10, "bold"), bg=background)
rate_your_day.place(x=20, y=100)

extra = Label(root, text="", bg=background, font=("Courier New", 10, "italic"))
update_extra()
extra.place(x=20, y=650)

entry = Text(root, width=79, height=10, borderwidth=1, font=(default_font, 10), wrap="word")
entry.place(x=20, y=390)

write_entry = Label(root, text="Write your entry here", font=(default_font, 10), bg=background)
write_entry.place(x=20, y=360)

write_tags = Label(root, text="Emotions you're currently feeling.", font=(default_font, 10, "bold"), bg=background)
write_tags.place(x=320, y=160)

add_photos = Label(root, text="Optional: Add photo", font=(default_font, 10, "bold"), bg=background)
add_photos.place(x=20, y=160)

select_photo_button = Button(root, text="Select photo", width=11, height=1, bg="#d0aad3", font=("MS Sans Serif", 10), command=load_icon)
select_photo_button.place(x=20, y=300)

tags_entry = Text(root, width=30, height=6, borderwidth=1, wrap="word")
tags_entry.place(x=320, y=190)

view_entries_button = Button(root, text="View Entries", width=10, height=1, bg="#d0aad3", font=("MS Sans Serif", 10), command=view_entries)
view_entries_button.place(x=130, y=570)

save_entry_button = Button(root, text="Save Entry", width=10, height=1, bg="#d0aad3", font=("MS Sans Serif", 10), command=save_entry)
save_entry_button.place(x=20, y=570)

select_emotions_button = Button(root, text="Select emotions", width=12, height=1, bg="#d0aad3", font=("MS Sans Serif", 10), command=open_new_window)
select_emotions_button.place(x=320, y=300)

awful_button = Radiobutton(root, text="Awful", bg=background, font=(default_font, 10), variable=rating, value="Awful", command=get_rating)
bad_button = Radiobutton(root, text="Bad", bg=background, font=(default_font, 10), variable=rating, value="Bad", command=get_rating)
okay_button = Radiobutton(root, text="Okay", bg=background, font=(default_font, 10), variable=rating, value="Okay", command=get_rating)
good_button = Radiobutton(root, text="Good", bg=background, font=(default_font, 10), variable=rating, value="Good", command=get_rating)
great_button = Radiobutton(root, text="Great", bg=background, font=(default_font, 10), variable=rating, value="Great", command=get_rating)

awful_button.place(x=20, y=120)
bad_button.place(x=90, y=120)
okay_button.place(x=160, y=120)
good_button.place(x=230, y=120)
great_button.place(x=300, y=120)




root.mainloop()
