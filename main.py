import sqlite3

conn = sqlite3.connect('specialties.db')

c = conn.cursor()

"""
c.execute('''
DELETE FROM student WHERE studentId = 2
''')
"""


print("students: ")
for row in c.execute('''SELECT * FROM student'''):
    print(row)

print("\nspecialities: ")
for row in c.execute('''SELECT * FROM speciality'''):
    print(row)


print()
# формирование балла по специальности
for row in c.execute('''
SELECT speciality.name, 
CASE 
    WHEN (((student.sub3 = speciality.sub3 OR student.sub3 = speciality.sub4) AND (student.sub4 = speciality.sub3 OR student.sub4 = speciality.sub4) AND v3 >= v4) OR 
        (student.sub3 = speciality.sub3 OR student.sub3 = speciality.sub4)) AND
        v3 >= minSub34
        THEN Ukrainian * kUkr + Math * kMath + attestation * kAttestation * 200/12 + v3 * ksub34
    
    WHEN (((student.sub3 = speciality.sub3 OR student.sub3 = speciality.sub4) AND  (student.sub4 = speciality.sub3 OR student.sub4 = speciality.sub4) AND v3 < v4) OR
        (student.sub4 = speciality.sub3 OR student.sub4 = speciality.sub4)) AND 
        v4 >= minSub34
        THEN Ukrainian * kUkr + Math * kMath + attestation * kAttestation * 200/12 + v4 * ksub34
    
    ELSE null


    END val
FROM student, speciality 
WHERE 
    Ukrainian >= minUkr AND 
    Math >= minMath AND 
    val >= lastYearMin AND 
    val is not null
'''):
    print(row)


conn.commit()
conn.close()

