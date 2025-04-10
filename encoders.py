import math
from typing import Optional
from pydantic import BaseModel
from pydantic_core.core_schema import (
    SerializationInfo,
    SerializeAsAny,
    plain_serializer,
    no_info_plain_validator_function,
    CoreSchema,
)

class CustomFloat(float):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        # Use the custom schema with validation and our own serialization
        return SerializeAsAny(cls._get_schema())

    @classmethod
    def _get_schema(cls) -> CoreSchema:
        # Build schema based on the no-info plain validator and add our custom serializer.
        base_schema = no_info_plain_validator_function(cls._validate).__schema__
        return base_schema.copy(
            serialization=plain_serializer(cls._serialize, return_type=float)
        )

    @classmethod
    def _validate(cls, value):
        try:
            # Convert the input to float and then to CustomFloat
            return cls(float(value))
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Value {value!r} is not a valid float") from exc

    @classmethod
    def _serialize(cls, value: float, _info: SerializationInfo) -> float:
        # If the value is not finite (NaN, inf), return it as-is.
        if not math.isfinite(value):
            return value
        # Multiply by 100, truncate, then divide by 100 to achieve truncation to 2 decimals.
        multiplier = 100.0
        return math.trunc(value * multiplier) / multiplier

    def __repr__(self):
        # Always display two decimal places.
        return f"{float(self):.2f}"

    def __str__(self):
        # Same for the string conversion.
        return f"{float(self):.2f}"


# Example usage in a Pydantic model:
class MyModel(BaseModel):
    value: Optional[CustomFloat] = None

# Example tests:
if __name__ == '__main__':
    # Test truncation and display
    m = MyModel(value=2.345)
    print(m.value)  # Output: 2.34
    m = MyModel(value=-2.345)
    print(m.value)  # Output: -2.34
    m = MyModel(value=1.0)
    print(m.value)  # Output: 1.00
