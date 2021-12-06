from rest_framework import serializers

from .models import Drone, Medication


class DroneSerializer(serializers.ModelSerializer):
    # serial_number = serializers.PrimaryKeyRelatedField(queryset=Drone.objects.all())
    # serial_number_id  = serializers.IntegerField(write_only=True)
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DroneSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            print(existing)
            print(allowed)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
            print(self.fields)
    class Meta:
        model = Drone
        fields = '__all__'



class MedicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medication
        fields = '__all__'
