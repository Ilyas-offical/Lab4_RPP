import os
import csv
from typing import List, Dict, Iterator, Generator


class Person:
    """Базовый класс для персоны"""

    def __init__(self, id: int, name: str, email: str):
        self._id = id
        self._name = name
        self._email = email

    def __setattr__(self, name: str, value: str) -> None:
        if name == '_id' and not isinstance(value, int):
            raise ValueError("ID должен быть целым числом")
        if name in ('_name', '_email') and not isinstance(value, str):
            raise ValueError(f"{name[1:]} должен быть строкой")
        super().__setattr__(name, value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id}, name='{self._name}')"

    @staticmethod
    def validate_email(email: str) -> bool:
        """Статический метод для проверки email"""
        return '@' in email and '.' in email.split('@')[-1]


class Student(Person):
    """Класс студента, наследуется от Person"""

    def __init__(self, id: int, name: str, email: str, group: str):
        super().__init__(id, name, email)
        self._group = group

    def __setattr__(self, name: str, value: str) -> None:
        if name == '_group' and not isinstance(value, str):
            raise ValueError("Группа должна быть строкой")
        super().__setattr__(name, value)

    def __repr__(self) -> str:
        return f"Student(id={self._id}, name='{self._name}', group='{self._group}')"


class StudentCollection:
    """Коллекция студентов с итератором и индексацией"""

    def __init__(self):
        self._students = []

    def __iter__(self) -> Iterator[Student]:
        return iter(self._students)

    def __getitem__(self, index: int) -> Student:
        return self._students[index]

    def __len__(self) -> int:
        return len(self._students)

    def __repr__(self) -> str:
        return f"StudentCollection(students={len(self._students)})"

    def add_student(self, student: Student) -> None:
        self._students.append(student)

    def sort_by_name(self) -> None:
        self._students.sort(key=lambda x: x._name)

    def sort_by_id(self) -> None:
        self._students.sort(key=lambda x: x._id)

    def filter_by_group(self, group: str) -> Generator[Student, None, None]:
        for student in self._students:
            if student._group == group:
                yield student

    @staticmethod
    def count_files_in_directory(directory: str) -> int:
        return len([name for name in os.listdir(directory)
                    if os.path.isfile(os.path.join(directory, name))])

    def save_to_csv(self, filename: str) -> None:
        with open(filename, mode='w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['№', 'ФИО', 'email', 'группа'])
            for student in self._students:
                writer.writerow([student._id, student._name,
                                 student._email, student._group])

    def load_from_csv(self, filename: str) -> None:
        with open(filename, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_student(Student(
                    id=int(row['№']),
                    name=row['ФИО'],
                    email=row['email'],
                    group=row['группа']
                ))


def main():
    # 1. Подсчет файлов в директории
    directory = input("Введите путь к директории для подсчета файлов: ").strip()
    file_count = StudentCollection.count_files_in_directory(directory)
    print(f"\nКоличество файлов в директории '{directory}': {file_count}\n")

    # 2. Работа с данными студентов
    students = StudentCollection()
    filename = 'data.csv'

    try:
        students.load_from_csv(filename)
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return

    # 2.1. Сортировка по строковому полю (ФИО)
    print("\nСтуденты, отсортированные по ФИО:")
    students.sort_by_name()
    for student in students:
        print(student)

    # 2.2. Сортировка по числовому полю (№)
    print("\nСтуденты, отсортированные по номеру:")
    students.sort_by_id()
    for student in students:
        print(student)

    # 2.3. Фильтрация по группе
    group_filter = input("\nВведите группу для фильтрации студентов: ")
    print(f"\nСтуденты из группы {group_filter}:")
    for student in students.filter_by_group(group_filter):
        print(student)

    # 3. Добавление нового студента
    print("\nДобавление нового студента:")
    new_student = Student(
        id=int(input("Номер: ")),
        name=input("ФИО: "),
        email=input("Email: "),
        group=input("Группа: ")
    )
    students.add_student(new_student)
    students.save_to_csv(filename)
    print("\nНовый студент добавлен, данные сохранены в файл.")


if __name__ == "__main__":
    main()