# type: ignore
from karrio.server.settings.base import *


INSTALLED_APPS += ["import_export"]

IMPORT_EXPORT_USE_TRANSACTIONS = True
IMPORT_EXPORT_SKIP_ADMIN_LOG = True
IMPORT_EXPORT_CHUNK_SIZE = 200
IMPORT_EXPORT_TMP_STORAGE_CLASS = "import_export.tmp_storages.TempFolderStorage"

SPECTACULAR_SETTINGS["ENUM_NAME_OVERRIDES"] = {
    **SPECTACULAR_SETTINGS["ENUM_NAME_OVERRIDES"],
    "BatchOperationStatus": "karrio.server.data.serializers.OPERATION_STATUS",
}
