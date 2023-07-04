import os, sys
import uuid
from tkinter import Tk, Frame, Entry, Label, Button, StringVar, Text
from tkinter import messagebox

from project import Project


RepositoryPath = r'D:\Yun\Codes\Python'

class MainUi(Tk):
    def __init__(self):
        super().__init__()
        self.title('新建工程')
        self.attributes('-toolwindow', 1)
        x = (self.winfo_screenwidth()) // 2 - 300
        y = (self.winfo_screenheight())//2 - 150
        self.geometry(f'+{x}+{y}')

        self.project_label = Label(self, text='请输入工程名称: ', justify='center')
        self.project_entry_var = StringVar(value='')
        self.project_entry = Entry(self, textvariable=self.project_entry_var, width=30)
        self.project_label.grid(row=0, column=0, padx=5, pady=2, ipady=5)
        self.project_entry.grid(row=0, column=1, padx=5, pady=2, ipady=5, sticky='w')

        self.author_label = Label(self, text='请输入作者名称: ', justify='center')
        self.author_entry_var = StringVar(value='wcy')
        self.author_entry = Entry(self, textvariable=self.author_entry_var, width=30)
        self.author_label.grid(row=1, column=0, padx=5, pady=2, ipady=5)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2, ipady=5, sticky='w')

        self.decription_label = Label(self, text='请输入工程简介: ', justify='center')
        self.decription_entry = Entry(self, width=30)
        self.decription_label.grid(row=2, column=0, padx=5, pady=2, ipady=5, sticky='ne')
        self.decription_entry.grid(row=2, column=1, padx=5, pady=2, ipady=5, sticky='w')

        self.comfirm_btn = Button(self, text='确  认', command=self.comfirm_handler)
        self.cancel_btn = Button(self, text='取  消', command=self.cancel_handler)
        self.comfirm_btn.grid(row=3, column=0, pady=6, ipadx=10)
        self.cancel_btn.grid(row=3, column=1, pady=6, ipadx=10)

    def cancel_handler(self):
        self.destroy()
        
    def comfirm_handler(self):
        project = Project()

        project_name = self.project_entry.get().strip()
        project_author = self.author_entry.get().strip()
        project_path = RepositoryPath
        project_decription = self.decription_entry.get().strip()

        if project_name:
            if not os.path.exists(os.path.join(project_path, project_name)):
                import time
                time.sleep(0.5)
                project.new(project_name, project_author, project_path, project_decription)
                messagebox.showinfo(title='成功', message='新建工程: \"%s\" 成功.' % project_name)
                self.destroy()
            else:
                messagebox.showerror(title='错误', message='新建工程失败, \"%s\"已存在.' % project_name)
        else:
            messagebox.showerror(title='错误', message='新建工程失败, 工程名不能为空白.')




if __name__ == '__main__':
    root = MainUi()
    root.mainloop()
