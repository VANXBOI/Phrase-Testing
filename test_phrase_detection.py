import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
from phrases import get_random_phrase


def record_audio(file_name, duration=5):
    fs = 44100  # Sample rate
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    wav.write(file_name, fs, recording)
    print(f"Recording finished and saved as {file_name}")


def record_with_phrase_detection():
    recognizer = sr.Recognizer()
    phrase_to_recognize = get_random_phrase()  # You can select a random phrase or cycle through them

    print(f"Please say the following phrase: '{phrase_to_recognize}'")
    time.sleep(2)

    # Record the audio
    audio_file = "temp.wav"
    record_audio(audio_file)

    # Recognize the speech using Google Web Speech API
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        print("Processing...")

    try:
        recognized_text = recognizer.recognize_google(audio)
        print(f"Recognized text: '{recognized_text}'")

        # Normalize text to lowercase and remove whitespace for comparison
        normalized_recognized_text = recognized_text.lower().strip()
        normalized_phrase_to_recognize = phrase_to_recognize.lower().strip()

        # Use fuzzy matching to allow for minor differences
        similarity_score = fuzz.ratio(normalized_recognized_text, normalized_phrase_to_recognize)
        print(f"Similarity score: {similarity_score}")

        if similarity_score > 80:  # Adjust the threshold as needed
            print("Phrase recognized correctly!")
        else:
            print("Phrase did not match.")

    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
    except sr.RequestError as e:
        print(f"Sorry, there was an error with the request: {e}")


if __name__ == "__main__":
    record_with_phrase_detection()
