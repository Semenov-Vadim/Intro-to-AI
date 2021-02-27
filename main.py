from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import Combobox
import sqlite3


# очередность расположения строк
rowInfo = 0
rowAttestation = 1
rowUkr = 2
rowMath = 3
row3Subject = 4
row4Subject = 5
rowRegionalCoef = 6
rowGetResult = 7
rowScrolledText = 8



# создание окна
window = Tk()
window.title("Поиск специальности по баллам ЗНО")
window.geometry('600x500')

# значения, введенные пользователем
valAttestationGrade = StringVar()
valUkrGrade = StringVar()
valMathGrade = StringVar()
val3SubjectGrade = StringVar()
val4SubjectGrade = StringVar()
valRegionalCoef = StringVar()

# оисание столбиков
lblName = Label(window, text="Название")
lblName.grid(column=0, row=rowInfo, pady=5)
lblGrade = Label(window, text="Балл")
lblGrade.grid(column=1, row=rowInfo)
lblEmpty = Label(window, text="")       # создает третий столбик в grid для красивого вывода infoPanel
lblEmpty.grid(column=2, row=rowInfo, padx=100)

# ввод баллов абитуриента
lblAttestation = Label(window, text="Аттестат")
lblAttestation.grid(column=0, row=rowAttestation)
txtAttestationGrade = Entry(window,width=10, textvariable=valAttestationGrade)
txtAttestationGrade.grid(column=1, row=rowAttestation)
txtAttestationGrade.insert(0, 2)

lblUkr = Label(window, text="Ураинский")
lblUkr.grid(column=0, row=rowUkr)
txtUkrGrade = Entry(window, width=10, textvariable=valUkrGrade)
txtUkrGrade.grid(column=1, row=rowUkr)
txtUkrGrade.insert(0, 100)

lblMath = Label(window, text="Математика")
lblMath.grid(column=0, row=rowMath)
txtMathGrade = Entry(window,width=10, textvariable=valMathGrade)
txtMathGrade.grid(column=1, row=rowMath)
txtMathGrade.insert(0, 100)

# предметы ЗНО без математики и украинского
remainingSubjects = ("History",
"Biology",
"Geography",
"Physics",
"Chemistry",
"English",
"Spanish",
"German",
"French")

# выбор 3 и 4 редмета и балла
comboSubject3Name = Combobox(window)
comboSubject3Name['values'] = remainingSubjects
comboSubject3Name.current(5)  # установите вариант по умолчанию
comboSubject3Name.grid(column=0, row=row3Subject)
lbl3SubjectGrade = Entry(window,width=10, textvariable=val3SubjectGrade)
lbl3SubjectGrade.grid(column=1, row=row3Subject)
lbl3SubjectGrade.insert(0, 100)

remainingSubjects += ("", )
comboSubject4Name = Combobox(window)
comboSubject4Name['values'] = (remainingSubjects)
comboSubject4Name.current(9)
comboSubject4Name.grid(column=0, row=row4Subject)
lbl4SubjectGrade = Entry(window, width=10, textvariable=val4SubjectGrade)
lbl4SubjectGrade.grid(column=1, row=row4Subject)
lbl4SubjectGrade.insert(0, 100)

lblRegionalCoef = Label(window, text="Региональный коэффициент")
lblRegionalCoef.grid(column=0, row=rowRegionalCoef)
txtRegionalCoef = Entry(window, width=10, textvariable=valRegionalCoef)
txtRegionalCoef.grid(column=1, row=rowRegionalCoef)
txtRegionalCoef.insert(0, 1.00)

# возвращает True, если полученный объект- число
def is_digit(string):
    string = string.replace(',', '.')
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False

