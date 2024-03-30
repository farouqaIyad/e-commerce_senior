def extract_from_serializer(serializer):
    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')
    first_name = serializer.validated_data.get('first_name')
    last_name = serializer.validated_data.get('last_name')
    return  email,password,first_name,last_name