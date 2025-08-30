import customtkinter as ctk


class Translator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 450, 550

        self.title("LinguaTalk")
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

        ctk.CTkLabel(self, text="LinguaTalk", font=("Helvetica", 30)).pack(pady=15)

        self.record_button = ctk.CTkButton(self, text="Record")
        self.record_button.pack()


def main():
    app = Translator()
    app.mainloop()

if __name__ == "__main__":
    main()