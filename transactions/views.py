from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Transaction
from .serializers import TransactionSerializer


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
    
    if month_filter == 'Current':
        current_month = datetime.now().month
        transactions = transactions.filter(date__month=current_month)
    

    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)
