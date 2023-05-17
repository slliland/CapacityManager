from django.http import HttpResponse
import json

def convert_to_uppercase(request):
    if request.method == 'POST':
        input_string = request.POST.get('inputString', '')
        output_string = input_string.upper()
        return HttpResponse({'outputString': output_string})
    else:
        return HttpResponse({'error': 'Invalid request method'})

def getnewoption(request):
    if request.method == "POST":
        r_list = json.loads(request.body)  # 前端向后端发送的参数
        # 对r_list进行操作，结果存入arr。以dict数据类型{'id': '', 'file': ''}格式存储，方便后续取用；
        arr = [{'id': '1', 'file': '111'},{'id': '2', 'file': '4444'}]  # 后端返回前端的参数
        return HttpResponse(json.dumps(arr, ensure_ascii=False), content_type='application/json', charset='utf-8')
    else:
        return HttpResponse({'error': 'Invalid request method'})
