from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import MonthlyBudget, Transaction
from .serializers import MonthlyBudgetSerializer, TransactionSerializer

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def createTransaction(request):
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'message': 'Transaction created successfully!', 'id': serializer.data['id']}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def updateTransaction(request, id):
    try:
        transaction = Transaction.objects.get(pk=id, user=request.user)
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TransactionSerializer(transaction, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Transaction updated successfully.'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def deleteTransaction(request, id):
    try:
        transaction = Transaction.objects.get(pk=id, user=request.user)
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

    transaction.delete()
    return Response({'message': 'Transaction deleted successfully.'})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getTransaction(request, id):
    try:
        transaction = Transaction.objects.get(pk=id, user=request.user)
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TransactionSerializer(transaction)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def transactionList(request):
    type_filter = request.GET.get('type','All')
    category_filter = request.GET.get('category','All')
    month_filter = request.GET.get('month', 'All')

    transactions = Transaction.objects.filter(user=request.user)

    if type_filter != "All":
        transactions = transactions.filter(type=type_filter)

    if category_filter != "All":
        transactions = transactions.filter(category=category_filter)

    if month_filter != "All":
        try:
            # Expecting month_filter like '2024-04'
            parsed_date = datetime.strptime(month_filter, "%Y-%m")
            transactions = transactions.filter(
                date__year=parsed_date.year,
                date__month=parsed_date.month
            )
        except ValueError:
            pass  # Invalid format, ignore filtering

    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

# views.py (continued)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getBudget(request):
    # Get the month from query parameters or use the current month as a default
    month = request.query_params.get('month', datetime.now().strftime('%Y-%m'))

    try:
        budget = MonthlyBudget.objects.get(user=request.user, month=month)
    except MonthlyBudget.DoesNotExist:
        return Response({'message': f'No budget found for the month {month}.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MonthlyBudgetSerializer(budget)
    return Response(serializer.data)


@api_view(['POST', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def createOrUpdateBudget(request):
    data = request.data.copy()
    print(f"Received data: {data}")

    # Ensure the month ends with '-01' if only 'YYYY-MM' was sent (fallback)
    if len(data.get('month', '')) == 7:
        data['month'] += '-01'

    serializer = MonthlyBudgetSerializer(data=data)
    if serializer.is_valid():
        budget, created = MonthlyBudget.objects.update_or_create(
            user=request.user,
            month=data['month'],
            defaults={'amount': serializer.validated_data['amount']}
        )
        return Response({
            'message': 'Budget created.' if created else 'Budget updated.',
            'budget': MonthlyBudgetSerializer(budget).data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def budgetList(request):
    budgets = MonthlyBudget.objects.filter(user=request.user).order_by('month').values_list('month', flat=True)
    available_months = sorted(set(budget.strftime('%Y-%m') for budget in budgets))
    return Response(available_months)
