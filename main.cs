// Роботу виконав студент групи ІП-72, Федоров Олександр Вікторович, варіант - 24.
// Індивідуальні завдання:
//    №2 - змінити алгоритм порівяння екземплярів класу "Людина"
//    №3 - додати інтерфейс для виведення оцінки за екзамен у форматах національному/ECTS
//    №8 - додати ітератор до класу "Студент" для виведення диференційованих екзаменів
//    №11 - додати метод для обчислення віку людини
//
// Зауваження: консоль Windows може некоректно відображати деякі букви українського алфавіту
// при спробі запустити скомпільований файл "main.exe"

using System;
using System.Linq;
using System.Collections;
using System.Collections.Generic;

class Person
{
  public string firstName;
  public string lastName;
  private DateTime _birthDate;

  // getter та setter року народження
  public int birthDate
  {
    get { return _birthDate.Year; }
    set { _birthDate = new DateTime(value, _birthDate.Month, _birthDate.Day); }
  }

  // конструктор за замовчуванням
  public Person()
  {
    firstName = "Іван";
    lastName = "Іванов";
    _birthDate = DateTime.Now;
  }

  // конструктор, який приймає аргументи
  public Person(string first, string last, DateTime date)
  {
    firstName = first;
    lastName = last;
    _birthDate = date;
  }

  // вивід інформації про людину
  public virtual void PrintFullInfo()
  {
    Console.WriteLine(String.Format("Ім'я: {0} {1}", lastName, firstName));
    Console.WriteLine(String.Format("Дата народження: {0}", _birthDate.ToString("dd-MM-yyyy")));
  }

  // індивідуальне завдання №2:
  // перевантаження метода порівняння
  public override bool Equals(object o)
  {
    var item = o as Person;
    if (item == null)
    {
      return false;
    }
    return this == item;
  }

  // перевантаження методу для отримання хеша об'єкту
  public override int GetHashCode()
  {
    return String.Format("{} {} {}", firstName, lastName, _birthDate.ToString("dd-MM-yyyy")).GetHashCode();
  }

  // перевантаження оператора рівності
  public static bool operator ==(Person p1, Person p2)
  {
    bool first = p1.firstName == p2.firstName;
    bool last = p1.lastName == p2.lastName;
    int date = DateTime.Compare(p1._birthDate, p2._birthDate);
    return first && last && date == 0;
  }

  // перевантаження методу нерівності
  public static bool operator !=(Person p1, Person p2)
  {
    return !(p1 == p2);
  }

  // індивідуальне завдання №11:
  // метод для розрахунку віку людини
  public int calculateAge()
  {
    DateTime now = DateTime.Now;
    int pYear = birthDate,
        pMonth = _birthDate.Month,
        pDay = _birthDate.Day;
    return now.Year - pYear - (pMonth > now.Month || (pMonth == now.Month && pDay > now.Day) ? 1 : 0);
  }
}


// індивідуальне завдання №3 част. 1:
// інтерфейс для виведення оцінки за екзамен
public interface IMarkName
{
  string NationalScaleName();
  string EctsScaleName();
}



class Examination : IMarkName
{
  public int semester;
  public string examName;
  public string teacherName;
  public int result;
  public bool differentiated;
  public DateTime examDate;

  // конструктор за замовчуванням
  public Examination()
  {
    semester = 1;
    examName = "Основи програмування";
    teacherName = "Іван І.І.";
    result = 100;
    differentiated = true;
    examDate = DateTime.Now;
  }

  // констуктор, який приймає аргументи
  public Examination(int sem, string exam, string teacher, int res, bool dif, DateTime date)
  {
    semester = sem;
    examName = exam;
    teacherName = teacher;
    result = res;
    differentiated = dif;
    examDate = date;
  }

  // перевантаження методу конвертації у рядок
  public override string ToString()
  {
    return String.Format("Екзамен: {0}, Викладач: {1}, Оцінка: {2}", examName, teacherName, result);
  }

  // індивідуальне завдання №3 част. 2:
  // метод для виведення оцінки у національному форматі
  public string NationalScaleName()
  {
    return result >= 95 ? "Відмінно" :
      result >= 85 ? "Дуже добре" :
      result >= 75 ? "Добре" :
      result >= 65 ? "Задовільно" :
      result >= 60 ? "Достатньо" : "Незадовільно";
  }

  // метод для виведення оцінки у форматі ECTS
  public string EctsScaleName()
  {
    return result >= 95 ? "A" :
      result >= 85 ? "B" :
      result >= 75 ? "C" :
      result >= 65 ? "D" :
      result >= 60 ? "E" : "F";
  }
}



class Student : Person, IEnumerable<Examination>
{
  public enum Education
  {
    Master,
    Bachelor,
    SecondEducation,
    PhD
  }

  public Education currentEducation;
  public string groupName;
  public int transcriptNumber;
  public Examination[] passedExams;
  
  public double averageMark
  {
    get { return (double)passedExams.Aggregate(0, (x, y) => x + y.result) / passedExams.Length; } 
  }

  // метод для додавання студенту екзаменів
  public void AddExams(Examination[] examList)
  {
    passedExams = examList;
  }

