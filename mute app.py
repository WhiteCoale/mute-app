from customtkinter import *
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from pynput import keyboard
import time

def get_all_session_names():
    res = []
    filter_arr = ["PowerToys.Peek.UI.exe"]
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process:
            if session.Process.name() not in filter_arr:
                res.append(session.Process.name())

    return list(set(res))


def mute(mute_hotkey, anmute_hotkey, program):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)

        if session.Process and session.Process.name() == program:

            ipt = 'in'
            with keyboard.Events() as events:
                event = events.get(1e6)

                while event.key != keyboard.Key.esc:
                    with keyboard.Events() as events:
                        event = events.get(1e6)

                        mute_button.delete(0, END)
                        anmute_button.delete(0, END)
                        mute_button.insert("0", mute_hotkey)
                        anmute_button.insert("0", anmute_hotkey)
                        app.update()

                        if event.key == keyboard.KeyCode.from_char(mute_hotkey):
                            volume.SetMute(1, None)
                        if event.key == keyboard.KeyCode.from_char(anmute_hotkey):
                            volume.SetMute(0, None)


def start_click():
    mute_input = mute_button.get()
    anmute_input = anmute_button.get()
    program = program_input.get()

    button.configure(text="Press Esc to Exit", fg_color="red", hover_color="darkred")
    app.update()

    mute(mute_input, anmute_input, program)
    button.configure(text="Start", fg_color="green", hover_color="darkgreen")


def update_dropdown():
    while True:
        try:
            process_names = get_all_session_names()
            program_input.configure(values=process_names)
            current_value = program_input.get()
            if current_value not in process_names:
                program_input.set("")
            app.update()
        except():
            time.sleep(1)
        time.sleep(0.2)


process_names = get_all_session_names()

app = CTk()
app.title("mute app")
app.geometry("300x350")
app.eval('tk::PlaceWindow . center')

frame = CTkFrame(master=app, fg_color="grey")
frame.grid(row=1, column=1)
frame.place(relx=0.5, rely=0.5, anchor="center")
CTkLabel(master=frame, text="mute app", font=("Arial Bold", 20), justify="center").pack(expand=True, pady=(30, 15))

program_input = CTkComboBox(master=frame, values=process_names)
program_input.pack(expand=True, pady=15, padx=20)

mute_button = CTkEntry(master=frame, placeholder_text="", width=40, justify="center")
mute_button.pack(expand=True, pady=15, padx=20)

anmute_button = CTkEntry(master=frame, placeholder_text="", width=40, justify="center")
anmute_button.pack(expand=True, pady=15, padx=20)

button = CTkButton(master=frame, text="Start", fg_color="green", hover_color="darkgreen", command=start_click,
                   font=("", 18))
button.pack(expand=True, fill="both", pady=(30, 15), padx=30)

update_dropdown()
app.mainloop()
