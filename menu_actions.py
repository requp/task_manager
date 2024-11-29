from typing import Dict

from task_manager import TaskManager, Task

from validators import (
    validate_title,
    validate_description,
    validate_category,
    validate_due_date,
    validate_priority,
    validate_task_id,
    validate_status
)

TASK_FORM = [
    {
        "field": "title",
        "label": "Название задачи",
        "validator": validate_title,
    },
    {
        "field": "description",
        "label": "Описание задачи",
        "validator": validate_description,
    },
    {
        "field": "category",
        "label": "Категория",
        "validator": validate_category,
    },
    {
        "field": "due_date",
        "label": "Срок выполнения (YYYY-MM-DD)",
        "validator": validate_due_date,
    },
    {
        "field": "priority",
        "label": "Приоритет (варианты: низкий, средний, высокий)",
        "validator": validate_priority,
    }
]


def ask_form(form, defaults = None) -> dict:
    data = {}
    if defaults is None:
        defaults = {}
    for field in form:
        default = defaults.get(field['field'])
        while True:
            if default:
                value = input(f"{field['label']} (или ENTER чтобы оставить {default}): ")
                value = value or default
            else:
                value = input(f"{field['label']}: ")
            try:
                field['validator'](value)
            except ValueError as ex:
                print(ex)
            else:
                break
        data[field['field']] = value
    return data


def list_of_tasks(task_manager: TaskManager):
    tasks = task_manager.view_tasks()
    if len(tasks):
        for task in tasks:
            task.to_presentation()
    else:
        print("нет задач")


def add_new_task(task_manager: TaskManager):
    data: Dict = ask_form(TASK_FORM)
    task_manager.create_task(**data)


def execute_task(task_manager: TaskManager):
    raw_task_id: str = input("Введите идентификатор задачи для выполнения: ")
    try:
        task_id: int = validate_task_id(raw_task_id)
        task_manager.complete_task(task_id)
        print("Задачи отмечена выполненой")
    except ValueError as ex:
        print(ex)


def delete_task(task_manager: TaskManager):
    raw_task_id: str = input("Введите идентификатор задачи для выполнения "
                             "(или оставьте пустым для удаления по категории): ")
    category = input("Введите категорию для удаления (или оставьте пустым для удаления по id): ")
    if raw_task_id:
        try:
            task_id: int = validate_task_id(raw_task_id)
            task_manager.delete_task(task_id=task_id)
            print("Задачи удалена успешно")
        except ValueError as e:
            print(e)
    elif category:
        task_manager.delete_task(category=category)
    else:
        print("Необходимо указать идентификатор или категорию.")


def update_task_fields(task_manager: TaskManager):
    raw_task_id: str = input("Введите идентификатор задачи для выполнения: ")
    custom_form = TASK_FORM[:]
    custom_form.append(
        {
        "field": "status",
        "label": "Статус (варианты: Выполнена, Не выполнена)",
        "validator": validate_status,
        }
    )
    try:
        task_id: int = validate_task_id(raw_task_id)
        task = task_manager.find_task(task_id=task_id)
        data = ask_form(custom_form, task.to_dict())
        task_manager.edit_task(task, data)
        task_manager.find_task(task_id=task_id).to_presentation()
    except ValueError as ex:
        print(ex)


def search_task_by_id(task_manager: TaskManager):
    raw_task_id: str = input("Введите идентификатор задачи для поиска: ")
    try:
        task_id: int = validate_task_id(raw_task_id)
        task: Task = task_manager.find_task(task_id)
        task.to_presentation()
    except ValueError as ex:
        print(ex)

def search_tasks_with_filters(task_manager: TaskManager):
    keyword = input("Введите ключевое слово для поиска (или оставьте пустым): ")
    category = input("Введите категорию для поиска (или оставьте пустым): ")
    status = input("Введите статус для поиска (выполнена/не выполнена, или оставьте пустым): ")
    results = task_manager.search_tasks(keyword, category, status)
    for task in results:
        task.to_presentation()


def exit_program():
    raise StopIteration()