# checking for incorrect input data
def checkInput():
    if valAttestationGrade.get() == '' or \
            valUkrGrade.get() == '' or \
            valMathGrade.get() == '' or \
            val3SubjectGrade.get() == '' or \
            valRegionalCoef.get() == '':
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'заполните пустые поля')

    elif is_digit(valAttestationGrade.get()) is False or \
            is_digit(valRegionalCoef.get()) is False:
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'поля должны быть заполнены числами')

    elif valUkrGrade.get().isdigit() is False or \
            valMathGrade.get().isdigit() is False or \
            val3SubjectGrade.get().isdigit() is False or \
            val4SubjectGrade.get().isdigit() is False:
        try:
            float(valUkrGrade.get().replace(',', '.'))
            float(valMathGrade.get().replace(',', '.'))
            float(val3SubjectGrade.get().replace(',', '.'))
            float(val4SubjectGrade.get().replace(',', '.'))
            infoPanel.delete(1.0, END)
            infoPanel.insert(INSERT, 'балл ЗНО не может быть дробным числом')
        except ValueError:
            infoPanel.delete(1.0, END)
            infoPanel.insert(INSERT, 'поля должны быть заполнены числами')

    elif float(valAttestationGrade.get().replace(',', '.')) < 2 or \
            float(valAttestationGrade.get().replace(',', '.')) > 12:
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'балл аттестата должен быть от 2 до 12')

    elif int(valUkrGrade.get()) < 100 or \
            int(valMathGrade.get()) < 100 or \
            int(val3SubjectGrade.get()) < 100 or \
            int(val4SubjectGrade.get()) < 100:
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'балл ЗНО не может быть меньше 100')

    elif int(valUkrGrade.get()) > 200 or \
            int(valMathGrade.get()) > 200 or \
            int(val3SubjectGrade.get()) > 200 or \
            int(val4SubjectGrade.get()) > 200:
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'балл ЗНО не может быть больше 200')

    elif comboSubject3Name.get() == comboSubject4Name.get():
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'Выберете другой 4-й предмет')

    elif comboSubject3Name.get() not in remainingSubjects or comboSubject4Name.get() not in remainingSubjects:
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'Выберете предмет из выпадающего списка')

    elif float(valRegionalCoef.get().replace(',', '.')) < 1.0 or float(valRegionalCoef.get().replace(',', '.')) > 1.1:
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, 'Региональный коэффициент должен быть от 1 до 1.1')

    else:
        valAttestationGrade.set(valAttestationGrade.get().replace(',', '.'))
        valRegionalCoef.set(valRegionalCoef.get().replace(',', '.'))
        return True
        '''
        infoPanel.delete(1.0, END)
        infoPanel.insert(INSERT, float(valAttestationGrade.get()))
        infoPanel.insert(INSERT, '\n')
        infoPanel.insert(INSERT, int(valUkrGrade.get()))
        infoPanel.insert(INSERT, '\n')
        infoPanel.insert(INSERT, int(valMathGrade.get()))
        infoPanel.insert(INSERT, '\n')
        infoPanel.insert(INSERT, comboSubject3Name.get())
        infoPanel.insert(INSERT, '\n')
        infoPanel.insert(INSERT, int(val3SubjectGrade.get()))
        infoPanel.insert(INSERT, '\n')
        infoPanel.insert(INSERT, comboSubject4Name.get())
        infoPanel.insert(INSERT, '\n')
        # infoPanel.insert(INSERT, int(val4SubjectGrade.get()))
        infoPanel.insert(INSERT, '\n')
        infoPanel.insert(INSERT, float(valRegionalCoef.get()))
        '''


