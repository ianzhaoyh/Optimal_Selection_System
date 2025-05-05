# front.py // frontend
import tkinter as tk
from tkinter import *
import tkinter.messagebox as messagebox
import Algorithm as back
import random as ra
import db
import os
import config as thread_running
from threading import Thread
import sys


global_t = 0
global_s = 0
global_e = list()
global_ran = list()
global_ans = list()

class TextRedirector(): 
    def __init__(self, widget): 
        self.widget = widget 
    def write(self, str): 
        self.widget.insert(tk.END, str) 
        self.widget.see(tk.END) 
    def flush(self): 
        pass

def input_n(entries,text_widget):
    text_v.delete('1.0','end')   
    entered_numbers.clear()
    i=0
    if(m_text.get().strip() and n_text.get().strip()):
        m_B = int(m_text.get().strip())
        n_B = int(n_text.get().strip())
    else:
        messagebox.showwarning("Input error", "Please enter the values of m and n!")
        return False
    validate_m=check_range1(m_B)
    validate_n=check_range2(n_B)
    if(validate_m and validate_n) == False:
        return False
    for Entry_List in entries:
        if Entry_List.get().strip():
            value = int(Entry_List.get().strip())
            if(value not in entered_numbers):
                entered_numbers.add(value)
            else:
                messagebox.showwarning("Input error", f"The number {value} is repeated, please re-enter it.")
                Entry_List.delete(0,"end")
                return False  
            i=i+1
            if not 1 <= value <= 54:
                messagebox.showwarning("Input error", f"The input value of the {i}th position must be between 1 and 54")  
                Entry_List.delete(0,"end")
                return False  
    if not i == n_B:
        for Entry_List in entries:
            Entry_List.delete(0,"end")
        messagebox.showwarning("Input error", f"The number of values entered should be equal to {n_B}")
        return False
    sys.stdout=TextRedirector(text_v) 
    global global_ran
    contents = [Entry_List.get() for Entry_List in entries if Entry_List.get().strip()] 
    global_ran = []
    global_ran = contents
    if contents:
        formatted_content = f"[{', '.join(contents)}]"  
        text_widget.insert(tk.END, formatted_content + '\n') 

def random_n():
    text_v.delete('1.0','end')
    if(m_text.get().strip() and n_text.get().strip()):
        m_B = int(m_text.get().strip())
        n_B = int(n_text.get().strip())
    else:
        messagebox.showwarning("Input error", "Please enter the values of m and n!")
        return False
    validate_m=check_range1(m_B)
    validate_n=check_range2(n_B)
    if(validate_m and validate_n) == False:
        return False
    sys.stdout=TextRedirector(text_v)
    global global_ran
    global_ran = list()
    for i in range (int(m_B)):
        global_ran.append(int(i+1))
    global_ran = ra.sample(global_ran, int(n_B))
    print(global_ran)

def storeDB():
    sys.stdout=TextRedirector(text_r)
    i=1
    j=0
    int(i)
    int(j)
    all_full = True
    for Rbutton_List in radio_buttons:
        if Rbutton_List.cget("text") == f"{m_text.get()}-{n_text.get()}-{k_text.get()}-{j_text.get()}-{s_text.get()}-{i}":
            i=i+1
    for Rbutton_List in radio_buttons:
        if Rbutton_List.cget("text") == "                      ":
            Rbutton_List.config(text=f"{m_text.get()}-{n_text.get()}-{k_text.get()}-{j_text.get()}-{s_text.get()}-{i}")
            db.Fstore(global_ans,Rbutton_List.cget("text"),j)
            all_full = False
            messagebox.showinfo("Storage completed!","Data saved successfully.")
            return True
        j=j+1
    if all_full:
        messagebox.showwarning("Wrong operation","Database is full!")
        return False


def Display():
    text_d.delete('1.0', tk.END)
    selected_option=selected_v.get()
    sys.stdout=TextRedirector(text_d)
    example=db.Fload(selected_option) 
    tag = db.Fget(selected_option)
    example = list(example)
    i=1
    for each in example:
        print(str(i)+'. '+str(each))
        i+=1
    print(tag)

def Delete_DB():
    text_d.delete('1.0', tk.END)
    selected_option=selected_v.get()
    db.Fdel(selected_option)
    for Rbutton_List in radio_buttons:
        if int(Rbutton_List.cget("value")) == selected_option:
            Rbutton_List.config(text="                      ")


def Next():
    window1.deiconify()
    root.withdraw()

def Previous1():
    window1.withdraw()
    root.deiconify()


def Previous2():
    window1.deiconify()
    window2.withdraw()

def select_window3():
    window3.deiconify()
    window2.withdraw()

def select_window4():
    window4.deiconify()
    window2.withdraw()
    
def select_window5():
    window2.withdraw()
    window5.deiconify()

