import time
from datetime import datetime, timedelta
from tkinter import *

''' TO-DO: 
    fix: if time is  01:00:00 clicking minus time doesnt allow the clock to go down
'''

class ShutdownTimerV2:
    def __init__(self, master):
        '''This function initialises all the widgets and sets global variables'''
        self.cd_hours_ = 0
        self.cd_mins_ = 0
        self.cd_seconds_ = 0
        self.cd_loop_count = 0
        self.cd_first_run_ = False
        self.timer_finished_ = False
        self.total_ = 0
        self.time_ = ''
        self.user_mode_choice = ""
        cd_label_font = ("times", 20, "bold")
        clock_label_font = ("times", 20, "bold")
        self.img = PhotoImage(file="stopwatch.gif")

        self.master = master
        self.frame = Frame(self.master, relief=SUNKEN, bg="blue")
        self.stopwatch_canvas = Canvas(self.frame, height=40, width=40)
        self.clock_label = Label(self.frame, text="")
        self.clock_label.config(width=15)
        self.cd_label = Label(self.frame, text=self.returns_formatted_time())
        self.clock_label.config(font=clock_label_font)
        self.cd_label.config(fg="red")
        self.cd_label.config(font=cd_label_font)

        self.reset_button = Button(self.frame, text="Reset", command=lambda: self.reset())
        self.add_time = Button(self.frame, text="+", repeatdelay=500,
                               repeatinterval=100, command=lambda: self.countdown_timer_maths(1))
        self.minus_time = Button(self.frame, text="-", repeatdelay=500,
                                 repeatinterval=100, command=lambda: self.countdown_timer_maths(-1))
        self.go_button = Button(self.frame, text="Go", command=lambda: self.countdown_start_toggle())
        self.test_minus_seconds = Button(self.frame, text="-s", command=lambda: self.minus_second())
        self.test_plus_hour = Button(self.frame, text="+1h", command=lambda: self.plus_hour())

        self.menu_options = ["Shutdown", "Sleep", "Restart"]
        self.menu_options_var = StringVar(master)
        self.menu_options_var.set(self.menu_options[0])
        self.task_menu = OptionMenu(self.frame, self.menu_options_var, "Shutdown", "Sleep", "Restart")
        self.task_menu.config(highlightthickness=0)

        self.clock_label.grid(row=0, column=0, columnspan=6, sticky="NEWS")
        self.cd_label.grid(row=1, column=2, columnspan=3, sticky="NEWS")
        self.minus_time.grid(row=1, column=0, sticky="NEWS")
        self.add_time.grid(row=1, column=5, sticky="NEWS")
        self.stopwatch_canvas.create_image(20, 20, image=self.img)
        self.stopwatch_canvas.place(x=48, y=36)
        # self.stopwatch_canvas.grid(row=1, column=1, sticky="NEWS")

        self.task_menu.grid(row=2, column=0, columnspan=3, sticky="NEWS")
        self.reset_button.grid(row=2, column=3, columnspan=2, sticky="NEWS")
        self.go_button.grid(row=2, column=5, sticky="NEWS")

        # TEST BUTTONS

        self.test_minus_seconds.grid(row=6, column=0, sticky="NEWS")
        self.test_plus_hour.grid(row=6, column=5, sticky="NEWS")

        self.frame.pack()

        # FINAL COUNTDOWN FRAME
        self.overlay_frame = Frame(self.master)
        self.final_countdown_label = Label(self.overlay_frame, text="")

        # FINAL COMMANDS
        self.update_clock()
        self.cd_label.bind('<Button-1>', self.event_handling)

    def minus_second(self):
        self.cd_seconds_ -= 55

    def plus_hour(self):
        self.cd_hours_ += 1

    def update_clock(self):
        # called every 200ms
        current_time = time.strftime('%H:%M:%S')
        if current_time != self.time_:
            self.time_ = current_time
            self.clock_label.config(text=self.time_)
        self.clock_label.after(200, self.update_clock)

    def countdown_timer_maths(self, click_count):
        if click_count == -1 and self.cd_mins_ == 0:
            # cant go negative
            pass
        else:
            self.cd_mins_ += click_count
            if self.cd_mins_ > 59:
                self.cd_hours_ += 1
                self.cd_mins_ = 0
        self.cd_label.config(text=self.returns_formatted_time())

    def returns_formatted_time(self):
        return '{:02d}:{:02d}:{:02d}'.format(self.cd_hours_, self.cd_mins_, self.cd_seconds_)

    def reset(self):
        self.cd_hours_ = 0
        self.cd_mins_ = 0
        self.cd_seconds_ = 0
        self.cd_label.config(text=self.returns_formatted_time())

    def countdown(self):
        # cd_after = self.cd_label.after(1000, self.countdown)
        self.cd_label.after(1000, self.countdown)
        if self.cd_mins_ <= 0 and self.cd_hours_ <= 0 and self.cd_seconds_ <= 0:
            self.timer_finished_ = True
            '''self.frame.after_cancel(cd_after) causes TclError: can't delete Tcl command'''
        if self.timer_finished_:
            self.shutdown_reset_sleep()
        if not self.cd_first_run_:
            if self.cd_hours_ > 0 and self.cd_mins_ == 0:
                self.cd_hours_ -= 1
                self.cd_mins_ = 59
                self.cd_seconds_ = 60
            else:
                self.cd_mins_ -= 1
                self.cd_seconds_ = 60
        elif self.cd_seconds_ <= 0 and self.cd_mins_ > 0:  # simplified expression bugs countdown?
            self.cd_mins_ -= 1
            self.cd_seconds_ = 60
        if self.cd_hours_ > 0 and self.cd_mins_ == 0 and self.cd_seconds_ <= 0:
            self.cd_hours_ -= 1
            self.cd_mins_ = 59
            self.cd_seconds_ = 60

        self.cd_seconds_ -= 1
        self.cd_first_run_ = True
        self.cd_label.config(text=self.returns_formatted_time())

    def shutdown_reset_sleep(self, action=0):
        print("works")
        # import subprocess
        # if action == 1:
        #     subprocess.call(["shutdown", "/s"])
        # elif action == 2:
        #     subprocess.call(["shutdown", "/r"])
        # else:
        #    # subprocess.call()
        #     pass

    def countdown_start_toggle(self):
        self.countdown()

    def event_handling(self, event):
        print(event)

def main():
    root = Tk()
    root.title("Shutdown Timer")
    ShutdownTimerV2(root)
    root.mainloop()

if __name__ == '__main__':
    main()
