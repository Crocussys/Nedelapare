# Описание
Nedelapare - веб-сервис с электронным учебным расписанием занятий для студентов и преподавателей.

До недавнего времени существовало мобильное приложение с электронным расписанием занятий в НГТУ им Р. Е. Алексеева, но на сегодняшний день, оно больше не поддерживается разработчиками и было удалено из App Store и Google Play.

Так же, в настоящее время расписание рассылается в Excel таблицах, в которых неудобно искать и смотреть информацию. Например, для студентов важен лишь один столбец, содержащий неотсортированные данные. А для преподавателей неудобно находить свои занятия по всей таблице. Если появляется необходимость перенести занятия в другую аудиторию, то трудно определить свободный кабинет и оперативно решить этот вопрос.

Для решения текущих проблем, принято решения разработать новый веб-сервис на основе мирового опыта и предыдущих решений с целью оптимизации работы с учебном расписанием с любого устройства.
# Системные требования
Docker Engine 19.03.0+
# Установка
1. Клонируем репозиторий

`git clone https://github.com/Crocussys/Nedelapare.git` <br>
или по ssh `git clone git@github.com:Crocussys/Nedelapare.git`

2. Переходим в директорию

`cd Nedelapare`

3. Устанавливаем через Docker

`docker compose build`
# Запуск
С помощью Docker

`docker compose up`