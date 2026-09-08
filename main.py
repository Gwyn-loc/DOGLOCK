import os.path
import tkinter as tk
import math
import os


class AnalogLockClock:
    def __init__(self, root):
        self.root = root
        self.root.title("DOG LOCK - SETUP")
        self.root.geometry("400x480")

        # Named for personal use
        self.folder_path = os.path.expanduser(r"C:\Users\Joerel Neri\Documents\PRELIM FOLDER")



        self.is_setup_mode = True
        self.SECRET_HOUR = None
        self.SECRET_MINUTE = None


        self.current_hour = 12
        self.current_minute = 0


        self.cx, self.cy, self.r = 200, 200, 150

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()


        self.canvas.create_oval(self.cx - self.r, self.cy - self.r, self.cx + self.r, self.cy + self.r, width=4)
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            nx = self.cx + (self.r - 20) * math.cos(angle)
            ny = self.cy + (self.r - 20) * math.sin(angle)
            self.canvas.create_text(nx, ny, text=str(i if i != 0 else 12), font=("Arial", 14, "bold"))


        self.hour_hand = self.canvas.create_line(self.cx, self.cy, self.cx, self.cy, width=6, fill="blue")
        self.min_hand = self.canvas.create_line(self.cx, self.cy, self.cx, self.cy, width=4, fill="blue")

        self.update_hands()


        self.canvas.bind("<B1-Motion>", self.drag_hand)
        self.canvas.bind("<Button-1>", self.drag_hand)


        self.instruction_label = tk.Label(root, text="SETUP: Set your password",
                                          font=("Arial", 11, "bold"), fg="darkorange")
        self.instruction_label.pack(pady=2)

        self.action_btn = tk.Button(root, text="Set This As Password", font=("Arial", 12),
                                    command=self.handle_button_click)
        self.action_btn.pack(pady=5)

    def update_hands(self):
        h_angle = math.radians(self.current_hour * 30 - 90)
        hx = self.cx + (self.r - 60) * math.cos(h_angle)
        hy = self.cy + (self.r - 60) * math.sin(h_angle)
        self.canvas.coords(self.hour_hand, self.cx, self.cy, hx, hy)

        m_angle = math.radians(self.current_minute * 6 - 90)
        mx = self.cx + (self.r - 30) * math.cos(m_angle)
        my = self.cy + (self.r - 30) * math.sin(m_angle)
        self.canvas.coords(self.min_hand, self.cx, self.cy, mx, my)

    def drag_hand(self, event):
        dx = event.x - self.cx
        dy = event.y - self.cy
        angle = math.degrees(math.atan2(dy, dx)) + 90
        if angle < 0: angle += 360

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > (self.r - 50):
            self.current_minute = int(round(angle / 6)) % 60
        else:
            self.current_hour = int(round(angle / 30)) % 12
            if self.current_hour == 0: self.current_hour = 12

        self.update_hands()


    def handle_button_click(self):
        if self.is_setup_mode:

            self.SECRET_HOUR = self.current_hour
            self.SECRET_MINUTE = self.current_minute


            self.is_setup_mode = False


            self.root.title("DOG LOCK - LOCKED")


            self.instruction_label.config(text="LOCKED: Scramble hands and click unlock", fg="red")
            self.action_btn.config(text="Unlock Folder")

        else:

            self.check_password()

    def check_password(self):
        if self.current_hour == self.SECRET_HOUR and self.current_minute == self.SECRET_MINUTE:
            self.instruction_label.config(text="Success! Folder Unlocked.", fg="green")


            os.startfile(self.folder_path)

            self.action_btn.config(state="disabled")
        else:
            self.instruction_label.config(text="Wrong Password! Try Again.", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = AnalogLockClock(root)
    root.mainloop()
