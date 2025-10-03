import karrio.lib as lib


class AutomationAuthType(lib.StrEnum):
    basic = "basic"
    oauth2 = "oauth2"
    api_key = "api_key"
    jwt = "jwt"


class AutomationActionType(lib.StrEnum):
    http_request = "http_request"
    data_mapping = "data_mapping"
    function_call = "function_call"
    conditional = "conditional"


class AutomationHTTPMethod(lib.StrEnum):
    get = "get"
    post = "post"
    put = "put"
    patch = "patch"
    delete = "delete"


class AutomationParametersType(lib.StrEnum):
    data = "data"
    querystring = "querystring"


class AutomationHTTPContentType(lib.StrEnum):
    json = "json"
    form = "form"
    text = "text"
    xml = "xml"


class AutomationEventType(lib.StrEnum):
    manual = "manual"
    scheduled = "scheduled"
    webhook = "webhook"
    auto = "auto"


class AutomationEventStatus(lib.StrEnum):
    pending = "pending"
    running = "running"
    success = "success"
    aborted = "aborted"
    failed = "failed"
    cancelled = "cancelled"


class AutomationTriggerType(lib.StrEnum):
    manual = "manual"
    scheduled = "scheduled"
    webhook = "webhook"


AUTH_TYPE = [(c.name, c.name) for c in list(AutomationAuthType)]
ACTION_TYPE = [(c.name, c.name) for c in list(AutomationActionType)]
HTTP_METHOD = [(c.name, c.name) for c in list(AutomationHTTPMethod)]
WORKFLOW_EVENT_TYPE = [(c.name, c.name) for c in list(AutomationEventType)]
PARAMETERS_TYPE = [(c.name, c.name) for c in list(AutomationParametersType)]
HTTP_CONTENT_TYPE = [(c.name, c.name) for c in list(AutomationHTTPContentType)]
WORKFLOW_TRIGGER_TYPE = [(c.name, c.name) for c in list(AutomationTriggerType)]
WORKFLOW_EVENT_STATUS = [(c.name, c.name) for c in list(AutomationEventStatus)]


class RateComparisonField(lib.StrEnum):
    total_charge = "total_charge"
    transit_days = "transit_days"
    estimated_delivery = "estimated_delivery"
    insurance_charge = "insurance_charge"
    fuel_surcharge = "fuel_surcharge"
    duty_charge = "duty_charge"
    tax_charge = "tax_charge"


class ComparisonOperator(lib.StrEnum):
    eq = "eq"
    gt = "gt"
    gte = "gte"
    lt = "lt"
    lte = "lte"


class SelectServiceStrategy(lib.StrEnum):
    cheapest = "cheapest"
    fastest = "fastest"
    preferred = "preferred"