def backwin2_1():
    window3.withdraw()
    window2.deiconify()

def backwin2_2():
    window4.withdraw()
    window2.deiconify()

def backwin2_3():
    window5.withdraw()
    window2.deiconify()

def Next1():
    window3.withdraw()
    window1.deiconify()

def Next2():
    window4.withdraw()
    window1.deiconify()

def Next3():
    window5.withdraw()
    window1.deiconify()


def Stop():
    thread_running.set(False)
    print("Threads have been ended.")


def Execute():
    thread_running.init()
    def thread_function():
        global global_t, global_s, global_e
        sys.stdout=TextRedirector(text_r)
        text_r.delete('1.0','end')
        content = text_v.get("1.0", "end-1c")
        n_B = n_text.get()
        k_B = k_text.get()
        j_B = j_text.get()
        s_B = s_text.get()
        a_B = a_text.get()

        # 参数a为用户输入的“at least samples”的值
        a_B = a_text.get()
        if m_text.get()==" " or n_B==" " or k_B==" " or j_B==" " or s_B==" " or content=="" or a_B==" ":
            messagebox.showwarning("Input error", "Please select samples first!")
            return False
        print("Loading...")
        print("If the process takes too long, you may choose to ")
        print("stop it.")
        
        global_t, global_s, global_e = back.manipulate(n_B, k_B, j_B, s_B, a_B)
        
        text_r.delete('1.0','end')
        if global_s == 0:
            print("successfully stopped!")
        else:
            print(f"running time:{global_t}")
            print(f"sample size:{global_s}")
            global global_ran
            global global_ans
            global_ans = list()
            for i in range(len(global_e)):
                tuplist = list()
                for j in range(len(global_e[i])):
                    no = int(global_e[i][j])
                    el = int(global_ran[no])
                    tuplist.append(el)
                print(tuplist)
                tuplist = tuple(tuplist)
                global_ans.append(tuplist)

    thread = Thread(target=thread_function)
    thread.start()


def DELETE():
    text_r.delete('1.0','end')
    text_v.delete('1.0','end')
    m_B.delete(0,"end")
    m_B.insert(0, ' ') 
    n_B.delete(0,"end")
    n_B.insert(0, ' ') 
    k_B.delete(0,"end")
    k_B.insert(0, ' ') 
    j_B.delete(0, "end")
    j_B.insert(0, ' ') 
    s_B.delete(0, "end")
    s_B.insert(0, ' ') 
    for Entry_List in entries:
        Entry_List.delete(0, "end")
        Entry_List.insert(0, ' ')
        
def check_range1(V):
    if V == " ":
        return True 
    try:
        value = int(V)
        if 45 <= value <= 54:
            return True
        else:
            messagebox.showwarning("Input error", "The input value of m must be between 45 and 54!")
            m_B.delete(0,"end")
            return False
    except ValueError:
        messagebox.showwarning("Input error", "Please enter a valid integer!")
        m_B.delete(0,"end")
        return False
    
def check_range2(V):
    if V == " ":
        return True 
    try:
        value = int(V)
        if 7 <= value <= 25:
            return True
        else:
            messagebox.showwarning("Input error", "The input value of n must be between 7 and 25!")
            n_B.delete(0,"end")
            return False
    except ValueError:
        messagebox.showwarning("Input error", "Please enter a valid integer!")
        n_B.delete(0,"end")
        return False
    
def check_range3(V):
    if V == " ":
        return True 
    try:
        value = int(V)
        if j_B.get().strip():
            j_value = int(j_B.get().strip())
            if not (value >= j_value):
                messagebox.showwarning("Input error", f"The input value of k must be bigger than {j_value}!")
                k_B.delete(0,"end")
                return False
        elif s_B.get().strip():
            s_value = int(k_B.get().strip())
            if not (value >= s_value):
                messagebox.showwarning("Input error", f"The input value of k must be bigger than {s_value}!")
                k_B.delete(0,"end")
                return False
        if 4 <= value <= 7:
            return True
        else:
            messagebox.showwarning("Input error", "The input value of k must be between 4 and 7!")
            k_B.delete(0,"end")
            return False
    except ValueError:
        messagebox.showwarning("Input error", "Please enter a valid integer!")
        k_B.delete(0,"end")
        return False
    
