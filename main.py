from menu_actions import (
    list_of_tasks,
    execute_task,
    delete_task,
    update_task_fields,
    search_task_by_id,
    search_tasks_with_filters,
    exit_program,
    add_new_task
)

from task_manager import TaskManager

MENU = [
    {
        "label": "Просмотр задач",
        "processor": list_of_tasks,
    },
    {
        "label": "Добавить задачу",
        "processor": add_new_task,
    },
    {
        "label": "Выполнить задачу",
        "processor": execute_task
    },
    {
        "label": "Удалить задачу",
        "processor": delete_task,
    },
     {
        "label": "Изменить задачу",
        "processor": update_task_fields,
    },
    {
        "label": "Поиск задачи по id",
        "processor": search_task_by_id,
    },
    {
        "label": "Поиск задач по фильтрам",
        "processor": search_tasks_with_filters,
    },
    {
        'label': "Выход",
        "processor": exit_program,
    }
]



def main():
    task_manager = TaskManager('tasks.json')
    while True:
        print("\nМенеджер задач")
        for index, menu_item in enumerate(MENU):
            print(f"{index+1}. {menu_item['label']}")

        choice = input("Выберите действие: ")
        try:
            choice = int(choice) - 1
            assert 0 <= choice < len(MENU)
        except Exception:
            print("Неверный выбор, попробуйте снова.")
            continue

        try:
            processor = MENU[choice]['processor']
            processor(task_manager)
        except StopIteration:
            break
        continue


if __name__ == "__main__":
    main()