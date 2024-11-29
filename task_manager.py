import json
import os
from typing import List, Dict, Optional

class Task:
    """
     Класс, представляющий задачу.

     Атрибуты:
         id (int): Уникальный идентификатор задачи.
         title (str): Заголовок задачи.
         description (str): Описание задачи.
         category (str): Категория задачи.
         due_date (str): Срок выполнения задачи (в формате YYYY-MM-DD).
         priority (str): Приоритет задачи (Низкий, Средний, Высокий).
         status (str): Статус выполнения задачи (Выполнена/Не выполнена).
     """

    def __init__(
            self,
            id: Optional[int],
            title: str,
            description: str,
            category: str,
            due_date: str,
            priority: str,
            status: str = "Не выполнена"
    ):
        self.id = id if id else self._get_new_id()
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def make_completed(self):
        """Отметить задачу как выполненную."""
        self.status = "Выполнена"

    def to_dict(self) -> Dict:
        """Преобразовать задачу в словарь для сохранения в JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status
        }

    def to_presentation(self):
        print("--------------")
        print(f"Данные по id задачи -- {self.id}")
        print(f"Заголовок: {self.title}")
        print(f"Описание: {self.description}")
        print(f"Категория: {self.category}")
        print(f"Срок выполнения: {self.due_date}")
        print(f"Приоритет: {self.priority}")
        print(f"Статус выполнения: {self.status}")

    @staticmethod
    def _get_new_id() -> int:
        """Получить новый id + 1 задачи от максимального id среди созданных задач
        или 0, если это первая задача"""
        tasks = TaskManager().tasks
        max_id: int = 0
        if len(tasks) == max_id:
            return max_id
        for task in tasks:
            if max_id < task.id:
                max_id = task.id
        return max_id + 1


class TaskManager:
    """
    Класс для управления списком задач.
    """
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks: List[Task] = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        """Загрузить задачи из файла JSON."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)
                return [Task(**task) for task in tasks_data]
        return []

    def find_task(self, task_id) -> Task:
        """Найди задачи при помощи id задачи"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError("Задача не найдена.")

    def save_tasks(self):
        """Сохранить задачи в файл JSON."""
        with open(self.data_file, 'w', encoding='utf-8') as file:
            new_tasks: List[Dict] = [task.to_dict() for task in self.tasks]
            json.dump(new_tasks, file, ensure_ascii=False, indent=4)

    def create_task(
            self,
            title: str,
            description: str,
            category: str,
            due_date: str,
            priority: str
    ) -> Task:
        """Создать новую задачу."""
        new_task = Task(
            id=None,
            title=title,
            description=description,
            category=category,
            due_date=due_date,
            priority=priority
        )
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    def complete_task(self, task_id: int):
        """Отметить задачу как выполненную."""
        for task in self.tasks:
            if task.id == task_id:
                task.make_completed()
                self.save_tasks()
                return
        raise ValueError("Задача не найдена.")

    def edit_task(self, task: Task, data):
        """Редактировать поле задачи."""
        task.__dict__.update(data)
        self.save_tasks()

    def delete_task(self, task_id: Optional[int] = None, category: Optional[str] = None):
        """Удалить задачу/и из списка по ее id или категории."""
        if task_id is not None:
            self.tasks = [task for task in self.tasks if task.id != task_id]
        elif category is not None:
            self.tasks = [task for task in self.tasks if task.category != category]
        else:
            raise ValueError("Необходимо указать id или категорию.")
        self.save_tasks()

    def search_tasks(
            self,
            keyword: str = "",
            category: str = "",
            status: str = ""
    ) -> List[Task]:
        """Поиск задач по ключевым словам в заголовке или описании,
        по категории и/или статусу задачи.
        """
        results = self.tasks
        if keyword:
            results = [
                task for task in results
                if keyword.lower() in task.title.lower()
                   or keyword.lower() in task.description.lower()
            ]
        if category:
            results = [task for task in results if task.category.lower() == category.lower()]
        if status:
            results = [task for task in results if task.status.lower() == status.lower()]
        return results


    def view_tasks(self) -> List[Task]:
        """Показать все существующие задачи."""
        return self.tasks
