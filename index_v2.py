import tkinter
from tkinter import X, Menu, ttk
from tkinter import filedialog
import arabic_reshaper
from bidi.algorithm import get_display
#---------------------------------------------------
class parageraph: # class for paragraph
    pr=str() 
    
    def __init__(self,text) : # text is one parageraph
        if text != "\n" :
            self.pr=text
    def main_words(self,content) : # content should be all parageraphs # this method find words that len >=3 and exist in content >= 2
        self.temp_words1=list()     # contain words that len ()>=3 , without repeat words
        self.temp_words2=dict()
        self.pr=self.pr.lower() 
        self.pr=self.pr.split()
        for a in self.pr: # making temp_words1 include words that len(>=3)
            if len(a)>=3:
                if a not in self.temp_words1:
                    self.temp_words1.append(a)
        for sent in content :
            sent=sent.split()            
            for b in sent : # counting temp_words 1 ( to find that how many of them are bigger than 2 )
                if b in self.temp_words1:
                    if b not in self.temp_words2 :
                        self.temp_words2[b]=1
                    else :
                        self.temp_words2[b]+=1
        self.words=list()                
        for c in self.temp_words2 : # check if any elemnt of dict temp_words2 value bigger than 2 : add it to words (main words) 
            if self.temp_words2[c]>=2:
                self.words.append(c)                 
#----------------------------------------------------
def sim (l_p_1,l_p_2): 
    data=dict()
    for a in l_p_1: # for each *word* in l_p_1
        for b in l_p_2: # for each *word* in l_p_2

            union=0 # ejtema
            intersection=0 # eshterak
            for c in a.words :
                if c in b.words:
                    intersection+=1
            union=len(a.words)+len(b.words)-intersection
            if union==0 :
                if len(a.words)==0 or len(b.words)==0 : 
                    print(f"ERROR ! sim paragraph {l_p_1.index(a)+1} file 1 and paragraph {l_p_2.index(b)+1} file 2 : no words in paragraph")
                else:    
                    data[f"sim paragraph {l_p_1.index(a)+1} file 1 and paragraph {l_p_2.index(b)+1} file 2 :"]=0
                
            else :
                data[f"sim paragraph {l_p_1.index(a)+1} file 1 and paragraph {l_p_2.index(b)+1} file 2 :"]=intersection/union

    return data 
#----------------------            
def output_main (data): 
    length=len(data) 
    temp=(sum(data.values())/length)*100 # sum of values of dict data , divide by length of dict data , multiply by 100
    return(f"total similarity : {round(temp)}%") 
#----------------------
def output_detail(data): # this method print details of similarity between two files
    global data_for_detail
    warn=False
    data_for_detail="" 
    for a in data:
        if data[a]>=0.5:
            data_for_detail+=a+str(round(data[a],2))+"\n"+"similarity is high !!!"+"\n"
            warn=True
        else:    
            data_for_detail+=a+str(round(data[a],2))+"\n"
    if warn==True:
        return("there is some similarity between parageraphs\nplease check details")
    else:
        return("")         
  
#----------------------------------------------------
path1=""
path2=""
text1=""
text2=""
f1=""
f2="" 
lang="english"
data_for_detail=""
def main(): # this method check if language is english or persian, if persian encode  and reshape it
    try:
        global f1
        global f2
        global text1
        global text2
        if lang=="persian":
            text1=""
            text2=""
            f1=""
            f2=""
            f1=open(path1,"r",encoding="utf-8")
            f2=open(path2,"r",encoding="utf-8")
            for line in f1:
                reshaped_line = arabic_reshaper.reshape(line)
                text1=text1+get_display(reshaped_line)
            for line in f2:
                reshaped_line = arabic_reshaper.reshape(line)
                text2=text2+get_display(reshaped_line)
                
            f1.close(),f2.close()
        elif lang=="english": 
            text1=""
            text2=""
            f1=""
            f2=""
            f1=open(path1)
            f2=open(path2)
            for line in f1:
                text1=text1+line
            for line in f2:
                text2=text2+line
            f1.close(),f2.close() 
    except:
        print("error in opening files")       
