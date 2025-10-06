"""
Модуль hello_world
Содержит функцию для возврата текстового сообщения
"""

def text():
    """
    Возвращает текстовое сообщениеpylint
    Returns:
        str: текстовое сообщение
    """
    message = "Hello World"
    return message

# Вызов функции для демонстрации
if __name__ == "__main__":
    print(text())