"""DTO-Klasse für die Adresse, insbesondere ohne Decorators für SQLAlchemy."""

from dataclasses import dataclass

import strawberry

from student.service.exceptions import AddressRequiredError
lazy from student.entity import Address


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type(name="Address")
class AddressDTO:
    """DTO-Klasse für die Adresse, insbesondere ohne Decorators für SQLAlchemy."""

    street: str
    house_number: str
    postal_code: str
    city: str

    @classmethod
    def from_address(cls, adresse: Address | None) -> AddressDTO:
        """Initialisierung von AddressDTO durch ein Entity-Objekt von Address.

        :param adresse: Address-Objekt mit Decorators für SQLAlchemy
        :return: AddressDTO-Objekt mit Daten aus dem Address-Objekt
        :rtype: AddressDTO
        :raises AddressRequiredError: falls adresse None ist
        """
        if adresse is None:
            raise AddressRequiredError

        return cls(
            street=adresse.street,
            house_number=adresse.house_number,
            postal_code=adresse.postal_code,
            city=adresse.city,
        )
