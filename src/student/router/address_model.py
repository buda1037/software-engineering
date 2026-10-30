"""Pydantic-Modell für die Adresse eines Studenten."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from student.entity import Address

__all__ = ["AddressModel"]


class AddressModel(BaseModel):
    """Pydantic-Modell für die Adresse eines Studenten."""

    street: Annotated[str, Field(min_length=1)]
    house_number: Annotated[str, Field(min_length=1)]
    postal_code: Annotated[str, Field(pattern=r"^\d{5}$")]
    city: Annotated[str, Field(min_length=1)]

    model_config = ConfigDict(extra="forbid", frozen=True)

    def to_address(self) -> Address:
        """Konvertierung in ein Entity-Objekt für SQLAlchemy.

        :return: Address-Objekt für SQLAlchemy
        :rtype: Address
        """
        return Address(
            street=self.street,
            house_number=self.house_number,
            postal_code=self.postal_code,
            city=self.city,
        )
