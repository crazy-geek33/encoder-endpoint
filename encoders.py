from pydantic import BaseModel, field_validator, ConfigDict
from pydantic.class_validators import field_serializer
from typing import Optional
import math


class CustomFloat(float):
    @field_validator
    @classmethod
    def validate_float(cls, value: float) -> float:
        # Ensure the value is a valid float and handle any type issues
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValueError(f'Value {value!r} is not a valid float')

    @field_serializer
    @classmethod
    def serialize_float(cls, value: float) -> float:
        # Truncate to exactly 2 decimal places
        if not math.isfinite(value):
            return value  # Keep NaN or infinities unchanged
        return math.trunc(value * 100) / 100.0

    def __repr__(self):
        # Always display two decimal places
        return f"{float(self):.2f}"

    def __str__(self):
        # Same for string representation
        return f"{float(self):.2f}"


# Pydantic model using CustomFloat
class MyModel(BaseModel):
    value: Optional[CustomFloat] = None

    model_config = ConfigDict(
        json_encoders={
            CustomFloat: lambda v: f"{v:.2f}"  # Enforce 2 decimal places in JSON
        }
    )


# Example usage
if __name__ == '__main__':
    m1 = MyModel(value=2.345)
    print(m1.value)  # Output: 2.34
    m2 = MyModel(value=-2.345)
    print(m2.value)  # Output: -2.34
    m3 = MyModel(value=1.0)
    print(m3.value)  # Output: 1.00
    print(m3.json())  # {"value": "1.00"} - JSON will have 2 decimal places
