from django.http import JsonResponse
import json
from . import one


def forecast(request,date,range_value,cluster):
    if request.method == "POST":
        input_data = json.loads(request.body)
        date = input_data.get('date')
        range_value = int(input_data.get('range_value'))
        cluster = input_data.get('cluster')

        result = one.get_input(date,range_value,cluster)


        print(result)
        return JsonResponse(result)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def forecast2(request,date,range_value,cluster):
    if request.method == "POST":
        input_data = json.loads(request.body)
        date = input_data.get('date')
        range_value = int(input_data.get('range_value'))
        cluster = input_data.get('cluster')

        result = {
            'xArray': list(range(1, 11)),  # 从1到10的数组
            'y1Array': list(range(10, 21)),  # 从10到20的数组
            'y2Array': list(range(20, 31)),
            'y3Array': list(range(30, 41))
        }


        print(result)
        return JsonResponse(result)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)