import numpy as np
import pyaudio
import wave
import soundfile as sf

# 1024 domyslna wartosc - liczba ramek na bufor
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
# czestotliwosc probkowania - liczba probek na sekunde
RATE = 96000
RECORD_SECONDS = 3


def writeToFile(file):
    # Utworzenie portu audio
    pya = pyaudio.PyAudio()

    # Otwarcie strumienia audio: format 16 bitowy (najwyzszy mozliwy), 2 kanaly, czestotliwosc probkowania, okreslenie jako strumienia wejsciowego, liczba ramek na bufor
    streamAudio = pya.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Rozpoczynam nagrywanie:")

    frames = []

    # Odczytanie ramek
    # liczba probek na sekunde / liczba ramek na bufor * liczba nagranych sek - calkowita liczba ramek na sekunde podzielona przez liczbe ramek na bufor = liczba kawalkow na sekunde
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        # CHUNK - liczba ramek do odczytania
        data = streamAudio.read(CHUNK)
        # Wstawienie odczytanych ramek do zmiennej przechowywujacej wszysktie ramki
        frames.append(data)

    print("Nagrywanie zakonczone. ")

    # Zamkniecie strumienia
    streamAudio.stop_stream()
    streamAudio.close()
    # Zamkniecie portu audio
    pya.terminate()

    # Otwarcie pliku wav
    waveFile = wave.open(file, 'wb')
    # Ustawienie liczby kanalow
    waveFile.setnchannels(CHANNELS)
    # Ustawienie wielkosci probki
    waveFile.setsampwidth(pya.get_sample_size(FORMAT))
    # Ustawienie czestotliwosci probkowania
    waveFile.setframerate(RATE)
    # Zapisuje ramki do pliku
    waveFile.writeframes(b''.join(frames))
    # Zamkniecie pliku
    waveFile.close()


def readFromFile(plik):
    print("Odczytywanie dzwięku. ")

    # Utworzenie portu audio i otwarcie pliku do odczytu
    waveFile = wave.open(plik, 'rb')
    pya = pyaudio.PyAudio()

    # Otwarcie strumienia audio ustawiajac parametry pobrane z parametrow pliku wav, ustawienie na strumien wyjsciowy
    streamAudio = pya.open(format=pya.get_format_from_width(waveFile.getsampwidth()),
                    channels=waveFile.getnchannels(),
                    rate=waveFile.getframerate(),
                    output=True)

    # Zwraca conajwyzej poanda liczbe odczytanych ramek z pliku dla pierwszej sekundy
    framesFromFile = waveFile.readframes(CHUNK)
    while len(framesFromFile) > 0:
        # Odtwarzanie ramek dla sekundy
        streamAudio.write(framesFromFile)
        # dla kolejnych sekund
        framesFromFile = waveFile.readframes(CHUNK)

    # Zamkniecie strumienia
    streamAudio.close()
    # Zakonczenie portu audio
    pya.terminate()

# Kwantyzacja dzwieku
def quantization(nazwa):
    # Odczytanie ramek z pliku, metoda .read zwraca ramki, czestotliwosc probkowania
    print("Wartosc SNR dla 16bitow wynosi: ", 6.02 * 16, "dB")
    print("Wartosc SNR dla 8bitow wynosi: ", 6.02 * 8, "dB")
    data, samplerate = sf.read(nazwa)
    plik = "16" + nazwa

    # Zapisanie ramek do pliku o danej czestotliwosci probkownaia, i podtypie 16 bitowym
    sf.write(plik, data, samplerate, subtype="PCM_16")

    # Odtworzenie pliku
    readFromFile(plik)
    plik = "8" + nazwa

    # Zapisanie ramek do pliku o danej czestotliwosci probkownaia, i podtypie 8 bitowym
    sf.write(plik, data, samplerate, subtype="PCM_U8")

    # Odtworzenie pliku
    readFromFile(plik)


def nagrajIOdtworz():
    # Nagrywanie dziweku z roznymi czestotliwosciami probkownia
    fileName = "Dzwiek.wav"

    stringRate = '96000'
    print("Czestotliwosc " + stringRate)
    writeToFile(stringRate + fileName)
    odtworz(stringRate + fileName)

    # pokrywa cały zakres pasma częstotliwości słyszalnych przez człowieka
    RATE = 44100
    stringRate = '44100'
    print("Czestotliwosc " + stringRate)
    writeToFile(stringRate + fileName)
    odtworz(stringRate + fileName)

    RATE = 22050
    stringRate = '22050'
    print("Czestotliwosc " + stringRate)
    writeToFile(stringRate + fileName)
    odtworz(stringRate + fileName)


def odtworz(fileName):
    readFromFile(fileName)
    quantization(fileName)


def main():
    wybor = input("1. Nagrywanie i odtwarzanie\n2. Odtwarzanie\n")
    if wybor == "1":
        nagrajIOdtworz()
    elif wybor == "2":
        fileName = "Bet.wav"
        odtworz(fileName)


if __name__ == '__main__':
    main()
