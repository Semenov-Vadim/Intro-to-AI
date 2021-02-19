import sqlite3

conn = sqlite3.connect('specialties.db')
c = conn.cursor()

'''
предметы зно

History
Biology
Geography
Physics
Chemistry
English
Spanish
German
French
'''



# """
c.execute('''DROP TABLE student ''')

#Create table
c.execute('''CREATE TABLE student(
studentId int PRIMARY KEY NOT NULL,
attestation float,
sub3 varchar(50),
sub4 varchar(50),
Ukrainian tinyint,
Math tinyint,
v3 tinyint,
v4 tinyint
)''')


# Insert a row of data
c.execute('''
INSERT INTO student 
VALUES 
(1, 10.5, 'English', 'Physics', 189, 172, 179, 175)
''')

"""
c.execute('''
INSERT INTO student
VALUES 
((SELECT MAX(studentId) + 1 FROM student), 11.2, 'History', 'English', 170, 172, 160, 175)
''')
"""

# ---------------------------------------------------

#"""
c.execute('''DROP TABLE speciality ''')

c.execute('''CREATE TABLE speciality(
specId int PRIMARY KEY NOT NULL,
name varchar(100),
city varchar(100),
university varchar(100),
school varchar(100),
lastYearMin float,
sub3 varchar(50),
sub4 varchar(50),

kUkr float,
kMath float, 
ksub34 float,
kAttestation float,
minUkr tinyint,
minMath tinyint,
minSub34 tinyint
)''')


c.execute('''
INSERT INTO speciality 
VALUES 
(1, '122 Computer Science', 'Kharkiv', 'VN Karazin Kharkiv National University', 'MIF', 164.383, 'English', 'Physics', 
0.2, 0.5, 0.2, 0.1, 100, 140, 100)
''')

c.execute('''
INSERT INTO speciality VALUES 
((SELECT MAX(specId) + 1 FROM speciality), '061 Journalism', 'Kharkiv', 'VN Karazin Kharkiv National University', 'FMIL', 198.390, 'English', 'History', 
0.4, 0.3, 0.2, 0.1, 100, 110, 100),
((SELECT MAX(specId) + 2 FROM speciality), '054 Sociology', 'Kharkiv', 'VN Karazin Kharkiv National University', 'SF', 180.744, 'English', 'History', 
0.35, 0.2, 0.35, 0.1, 100, 100, 100),
((SELECT MAX(specId) + 3 FROM speciality), '105 Applied physics and nanomaterials', 'Kharkiv', 'VN Karazin Kharkiv National University', 'FRBELKS', 146.072, 'English', 'Physics', 
0.2, 0.4, 0.3, 0.1, 100, 110, 110),
((SELECT MAX(specId) + 4 FROM speciality), '053 Psychology', 'Kharkiv', 'VN Karazin Kharkiv National University', 'FP', 179.826, 'English', 'Biology', 
0.25, 0.4, 0.25, 0.1, 100, 110, 110),

((SELECT MAX(specId) + 5 FROM speciality), '055 Psychology', 'Kharkiv', 'VN Karazin Kharkiv National University', 'FP', 179.826, 'English', 'Biology', 
0.25, 0.4, 0.25, 0.1, 100, 180, 110),
((SELECT MAX(specId) + 6 FROM speciality), '056 Psychology', 'Kharkiv', 'VN Karazin Kharkiv National University', 'FP', 179.826, 'Physics', 'Biology', 
0.25, 0.4, 0.25, 0.1, 100, 110, 110),
((SELECT MAX(specId) + 7 FROM speciality), '057 Psychology', 'Kharkiv', 'VN Karazin Kharkiv National University', 'FP', 179.826, 'Spanish', 'Chemistry', 
0.25, 0.4, 0.25, 0.1, 100, 110, 110)
''')

#"""



# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.'''
conn.close()


