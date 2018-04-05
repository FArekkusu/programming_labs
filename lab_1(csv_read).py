import csv

# read from an existing .csv file
with open("students.csv", encoding="utf-8") as file:
    students = [x for x in csv.reader(file)][1:]

# filter STUDENTS by last column being "TRUE"
students = list(filter(lambda x: x[-1] == "TRUE", students))

# replace array with an array of names and average results
students = [[student[0], sum([int(x) for x in student[1:-1]]) / 5] for student in students]

# sort students by their average results
students = sorted(students, key=lambda x: x[1], reverse=True)

# get 40% of students
students = students[:len(students) * 2 // 5]

# write to a new .csv file
with open("filtered_students.csv", "w", encoding="utf-8", newline="") as new_file:
    content = csv.writer(new_file)
    for student in students:
        content.writerow([student[0], str(student[1])])