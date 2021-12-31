# import codecs
# pw=[]
# nw=[]
# with codecs.open("..\\words\\pos1.txt",'rw',encoding='utf-8-sig') as p1:
#     with codecs.open("..\\words\\neg1.txt",'rw',encoding='utf-8-sig') as n1:
#         with codecs.open("..\\words\\pos.txt",'rw',encoding='utf-8-sig') as p:
#             with codecs.open("..\\words\\neg.txt",'rw',encoding='utf-8-sig') as n:
#                 pw = p.read().splitlines()
#                 nw = n.read().splitlines()
#                 for w in pw :
#                     if w in nw:
#                         nw.remove(w)
#                 for w in nw :
#                     if w in nw:
#                         nw.remove(w)
#shit



# def get_text_from_voice(model,filename ):

#     sound = AudioSegment.from_file(filename, format='wav', frame_rate=8000)
#     sound = sound.set_frame_rate(16000)
#     sound.export(filename, format='wav')


#     wf = wave.open(filename, "rb")
#     if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
#         print ("Audio file must be WAV format mono PCM.")
#         exit (1)

#     rec = KaldiRecognizer(model, wf.getframerate())
#     rec.SetWords(True)

#     textResults=[]
#     results = ""


#     while True:
#         data = wf.readframes(wf.getnframes())
#         if len(data) == 0:
#             break
#         if rec.AcceptWaveform(data):
#             recResult = rec.Result()
#             results = results + recResult
#             # convert the recResult string into a dictionary  
#             resultDict = json.loads(recResult)
#             # save the 'text' value from the dictionary into a list
#             textResults.append(resultDict.get("text", ""))

            
#     # process "final" result
#     results = results + rec.FinalResult()
#     resultDict = json.loads(rec.FinalResult())
#     textResults.append(resultDict.get("text", ""))
#     return " ".join(map(str,textResults))

        


        


