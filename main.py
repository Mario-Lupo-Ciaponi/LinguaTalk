import customtkinter as ctk

import os

import speech_recognition as sr
import pyttsx3
from gtts import gTTS

from playsound import playsound

from translate import Translator
from langdetect import detect, DetectorFactory

import whisper


DetectorFactory.seed = 0
recognizer = sr.Recognizer()


class TranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 450, 300

        self.title("LinguaTalk")
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

        ctk.CTkLabel(self, text="LinguaTalk", font=("Helvetica", 30)).pack(pady=15)

        self.record_button = ctk.CTkButton(self, text="Record", command=self.translate_text)
        self.record_button.pack()

        self.recognized_label = ctk.CTkLabel(self, text="Recognized: ")
        self.recognized_label.pack(pady=5)

        self.translated_label = ctk.CTkLabel(self, text="Translated: ")
        self.translated_label.pack(pady=5)

    def record_audio(self):
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            print("Listening...")

            audio = recognizer.listen(source)

        with open("temp.wav", "wb") as f:
            f.write(audio.get_wav_data())
            print("2")

        model = whisper.load_model("large")
        result = model.transcribe("temp.wav")

        print("4")

        text = result["text"]
        lang = result["language"]

        self.recognized_label.configure(text=f"Recognized: {text}")

        return text, lang

    def translate_text(self):
        target_lang = "en"

        text, lang = self.record_audio()

        if not text:
            # TODO: add messages
            return

        try:
            translator = Translator(from_lang=lang, to_lang=target_lang)
            translated = translator.translate(text)

            self.translated_label.configure(text=f"Translated: {translated}")
        except Exception as e:
            # TODO: add messages
            print(f"Translation failed: {e}")
            translated = text

        self.output_audio(translated, target_lang)

    @staticmethod
    def output_audio(text, lang):
        try:
            output = gTTS(text=text, lang=lang, slow=False)
            file_name = "output.mp3"
            output.save(file_pename)
            playsound(file_name)
            os.remove(file_name)
        except Exception as e:
            #TODO: add messages
            print(e)


def main():
    app = TranslatorApp()
    app.mainloop()

if __name__ == "__main__":
    main()