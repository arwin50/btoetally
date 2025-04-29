from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import TransactionForm
import json
from .models import Transaction

@csrf_exempt
def createTransaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

        allowed_fields = ['type', 'category', 'subject', 'amount', 'date', 'notes']
        filtered_data = {key: value for key, value in data.items() if key in allowed_fields}

        form = TransactionForm(filtered_data)

        if form.is_valid():
            transaction = form.save(commit=False)

            transaction.user_id = data.get('user')
            transaction.save()

            return JsonResponse({
                'message': 'Transaction created successfully!',
                'id': transaction.id
            }, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def updateTransaction(request, id):
    if request.method == 'PUT':
        try:
            transaction = Transaction.objects.get(pk=id)
        except Transaction.DoesNotExist:
            return JsonResponse({'error': 'Transaction not found.'}, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

        allowed_fields = ['type', 'category', 'subject', 'amount', 'date', 'notes']
        
        initial_data = {
            'type': transaction.type,
            'category': transaction.category,
            'subject': transaction.subject,
            'amount': transaction.amount,
            'date': transaction.date,
            'notes': transaction.notes,
        }
        
        initial_data.update({key: value for key, value in data.items() if key in allowed_fields})

        form = TransactionForm(initial_data, instance=transaction)

        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Transaction updated successfully.'}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'PUT request required.'}, status=405)

@csrf_exempt
def deleteTransaction(request, id):
    if request.method == 'DELETE':
        try:
            transaction = Transaction.objects.get(pk=id)
        except Transaction.DoesNotExist:
            return JsonResponse({'error': 'Transaction not found.'}, status=404)

        transaction.delete()

        return JsonResponse({'message': 'Transaction deleted successfully.'}, status=200)

    return JsonResponse({'error': 'DELETE request required.'}, status=405)

@csrf_exempt
def getTransaction(request, id):
    if request.method == 'GET':
        try:
            transaction = Transaction.objects.get(pk=id)
        except Transaction.DoesNotExist:
            return JsonResponse({'error': 'Transaction not found.'}, status=404)

        transaction_data = {
            'id': transaction.id,
            'user': transaction.user.id,
            'type': transaction.type,
            'subject': transaction.subject,
            'amount': str(transaction.amount),
            'date': transaction.date.strftime('%Y-%m-%d'),
            'category': transaction.category,
            'notes': transaction.notes,
            'created_at': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return JsonResponse(transaction_data, status=200)

    return JsonResponse({'error': 'GET request required'}, status=405)


@csrf_exempt
def transactionList(request):
    if request.method == 'GET':
        type_filter = request.GET.get('type')
        category_filter = request.GET.get('category')

        transactions = Transaction.objects.all()

        if type_filter and type_filter != "All":
            transactions = transactions.filter(type=type_filter)

        if category_filter and category_filter != "All":
            transactions = transactions.filter(category=category_filter)

        transactions_list = list(transactions.values(
            'id', 'user', 'type', 'subject', 'amount', 'date', 'category', 'notes', 'created_at'
        ))

        return JsonResponse(transactions_list, safe=False, status=200)

    return JsonResponse({'error': 'GET request required'}, status=405)

