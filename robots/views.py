import json
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pytz
from .models import Robot

import xlwt
from django.db.models import Count
from django.http import HttpResponse
from orders.models import Order

import smtplib
from email.mime.text import MIMEText


# Для отправки email сообщения
def email_send(customer, serial):
    sender = "7732469tl@gmail.com"
    password = "ptziyfbbkagfkaob"  # временный пароль для ненадежных приложений, пока могу предоставить, вскоре удалю
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    message = f'''Добрый день!
Недавно вы интересовались нашим роботом модели {serial[:2]}, версии {serial[3:]}. 
Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'''

    server.login(sender, password)
    msg = MIMEText(message)
    msg["Subject"] = "Robot.co"
    server.sendmail(sender, customer, msg.as_string())


# добавление созданного робота в базу данных с валидацией
@csrf_exempt
def robot_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # валидация входных данных, на соответствие существующим в системе моделям.
            correct_data = ['model', 'version', 'created']
            for value in correct_data:
                if value not in data:
                    return JsonResponse({'error': f'Поле {value} отсутствует в запросе'}, status=400)
            # валидация входных данных на правильность переданных даты и время
            try:
                created_datetime = datetime.strptime(data['created'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
                current_datetime = datetime.now(pytz.UTC)
                if created_datetime > current_datetime:
                    return JsonResponse({'error': 'Задано время в будущем'}, status=400)
            except ValueError:
                return JsonResponse({'error': 'Неверный формат времени (ожидалось: YYYY-MM-DD HH:MM:SS)'}, status=400)
            # валидация входных на количество символов для добавления в базу данных
            if len(data['version']) > 2 or len(data['model']) > 2:
                return JsonResponse(
                    {'error': 'Поля version, model могут содержать максимум 2 символа'},
                    status=400)
            # добавление робота в базу данных
            robot = Robot(
                serial=f"{data['model']}-{data['version']}",
                model=data['model'],
                version=data['version'],
                created=data['created'],
            )
            robot.save()
            try:
                orders = Order.objects.filter(robot_serial=f"{data['model']}-{data['version']}")
                # отправка сообщений всем заказчикам
                for i in orders:
                    email_send(i.customer.email, i.robot_serial)

            except:
                pass

            return JsonResponse({'message': 'Робот успешно создан'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Неверный формат, ожидаемый формат - JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Такой метод не прописан'}, status=405)


def export_to_excel(request):
    # Вычисляем дату понедельника и воскресенья последней недели
    current_date = datetime.now()
    current_weekday = current_date.weekday()
    last_monday = (current_date - timedelta(days=current_weekday + 7)).replace(hour=0, minute=0,
                                                                               second=0, microsecond=0)
    last_sunday = (last_monday + timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=0)

    # Создаем HttpResponse для загрузки Excel-файла
    response = HttpResponse(content_type='application/ms-excel')
    response[
        'Content-Disposition'] = f'attachment; filename="{last_monday.date()}--{last_sunday.date()}_robots.xls"'

    # Создаем новую книгу Excel
    wb = xlwt.Workbook(encoding='utf-8')
    sheets = 0
    date_style = xlwt.XFStyle()
    date_style.num_format_str = 'yyyy-mm-dd HH:mm:ss'

    robot_models = Robot.objects.filter(created__range=(last_monday, last_sunday)).values_list('model',
                                                                                               flat=True).distinct()
    for model in robot_models:
        # Добавляем новый лист Excel для каждой модели робота
        ws = wb.add_sheet(model)
        sheets += 1

        row_num = 0
        columns = ['Модель', 'Версия', 'Количество за неделю']

        # Заполняем первую строку листа заголовками столбцов
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        # Делаем Group by для удобного взаимодействия с объектами
        robots_by_model = Robot.objects.filter(created__range=(last_monday, last_sunday), model=model) \
            .values('model', 'version') \
            .annotate(count=Count('id'))

        # Для каждой версии создаем новую строку и заполняем ее
        for robot_by_version in robots_by_model:
            row_num += 1
            ws.write(row_num, 0, robot_by_version['model'])
            ws.write(row_num, 1, robot_by_version['version'])
            ws.write(row_num, 2, robot_by_version['count'])

    # Если роботов на последней неделе не произвели
    if sheets == 0:
        ws = wb.add_sheet('None')
        ws.write(1, 1, f'Роботов на неделе {last_monday.date()}-{last_sunday.date()} не произвели')

    wb.save(response)
    return response
