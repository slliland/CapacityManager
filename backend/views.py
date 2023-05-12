from django.http import HttpResponse


def convert_to_uppercase(request):
    if request.method == 'POST':
        input_string = request.POST.get('inputString', '')
        output_string = input_string.upper()
        return HttpResponse({'outputString': output_string})
    else:
        return HttpResponse({'error': 'Invalid request method'})
