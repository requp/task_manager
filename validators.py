from datetime import datetime
from typing import Tuple, Dict, Any, Optional

MIN_LEN_TITLE: int = 1
MAX_LEN_TITLE: int = 100
MIN_LEN_DESCRIPTION: int = 1
MAX_LEN_DESCRIPTION: int = 1000
MIN_LEN_CATEGORY: int = 1
MAX_LEN_CATEGORY: int = 50
PRIORITY_CHOICES: Tuple = ("Низкий", "Средний", "Высокий")
STATUS_CHOICES: Tuple = ("Не выполнена", "Выполнена")

def validate_task_id(raw_id: str) -> int:
    if not raw_id.isdigit():
        raise ValueError(
            f"Индентификатор не является целым числом"
        )
    task_id: int = int(raw_id)
    if task_id < 0:
        raise ValueError(
            f"Индентификатор не может быть меньше 0"
        )
    return task_id

def validate_title(title: str) -> str:
    if not (MIN_LEN_TITLE <= len(title) <= MAX_LEN_TITLE):
        raise ValueError(
            f"Длина названия задачи не входит в диапозон {MIN_LEN_TITLE} - {MAX_LEN_TITLE}"
        )
    return title

def validate_description(description: str) -> str:
    if not (MIN_LEN_DESCRIPTION <= len(description) <= MAX_LEN_DESCRIPTION):
        raise ValueError(
            f"Длина описания задачи не входит в диапозон {MIN_LEN_DESCRIPTION} - {MAX_LEN_DESCRIPTION}"
        )
    return description


def validate_category(category: str) -> str:
    if not (MIN_LEN_CATEGORY <= len(category) <= MAX_LEN_CATEGORY):
        raise ValueError(
            f"Длина категории задачи не входит в диапозон {MIN_LEN_CATEGORY} - {MAX_LEN_CATEGORY}"
        )
    return category


def validate_due_date(due_date: str) -> str:
    try:
        datetime.strptime(due_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Дата указана в неправильном формате")
    return due_date


def validate_priority(priority: str) -> str:
    if priority.capitalize() not in PRIORITY_CHOICES:
        raise ValueError("Введенный Вами приоритет не предусмотрен")
    return priority.capitalize()


def validate_status(status: str) -> str:
    if status.capitalize() not in STATUS_CHOICES:
        raise ValueError("Введенный Вами статус не предусмотрен")
    return status.capitalize()

VALIDATE_DICT: Dict = {
        "title": validate_title,
        "description": validate_description,
        "category": validate_category,
        "due_date": validate_due_date,
        "priority": validate_priority,
        "status": validate_status
    }

def validate_task_fields(kwargs) -> Dict:
    for key, value in kwargs.items():
        if key in VALIDATE_DICT:
            validate_field = VALIDATE_DICT[key]
            validate_field(value)
    return kwargs