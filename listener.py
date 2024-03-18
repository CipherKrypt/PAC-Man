import sounddevice as sd
import soundfile as sf
from threading import Thread
from faster_whisper import WhisperModel
import queue
from Recorder import Recorder

class Listener():
    def __init__(self):
        self.RESUME1 = queue.Queue(1)
        self.RESUME2 = queue.Queue(1)
        self.SAMPLE = queue.Queue(1)
        self.RESULT = queue.Queue(1)
        self.MODEL = WhisperModel("tiny.en", device="cpu", cpu_threads=6, compute_type="float32")

    def transcribe_chunk(self, bm, chunk_file):
        chunk_file+= ".wav"
        segments, _ = self.MODEL.transcribe(chunk_file, beam_size= bm, vad_filter=True)
        transcription = ' '.join(segment.text for segment in segments)
        return transcription

    def check_silence(self):
        print("checking in the background")
        while True:
            sample = self.SAMPLE.get(block=True)
            print("Checking: ", end='')
            smpl = self.transcribe_chunk(7,sample)
            if len(smpl) == 0:
                # print("Check passed\n")
                self.RESUME1.put(False, block=True)
                self.RESUME2.put(False, block=True)
                return
            else:
                print("Check failed\n")


    def rec(self,file:str,dur:int|None = None)-> None:
        """
        Function to record audio using the soundevice library and save the audio to a file 
        using the soundfile library
        PARAMETERS: 
        dur - duration of recording as int
        file - name of the file without extension to store the audio in as str. '.wav' will be added automatically
        wait - a boolean to check whether the rec() has to wait to record the audio for the specified duration or 
            run a while loop looking for the RESUME variable
        play - a boolean to check whether the recorded audio needs to be played back"""
        
        if dur:
            fs = 44000
            sd.default.samplerate = fs
            sd.default.channels = 1
        else:
            r = Recorder(channels=1, rate=16000)
        # print("recording", file)
        if dur:
            i = 1
            while True:
                try:
                    r = self.RESUME1.get(timeout=0.1)
                    if not r:
                        break
                except:
                    myarray =  sd.rec(int(dur* fs))
                    sd.wait()
                    sf.write(f"{file}.wav", myarray, fs)
                    self.SAMPLE.put(file, block=True)
                    
            return
        else:
            cue, sr1 = sf.read("start-tone.wav")
            end, sr2 = sf.read("end-tone.wav")
            sd.play(cue,sr1,blocking=True)
            
            r.start()
            while True:
                if not self.RESUME2.get(block=True):
                    print("STOPPED")
                    r.stop()
                    sd.play(end,sr2)
                    sd.wait()
                    r.save(file)
                    transcription = self.transcribe_chunk(5, file)
                    if __name__ == "__main__":
                        print("     T R A N S C R I P T I O N     \n",'-'*36,'\n',transcription)
                    break
            self.RESULT.put(transcription, block=True)     
            return 


    def listen(self) -> str:
        result = Thread(target = self.rec, args=("audio",))
        sample = Thread(target = self.rec, args=("sample", 3))
        checker = Thread(target = self.check_silence)
        result.start()
        sample.start()
        checker.start()
        print("Listening")
        result.join()
        return self.RESULT.get(block=True)
    


if __name__ == "__main__":
    listener = Listener()
    result = listener.listen()
    print(result)


