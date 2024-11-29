import pytest
import os
from unittest.mock import patch, MagicMock
from task_manager import TaskManager, Task

@pytest.fixture
def task_manager():
    test_file = 'test_tasks.json'
    manager = TaskManager(test_file)
    yield manager
    if os.path.exists(test_file):
        os.remove(test_file)


def test_create_task(task_manager):
    """Тест на создание задачи."""
    task = task_manager.create_task(
        title="Тестовая задача",
        description="Описание задачи",
        category="Работа",
        due_date="2024-12-31",
        priority="Высокий"
    )
    assert task.title == "Тестовая задача"
    assert task.description == "Описание задачи"
    assert task.category == "Работа"
    assert task.due_date == "2024-12-31"
    assert task.priority == "Высокий"
    assert task.status == "Не выполнена"


def test_complete_task(task_manager):
    """Тест на выполнение задачи."""
    task = task_manager.create_task(
        title="Тестовая задача",
        description="Описание задачи",
        category="Работа",
        due_date="2024-12-31",
        priority="Высокий"
    )
    task_manager.complete_task(task.id)
    assert task.status == "Выполнена"


def test_find_task(task_manager):
    """Тест на поиск задачи по ID."""
    task = task_manager.create_task(
        title="Тестовая задача",
        description="Описание задачи",
        category="Работа",
        due_date="2024-12-31",
        priority="Высокий"
    )
    found_task = task_manager.find_task(task.id)
    assert found_task.id == task.id
    assert found_task.title == task.title


def test_delete_task_by_id(task_manager):
    """Тест на удаление задачи по ID."""
    task = task_manager.create_task(
        title="Тестовая задача",
        description="Описание задачи",
        category="Работа",
        due_date="2024-12-31",
        priority="Высокий"
    )
    task_manager.delete_task(task_id=task.id)
    with pytest.raises(ValueError, match="Задача не найдена."):
        task_manager.find_task(task.id)


def test_edit_task(task_manager):
    """Тест на редактирование задачи."""
    task = task_manager.create_task(
        title="Тестовая задача",
        description="Описание задачи",
        category="Работа",
        due_date="2024-12-31",
        priority="Высокий"
    )

    updated_data = {
        "title": "Обновленный заголовок",
        "description": "Обновленное описание",
        "category": "Личное",
        "due_date": "2025-01-01",
        "priority": "Низкий",
        "status": "Не выполнена"
    }

    task_manager.edit_task(task, updated_data)

    updated_task = task_manager.find_task(task.id)
    assert updated_task.title == "Обновленный заголовок"
    assert updated_task.description == "Обновленное описание"
    assert updated_task.category == "Личное"
    assert updated_task.due_date == "2025-01-01"
    assert updated_task.priority == "Низкий"


def test_search_tasks(task_manager):
    """Тест на поиск задач."""
    task1: Task = task_manager.create_task(
        title="Тестовая задача 1",
        description="Описание задачи 1",
        category="Работа",
        due_date="2024-12-31",
        priority="Высокий"
    )
    task2: Task = task_manager.create_task(
        title="Тестовая задача 2",
        description="Описание задачи 2",
        category="Личное",
        due_date="2025-01-01",
        priority="Низкий"
    )

    results = task_manager.search_tasks(keyword="Тестовая задача")
    assert len(results) == 2

    results = task_manager.search_tasks(category="Работа")
    assert len(results) == 1
    assert results[0].id == task1.id

    results = task_manager.search_tasks(status="Не выполнена")
    assert len(results) == 2


def test_view_tasks(task_manager):
    """Тест на просмотр всех задач."""
    task_manager.create_task(
        title="Тестовая задача",
        description="Описание задачи",
        category="Работа",
        due_date="2024-12-31",
        priority="Высокий"
    )
    tasks = task_manager.view_tasks()
    assert len(tasks) == 1


def test_load_tasks_from_file(task_manager):
    """Тест на загрузку задач из файла."""
    task_manager.create_task(
        title="Тестовая задача",
        description="Описание задачи",
        category="Работа",
        due_date="2024-12-31",
        priority="Высокий"
    )

    # Создаем новый экземпляр TaskManager, чтобы проверить загрузку
    new_manager = TaskManager("test_tasks.json")
    assert len(new_manager.view_tasks()) == 1


def test_delete_task_by_category(task_manager):
    """Тест на удаление задач по категории."""
    task_manager.create_task(
        title="Тестовая задача 1",
        description="Описание задачи 1",
        category="Работа",
        due_date="2024-12-31",
        priority="Высокий"
    )
    task_manager.create_task(
        title="Тестовая задача 2",
        description="Описание задачи 2",
        category="Работа",
        due_date="2025-01-01",
        priority="Низкий"
    )

    task_manager.delete_task(category="Работа")
    assert len(task_manager.view_tasks()) == 0