def check_range4(V):
    if V == " ":
        return True 
    try:
        value = int(V)
        if (k_B.get().strip() and s_B.get().strip()):
            k_value = int(k_B.get().strip())
            s_value = int(s_B.get().strip())
            if not (s_value <= value <= k_value):
                messagebox.showwarning("Input error", f"The input value of j must be between {s_value} and {k_value}!")
                j_B.delete(0,"end")
                return False
        elif (k_B.get().strip()):
            k_value = int(k_B.get().strip())
            if not (3 <= value <= k_value):
                messagebox.showwarning("Input error", f"The input value of j must be between 3 and {k_value}!")
                j_B.delete(0,"end")
                return False
        elif (s_B.get().strip()):
            s_value = int(s_B.get().strip())
            if k_value is not None and not (s_value <= value <= k_value):
                messagebox.showwarning("Input error", f"The input value of j must be between {s_value} and 7!")
                j_B.delete(0,"end")
                return False
        if (3 <= value <= 7):
            return True
        else:
            messagebox.showwarning("Input error", "The input value of j must be between 3 and 7!")
            j_B.delete(0,"end")
            return False
    except ValueError:
        messagebox.showwarning("Input error", "Please enter a valid integer!")
        j_B.delete(0,"end")
        return False

def check_range5(V):
    if V == " ":
        return True 
    try:
        value = int(V)
        if j_B.get().strip():
            j_value = int(j_B.get().strip())
            if not (value <= j_value):
                messagebox.showwarning("Input error", f"The input value of s must be smaller than {j_value}!")
                s_B.delete(0,"end")
                return False
        elif k_B.get().strip():
            k_value = int(k_B.get().strip())
            if not (value <= k_value):
                messagebox.showwarning("Input error", f"The input value of s must be smaller than {k_value}!")
                s_B.delete(0,"end")
                return False
        if 3 <= value <= 7:
            return True
        else:
            messagebox.showwarning("Input error", "The input value of s must be between 3 and 7!")
            s_B.delete(0,"end")
            return False
    except ValueError:
        messagebox.showwarning("Input error", "Please enter a valid integer!")
        s_B.delete(0,"end")
        return False

def Store_DBN():
    num=int(0)
    selected = selected_o.get()
    for Rbutton_List in radio_buttons:
            if int(Rbutton_List.cget("value")) == selected_v.get():
                T=Rbutton_List.cget("text")
                break
    if selected == 1:
        for Rbutton_List in radio_buttons:
            if Rbutton_List.cget("text")=="                      ":
                Rbutton_List.config(text=window3_entry4.get())
                break
            else:
                num=num+1
        selected_value = window3_selected.get()
        value0=selected_v.get()
        value1, value2, value3 = window3_entry1[0].get(), window3_entry1[1].get(), window3_entry1[2].get() 
        if selected_value == 0:
            value4, value5, value6 = window3_entry2[0].get(), window3_entry2[1].get(), window3_entry2[2].get()
            R1=rf.Ref1(db.Fload(value0), value1, value2, value3, selected_value, value4, value5, value6)
            db.Fstore(R1,T,num)
        if selected_value == 1:
            value7, value8, value9 = window3_entry3[0].get(), window3_entry3[1].get(), window3_entry3[2].get()
            R2=rf.Ref1(db.Fload(value0), value1, value2, value3, selected_value, value7, value8, value9)
            db.Fstore(R2,T,num)
    elif selected == 2:
        for Rbutton_List in radio_buttons:
            if Rbutton_List.cget("text")=="                      ":
                Rbutton_List.config(text=window4_entry4.get())
                break
            else:
                num=num+1
        selected_value = window4_selected.get()
        value0=selected_v.get()
        value1, value2, value3 = window4_entry1[0].get(), window4_entry1[1].get(), window4_entry1[2].get()
        if selected_value == 0:
            value4, value5, value6 = window4_entry2[0].get(), window4_entry2[1].get(), window4_entry2[2].get()
            value7, value8, value9 = window4_entry21[0].get(), window4_entry21[1].get(), window4_entry21[2].get()
            R1=rf.Ref2(db.Fload(value0), value1, value2, value3, selected_value, value4, value7, value5,value8, value6, value9)
            db.Fstore(R1,T,num)
        if selected_value == 1:
            value10, value11, value12 = window4_entry3[0].get(), window4_entry3[1].get(), window4_entry3[2].get()
            value13, value14, value15 = window4_entry22[0].get(), window4_entry22[1].get(), window4_entry22[2].get()
            R2=rf.Ref2(db.Fload(value0), value1, value2, value3, selected_value, value10, value13, value11,value14, value12, value15)
            db.Fstore(R2,T,num)
    elif selected == 3:
        for Rbutton_List in radio_buttons:
            if Rbutton_List.cget("text")=="                      ":
                Rbutton_List.config(text=window5_entry4.get())
                break
            else:
                num=num+1
        value0=selected_v.get()
        value1, value2, value3 = window5_entry2[0].get(), window5_entry2[1].get(), window5_entry2[2].get()
        value4 = window5_entry3.get()
        R1=rf.Ref3(db.Fload(value0),value1, value2, value3,value4)
        db.Fstore(R1,T,num)

def disable_input(event):
    return "break"


#root S1

root = tk.Tk()
root.title("An Optimal Samples Selection System")

window1 = tk.Toplevel(root)
window1.withdraw()

