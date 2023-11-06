import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pytz
from .models import Robot


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
            if len(data['version']) != 2 or len(data['model']) != 2:
                return JsonResponse(
                    {'error': 'Поля version, model должны содержать 2 символа'},
                    status=400)
            # добавления робота в базу данных
            robot = Robot(
                serial=f"{data['model']}-{data['version']}",
                model=data['model'],
                version=data['version'],
                created=data['created'],
            )
            robot.save()

            return JsonResponse({'message': 'Робот успешно создан'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Неверный формат, ожидаемый формат - JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Такой метод не прописан'}, status=405)
