from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Car
from .serializers import CarSerializer
from permissions import IsSafeOrAdmin


class CarListView(ListAPIView):
    queryset = Car.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        status_code = status.HTTP_200_OK
        response = {
            'success': 'true',
            'status code': status_code,
            'message': 'Car fetched successfully',
            'data': [car.to_dict() for car in self.get_queryset()]
        }
        return Response(response, status=status_code)


class CarView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSafeOrAdmin,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = CarSerializer
    queryset = Car.objects.all()

    def get(self, request, pk):
        try:
            car = self.queryset.get(pk=pk)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'Car fetched successfully',
                'data': car.to_dict()
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_code,
                'message': 'Car does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)

    def put(self, request, pk):
        try:
            car = self.queryset.get(pk=pk)
            car_serializer = self.serializer_class(instance=car, data=request.data, partial=True)
            if car_serializer.is_valid(raise_exception=True):
                car_serializer.save()
                status_code = status.HTTP_200_OK
                response = {
                    'success': 'True',
                    'status code': status_code,
                    'message': 'Car updated successfully',
                    'car': car_serializer.data
                }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_code,
                'message': 'Car does not exists',
                'error': str(e)
            }

        return Response(response, status=status_code)

    def delete(self, request, pk):
        try:
            car = self.queryset.get(pk=pk)
            car.delete()
            status_code = status.HTTP_204_NO_CONTENT
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'Car deleted successfully',
                'car': {}
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_code,
                'message': 'Car does not exists',
                'error': str(e)
            }

        return Response(response, status=status_code)
