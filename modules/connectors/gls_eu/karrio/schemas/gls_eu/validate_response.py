from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class IssueType:
    Rule: Optional[str] = None
    Location: Optional[str] = None


@s(auto_attribs=True)
class ValidationResultType:
    Issues: List[IssueType] = JList[IssueType]


@s(auto_attribs=True)
class ValidateResponseType:
    success: Optional[bool] = None
    validationResult: Optional[ValidationResultType] = JStruct[ValidationResultType]
