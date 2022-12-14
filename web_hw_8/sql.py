import random
from random import randint

import psycopg2
from faker import Faker

fake = Faker()

conn = psycopg2.connect(dbname='postgres', user='postgres',
                        password='---', host='localhost')
cursor = conn.cursor()

# Створення таблиць:

create_table_groups = """ DROP TABLE IF EXISTS groups CASCADE;
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
); 
"""

create_table_students = """ DROP TABLE IF EXISTS students CASCADE;
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    group_id INTEGER,
    CONSTRAINT group_of_student
    FOREIGN KEY(group_id)
    REFERENCES groups(id)
    ON DELETE SET NULL
);
CREATE INDEX student_name_index ON students (name);
"""

create_table_teachers = """DROP TABLE IF EXISTS teachers CASCADE;
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL 
);
"""
create_table_subjects = """ DROP TABLE IF EXISTS subjects CASCADE;
CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    teacher_id INTEGER,
    CONSTRAINT teacher_of_subject
    FOREIGN KEY(teacher_id)
    REFERENCES teachers(id)
    ON DELETE SET NULL
);
"""
create_table_marks = """ DROP TABLE IF EXISTS marks;
CREATE TABLE marks (
    id SERIAL PRIMARY KEY,
    mark SMALLINT NOT NULL,
    subject_id INTEGER,
    student_id INTEGER,
    acquired_at TIMESTAMP,
    CONSTRAINT mark_of_student
    FOREIGN KEY(student_id)
    REFERENCES students(id)
    ON DELETE CASCADE,
    CONSTRAINT mark_of_subject
    FOREIGN KEY(subject_id)
    REFERENCES subjects(id)
    ON DELETE CASCADE
); 
"""
dates = (fake.date_this_month(), fake.date_this_month(), fake.date_this_month(),)
data_groups = [fake.job for name in range(3)]
data_students = [fake.name for name in range(30)]
data_subjects = [fake.word for name in range(5)]
data_teachers = [fake.name for name in range(3)]
data_marks = []

for i in range(1, len(data_students) + 1):
    for j in range(20):
        data_marks.append((randint(1, 12), randint(1, 3), i, random.choice(dates),))

cursor.execute(create_table_groups)
cursor.execute(create_table_students)
cursor.execute(create_table_teachers)
cursor.execute(create_table_subjects)
cursor.execute(create_table_marks)
cursor.executemany(""" INSERT INTO groups (name) VALUES (%s) """, data_groups)
cursor.executemany(""" INSERT INTO students (name, group_id) VALUES (%s, %s)""", data_students)
cursor.executemany(""" INSERT INTO teachers (name) VALUES (%s) """, data_teachers)
cursor.executemany(""" INSERT INTO subjects (name, teacher_id) VALUES (%s, %s) """, data_subjects)
cursor.executemany(""" INSERT INTO marks (mark, subject_id, student_id, acquired_at) VALUES (%s, %s, %s, %s) """,
                   data_marks)
                   
# Виконання запитів до бази даних:
print('1 студент із найвищим середнім балом з одного предмета.')
cursor.execute("""select
	s.id,
	s.name,
	avg(m.mark) as average_mark
from
	students s
join marks as m on m.student_id = s.id 
where m.subject_id = %s
group by s.id 
order by average_mark desc
limit 1;""", (2,))
print(cursor.fetchall())

print("Середній бал у групі з одного предмета.")
cursor.execute("""select
avg(m.mark) as average_mark
from
marks m
join students as s on m.student_id = s.id 
where m.subject_id = %s and s.group_id = %s
group by s.group_id; """, (3, 2,))
print(cursor.fetchall())

print("5 студентів з найбільшим середнім балом з усіх предметів.")
cursor.execute("""select
	s.id,
	s.name,
	avg(m.mark) as average_mark
from
	students s
join marks as m on m.student_id = s.id
group by s.id 
order by average_mark desc 
limit 5; """)
print(cursor.fetchall())

print("Середній бал у потоці.")
cursor.execute("""select
avg(m.mark) as average_mark
from
marks m
join students as s on m.student_id = s.id 
where s.group_id = %s
group by s.group_id;""", (2,))
print(cursor.fetchall())

print("Курси, які веде викладач.")
cursor.execute("""select 
s.name,
t.name
from
subjects s 
join teachers as t on s.teacher_id = t.id;""")
print(cursor.fetchall())

print("Список студентів у групі.")
cursor.execute("""select
s.name
from
students s 
where s.group_id  = %s;""", (3,))
print(cursor.fetchall())

print("Оцінки студентів у групі з предмета.")
cursor.execute("""select
m.mark,
s."name" 
from
marks m
join students as s on m.student_id = s.id 
where m.subject_id = %s and s.group_id = %s;""", (3, 2))
print(cursor.fetchall())

print("Оцінки студентів у групі з предмета на останньому занятті.")
cursor.execute(""" select
m.mark,
s."name",
m.acquired_at
from
marks m
join students as s on m.student_id = s.id 
where m.subject_id = %s and s.group_id = %s and m.acquired_at = (select max(acquired_at) from marks ); """, (3, 2))
print(cursor.fetchall())

print("Список курсів, які відвідує студент.")
cursor.execute(""" select
	s.name,
	subs."name"
from
	students s
join marks as m on
	s.id = m.student_id
join subjects as subs on
	m.subject_id = subs.id
where
	s.id = %s
group by
	subs.id, s."name" ; """, (18,))
print(cursor.fetchall())

print("Список курсів, які викладає викладач.")
cursor.execute(""" select
	s.name,
	subs."name",
	t."name" 
from
	students s
join marks as m on
	s.id = m.student_id
join subjects as subs on
	m.subject_id = subs.id
join teachers as t on subs.teacher_id = t.id 
where
	s.id = %s and subs.teacher_id  = %s
group by
	subs.id, s."name", t."name"  ;""", (18, 2))
print(cursor.fetchall())

print("Середній бал, який викладач ставить студенту.")
cursor.execute(""" select
	avg(m.mark) as average_mark
from
	marks m
join subjects as subs on
	m.subject_id = subs.id
where
	m.student_id = %s
	and subs.teacher_id = %s
group by
	subs.teacher_id,
	m.student_id ; """, (15, 3))
print(cursor.fetchall())

print("Середній бал, який ставить викладач.")
cursor.execute(""" select
	avg(m.mark) as average_mark
from
	marks m
join subjects as subs on
	m.subject_id = subs.id
where
	subs.teacher_id = %s
group by
	subs.teacher_id;""", (3,))
print(cursor.fetchall())

conn.commit()
cursor.close()
conn.close()
