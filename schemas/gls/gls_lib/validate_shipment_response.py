from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class Issue:
    Rule: Optional[str] = None
    Location: Optional[str] = None


@s(auto_attribs=True)
class ValidationResult:
    Issues: List[Issue] = JList[Issue]


@s(auto_attribs=True)
class ValidateShipmentResponse:
    success: Optional[bool] = None
    validationResult: Optional[ValidationResult] = JStruct[ValidationResult]
