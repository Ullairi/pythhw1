from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError


#--Address Model--
class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)

#-- User Model-
class User(BaseModel):
    name: str = Field(...,min_length=2, pattern=r'^[a-zA-Z\s]+$')
    age: int = Field(...,ge=0,le=100)
    email: EmailStr
    is_employed: bool
    address: Address

#--Validation--
    @field_validator('age')
    def validate_age(cls, v, info):
        is_employed = info.data.get('is_employed')
        if is_employed and not (18 <= v <= 65):
            raise ValueError("Age must be between 18 and 65")
        return v

#--JSON process--
def json_process(json_str: str) -> str:
    try:
        user = User.model_validate_json(json_str)
        if user.is_employed and not (18 <= user.age <= 65):
            raise ValueError("Age must be between 18 and 65")
        return user.model_dump_json(indent=2)
    except (ValidationError, ValueError)as e:
        return(f"Validation error:\n{e}")


#--JSON files--
json_input_invalid_age = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

json_input_valid = """{
    "name": "John Doh",
    "age": 30,
    "email": "john.doh@example.com",
    "is_employed": true,
    "address": {
        "city": "California",
        "street": "7th Kolkata",
        "house_number": 54
    }
}"""

json_input_invalid_address = """{
    "name": "Kate Lou",
    "age": 20,
    "email": "kate.lou@example.com",
    "is_employed": true,
    "address": {
        "city": "",
        "street": "street",
        "house_number": -13
    }
}"""

json_input_not_employed = """{
    "name": "Matt Lop",
    "age": 45,
    "email": "matt.lop@example.com",
    "is_employed": false,
    "address": {
        "city": "San Francisco",
        "street": "7th Avenue",
        "house_number": 21
    }
}"""
print(json_process(json_input_invalid_age))
print(json_process(json_input_valid))
print(json_process(json_input_invalid_address))
print(json_process(json_input_not_employed))