window2 = tk.Toplevel(root)
window2.withdraw()

frame1 = tk.Frame(root)
frame1.grid(row=0,column=0)

frame2 = tk.Frame(root)
frame2.grid(row=10,column=0)

entered_numbers = set()

system_Title = tk.Label(frame1, text="An Optimal Samples Selection System",font=('Arial',25))
system_Title.grid(row=0,column=2,pady=10,columnspan=5,padx=(20,0))

req=tk.Label(frame1,text="Please input the following parameters")
req.grid(row=1,column=4,pady=10,columnspan=2)

def setup_validation():
    vcmd1 = root.register(lambda V: check_range1(V)), '%P'
    vcmd2 = root.register(lambda V: check_range2(V)), '%P'
    vcmd3 = root.register(lambda V: check_range3(V)), '%P'
    vcmd4 = root.register(lambda V: check_range4(V)), '%P'
    vcmd5 = root.register(lambda V: check_range5(V)), '%P'
    m_B.configure(validate="focusout", validatecommand=vcmd1)
    n_B.configure(validate="focusout", validatecommand=vcmd2)
    k_B.configure(validate="focusout", validatecommand=vcmd3)
    j_B.configure(validate="focusout", validatecommand=vcmd4)
    s_B.configure(validate="focusout", validatecommand=vcmd5)

m=tk.Label(frame1,text="m")
m.grid(row=2,column=0,pady=10,padx=(10,0),sticky='W')

m_text=StringVar()
m_text.set(" ")
m_B = tk.Entry(frame1,textvariable = m_text)
m_B.grid(row=2,column=1,pady=10,padx=(10,0))

m_R = tk.Label(frame1,text="45≤m≤54")
m_R.grid(row=2,column=2,pady=10,padx=(14,0))

n=tk.Label(frame1,text="n")
n.grid(row=2,column=3,pady=10,padx=(40,0))

n_text=StringVar()
n_text.set(" ")
n_B = tk.Entry(frame1,textvariable = n_text)
n_B.grid(row=2,column=4,pady=10,sticky='W',padx=(10,0))

n_R = tk.Label(frame1,text="7≤n≤25")
n_R.grid(row=2,column=5,pady=10,sticky='W')

k=tk.Label(frame1,text="k")
k.grid(row=3,column=0,pady=10,padx=(10,0))

k_text=StringVar()
k_text.set(" ")
k_B = tk.Entry(frame1,textvariable = k_text)
k_B.grid(row=3,column=1,pady=10,padx=(10,0))

k_R = tk.Label(frame1,text="4≤k≤7")
k_R.grid(row=3,column=2,pady=10)

j=tk.Label(frame1,text="j")
j.grid(row=3,column=3,pady=10,padx=(40,0))

j_text=StringVar()
j_text.set(" ")
j_B = tk.Entry(frame1,textvariable = j_text)
j_B.grid(row=3,column=4,pady=10,padx=(10,0),sticky='W')

j_R = tk.Label(frame1,text="s≤j≤k")
j_R.grid(row=3,column=5,pady=10,sticky='W')

s=tk.Label(frame1,text="s")
s.grid(row=3,column=6,pady=10,padx=(40,0))

s_text=StringVar()
s_text.set(" ")
s_B = tk.Entry(frame1,textvariable = s_text)
s_B.grid(row=3,column=7,pady=10,padx=(10,0))

s_R = tk.Label(frame1,text="3≤s≤7")
s_R.grid(row=3,column=8,pady=10,padx=(20,10))

user_input_n = tk.Label(frame1,text="User input:",font=('Arial',12))
user_input_n.grid(row=9,column=1,columnspan=2,pady=10)


v = IntVar() 

random = tk.Radiobutton(frame1, text="Random n", variable=v, value=1,command=random_n)
random.grid(row=5,column=1,pady=10)

input = tk.Radiobutton(frame1, text="Input n", variable=v, value=2,command=lambda:input_n(entries,text_v))
input.grid(row=5,column=2,pady=10)

# 新增at least (  ) S samples
at_least_label = tk.Label(frame1, text="at least")
at_least_label.grid(row=4, column=2, pady=5, padx=(5, 0), sticky='E')

a_text = StringVar()
a_text.set(" ")
a_B = tk.Entry(frame1, textvariable=a_text, width=15)
a_B.grid(row=4, column=3, pady=10, padx=(5, 0), sticky='W')

s_samples_label = tk.Label(frame1, text="s sample")
s_samples_label.grid(row=4, column=3, pady=10, padx=(5, 0), sticky='E')

# Execute 按钮的位置
execute = tk.Button(frame1, text="Execute", command=Execute)
execute.grid(row=5, column=6, pady=10)

# Store 按钮的位置
store = tk.Button(frame1, text="Store", command=storeDB)
store.grid(row=5, column=7, pady=10)

