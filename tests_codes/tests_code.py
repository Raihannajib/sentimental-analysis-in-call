from pydub import AudioSegment


#! /usr/bin/env python
# encoding: utf-8



import numpy
import scipy.io.wavfile as wf
import sys



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
 

# usage:
wav = wf.read('test2.wav')
ch = wav[1].shape[1]
sr = wav[0]

c0 = wav[1][:,0]
c1 = wav[1][:,1]

print('c0 %i'%c0.size)

vad = VoiceActivityDetection()
vad.process(c0)
voice_samples = vad.get_voice_samples()
wf.write('output.1.wav',sr,voice_samples)

if ch==1:
    exit()
    
vad = VoiceActivityDetection()
vad.process(c1)
voice_samples = vad.get_voice_samples()
wf.write('output.2.wav',sr,voice_samples)

# def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
#     '''
#     sound is a pydub.AudioSegment
#     silence_threshold in dB
#     chunk_size in ms
#     iterate over chunks until you find the first one with sound
#     '''
#     trim_ms = 0  # ms
#     while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold:
#         trim_ms += chunk_size

#     return trim_ms


# if __name__ == '__main__':
#     import sys

#     sound = AudioSegment.from_file('test2.wav', format="wav")

#     start_trim = detect_leading_silence(sound)
#     end_trim = detect_leading_silence(sound.reverse())

#     duration = len(sound)
#     trimmed_sound = sound[start_trim:duration-end_trim]
#     trimmed_sound.export('output.wav', format="wav")




# url = "https://traffic.megaphone.fm/ADL8016987494.mp3"
# output_file = "/tmp/ageofnapoleon.mp3"
# urllib.request.urlretrieve(url, output_file)
# song = pydub.AudioSegment.from_mp3(output_file)

# wav_file = "/tmp/ageofnapoleon.wav"
# song = song.set_channels(1)
# song = song.set_frame_rate(16000)
# song.export(wav_file,format="wav")



# model_path = "/tmp/vosk-model-en-us-daanzu-20200328"
# model = Model(model_path)
# wf = wave.open(wav_file, "rb")
# rec = KaldiRecognizer(model, wf.getframerate())
# while True:
#     data = wf.readframes(4000)
#     if len(data) == 0:
#         break
#     a = rec.AcceptWaveform(data)
#     if (a) and 'result' in rec.Result():
        # print(json.loads(rec.Result())['text'])