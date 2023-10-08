# Как работать с этим кодом
Все pull requests сделаны со второго аккаунта, каждое задание это отдельная ветка форкнутого репозитория https://github.com/Vladlenuser/BST_test_project
Основная ветка master является изначальной (пустой) версией проекта.
Тестовый проект состоит из 3 заданий, каждое задание загружено отдельным pull request в этот репозиторий.
Мои личные пояснения по заданию описаны в файле about_task.md.
Так как для решения каждого следующего задания нужно было предыдущее то конечная версия проекта это third_task pull request - этот pull request содержит все 3 задания.

После скачивания кода нужно создать виртуальное окружение, это можно сделать установивив модуль venv

 python -m pip install --user virtualenv
 
Затем нужно создать само виртуальное окружение

 python -m venv venv
 
После, нужно его включить для этого нужно перейти в папку venv/Scripts и прописать activate

После того как мы разобрались с виртуальным окружением надо установить все нужные библиотеки, для этого нужно вернуться в корневую дирректорию
и в терминале прописать команду ( для каждого нового задания свой файл requirements.txt) 

 pip install -r requirements.txt

Все нужные миграции произведены, поэтому остается лишь запустить проект

 py manage.py runserver


# R4C - Robots for consumers

## Небольшая предыстория.
Давным-давно, в далёкой-далёкой галактике, была компания производящая различных 
роботов. 

Каждый робот(**Robot**) имел определенную модель выраженную двух-символьной 
последовательностью(например R2). Одновременно с этим, модель имела различные 
версии(например D2). Напоминает популярный телефон различных моделей(11,12,13...) и его версии
(X,XS,Pro...). Вне компании роботов чаще всего называли по серийному номеру, объединяя модель и версию(например R2-D2).

Также у компании были покупатели(**Customer**) которые периодически заказывали того или иного робота. 

Когда роботов не было в наличии - заказы покупателей(**Order**) попадали в список ожидания.

---
## Что делает данный код?
Это заготовка для сервиса, который ведет учет произведенных роботов,а также 
выполняет некие операции связанные с этим процессом.

Сервис нацелен на удовлетворение потребностей трёх категорий пользователей:
- Технические специалисты компании. Они будут присылать информацию
- Менеджмент компании. Они будут запрашивать информацию
- Клиенты. Им будут отправляться информация
___

## Как с этим работать?
- Создать для этого проекта репозиторий на GitHub
- Открыть данный проект в редакторе/среде разработки которую вы используете
- Ознакомиться с задачами в файле tasks.md
- Написать понятный и поддерживаемый код для каждой задачи 
- Сделать по 1 отдельному PR с решением для каждой задачи
- Прислать ссылку на своё решение