# Stop 按钮的位置
end = tk.Button(frame1, text="Stop", command=Stop)
end.grid(row=5, column=8, pady=10)

# Delete 按钮的位置
Delete = tk.Button(frame1, text="Clear", command=DELETE)
Delete.grid(row=5, column=9, pady=10)

#clear?

Print = tk.Button(frame1,text="print")
Print.grid(row=7,column=8,sticky='WN')

next = tk.Button(frame1,text="NEXT",command=Next)
next.grid(row=7,column=10,sticky='WN')


value_input = tk.Label(frame1, text="value input")
value_input.grid(row=6,column=1,pady=10,sticky='E')

results = tk.Label(frame1, text="results")
results.grid(row=6,column=5,pady=10,sticky='W',padx=(55,0))


text_v = tk.Text(frame1,height=10,width=41)
text_v.insert(tk.END," ")
text_v.grid(row=7,column=0,columnspan=5,rowspan=2,sticky='W',padx=(5,0))

scrollbar_v = tk.Scrollbar(frame1)
scrollbar_v.grid(row=7, column=3, sticky='ns',rowspan=2)

text_v.config(yscrollcommand=scrollbar_v.set)
scrollbar_v.config(command=text_v.yview)

text_r = tk.Text(frame1,height=10,width=52)
text_r.insert(tk.END," ")
text_r.grid(row=7,column=4,columnspan=5,rowspan=2,sticky='W',padx=(55,0))

scrollbar_r = tk.Scrollbar(frame1)
scrollbar_r.grid(row=7, column=7,sticky='ns',rowspan=2)

text_r.config(yscrollcommand=scrollbar_r.set)
scrollbar_r.config(command=text_r.yview)

i=0
entries=[tk.Entry(frame2,width=2) for _ in range(25)]
for Entry_List in entries:
    Entry_List.grid(row=1,column=2*i,columnspan=2,padx=(10,0))
    i=i+1
j=0
labels=[tk.Label(frame2,text=str(j+1)) for j in range(0,25)]
for Label_List in labels:
    Label_List.grid(row=2,column=2*j,columnspan=2,padx=(10,0))
    j=j+1

root.after(100, setup_validation)

#S2 database

frame3 = tk.Frame(window1)
frame3.grid(row=0,column=0)

frame4 = tk.Frame(window1)
frame4.grid(row=1,column=0)

frame5 = tk.Frame(window1)
frame5.grid(row=2,column=0)

frame6 = tk.Frame(window1)
frame6.grid(row=8,column=0)

window1_Title = tk.Label(frame3, text="An Optimal Samples Selection System",font=('Arial',25))
window1_Title.grid(row=0,column=2,pady=10,columnspan=10,padx=20)
    
DBR = tk.Label(frame4, text="Data Base Resource",font=('Arial',12))
DBR.grid(row=1,column=0,columnspan=5,padx=20)

display = tk.Button(frame4,text="Display",command=Display)
display.grid(row=1,column=7,columnspan=3,padx=20)

delete = tk.Button(frame4,text="Delete",command=Delete_DB)
delete.grid(row=1,column=12,columnspan=3,padx=20)

selected_v = tk.IntVar(value=0)
selected_v.set("0")

radio_buttons = [tk.Radiobutton(frame5,text="                      ",variable=selected_v,value=k) for k in range(0,12)]
for l,Rbutton_List in enumerate(radio_buttons):
    Rbutton_List.grid(row=int(l/3), column=l%3, columnspan=2, padx=100,pady=5,sticky='W')

#path = os.path.abspath(os.path.dirname(sys.argv[0])) + "\\db\\"  win写法
path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "db")
os.makedirs(path, exist_ok=True)  #跨平台写法
flist = os.listdir(path)
for each in flist:
    fno = int(each[0])
    eno=int(0)
    for Rbutton_List in radio_buttons:
        if eno==fno:
            Rbutton_List.config(text=db.Fget(fno))
        eno += 1


text_d = tk.Text(frame6,height=10,width=40)
text_d.insert(tk.END," ")
text_d.grid(row=6,column=0,columnspan=5,rowspan=3,sticky='W',padx=10)

scrollbar_d = tk.Scrollbar(frame6)
scrollbar_d.grid(row=6, column=5, sticky='ns',rowspan=3)

text_d.config(yscrollcommand=scrollbar_d.set)
scrollbar_d.config(command=text_d.yview)

previous = tk.Button(frame6,text="Back",command=Previous1)
previous.grid(row=6,column=10)



#24: new, 25: only back?

PRINT = tk.Button(frame6,text="PRINT")
PRINT.grid(row=8,column=10)

#S3

def switch_page():
    selected = selected_o.get()
    if selected == 1:
        select_window3()
    elif selected == 2:
        select_window4()
    elif selected == 3:
        select_window5()

