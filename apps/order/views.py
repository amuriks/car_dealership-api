from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from car_dealership.permissions import IsOwnerOrAdmin
from .models import Order
from .serializers import OrderSerializer


class OrderView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)
    authentication_classes = JSONWebTokenAuthentication
    serializer_class = OrderSerializer

    def get(self, request, pk):
        try:
            order = self.queryset.get(pk=pk)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'Order fetched successfully',
                'data': order.to_dict()
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_code,
                'message': 'Order does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)

    def patch(self, request, pk):
        try:
            order = self.queryset.get(pk=pk)
            order_serializer = self.serializer_class(instance=order, data=request.data, partial=True)
            if order_serializer.is_valid(raise_exception=True):
                order_serializer.save()
                status_code = status.HTTP_200_OK
                response = {
                    'success': 'True',
                    'status code': status_code,
                    'message': 'order updated successfully',
                    'data': order_serializer.data
                }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_code,
                'message': 'Order does not exists',
                'error': str(e)
            }

        return Response(response, status=status_code)

    def delete(self, request, pk):
        try:
            order = self.queryset.get(pk=pk)
            order.delete()
            status_code = status.HTTP_204_NO_CONTENT
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'Order deleted successfully',
                'data': {}
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_code,
                'message': 'Order does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)


class OrderCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = JSONWebTokenAuthentication
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Order successfully saved',
            'data': serializer.data
        }
        return Response(response, status=status_code)


class OrderGetAllView(ListAPIView):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = JSONWebTokenAuthentication

    def get(self, request):
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Order successfully saved',
            'data': [order.to_dict() for order in self.queryset.all()]
        }
        return Response(response, status=status_code)
