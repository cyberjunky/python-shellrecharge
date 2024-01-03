from typing import Literal, Optional

import pydantic
from pydantic import BaseModel, confloat, constr

DateTimeISO8601 = str
Status = Literal["Available", "Unavailable", "Occupied", "Unknown"]
ConnectorTypes = Literal[
    "Avcon",
    "Domestic",
    "Industrial2PDc",
    "IndustrialPneAc",
    "Industrial3PEAc",
    "Industrial3PENAc",
    "Type1",
    "Type1Combo",
    "Type2",
    "Type2Combo",
    "Type3",
    "LPI",
    "Nema520",
    "SAEJ1772",
    "SPI",
    "TepcoCHAdeMO",
    "Tesla",
    "Unspecified",
]
UpdatedBy = Literal["Feed", "Admin", "TariffService", "Default"]

# AuthMethods = Literal["NewMotionApp", "RFIDToken", "PnC"]

if pydantic.version.VERSION.startswith("1"):
    EvseId = constr(
        regex=r"^(([A-Z]{2}\*?[A-Z0-9]{3}\*?E[A-Z0-9\*]{1,30})|(\+?[0-9]{1,3}\*[0-9]{3}\*[0-9\*]{1,32}))$"
    )
else:
    EvseId = constr(
        pattern=r"^(([A-Z]{2}\*?[A-Z0-9]{3}\*?E[A-Z0-9\*]{1,30})|(\+?[0-9]{1,3}\*[0-9]{3}\*[0-9\*]{1,32}))$"
    )


class ElectricalProperties(BaseModel):
    powerType: str
    voltage: int
    amperage: float
    maxElectricPower: float


class Tariff(BaseModel):
    perKWh: float
    currency: str
    updated: DateTimeISO8601
    updatedBy: UpdatedBy
    structure: str


class Connector(BaseModel):
    uid: int
    externalId: str
    connectorType: ConnectorTypes
    electricalProperties: ElectricalProperties
    fixedCable: bool
    tariff: Tariff
    updated: DateTimeISO8601
    updatedBy: UpdatedBy
    externalTariffId: Optional[str] = ""


class Evse(BaseModel):
    uid: int
    externalId: str
    evseId: EvseId
    status: Status
    connectors: list[Connector]
    authorizationMethods: list[str]
    physicalReference: str
    updated: DateTimeISO8601


class Coordinates(BaseModel):
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)


class Address(BaseModel):
    streetAndNumber: str
    postalCode: str
    city: str
    country: str


class Accessibility(BaseModel):
    status: str
    remark: Optional[str] = ""
    statusV2: str


class AccessibilityV2(BaseModel):
    status: str


class OpeningHours(BaseModel):
    weekDay: str
    startTime: str
    endTime: str


class PredictedOccupancies(BaseModel):
    weekDay: str
    occupancy: int
    startTime: str
    endTime: str


class Location(BaseModel):
    uid: int
    externalId: int | str
    coordinates: Coordinates
    operatorName: str
    operatorId: Optional[str] = ""
    address: Address
    accessibility: Accessibility
    accessibilityV2: AccessibilityV2
    evses: list[Evse]
    openTwentyFourSeven: bool
    openingHours: list[OpeningHours]
    updated: DateTimeISO8601
    locationType: str
    supportPhoneNumber: str
    facilities: Optional[list[str]] = []
    predictedOccupancies: list[PredictedOccupancies]
    vat: float
    suboperatorName: Optional[str] = ""
    countryCode: str
    partyId: str
    roamingSource: str