# выводит рекомендуемые абитуриенту специальности и предполагаемый балл при поступлении
def getSpecialities():
    if checkInput() != True:
        return
    # подсоединение к БД
    conn = sqlite3.connect('specialties.db')
    c = conn.cursor()

    # очиста списка абитуриентов
    c.execute("DELETE FROM student")

    if comboSubject4Name.get() == '':
        c.execute("INSERT INTO student VALUES(1, ?, ?, ?, ?, ?, ?, ?, ? )",
              (float(valAttestationGrade.get()), comboSubject3Name.get(), 'NULL', int(valUkrGrade.get()),
               int(valMathGrade.get()), int(val3SubjectGrade.get()), 'NULL', float(valRegionalCoef.get())))
    elif comboSubject3Name.get() == '':
        c.execute("INSERT INTO student VALUES(1, ?, ?, ?, ?, ?, ?, ?, ? )",
                  (float(valAttestationGrade.get()), 'NULL', comboSubject4Name.get(), int(valUkrGrade.get()),
                   int(valMathGrade.get()), 'NULL', int(val4SubjectGrade.get()) , float(valRegionalCoef.get())))
    else:
        c.execute("INSERT INTO student VALUES(1, ?, ?, ?, ?, ?, ?, ?, ? )",
                  (float(valAttestationGrade.get()), comboSubject3Name.get(), comboSubject4Name.get(), int(valUkrGrade.get()),
                   int(valMathGrade.get()), int(val3SubjectGrade.get()), int(val4SubjectGrade.get()), float(valRegionalCoef.get())))

    """
    # вывод списка студентов и специальностей
    print("\nstudents: ")
    for row in c.execute('''SELECT * FROM student'''):
        print(row)

    print("\nspecialities: ")
    for row in c.execute('''SELECT * FROM speciality'''):
        print(row)
    """

    # очистка панели вывода
    infoPanel.delete(1.0, END)

    infoPanel.insert(INSERT, "Балл     Название специальности")
    infoPanel.insert(INSERT, '\n')

    numberOfSpecGreaterThenZero = False

    # print("\nRecommended specialities: ")
    # формирование балла по специальности
    # балл аттестата из 12-бальной с-мы в 200-балльную переводится по формуле (attestation * 10 + 80)
    for row in c.execute('''
    SELECT 
    CASE 
        WHEN ((student.sub3 = speciality.sub3 OR student.sub3 = speciality.sub4) AND (student.sub4 = speciality.sub3 OR student.sub4 = speciality.sub4)) AND student.v3 >= student.v4  AND student.v3 >= minSub34
            THEN (Ukrainian * kUkr + Math * kMath + (attestation * 10 + 80) * kAttestation + v3 * ksub34) * kReg

        WHEN ((student.sub3 = speciality.sub3 OR student.sub3 = speciality.sub4) AND (student.sub4 = speciality.sub3 OR student.sub4 = speciality.sub4)) AND student.v3 < student.v4 AND student.v4 >= minSub34
            THEN (Ukrainian * kUkr + Math * kMath + (attestation * 10 + 80) * kAttestation + student.v4 * ksub34) * kReg

        WHEN (student.sub3 = speciality.sub3 OR student.sub3 = speciality.sub4) AND student.v3 >= minSub34
            THEN (Ukrainian * kUkr + Math * kMath + (attestation * 10 + 80) * kAttestation + student.v3 * ksub34) * kReg

        WHEN (student.sub4 = speciality.sub3 OR student.sub4 = speciality.sub4) AND student.v4 >= minSub34
            THEN (Ukrainian * kUkr + Math * kMath + (attestation * 10 + 80) * kAttestation + student.v4 * ksub34) * kReg

        ELSE null


        END score, speciality.name
    FROM student, speciality 
    WHERE 
        Ukrainian >= minUkr AND 
        Math >= minMath AND 
        score >= lastYearMin AND 
        score is not null
    '''):
        numberOfSpecGreaterThenZero = True
        if row[0] >= 200:
            infoPanel.insert(INSERT, 200)
        else:
            infoPanel.insert(INSERT, ('%.3f' %round(row[0], 3)))
            # print('%.3f' %round(row[0], 3))
        infoPanel.insert(INSERT, '  ')
        infoPanel.insert(INSERT, row[1])
        infoPanel.insert(INSERT, '\n')
        # print(row)

    if numberOfSpecGreaterThenZero == False:
        infoPanel.insert(INSERT, "Нет рекомендованных специальностей")
        infoPanel.insert(INSERT, '\n')
    conn.commit()
    conn.close()

btnGetSpecialities = Button(window, text="Получить список рекомендуемых специальностей", command=getSpecialities)
btnGetSpecialities.grid(column=0, row=rowGetResult, columnspan=2, padx=5, pady=10)

infoPanel = scrolledtext.ScrolledText(window, width=60, height=16)
infoPanel.grid(column=0, row=rowScrolledText, columnspan=3, padx=5)
# infoPanel.pack(expand = True, fill=BOTH)



# Эта функция вызывает бесконечный цикл окна, поэтому окно будет ждать любого взаимодействия с пользователем, пока не будет закрыто
window.mainloop()


