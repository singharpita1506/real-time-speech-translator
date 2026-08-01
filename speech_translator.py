import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import playsound
import os

# Supported languages (input + output)
LANGUAGES = {
    "1": ("English", "en", "en-US"),
    "2": ("Hindi", "hi", "hi-IN"),
    "3": ("Telugu", "te", "te-IN"),
    "4": ("Tamil", "ta", "ta-IN"),
    "5": ("Marathi", "mr", "mr-IN"),
    "6": ("Gujarati", "gu", "gu-IN"),
    "7": ("Punjabi", "pa", "pa-IN"),
    "8": ("French", "fr", "fr-FR"),
    "9": ("Spanish", "es", "es-ES"),
}

def recognize_speech(lang_code):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"🎤 Speak something in {lang_code}...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language=lang_code)
        print("✅ You said:", text)
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, I couldn't understand.")
        return None
    except sr.RequestError:
        print("⚠️ API unavailable.")
        return None

def translate_text(text, src_lang, target_lang):
    try:
        result = GoogleTranslator(source=src_lang, target=target_lang).translate(text)
        print(f"🌍 Translated ({target_lang}): {result}")
        return result
    except Exception as e:
        print("⚠️ Translation error:", e)
        return None

def speak_text(text, lang):
    try:
        tts = gTTS(text=text, lang=lang)
        filename = "output.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        print("⚠️ TTS error:", e)

if __name__ == "__main__":
    # Choose input language
    print("\n🎤 Input Languages:")
    for key, (name, _, code) in LANGUAGES.items():
        print(f"{key}. {name} ({code})")
    src_choice = input("Choose input language number: ")

    #Choose output language
    print("\n🔊 Output Languages:")
    for key, (name, code, _) in LANGUAGES.items():
        print(f"{key}. {name} ({code})")
    tgt_choice = input("Choose output language number: ")

    if src_choice in LANGUAGES and tgt_choice in LANGUAGES:
        src_lang_name, src_lang, src_code = LANGUAGES[src_choice]
        tgt_lang_name, tgt_lang, _ = LANGUAGES[tgt_choice]

        # Speech Recognition
        spoken_text = recognize_speech(src_code)

        if spoken_text:
            # Translate
            translated = translate_text(spoken_text, src_lang, tgt_lang)

            #Speak output language
            if translated:
                speak_text(translated, tgt_lang)
    else:
        print("❌ Invalid choice")