import customtkinter as ctk
from tkinter import messagebox

import os

import speech_recognition as sr
import pyttsx3
from gtts import gTTS

from playsound import playsound

from translate import Translator
from langdetect import detect, DetectorFactory

import threading

import whisper


DetectorFactory.seed = 0
recognizer = sr.Recognizer()


class TranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 450, 300

        x = (self.winfo_screenwidth() // 2) - (self.WINDOW_WIDTH // 2)
        y = (self.winfo_screenheight() // 2) - (self.WINDOW_HEIGHT // 2)

        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")

        self.title("LinguaTalk")

        ctk.CTkLabel(self, text="LinguaTalk", font=("Helvetica", 30)).pack(pady=15)

        self.record_button = ctk.CTkButton(self, text="Record", command=self.translate_text)
        self.record_button.pack()

        self.lang_dict = whisper.tokenizer.LANGUAGES

        self.name_to_code = {v.capitalize(): k for k, v in self.lang_dict.items()}

        self.lang_var = ctk.StringVar(value="English")
        self.selected_language_code = "en"
        self.lang_code = self.name_to_code[self.lang_var.get()]

        self.label = ctk.CTkLabel(self, text="Choose language:")
        self.label.pack(pady=10)

        self.lang_menu = ctk.CTkOptionMenu(
            self,
            values=[k for k in self.name_to_code.keys()],
            variable=self.lang_var,
            command=self.on_language_change
        )
        self.lang_menu.pack()


        self.loading_label = ctk.CTkLabel(self, text="")
        self.loading_label.pack()

        ctk.CTkLabel(self, text="Recognized:").pack()
        self.recognized_label = ctk.CTkLabel(self, text="")
        self.recognized_label.pack(pady=5)

        ctk.CTkLabel(self, text="Translated:").pack()
        self.translated_label = ctk.CTkLabel(self, text="")
        self.translated_label.pack(pady=5)

    def on_language_change(self, choice):
        lang_code = self.name_to_code[choice]
        self.selected_lang_code = lang_code

    def record_audio(self):
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)

            self.loading_label.configure(text="Listening...")
            self.loading_label.pack_configure(pady=15)

            audio = recognizer.listen(source)

        with open("temp.wav", "wb") as f:
            f.write(audio.get_wav_data())

        self.loading_label.configure(text="Translating...")

        model = whisper.load_model("large")
        result = model.transcribe("temp.wav")

        text = result["text"]
        lang = result["language"]

        self.recognized_label.configure(text=f"{text} (Language recognized: {lang})")

        return text, lang


    def translate_text(self):
        threading.Thread(target=self._translate_worker).start()

    def _translate_worker(self):
        text, lang = self.record_audio()

        if not text:
            messagebox.showerror("No text provided!", "We could not hear your voice!")
            return

        try:
            translator = Translator(from_lang=lang, to_lang=self.selected_lang_code)
            translated = translator.translate(text)

            self.translated_label.configure(text=f"{translated}")
        except Exception as e:
            messagebox.showerror("Translation failed!", "Sorry, but the translation failed!")
            return

        self.output_audio(translated, self.selected_lang_code)

    def output_audio(self, text, lang):
        try:
            output = gTTS(text=text, lang=lang, slow=False)
            file_name = "output.mp3"
            output.save(file_name)
            playsound(file_name)
            os.remove(file_name)
        except Exception as e:
            messagebox.showerror(
                "No output audio",
                "Sorry, but we could not provide you with audio right now!"
            )

        self.loading_label.configure("")
        self.loading_label.pack_configure(pady=0)


def main():
    app = TranslatorApp()
    app.mainloop()

if __name__ == "__main__":
    main()