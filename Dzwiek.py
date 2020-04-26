import numpy as np
import pyaudio
import wave
import soundfile as sf

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 88200
# pokrywa cały zakres pasma częstotliwości słyszalnych przez człowieka oraz prawie cały zakres rozpiętości dynamicznej słyszalnych dźwięków.
RECORD_SECONDS = 2


def writeToFile(file):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Rozpoczynam nagrywanie:")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Nagrywanie zakonczone. ")

    stream.stop_stream()
    stream.close()
    p.terminate()

    waveFile = wave.open(file, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def readFromFile(plik):
    print("Odczytywanie dzwięku. ")

    waveFile = wave.open(plik, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(waveFile.getsampwidth()),
                    channels=waveFile.getnchannels(),
                    rate=waveFile.getframerate(),
                    output=True)
    framesFromFile = waveFile.readframes(CHUNK)
    while len(framesFromFile) > 0:
        stream.write(framesFromFile)
        framesFromFile = waveFile.readframes(CHUNK)
    stream.close()
    p.terminate()


def quantization(nazwa):
    data, samplerate = sf.read(nazwa)
    plik = "16" + nazwa
    sf.write(plik, data, samplerate, subtype="PCM_16")
    readFromFile(plik)
    plik = "8" + nazwa
    sf.write(plik, data, samplerate, subtype="PCM_U8")
    readFromFile(plik)




    stringRate = '88200'
    fileName = "Dzwiek.wav"
    print("Czestotliwosc " + stringRate)
    writeToFile(stringRate + fileName)
    readFromFile(stringRate + fileName)
    quantization(stringRate + fileName)
    RATE = 44100
    stringRate = '44100'
    print("Czestotliwosc " + stringRate)
    writeToFile(stringRate + fileName)
    readFromFile(stringRate + fileName)
    quantization(stringRate + fileName)
    RATE = 22050
    stringRate = '22050'
    print("Czestotliwosc " + stringRate)
    writeToFile(stringRate + fileName)
    readFromFile(stringRate + fileName)
    quantization(stringRate + fileName)
