import json

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from robots.models import Robot
from .models import Order
from customers.models import Customer


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # валидация входных данных, на соответствие существующим в системе моделям.
            correct_data = ['customer', 'robot_serial']
            for value in correct_data:
                if value not in data:
                    return JsonResponse({'error': f'Поле {value} отсутствует в запросе'}, status=400)
            # валидация входных на количество символов для добавления в базу данных
            if len(data['robot_serial']) > 5:
                return JsonResponse(
                    {'error': 'Поле robot_serial может содержать не больше 5 символов'},
                    status=400)
            if '-' not in data['robot_serial']:
                return JsonResponse({'error': 'Неверный формат поля robot_serial (ожидалось: SS-SS)'}, status=400)

            robots_available = Robot.objects.all().values('serial')
            if data['robot_serial'] in [i['serial'] for i in robots_available]:
                return JsonResponse({'message': 'Этот робот доступен для заказа'}, status=201)
            else:
                try:
                    customer = Customer.objects.get(email=data['customer'])
                except:
                    new_customer = Customer(email=data['customer'])
                    new_customer.save()
                    customer = Customer.objects.get(email=data['customer'])

                robot_order = Order(robot_serial=data['robot_serial'], customer=customer)
                robot_order.save()
                return JsonResponse(
                    {
                        'message': 'Заказ занесен в базу данных, мы сообщим вам если этот робот станет доступен '},
                    status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Неверный формат, ожидаемый формат - JSON'}, status=400)
