import pyaudio
import wave

class recoder:
    def __init__(self, chunk=1024, format=pyaudio.paInt16, channels=2, rate=44100, p=pyaudio.PyAudio()):
       
        self.FORMAT = format
        self.CHANNELS = channels
        self.RATE = rate
        self.CHUNK = chunk
        self.p = p
        self.frames = []
        

        self.STARTED = False
        self.PAUSED = False

    def start(self) : 
        print('START', (self.STARTED, self.PAUSED))
        if not self.STARTED:
            self.STARTED = True
            self.stream = self.p.open(
                format=self.FORMAT, 
                channels=self.CHANNELS, 
                rate=self.RATE, 
                input=True, 
                frames_per_buffer=self.CHUNK
            )


        elif self.PAUSED: 
            self.PAUSED = False
            self.stream.start_stream()
        
        # while self.STARTED and not self.PAUSED:
        #     data = self.stream.read(self.CHUNK)
        #     self.frames.append(data)
        #     self.main.update()

    def get_data(self):
        data = self.stream.read(self.CHUNK)
        self.frames.append(data)

    def pause(self) : 
        print('PAUSE', (self.STARTED, self.PAUSED))
        self.PAUSED = True 
        self.stream.stop_stream()
    
    def resume(self) : 
        self.start()
    
    def stop(self) : 
        print('STOP', (self.STARTED, self.PAUSED))
        self.STARTED = False
        self.PAUSED = False
        self.stream.close()
        

    def write(self, path) : 
        wf = wave.open(path, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        self.frames = []
        