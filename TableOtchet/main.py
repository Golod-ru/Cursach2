from tkinter.ttk import Combobox
import psycopg2
from tkinter import *
from tkinter import ttk
import time

connection = psycopg2.connect(user="postgres",
                                  password="123",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="test_base")

borderwig = 7

def data_seru(date):
    try:
        valid_date = time.strptime(date, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def insert(main_frame,name_table,date,i=0):

    cursor = connection.cursor()
    def clik(i):
        if i+1 < how_many:
            com = combobox.get()
            if com == 'Был +':
                com = '+'
            elif com == 'Не был -':
                com = '-'
            elif com == 'Не был(уважительная) -(у)':
                com = '-(у)'
            else:
                com = 'Пропущено'
            cursor.execute('update ' + '"' + str(name_table) + '"' + ' set ' + str('"name' + str(i) + '"') + '=' + str("'" + str(com) + "'")+ 'where "Data" ='"'" + str(date) + "'")
            connection.commit()
            i+=1
            insert(main_frame,name_table,date,i)
        else:
            main_window(main_frame)


    main_frame.destroy()
    main_frame = Frame(root)
    main_frame.pack()

    cursor.execute('select "Name" from "Users"')
    list_student = cursor.fetchall()

    how_many = len(list_student)
    ost = (how_many - i)-1
    labe = Label(master=main_frame, text="Осталось заполнить " + str(ost))
    labe.grid(row=0, column=0, sticky="nsew")
    exep_btn = Button(master=main_frame, relief=RAISED, borderwidth=6, text='Добавить', command=lambda: clik(i))
    exep_btn.grid(row=2, column=1, sticky="nsew")

    lable = Label(master=main_frame,text="Студент "+str(list_student[i][0])+" Был на занятии?")
    lable.grid(row=1, column=0, sticky="nsew")

    labels = [
        'Был +',
        'Не был -',
        'Не был(уважительная) -(у)'
    ]
    combobox = Combobox(master=main_frame, values=labels, state="readonly")
    combobox.grid(row=2, column=0, sticky="nsew")

def Serch_right_table(main_frame,status,error,error2):

    def clik():
        date = date_ent.get()
        date_prove = data_seru(date)
        if date_prove:
            name_table = combobox.get()
            if name_table == '':
                Serch_right_table(main_frame, status, False, True)
            cursor = connection.cursor()
            cursor.execute(
                'Insert into ' + '"' + str(name_table) + '"' + ' ("Data") Values (' + "'" + str(date) + "'" + ')')
            connection.commit()
            cursor.close()
            insert(main_frame,name_table,date)

        else:
            Serch_right_table(main_frame, status,True,False)


    main_frame.destroy()
    main_frame = Frame(root)
    main_frame.pack()
    if error:
        labale_e = Label(master=main_frame,
                         text="Ошибка, попробуйте ещё раз. Возможно вы ввели непраивльно дату занятия")
        labale_e.pack()
    if error2:
        labale_e2 = Label(master=main_frame,
                         text="Ошибка, попробуйте ещё раз. Возможно вы ввели непраивльно дату занятия")
        labale_e2.pack()
    sex_form = Frame(main_frame, relief=SUNKEN, borderwidth=borderwig)
    sex_form.pack(fill=BOTH, side=RIGHT, ipadx=5, expand=True)
    labale = Label(master=sex_form,
                   text="Добавление новых значений в таблицы. \n"
                        "Нажмите на кнопку чтобы выбрать нужную таблицу из списка")
    labale.grid(row=0, column=0, sticky="nsew")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
    record = cursor.fetchall()
    cursor.close()
    li = []
    for i in range(len(record)):
        if record[i][0] == "Users":
            pass
        else:
            li.append(record[i][0])
    print(li)
    combobox = Combobox(master=sex_form, values=li, state="readonly")
    combobox.grid(row=1, column=0, sticky="nsew")
    but_form = Frame(main_frame, relief=SUNKEN, borderwidth=borderwig)
    but_form.pack(fill=BOTH, side=RIGHT, ipadx=5, expand=True)
    comb_btn = Button(master=but_form, relief=RAISED, borderwidth=6, bg="green", text='Добавить', command=clik)
    exit_btn = Button(master=but_form, relief=RAISED, borderwidth=6, bg="red", text='отменить и выйти',
                      command=lambda: main_window(main_frame, status))
    date_lbl = Label(master=but_form, text="Введите дату занятия.\n"
                                           "Пример: 2/2/2002")
    date_lbl.grid(row=0, column=0, sticky="nsew")
    date_ent = Entry(master=but_form, width=20)
    date_ent.grid(row=1, column=0, sticky="nsew")
    exit_btn.grid(row=3, column=0, sticky="nsew")
    comb_btn.grid(row=2, column=0, sticky="nsew")

def creat(main_frame,status):

    main_frame.destroy()
    main_frame = Frame(root)
    main_frame.pack()


    def clear():
        name_ent.delete(0,END)
    def clik():
        name = name_ent.get()
        nametable = '"'+str(name)+'"'
        cursor = connection.cursor()
        cursor.execute('select "Name" from "Users"')
        list_student = cursor.fetchall()
        cursor.execute('create table'+str(nametable)+''
                       '('
                       '"Data" character varying(15) PRIMARY KEY NOT NULL'
                       ')')
        connection.commit()
        for i in range(len(list_student)):
            cursor.execute('ALTER TABLE ' + str(nametable) + 'add column ' + str("name" + str(i)) + ' character varying(15)')
            connection.commit()
        cursor.execute('Insert into '+str(nametable)+' ("Data") Values ('+"'"+'список'+"'"')')
        connection.commit()
        for i in range(len(list_student)):
            cursor.execute('update '+str(nametable)+ ' set ' + str('"name' + str(i) +'"') + '=' + str("'"+ str(list_student[i][0]) +"'"))
            connection.commit()
        cursor.close()
        main_window(main_frame,status)



    frm_form = Frame(main_frame,relief=SUNKEN, borderwidth=borderwig)
    frm_form.pack(fill=BOTH, side=RIGHT, ipadx=5, expand=True)
    name_lbl = Label(master=frm_form,text="Введите название предмета")
    name_lbl.grid(row=1, column=0, sticky="nsew")
    name_ent = Entry(master=frm_form, width=75)
    name_ent.grid(row=1, column=1, sticky="nsew")

    frm_buttons = Frame(main_frame)
    frm_buttons.pack(fill=BOTH, side=LEFT, expand=True)

    btn_clear = Button(master=frm_buttons, relief=RAISED, borderwidth=borderwig, text="Создать",
                          command=clik)
    btn_clear.pack()

    btn_submit = Button(master=frm_buttons, relief=RAISED, borderwidth=borderwig, text="Выйти", bg="red",
                           command=lambda: main_window(main_frame,status))
    btn_submit.pack(ipadx=28)

    btn_reg = Button(master=frm_buttons, relief=RAISED, borderwidth=borderwig, text="Очистить поля",
                        bg="orange", command=clear)
    btn_reg.pack(ipadx=7)

def delete(main_frame):

    def clik():
        cum = combobox.get()
        if cum == '':
            main_window(main_frame)
        else:
            cursor = connection.cursor()
            cursor.execute("DROP TABLE "+str(cum))
            connection.commit()
            main_window(main_frame)
    main_frame.destroy()
    main_frame = Frame(root)
    main_frame.pack()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
    record = cursor.fetchall()
    cursor.close()
    li = []
    for i in range(len(record)):
        if record[i][0] == "Users":
            pass
        else:
            li.append(record[i][0])
    print(li)
    lb =Label(master=main_frame, text="Выбери нужную таблицу для удаления\n"
                                      "Если ничего не выберешь - ничего не удалиться")
    lb.grid(row=0, column=0, sticky="nsew")
    combobox = Combobox(master=main_frame, values=li, state="readonly")
    combobox.grid(row=1, column=0, sticky="nsew")
    btn = Button(master=main_frame, relief=RAISED, borderwidth=borderwig, text="Удалить таблицу",command=clik)
    btn.grid(row=2, column=0, sticky="nsew")
    btnEx = Button(master=main_frame, relief=RAISED, borderwidth=borderwig,bg="red", text="Выйти",command=lambda: main_window(main_frame))
    btnEx.grid(row=3, column=0, sticky="nsew")

def show_time(main_frame, status):
    main_frame.destroy()
    main_frame = Frame(root)
    main_frame.pack()

    menu_frame = Frame(main_frame,relief=SUNKEN, borderwidth=borderwig)
    menu_frame.pack()

    Table_frame = Frame(main_frame, relief=SUNKEN, borderwidth=borderwig)
    Table_frame.pack()
    def clik():
        for widget in Table_frame.winfo_children():
            widget.destroy()
        com = combobox.get()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM "'+str(com)+'"')
        fulldata = cursor.fetchall()
        columns = fulldata[0]
        data = fulldata[1:]

        tree = ttk.Treeview(Table_frame,columns=columns, show="headings")
        tree.pack(fill=BOTH, expand=1)
        for i in range(len(columns)):
            tree.heading(str(columns[i]), text=columns[i])
        for i in data:
            tree.insert("", END, values=i)



    cursor = connection.cursor()
    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
    record = cursor.fetchall()
    cursor.close()
    li = []
    for i in range(len(record)):
        if record[i][0] == "Users":
            pass
        else:
            li.append(record[i][0])
    lb = Label(master=menu_frame, text="Выбери нужную таблицу для просмотра\n"
                                       "Если ничего не выберешь - ничего не откроется")
    lb.grid(row=0, column=0, sticky="nsew")
    combobox = Combobox(master=menu_frame, values=li, state="readonly")
    combobox.grid(row=1, column=0, sticky="nsew")
    exit_but = Button(master=menu_frame, relief=RAISED, borderwidth=borderwig, text="Выйти",
                      command=lambda: main_window(main_frame, status))
    exit_but.grid(row=2, column=1, sticky="nsew")
    btn = Button(master=menu_frame, relief=RAISED, borderwidth=borderwig, text="просмотреть таблицу", command=clik)
    btn.grid(row=2, column=0, sticky="nsew")

def redact(main_frame):
    main_frame.destroy()
    main_frame = Frame(root)
    main_frame.pack()

    def clik1():
        def clik2(name):
            def clik3(name,u_name):
                def clik4(name,u_name,data):
                    com = combobox3.get()
                    if com == 'Был +':
                        com = '+'
                    elif com == 'Не был -':
                        com = '-'
                    elif com == 'Не был(уважительная) -(у)':
                        com = '-(у)'
                    else:
                        com = 'Пропущено'

                    cursor = connection.cursor()
                    cursor.execute(
                        'update ' + '"' + str(name) + '"' + ' set ' + str('"name' + str(u_name) + '"') + '=' + str(
                            "'" + str(com) + "'") + 'where "Data" ='"'" + str(data) + "'")
                    connection.commit()
                    main_window(main_frame)

                data = combobox2.get()
                combobox2.configure(state=DISABLED)
                con_but2.configure(state=DISABLED)
                labels = [
                    'Был +',
                    'Не был -',
                    'Не был(уважительная) -(у)'
                ]
                frame4 = Frame(main_frame, relief=SUNKEN, borderwidth=borderwig)
                frame4.pack()
                combobox3 = Combobox(master=frame4, values=labels, state="readonly")
                combobox3.grid(row=0, column=0, sticky="nsew")
                con_but = Button(master=frame4, relief=RAISED, borderwidth=borderwig, text="Внести изменения",
                                 command=lambda: clik4(name,u_name,data))
                con_but.grid(row=1, column=1, sticky="nsew")

            u_name = combobox1.get()
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM ' + '"' + str(name) + '"' + 'where "Data" =' + "'список'")
            record = cursor.fetchall()
            record = record[0]
            cursor.close()
            i_u_name =0
            pus = []
            for i in range(len(record)):
                if record[i] == "список":
                    pass
                else:
                    pus.append(record[i])
            for i in range(len(pus)):
                if pus[i] == u_name:
                    break
                else:
                    i_u_name += 1
            combobox1.configure(state=DISABLED)
            con_but1.configure(state=DISABLED)
            cursor = connection.cursor()
            cursor.execute('SELECT "Data" FROM ' + '"' + str(name) + '"')
            record = cursor.fetchall()
            cursor.close()
            data = []
            for i in range(len(record)):
                if record[i][0] == "список":
                    pass
                else:
                    data.append(record[i][0])
            frame3 = Frame(main_frame, relief=SUNKEN, borderwidth=borderwig)
            frame3.pack()
            combobox2 = Combobox(master=frame3, values=data, state="readonly")
            combobox2.grid(row=0, column=0, sticky="nsew")
            con_but2 = Button(master=frame3, relief=RAISED, borderwidth=borderwig, text="Выбрать дату",
                             command=lambda: clik3(name,i_u_name))
            con_but2.grid(row=1, column=1, sticky="nsew")


        name = combobox.get()
        combobox.configure(state=DISABLED)
        con_but.configure(state=DISABLED)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM '+ '"'+ str(name)+'"' + 'where "Data" =' +"'список'")
        record = cursor.fetchall()
        print(record)
        cursor.close()
        record1 = []
        record = record[0]
        for i in range(len(record)):
            if record[i] == "список":
                pass
            else:
                record1.append(record[i])
        print(record1)
        frame2 =Frame(main_frame,relief=SUNKEN, borderwidth=borderwig)
        frame2.pack()
        combobox1 = Combobox(master=frame2, values=record1, state="readonly")
        combobox1.grid(row=0, column=0, sticky="nsew")
        con_but1 = Button(master=frame2, relief=RAISED, borderwidth=borderwig, text="Выбрать пользователя",
                         command=lambda: clik2(name))
        con_but1.grid(row=1, column=1, sticky="nsew")


    frame1 = Frame(main_frame,relief=SUNKEN, borderwidth=borderwig)
    frame1.pack()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
    record = cursor.fetchall()
    cursor.close()

    li = []
    for i in range(len(record)):
        if record[i][0] == "Users":
            pass
        else:
            li.append(record[i][0])

    combobox = Combobox(master=frame1, values=li, state="readonly")
    combobox.grid(row=0, column=0, sticky="nsew")
    exit_but = Button(master=frame1, relief=RAISED, borderwidth=borderwig, text="Выйти",
                      command=lambda: main_window(main_frame))
    exit_but.grid(row=0, column=1, sticky="nsew")

    con_but = Button(master=frame1, relief=RAISED, borderwidth=borderwig, text="Выбрать таблицу",
                      command=clik1)
    con_but.grid(row=1, column=1, sticky="nsew")

def main_window(main_frame,status=True):

    main_frame.destroy()
    main_frame = Frame(root)
    main_frame.pack()

    if status:
        all_botton = Frame(main_frame,relief=SUNKEN, borderwidth=borderwig)
        all_botton.pack(fill=BOTH, side=LEFT, expand=True)
        group_lbl = Label(master=all_botton,text="Староста группы")
        group_lbl.pack()

        btn_creat = Button(master=all_botton, relief=RAISED, borderwidth=borderwig, text="создать таблицу",command=lambda: creat(main_frame,status))
        btn_creat.pack()

        btn_ins = Button(master=all_botton, relief=RAISED, borderwidth=borderwig, text="Дабавить новые записи в таблицу",command=lambda: Serch_right_table(main_frame,status,False,False))
        btn_ins.pack()

        btn_del = Button(master=all_botton, relief=RAISED, borderwidth=borderwig, text="удалить таблицу", command=lambda: delete(main_frame))
        btn_del.pack()

        btn_watch = Button(master=all_botton, relief=RAISED, borderwidth=borderwig, text="просмотреть таблицу", command=lambda: show_time(main_frame, status))
        btn_watch.pack()
        btn_watch = Button(master=all_botton, relief=RAISED, borderwidth=borderwig, text="редактировать таблицу",command=lambda: redact(main_frame))
        btn_watch.pack()
        btn_exit = Button(master=all_botton, relief=RAISED, borderwidth=borderwig, text="выйти", command=lambda: reg_aut_window(main_frame))
        btn_exit.pack()
    else:

        all_botton = Frame(main_frame,relief=SUNKEN, borderwidth=borderwig)
        all_botton.pack(fill=BOTH, side=LEFT, expand=True)


        btn_watch = Button(master=all_botton, relief=RAISED, borderwidth=borderwig, text="просмотреть таблицу", command=lambda: show_time(main_frame, status))
        btn_watch.pack()
        #Доделаю к сдаче
        btn_exit = Button(master=all_botton, relief=RAISED, borderwidth=borderwig, text="выйти", command=lambda: reg_aut_window(main_frame))
        btn_exit.pack()

def registr_window(main_frame):

    main_frame.destroy()
    main_frame = Frame(root)
    main_frame.pack()

    def clear():
        name_ent.delete(0, END)
        pass_ent.delete(0, END)
        pass_rep_ent.delete(0, END)

    def reg():
        name = name_ent.get()
        passw = pass_ent.get()
        passwrep = pass_rep_ent.get()
        s = combobox.get()
        status = bool
        if s == "Студент":
            status = False
        else:
            status = True
        if passw == passwrep:
            cursor = connection.cursor()
            cursor.execute('select "Name" from "Users" where "Name" =' + "'" + name + "'")
            record = cursor.fetchall()
            if len(record) != 0:
                window_error = Tk()
                window_error.title("Ошибка")
                error = Label(master=window_error, text="Имя уже есть в системе, придумай другой")
                error.pack()
            else:
                name = "'" + name + "'"
                insertData = "(" + str(name) + ", " + str(passw) + ", " + str(status) + ")"
                cursor.execute('INSERT INTO "Users" ("Name","Password","Status") VALUES ' + insertData)
                connection.commit()
                cursor.close()
                reg_aut_window(main_frame)
        else:
            window_error2 = Tk()
            window_error2.title("Ошибка")
            error2 = Label(master=window_error2, text="Пароли не совпадают")
            error2.pack()

    labels = [
        "Твой статус в группе",
        "Имя",
        "Пароль:",
        "Повтор пароля:"
    ]
    frm_form2 = Frame(main_frame,relief=SUNKEN, borderwidth=borderwig)
    frm_form2.pack(fill=BOTH, side=LEFT, expand=True)

    cursor = connection.cursor()
    cursor.execute('select * from "Users" where "Status" =' + str("True"))
    rec = cursor.fetchall()
    labels2_1 = ["Студент"]
    labels2 = ["Студент", "Староста"]
    comb_lbl = Label(master=frm_form2, text=labels[0])
    comb_lbl.grid(row=2, column=0, sticky="nsew")
    if len(rec) != 0:
        combobox = Combobox(master=frm_form2, values=labels2_1, state="readonly")
        combobox.grid(row=2, column=1, sticky="nsew")
    else:
        combobox = Combobox(master=frm_form2, values=labels2, state="readonly")
        combobox.grid(row=2, column=1, sticky="nsew")
    name_lbl = Label(master=frm_form2, text=labels[1])
    name_lbl.grid(row=3, column=0, sticky="nsew")
    name_ent = Entry(master=frm_form2, width=50)
    name_ent.grid(row=3, column=1)
    pass_lbl = Label(master=frm_form2, text=labels[2])
    pass_lbl.grid(row=4, column=0, sticky="nsew")
    pass_ent = Entry(master=frm_form2, width=50)
    pass_ent.grid(row=4, column=1)
    pass_rep_lbl = Label(master=frm_form2, text=labels[3])
    pass_rep_lbl.grid(row=5, column=0, sticky="nsew")
    pass_rep_ent = Entry(master=frm_form2, width=50)
    pass_rep_ent.grid(row=5, column=1)

    frm_buttons2 = Frame(main_frame)
    frm_buttons2.pack(fill=BOTH, side=LEFT, expand=True)

    btn_clear = Button(master=frm_buttons2, relief=RAISED, borderwidth=borderwig, text="Зарегистрироваться", command=reg)
    btn_clear.pack()

    btn_submit = Button(master=frm_buttons2, relief=RAISED, borderwidth=borderwig, text="Выйти", bg="red", command=lambda: reg_aut_window(main_frame))
    btn_submit.pack(ipadx=28)

    btn_reg = Button(master=frm_buttons2, relief=RAISED, borderwidth=borderwig, text="Очистить поля", bg="orange",
                        command=clear)
    btn_reg.pack(ipadx=7)

def reg_aut_window(main_frame):

    main_frame.destroy()
    main_frame = Frame(root)
    main_frame.pack()
    frm_form = Frame(main_frame,relief=SUNKEN, borderwidth=borderwig)
    frm_form.pack(fill=BOTH, side=LEFT, expand=True)


    def clear():
        name_ent.delete(0, END)
        pass_ent.delete(0, END)

    def ent():
        name = name_ent.get()
        passw = pass_ent.get()
        cursor = connection.cursor()
        cursor.execute('select "Name","Password","Status" from "Users" where "Name" =' + "'" + name + "'")
        record = cursor.fetchall()
        if len(record) == 0:
            window_error = Tk()
            window_error.title("Ошибка")
            error = Label(master=window_error, text="ИМЯ НЕ НАЙДЕНО")
            error.pack()
        else:
            name_db = record[0][0]
            passw_db = record[0][1]
            status = record[0][2]
            if name == name_db and passw == passw_db:
                cursor.close()
                main_window(main_frame,status)
            else:
                window_error = Tk()
                window_error.title("Ошибка")
                error = Label(master=window_error, text="ПАРОЛЬ НЕ СОВПАДАЕТ")
                error.pack()

    labels = [
        "Добро пожаловать, Войдите или Зарегистрируйтесь",
        "Имя:",
        "Пароль:"
    ]

    ent_lbl = Label(master=frm_form, text=labels[0])
    ent_lbl.grid(row=0, column=1, sticky="e")

    name_lbl = Label(master=frm_form, text=labels[1])
    name_lbl.grid(row=1, column=0, sticky="nsew")
    name_ent = Entry(master=frm_form, width=50)
    name_ent.grid(row=1, column=1)
    pass_lbl = Label(master=frm_form, text=labels[2])
    pass_lbl.grid(row=2, column=0, sticky="nsew")
    pass_ent = Entry(master=frm_form, width=50)
    pass_ent.grid(row=2, column=1)

    frm_buttons = Frame(main_frame)
    frm_buttons.pack(fill=BOTH, side=LEFT, expand=True)

    btn_clear = Button(master=frm_buttons, relief=RAISED, borderwidth=borderwig, text="Очистить поля", command=clear)
    btn_clear.pack()

    btn_submit = Button(master=frm_buttons, relief=RAISED, borderwidth=borderwig, text="Вход", bg="green", command=ent)
    btn_submit.pack(ipadx=28)

    btn_reg = Button(master=frm_buttons, relief=RAISED, borderwidth=borderwig, text="Регестрация", bg="orange",command=lambda: registr_window(main_frame))
    btn_reg.pack(ipadx=7)

    btn_ext = Button(master=frm_buttons, relief=RAISED, borderwidth=borderwig, text="Выйти", bg="red", command= lambda: exit())
    btn_ext.pack(ipadx=23)

root = Tk()

main_frame = Frame(root)
main_frame.pack()

reg_aut_window(main_frame)

root.mainloop()