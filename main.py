import sqlite3

# ввод баллов абитуриента
print("Input data")
attestation = float(input("attestation: "))
while attestation < 2 or attestation > 12:
    print("incorrect data")
    attestation = float(input("input attestation: "))

ukr = int(input("Ukrainian: "))
while ukr < 100 or ukr > 200:
    print("incorrect data")
    ukr = int(input("input Ukrainian: "))

math = int(input("Math: "))
while math < 100 or math > 200:
    print("incorrect data")
    math = int(input("input Math: "))

kReg = float(input("regional coefficient: "))
while kReg < 1:
    print("incorrect data")
    kReg = float(input("input regional coefficient: "))


print('''enter the number corresponding to the name of the third subject:
1.History
2.Biology
3.Geography
4.Physics
5.Chemistry
6.English
7.Spanish
8.German
9.French''')
s3 = int(input())
while s3 < 1 or s3 > 9:
    print("incorrect data")
    s3 = int(input("input third subject: "))
if s3 == 1:
    sub3 = "History"
elif s3 == 2:
    sub3 = "Biology"
elif s3 == 3:
    sub3 = "Geography"
elif s3 == 4:
    sub3 = "Physics"
elif s3 == 5:
    sub3 = "Chemistry"
elif s3 == 6:
    sub3 = "English"
elif s3 == 7:
    sub3 = "Spanish"
elif s3 == 8:
    sub3 = "German"
elif s3 == 9:
    sub3 = "French"

print(sub3, ": ", end='', sep='')
v3 = int(input())
while v3 < 100 or v3 > 200:
    print("incorrect data")
    print(sub3, ": ", end='', sep='')
    v3 = int(input())

print('''enter the number corresponding to the name of the fourth subject:
or enter 0 if you don't have it''')
s4 = int(input())
while (s4 < 0 or s4 > 9) or s3 == s4:
    print("incorrect data")
    if s3 == s4:
        print("choose another subject")
    s4 = int(input("input fourth subject: "))
if s4 == 1:
    sub4 = "History"
elif s4 == 2:
    sub4 = "Biology"
elif s4 == 3:
    sub4 = "Geography"
elif s4 == 4:
    sub4 = "Physics"
elif s4 == 5:
    sub4 = "Chemistry"
elif s4 == 6:
    sub4 = "English"
elif s4 == 7:
    sub4 = "Spanish"
elif s4 == 8:
    sub4 = "German"
elif s4 == 9:
    sub4 = "French"
elif s4 == 0:
    sub4 = "null"

if s4 != 0:
    print(sub4, ": ", end='', sep='')
    v4 = int(input())
    while v4 < 100 or v4 > 200:
        print("incorrect data")
        print(sub4, ": ", end='', sep='')
        v4 = int(input())
else:
    v4 = "null"

# print(attestation, ukr, math, kReg, s3, sub3, s4, sub4, v3, v4)




# -------------------------------------------------------
# подсоединение к БД
conn = sqlite3.connect('specialties.db')
c = conn.cursor()

# очиста списка абитуриентов
c.execute("DELETE FROM student")


# c.execute("INSERT INTO student VALUES(1,", attestation, ",", sub3, ",", sub4, ",", ukr, ",", math, ",", v3, ",", v4, ",", kReg, ")")
c.execute("INSERT INTO student VALUES(1, ?, ?, ?, ?, ?, ?, ?, ? )", (attestation, sub3, sub4, ukr, math, v3, v4, kReg))

"""
c.execute('''
INSERT INTO student 
VALUES 
(1, 10.5, 'English', 'Physics', 180, 180, 180, 170, 1.0)
''')
"""

# вывод списка студентов и специальностей
print("\nstudents: ")
for row in c.execute('''SELECT * FROM student'''):
    print(row)

print("\nspecialities: ")
for row in c.execute('''SELECT * FROM speciality'''):
    print(row)




print("\nRecommended specialities: ")
# формирование балла по специальности
# балл аттестата из 12-бальной с-мы в 200-балльную переводится по формуле (attestation * 10 + 80)
for row in c.execute('''
SELECT speciality.name, 
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


    END score
FROM student, speciality 
WHERE 
    Ukrainian >= minUkr AND 
    Math >= minMath AND 
    score >= lastYearMin AND 
    score is not null
'''):
    print(row)


conn.commit()
conn.close()

