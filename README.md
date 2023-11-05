# Описание
Сайт с расписанием для студентов и преподавателей НГТУ им Р. Е. Алексеева
# Системные требования
- Windows 10 или выше (Протестировано на Windows 10 22H2)
- Python 3.10 или выше (Протестировано на Python 3.12)
- PostgreSQL 16 или выше (Протестировано на PostgreSQL 16)
# Установка на Windows
1. `git clone https://github.com/Crocussys/Nedelapare.git` <br>
или по ssh `git@github.com:Crocussys/Nedelapare.git`
2. `cd .\Nedelapare\ `
3. `python -m venv .\venv`
4. `.\venv\Scripts\activate`
5. `pip install -r requirements.txt`
# Запуск
1. `.\venv\Scripts\activate`<br>
2. `cd .\www`
4. `python manage.py runserver`