# ui lang bu language checker
def english(): 
    global lang
    lang="english"
    lbl.configure(text="txt file similarity checker",)
    lbl.place_configure(width=170)
    lbl2.configure(text="main result")
    btn.configure(text="open file 1")
    btn2.configure(text="open file 2")
    btn3.configure(text="check similarity")
    btn4.configure(text="more details")
def persian():
    global lang
    lang="persian"
    lbl.configure(text="بررسی تقلب فایل های متنی",font=("Arial",12))
    lbl.place_configure(width=150)
    lbl2.configure(text="نتیجه نهایی")
    lbl2.place(x=100,y=180,width=280,height=30)
    btn.configure(text="انتخاب فایل اول")
    btn2.configure(text="انتخاب فایل دوم")
    btn3.configure(text="بررسی")
    btn4.configure(text=" نمایش  جزئیات بیشتر")
    btn4.place(height=30,width=150,x=50,y=260)       
#----------------------------------------------------
def clicked ():
    global path1
    path1 = filedialog.askopenfilename (initialfile = 'Untitled.txt' , title="Open Text file",   defaultextension=".txt",filetypes=[("Text Documents","*.txt")])
def clicked2 ():
    global path2
    path2 = filedialog.askopenfilename (initialfile = 'Untitled.txt' , title="Open Text file",   defaultextension=".txt",filetypes=[("Text Documents","*.txt")])
def clicked3 ():
    global text1
    global text2
    main() # + check language
    text1=text1.split("\n")
    text2=text2.split("\n")

    l_p_1=list() # a list that elements are object of class parageraph , that from text 1
    l_p_2=list() # "         "        "       "           "            " , that from text 2

    for i in text1 :
            temp=parageraph(i)
            temp.main_words(text1)
            l_p_1.append(temp)
    for j in text2 :
            temp=parageraph(j)
            temp.main_words(text2)
            l_p_2.append(temp)
    warn_and_detail=output_detail(sim(l_p_1,l_p_2))           
    lbl3.configure(text=output_main(sim(l_p_1,l_p_2))+"\n"+warn_and_detail)
             
def clicked4 (): 
    global data_for_detail
    root4=tkinter.Tk()
    root4.title("Detail")
    root4.geometry("300x300")
    lbl4=ttk.Label(root4,text="")
    lbl4.configure(text=("-"*10)+"\n"+data_for_detail)
    lbl4.pack()
    lbl4.place(x=0,y=0)
    root4.mainloop() 
#----------------------------------------------------
root=tkinter.Tk()
root.geometry("270x320")
root.resizable(False,False)
root.title("similarity checker")
#---------
menubar=Menu(root)
root.config(menu=menubar)
mainmenue=Menu(menubar)
menubar.add_cascade(label="language", menu=mainmenue)
mainmenue.add_command(label="English",command=english)
mainmenue.add_command(label="Persian",command=persian)
#---------
lbl=ttk.Label(root,text="txt file similarity checker",border=2,relief="raised",font=("Arial",10,"bold"))
lbl.place(x=50,y=10,width=170,height=30)
lbl.configure(foreground="black")
#---------
btn=ttk.Button(root,text="open file 1",command=clicked)
btn.place(height=30,width=100,x=80,y=60)
#---------
btn2=ttk.Button(root,text="open file 2",command=clicked2)
btn2.place(height=30,width=100,x=80,y=100)
#---------
btn3=ttk.Button(root,text="check similarity",command=clicked3)
btn3.place(height=30,width=100,x=80,y=140)
#---------
lbl2=ttk.Label(root,text=" main resault",border=2,font=("Arial",10,"bold"))
lbl2.place(x=80,y=180,width=280,height=30)
#---------
lbl3=ttk.Label(root,text="",border=2,relief="solid",background="white")
lbl3.place(x=10,y=205,width=250,height=50)
#---------
btn4=ttk.Button(root,text="more details",command=clicked4)
btn4.place(height=30,width=100,x=80,y=260)
#---------
lbl4=ttk.Label(root,text="made with 💛 by @rezaaem",border=2,relief="solid",background="black",foreground="gold",anchor="center")
lbl4.place(x=0,y=299,width=270,height=25)
lbl4.configure()
root.mainloop()    
