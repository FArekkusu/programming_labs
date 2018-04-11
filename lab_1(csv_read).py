import csv

with open("students.csv", encoding="utf-8") as file:
    students = [x for x in csv.reader(file)][1:]

students = list(filter(lambda x: x[-1] == "TRUE", students))
students = [[student[0], sum([int(x) for x in student[1:-1]]) / 5] for student in students]
students = sorted(students, key=lambda x: x[1], reverse=True)
students = students[:len(students) * 2 // 5]

with open("filtered_students.csv", "w", encoding="utf-8", newline="") as new_file:
    content = csv.writer(new_file)
    for student in students:
        content.writerow([student[0], str(student[1])])