window2_Title = tk.Label(window2, text="An Optimal Samples Selection System",font=('Arial',25))
window2_Title.grid(row=0,column=0,pady=10,padx=(20,0))

window2_option = tk.Label(window2, text="Please select the filter methods",font=('Arial',12))
window2_option.grid(row=1,column=0,pady=10,padx=(20,0))

selected_o = tk.IntVar()

Filter_M1 = tk.Radiobutton(window2, text="Define positions and numbers", variable=selected_o, value=1,font=(10))
Filter_M1.grid(row=2,column=0,pady=10,sticky="W")

Filter_M2 = tk.Radiobutton(window2, text="Define positions and range of numbers", variable=selected_o, value=2,font=(10))
Filter_M2.grid(row=3,column=0,pady=10,sticky="W")

Filter_M3 = tk.Radiobutton(window2, text="Select positions and fixed numbers", variable=selected_o, value=3,font=(10))
Filter_M3.grid(row=4,column=0,pady=10,sticky="W")

window2_previous = tk.Button(window2,text="Back",command=Previous2)
window2_previous.grid(row=5,column=0,sticky="E",pady=10,padx=(0,60))

window2_Next = tk.Button(window2,text="Next",command= switch_page)
window2_Next.grid(row=5,column=0,sticky="E",pady=10,padx=(0,20))

#S4

window3 = tk.Toplevel(root)
window3.withdraw()

frame7 = tk.Frame(window3)
frame7.grid(row=3,column=0,columnspan=10)

window3_Title = tk.Label(window3, text="An Optimal Samples Selection System",font=('Arial',25))
window3_Title.grid(row=0,column=0,pady=10,columnspan=10,padx=(20,0))

window3_LD = tk.Label(window3, text="Define positions and numbers",font=('Arial',15))
window3_LD.grid(row=1,column=0,columnspan=10,pady=10)

window3_LP = tk.Label(window3,text= "Please input 3 positions")
window3_LP.grid(row=2,column=0,pady=10,padx=10)

window3_entry1=[tk.Entry(window3,width=4) for _ in range(3)]
entry_num=1
for window3_entrylist1 in window3_entry1:
    window3_entrylist1.grid(row=2,column=entry_num,padx=(30,30))
    entry_num=entry_num+1

window3_selected = tk.IntVar()

window3_Rbutton1 = tk.Radiobutton(frame7, text="Please input the corresponding numbers", variable=window3_selected, value=0)
window3_Rbutton1.grid(row=3,column=0,pady=10,columnspan=6,sticky="W")

window3_Label1=tk.Label(frame7,text="1st position")
window3_Label1.grid(row=4,column=0,pady=10)

window3_Label2=tk.Label(frame7,text="2nd position")
window3_Label2.grid(row=4,column=2,pady=10)

window3_Label3=tk.Label(frame7,text="3rd position")
window3_Label3.grid(row=4,column=4,pady=10)

window3_entry2=[tk.Entry(frame7,width=2) for _ in range(3)]
entry_num1=1
for window3_entrylist2 in window3_entry2:
    window3_entrylist2.grid(row=4,column=int(entry_num1)*2-1)
    entry_num1=entry_num1+1

window3_Rbutton2 = tk.Radiobutton(frame7, text="Please input the numbers not to be included in the corresponding positions", variable=window3_selected, value=1)
window3_Rbutton2.grid(row=5,column=0,pady=10,columnspan=6)

window3_Label4=tk.Label(frame7,text="1st position")
window3_Label4.grid(row=6,column=0,pady=10)

window3_Label5=tk.Label(frame7,text="2nd position")
window3_Label5.grid(row=6,column=2,pady=10)

window3_Label6=tk.Label(frame7,text="3rd position")
window3_Label6.grid(row=6,column=4,pady=10)

window3_entry3=[tk.Entry(frame7,width=2) for _ in range(3)]
entry_num2=1
for window3_entrylist3 in window3_entry3:
    window3_entrylist3.grid(row=6,column=int(entry_num2)*2-1)
    entry_num2=entry_num2+1

frame8=tk.Frame(window3)
frame8.grid(row=7,column=0,columnspan=10)

window3_label7=tk.Label(frame8,text="Please name a file to create")
window3_label7.grid(row=0,column=0,pady=10,sticky="E")

window3_entry4=tk.Entry(frame8,width=50)
window3_entry4.grid(row=0,column=1,columnspan=50,pady=10)

window3_text = tk.Text(frame8,height=10,width=44)
window3_text.insert(tk.END," ")
window3_text.grid(row=1,column=0,columnspan=5,rowspan=2,sticky='W',padx=(5,0),pady=10)

window3_scrollbar = tk.Scrollbar(frame8)
window3_scrollbar.grid(row=1, column=5, sticky='ns',rowspan=2)

window3_text.config(yscrollcommand=window3_scrollbar.set)
window3_scrollbar.config(command=window3_text.yview)



