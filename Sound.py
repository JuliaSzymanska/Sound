import pyaudio
import wave
import soundfile as sf

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 96000
RECORD_SECONDS = 3


def writeToFile(file):
    pya = pyaudio.PyAudio()

    streamAudio = pya.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording started:")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = streamAudio.read(CHUNK)
        frames.append(data)

    print("Recording finished. ")

    streamAudio.stop_stream()
    streamAudio.close()
    pya.terminate()

    waveFile = wave.open(file, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(pya.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def readFromFile(plik):
    print("Reading sound. ")

    waveFile = wave.open(plik, 'rb')
    pya = pyaudio.PyAudio()

    streamAudio = pya.open(format=pya.get_format_from_width(waveFile.getsampwidth()),
                    channels=waveFile.getnchannels(),
                    rate=waveFile.getframerate(),
                    output=True)

    framesFromFile = waveFile.readframes(CHUNK)
    while len(framesFromFile) > 0:
        streamAudio.write(framesFromFile)
        framesFromFile = waveFile.readframes(CHUNK)

    streamAudio.close()
    pya.terminate()

def quantization(nazwa):
    data, samplerate = sf.read(nazwa)
    plik = "Rate_16_" + nazwa

    sf.write(plik, data, samplerate, subtype="PCM_16")

    readFromFile(plik)
    plik = "Rate_8_" + nazwa

    sf.write(plik, data, samplerate, subtype="PCM_U8")

    readFromFile(plik)


def nagrajIOdtworz():
    fileName = "Sound.py"

    stringRate = '96000'
    print("Rate " + stringRate)
    writeToFile(stringRate + fileName)
    odtworz(stringRate + fileName)

    RATE = 44100
    stringRate = '44100'
    print("Rate " + stringRate)
    writeToFile(stringRate + fileName)
    odtworz(stringRate + fileName)

    RATE = 22050
    stringRate = '22050'
    print("Rate " + stringRate)
    writeToFile(stringRate + fileName)
    odtworz(stringRate + fileName)


def odtworz(fileName):
    readFromFile(fileName)
    quantization(fileName)


def main():
    wybor = input("1. Recording and playing\n2. Playing\n")
    if wybor == "1":
        nagrajIOdtworz()
    elif wybor == "2":
        fileName = "Beethoven.wav"
        odtworz(fileName)


if __name__ == '__main__':
    main()
