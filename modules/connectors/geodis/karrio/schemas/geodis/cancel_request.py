from attr import s
from typing import List


@s(auto_attribs=True)
class CancelRequestType:
    listNosRecepisses: List[str] = []
    listNosSuivis: List[str] = []
    listReferences: List[str] = []
