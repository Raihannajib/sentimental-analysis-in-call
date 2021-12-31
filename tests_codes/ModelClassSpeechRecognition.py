
from warnings import simplefilter
from pydub import AudioSegment
import wave
from vosk import Model, KaldiRecognizer
import wave
import json
import os
import csv

class ModelClassSpeechRecognition:

        __instance = None

        @staticmethod
        def get_insatnce(filename):
            if ModelClassSpeechRecognition.__instance == None :
                ModelClassSpeechRecognition(filename)
            return ModelClassSpeechRecognition.__instance

        def __init__(self , filename  ) :
            self.wfa = None
            self.model = None
            self.rec = None
            
            if not os.path.exists("model"):
                print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
                exit (1)

            if ModelClassSpeechRecognition.__instance == None :
                self.model = Model("model")

                sound = AudioSegment.from_file(filename, format='wav', frame_rate=8000)
                sound = sound.set_frame_rate(16000)
                sound.export(filename, format='wav')


                self.wfa = wave.open(filename, "rb")
                if self.wfa.getnchannels() != 1 or self.wfa.getsampwidth() != 2 or self.wfa.getcomptype() != "NONE":
                    print ("Audio file must be WAV format mono PCM.")
                    exit (1)

                self.rec = KaldiRecognizer(self.model, self.wfa.getframerate())
                self.rec.SetWords(True)

                ModelClassSpeechRecognition.__instance = self
                

            


        def get_text_from_voice(self,csv_folder_p):
            textResults=[]
            results = ""
            while True:
                data = self.wfa.readframes(self.wfa.getnframes())
                if len(data) == 0:
                    break
                if self.rec.AcceptWaveform(data):
                    self.recResult = self.rec.Result()
                    results = results + self.recResult
                    # convert the self.recResult string into a dictionary  
                    resultDict = json.loads(self.recResult)
                    # save the 'text' value from the dictionary into a list
                    textResults.append(resultDict.get("text", ""))

                    
            # process "final" result
            results = results + self.rec.FinalResult()
            resultDict = json.loads(self.rec.FinalResult())
            textResults.append(resultDict.get("text", ""))
            print(textResults)
            text = " ".join(map(str,textResults))
            with open(csv_folder_p+'/client.csv', 'w') as output:
                    writer = csv.DictWriter(output, fieldnames=["paroles"])
                    writer.writeheader()
                    parole = text
                    print(parole)
                    print(parole, file=output)
                    with open('clients_all.csv', 'a') as output_all:
                        print(parole, file=output_all)

        # def client_to_csv(self,csv_folder_p):
        #         with open(csv_folder_p+'/client.csv', 'w') as output:
        #             writer = csv.DictWriter(output, fieldnames=["paroles"])
        #             writer.writeheader()
        #             parole = self.get_text_from_voice()
        #             print(parole)
        #             print(parole, file=output)
        #             with open('clients_all.csv', 'a') as output_all:
        #                 print(parole, file=output_all)

        def agent_to_csv(self,csv_folder_p,audio_folder_p):

                pass









