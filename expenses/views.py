from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ExpensesSerializer
from .models import Expense
from rest_framework import permissions
from .permissions import IsOwner

# Create your views here.
#Expense Views



class ExpenseListAPIView(ListCreateAPIView):
    serializer_class = ExpensesSerializer
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated,)  #with this only authenticated users can access this

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpensesSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    #additional config is needed outside of IsAuthenticate
    #so that only the user who created the expense can temper with it
    #create permission.py
    queryset = Expense.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
