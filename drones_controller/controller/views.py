from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging


class DroneViewSet(APIView):
    def get(self, request, serial_number=None):
        query_type = request.query_params.get("type")
        if serial_number:
            # first check if drone exists
            try:
                drone = Drone.objects.get(serial_number=serial_number)
            except:
                return Response({"status": "error"}, status=status.HTTP_404_NOT_FOUND)

            if query_type == "battery_capacity":
                serializer = DroneSerializer(drone, fields=('battery_capacity',))
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

            elif query_type == "medications":
                medications = Medication.objects.filter(drone=drone)
                serializer = MedicationSerializer(medications, many=True)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

            else:
                serializer = DroneSerializer(drone)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        if query_type == "available_drones":  # todo
            min_battery = 25
            drone = Drone.objects.filter(battery_capacity__gte=min_battery)
            serializer = DroneSerializer(drone, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        drone = Drone.objects.all()
        serializer = DroneSerializer(drone, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, serial_number=None):
        try:
            item = Drone.objects.get(serial_number=serial_number)
        except:
            return Response({"status": "error"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DroneSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def post(self, request):
        serializer = DroneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MedicationViewSet(APIView):
    @staticmethod
    def check_drone_availability(med_weight, drone_id):
        errors = []
        drone = Drone.objects.get(id=drone_id)
        weight_limit = drone.weight_limit
        battery_capacity = drone.battery_capacity
        current_medications = Medication.objects.filter(drone=drone)
        current_weight = 0
        for med in current_medications:
            current_weight += med.weight
        weight_flag = True
        battery_flag = True
        if not current_weight + med_weight <= weight_limit:
            weight_flag = False
            errors.append("overload weight")

        if not battery_capacity >= 25:
            battery_flag = False
            errors.append("weak battery")
        status = True if (weight_flag and battery_flag) else False

        return status, errors

    def get(self, request):
        medications = Medication.objects.all()
        serializer = MedicationSerializer(medications, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MedicationSerializer(data=request.data)
        if serializer.is_valid():
            drone_id = serializer.validated_data["drone"].id
            med_weight = serializer.validated_data["weight"]
            drone_status, errors = self.check_drone_availability(med_weight, drone_id)
            if drone_status:
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "data": f"selected drone can't be loaded with more medications because : {errors}"
                },
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
