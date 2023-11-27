var Karrio = (function () {
    'use strict';

    /******************************************************************************
    Copyright (c) Microsoft Corporation.

    Permission to use, copy, modify, and/or distribute this software for any
    purpose with or without fee is hereby granted.

    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
    REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
    AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
    INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
    LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
    OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
    PERFORMANCE OF THIS SOFTWARE.
    ***************************************************************************** */
    /* global Reflect, Promise, SuppressedError, Symbol */

    var extendStatics = function(d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };

    function __extends(d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    }

    var __assign = function() {
        __assign = Object.assign || function __assign(t) {
            for (var s, i = 1, n = arguments.length; i < n; i++) {
                s = arguments[i];
                for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
            }
            return t;
        };
        return __assign.apply(this, arguments);
    };

    function __awaiter(thisArg, _arguments, P, generator) {
        function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
        return new (P || (P = Promise))(function (resolve, reject) {
            function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
            function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
            function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }

    function __generator(thisArg, body) {
        var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
        return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
        function verb(n) { return function (v) { return step([n, v]); }; }
        function step(op) {
            if (f) throw new TypeError("Generator is already executing.");
            while (g && (g = 0, op[0] && (_ = 0)), _) try {
                if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
                if (y = 0, t) op = [op[0] & 2, t.value];
                switch (op[0]) {
                    case 0: case 1: t = op; break;
                    case 4: _.label++; return { value: op[1], done: false };
                    case 5: _.label++; y = op[1]; op = [0]; continue;
                    case 7: op = _.ops.pop(); _.trys.pop(); continue;
                    default:
                        if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                        if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                        if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                        if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                        if (t[2]) _.ops.pop();
                        _.trys.pop(); continue;
                }
                op = body.call(thisArg, _);
            } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
            if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
        }
    }

    typeof SuppressedError === "function" ? SuppressedError : function (error, suppressed, message) {
        var e = new Error(message);
        return e.name = "SuppressedError", e.error = error, e.suppressed = suppressed, e;
    };

    /* tslint:disable */
    var BASE_PATH = "http://localhost".replace(/\/+$/, "");
    var Configuration = /** @class */ (function () {
        function Configuration(configuration) {
            if (configuration === void 0) { configuration = {}; }
            this.configuration = configuration;
        }
        Object.defineProperty(Configuration.prototype, "config", {
            set: function (configuration) {
                this.configuration = configuration;
            },
            enumerable: false,
            configurable: true
        });
        Object.defineProperty(Configuration.prototype, "basePath", {
            get: function () {
                return this.configuration.basePath != null ? this.configuration.basePath : BASE_PATH;
            },
            enumerable: false,
            configurable: true
        });
        Object.defineProperty(Configuration.prototype, "fetchApi", {
            get: function () {
                return this.configuration.fetchApi;
            },
            enumerable: false,
            configurable: true
        });
        Object.defineProperty(Configuration.prototype, "middleware", {
            get: function () {
                return this.configuration.middleware || [];
            },
            enumerable: false,
            configurable: true
        });
        Object.defineProperty(Configuration.prototype, "queryParamsStringify", {
            get: function () {
                return this.configuration.queryParamsStringify || querystring;
            },
            enumerable: false,
            configurable: true
        });
        Object.defineProperty(Configuration.prototype, "username", {
            get: function () {
                return this.configuration.username;
            },
            enumerable: false,
            configurable: true
        });
        Object.defineProperty(Configuration.prototype, "password", {
            get: function () {
                return this.configuration.password;
            },
            enumerable: false,
            configurable: true
        });
        Object.defineProperty(Configuration.prototype, "apiKey", {
            get: function () {
                var apiKey = this.configuration.apiKey;
                if (apiKey) {
                    return typeof apiKey === 'function' ? apiKey : function () { return apiKey; };
                }
                return undefined;
            },
            enumerable: false,
            configurable: true
        });
        Object.defineProperty(Configuration.prototype, "accessToken", {
            get: function () {
                var _this = this;
                var accessToken = this.configuration.accessToken;
                if (accessToken) {
                    return typeof accessToken === 'function' ? accessToken : function () { return __awaiter(_this, void 0, void 0, function () { return __generator(this, function (_a) {
                        return [2 /*return*/, accessToken];
                    }); }); };
                }
                return undefined;
            },
            enumerable: false,
            configurable: true
        });
        Object.defineProperty(Configuration.prototype, "headers", {
            get: function () {
                return this.configuration.headers;
            },
            enumerable: false,
            configurable: true
        });
        Object.defineProperty(Configuration.prototype, "credentials", {
            get: function () {
                return this.configuration.credentials;
            },
            enumerable: false,
            configurable: true
        });
        return Configuration;
    }());
    var DefaultConfig = new Configuration();
    /**
     * This is the base class for all generated API classes.
     */
    var BaseAPI = /** @class */ (function () {
        function BaseAPI(configuration) {
            if (configuration === void 0) { configuration = DefaultConfig; }
            var _this = this;
            this.configuration = configuration;
            this.fetchApi = function (url, init) { return __awaiter(_this, void 0, void 0, function () {
                var fetchParams, _i, _a, middleware, response, e_1, _b, _c, middleware, _d, _e, middleware;
                return __generator(this, function (_f) {
                    switch (_f.label) {
                        case 0:
                            fetchParams = { url: url, init: init };
                            _i = 0, _a = this.middleware;
                            _f.label = 1;
                        case 1:
                            if (!(_i < _a.length)) return [3 /*break*/, 4];
                            middleware = _a[_i];
                            if (!middleware.pre) return [3 /*break*/, 3];
                            return [4 /*yield*/, middleware.pre(__assign({ fetch: this.fetchApi }, fetchParams))];
                        case 2:
                            fetchParams = (_f.sent()) || fetchParams;
                            _f.label = 3;
                        case 3:
                            _i++;
                            return [3 /*break*/, 1];
                        case 4:
                            response = undefined;
                            _f.label = 5;
                        case 5:
                            _f.trys.push([5, 7, , 12]);
                            return [4 /*yield*/, (this.configuration.fetchApi || fetch)(fetchParams.url, fetchParams.init)];
                        case 6:
                            response = _f.sent();
                            return [3 /*break*/, 12];
                        case 7:
                            e_1 = _f.sent();
                            _b = 0, _c = this.middleware;
                            _f.label = 8;
                        case 8:
                            if (!(_b < _c.length)) return [3 /*break*/, 11];
                            middleware = _c[_b];
                            if (!middleware.onError) return [3 /*break*/, 10];
                            return [4 /*yield*/, middleware.onError({
                                    fetch: this.fetchApi,
                                    url: fetchParams.url,
                                    init: fetchParams.init,
                                    error: e_1,
                                    response: response ? response.clone() : undefined,
                                })];
                        case 9:
                            response = (_f.sent()) || response;
                            _f.label = 10;
                        case 10:
                            _b++;
                            return [3 /*break*/, 8];
                        case 11:
                            if (response === undefined) {
                                if (e_1 instanceof Error) {
                                    throw new FetchError(e_1, 'The request failed and the interceptors did not return an alternative response');
                                }
                                else {
                                    throw e_1;
                                }
                            }
                            return [3 /*break*/, 12];
                        case 12:
                            _d = 0, _e = this.middleware;
                            _f.label = 13;
                        case 13:
                            if (!(_d < _e.length)) return [3 /*break*/, 16];
                            middleware = _e[_d];
                            if (!middleware.post) return [3 /*break*/, 15];
                            return [4 /*yield*/, middleware.post({
                                    fetch: this.fetchApi,
                                    url: fetchParams.url,
                                    init: fetchParams.init,
                                    response: response.clone(),
                                })];
                        case 14:
                            response = (_f.sent()) || response;
                            _f.label = 15;
                        case 15:
                            _d++;
                            return [3 /*break*/, 13];
                        case 16: return [2 /*return*/, response];
                    }
                });
            }); };
            this.middleware = configuration.middleware;
        }
        BaseAPI.prototype.withMiddleware = function () {
            var _a;
            var middlewares = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                middlewares[_i] = arguments[_i];
            }
            var next = this.clone();
            next.middleware = (_a = next.middleware).concat.apply(_a, middlewares);
            return next;
        };
        BaseAPI.prototype.withPreMiddleware = function () {
            var preMiddlewares = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                preMiddlewares[_i] = arguments[_i];
            }
            var middlewares = preMiddlewares.map(function (pre) { return ({ pre: pre }); });
            return this.withMiddleware.apply(this, middlewares);
        };
        BaseAPI.prototype.withPostMiddleware = function () {
            var postMiddlewares = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                postMiddlewares[_i] = arguments[_i];
            }
            var middlewares = postMiddlewares.map(function (post) { return ({ post: post }); });
            return this.withMiddleware.apply(this, middlewares);
        };
        /**
         * Check if the given MIME is a JSON MIME.
         * JSON MIME examples:
         *   application/json
         *   application/json; charset=UTF8
         *   APPLICATION/JSON
         *   application/vnd.company+json
         * @param mime - MIME (Multipurpose Internet Mail Extensions)
         * @return True if the given MIME is JSON, false otherwise.
         */
        BaseAPI.prototype.isJsonMime = function (mime) {
            if (!mime) {
                return false;
            }
            return BaseAPI.jsonRegex.test(mime);
        };
        BaseAPI.prototype.request = function (context, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var _a, url, init, response;
                return __generator(this, function (_b) {
                    switch (_b.label) {
                        case 0: return [4 /*yield*/, this.createFetchParams(context, initOverrides)];
                        case 1:
                            _a = _b.sent(), url = _a.url, init = _a.init;
                            return [4 /*yield*/, this.fetchApi(url, init)];
                        case 2:
                            response = _b.sent();
                            if (response && (response.status >= 200 && response.status < 300)) {
                                return [2 /*return*/, response];
                            }
                            throw new ResponseError(response, 'Response returned an error code');
                    }
                });
            });
        };
        BaseAPI.prototype.createFetchParams = function (context, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var url, headers, initOverrideFn, initParams, overriddenInit, _a, body, init;
                var _this = this;
                return __generator(this, function (_b) {
                    switch (_b.label) {
                        case 0:
                            url = this.configuration.basePath + context.path;
                            if (context.query !== undefined && Object.keys(context.query).length !== 0) {
                                // only add the querystring to the URL if there are query parameters.
                                // this is done to avoid urls ending with a "?" character which buggy webservers
                                // do not handle correctly sometimes.
                                url += '?' + this.configuration.queryParamsStringify(context.query);
                            }
                            headers = Object.assign({}, this.configuration.headers, context.headers);
                            Object.keys(headers).forEach(function (key) { return headers[key] === undefined ? delete headers[key] : {}; });
                            initOverrideFn = typeof initOverrides === "function"
                                ? initOverrides
                                : function () { return __awaiter(_this, void 0, void 0, function () { return __generator(this, function (_a) {
                                    return [2 /*return*/, initOverrides];
                                }); }); };
                            initParams = {
                                method: context.method,
                                headers: headers,
                                body: context.body,
                                credentials: this.configuration.credentials,
                            };
                            _a = [__assign({}, initParams)];
                            return [4 /*yield*/, initOverrideFn({
                                    init: initParams,
                                    context: context,
                                })];
                        case 1:
                            overriddenInit = __assign.apply(void 0, _a.concat([(_b.sent())]));
                            if (isFormData(overriddenInit.body)
                                || (overriddenInit.body instanceof URLSearchParams)
                                || isBlob(overriddenInit.body)) {
                                body = overriddenInit.body;
                            }
                            else if (this.isJsonMime(headers['Content-Type'])) {
                                body = JSON.stringify(overriddenInit.body);
                            }
                            else {
                                body = overriddenInit.body;
                            }
                            init = __assign(__assign({}, overriddenInit), { body: body });
                            return [2 /*return*/, { url: url, init: init }];
                    }
                });
            });
        };
        /**
         * Create a shallow clone of `this` by constructing a new instance
         * and then shallow cloning data members.
         */
        BaseAPI.prototype.clone = function () {
            var constructor = this.constructor;
            var next = new constructor(this.configuration);
            next.middleware = this.middleware.slice();
            return next;
        };
        BaseAPI.jsonRegex = new RegExp('^(:?application\/json|[^;/ \t]+\/[^;/ \t]+[+]json)[ \t]*(:?;.*)?$', 'i');
        return BaseAPI;
    }());
    function isBlob(value) {
        return typeof Blob !== 'undefined' && value instanceof Blob;
    }
    function isFormData(value) {
        return typeof FormData !== "undefined" && value instanceof FormData;
    }
    var ResponseError = /** @class */ (function (_super) {
        __extends(ResponseError, _super);
        function ResponseError(response, msg) {
            var _this = _super.call(this, msg) || this;
            _this.response = response;
            _this.name = "ResponseError";
            return _this;
        }
        return ResponseError;
    }(Error));
    var FetchError = /** @class */ (function (_super) {
        __extends(FetchError, _super);
        function FetchError(cause, msg) {
            var _this = _super.call(this, msg) || this;
            _this.cause = cause;
            _this.name = "FetchError";
            return _this;
        }
        return FetchError;
    }(Error));
    var RequiredError = /** @class */ (function (_super) {
        __extends(RequiredError, _super);
        function RequiredError(field, msg) {
            var _this = _super.call(this, msg) || this;
            _this.field = field;
            _this.name = "RequiredError";
            return _this;
        }
        return RequiredError;
    }(Error));
    function exists(json, key) {
        var value = json[key];
        return value !== null && value !== undefined;
    }
    function querystring(params, prefix) {
        if (prefix === void 0) { prefix = ''; }
        return Object.keys(params)
            .map(function (key) { return querystringSingleKey(key, params[key], prefix); })
            .filter(function (part) { return part.length > 0; })
            .join('&');
    }
    function querystringSingleKey(key, value, keyPrefix) {
        if (keyPrefix === void 0) { keyPrefix = ''; }
        var fullKey = keyPrefix + (keyPrefix.length ? "[".concat(key, "]") : key);
        if (value instanceof Array) {
            var multiValue = value.map(function (singleValue) { return encodeURIComponent(String(singleValue)); })
                .join("&".concat(encodeURIComponent(fullKey), "="));
            return "".concat(encodeURIComponent(fullKey), "=").concat(multiValue);
        }
        if (value instanceof Set) {
            var valueAsArray = Array.from(value);
            return querystringSingleKey(key, valueAsArray, keyPrefix);
        }
        if (value instanceof Date) {
            return "".concat(encodeURIComponent(fullKey), "=").concat(encodeURIComponent(value.toISOString()));
        }
        if (value instanceof Object) {
            return querystring(value, fullKey);
        }
        return "".concat(encodeURIComponent(fullKey), "=").concat(encodeURIComponent(String(value)));
    }
    function canConsumeForm(consumes) {
        for (var _i = 0, consumes_1 = consumes; _i < consumes_1.length; _i++) {
            var consume = consumes_1[_i];
            if ('multipart/form-data' === consume.contentType) {
                return true;
            }
        }
        return false;
    }
    var JSONApiResponse = /** @class */ (function () {
        function JSONApiResponse(raw, transformer) {
            if (transformer === void 0) { transformer = function (jsonValue) { return jsonValue; }; }
            this.raw = raw;
            this.transformer = transformer;
        }
        JSONApiResponse.prototype.value = function () {
            return __awaiter(this, void 0, void 0, function () {
                var _a;
                return __generator(this, function (_b) {
                    switch (_b.label) {
                        case 0:
                            _a = this.transformer;
                            return [4 /*yield*/, this.raw.json()];
                        case 1: return [2 /*return*/, _a.apply(this, [_b.sent()])];
                    }
                });
            });
        };
        return JSONApiResponse;
    }());

    /* tslint:disable */
    function AddressValidationFromJSON(json) {
        return AddressValidationFromJSONTyped(json);
    }
    function AddressValidationFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'success': json['success'],
            'meta': !exists(json, 'meta') ? undefined : json['meta'],
        };
    }
    function AddressValidationToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'success': value.success,
            'meta': value.meta,
        };
    }

    /* tslint:disable */
    function AddressFromJSON(json) {
        return AddressFromJSONTyped(json);
    }
    function AddressFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'postal_code': !exists(json, 'postal_code') ? undefined : json['postal_code'],
            'city': !exists(json, 'city') ? undefined : json['city'],
            'federal_tax_id': !exists(json, 'federal_tax_id') ? undefined : json['federal_tax_id'],
            'state_tax_id': !exists(json, 'state_tax_id') ? undefined : json['state_tax_id'],
            'person_name': !exists(json, 'person_name') ? undefined : json['person_name'],
            'company_name': !exists(json, 'company_name') ? undefined : json['company_name'],
            'country_code': json['country_code'],
            'email': !exists(json, 'email') ? undefined : json['email'],
            'phone_number': !exists(json, 'phone_number') ? undefined : json['phone_number'],
            'state_code': !exists(json, 'state_code') ? undefined : json['state_code'],
            'suburb': !exists(json, 'suburb') ? undefined : json['suburb'],
            'residential': !exists(json, 'residential') ? undefined : json['residential'],
            'street_number': !exists(json, 'street_number') ? undefined : json['street_number'],
            'address_line1': !exists(json, 'address_line1') ? undefined : json['address_line1'],
            'address_line2': !exists(json, 'address_line2') ? undefined : json['address_line2'],
            'validate_location': !exists(json, 'validate_location') ? undefined : json['validate_location'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'validation': !exists(json, 'validation') ? undefined : AddressValidationFromJSON(json['validation']),
        };
    }
    function AddressToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'id': value.id,
            'postal_code': value.postal_code,
            'city': value.city,
            'federal_tax_id': value.federal_tax_id,
            'state_tax_id': value.state_tax_id,
            'person_name': value.person_name,
            'company_name': value.company_name,
            'country_code': value.country_code,
            'email': value.email,
            'phone_number': value.phone_number,
            'state_code': value.state_code,
            'suburb': value.suburb,
            'residential': value.residential,
            'street_number': value.street_number,
            'address_line1': value.address_line1,
            'address_line2': value.address_line2,
            'validate_location': value.validate_location,
            'object_type': value.object_type,
            'validation': AddressValidationToJSON(value.validation),
        };
    }

    /* tslint:disable */
    function AddressDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'postal_code': value.postal_code,
            'city': value.city,
            'federal_tax_id': value.federal_tax_id,
            'state_tax_id': value.state_tax_id,
            'person_name': value.person_name,
            'company_name': value.company_name,
            'country_code': value.country_code,
            'email': value.email,
            'phone_number': value.phone_number,
            'state_code': value.state_code,
            'suburb': value.suburb,
            'residential': value.residential,
            'street_number': value.street_number,
            'address_line1': value.address_line1,
            'address_line2': value.address_line2,
            'validate_location': value.validate_location,
        };
    }

    /* tslint:disable */
    function AddressListFromJSON(json) {
        return AddressListFromJSONTyped(json);
    }
    function AddressListFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'count': !exists(json, 'count') ? undefined : json['count'],
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(AddressFromJSON)),
        };
    }

    /* tslint:disable */
    function BatchObjectFromJSON(json) {
        return BatchObjectFromJSONTyped(json);
    }
    function BatchObjectFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'status': json['status'],
            'errors': !exists(json, 'errors') ? undefined : json['errors'],
        };
    }

    /* tslint:disable */
    function BatchOperationFromJSON(json) {
        return BatchOperationFromJSONTyped(json);
    }
    function BatchOperationFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'status': json['status'],
            'resource_type': json['resource_type'],
            'resources': (json['resources'].map(BatchObjectFromJSON)),
            'created_at': (new Date(json['created_at'])),
            'updated_at': (new Date(json['updated_at'])),
            'test_mode': json['test_mode'],
        };
    }

    /* tslint:disable */
    function BatchOperationsFromJSON(json) {
        return BatchOperationsFromJSONTyped(json);
    }
    function BatchOperationsFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'count': !exists(json, 'count') ? undefined : json['count'],
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(BatchOperationFromJSON)),
        };
    }

    /* tslint:disable */
    function CommodityDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'weight': value.weight,
            'weight_unit': value.weight_unit,
            'title': value.title,
            'description': value.description,
            'quantity': value.quantity,
            'sku': value.sku,
            'hs_code': value.hs_code,
            'value_amount': value.value_amount,
            'value_currency': value.value_currency,
            'origin_country': value.origin_country,
            'parent_id': value.parent_id,
            'metadata': value.metadata,
        };
    }

    /* tslint:disable */
    function OrderBillingAddressFromJSON(json) {
        return OrderBillingAddressFromJSONTyped(json);
    }
    function OrderBillingAddressFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'postal_code': !exists(json, 'postal_code') ? undefined : json['postal_code'],
            'city': !exists(json, 'city') ? undefined : json['city'],
            'federal_tax_id': !exists(json, 'federal_tax_id') ? undefined : json['federal_tax_id'],
            'state_tax_id': !exists(json, 'state_tax_id') ? undefined : json['state_tax_id'],
            'person_name': !exists(json, 'person_name') ? undefined : json['person_name'],
            'company_name': !exists(json, 'company_name') ? undefined : json['company_name'],
            'country_code': json['country_code'],
            'email': !exists(json, 'email') ? undefined : json['email'],
            'phone_number': !exists(json, 'phone_number') ? undefined : json['phone_number'],
            'state_code': !exists(json, 'state_code') ? undefined : json['state_code'],
            'suburb': !exists(json, 'suburb') ? undefined : json['suburb'],
            'residential': !exists(json, 'residential') ? undefined : json['residential'],
            'street_number': !exists(json, 'street_number') ? undefined : json['street_number'],
            'address_line1': !exists(json, 'address_line1') ? undefined : json['address_line1'],
            'address_line2': !exists(json, 'address_line2') ? undefined : json['address_line2'],
            'validate_location': !exists(json, 'validate_location') ? undefined : json['validate_location'],
        };
    }
    function OrderBillingAddressToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'postal_code': value.postal_code,
            'city': value.city,
            'federal_tax_id': value.federal_tax_id,
            'state_tax_id': value.state_tax_id,
            'person_name': value.person_name,
            'company_name': value.company_name,
            'country_code': value.country_code,
            'email': value.email,
            'phone_number': value.phone_number,
            'state_code': value.state_code,
            'suburb': value.suburb,
            'residential': value.residential,
            'street_number': value.street_number,
            'address_line1': value.address_line1,
            'address_line2': value.address_line2,
            'validate_location': value.validate_location,
        };
    }

    /* tslint:disable */
    function OrderDataShippingFromToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'postal_code': value.postal_code,
            'city': value.city,
            'federal_tax_id': value.federal_tax_id,
            'state_tax_id': value.state_tax_id,
            'person_name': value.person_name,
            'company_name': value.company_name,
            'country_code': value.country_code,
            'email': value.email,
            'phone_number': value.phone_number,
            'state_code': value.state_code,
            'suburb': value.suburb,
            'residential': value.residential,
            'street_number': value.street_number,
            'address_line1': value.address_line1,
            'address_line2': value.address_line2,
            'validate_location': value.validate_location,
        };
    }

    /* tslint:disable */
    function OrderDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'order_id': value.order_id,
            'order_date': value.order_date,
            'source': value.source,
            'shipping_to': AddressDataToJSON(value.shipping_to),
            'shipping_from': OrderDataShippingFromToJSON(value.shipping_from),
            'billing_address': OrderBillingAddressToJSON(value.billing_address),
            'line_items': (value.line_items.map(CommodityDataToJSON)),
            'options': value.options,
            'metadata': value.metadata,
        };
    }

    /* tslint:disable */
    function BatchOrderDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'orders': (value.orders.map(OrderDataToJSON)),
        };
    }

    /* tslint:disable */
    function ParcelDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'weight': value.weight,
            'width': value.width,
            'height': value.height,
            'length': value.length,
            'packaging_type': value.packaging_type,
            'package_preset': value.package_preset,
            'description': value.description,
            'content': value.content,
            'is_document': value.is_document,
            'weight_unit': value.weight_unit,
            'dimension_unit': value.dimension_unit,
            'items': value.items === undefined ? undefined : (value.items.map(CommodityDataToJSON)),
            'reference_number': value.reference_number,
            'freight_class': value.freight_class,
            'options': value.options,
        };
    }

    /* tslint:disable */
    function PaymentFromJSON(json) {
        return PaymentFromJSONTyped(json);
    }
    function PaymentFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'paid_by': !exists(json, 'paid_by') ? undefined : json['paid_by'],
            'currency': !exists(json, 'currency') ? undefined : json['currency'],
            'account_number': !exists(json, 'account_number') ? undefined : json['account_number'],
        };
    }
    function PaymentToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'paid_by': value.paid_by,
            'currency': value.currency,
            'account_number': value.account_number,
        };
    }

    /* tslint:disable */
    function ShipmentDataBillingAddressToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'postal_code': value.postal_code,
            'city': value.city,
            'federal_tax_id': value.federal_tax_id,
            'state_tax_id': value.state_tax_id,
            'person_name': value.person_name,
            'company_name': value.company_name,
            'country_code': value.country_code,
            'email': value.email,
            'phone_number': value.phone_number,
            'state_code': value.state_code,
            'suburb': value.suburb,
            'residential': value.residential,
            'street_number': value.street_number,
            'address_line1': value.address_line1,
            'address_line2': value.address_line2,
            'validate_location': value.validate_location,
        };
    }

    /* tslint:disable */
    function CustomsDataDutyBillingAddressToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'postal_code': value.postal_code,
            'city': value.city,
            'federal_tax_id': value.federal_tax_id,
            'state_tax_id': value.state_tax_id,
            'person_name': value.person_name,
            'company_name': value.company_name,
            'country_code': value.country_code,
            'email': value.email,
            'phone_number': value.phone_number,
            'state_code': value.state_code,
            'suburb': value.suburb,
            'residential': value.residential,
            'street_number': value.street_number,
            'address_line1': value.address_line1,
            'address_line2': value.address_line2,
            'validate_location': value.validate_location,
        };
    }

    /* tslint:disable */
    function CustomsDutyFromJSON(json) {
        return CustomsDutyFromJSONTyped(json);
    }
    function CustomsDutyFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'paid_by': !exists(json, 'paid_by') ? undefined : json['paid_by'],
            'currency': !exists(json, 'currency') ? undefined : json['currency'],
            'declared_value': !exists(json, 'declared_value') ? undefined : json['declared_value'],
            'account_number': !exists(json, 'account_number') ? undefined : json['account_number'],
        };
    }
    function CustomsDutyToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'paid_by': value.paid_by,
            'currency': value.currency,
            'declared_value': value.declared_value,
            'account_number': value.account_number,
        };
    }

    /* tslint:disable */
    function ShipmentDataCustomsToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'commodities': (value.commodities.map(CommodityDataToJSON)),
            'duty': CustomsDutyToJSON(value.duty),
            'duty_billing_address': CustomsDataDutyBillingAddressToJSON(value.duty_billing_address),
            'content_type': value.content_type,
            'content_description': value.content_description,
            'incoterm': value.incoterm,
            'invoice': value.invoice,
            'invoice_date': value.invoice_date,
            'commercial_invoice': value.commercial_invoice,
            'certify': value.certify,
            'signer': value.signer,
            'options': value.options,
        };
    }

    /* tslint:disable */
    function ShipmentDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'shipper': AddressDataToJSON(value.shipper),
            'recipient': AddressDataToJSON(value.recipient),
            'parcels': (value.parcels.map(ParcelDataToJSON)),
            'options': value.options,
            'payment': PaymentToJSON(value.payment),
            'billing_address': ShipmentDataBillingAddressToJSON(value.billing_address),
            'customs': ShipmentDataCustomsToJSON(value.customs),
            'reference': value.reference,
            'label_type': value.label_type,
            'service': value.service,
            'services': value.services,
            'carrier_ids': value.carrier_ids,
            'metadata': value.metadata,
        };
    }

    /* tslint:disable */
    function BatchShipmentDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'shipments': (value.shipments.map(ShipmentDataToJSON)),
        };
    }

    /* tslint:disable */
    function TrackerUpdateDataInfoToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'carrier_tracking_link': value.carrier_tracking_link,
            'customer_name': value.customer_name,
            'expected_delivery': value.expected_delivery,
            'note': value.note,
            'order_date': value.order_date,
            'order_id': value.order_id,
            'package_weight': value.package_weight,
            'package_weight_unit': value.package_weight_unit,
            'shipment_package_count': value.shipment_package_count,
            'shipment_pickup_date': value.shipment_pickup_date,
            'shipment_delivery_date': value.shipment_delivery_date,
            'shipment_service': value.shipment_service,
            'shipment_origin_country': value.shipment_origin_country,
            'shipment_origin_postal_code': value.shipment_origin_postal_code,
            'shipment_destination_country': value.shipment_destination_country,
            'shipment_destination_postal_code': value.shipment_destination_postal_code,
            'shipping_date': value.shipping_date,
            'signed_by': value.signed_by,
            'source': value.source,
        };
    }

    /* tslint:disable */
    function TrackingDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'tracking_number': value.tracking_number,
            'carrier_name': value.carrier_name,
            'account_number': value.account_number,
            'reference': value.reference,
            'info': TrackerUpdateDataInfoToJSON(value.info),
            'metadata': value.metadata,
        };
    }

    /* tslint:disable */
    function BatchTrackerDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'trackers': (value.trackers.map(TrackingDataToJSON)),
        };
    }

    /* tslint:disable */
    function CarrierSettingsFromJSON(json) {
        return CarrierSettingsFromJSONTyped(json);
    }
    function CarrierSettingsFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': json['id'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'carrier_id': json['carrier_id'],
            'carrier_name': json['carrier_name'],
            'display_name': !exists(json, 'display_name') ? undefined : json['display_name'],
            'test_mode': json['test_mode'],
            'active': json['active'],
            'capabilities': !exists(json, 'capabilities') ? undefined : json['capabilities'],
            'metadata': !exists(json, 'metadata') ? undefined : json['metadata'],
            'config': !exists(json, 'config') ? undefined : json['config'],
        };
    }

    /* tslint:disable */
    function CarrierListFromJSON(json) {
        return CarrierListFromJSONTyped(json);
    }
    function CarrierListFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'count': !exists(json, 'count') ? undefined : json['count'],
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(CarrierSettingsFromJSON)),
        };
    }

    /* tslint:disable */
    function ChargeFromJSON(json) {
        return ChargeFromJSONTyped(json);
    }
    function ChargeFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'name': !exists(json, 'name') ? undefined : json['name'],
            'amount': !exists(json, 'amount') ? undefined : json['amount'],
            'currency': !exists(json, 'currency') ? undefined : json['currency'],
        };
    }
    function ChargeToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'name': value.name,
            'amount': value.amount,
            'currency': value.currency,
        };
    }

    /* tslint:disable */
    function CommodityFromJSON(json) {
        return CommodityFromJSONTyped(json);
    }
    function CommodityFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'weight': json['weight'],
            'weight_unit': json['weight_unit'],
            'title': !exists(json, 'title') ? undefined : json['title'],
            'description': !exists(json, 'description') ? undefined : json['description'],
            'quantity': !exists(json, 'quantity') ? undefined : json['quantity'],
            'sku': !exists(json, 'sku') ? undefined : json['sku'],
            'hs_code': !exists(json, 'hs_code') ? undefined : json['hs_code'],
            'value_amount': !exists(json, 'value_amount') ? undefined : json['value_amount'],
            'value_currency': !exists(json, 'value_currency') ? undefined : json['value_currency'],
            'origin_country': !exists(json, 'origin_country') ? undefined : json['origin_country'],
            'parent_id': !exists(json, 'parent_id') ? undefined : json['parent_id'],
            'metadata': !exists(json, 'metadata') ? undefined : json['metadata'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
        };
    }
    function CommodityToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'id': value.id,
            'weight': value.weight,
            'weight_unit': value.weight_unit,
            'title': value.title,
            'description': value.description,
            'quantity': value.quantity,
            'sku': value.sku,
            'hs_code': value.hs_code,
            'value_amount': value.value_amount,
            'value_currency': value.value_currency,
            'origin_country': value.origin_country,
            'parent_id': value.parent_id,
            'metadata': value.metadata,
            'object_type': value.object_type,
        };
    }

    /* tslint:disable */
    function CustomsDutyBillingAddressFromJSON(json) {
        return CustomsDutyBillingAddressFromJSONTyped(json);
    }
    function CustomsDutyBillingAddressFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'postal_code': !exists(json, 'postal_code') ? undefined : json['postal_code'],
            'city': !exists(json, 'city') ? undefined : json['city'],
            'federal_tax_id': !exists(json, 'federal_tax_id') ? undefined : json['federal_tax_id'],
            'state_tax_id': !exists(json, 'state_tax_id') ? undefined : json['state_tax_id'],
            'person_name': !exists(json, 'person_name') ? undefined : json['person_name'],
            'company_name': !exists(json, 'company_name') ? undefined : json['company_name'],
            'country_code': json['country_code'],
            'email': !exists(json, 'email') ? undefined : json['email'],
            'phone_number': !exists(json, 'phone_number') ? undefined : json['phone_number'],
            'state_code': !exists(json, 'state_code') ? undefined : json['state_code'],
            'suburb': !exists(json, 'suburb') ? undefined : json['suburb'],
            'residential': !exists(json, 'residential') ? undefined : json['residential'],
            'street_number': !exists(json, 'street_number') ? undefined : json['street_number'],
            'address_line1': !exists(json, 'address_line1') ? undefined : json['address_line1'],
            'address_line2': !exists(json, 'address_line2') ? undefined : json['address_line2'],
            'validate_location': !exists(json, 'validate_location') ? undefined : json['validate_location'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'validation': !exists(json, 'validation') ? undefined : AddressValidationFromJSON(json['validation']),
        };
    }

    /* tslint:disable */
    function CustomsFromJSON(json) {
        return CustomsFromJSONTyped(json);
    }
    function CustomsFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'commodities': !exists(json, 'commodities') ? undefined : (json['commodities'].map(CommodityFromJSON)),
            'duty': !exists(json, 'duty') ? undefined : CustomsDutyFromJSON(json['duty']),
            'duty_billing_address': !exists(json, 'duty_billing_address') ? undefined : CustomsDutyBillingAddressFromJSON(json['duty_billing_address']),
            'content_type': !exists(json, 'content_type') ? undefined : json['content_type'],
            'content_description': !exists(json, 'content_description') ? undefined : json['content_description'],
            'incoterm': !exists(json, 'incoterm') ? undefined : json['incoterm'],
            'invoice': !exists(json, 'invoice') ? undefined : json['invoice'],
            'invoice_date': !exists(json, 'invoice_date') ? undefined : json['invoice_date'],
            'commercial_invoice': !exists(json, 'commercial_invoice') ? undefined : json['commercial_invoice'],
            'certify': !exists(json, 'certify') ? undefined : json['certify'],
            'signer': !exists(json, 'signer') ? undefined : json['signer'],
            'options': !exists(json, 'options') ? undefined : json['options'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
        };
    }

    /* tslint:disable */
    function CustomsDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'commodities': (value.commodities.map(CommodityDataToJSON)),
            'duty': CustomsDutyToJSON(value.duty),
            'duty_billing_address': CustomsDataDutyBillingAddressToJSON(value.duty_billing_address),
            'content_type': value.content_type,
            'content_description': value.content_description,
            'incoterm': value.incoterm,
            'invoice': value.invoice,
            'invoice_date': value.invoice_date,
            'commercial_invoice': value.commercial_invoice,
            'certify': value.certify,
            'signer': value.signer,
            'options': value.options,
        };
    }

    /* tslint:disable */
    function CustomsListFromJSON(json) {
        return CustomsListFromJSONTyped(json);
    }
    function CustomsListFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'count': !exists(json, 'count') ? undefined : json['count'],
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(CustomsFromJSON)),
        };
    }

    /* tslint:disable */
    function DocumentDetailsFromJSON(json) {
        return DocumentDetailsFromJSONTyped(json);
    }
    function DocumentDetailsFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'doc_id': !exists(json, 'doc_id') ? undefined : json['doc_id'],
            'file_name': !exists(json, 'file_name') ? undefined : json['file_name'],
        };
    }

    /* tslint:disable */
    function DocumentFileDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'doc_file': value.doc_file,
            'doc_name': value.doc_name,
            'doc_format': value.doc_format,
            'doc_type': value.doc_type,
        };
    }

    /* tslint:disable */
    function DocumentUploadDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'shipment_id': value.shipment_id,
            'document_files': (value.document_files.map(DocumentFileDataToJSON)),
            'reference': value.reference,
        };
    }

    /* tslint:disable */
    function MessageFromJSON(json) {
        return MessageFromJSONTyped(json);
    }
    function MessageFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'message': !exists(json, 'message') ? undefined : json['message'],
            'code': !exists(json, 'code') ? undefined : json['code'],
            'details': !exists(json, 'details') ? undefined : json['details'],
            'carrier_name': !exists(json, 'carrier_name') ? undefined : json['carrier_name'],
            'carrier_id': !exists(json, 'carrier_id') ? undefined : json['carrier_id'],
        };
    }

    /* tslint:disable */
    function DocumentUploadRecordFromJSON(json) {
        return DocumentUploadRecordFromJSONTyped(json);
    }
    function DocumentUploadRecordFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'carrier_name': !exists(json, 'carrier_name') ? undefined : json['carrier_name'],
            'carrier_id': !exists(json, 'carrier_id') ? undefined : json['carrier_id'],
            'documents': !exists(json, 'documents') ? undefined : (json['documents'].map(DocumentDetailsFromJSON)),
            'meta': !exists(json, 'meta') ? undefined : json['meta'],
            'reference': !exists(json, 'reference') ? undefined : json['reference'],
            'messages': !exists(json, 'messages') ? undefined : (json['messages'].map(MessageFromJSON)),
        };
    }

    /* tslint:disable */
    function DocumentUploadRecordsFromJSON(json) {
        return DocumentUploadRecordsFromJSONTyped(json);
    }
    function DocumentUploadRecordsFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'count': !exists(json, 'count') ? undefined : json['count'],
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(DocumentUploadRecordFromJSON)),
        };
    }

    /* tslint:disable */
    function LineItemFromJSON(json) {
        return LineItemFromJSONTyped(json);
    }
    function LineItemFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'weight': json['weight'],
            'weight_unit': json['weight_unit'],
            'title': !exists(json, 'title') ? undefined : json['title'],
            'description': !exists(json, 'description') ? undefined : json['description'],
            'quantity': !exists(json, 'quantity') ? undefined : json['quantity'],
            'sku': !exists(json, 'sku') ? undefined : json['sku'],
            'hs_code': !exists(json, 'hs_code') ? undefined : json['hs_code'],
            'value_amount': !exists(json, 'value_amount') ? undefined : json['value_amount'],
            'value_currency': !exists(json, 'value_currency') ? undefined : json['value_currency'],
            'origin_country': !exists(json, 'origin_country') ? undefined : json['origin_country'],
            'parent_id': !exists(json, 'parent_id') ? undefined : json['parent_id'],
            'metadata': !exists(json, 'metadata') ? undefined : json['metadata'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'unfulfilled_quantity': !exists(json, 'unfulfilled_quantity') ? undefined : json['unfulfilled_quantity'],
        };
    }

    /* tslint:disable */
    function OperationFromJSON(json) {
        return OperationFromJSONTyped(json);
    }
    function OperationFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'operation': json['operation'],
            'success': json['success'],
        };
    }

    /* tslint:disable */
    function OperationConfirmationFromJSON(json) {
        return OperationConfirmationFromJSONTyped(json);
    }
    function OperationConfirmationFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'operation': json['operation'],
            'success': json['success'],
            'carrier_name': json['carrier_name'],
            'carrier_id': json['carrier_id'],
        };
    }

    /* tslint:disable */
    function OperationResponseFromJSON(json) {
        return OperationResponseFromJSONTyped(json);
    }
    function OperationResponseFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'messages': !exists(json, 'messages') ? undefined : (json['messages'].map(MessageFromJSON)),
            'confirmation': !exists(json, 'confirmation') ? undefined : OperationConfirmationFromJSON(json['confirmation']),
        };
    }

    /* tslint:disable */
    function OrderShippingFromFromJSON(json) {
        return OrderShippingFromFromJSONTyped(json);
    }
    function OrderShippingFromFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'postal_code': !exists(json, 'postal_code') ? undefined : json['postal_code'],
            'city': !exists(json, 'city') ? undefined : json['city'],
            'federal_tax_id': !exists(json, 'federal_tax_id') ? undefined : json['federal_tax_id'],
            'state_tax_id': !exists(json, 'state_tax_id') ? undefined : json['state_tax_id'],
            'person_name': !exists(json, 'person_name') ? undefined : json['person_name'],
            'company_name': !exists(json, 'company_name') ? undefined : json['company_name'],
            'country_code': json['country_code'],
            'email': !exists(json, 'email') ? undefined : json['email'],
            'phone_number': !exists(json, 'phone_number') ? undefined : json['phone_number'],
            'state_code': !exists(json, 'state_code') ? undefined : json['state_code'],
            'suburb': !exists(json, 'suburb') ? undefined : json['suburb'],
            'residential': !exists(json, 'residential') ? undefined : json['residential'],
            'street_number': !exists(json, 'street_number') ? undefined : json['street_number'],
            'address_line1': !exists(json, 'address_line1') ? undefined : json['address_line1'],
            'address_line2': !exists(json, 'address_line2') ? undefined : json['address_line2'],
            'validate_location': !exists(json, 'validate_location') ? undefined : json['validate_location'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'validation': !exists(json, 'validation') ? undefined : AddressValidationFromJSON(json['validation']),
        };
    }

    /* tslint:disable */
    function ParcelFromJSON(json) {
        return ParcelFromJSONTyped(json);
    }
    function ParcelFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'weight': json['weight'],
            'width': !exists(json, 'width') ? undefined : json['width'],
            'height': !exists(json, 'height') ? undefined : json['height'],
            'length': !exists(json, 'length') ? undefined : json['length'],
            'packaging_type': !exists(json, 'packaging_type') ? undefined : json['packaging_type'],
            'package_preset': !exists(json, 'package_preset') ? undefined : json['package_preset'],
            'description': !exists(json, 'description') ? undefined : json['description'],
            'content': !exists(json, 'content') ? undefined : json['content'],
            'is_document': !exists(json, 'is_document') ? undefined : json['is_document'],
            'weight_unit': json['weight_unit'],
            'dimension_unit': !exists(json, 'dimension_unit') ? undefined : json['dimension_unit'],
            'items': !exists(json, 'items') ? undefined : (json['items'].map(CommodityFromJSON)),
            'reference_number': !exists(json, 'reference_number') ? undefined : json['reference_number'],
            'freight_class': !exists(json, 'freight_class') ? undefined : json['freight_class'],
            'options': !exists(json, 'options') ? undefined : json['options'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
        };
    }
    function ParcelToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'id': value.id,
            'weight': value.weight,
            'width': value.width,
            'height': value.height,
            'length': value.length,
            'packaging_type': value.packaging_type,
            'package_preset': value.package_preset,
            'description': value.description,
            'content': value.content,
            'is_document': value.is_document,
            'weight_unit': value.weight_unit,
            'dimension_unit': value.dimension_unit,
            'items': value.items === undefined ? undefined : (value.items.map(CommodityToJSON)),
            'reference_number': value.reference_number,
            'freight_class': value.freight_class,
            'options': value.options,
            'object_type': value.object_type,
        };
    }

    /* tslint:disable */
    function RateFromJSON(json) {
        return RateFromJSONTyped(json);
    }
    function RateFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'carrier_name': json['carrier_name'],
            'carrier_id': json['carrier_id'],
            'currency': !exists(json, 'currency') ? undefined : json['currency'],
            'service': !exists(json, 'service') ? undefined : json['service'],
            'total_charge': !exists(json, 'total_charge') ? undefined : json['total_charge'],
            'transit_days': !exists(json, 'transit_days') ? undefined : json['transit_days'],
            'extra_charges': !exists(json, 'extra_charges') ? undefined : (json['extra_charges'].map(ChargeFromJSON)),
            'estimated_delivery': !exists(json, 'estimated_delivery') ? undefined : json['estimated_delivery'],
            'meta': !exists(json, 'meta') ? undefined : json['meta'],
            'test_mode': json['test_mode'],
        };
    }
    function RateToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'id': value.id,
            'object_type': value.object_type,
            'carrier_name': value.carrier_name,
            'carrier_id': value.carrier_id,
            'currency': value.currency,
            'service': value.service,
            'total_charge': value.total_charge,
            'transit_days': value.transit_days,
            'extra_charges': value.extra_charges === undefined ? undefined : (value.extra_charges.map(ChargeToJSON)),
            'estimated_delivery': value.estimated_delivery,
            'meta': value.meta,
            'test_mode': value.test_mode,
        };
    }

    /* tslint:disable */
    function ShipmentBillingAddressFromJSON(json) {
        return ShipmentBillingAddressFromJSONTyped(json);
    }
    function ShipmentBillingAddressFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'postal_code': !exists(json, 'postal_code') ? undefined : json['postal_code'],
            'city': !exists(json, 'city') ? undefined : json['city'],
            'federal_tax_id': !exists(json, 'federal_tax_id') ? undefined : json['federal_tax_id'],
            'state_tax_id': !exists(json, 'state_tax_id') ? undefined : json['state_tax_id'],
            'person_name': !exists(json, 'person_name') ? undefined : json['person_name'],
            'company_name': !exists(json, 'company_name') ? undefined : json['company_name'],
            'country_code': json['country_code'],
            'email': !exists(json, 'email') ? undefined : json['email'],
            'phone_number': !exists(json, 'phone_number') ? undefined : json['phone_number'],
            'state_code': !exists(json, 'state_code') ? undefined : json['state_code'],
            'suburb': !exists(json, 'suburb') ? undefined : json['suburb'],
            'residential': !exists(json, 'residential') ? undefined : json['residential'],
            'street_number': !exists(json, 'street_number') ? undefined : json['street_number'],
            'address_line1': !exists(json, 'address_line1') ? undefined : json['address_line1'],
            'address_line2': !exists(json, 'address_line2') ? undefined : json['address_line2'],
            'validate_location': !exists(json, 'validate_location') ? undefined : json['validate_location'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'validation': !exists(json, 'validation') ? undefined : AddressValidationFromJSON(json['validation']),
        };
    }

    /* tslint:disable */
    function ShipmentCustomsFromJSON(json) {
        return ShipmentCustomsFromJSONTyped(json);
    }
    function ShipmentCustomsFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'commodities': !exists(json, 'commodities') ? undefined : (json['commodities'].map(CommodityFromJSON)),
            'duty': !exists(json, 'duty') ? undefined : CustomsDutyFromJSON(json['duty']),
            'duty_billing_address': !exists(json, 'duty_billing_address') ? undefined : CustomsDutyBillingAddressFromJSON(json['duty_billing_address']),
            'content_type': !exists(json, 'content_type') ? undefined : json['content_type'],
            'content_description': !exists(json, 'content_description') ? undefined : json['content_description'],
            'incoterm': !exists(json, 'incoterm') ? undefined : json['incoterm'],
            'invoice': !exists(json, 'invoice') ? undefined : json['invoice'],
            'invoice_date': !exists(json, 'invoice_date') ? undefined : json['invoice_date'],
            'commercial_invoice': !exists(json, 'commercial_invoice') ? undefined : json['commercial_invoice'],
            'certify': !exists(json, 'certify') ? undefined : json['certify'],
            'signer': !exists(json, 'signer') ? undefined : json['signer'],
            'options': !exists(json, 'options') ? undefined : json['options'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
        };
    }

    /* tslint:disable */
    function ShipmentSelectedRateFromJSON(json) {
        return ShipmentSelectedRateFromJSONTyped(json);
    }
    function ShipmentSelectedRateFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'carrier_name': json['carrier_name'],
            'carrier_id': json['carrier_id'],
            'currency': !exists(json, 'currency') ? undefined : json['currency'],
            'service': !exists(json, 'service') ? undefined : json['service'],
            'total_charge': !exists(json, 'total_charge') ? undefined : json['total_charge'],
            'transit_days': !exists(json, 'transit_days') ? undefined : json['transit_days'],
            'extra_charges': !exists(json, 'extra_charges') ? undefined : (json['extra_charges'].map(ChargeFromJSON)),
            'estimated_delivery': !exists(json, 'estimated_delivery') ? undefined : json['estimated_delivery'],
            'meta': !exists(json, 'meta') ? undefined : json['meta'],
            'test_mode': json['test_mode'],
        };
    }

    /* tslint:disable */
    function ShipmentFromJSON(json) {
        return ShipmentFromJSONTyped(json);
    }
    function ShipmentFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'tracking_url': !exists(json, 'tracking_url') ? undefined : json['tracking_url'],
            'shipper': AddressFromJSON(json['shipper']),
            'recipient': AddressFromJSON(json['recipient']),
            'parcels': (json['parcels'].map(ParcelFromJSON)),
            'services': !exists(json, 'services') ? undefined : json['services'],
            'options': !exists(json, 'options') ? undefined : json['options'],
            'payment': !exists(json, 'payment') ? undefined : PaymentFromJSON(json['payment']),
            'billing_address': !exists(json, 'billing_address') ? undefined : ShipmentBillingAddressFromJSON(json['billing_address']),
            'customs': !exists(json, 'customs') ? undefined : ShipmentCustomsFromJSON(json['customs']),
            'rates': !exists(json, 'rates') ? undefined : (json['rates'].map(RateFromJSON)),
            'reference': !exists(json, 'reference') ? undefined : json['reference'],
            'label_type': !exists(json, 'label_type') ? undefined : json['label_type'],
            'carrier_ids': !exists(json, 'carrier_ids') ? undefined : json['carrier_ids'],
            'tracker_id': !exists(json, 'tracker_id') ? undefined : json['tracker_id'],
            'created_at': json['created_at'],
            'metadata': !exists(json, 'metadata') ? undefined : json['metadata'],
            'messages': !exists(json, 'messages') ? undefined : (json['messages'].map(MessageFromJSON)),
            'status': !exists(json, 'status') ? undefined : json['status'],
            'carrier_name': !exists(json, 'carrier_name') ? undefined : json['carrier_name'],
            'carrier_id': !exists(json, 'carrier_id') ? undefined : json['carrier_id'],
            'tracking_number': !exists(json, 'tracking_number') ? undefined : json['tracking_number'],
            'shipment_identifier': !exists(json, 'shipment_identifier') ? undefined : json['shipment_identifier'],
            'selected_rate': !exists(json, 'selected_rate') ? undefined : ShipmentSelectedRateFromJSON(json['selected_rate']),
            'meta': !exists(json, 'meta') ? undefined : json['meta'],
            'service': !exists(json, 'service') ? undefined : json['service'],
            'selected_rate_id': !exists(json, 'selected_rate_id') ? undefined : json['selected_rate_id'],
            'test_mode': json['test_mode'],
            'label_url': !exists(json, 'label_url') ? undefined : json['label_url'],
            'invoice_url': !exists(json, 'invoice_url') ? undefined : json['invoice_url'],
        };
    }

    /* tslint:disable */
    function OrderFromJSON(json) {
        return OrderFromJSONTyped(json);
    }
    function OrderFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'order_id': json['order_id'],
            'order_date': !exists(json, 'order_date') ? undefined : json['order_date'],
            'source': !exists(json, 'source') ? undefined : json['source'],
            'status': !exists(json, 'status') ? undefined : json['status'],
            'shipping_to': AddressFromJSON(json['shipping_to']),
            'shipping_from': !exists(json, 'shipping_from') ? undefined : OrderShippingFromFromJSON(json['shipping_from']),
            'billing_address': !exists(json, 'billing_address') ? undefined : OrderBillingAddressFromJSON(json['billing_address']),
            'line_items': (json['line_items'].map(LineItemFromJSON)),
            'options': !exists(json, 'options') ? undefined : json['options'],
            'meta': !exists(json, 'meta') ? undefined : json['meta'],
            'metadata': !exists(json, 'metadata') ? undefined : json['metadata'],
            'shipments': !exists(json, 'shipments') ? undefined : (json['shipments'].map(ShipmentFromJSON)),
            'test_mode': json['test_mode'],
            'created_at': json['created_at'],
        };
    }

    /* tslint:disable */
    function OrderListFromJSON(json) {
        return OrderListFromJSONTyped(json);
    }
    function OrderListFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'count': !exists(json, 'count') ? undefined : json['count'],
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(OrderFromJSON)),
        };
    }

    /* tslint:disable */
    function OrderUpdateDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'options': value.options,
            'metadata': value.metadata,
        };
    }

    /* tslint:disable */
    function ParcelListFromJSON(json) {
        return ParcelListFromJSONTyped(json);
    }
    function ParcelListFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'count': !exists(json, 'count') ? undefined : json['count'],
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(ParcelFromJSON)),
        };
    }

    /* tslint:disable */
    function PatchedAddressDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'postal_code': value.postal_code,
            'city': value.city,
            'federal_tax_id': value.federal_tax_id,
            'state_tax_id': value.state_tax_id,
            'person_name': value.person_name,
            'company_name': value.company_name,
            'country_code': value.country_code,
            'email': value.email,
            'phone_number': value.phone_number,
            'state_code': value.state_code,
            'suburb': value.suburb,
            'residential': value.residential,
            'street_number': value.street_number,
            'address_line1': value.address_line1,
            'address_line2': value.address_line2,
            'validate_location': value.validate_location,
        };
    }

    /* tslint:disable */
    function PatchedCustomsDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'commodities': value.commodities === undefined ? undefined : (value.commodities.map(CommodityDataToJSON)),
            'duty': CustomsDutyToJSON(value.duty),
            'duty_billing_address': CustomsDataDutyBillingAddressToJSON(value.duty_billing_address),
            'content_type': value.content_type,
            'content_description': value.content_description,
            'incoterm': value.incoterm,
            'invoice': value.invoice,
            'invoice_date': value.invoice_date,
            'commercial_invoice': value.commercial_invoice,
            'certify': value.certify,
            'signer': value.signer,
            'options': value.options,
        };
    }

    /* tslint:disable */
    function PatchedParcelDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'weight': value.weight,
            'width': value.width,
            'height': value.height,
            'length': value.length,
            'packaging_type': value.packaging_type,
            'package_preset': value.package_preset,
            'description': value.description,
            'content': value.content,
            'is_document': value.is_document,
            'weight_unit': value.weight_unit,
            'dimension_unit': value.dimension_unit,
            'items': value.items === undefined ? undefined : (value.items.map(CommodityDataToJSON)),
            'reference_number': value.reference_number,
            'freight_class': value.freight_class,
            'options': value.options,
        };
    }

    /* tslint:disable */
    function PatchedWebhookDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'url': value.url,
            'description': value.description,
            'enabled_events': value.enabled_events,
            'disabled': value.disabled,
        };
    }

    /* tslint:disable */
    function PickupPickupChargeFromJSON(json) {
        return PickupPickupChargeFromJSONTyped(json);
    }
    function PickupPickupChargeFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'name': !exists(json, 'name') ? undefined : json['name'],
            'amount': !exists(json, 'amount') ? undefined : json['amount'],
            'currency': !exists(json, 'currency') ? undefined : json['currency'],
        };
    }

    /* tslint:disable */
    function PickupFromJSON(json) {
        return PickupFromJSONTyped(json);
    }
    function PickupFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'carrier_name': json['carrier_name'],
            'carrier_id': json['carrier_id'],
            'confirmation_number': json['confirmation_number'],
            'pickup_date': !exists(json, 'pickup_date') ? undefined : json['pickup_date'],
            'pickup_charge': !exists(json, 'pickup_charge') ? undefined : PickupPickupChargeFromJSON(json['pickup_charge']),
            'ready_time': !exists(json, 'ready_time') ? undefined : json['ready_time'],
            'closing_time': !exists(json, 'closing_time') ? undefined : json['closing_time'],
            'address': AddressFromJSON(json['address']),
            'parcels': (json['parcels'].map(ParcelFromJSON)),
            'instruction': !exists(json, 'instruction') ? undefined : json['instruction'],
            'package_location': !exists(json, 'package_location') ? undefined : json['package_location'],
            'options': !exists(json, 'options') ? undefined : json['options'],
            'metadata': !exists(json, 'metadata') ? undefined : json['metadata'],
            'test_mode': json['test_mode'],
        };
    }

    /* tslint:disable */
    function PickupCancelDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'reason': value.reason,
        };
    }

    /* tslint:disable */
    function PickupCancelRequestToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'confirmation_number': value.confirmation_number,
            'address': AddressDataToJSON(value.address),
            'pickup_date': value.pickup_date,
            'reason': value.reason,
        };
    }

    /* tslint:disable */
    function PickupDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'pickup_date': value.pickup_date,
            'address': AddressDataToJSON(value.address),
            'ready_time': value.ready_time,
            'closing_time': value.closing_time,
            'instruction': value.instruction,
            'package_location': value.package_location,
            'options': value.options,
            'tracking_numbers': value.tracking_numbers,
            'metadata': value.metadata,
        };
    }

    /* tslint:disable */
    function PickupListFromJSON(json) {
        return PickupListFromJSONTyped(json);
    }
    function PickupListFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'count': !exists(json, 'count') ? undefined : json['count'],
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(PickupFromJSON)),
        };
    }

    /* tslint:disable */
    function PickupRequestToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'pickup_date': value.pickup_date,
            'address': AddressDataToJSON(value.address),
            'parcels': (value.parcels.map(ParcelDataToJSON)),
            'ready_time': value.ready_time,
            'closing_time': value.closing_time,
            'instruction': value.instruction,
            'package_location': value.package_location,
            'options': value.options,
        };
    }

    /* tslint:disable */
    function PickupResponseFromJSON(json) {
        return PickupResponseFromJSONTyped(json);
    }
    function PickupResponseFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'messages': !exists(json, 'messages') ? undefined : (json['messages'].map(MessageFromJSON)),
            'pickup': !exists(json, 'pickup') ? undefined : PickupFromJSON(json['pickup']),
        };
    }

    /* tslint:disable */
    function PickupUpdateDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'pickup_date': value.pickup_date,
            'address': AddressDataToJSON(value.address),
            'ready_time': value.ready_time,
            'closing_time': value.closing_time,
            'instruction': value.instruction,
            'package_location': value.package_location,
            'options': value.options,
            'tracking_numbers': value.tracking_numbers,
            'metadata': value.metadata,
            'confirmation_number': value.confirmation_number,
        };
    }

    /* tslint:disable */
    function PickupUpdateRequestToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'pickup_date': value.pickup_date,
            'address': AddressToJSON(value.address),
            'parcels': (value.parcels.map(ParcelToJSON)),
            'confirmation_number': value.confirmation_number,
            'ready_time': value.ready_time,
            'closing_time': value.closing_time,
            'instruction': value.instruction,
            'package_location': value.package_location,
            'options': value.options,
        };
    }

    /* tslint:disable */
    function RateRequestToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'shipper': AddressDataToJSON(value.shipper),
            'recipient': AddressDataToJSON(value.recipient),
            'parcels': (value.parcels.map(ParcelDataToJSON)),
            'services': value.services,
            'options': value.options,
            'reference': value.reference,
            'carrier_ids': value.carrier_ids,
        };
    }

    /* tslint:disable */
    function RateResponseFromJSON(json) {
        return RateResponseFromJSONTyped(json);
    }
    function RateResponseFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'messages': !exists(json, 'messages') ? undefined : (json['messages'].map(MessageFromJSON)),
            'rates': (json['rates'].map(RateFromJSON)),
        };
    }

    /* tslint:disable */
    function ShipmentCancelRequestToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'shipment_identifier': value.shipment_identifier,
            'service': value.service,
            'options': value.options,
        };
    }

    /* tslint:disable */
    function ShipmentListFromJSON(json) {
        return ShipmentListFromJSONTyped(json);
    }
    function ShipmentListFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'count': !exists(json, 'count') ? undefined : json['count'],
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(ShipmentFromJSON)),
        };
    }

    /* tslint:disable */
    function ShipmentPurchaseDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'selected_rate_id': value.selected_rate_id,
            'label_type': value.label_type,
            'payment': PaymentToJSON(value.payment),
            'reference': value.reference,
            'metadata': value.metadata,
        };
    }

    /* tslint:disable */
    function ShipmentRateDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'services': value.services,
            'carrier_ids': value.carrier_ids,
            'reference': value.reference,
            'metadata': value.metadata,
        };
    }

    /* tslint:disable */
    function ShipmentUpdateDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'label_type': value.label_type,
            'payment': PaymentToJSON(value.payment),
            'options': value.options,
            'reference': value.reference,
            'metadata': value.metadata,
        };
    }

    /* tslint:disable */
    function ShippingRequestToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'shipper': AddressDataToJSON(value.shipper),
            'recipient': AddressDataToJSON(value.recipient),
            'parcels': (value.parcels.map(ParcelDataToJSON)),
            'options': value.options,
            'payment': PaymentToJSON(value.payment),
            'billing_address': ShipmentDataBillingAddressToJSON(value.billing_address),
            'customs': ShipmentDataCustomsToJSON(value.customs),
            'reference': value.reference,
            'label_type': value.label_type,
            'selected_rate_id': value.selected_rate_id,
            'rates': (value.rates.map(RateToJSON)),
        };
    }

    /* tslint:disable */
    function ShippingResponseDocsFromJSON(json) {
        return ShippingResponseDocsFromJSONTyped(json);
    }
    function ShippingResponseDocsFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'label': !exists(json, 'label') ? undefined : json['label'],
            'invoice': !exists(json, 'invoice') ? undefined : json['invoice'],
        };
    }

    /* tslint:disable */
    function ShippingResponseFromJSON(json) {
        return ShippingResponseFromJSONTyped(json);
    }
    function ShippingResponseFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'tracking_url': !exists(json, 'tracking_url') ? undefined : json['tracking_url'],
            'shipper': AddressFromJSON(json['shipper']),
            'recipient': AddressFromJSON(json['recipient']),
            'parcels': (json['parcels'].map(ParcelFromJSON)),
            'services': !exists(json, 'services') ? undefined : json['services'],
            'options': !exists(json, 'options') ? undefined : json['options'],
            'payment': !exists(json, 'payment') ? undefined : PaymentFromJSON(json['payment']),
            'billing_address': !exists(json, 'billing_address') ? undefined : ShipmentBillingAddressFromJSON(json['billing_address']),
            'customs': !exists(json, 'customs') ? undefined : ShipmentCustomsFromJSON(json['customs']),
            'rates': !exists(json, 'rates') ? undefined : (json['rates'].map(RateFromJSON)),
            'reference': !exists(json, 'reference') ? undefined : json['reference'],
            'label_type': !exists(json, 'label_type') ? undefined : json['label_type'],
            'carrier_ids': !exists(json, 'carrier_ids') ? undefined : json['carrier_ids'],
            'tracker_id': !exists(json, 'tracker_id') ? undefined : json['tracker_id'],
            'created_at': json['created_at'],
            'metadata': !exists(json, 'metadata') ? undefined : json['metadata'],
            'messages': !exists(json, 'messages') ? undefined : (json['messages'].map(MessageFromJSON)),
            'status': !exists(json, 'status') ? undefined : json['status'],
            'carrier_name': !exists(json, 'carrier_name') ? undefined : json['carrier_name'],
            'carrier_id': !exists(json, 'carrier_id') ? undefined : json['carrier_id'],
            'tracking_number': !exists(json, 'tracking_number') ? undefined : json['tracking_number'],
            'shipment_identifier': !exists(json, 'shipment_identifier') ? undefined : json['shipment_identifier'],
            'selected_rate': !exists(json, 'selected_rate') ? undefined : ShipmentSelectedRateFromJSON(json['selected_rate']),
            'docs': !exists(json, 'docs') ? undefined : ShippingResponseDocsFromJSON(json['docs']),
            'meta': !exists(json, 'meta') ? undefined : json['meta'],
            'service': !exists(json, 'service') ? undefined : json['service'],
            'selected_rate_id': !exists(json, 'selected_rate_id') ? undefined : json['selected_rate_id'],
            'test_mode': json['test_mode'],
        };
    }

    /* tslint:disable */
    function TokenObtainPairToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'email': value.email,
            'password': value.password,
        };
    }

    /* tslint:disable */
    function TokenPairFromJSON(json) {
        return TokenPairFromJSONTyped(json);
    }
    function TokenPairFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'access': json['access'],
            'refresh': json['refresh'],
        };
    }

    /* tslint:disable */
    function TokenRefreshToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'refresh': value.refresh,
        };
    }

    /* tslint:disable */
    function TokenVerifyToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'token': value.token,
        };
    }

    /* tslint:disable */
    function TrackingEventFromJSON(json) {
        return TrackingEventFromJSONTyped(json);
    }
    function TrackingEventFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'date': !exists(json, 'date') ? undefined : json['date'],
            'description': !exists(json, 'description') ? undefined : json['description'],
            'location': !exists(json, 'location') ? undefined : json['location'],
            'code': !exists(json, 'code') ? undefined : json['code'],
            'time': !exists(json, 'time') ? undefined : json['time'],
            'latitude': !exists(json, 'latitude') ? undefined : json['latitude'],
            'longitude': !exists(json, 'longitude') ? undefined : json['longitude'],
        };
    }

    /* tslint:disable */
    function TrackingStatusInfoFromJSON(json) {
        return TrackingStatusInfoFromJSONTyped(json);
    }
    function TrackingStatusInfoFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'carrier_tracking_link': !exists(json, 'carrier_tracking_link') ? undefined : json['carrier_tracking_link'],
            'customer_name': !exists(json, 'customer_name') ? undefined : json['customer_name'],
            'expected_delivery': !exists(json, 'expected_delivery') ? undefined : json['expected_delivery'],
            'note': !exists(json, 'note') ? undefined : json['note'],
            'order_date': !exists(json, 'order_date') ? undefined : json['order_date'],
            'order_id': !exists(json, 'order_id') ? undefined : json['order_id'],
            'package_weight': !exists(json, 'package_weight') ? undefined : json['package_weight'],
            'package_weight_unit': !exists(json, 'package_weight_unit') ? undefined : json['package_weight_unit'],
            'shipment_package_count': !exists(json, 'shipment_package_count') ? undefined : json['shipment_package_count'],
            'shipment_pickup_date': !exists(json, 'shipment_pickup_date') ? undefined : json['shipment_pickup_date'],
            'shipment_delivery_date': !exists(json, 'shipment_delivery_date') ? undefined : json['shipment_delivery_date'],
            'shipment_service': !exists(json, 'shipment_service') ? undefined : json['shipment_service'],
            'shipment_origin_country': !exists(json, 'shipment_origin_country') ? undefined : json['shipment_origin_country'],
            'shipment_origin_postal_code': !exists(json, 'shipment_origin_postal_code') ? undefined : json['shipment_origin_postal_code'],
            'shipment_destination_country': !exists(json, 'shipment_destination_country') ? undefined : json['shipment_destination_country'],
            'shipment_destination_postal_code': !exists(json, 'shipment_destination_postal_code') ? undefined : json['shipment_destination_postal_code'],
            'shipping_date': !exists(json, 'shipping_date') ? undefined : json['shipping_date'],
            'signed_by': !exists(json, 'signed_by') ? undefined : json['signed_by'],
            'source': !exists(json, 'source') ? undefined : json['source'],
        };
    }

    /* tslint:disable */
    function TrackingStatusFromJSON(json) {
        return TrackingStatusFromJSONTyped(json);
    }
    function TrackingStatusFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'carrier_name': json['carrier_name'],
            'carrier_id': json['carrier_id'],
            'tracking_number': json['tracking_number'],
            'info': !exists(json, 'info') ? undefined : TrackingStatusInfoFromJSON(json['info']),
            'events': !exists(json, 'events') ? undefined : (json['events'] === null ? null : json['events'].map(TrackingEventFromJSON)),
            'delivered': !exists(json, 'delivered') ? undefined : json['delivered'],
            'test_mode': json['test_mode'],
            'status': !exists(json, 'status') ? undefined : json['status'],
            'estimated_delivery': !exists(json, 'estimated_delivery') ? undefined : json['estimated_delivery'],
            'meta': !exists(json, 'meta') ? undefined : json['meta'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'metadata': !exists(json, 'metadata') ? undefined : json['metadata'],
            'messages': !exists(json, 'messages') ? undefined : (json['messages'].map(MessageFromJSON)),
        };
    }

    /* tslint:disable */
    function TrackerListFromJSON(json) {
        return TrackerListFromJSONTyped(json);
    }
    function TrackerListFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'count': !exists(json, 'count') ? undefined : json['count'],
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(TrackingStatusFromJSON)),
        };
    }

    /* tslint:disable */
    function TrackerUpdateDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'info': TrackerUpdateDataInfoToJSON(value.info),
            'metadata': value.metadata,
        };
    }

    /* tslint:disable */
    function TrackingResponseFromJSON(json) {
        return TrackingResponseFromJSONTyped(json);
    }
    function TrackingResponseFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'messages': !exists(json, 'messages') ? undefined : (json['messages'].map(MessageFromJSON)),
            'tracking': !exists(json, 'tracking') ? undefined : TrackingStatusFromJSON(json['tracking']),
        };
    }

    /* tslint:disable */
    function VerifiedTokenObtainPairToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'refresh': value.refresh,
            'otp_token': value.otp_token,
        };
    }

    /* tslint:disable */
    function WebhookFromJSON(json) {
        return WebhookFromJSONTyped(json);
    }
    function WebhookFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': !exists(json, 'id') ? undefined : json['id'],
            'url': json['url'],
            'description': !exists(json, 'description') ? undefined : json['description'],
            'enabled_events': json['enabled_events'],
            'disabled': !exists(json, 'disabled') ? undefined : json['disabled'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'last_event_at': !exists(json, 'last_event_at') ? undefined : (json['last_event_at'] === null ? null : new Date(json['last_event_at'])),
            'secret': json['secret'],
            'test_mode': json['test_mode'],
        };
    }

    /* tslint:disable */
    function WebhookDataToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'url': value.url,
            'description': value.description,
            'enabled_events': value.enabled_events,
            'disabled': value.disabled,
        };
    }

    /* tslint:disable */
    function WebhookListFromJSON(json) {
        return WebhookListFromJSONTyped(json);
    }
    function WebhookListFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'count': !exists(json, 'count') ? undefined : json['count'],
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(WebhookFromJSON)),
        };
    }

    /* tslint:disable */
    function WebhookTestRequestToJSON(value) {
        if (value === undefined) {
            return undefined;
        }
        if (value === null) {
            return null;
        }
        return {
            'payload': value.payload,
        };
    }

    /* tslint:disable */
    /**
     *
     */
    var AddressesApi = /** @class */ (function (_super) {
        __extends(AddressesApi, _super);
        function AddressesApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Create a new address.
         * Create an address
         */
        AddressesApi.prototype.createRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.addressData === null || requestParameters.addressData === undefined) {
                                throw new RequiredError('addressData', 'Required parameter requestParameters.addressData was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/addresses",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: AddressDataToJSON(requestParameters.addressData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return AddressFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create a new address.
         * Create an address
         */
        AddressesApi.prototype.create = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.createRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Discard an address.
         * Discard an address
         */
        AddressesApi.prototype.discardRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling discard.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/addresses/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return AddressFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Discard an address.
         * Discard an address
         */
        AddressesApi.prototype.discard = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.discardRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve all addresses.
         * List all addresses
         */
        AddressesApi.prototype.listRaw = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/addresses",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return AddressListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all addresses.
         * List all addresses
         */
        AddressesApi.prototype.list = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.listRaw(initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve an address.
         * Retrieve an address
         */
        AddressesApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/addresses/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return AddressFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve an address.
         * Retrieve an address
         */
        AddressesApi.prototype.retrieve = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.retrieveRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * update an address.
         * Update an address
         */
        AddressesApi.prototype.updateRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/addresses/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'PATCH',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PatchedAddressDataToJSON(requestParameters.patchedAddressData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return AddressFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * update an address.
         * Update an address
         */
        AddressesApi.prototype.update = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.updateRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return AddressesApi;
    }(BaseAPI));

    /* tslint:disable */
    /**
     *
     */
    var APIApi = /** @class */ (function (_super) {
        __extends(APIApi, _super);
        function APIApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Authenticate the user and return a token pair
         * Obtain auth token pair
         */
        APIApi.prototype.authenticateRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.tokenObtainPair === null || requestParameters.tokenObtainPair === undefined) {
                                throw new RequiredError('tokenObtainPair', 'Required parameter requestParameters.tokenObtainPair was null or undefined when calling authenticate.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            return [4 /*yield*/, this.request({
                                    path: "/api/token",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: TokenObtainPairToJSON(requestParameters.tokenObtainPair),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TokenPairFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Authenticate the user and return a token pair
         * Obtain auth token pair
         */
        APIApi.prototype.authenticate = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.authenticateRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Data References
         */
        APIApi.prototype.dataRaw = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            headerParameters = {};
                            return [4 /*yield*/, this.request({
                                    path: "/v1/references",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response)];
                    }
                });
            });
        };
        /**
         * Data References
         */
        APIApi.prototype.data = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.dataRaw(initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Get a verified JWT token pair by submitting a Two-Factor authentication code.
         * Get verified JWT token
         */
        APIApi.prototype.getVerifiedTokenRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.verifiedTokenObtainPair === null || requestParameters.verifiedTokenObtainPair === undefined) {
                                throw new RequiredError('verifiedTokenObtainPair', 'Required parameter requestParameters.verifiedTokenObtainPair was null or undefined when calling getVerifiedToken.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            return [4 /*yield*/, this.request({
                                    path: "/api/token/verified",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: VerifiedTokenObtainPairToJSON(requestParameters.verifiedTokenObtainPair),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TokenPairFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Get a verified JWT token pair by submitting a Two-Factor authentication code.
         * Get verified JWT token
         */
        APIApi.prototype.getVerifiedToken = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.getVerifiedTokenRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Instance Metadata
         */
        APIApi.prototype.pingRaw = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            headerParameters = {};
                            return [4 /*yield*/, this.request({
                                    path: "/",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response)];
                    }
                });
            });
        };
        /**
         * Instance Metadata
         */
        APIApi.prototype.ping = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.pingRaw(initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Authenticate the user and return a token pair
         * Refresh auth token
         */
        APIApi.prototype.refreshTokenRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.tokenRefresh === null || requestParameters.tokenRefresh === undefined) {
                                throw new RequiredError('tokenRefresh', 'Required parameter requestParameters.tokenRefresh was null or undefined when calling refreshToken.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            return [4 /*yield*/, this.request({
                                    path: "/api/token/refresh",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: TokenRefreshToJSON(requestParameters.tokenRefresh),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TokenPairFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Authenticate the user and return a token pair
         * Refresh auth token
         */
        APIApi.prototype.refreshToken = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.refreshTokenRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Verify an existent authentication token
         * Verify token
         */
        APIApi.prototype.verifyTokenRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.tokenVerify === null || requestParameters.tokenVerify === undefined) {
                                throw new RequiredError('tokenVerify', 'Required parameter requestParameters.tokenVerify was null or undefined when calling verifyToken.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            return [4 /*yield*/, this.request({
                                    path: "/api/token/verify",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: TokenVerifyToJSON(requestParameters.tokenVerify),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response)];
                    }
                });
            });
        };
        /**
         * Verify an existent authentication token
         * Verify token
         */
        APIApi.prototype.verifyToken = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.verifyTokenRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return APIApi;
    }(BaseAPI));

    /* tslint:disable */
    /**
     *
     */
    var CarriersApi = /** @class */ (function (_super) {
        __extends(CarriersApi, _super);
        function CarriersApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Retrieve a carrier\'s services
         * Get carrier services
         */
        CarriersApi.prototype.getServicesRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling getServices.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/carriers/{carrier_name}/services".replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response)];
                    }
                });
            });
        };
        /**
         * Retrieve a carrier\'s services
         * Get carrier services
         */
        CarriersApi.prototype.getServices = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.getServicesRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Returns the list of configured carriers
         * List all carriers
         */
        CarriersApi.prototype.listRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.active !== undefined) {
                                queryParameters['active'] = requestParameters.active;
                            }
                            if (requestParameters.carrierName !== undefined) {
                                queryParameters['carrier_name'] = requestParameters.carrierName;
                            }
                            if (requestParameters.systemOnly !== undefined) {
                                queryParameters['system_only'] = requestParameters.systemOnly;
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/carriers",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return CarrierListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Returns the list of configured carriers
         * List all carriers
         */
        CarriersApi.prototype.list = function (requestParameters, initOverrides) {
            if (requestParameters === void 0) { requestParameters = {}; }
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.listRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return CarriersApi;
    }(BaseAPI));

    /* tslint:disable */
    /**
     *
     */
    var CustomsApi = /** @class */ (function (_super) {
        __extends(CustomsApi, _super);
        function CustomsApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Create a new customs declaration.
         * Create a customs info
         */
        CustomsApi.prototype.createRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.customsData === null || requestParameters.customsData === undefined) {
                                throw new RequiredError('customsData', 'Required parameter requestParameters.customsData was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/customs_info",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: CustomsDataToJSON(requestParameters.customsData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return CustomsFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create a new customs declaration.
         * Create a customs info
         */
        CustomsApi.prototype.create = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.createRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Discard a customs declaration.
         * Discard a customs info
         */
        CustomsApi.prototype.discardRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling discard.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/customs_info/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return CustomsFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Discard a customs declaration.
         * Discard a customs info
         */
        CustomsApi.prototype.discard = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.discardRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve all stored customs declarations.
         * List all customs info
         */
        CustomsApi.prototype.listRaw = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/customs_info",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return CustomsListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all stored customs declarations.
         * List all customs info
         */
        CustomsApi.prototype.list = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.listRaw(initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve customs declaration.
         * Retrieve a customs info
         */
        CustomsApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/customs_info/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return CustomsFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve customs declaration.
         * Retrieve a customs info
         */
        CustomsApi.prototype.retrieve = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.retrieveRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * modify an existing customs declaration.
         * Update a customs info
         */
        CustomsApi.prototype.updateRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/customs_info/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'PATCH',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PatchedCustomsDataToJSON(requestParameters.patchedCustomsData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return CustomsFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * modify an existing customs declaration.
         * Update a customs info
         */
        CustomsApi.prototype.update = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.updateRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return CustomsApi;
    }(BaseAPI));

    /* tslint:disable */
    /**
     *
     */
    var ParcelsApi = /** @class */ (function (_super) {
        __extends(ParcelsApi, _super);
        function ParcelsApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Create a new parcel.
         * Create a parcel
         */
        ParcelsApi.prototype.createRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.parcelData === null || requestParameters.parcelData === undefined) {
                                throw new RequiredError('parcelData', 'Required parameter requestParameters.parcelData was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/parcels",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ParcelDataToJSON(requestParameters.parcelData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ParcelFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create a new parcel.
         * Create a parcel
         */
        ParcelsApi.prototype.create = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.createRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Remove a parcel.
         * Remove a parcel
         */
        ParcelsApi.prototype.discardRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling discard.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/parcels/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ParcelFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Remove a parcel.
         * Remove a parcel
         */
        ParcelsApi.prototype.discard = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.discardRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve all stored parcels.
         * List all parcels
         */
        ParcelsApi.prototype.listRaw = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/parcels",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ParcelListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all stored parcels.
         * List all parcels
         */
        ParcelsApi.prototype.list = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.listRaw(initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve a parcel.
         * Retrieve a parcel
         */
        ParcelsApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/parcels/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ParcelFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve a parcel.
         * Retrieve a parcel
         */
        ParcelsApi.prototype.retrieve = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.retrieveRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * modify an existing parcel\'s details.
         * Update a parcel
         */
        ParcelsApi.prototype.updateRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/parcels/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'PATCH',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PatchedParcelDataToJSON(requestParameters.patchedParcelData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ParcelFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * modify an existing parcel\'s details.
         * Update a parcel
         */
        ParcelsApi.prototype.update = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.updateRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return ParcelsApi;
    }(BaseAPI));

    /* tslint:disable */
    /**
     *
     */
    var PickupsApi = /** @class */ (function (_super) {
        __extends(PickupsApi, _super);
        function PickupsApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Cancel a pickup of one or more shipments.
         * Cancel a pickup
         */
        PickupsApi.prototype.cancelRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling cancel.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/pickups/{id}/cancel".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupCancelDataToJSON(requestParameters.pickupCancelData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return PickupFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Cancel a pickup of one or more shipments.
         * Cancel a pickup
         */
        PickupsApi.prototype.cancel = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.cancelRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve all scheduled pickups.
         * List shipment pickups
         */
        PickupsApi.prototype.listRaw = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/pickups",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return PickupListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all scheduled pickups.
         * List shipment pickups
         */
        PickupsApi.prototype.list = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.listRaw(initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve a scheduled pickup.
         * Retrieve a pickup
         */
        PickupsApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/pickups/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return PickupFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve a scheduled pickup.
         * Retrieve a pickup
         */
        PickupsApi.prototype.retrieve = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.retrieveRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Schedule a pickup for one or many shipments with labels already purchased.
         * Schedule a pickup
         */
        PickupsApi.prototype.scheduleRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling schedule.');
                            }
                            if (requestParameters.pickupData === null || requestParameters.pickupData === undefined) {
                                throw new RequiredError('pickupData', 'Required parameter requestParameters.pickupData was null or undefined when calling schedule.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/pickups/{carrier_name}/schedule".replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupDataToJSON(requestParameters.pickupData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return PickupFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Schedule a pickup for one or many shipments with labels already purchased.
         * Schedule a pickup
         */
        PickupsApi.prototype.schedule = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.scheduleRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Modify a pickup for one or many shipments with labels already purchased.
         * Update a pickup
         */
        PickupsApi.prototype.updateRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            if (requestParameters.pickupUpdateData === null || requestParameters.pickupUpdateData === undefined) {
                                throw new RequiredError('pickupUpdateData', 'Required parameter requestParameters.pickupUpdateData was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/pickups/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupUpdateDataToJSON(requestParameters.pickupUpdateData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return PickupFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Modify a pickup for one or many shipments with labels already purchased.
         * Update a pickup
         */
        PickupsApi.prototype.update = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.updateRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return PickupsApi;
    }(BaseAPI));

    /* tslint:disable */
    /**
     *
     */
    var ProxyApi = /** @class */ (function (_super) {
        __extends(ProxyApi, _super);
        function ProxyApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Once the shipping rates are retrieved, provide the required info to submit the shipment by specifying your preferred rate.
         * Buy a shipment label
         */
        ProxyApi.prototype.buyLabelRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.shippingRequest === null || requestParameters.shippingRequest === undefined) {
                                throw new RequiredError('shippingRequest', 'Required parameter requestParameters.shippingRequest was null or undefined when calling buyLabel.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/shipping",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShippingRequestToJSON(requestParameters.shippingRequest),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ShippingResponseFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Once the shipping rates are retrieved, provide the required info to submit the shipment by specifying your preferred rate.
         * Buy a shipment label
         */
        ProxyApi.prototype.buyLabel = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.buyLabelRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Cancel a pickup previously scheduled
         * Cancel a pickup
         */
        ProxyApi.prototype.cancelPickupRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling cancelPickup.');
                            }
                            if (requestParameters.pickupCancelRequest === null || requestParameters.pickupCancelRequest === undefined) {
                                throw new RequiredError('pickupCancelRequest', 'Required parameter requestParameters.pickupCancelRequest was null or undefined when calling cancelPickup.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/pickups/{carrier_name}/cancel".replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupCancelRequestToJSON(requestParameters.pickupCancelRequest),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OperationResponseFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Cancel a pickup previously scheduled
         * Cancel a pickup
         */
        ProxyApi.prototype.cancelPickup = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.cancelPickupRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         *  The Shipping process begins by fetching rates for your shipment. Use this service to fetch a shipping rates available.
         * Fetch shipment rates
         */
        ProxyApi.prototype.fetchRatesRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.rateRequest === null || requestParameters.rateRequest === undefined) {
                                throw new RequiredError('rateRequest', 'Required parameter requestParameters.rateRequest was null or undefined when calling fetchRates.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/rates",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: RateRequestToJSON(requestParameters.rateRequest),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return RateResponseFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         *  The Shipping process begins by fetching rates for your shipment. Use this service to fetch a shipping rates available.
         * Fetch shipment rates
         */
        ProxyApi.prototype.fetchRates = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.fetchRatesRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * You can track a shipment by specifying the carrier and the shipment tracking number.
         * Get tracking details
         */
        ProxyApi.prototype.getTrackingRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.trackingData === null || requestParameters.trackingData === undefined) {
                                throw new RequiredError('trackingData', 'Required parameter requestParameters.trackingData was null or undefined when calling getTracking.');
                            }
                            queryParameters = {};
                            if (requestParameters.hub !== undefined) {
                                queryParameters['hub'] = requestParameters.hub;
                            }
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/tracking",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: TrackingDataToJSON(requestParameters.trackingData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackingResponseFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * You can track a shipment by specifying the carrier and the shipment tracking number.
         * Get tracking details
         */
        ProxyApi.prototype.getTracking = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.getTrackingRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Schedule one or many parcels pickup
         * Schedule a pickup
         */
        ProxyApi.prototype.schedulePickupRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling schedulePickup.');
                            }
                            if (requestParameters.pickupRequest === null || requestParameters.pickupRequest === undefined) {
                                throw new RequiredError('pickupRequest', 'Required parameter requestParameters.pickupRequest was null or undefined when calling schedulePickup.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/pickups/{carrier_name}".replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupRequestToJSON(requestParameters.pickupRequest),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return PickupResponseFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Schedule one or many parcels pickup
         * Schedule a pickup
         */
        ProxyApi.prototype.schedulePickup = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.schedulePickupRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * You can track a shipment by specifying the carrier and the shipment tracking number.
         * Track a shipment
         * @deprecated
         */
        ProxyApi.prototype.trackShipmentRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling trackShipment.');
                            }
                            if (requestParameters.trackingNumber === null || requestParameters.trackingNumber === undefined) {
                                throw new RequiredError('trackingNumber', 'Required parameter requestParameters.trackingNumber was null or undefined when calling trackShipment.');
                            }
                            queryParameters = {};
                            if (requestParameters.hub !== undefined) {
                                queryParameters['hub'] = requestParameters.hub;
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/tracking/{carrier_name}/{tracking_number}".replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))).replace("{".concat("tracking_number", "}"), encodeURIComponent(String(requestParameters.trackingNumber))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackingResponseFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * You can track a shipment by specifying the carrier and the shipment tracking number.
         * Track a shipment
         * @deprecated
         */
        ProxyApi.prototype.trackShipment = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.trackShipmentRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Modify a scheduled pickup
         * Update a pickup
         */
        ProxyApi.prototype.updatePickupRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling updatePickup.');
                            }
                            if (requestParameters.pickupUpdateRequest === null || requestParameters.pickupUpdateRequest === undefined) {
                                throw new RequiredError('pickupUpdateRequest', 'Required parameter requestParameters.pickupUpdateRequest was null or undefined when calling updatePickup.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/pickups/{carrier_name}/update".replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupUpdateRequestToJSON(requestParameters.pickupUpdateRequest),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return PickupResponseFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Modify a scheduled pickup
         * Update a pickup
         */
        ProxyApi.prototype.updatePickup = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.updatePickupRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Cancel a shipment and the label previously created
         * Void a shipment label
         */
        ProxyApi.prototype.voidLabelRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling voidLabel.');
                            }
                            if (requestParameters.shipmentCancelRequest === null || requestParameters.shipmentCancelRequest === undefined) {
                                throw new RequiredError('shipmentCancelRequest', 'Required parameter requestParameters.shipmentCancelRequest was null or undefined when calling voidLabel.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/shipping/{carrier_name}/cancel".replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentCancelRequestToJSON(requestParameters.shipmentCancelRequest),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OperationResponseFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Cancel a shipment and the label previously created
         * Void a shipment label
         */
        ProxyApi.prototype.voidLabel = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.voidLabelRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return ProxyApi;
    }(BaseAPI));

    /* tslint:disable */
    /**
     *
     */
    var ShipmentsApi = /** @class */ (function (_super) {
        __extends(ShipmentsApi, _super);
        function ShipmentsApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Void a shipment with the associated label.
         * Cancel a shipment
         */
        ShipmentsApi.prototype.cancelRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling cancel.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/shipments/{id}/cancel".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ShipmentFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Void a shipment with the associated label.
         * Cancel a shipment
         */
        ShipmentsApi.prototype.cancel = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.cancelRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Create a new shipment instance.
         * Create a shipment
         */
        ShipmentsApi.prototype.createRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.shipmentData === null || requestParameters.shipmentData === undefined) {
                                throw new RequiredError('shipmentData', 'Required parameter requestParameters.shipmentData was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/shipments",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentDataToJSON(requestParameters.shipmentData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ShipmentFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create a new shipment instance.
         * Create a shipment
         */
        ShipmentsApi.prototype.create = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.createRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve all shipments.
         * List all shipments
         */
        ShipmentsApi.prototype.listRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.address !== undefined) {
                                queryParameters['address'] = requestParameters.address;
                            }
                            if (requestParameters.carrierName !== undefined) {
                                queryParameters['carrier_name'] = requestParameters.carrierName;
                            }
                            if (requestParameters.createdAfter !== undefined) {
                                queryParameters['created_after'] = requestParameters.createdAfter.toISOString();
                            }
                            if (requestParameters.createdBefore !== undefined) {
                                queryParameters['created_before'] = requestParameters.createdBefore.toISOString();
                            }
                            if (requestParameters.keyword !== undefined) {
                                queryParameters['keyword'] = requestParameters.keyword;
                            }
                            if (requestParameters.metadataKey !== undefined) {
                                queryParameters['metadata_key'] = requestParameters.metadataKey;
                            }
                            if (requestParameters.metadataValue !== undefined) {
                                queryParameters['metadata_value'] = requestParameters.metadataValue;
                            }
                            if (requestParameters.optionKey !== undefined) {
                                queryParameters['option_key'] = requestParameters.optionKey;
                            }
                            if (requestParameters.optionValue !== undefined) {
                                queryParameters['option_value'] = requestParameters.optionValue;
                            }
                            if (requestParameters.reference !== undefined) {
                                queryParameters['reference'] = requestParameters.reference;
                            }
                            if (requestParameters.service !== undefined) {
                                queryParameters['service'] = requestParameters.service;
                            }
                            if (requestParameters.status !== undefined) {
                                queryParameters['status'] = requestParameters.status;
                            }
                            if (requestParameters.trackingNumber !== undefined) {
                                queryParameters['tracking_number'] = requestParameters.trackingNumber;
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/shipments",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ShipmentListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all shipments.
         * List all shipments
         */
        ShipmentsApi.prototype.list = function (requestParameters, initOverrides) {
            if (requestParameters === void 0) { requestParameters = {}; }
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.listRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Select your preferred rates to buy a shipment label.
         * Buy a shipment label
         */
        ShipmentsApi.prototype.purchaseRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling purchase.');
                            }
                            if (requestParameters.shipmentPurchaseData === null || requestParameters.shipmentPurchaseData === undefined) {
                                throw new RequiredError('shipmentPurchaseData', 'Required parameter requestParameters.shipmentPurchaseData was null or undefined when calling purchase.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/shipments/{id}/purchase".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentPurchaseDataToJSON(requestParameters.shipmentPurchaseData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ShipmentFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Select your preferred rates to buy a shipment label.
         * Buy a shipment label
         */
        ShipmentsApi.prototype.purchase = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.purchaseRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Refresh the list of the shipment rates
         * Fetch new shipment rates
         */
        ShipmentsApi.prototype.ratesRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling rates.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/shipments/{id}/rates".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentRateDataToJSON(requestParameters.shipmentRateData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ShipmentFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Refresh the list of the shipment rates
         * Fetch new shipment rates
         */
        ShipmentsApi.prototype.rates = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.ratesRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve a shipment.
         * Retrieve a shipment
         */
        ShipmentsApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/shipments/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ShipmentFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve a shipment.
         * Retrieve a shipment
         */
        ShipmentsApi.prototype.retrieve = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.retrieveRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * This operation allows for updating properties of a shipment including `label_type`, `reference`, `payment`, `options` and `metadata`. It is not for editing the parcels of a shipment.
         * Update a shipment
         */
        ShipmentsApi.prototype.updateRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/shipments/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'PUT',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentUpdateDataToJSON(requestParameters.shipmentUpdateData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ShipmentFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * This operation allows for updating properties of a shipment including `label_type`, `reference`, `payment`, `options` and `metadata`. It is not for editing the parcels of a shipment.
         * Update a shipment
         */
        ShipmentsApi.prototype.update = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.updateRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return ShipmentsApi;
    }(BaseAPI));

    /* tslint:disable */
    /**
     *
     */
    var TrackersApi = /** @class */ (function (_super) {
        __extends(TrackersApi, _super);
        function TrackersApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * This API creates or retrieves (if existent) a tracking status object containing the details and events of a shipping in progress.
         * Add a package tracker
         */
        TrackersApi.prototype.addRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.trackingData === null || requestParameters.trackingData === undefined) {
                                throw new RequiredError('trackingData', 'Required parameter requestParameters.trackingData was null or undefined when calling add.');
                            }
                            queryParameters = {};
                            if (requestParameters.hub !== undefined) {
                                queryParameters['hub'] = requestParameters.hub;
                            }
                            if (requestParameters.pendingPickup !== undefined) {
                                queryParameters['pending_pickup'] = requestParameters.pendingPickup;
                            }
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/trackers",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: TrackingDataToJSON(requestParameters.trackingData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackingStatusFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * This API creates or retrieves (if existent) a tracking status object containing the details and events of a shipping in progress.
         * Add a package tracker
         */
        TrackersApi.prototype.add = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.addRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * This API creates or retrieves (if existent) a tracking status object containing the details and events of a shipping in progress.
         * Create a package tracker
         * @deprecated
         */
        TrackersApi.prototype.createRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling create.');
                            }
                            if (requestParameters.carrierName2 === null || requestParameters.carrierName2 === undefined) {
                                throw new RequiredError('carrierName2', 'Required parameter requestParameters.carrierName2 was null or undefined when calling create.');
                            }
                            if (requestParameters.trackingNumber === null || requestParameters.trackingNumber === undefined) {
                                throw new RequiredError('trackingNumber', 'Required parameter requestParameters.trackingNumber was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            if (requestParameters.carrierName2 !== undefined) {
                                queryParameters['carrier_name'] = requestParameters.carrierName2;
                            }
                            if (requestParameters.hub !== undefined) {
                                queryParameters['hub'] = requestParameters.hub;
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/trackers/{carrier_name}/{tracking_number}".replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))).replace("{".concat("tracking_number", "}"), encodeURIComponent(String(requestParameters.trackingNumber))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackingStatusFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * This API creates or retrieves (if existent) a tracking status object containing the details and events of a shipping in progress.
         * Create a package tracker
         * @deprecated
         */
        TrackersApi.prototype.create = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.createRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve all shipment trackers.
         * List all package trackers
         */
        TrackersApi.prototype.listRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.carrierName !== undefined) {
                                queryParameters['carrier_name'] = requestParameters.carrierName;
                            }
                            if (requestParameters.createdAfter !== undefined) {
                                queryParameters['created_after'] = requestParameters.createdAfter.toISOString();
                            }
                            if (requestParameters.createdBefore !== undefined) {
                                queryParameters['created_before'] = requestParameters.createdBefore.toISOString();
                            }
                            if (requestParameters.status !== undefined) {
                                queryParameters['status'] = requestParameters.status;
                            }
                            if (requestParameters.trackingNumber !== undefined) {
                                queryParameters['tracking_number'] = requestParameters.trackingNumber;
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/trackers",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackerListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all shipment trackers.
         * List all package trackers
         */
        TrackersApi.prototype.list = function (requestParameters, initOverrides) {
            if (requestParameters === void 0) { requestParameters = {}; }
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.listRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Discard a package tracker.
         * Discard a package tracker
         */
        TrackersApi.prototype.removeRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.idOrTrackingNumber === null || requestParameters.idOrTrackingNumber === undefined) {
                                throw new RequiredError('idOrTrackingNumber', 'Required parameter requestParameters.idOrTrackingNumber was null or undefined when calling remove.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/trackers/{id_or_tracking_number}".replace("{".concat("id_or_tracking_number", "}"), encodeURIComponent(String(requestParameters.idOrTrackingNumber))),
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackingStatusFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Discard a package tracker.
         * Discard a package tracker
         */
        TrackersApi.prototype.remove = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.removeRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve a package tracker
         * Retrieves a package tracker
         */
        TrackersApi.prototype.retrievesRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.idOrTrackingNumber === null || requestParameters.idOrTrackingNumber === undefined) {
                                throw new RequiredError('idOrTrackingNumber', 'Required parameter requestParameters.idOrTrackingNumber was null or undefined when calling retrieves.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/trackers/{id_or_tracking_number}".replace("{".concat("id_or_tracking_number", "}"), encodeURIComponent(String(requestParameters.idOrTrackingNumber))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackingStatusFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve a package tracker
         * Retrieves a package tracker
         */
        TrackersApi.prototype.retrieves = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.retrievesRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Mixin to log requests
         * Update tracker data
         */
        TrackersApi.prototype.updateRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.idOrTrackingNumber === null || requestParameters.idOrTrackingNumber === undefined) {
                                throw new RequiredError('idOrTrackingNumber', 'Required parameter requestParameters.idOrTrackingNumber was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/trackers/{id_or_tracking_number}".replace("{".concat("id_or_tracking_number", "}"), encodeURIComponent(String(requestParameters.idOrTrackingNumber))),
                                    method: 'PUT',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: TrackerUpdateDataToJSON(requestParameters.trackerUpdateData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackingStatusFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Mixin to log requests
         * Update tracker data
         */
        TrackersApi.prototype.update = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.updateRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return TrackersApi;
    }(BaseAPI));

    /* tslint:disable */
    /**
     *
     */
    var WebhooksApi = /** @class */ (function (_super) {
        __extends(WebhooksApi, _super);
        function WebhooksApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Create a new webhook.
         * Create a webhook
         */
        WebhooksApi.prototype.createRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.webhookData === null || requestParameters.webhookData === undefined) {
                                throw new RequiredError('webhookData', 'Required parameter requestParameters.webhookData was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/webhooks",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: WebhookDataToJSON(requestParameters.webhookData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return WebhookFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create a new webhook.
         * Create a webhook
         */
        WebhooksApi.prototype.create = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.createRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve all webhooks.
         * List all webhooks
         */
        WebhooksApi.prototype.listRaw = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/webhooks",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return WebhookListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all webhooks.
         * List all webhooks
         */
        WebhooksApi.prototype.list = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.listRaw(initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Remove a webhook.
         * Remove a webhook
         */
        WebhooksApi.prototype.removeRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling remove.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/webhooks/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OperationFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Remove a webhook.
         * Remove a webhook
         */
        WebhooksApi.prototype.remove = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.removeRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve a webhook.
         * Retrieve a webhook
         */
        WebhooksApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/webhooks/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return WebhookFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve a webhook.
         * Retrieve a webhook
         */
        WebhooksApi.prototype.retrieve = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.retrieveRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * test a webhook.
         * Test a webhook
         */
        WebhooksApi.prototype.testRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling test.');
                            }
                            if (requestParameters.webhookTestRequest === null || requestParameters.webhookTestRequest === undefined) {
                                throw new RequiredError('webhookTestRequest', 'Required parameter requestParameters.webhookTestRequest was null or undefined when calling test.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/webhooks/{id}/test".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: WebhookTestRequestToJSON(requestParameters.webhookTestRequest),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OperationFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * test a webhook.
         * Test a webhook
         */
        WebhooksApi.prototype.test = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.testRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * update a webhook.
         * Update a webhook
         */
        WebhooksApi.prototype.updateRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/webhooks/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'PATCH',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PatchedWebhookDataToJSON(requestParameters.patchedWebhookData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return WebhookFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * update a webhook.
         * Update a webhook
         */
        WebhooksApi.prototype.update = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.updateRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return WebhooksApi;
    }(BaseAPI));

    /* tslint:disable */
    /**
     *
     */
    var OrdersApi = /** @class */ (function (_super) {
        __extends(OrdersApi, _super);
        function OrdersApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Cancel an order.
         * Cancel an order
         */
        OrdersApi.prototype.cancelRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling cancel.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/orders/{id}/cancel".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OrderFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Cancel an order.
         * Cancel an order
         */
        OrdersApi.prototype.cancel = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.cancelRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Create a new order object.
         * Create an order
         */
        OrdersApi.prototype.createRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.orderData === null || requestParameters.orderData === undefined) {
                                throw new RequiredError('orderData', 'Required parameter requestParameters.orderData was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/orders",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: OrderDataToJSON(requestParameters.orderData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OrderFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create a new order object.
         * Create an order
         */
        OrdersApi.prototype.create = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.createRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Dismiss an order from fulfillment.
         * Dismiss an order
         * @deprecated
         */
        OrdersApi.prototype.dismissRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling dismiss.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/orders/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OrderFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Dismiss an order from fulfillment.
         * Dismiss an order
         * @deprecated
         */
        OrdersApi.prototype.dismiss = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.dismissRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve all orders.
         * List all orders
         */
        OrdersApi.prototype.listRaw = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/orders",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OrderListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all orders.
         * List all orders
         */
        OrdersApi.prototype.list = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.listRaw(initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve an order.
         * Retrieve an order
         */
        OrdersApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/orders/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OrderFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve an order.
         * Retrieve an order
         */
        OrdersApi.prototype.retrieve = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.retrieveRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * This operation allows for updating properties of an order including `options` and `metadata`. It is not for editing the line items of an order.
         * Update an order
         */
        OrdersApi.prototype.updateRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/orders/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'PUT',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: OrderUpdateDataToJSON(requestParameters.orderUpdateData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OrderFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * This operation allows for updating properties of an order including `options` and `metadata`. It is not for editing the line items of an order.
         * Update an order
         */
        OrdersApi.prototype.update = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.updateRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return OrdersApi;
    }(BaseAPI));

    /* tslint:disable */
    /**
     *
     */
    var BatchesApi = /** @class */ (function (_super) {
        __extends(BatchesApi, _super);
        function BatchesApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Create multiple orders in a single batch. `Beta`
         * Create orders
         */
        BatchesApi.prototype.createOrdersRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.batchOrderData === null || requestParameters.batchOrderData === undefined) {
                                throw new RequiredError('batchOrderData', 'Required parameter requestParameters.batchOrderData was null or undefined when calling createOrders.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/batches/orders",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: BatchOrderDataToJSON(requestParameters.batchOrderData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return BatchOperationFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create multiple orders in a single batch. `Beta`
         * Create orders
         */
        BatchesApi.prototype.createOrders = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.createOrdersRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Create multiple shipments in a single batch. `Beta`
         * Create shipments
         */
        BatchesApi.prototype.createShipmentsRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.batchShipmentData === null || requestParameters.batchShipmentData === undefined) {
                                throw new RequiredError('batchShipmentData', 'Required parameter requestParameters.batchShipmentData was null or undefined when calling createShipments.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/batches/shipments",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: BatchShipmentDataToJSON(requestParameters.batchShipmentData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return BatchOperationFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create multiple shipments in a single batch. `Beta`
         * Create shipments
         */
        BatchesApi.prototype.createShipments = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.createShipmentsRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Create multiple trackers in a single batch. `Beta`
         * Create trackers
         */
        BatchesApi.prototype.createTrackersRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.batchTrackerData === null || requestParameters.batchTrackerData === undefined) {
                                throw new RequiredError('batchTrackerData', 'Required parameter requestParameters.batchTrackerData was null or undefined when calling createTrackers.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/batches/trackers",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: BatchTrackerDataToJSON(requestParameters.batchTrackerData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return BatchOperationFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create multiple trackers in a single batch. `Beta`
         * Create trackers
         */
        BatchesApi.prototype.createTrackers = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.createTrackersRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Import csv, xls and xlsx data files for: `Beta`<br/> - trackers data - orders data - shipments data - billing data (soon)<br/><br/> **This operation will return a batch operation that you can poll to follow the import progression.**
         * Import data files
         */
        BatchesApi.prototype.importFileRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, consumes, canConsumeForm$1, formParams, useForm, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.dataFile !== undefined) {
                                queryParameters['data_file'] = requestParameters.dataFile;
                            }
                            if (requestParameters.dataTemplate !== undefined) {
                                queryParameters['data_template'] = requestParameters.dataTemplate;
                            }
                            if (requestParameters.resourceType !== undefined) {
                                queryParameters['resource_type'] = requestParameters.resourceType;
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            consumes = [
                                { contentType: 'multipart/form-data' },
                            ];
                            canConsumeForm$1 = canConsumeForm(consumes);
                            useForm = false;
                            // use FormData to transmit files using content-type "multipart/form-data"
                            useForm = canConsumeForm$1;
                            if (useForm) {
                                formParams = new FormData();
                            }
                            else {
                                formParams = new URLSearchParams();
                            }
                            if (requestParameters.resourceType2 !== undefined) {
                                formParams.append('resource_type', requestParameters.resourceType2);
                            }
                            if (requestParameters.dataTemplate2 !== undefined) {
                                formParams.append('data_template', requestParameters.dataTemplate2);
                            }
                            if (requestParameters.dataFile2 !== undefined) {
                                formParams.append('data_file', requestParameters.dataFile2);
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/batches/data/import",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: formParams,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return BatchOperationFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Import csv, xls and xlsx data files for: `Beta`<br/> - trackers data - orders data - shipments data - billing data (soon)<br/><br/> **This operation will return a batch operation that you can poll to follow the import progression.**
         * Import data files
         */
        BatchesApi.prototype.importFile = function (requestParameters, initOverrides) {
            if (requestParameters === void 0) { requestParameters = {}; }
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.importFileRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve all batch operations. `Beta`
         * List all batch operations
         */
        BatchesApi.prototype.listRaw = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/batches/operations",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return BatchOperationsFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all batch operations. `Beta`
         * List all batch operations
         */
        BatchesApi.prototype.list = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.listRaw(initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve a batch operation. `Beta`
         * Retrieve a batch operation
         */
        BatchesApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/batches/operations/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return BatchOperationFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve a batch operation. `Beta`
         * Retrieve a batch operation
         */
        BatchesApi.prototype.retrieve = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.retrieveRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return BatchesApi;
    }(BaseAPI));

    /* tslint:disable */
    /**
     *
     */
    var DocumentsApi = /** @class */ (function (_super) {
        __extends(DocumentsApi, _super);
        function DocumentsApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Retrieve all shipping document upload records.
         * List all upload records
         */
        DocumentsApi.prototype.listRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.createdAfter !== undefined) {
                                queryParameters['created_after'] = requestParameters.createdAfter.toISOString();
                            }
                            if (requestParameters.createdBefore !== undefined) {
                                queryParameters['created_before'] = requestParameters.createdBefore.toISOString();
                            }
                            if (requestParameters.shipmentId !== undefined) {
                                queryParameters['shipment_id'] = requestParameters.shipmentId;
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/documents",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return DocumentUploadRecordsFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all shipping document upload records.
         * List all upload records
         */
        DocumentsApi.prototype.list = function (requestParameters, initOverrides) {
            if (requestParameters === void 0) { requestParameters = {}; }
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.listRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve a shipping document upload record.
         * Retrieve an upload record
         */
        DocumentsApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/documents/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return DocumentUploadRecordFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve a shipping document upload record.
         * Retrieve an upload record
         */
        DocumentsApi.prototype.retrieve = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.retrieveRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Upload a shipping document.
         * Upload documents
         */
        DocumentsApi.prototype.uploadRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, response;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            if (requestParameters.documentUploadData === null || requestParameters.documentUploadData === undefined) {
                                throw new RequiredError('documentUploadData', 'Required parameter requestParameters.documentUploadData was null or undefined when calling upload.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _c.sent();
                            _c.label = 2;
                        case 2:
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/documents",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: DocumentUploadDataToJSON(requestParameters.documentUploadData),
                                }, initOverrides)];
                        case 3:
                            response = _c.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return DocumentUploadRecordFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Upload a shipping document.
         * Upload documents
         */
        DocumentsApi.prototype.upload = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.uploadRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return DocumentsApi;
    }(BaseAPI));

    var KarrioClient = /** @class */ (function () {
        function KarrioClient(clientConfig) {
            var config = new Configuration(__assign({ credentials: "include", headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                } }, clientConfig));
            this.config = clientConfig;
            this.API = new APIApi(config);
            this.addresses = new AddressesApi(config);
            this.carriers = new CarriersApi(config);
            this.customs = new CustomsApi(config);
            this.parcels = new ParcelsApi(config);
            this.pickups = new PickupsApi(config);
            this.proxy = new ProxyApi(config);
            this.shipments = new ShipmentsApi(config);
            this.trackers = new TrackersApi(config);
            this.webhooks = new WebhooksApi(config);
            this.orders = new OrdersApi(config);
            this.batches = new BatchesApi(config);
            this.documents = new DocumentsApi(config);
        }
        return KarrioClient;
    }());

    function Karrio(apiKey, host, apiKeyPrefix) {
        if (host === void 0) { host = 'https://api.karrio.io'; }
        if (apiKeyPrefix === void 0) { apiKeyPrefix = 'Token'; }
        var clientConfig = {
            basePath: host,
            apiKey: "".concat(apiKeyPrefix, " ").concat(apiKey),
        };
        return new KarrioClient(clientConfig);
    }
    Karrio.Client = KarrioClient;

    return Karrio;

})();
//# sourceMappingURL=karrio.js.map
