"""Models for pydantic parsing."""

from typing import Literal, Optional

from pydantic import UUID4, BaseModel, Field

DateTimeISO8601 = str
ChargePointStatus = Literal["Available", "Unavailable", "Occupied", "Unknown"]
ChargePointDetailedStatus = Literal["available", "preparing", "charging", "suspendedev"]
Vendor = Literal["NewMotion"]


class ChargeToken(BaseModel):
    """Charge card."""

    uuid: Optional[str] = None
    rfid: str
    printedNumber: str
    name: Optional[str] = None


class OccupyingToken(ChargeToken):
    """Charge card occupying a charger"""

    timestamp: DateTimeISO8601


class Evse(BaseModel):
    """Basic EVSE representation for charge points."""

    evseId: str
    number: int
    occupyingToken: OccupyingToken
    status: ChargePointStatus


class ChargePoint(BaseModel):
    """Charge point."""

    evses: list[Evse]
    name: str
    serial: str
    uuid: UUID4


class Assets(BaseModel):
    chargePoints: list[ChargePoint]
    chargeTokens: list[ChargeToken]


class Address(BaseModel):
    """Address."""

    city: str
    country: str
    number: str
    street: str
    zip: str


class Coordinates(BaseModel):
    """Location."""

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class PlugAndCharge(BaseModel):
    """Plug & charge support."""

    capable: Literal[True, False]


class LatestOnlineStatus(BaseModel):
    """Last time the charger was online."""

    lastChanged: DateTimeISO8601
    online: Literal[True, False]


class Href(BaseModel):
    """API path."""

    href: str


class Links(BaseModel):
    """Self-describing links."""

    self: Href
    evses: Optional[Href] = None


class Connector(BaseModel):
    """Specs of the charger."""

    connectorType: str
    electricCurrentType: Literal["AC", "DC"]
    maxCurrentInAmps: int
    maxPowerInWatts: int = Field(ge=1000)
    number: int
    numberOfPhases: Literal[1, 3]


class DetailedEvse(BaseModel):
    """Evse instance."""

    _links: Href
    connectors: list[Connector]
    currentType: Literal["ac", "dc"]
    evseId: str
    id: UUID4
    maxPower: str
    number: str
    status: ChargePointDetailedStatus
    statusDetails: OccupyingToken


class Embedded(BaseModel):
    """Embedded charger details."""

    evses: list[DetailedEvse]


class DetailedChargePoint(BaseModel):
    """Charge point details."""

    _embedded: Embedded
    _links: Links
    address: Address
    connectivity: Literal["online", "offline"]
    coordinates: Coordinates
    firstConnection: DateTimeISO8601
    id: UUID4
    lastConnection: DateTimeISO8601
    lastSession: DateTimeISO8601
    latestOnlineStatus: LatestOnlineStatus
    model: str
    name: str
    plugAndCharge: PlugAndCharge
    protocol: Literal["ocpp 1.6-j"]
    serial: str
    sharing: Literal["private", "public"]
    vendor: Vendor
