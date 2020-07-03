import recorder
import tkinter
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import constants
import crawler
import re
import os
def split_sentences(content):
    return re.split(r'\.\s', content)

class GUI :
    def __init__(self) : 
        self.recorder = recorder.Recorder()
        self.main = tk.Tk()
        self.collections = []
        self.main.geometry('1000x580')
        self.main.title('Recording')


        self.header = tk.Label(self.main, text='RECORDER',fg='white',pady=30,background='#4d4d4d')
        self.header.pack(fill=tk.X)
        self.submit_button = tk.Button(self.header,padx=100,pady=30, text='SUBMIT', bg='#00e600', fg='white', command=self.handle_submit)
        self.submit_button.pack(side=tk.RIGHT)

        self.left_bar = tk.Frame(self.main)
        self.left_bar.pack(side=tk.LEFT, fill=tk.Y)

        self.categories_buttons = []
        for category_path, category_name in constants.categories.items() : 
            select_category_btn = tk.Button(self.left_bar, text=category_name, fg='white', bg='#666666')
            select_category_btn.bind("<ButtonPress-1>", lambda event, arg=category_path: self.handle_select_category(event, arg))
            select_category_btn.pack(fill=tk.X)
            self.categories_buttons.append(select_category_btn)

        self.start_pause_button = tk.Button(self.main ,padx=100,pady=30, text='START', bg='#737373', fg='white', command=self.handle_start_pause)
        self.start_pause_button.pack( fill=tk.X,side=tk.BOTTOM)

        self.current = {
            "category" : None,
            "sentence_no" : None,
            "article_url" : None
        }

        self.fetched_article_sentences = None

        self.target_text = tk.Label(self.main, text='', bg='white', pady=20, wraplength=500)
        self.target_text.pack(fill=tk.BOTH)

        self.next_button = tk.Button(self.main, text='NEXT', bg='blue', fg='white', pady=10, padx=20, command=self.handle_next_sentence)
        self.next_button.pack(side=tk.BOTTOM)
        self.main.mainloop()
        

    def handle_next_sentence(self) : 
        self.current['sentence_no'] = self.current['sentence_no'] + 1
        try :
            self.target_text.config(text=self.fetched_article_sentences[self.current['sentence_no']])
        except Exception : 
            self.target_text.config(text='')
        
    def handle_select_category(self,event, selected_category) :
        self.current['category'] = selected_category
        self.current['sentence_no'] = 0

        content, article_url = crawler.get_content_by_category(self.current['category'])
        self.current['article_url'] = article_url

        meta_file_path = 'data/%s/meta.txt' % self.current['category']
        os.makedirs(os.path.dirname(meta_file_path), exist_ok=True)
        f = open(meta_file_path, 'w+')
        f.write(article_url + '\n')
        f.close()

        sentences = split_sentences(content)
        self.fetched_article_sentences = sentences
        # print(self.fetched_article_sentences[self.current['sentence_no']])
        self.target_text.config(text=self.fetched_article_sentences[self.current['sentence_no']])

    def start_recording(self) : 
        self.recorder.start()
        while self.recorder.STARTED and not self.recorder.PAUSED : 
            self.recorder.get_data()
            self.main.update()


    def handle_submit(self) : 
        self.recorder.stop()
        self.write_data()
        self.start_pause_button.config(text='START', bg='#737373')
        

        self.handle_next_sentence()

    def write_data(self): 
        audio_file_name = '%s.wav' % str(self.current['sentence_no'])
        self.recorder.write('data/%s/%s' % (self.current['category'], audio_file_name))

        f = open('data/%s/meta.txt' % self.current['category'], 'a+')
        f.write(audio_file_name + '\n')
        f.write(self.fetched_article_sentences[self.current['sentence_no']] + '\n')
        f.close()


    def handle_start_pause(self):
        print(self.recorder.STARTED)
        if not self.recorder.STARTED or self.recorder.PAUSED:
            self.start_pause_button.config(text='PAUSED', bg='#ff3333')
            self.start_recording()
            
            print('1',self.recorder.STARTED, self.recorder.PAUSED)
        # elif self.recorder.PAUSED : 

        #     self.start_pause_button.config(text='PAUSED', bg='#ff3333')
        #     print('2',self.recorder.STARTED, self.recorder.PAUSED)
        else :   
            self.start_pause_button.config(text='RESUME', bg='#737373') 
            self.recorder.pause()
            
            print('3',self.recorder.STARTED, self.recorder.PAUSED)

    
GUI()