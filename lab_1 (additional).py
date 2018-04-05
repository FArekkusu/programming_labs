with open("students.csv", "r", encoding="utf-8") as file:
    lines = [line for line in file.readlines()][1:]

split_lines = [line.split(",") for line in lines]
filtered_lines = [[line[0], sum(int(x) for x in line[1:-1])/5] for line in split_lines if "TRUE" in line[-1]]
sorted_lines = sorted(filtered_lines, key=lambda x: x[-1], reverse=True)
top_40_percent = sorted_lines[:len(sorted_lines)*2//5]

with open("filtered_students.csv", "w", encoding="utf-8", newline="\n") as new_file:
    to_write = [",".join([student[0], str(student[-1])]) for student in top_40_percent]
    new_file.write("\n".join(to_write))