  // перевантаження методу конвертації у рядок
  public override string ToString()
  {
    return String.Format("Ім'я: {0} {1}, Група: {2}", lastName, firstName, groupName);
  }

  // перевантаження методу для виводу інформації про студента
  public override void PrintFullInfo()
  {
    string exams = string.Join("\n\t   ", passedExams.Select(x => x.ToString()));

    Console.WriteLine(String.Format("Рівень кваліфікації: {0}", currentEducation));
    Console.WriteLine(String.Format("Група: {0}", groupName));
    Console.WriteLine(String.Format("Номер залікової книжки: {0}", transcriptNumber));
    Console.WriteLine(String.Format("Екзамени: [{0}]", exams));
    Console.WriteLine(String.Format("Середня оцінка: {0}", averageMark));
  }

  // індивідуальне завдання №8:
  // ітератор для перелічення іспитів (диференційованих екзаменів)
  public IEnumerator<Examination> GetEnumerator()
  {
    for (int i = 0; i < passedExams.Length; i++)
    {
      if (passedExams[i].differentiated == true)
      {
        yield return passedExams[i];
      }
    }
  }

  IEnumerator IEnumerable.GetEnumerator()
  {
    return GetEnumerator();
  }
}



class MainClass
{
  public static void Main (string[] args)
  {
    // основне завдання:
    // створення екземпляра класу "Студент"
    Student student = new Student();
    student.firstName = "Олександр";
    student.lastName = "Федоров";
    student.currentEducation = Student.Education.Bachelor;
    student.groupName = "ІП-72";
    student.transcriptNumber = 29;

    // конвертація екземпляра у рядок
    Console.WriteLine(student.ToString());
    
    Console.WriteLine();

    // створення масиву екзаменів, використовуючи конструктор за замовчуванням, змінюючи значення оцінки
    // за кожен з них; кожен другий екзамен вказується як диференційований (іспит)

    // набір випадкових чисел - середня оцінка: 494/6  ==  82 + 1/3  ==  82.3333333333
    int[] results = {75, 61, 99, 84, 83, 92};
    Examination[] examsArray = new Examination[results.Length];

    for (int i = 0; i < results.Length; i++)
    {
      examsArray[i] = new Examination();
      examsArray[i].differentiated = i % 2 == 1;
      examsArray[i].result = results[i];
    }

    // додавання екзаменів студенту і вивід інформації про нього
    student.AddExams(examsArray);
    student.PrintFullInfo();

    Console.WriteLine();


    // індивідуальне завдання №2:
    // створення 5 екземплярів класу "Людина":
    // друга однакова із першою, третя відрізняється прізвищем, четверта - ім'ям, п'ята - датою народження
    Person p1 = new Person("A", "A", new DateTime(2000, 1, 2));
    Person p2 = new Person("A", "A", new DateTime(2000, 1, 2));
    Person p3 = new Person("A", "B", new DateTime(2000, 1, 2));
    Person p4 = new Person("B", "A", new DateTime(2000, 1, 2));
    Person p5 = new Person("A", "A", new DateTime(1999, 1, 2));
    Console.WriteLine(String.Format("{0} {1} {2} {3}", p1 == p2, p1 == p3, p1 == p4, p1 == p5));
    Console.WriteLine(String.Format("{0} {1} {2} {3}", p1 != p2, p1 != p3, p1 != p4, p1 != p5));

    Console.WriteLine();

    // індивідуальне завдання №3:
    // створення екземпляра класу "Екзамен", поступове зниження оцінки за нього, аби показати,
    // як змінюється відображення оцінки в форматах: національному/ECTS
    Examination exam = new Examination();
    for (int i = 0; i < 6; i++) {
      exam.result -= i == 0 || i == 4 ? 5 : 10;
      Console.WriteLine(String.Format("{0} ({1})", exam.NationalScaleName(), exam.EctsScaleName()));
    }

    Console.WriteLine();
    

    // індивідуальне завдання №8:
    // ітерація по створеному раніше студенту, яка повинна вивести на екран лише диференційовані екзамени
    foreach (Examination currentExam in student)
    {
      Console.WriteLine(currentExam.ToString());
    }

    Console.WriteLine();


    // індивідуальне завдання №11:
    // розрахунок віку людини

    // поточний місяць, перше число вже настало - 18 років
    p1 = new Person("A", "A", new DateTime(2000, 12, 1));

    // поточний місяць, тридцять перше число ще не настало - 17 років
    p2 = new Person("A", "A", new DateTime(2000, 12, 31));

     // попередній місяць, в поточному місяці перше число вже настало - 18 років
    p3 = new Person("A", "A", new DateTime(2000, 11, 1));

    // попередній місяць, але тридцяте число поточного місяці ще не настало
    // (можлива помилка за неправильного алгоритму) - все одно 18 років
    p4 = new Person("A", "A", new DateTime(2000, 11, 30));

    Console.WriteLine(p1.calculateAge());
    Console.WriteLine(p2.calculateAge());
    Console.WriteLine(p3.calculateAge());
    Console.WriteLine(p4.calculateAge());

    Console.Read(); // очікування вводу користувачем, аби вікно програми не закривалося одразу
  }
}