window3_button2=tk.Button(frame8,text="execute",command=Store_DBN)
window3_button2.grid(row=1, column=7,padx=(10,10))

window3_button3=tk.Button(frame8,text="Back",command=backwin2_1)
window3_button3.grid(row=1, column=8,padx=(10,10))

window3_button4=tk.Button(frame8,text="Print")
window3_button4.grid(row=2, column=7,padx=(10,10))

window3_button5=tk.Button(frame8,text="NEXT",command=Next1)
window3_button5.grid(row=2, column=8,padx=(10,10))

#S5

window4 = tk.Toplevel(root)
window4.withdraw()

frame9 = tk.Frame(window4)
frame9.grid(row=3,column=0,columnspan=10)

window4_Title = tk.Label(window4, text="An Optimal Samples Selection System",font=('Arial',25))
window4_Title.grid(row=0,column=0,pady=10,columnspan=10,padx=(20,0))

window4_LD = tk.Label(window4, text="Define positions and range of numbers",font=('Arial',15))
window4_LD.grid(row=1,column=0,columnspan=10,pady=10)

window4_LP = tk.Label(window4,text= "Please input 3 positions")
window4_LP.grid(row=2,column=0,pady=10,padx=10)

window4_entry1=[tk.Entry(window4,width=4) for _ in range(3)]
entry_num=1
for window4_entrylist1 in window4_entry1:
    window4_entrylist1.grid(row=2,column=entry_num,padx=(30,30))
    entry_num=entry_num+1

window4_selected = tk.IntVar()

window4_Rbutton1 = tk.Radiobutton(frame9, text="Please input the range of numbers for", variable=window4_selected, value=0)
window4_Rbutton1.grid(row=3,column=0,padx=(0,50),pady=10,columnspan=6,sticky="W")

frame10 = tk.Frame(window4)
frame10.grid(row=4,column=0,columnspan=10)

window4_Label1=tk.Label(frame10,text="1st position")
window4_Label1.grid(row=4,column=0,pady=10,padx=10)

window4_Label2=tk.Label(frame10,text="2nd position")
window4_Label2.grid(row=4,column=4,pady=10,padx=10)

window4_Label3=tk.Label(frame10,text="3rd position")
window4_Label3.grid(row=4,column=8,pady=10,padx=10)

window4_entry2=[tk.Entry(frame10,width=2) for _ in range(3)]
entry_num2=1
for window4_entrylist2 in window4_entry2:
    window4_entrylist2.grid(row=4,column=int(entry_num2)*4-3,padx=10)
    entry_num2=entry_num2+1

window4___Label=[tk.Label(frame10,text="-")for _ in range(3)]
entry_num22=1
for window4___LabeList in window4___Label:
    window4___LabeList.grid(row=4,column=int(entry_num22)*4-2)
    entry_num22=entry_num22+1

window4_entry21=[tk.Entry(frame10,width=2) for _ in range(3)]
entry_num21=1
for window4_entrylist21 in window4_entry21:
    window4_entrylist21.grid(row=4,column=int(entry_num21)*4-1,padx=10)
    entry_num21=entry_num21+1

frame11 = tk.Frame(window4)
frame11.grid(row=5,column=0,columnspan=10)

window4_Rbutton2 = tk.Radiobutton(frame11, text="Please input range of numbers not to be included for", variable=window4_selected, value=1)
window4_Rbutton2.grid(row=5,column=0,pady=10,columnspan=6,padx=10)

frame12 = tk.Frame(window4)
frame12.grid(row=6,column=0,columnspan=10)

window4_Label4=tk.Label(frame12,text="1st position")
window4_Label4.grid(row=4,column=0,pady=10,padx=10)

window4_Label5=tk.Label(frame12,text="2nd position")
window4_Label5.grid(row=4,column=4,pady=10,padx=10)

window4_Label6=tk.Label(frame12,text="3rd position")
window4_Label6.grid(row=4,column=8,pady=10,padx=10)

window4_entry3=[tk.Entry(frame12,width=2) for _ in range(3)]
entry_num3=1
for window4_entrylist3 in window4_entry3:
    window4_entrylist3.grid(row=4,column=int(entry_num3)*4-3,padx=10)
    entry_num3=entry_num3+1

window4___Labe2=[tk.Label(frame12,text="-")for _ in range(3)]
entry_num23=1
for window4___LabeList2 in window4___Labe2:
    window4___LabeList2.grid(row=4,column=int(entry_num23)*4-2)
    entry_num23=entry_num23+1

window4_entry22=[tk.Entry(frame12,width=2) for _ in range(3)]
entry_num24=1
for window4_entrylist22 in window4_entry22:
    window4_entrylist22.grid(row=4,column=int(entry_num24)*4-1,padx=10)
    entry_num24=entry_num24+1

