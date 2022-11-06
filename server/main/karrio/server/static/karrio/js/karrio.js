(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
    typeof define === 'function' && define.amd ? define(factory) :
    (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.Karrio = factory());
})(this, (function () { 'use strict';

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
    /* global Reflect, Promise */

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
            while (_) try {
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

    /* tslint:disable */
    var BASE_PATH = "https://app.karrio.io".replace(/\/+$/, "");
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
                var url, headers, initOverrideFn, initParams, overridedInit, _a, init;
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
                            overridedInit = __assign.apply(void 0, _a.concat([(_b.sent())]));
                            init = __assign(__assign({}, overridedInit), { body: isFormData(overridedInit.body) ||
                                    overridedInit.body instanceof URLSearchParams ||
                                    isBlob(overridedInit.body)
                                    ? overridedInit.body
                                    : JSON.stringify(overridedInit.body) });
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
            'address_line1': value.address_line1,
            'address_line2': value.address_line2,
            'validate_location': value.validate_location,
            'object_type': value.object_type,
            'validation': AddressValidationToJSON(value.validation),
        };
    }

    /* tslint:disable */
    function AddressDataFromJSON(json) {
        return AddressDataFromJSONTyped(json);
    }
    function AddressDataFromJSONTyped(json, ignoreDiscriminator) {
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
            'address_line1': !exists(json, 'address_line1') ? undefined : json['address_line1'],
            'address_line2': !exists(json, 'address_line2') ? undefined : json['address_line2'],
            'validate_location': !exists(json, 'validate_location') ? undefined : json['validate_location'],
        };
    }
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
    function CarrierSettingsFromJSON(json) {
        return CarrierSettingsFromJSONTyped(json);
    }
    function CarrierSettingsFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'id': json['id'],
            'carrier_name': json['carrier_name'],
            'carrier_id': json['carrier_id'],
            'test_mode': json['test_mode'],
            'active': json['active'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
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
    function DutyFromJSON(json) {
        return DutyFromJSONTyped(json);
    }
    function DutyFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'paid_by': !exists(json, 'paid_by') ? undefined : json['paid_by'],
            'currency': !exists(json, 'currency') ? undefined : json['currency'],
            'declared_value': !exists(json, 'declared_value') ? undefined : json['declared_value'],
            'account_number': !exists(json, 'account_number') ? undefined : json['account_number'],
            'bill_to': !exists(json, 'bill_to') ? undefined : AddressFromJSON(json['bill_to']),
        };
    }
    function DutyToJSON(value) {
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
            'bill_to': AddressToJSON(value.bill_to),
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
            'duty': !exists(json, 'duty') ? undefined : DutyFromJSON(json['duty']),
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
            'duty': DutyToJSON(value.duty),
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
    function Data200ResponseFromJSON(json) {
        return Data200ResponseFromJSONTyped(json);
    }
    function Data200ResponseFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'version': !exists(json, 'VERSION') ? undefined : json['VERSION'],
            'app_name': !exists(json, 'APP_NAME') ? undefined : json['APP_NAME'],
            'app_website': !exists(json, 'APP_WEBSITE') ? undefined : json['APP_WEBSITE'],
            'audit_logging': !exists(json, 'AUDIT_LOGGING') ? undefined : json['AUDIT_LOGGING'],
            'allow_signup': !exists(json, 'ALLOW_SIGNUP') ? undefined : json['ALLOW_SIGNUP'],
            'allow_admin_approved_signup': !exists(json, 'ALLOW_ADMIN_APPROVED_SIGNUP') ? undefined : json['ALLOW_ADMIN_APPROVED_SIGNUP'],
            'allow_multi_account': !exists(json, 'ALLOW_MULTI_ACCOUNT') ? undefined : json['ALLOW_MULTI_ACCOUNT'],
            'multi_organizations': !exists(json, 'MULTI_ORGANIZATIONS') ? undefined : json['MULTI_ORGANIZATIONS'],
            'orders_management': !exists(json, 'ORDERS_MANAGEMENT') ? undefined : json['ORDERS_MANAGEMENT'],
            'apps_management': !exists(json, 'APPS_MANAGEMENT') ? undefined : json['APPS_MANAGEMENT'],
            'documents_management': !exists(json, 'DOCUMENTS_MANAGEMENT') ? undefined : json['DOCUMENTS_MANAGEMENT'],
            'data_import_export': !exists(json, 'DATA_IMPORT_EXPORT') ? undefined : json['DATA_IMPORT_EXPORT'],
            'custom_carrier_definition': !exists(json, 'CUSTOM_CARRIER_DEFINITION') ? undefined : json['CUSTOM_CARRIER_DEFINITION'],
            'persist_sdk_tracing': !exists(json, 'PERSIST_SDK_TRACING') ? undefined : json['PERSIST_SDK_TRACING'],
            'admin': !exists(json, 'ADMIN') ? undefined : json['ADMIN'],
            'openapi': !exists(json, 'OPENAPI') ? undefined : json['OPENAPI'],
            'graphql': !exists(json, 'GRAPHQL') ? undefined : json['GRAPHQL'],
            'address_auto_complete': !exists(json, 'ADDRESS_AUTO_COMPLETE') ? undefined : json['ADDRESS_AUTO_COMPLETE'],
            'countries': !exists(json, 'countries') ? undefined : json['countries'],
            'currencies': !exists(json, 'currencies') ? undefined : json['currencies'],
            'carriers': !exists(json, 'carriers') ? undefined : json['carriers'],
            'custom_carriers': !exists(json, 'custom_carriers') ? undefined : json['custom_carriers'],
            'customs_content_type': !exists(json, 'customs_content_type') ? undefined : json['customs_content_type'],
            'incoterms': !exists(json, 'incoterms') ? undefined : json['incoterms'],
            'states': !exists(json, 'states') ? undefined : json['states'],
            'services': !exists(json, 'services') ? undefined : json['services'],
            'service_names': !exists(json, 'service_names') ? undefined : json['service_names'],
            'options': !exists(json, 'options') ? undefined : json['options'],
            'option_names': !exists(json, 'option_names') ? undefined : json['option_names'],
            'package_presets': !exists(json, 'package_presets') ? undefined : json['package_presets'],
            'packaging_types': !exists(json, 'packaging_types') ? undefined : json['packaging_types'],
            'payment_types': !exists(json, 'payment_types') ? undefined : json['payment_types'],
            'carrier_capabilities': !exists(json, 'carrier_capabilities') ? undefined : json['carrier_capabilities'],
            'service_levels': !exists(json, 'service_levels') ? undefined : json['service_levels'],
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
    function DocumentsFromJSON(json) {
        return DocumentsFromJSONTyped(json);
    }
    function DocumentsFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'label': !exists(json, 'label') ? undefined : json['label'],
            'invoice': !exists(json, 'invoice') ? undefined : json['invoice'],
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
            'currency': json['currency'],
            'service': !exists(json, 'service') ? undefined : json['service'],
            'total_charge': !exists(json, 'total_charge') ? undefined : json['total_charge'],
            'transit_days': !exists(json, 'transit_days') ? undefined : json['transit_days'],
            'extra_charges': !exists(json, 'extra_charges') ? undefined : (json['extra_charges'].map(ChargeFromJSON)),
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
            'meta': value.meta,
            'test_mode': value.test_mode,
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
            'customs': !exists(json, 'customs') ? undefined : CustomsFromJSON(json['customs']),
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
            'selected_rate': !exists(json, 'selected_rate') ? undefined : RateFromJSON(json['selected_rate']),
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
            'shipping_from': !exists(json, 'shipping_from') ? undefined : AddressFromJSON(json['shipping_from']),
            'billing_address': !exists(json, 'billing_address') ? undefined : AddressDataFromJSON(json['billing_address']),
            'line_items': (json['line_items'].map(LineItemFromJSON)),
            'options': !exists(json, 'options') ? undefined : json['options'],
            'metadata': !exists(json, 'metadata') ? undefined : json['metadata'],
            'shipments': !exists(json, 'shipments') ? undefined : (json['shipments'].map(ShipmentFromJSON)),
            'test_mode': json['test_mode'],
            'created_at': json['created_at'],
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
            'shipping_from': AddressDataToJSON(value.shipping_from),
            'billing_address': AddressDataToJSON(value.billing_address),
            'line_items': (value.line_items.map(CommodityDataToJSON)),
            'options': value.options,
            'metadata': value.metadata,
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
            'pickup_charge': !exists(json, 'pickup_charge') ? undefined : ChargeFromJSON(json['pickup_charge']),
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
    function Ping200ResponseFromJSON(json) {
        return Ping200ResponseFromJSONTyped(json);
    }
    function Ping200ResponseFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'version': !exists(json, 'VERSION') ? undefined : json['VERSION'],
            'app_name': !exists(json, 'APP_NAME') ? undefined : json['APP_NAME'],
            'app_website': !exists(json, 'APP_WEBSITE') ? undefined : json['APP_WEBSITE'],
            'audit_logging': !exists(json, 'AUDIT_LOGGING') ? undefined : json['AUDIT_LOGGING'],
            'allow_signup': !exists(json, 'ALLOW_SIGNUP') ? undefined : json['ALLOW_SIGNUP'],
            'allow_admin_approved_signup': !exists(json, 'ALLOW_ADMIN_APPROVED_SIGNUP') ? undefined : json['ALLOW_ADMIN_APPROVED_SIGNUP'],
            'allow_multi_account': !exists(json, 'ALLOW_MULTI_ACCOUNT') ? undefined : json['ALLOW_MULTI_ACCOUNT'],
            'multi_organizations': !exists(json, 'MULTI_ORGANIZATIONS') ? undefined : json['MULTI_ORGANIZATIONS'],
            'orders_management': !exists(json, 'ORDERS_MANAGEMENT') ? undefined : json['ORDERS_MANAGEMENT'],
            'apps_management': !exists(json, 'APPS_MANAGEMENT') ? undefined : json['APPS_MANAGEMENT'],
            'documents_management': !exists(json, 'DOCUMENTS_MANAGEMENT') ? undefined : json['DOCUMENTS_MANAGEMENT'],
            'data_import_export': !exists(json, 'DATA_IMPORT_EXPORT') ? undefined : json['DATA_IMPORT_EXPORT'],
            'custom_carrier_definition': !exists(json, 'CUSTOM_CARRIER_DEFINITION') ? undefined : json['CUSTOM_CARRIER_DEFINITION'],
            'persist_sdk_tracing': !exists(json, 'PERSIST_SDK_TRACING') ? undefined : json['PERSIST_SDK_TRACING'],
            'admin': !exists(json, 'ADMIN') ? undefined : json['ADMIN'],
            'openapi': !exists(json, 'OPENAPI') ? undefined : json['OPENAPI'],
            'graphql': !exists(json, 'GRAPHQL') ? undefined : json['GRAPHQL'],
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
            'customs': CustomsDataToJSON(value.customs),
            'reference': value.reference,
            'label_type': value.label_type,
            'service': value.service,
            'services': value.services,
            'carrier_ids': value.carrier_ids,
            'metadata': value.metadata,
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
            'customs': CustomsDataToJSON(value.customs),
            'reference': value.reference,
            'label_type': value.label_type,
            'selected_rate_id': value.selected_rate_id,
            'rates': (value.rates.map(RateToJSON)),
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
            'customs': !exists(json, 'customs') ? undefined : CustomsFromJSON(json['customs']),
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
            'selected_rate': !exists(json, 'selected_rate') ? undefined : RateFromJSON(json['selected_rate']),
            'docs': !exists(json, 'docs') ? undefined : DocumentsFromJSON(json['docs']),
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/addresses",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: AddressDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling discard.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
        AddressesApi.prototype.listRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.limit !== undefined) {
                                queryParameters['limit'] = requestParameters.limit;
                            }
                            if (requestParameters.offset !== undefined) {
                                queryParameters['offset'] = requestParameters.offset;
                            }
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return AddressListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all addresses.
         * List all addresses
         */
        AddressesApi.prototype.list = function (requestParameters, initOverrides) {
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
         * Retrieve an address.
         * Retrieve an address
         */
        AddressesApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/addresses/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'PATCH',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: AddressDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling authenticate.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/api/token",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: TokenObtainPairToJSON(requestParameters.data),
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
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/references",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return Data200ResponseFromJSON(jsonValue); })];
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
         *  Get a verified JWT token pair by submitting a Two-Factor authentication code.
         * Get verified JWT token
         */
        APIApi.prototype.getVerifiedTokenRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling getVerifiedToken.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/api/token/verified",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: VerifiedTokenObtainPairToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TokenPairFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         *  Get a verified JWT token pair by submitting a Two-Factor authentication code.
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
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/",
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return Ping200ResponseFromJSON(jsonValue); })];
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
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling refreshToken.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/api/token/refresh",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: TokenRefreshToJSON(requestParameters.data),
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
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling verifyToken.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/api/token/verify",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: TokenVerifyToJSON(requestParameters.data),
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling getServices.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.limit !== undefined) {
                                queryParameters['limit'] = requestParameters.limit;
                            }
                            if (requestParameters.offset !== undefined) {
                                queryParameters['offset'] = requestParameters.offset;
                            }
                            if (requestParameters.carrierName !== undefined) {
                                queryParameters['carrier_name'] = requestParameters.carrierName;
                            }
                            if (requestParameters.active !== undefined) {
                                queryParameters['active'] = requestParameters.active;
                            }
                            if (requestParameters.systemOnly !== undefined) {
                                queryParameters['system_only'] = requestParameters.systemOnly;
                            }
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/customs_info",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: CustomsDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling discard.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
        CustomsApi.prototype.listRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.limit !== undefined) {
                                queryParameters['limit'] = requestParameters.limit;
                            }
                            if (requestParameters.offset !== undefined) {
                                queryParameters['offset'] = requestParameters.offset;
                            }
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return CustomsListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all stored customs declarations.
         * List all customs info
         */
        CustomsApi.prototype.list = function (requestParameters, initOverrides) {
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
         * Retrieve customs declaration.
         * Retrieve a customs info
         */
        CustomsApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/customs_info/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'PATCH',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: CustomsDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/parcels",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ParcelDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling discard.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
        ParcelsApi.prototype.listRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.limit !== undefined) {
                                queryParameters['limit'] = requestParameters.limit;
                            }
                            if (requestParameters.offset !== undefined) {
                                queryParameters['offset'] = requestParameters.offset;
                            }
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ParcelListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all stored parcels.
         * List all parcels
         */
        ParcelsApi.prototype.list = function (requestParameters, initOverrides) {
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
         * Retrieve a parcel.
         * Retrieve a parcel
         */
        ParcelsApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/parcels/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'PATCH',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ParcelDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling cancel.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling cancel.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/pickups/{id}/cancel".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupCancelDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
        PickupsApi.prototype.listRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.limit !== undefined) {
                                queryParameters['limit'] = requestParameters.limit;
                            }
                            if (requestParameters.offset !== undefined) {
                                queryParameters['offset'] = requestParameters.offset;
                            }
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return PickupListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all scheduled pickups.
         * List shipment pickups
         */
        PickupsApi.prototype.list = function (requestParameters, initOverrides) {
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
         * Retrieve a scheduled pickup.
         * Retrieve a pickup
         */
        PickupsApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling schedule.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling schedule.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/pickups/{carrier_name}/schedule".replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/pickups/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupUpdateDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling buyLabel.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/shipping",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShippingRequestToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling cancelPickup.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling cancelPickup.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/pickups/{carrier_name}/cancel".replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupCancelRequestToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling fetchRates.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/rates",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: RateRequestToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
         * Schedule one or many parcels pickup
         * Schedule a pickup
         */
        ProxyApi.prototype.schedulePickupRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling schedulePickup.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling schedulePickup.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/pickups/{carrier_name}".replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupRequestToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
         */
        ProxyApi.prototype.trackShipmentRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.trackingNumber === null || requestParameters.trackingNumber === undefined) {
                                throw new RequiredError('trackingNumber', 'Required parameter requestParameters.trackingNumber was null or undefined when calling trackShipment.');
                            }
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling trackShipment.');
                            }
                            queryParameters = {};
                            if (requestParameters.hub !== undefined) {
                                queryParameters['hub'] = requestParameters.hub;
                            }
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/tracking/{carrier_name}/{tracking_number}".replace("{".concat("tracking_number", "}"), encodeURIComponent(String(requestParameters.trackingNumber))).replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackingResponseFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * You can track a shipment by specifying the carrier and the shipment tracking number.
         * Track a shipment
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling updatePickup.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling updatePickup.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/pickups/{carrier_name}/update".replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupUpdateRequestToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling voidLabel.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling voidLabel.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/proxy/shipping/{carrier_name}/cancel".replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentCancelRequestToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling cancel.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/shipments/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/shipments",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.address !== undefined) {
                                queryParameters['address'] = requestParameters.address;
                            }
                            if (requestParameters.createdAfter !== undefined) {
                                queryParameters['created_after'] = requestParameters.createdAfter;
                            }
                            if (requestParameters.createdBefore !== undefined) {
                                queryParameters['created_before'] = requestParameters.createdBefore;
                            }
                            if (requestParameters.carrierName !== undefined) {
                                queryParameters['carrier_name'] = requestParameters.carrierName;
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
                            if (requestParameters.optionKey !== undefined) {
                                queryParameters['option_key'] = requestParameters.optionKey;
                            }
                            if (requestParameters.optionValue !== undefined) {
                                queryParameters['option_value'] = requestParameters.optionValue;
                            }
                            if (requestParameters.metadataKey !== undefined) {
                                queryParameters['metadata_key'] = requestParameters.metadataKey;
                            }
                            if (requestParameters.metadataValue !== undefined) {
                                queryParameters['metadata_value'] = requestParameters.metadataValue;
                            }
                            if (requestParameters.trackingNumber !== undefined) {
                                queryParameters['tracking_number'] = requestParameters.trackingNumber;
                            }
                            if (requestParameters.keyword !== undefined) {
                                queryParameters['keyword'] = requestParameters.keyword;
                            }
                            if (requestParameters.limit !== undefined) {
                                queryParameters['limit'] = requestParameters.limit;
                            }
                            if (requestParameters.offset !== undefined) {
                                queryParameters['offset'] = requestParameters.offset;
                            }
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling purchase.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling purchase.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/shipments/{id}/purchase".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentPurchaseDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling rates.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling rates.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/shipments/{id}/rates".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentRateDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/shipments/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'PUT',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentUpdateDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
         * Create a shipment tracker
         */
        TrackersApi.prototype.createRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.trackingNumber === null || requestParameters.trackingNumber === undefined) {
                                throw new RequiredError('trackingNumber', 'Required parameter requestParameters.trackingNumber was null or undefined when calling create.');
                            }
                            if (requestParameters.carrierName === null || requestParameters.carrierName === undefined) {
                                throw new RequiredError('carrierName', 'Required parameter requestParameters.carrierName was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            if (requestParameters.hub !== undefined) {
                                queryParameters['hub'] = requestParameters.hub;
                            }
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/trackers/{carrier_name}/{tracking_number}".replace("{".concat("tracking_number", "}"), encodeURIComponent(String(requestParameters.trackingNumber))).replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters.carrierName))),
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackingStatusFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * This API creates or retrieves (if existent) a tracking status object containing the details and events of a shipping in progress.
         * Create a shipment tracker
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
         * List all shipment trackers
         */
        TrackersApi.prototype.listRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.trackingNumber !== undefined) {
                                queryParameters['tracking_number'] = requestParameters.trackingNumber;
                            }
                            if (requestParameters.createdAfter !== undefined) {
                                queryParameters['created_after'] = requestParameters.createdAfter;
                            }
                            if (requestParameters.createdBefore !== undefined) {
                                queryParameters['created_before'] = requestParameters.createdBefore;
                            }
                            if (requestParameters.carrierName !== undefined) {
                                queryParameters['carrier_name'] = requestParameters.carrierName;
                            }
                            if (requestParameters.status !== undefined) {
                                queryParameters['status'] = requestParameters.status;
                            }
                            if (requestParameters.limit !== undefined) {
                                queryParameters['limit'] = requestParameters.limit;
                            }
                            if (requestParameters.offset !== undefined) {
                                queryParameters['offset'] = requestParameters.offset;
                            }
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackerListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all shipment trackers.
         * List all shipment trackers
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
         * Discard a shipment tracker.
         * Discard a shipment tracker
         */
        TrackersApi.prototype.removeRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.idOrTrackingNumber === null || requestParameters.idOrTrackingNumber === undefined) {
                                throw new RequiredError('idOrTrackingNumber', 'Required parameter requestParameters.idOrTrackingNumber was null or undefined when calling remove.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackingStatusFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Discard a shipment tracker.
         * Discard a shipment tracker
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
         * Retrieve a shipment tracker
         * Retrieves a shipment tracker
         */
        TrackersApi.prototype.retrievesRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.idOrTrackingNumber === null || requestParameters.idOrTrackingNumber === undefined) {
                                throw new RequiredError('idOrTrackingNumber', 'Required parameter requestParameters.idOrTrackingNumber was null or undefined when calling retrieves.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackingStatusFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve a shipment tracker
         * Retrieves a shipment tracker
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/webhooks",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: WebhookDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
        WebhooksApi.prototype.listRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.limit !== undefined) {
                                queryParameters['limit'] = requestParameters.limit;
                            }
                            if (requestParameters.offset !== undefined) {
                                queryParameters['offset'] = requestParameters.offset;
                            }
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return WebhookListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all webhooks.
         * List all webhooks
         */
        WebhooksApi.prototype.list = function (requestParameters, initOverrides) {
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
         * Remove a webhook.
         * Remove a webhook
         */
        WebhooksApi.prototype.removeRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling remove.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling test.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling test.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/webhooks/{id}/test".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: WebhookTestRequestToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/webhooks/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'PATCH',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: WebhookDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling cancel.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling create.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/orders",
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: OrderDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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
         * Retrieve all orders.
         * List all orders
         */
        OrdersApi.prototype.listRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters.address !== undefined) {
                                queryParameters['address'] = requestParameters.address;
                            }
                            if (requestParameters.id !== undefined) {
                                queryParameters['id'] = requestParameters.id;
                            }
                            if (requestParameters.orderId !== undefined) {
                                queryParameters['order_id'] = requestParameters.orderId;
                            }
                            if (requestParameters.source !== undefined) {
                                queryParameters['source'] = requestParameters.source;
                            }
                            if (requestParameters.createdAfter !== undefined) {
                                queryParameters['created_after'] = requestParameters.createdAfter;
                            }
                            if (requestParameters.createdBefore !== undefined) {
                                queryParameters['created_before'] = requestParameters.createdBefore;
                            }
                            if (requestParameters.status !== undefined) {
                                queryParameters['status'] = requestParameters.status;
                            }
                            if (requestParameters.optionKey !== undefined) {
                                queryParameters['option_key'] = requestParameters.optionKey;
                            }
                            if (requestParameters.optionValue !== undefined) {
                                queryParameters['option_value'] = requestParameters.optionValue;
                            }
                            if (requestParameters.metadataKey !== undefined) {
                                queryParameters['metadata_key'] = requestParameters.metadataKey;
                            }
                            if (requestParameters.metadataValue !== undefined) {
                                queryParameters['metadata_value'] = requestParameters.metadataValue;
                            }
                            if (requestParameters.keyword !== undefined) {
                                queryParameters['keyword'] = requestParameters.keyword;
                            }
                            if (requestParameters.limit !== undefined) {
                                queryParameters['limit'] = requestParameters.limit;
                            }
                            if (requestParameters.offset !== undefined) {
                                queryParameters['offset'] = requestParameters.offset;
                            }
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OrderListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all orders.
         * List all orders
         */
        OrdersApi.prototype.list = function (requestParameters, initOverrides) {
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
         * Retrieve an order.
         * Retrieve an order
         */
        OrdersApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling retrieve.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
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
                        case 1:
                            response = _a.sent();
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters.id === null || requestParameters.id === undefined) {
                                throw new RequiredError('id', 'Required parameter requestParameters.id was null or undefined when calling update.');
                            }
                            if (requestParameters.data === null || requestParameters.data === undefined) {
                                throw new RequiredError('data', 'Required parameter requestParameters.data was null or undefined when calling update.');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // JWT authentication
                            }
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                    path: "/v1/orders/{id}".replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters.id))),
                                    method: 'PUT',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: OrderUpdateDataToJSON(requestParameters.data),
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
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

}));
//# sourceMappingURL=karrio.js.map
