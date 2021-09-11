

# ######################################## split into pieces of 1 min


from warnings import simplefilter
from pydub import AudioSegment
import math
import wave
import numpy 
import time
from vosk import Model, KaldiRecognizer
import wave
import json
import os
import scipy.io.wavfile as wf
import csv


class VoiceActivityDetection:

    def __init__(self):
        self.__step = 160
        self.__buffer_size = 160 
        self.__buffer = numpy.array([],dtype=numpy.int16)
        self.__out_buffer = numpy.array([],dtype=numpy.int16)
        self.__n = 0
        self.__VADthd = 0.
        self.__VADn = 0.
        self.__silence_counter = 0

    # Voice Activity Detection
    # Adaptive threshold
    def vad(self, _frame):
        frame = numpy.array(_frame) ** 2.
        result = True
        threshold = 0.1
        thd = numpy.min(frame) + numpy.ptp(frame) * threshold
        self.__VADthd = (self.__VADn * self.__VADthd + thd) / float(self.__VADn + 1.)
        self.__VADn += 1.

        if numpy.mean(frame) <= self.__VADthd:
            self.__silence_counter += 1
        else:
            self.__silence_counter = 0

        if self.__silence_counter > 20:
            result = False
        return result

    # Push new audio samples into the buffer.
    def add_samples(self, data):
        self.__buffer = numpy.append(self.__buffer, data)
        result = len(self.__buffer) >= self.__buffer_size
        # print('__buffer size %i'%self.__buffer.size)
        return result

    # Pull a portion of the buffer to process
    # (pulled samples are deleted after being
    # processed
    def get_frame(self):
        window = self.__buffer[:self.__buffer_size]
        self.__buffer = self.__buffer[self.__step:]
        # print('__buffer size %i'%self.__buffer.size)
        return window

    # Adds new audio samples to the internal
    # buffer and process them
    def process(self, data):
        if self.add_samples(data):
            while len(self.__buffer) >= self.__buffer_size:
                # Framing
                window = self.get_frame()
                # print('window size %i'%window.size)
                if self.vad(window):  # speech frame
                	self.__out_buffer = numpy.append(self.__out_buffer, window)
                # print('__out_buffer size %i'%self.__out_buffer.size)

    def get_voice_samples(self):
        return self.__out_buffer
 


#################################### cannaux

def get_text_from_voice(filename):

    if not os.path.exists("model"):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)

    sound = AudioSegment.from_file(filename, format='wav', frame_rate=8000)
    sound = sound.set_frame_rate(16000)
    sound.export(filename, format='wav')


    wf = wave.open(filename, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    model = Model("model")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    textResults=[]
    results = ""



    while True:
        data = wf.readframes(wf.getnframes())
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            recResult = rec.Result()
            results = results + recResult
            # convert the recResult string into a dictionary  
            resultDict = json.loads(recResult)
            # save the 'text' value from the dictionary into a list
            textResults.append(resultDict.get("text", ""))

            
    # process "final" result
    results = results + rec.FinalResult()
    resultDict = json.loads(rec.FinalResult())
    textResults.append(resultDict.get("text", ""))
    return " ".join(map(str,textResults))

    
if __name__ == '__main__' :

    # split voices and remove silence
    wav = wf.read('calls\\call.wav')
    ch = wav[1].shape[1]
    sr = wav[0]

    c0 = wav[1][:,0]
    c1 = wav[1][:,1]

    print('c0 %i'%c0.size)

    vad = VoiceActivityDetection()
    vad.process(c0)
    voice_samples = vad.get_voice_samples()
    wf.write('output.2.wav',sr,voice_samples)

    if ch==1:
        exit()
        
    vad = VoiceActivityDetection()
    vad.process(c1)
    voice_samples = vad.get_voice_samples()
    wf.write('output.1.wav',sr,voice_samples)


    # # recognize
    

    with open('client.csv', 'w') as output:
        writer = csv.DictWriter(output, fieldnames=["paroles"])
        writer.writeheader()
        print(get_text_from_voice('output.2.wav'), file=output)

    with open('agent.csv', 'w') as output:
                print(get_text_from_voice('output.1.wav'), file=output)