frame13=tk.Frame(window4)
frame13.grid(row=7,column=0,columnspan=10)

window4_label7=tk.Label(frame13,text="Please name a file to create")
window4_label7.grid(row=0,column=0,pady=10,sticky="E")

window4_entry4=tk.Entry(frame13,width=50)
window4_entry4.grid(row=0,column=1,columnspan=50,pady=10)

window4_text = tk.Text(frame13,height=10,width=44)
window4_text.insert(tk.END," ")
window4_text.grid(row=1,column=0,columnspan=5,rowspan=2,sticky='W',padx=(5,0),pady=10)

window4_scrollbar = tk.Scrollbar(frame13)
window4_scrollbar.grid(row=1, column=5, sticky='ns',rowspan=2)

window4_text.config(yscrollcommand=window4_scrollbar.set)
window4_scrollbar.config(command=window4_text.yview)


window4_button2=tk.Button(frame13,text="execute",command=Store_DBN)
window4_button2.grid(row=1, column=7,padx=(10,10))

window4_button3=tk.Button(frame13,text="Previous",command=backwin2_2)
window4_button3.grid(row=1, column=8,padx=(10,10))

window4_button4=tk.Button(frame13,text="Print")
window4_button4.grid(row=2, column=7,padx=(10,10))

window4_button5=tk.Button(frame13,text="Next",command=Next2)
window4_button5.grid(row=2, column=8,padx=(10,10))

#S6

window5 = tk.Toplevel(root)
window5.withdraw()

window5_Title = tk.Label(window5, text="An Optimal Samples Selection System",font=('Arial',25))
window5_Title.grid(row=0,column=0,pady=10,columnspan=10,padx=(20,0))

window5_LD = tk.Label(window5, text="Select positions and fixed numbers",font=('Arial',15))
window5_LD.grid(row=1,column=0,columnspan=10,pady=10)

window5_LP = tk.Label(window5,text= "Please select 3 positions")
window5_LP.grid(row=2,column=0,columnspan=10,pady=10,padx=10)

frame14 = tk.Frame(window5)
frame14.grid(row=3,column=0,columnspan=10)

window5_Label1=tk.Label(frame14,text="1st position")
window5_Label1.grid(row=4,column=0,pady=10,padx=10)

window5_Label2=tk.Label(frame14,text="2nd position")
window5_Label2.grid(row=4,column=2,pady=10,padx=10)

window5_Label3=tk.Label(frame14,text="3rd position")
window5_Label3.grid(row=4,column=4,pady=10,padx=10)

window5_entry2=[tk.Entry(frame14,width=2) for _ in range(3)]
entry_num4=1
for window5_entrylist2 in window5_entry2:
    window5_entrylist2.grid(row=4,column=int(entry_num4)*2-1,padx=10,pady=10)
    entry_num4=entry_num4+1

window5_Label4=tk.Label(window5,text="Please enter the sum of there 3 numbers in positions")
window5_Label4.grid(row=4,column=0,columnspan=4,pady=10,padx=10)

window5_entry3=tk.Entry(window5,width=5)
window5_entry3.grid(row=4,column=5)

frame15=tk.Frame(window5)
frame15.grid(row=7,column=0,columnspan=10)

window5_label7=tk.Label(frame15,text="Please name a file to create")
window5_label7.grid(row=0,column=0,pady=10,sticky="E")

window5_entry4=tk.Entry(frame15,width=50)
window5_entry4.grid(row=0,column=1,columnspan=50,pady=10)

window5_text = tk.Text(frame15,height=10,width=44)
window5_text.insert(tk.END," ")
window5_text.grid(row=1,column=0,columnspan=5,rowspan=2,sticky='W',padx=(5,0),pady=10)

window5_scrollbar = tk.Scrollbar(frame15)
window5_scrollbar.grid(row=1, column=5, sticky='ns',rowspan=2)

window5_text.config(yscrollcommand=window5_scrollbar.set)
window5_scrollbar.config(command=window5_text.yview)



window5_button2=tk.Button(frame15,text="execute", command=Store_DBN)
window5_button2.grid(row=1, column=7,padx=(10,10))

window5_button3=tk.Button(frame15,text="Previous",command=backwin2_3)
window5_button3.grid(row=1, column=8,padx=(10,10))

window5_button4=tk.Button(frame15,text="Print")
window5_button4.grid(row=2, column=7,padx=(10,10))

window5_button5=tk.Button(frame15,text="Next",command=Next3)
window5_button5.grid(row=2, column=8,padx=(10,10))

text_r.bind("<Key>", disable_input)
text_v.bind("<Key>", disable_input)
text_d.bind("<Key>", disable_input)
window3_text.bind("<Key>", disable_input)
window4_text.bind("<Key>", disable_input)
window5_text.bind("<Key>", disable_input)

root.mainloop()


