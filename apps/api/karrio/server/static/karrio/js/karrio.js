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
    /* global Reflect, Promise, SuppressedError, Symbol, Iterator */

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
        var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
        return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
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
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
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
    var BlobApiResponse = /** @class */ (function () {
        function BlobApiResponse(raw) {
            this.raw = raw;
        }
        BlobApiResponse.prototype.value = function () {
            return __awaiter(this, void 0, void 0, function () {
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.raw.blob()];
                        case 1: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        return BlobApiResponse;
    }());

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the AddressValidation interface.
     */
    function AddressValidationFromJSON(json) {
        return AddressValidationFromJSONTyped(json);
    }
    function AddressValidationFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'success': json['success'],
            'meta': json['meta'] == null ? undefined : json['meta'],
        };
    }
    function AddressValidationToJSON(json) {
        return AddressValidationToJSONTyped(json);
    }
    function AddressValidationToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'success': value['success'],
            'meta': value['meta'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function AddressFromJSON(json) {
        return AddressFromJSONTyped(json);
    }
    function AddressFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'postal_code': json['postal_code'] == null ? undefined : json['postal_code'],
            'city': json['city'] == null ? undefined : json['city'],
            'federal_tax_id': json['federal_tax_id'] == null ? undefined : json['federal_tax_id'],
            'state_tax_id': json['state_tax_id'] == null ? undefined : json['state_tax_id'],
            'person_name': json['person_name'] == null ? undefined : json['person_name'],
            'company_name': json['company_name'] == null ? undefined : json['company_name'],
            'country_code': json['country_code'],
            'email': json['email'] == null ? undefined : json['email'],
            'phone_number': json['phone_number'] == null ? undefined : json['phone_number'],
            'state_code': json['state_code'] == null ? undefined : json['state_code'],
            'residential': json['residential'] == null ? undefined : json['residential'],
            'street_number': json['street_number'] == null ? undefined : json['street_number'],
            'address_line1': json['address_line1'] == null ? undefined : json['address_line1'],
            'address_line2': json['address_line2'] == null ? undefined : json['address_line2'],
            'validate_location': json['validate_location'] == null ? undefined : json['validate_location'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'validation': json['validation'] == null ? undefined : AddressValidationFromJSON(json['validation']),
        };
    }
    function AddressToJSON(json) {
        return AddressToJSONTyped(json);
    }
    function AddressToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'id': value['id'],
            'postal_code': value['postal_code'],
            'city': value['city'],
            'federal_tax_id': value['federal_tax_id'],
            'state_tax_id': value['state_tax_id'],
            'person_name': value['person_name'],
            'company_name': value['company_name'],
            'country_code': value['country_code'],
            'email': value['email'],
            'phone_number': value['phone_number'],
            'state_code': value['state_code'],
            'residential': value['residential'],
            'street_number': value['street_number'],
            'address_line1': value['address_line1'],
            'address_line2': value['address_line2'],
            'validate_location': value['validate_location'],
            'object_type': value['object_type'],
            'validation': AddressValidationToJSON(value['validation']),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function AddressDataFromJSON(json) {
        return AddressDataFromJSONTyped(json);
    }
    function AddressDataFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'postal_code': json['postal_code'] == null ? undefined : json['postal_code'],
            'city': json['city'] == null ? undefined : json['city'],
            'federal_tax_id': json['federal_tax_id'] == null ? undefined : json['federal_tax_id'],
            'state_tax_id': json['state_tax_id'] == null ? undefined : json['state_tax_id'],
            'person_name': json['person_name'] == null ? undefined : json['person_name'],
            'company_name': json['company_name'] == null ? undefined : json['company_name'],
            'country_code': json['country_code'],
            'email': json['email'] == null ? undefined : json['email'],
            'phone_number': json['phone_number'] == null ? undefined : json['phone_number'],
            'state_code': json['state_code'] == null ? undefined : json['state_code'],
            'residential': json['residential'] == null ? undefined : json['residential'],
            'street_number': json['street_number'] == null ? undefined : json['street_number'],
            'address_line1': json['address_line1'] == null ? undefined : json['address_line1'],
            'address_line2': json['address_line2'] == null ? undefined : json['address_line2'],
            'validate_location': json['validate_location'] == null ? undefined : json['validate_location'],
        };
    }
    function AddressDataToJSON(json) {
        return AddressDataToJSONTyped(json);
    }
    function AddressDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'postal_code': value['postal_code'],
            'city': value['city'],
            'federal_tax_id': value['federal_tax_id'],
            'state_tax_id': value['state_tax_id'],
            'person_name': value['person_name'],
            'company_name': value['company_name'],
            'country_code': value['country_code'],
            'email': value['email'],
            'phone_number': value['phone_number'],
            'state_code': value['state_code'],
            'residential': value['residential'],
            'street_number': value['street_number'],
            'address_line1': value['address_line1'],
            'address_line2': value['address_line2'],
            'validate_location': value['validate_location'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function AddressListFromJSON(json) {
        return AddressListFromJSONTyped(json);
    }
    function AddressListFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'count': json['count'] == null ? undefined : json['count'],
            'next': json['next'] == null ? undefined : json['next'],
            'previous': json['previous'] == null ? undefined : json['previous'],
            'results': (json['results'].map(AddressFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Aramex interface.
     */
    function instanceOfAramex(value) {
        if (!('username' in value) || value['username'] === undefined)
            return false;
        if (!('password' in value) || value['password'] === undefined)
            return false;
        if (!('account_pin' in value) || value['account_pin'] === undefined)
            return false;
        if (!('account_entity' in value) || value['account_entity'] === undefined)
            return false;
        if (!('account_number' in value) || value['account_number'] === undefined)
            return false;
        if (!('account_country_code' in value) || value['account_country_code'] === undefined)
            return false;
        return true;
    }
    function AramexFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'username': json['username'],
            'password': json['password'],
            'account_pin': json['account_pin'],
            'account_entity': json['account_entity'],
            'account_number': json['account_number'],
            'account_country_code': json['account_country_code'],
        };
    }
    function AramexToJSON(json) {
        return AramexToJSONTyped(json);
    }
    function AramexToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'username': value['username'],
            'password': value['password'],
            'account_pin': value['account_pin'],
            'account_entity': value['account_entity'],
            'account_number': value['account_number'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the AsendiaUs interface.
     */
    function instanceOfAsendiaUs(value) {
        if (!('username' in value) || value['username'] === undefined)
            return false;
        if (!('password' in value) || value['password'] === undefined)
            return false;
        if (!('api_key' in value) || value['api_key'] === undefined)
            return false;
        return true;
    }
    function AsendiaUsFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'username': json['username'],
            'password': json['password'],
            'api_key': json['api_key'],
            'account_number': json['account_number'] == null ? undefined : json['account_number'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function AsendiaUsToJSON(json) {
        return AsendiaUsToJSONTyped(json);
    }
    function AsendiaUsToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'username': value['username'],
            'password': value['password'],
            'api_key': value['api_key'],
            'account_number': value['account_number'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Australiapost interface.
     */
    function instanceOfAustraliapost(value) {
        if (!('api_key' in value) || value['api_key'] === undefined)
            return false;
        if (!('password' in value) || value['password'] === undefined)
            return false;
        if (!('account_number' in value) || value['account_number'] === undefined)
            return false;
        return true;
    }
    function AustraliapostFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'api_key': json['api_key'],
            'password': json['password'],
            'account_number': json['account_number'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function AustraliapostToJSON(json) {
        return AustraliapostToJSONTyped(json);
    }
    function AustraliapostToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'api_key': value['api_key'],
            'password': value['password'],
            'account_number': value['account_number'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function BatchObjectFromJSON(json) {
        return BatchObjectFromJSONTyped(json);
    }
    function BatchObjectFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'status': json['status'],
            'errors': json['errors'] == null ? undefined : json['errors'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function BatchOperationFromJSON(json) {
        return BatchOperationFromJSONTyped(json);
    }
    function BatchOperationFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'status': json['status'],
            'resource_type': json['resource_type'],
            'resources': (json['resources'].map(BatchObjectFromJSON)),
            'created_at': (new Date(json['created_at'])),
            'updated_at': (new Date(json['updated_at'])),
            'test_mode': json['test_mode'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function BatchOperationsFromJSON(json) {
        return BatchOperationsFromJSONTyped(json);
    }
    function BatchOperationsFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'count': json['count'] == null ? undefined : json['count'],
            'next': json['next'] == null ? undefined : json['next'],
            'previous': json['previous'] == null ? undefined : json['previous'],
            'results': (json['results'].map(BatchOperationFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function CommodityDataToJSON(json) {
        return CommodityDataToJSONTyped(json);
    }
    function CommodityDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'weight': value['weight'],
            'weight_unit': value['weight_unit'],
            'title': value['title'],
            'description': value['description'],
            'quantity': value['quantity'],
            'sku': value['sku'],
            'hs_code': value['hs_code'],
            'value_amount': value['value_amount'],
            'value_currency': value['value_currency'],
            'origin_country': value['origin_country'],
            'product_url': value['product_url'],
            'image_url': value['image_url'],
            'product_id': value['product_id'],
            'variant_id': value['variant_id'],
            'parent_id': value['parent_id'],
            'metadata': value['metadata'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function OrderDataToJSON(json) {
        return OrderDataToJSONTyped(json);
    }
    function OrderDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'order_id': value['order_id'],
            'order_date': value['order_date'],
            'source': value['source'],
            'shipping_to': AddressDataToJSON(value['shipping_to']),
            'shipping_from': AddressDataToJSON(value['shipping_from']),
            'billing_address': AddressDataToJSON(value['billing_address']),
            'line_items': (value['line_items'].map(CommodityDataToJSON)),
            'options': value['options'],
            'metadata': value['metadata'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function BatchOrderDataToJSON(json) {
        return BatchOrderDataToJSONTyped(json);
    }
    function BatchOrderDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'orders': (value['orders'].map(OrderDataToJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function PaymentFromJSON(json) {
        return PaymentFromJSONTyped(json);
    }
    function PaymentFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'paid_by': json['paid_by'] == null ? undefined : json['paid_by'],
            'currency': json['currency'] == null ? undefined : json['currency'],
            'account_number': json['account_number'] == null ? undefined : json['account_number'],
        };
    }
    function PaymentToJSON(json) {
        return PaymentToJSONTyped(json);
    }
    function PaymentToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'paid_by': value['paid_by'],
            'currency': value['currency'],
            'account_number': value['account_number'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function DutyFromJSON(json) {
        return DutyFromJSONTyped(json);
    }
    function DutyFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'paid_by': json['paid_by'] == null ? undefined : json['paid_by'],
            'currency': json['currency'] == null ? undefined : json['currency'],
            'declared_value': json['declared_value'] == null ? undefined : json['declared_value'],
            'account_number': json['account_number'] == null ? undefined : json['account_number'],
        };
    }
    function DutyToJSON(json) {
        return DutyToJSONTyped(json);
    }
    function DutyToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'paid_by': value['paid_by'],
            'currency': value['currency'],
            'declared_value': value['declared_value'],
            'account_number': value['account_number'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function CustomsDataToJSON(json) {
        return CustomsDataToJSONTyped(json);
    }
    function CustomsDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'commodities': (value['commodities'].map(CommodityDataToJSON)),
            'duty': DutyToJSON(value['duty']),
            'duty_billing_address': AddressDataToJSON(value['duty_billing_address']),
            'content_type': value['content_type'],
            'content_description': value['content_description'],
            'incoterm': value['incoterm'],
            'invoice': value['invoice'],
            'invoice_date': value['invoice_date'],
            'commercial_invoice': value['commercial_invoice'],
            'certify': value['certify'],
            'signer': value['signer'],
            'options': value['options'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ParcelDataToJSON(json) {
        return ParcelDataToJSONTyped(json);
    }
    function ParcelDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'weight': value['weight'],
            'width': value['width'],
            'height': value['height'],
            'length': value['length'],
            'packaging_type': value['packaging_type'],
            'package_preset': value['package_preset'],
            'description': value['description'],
            'content': value['content'],
            'is_document': value['is_document'],
            'weight_unit': value['weight_unit'],
            'dimension_unit': value['dimension_unit'],
            'items': value['items'] == null ? undefined : (value['items'].map(CommodityDataToJSON)),
            'reference_number': value['reference_number'],
            'freight_class': value['freight_class'],
            'options': value['options'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ShipmentDataReferenceToJSON(json) {
        return ShipmentDataReferenceToJSONTyped(json);
    }
    function ShipmentDataReferenceToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'recipient': AddressDataToJSON(value['recipient']),
            'shipper': AddressDataToJSON(value['shipper']),
            'return_address': AddressDataToJSON(value['return_address']),
            'billing_address': AddressDataToJSON(value['billing_address']),
            'parcels': (value['parcels'].map(ParcelDataToJSON)),
            'options': value['options'],
            'payment': PaymentToJSON(value['payment']),
            'customs': CustomsDataToJSON(value['customs']),
            'reference': value['reference'],
            'label_type': value['label_type'],
            'service': value['service'],
            'services': value['services'],
            'carrier_ids': value['carrier_ids'],
            'metadata': value['metadata'],
            'id': value['id'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function BatchShipmentDataToJSON(json) {
        return BatchShipmentDataToJSONTyped(json);
    }
    function BatchShipmentDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'shipments': (value['shipments'].map(ShipmentDataReferenceToJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the TrackingInfo interface.
     */
    function TrackingInfoFromJSON(json) {
        return TrackingInfoFromJSONTyped(json);
    }
    function TrackingInfoFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'carrier_tracking_link': json['carrier_tracking_link'] == null ? undefined : json['carrier_tracking_link'],
            'customer_name': json['customer_name'] == null ? undefined : json['customer_name'],
            'expected_delivery': json['expected_delivery'] == null ? undefined : json['expected_delivery'],
            'note': json['note'] == null ? undefined : json['note'],
            'order_date': json['order_date'] == null ? undefined : json['order_date'],
            'order_id': json['order_id'] == null ? undefined : json['order_id'],
            'package_weight': json['package_weight'] == null ? undefined : json['package_weight'],
            'package_weight_unit': json['package_weight_unit'] == null ? undefined : json['package_weight_unit'],
            'shipment_package_count': json['shipment_package_count'] == null ? undefined : json['shipment_package_count'],
            'shipment_pickup_date': json['shipment_pickup_date'] == null ? undefined : json['shipment_pickup_date'],
            'shipment_delivery_date': json['shipment_delivery_date'] == null ? undefined : json['shipment_delivery_date'],
            'shipment_service': json['shipment_service'] == null ? undefined : json['shipment_service'],
            'shipment_origin_country': json['shipment_origin_country'] == null ? undefined : json['shipment_origin_country'],
            'shipment_origin_postal_code': json['shipment_origin_postal_code'] == null ? undefined : json['shipment_origin_postal_code'],
            'shipment_destination_country': json['shipment_destination_country'] == null ? undefined : json['shipment_destination_country'],
            'shipment_destination_postal_code': json['shipment_destination_postal_code'] == null ? undefined : json['shipment_destination_postal_code'],
            'shipping_date': json['shipping_date'] == null ? undefined : json['shipping_date'],
            'signed_by': json['signed_by'] == null ? undefined : json['signed_by'],
            'source': json['source'] == null ? undefined : json['source'],
        };
    }
    function TrackingInfoToJSON(json) {
        return TrackingInfoToJSONTyped(json);
    }
    function TrackingInfoToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'carrier_tracking_link': value['carrier_tracking_link'],
            'customer_name': value['customer_name'],
            'expected_delivery': value['expected_delivery'],
            'note': value['note'],
            'order_date': value['order_date'],
            'order_id': value['order_id'],
            'package_weight': value['package_weight'],
            'package_weight_unit': value['package_weight_unit'],
            'shipment_package_count': value['shipment_package_count'],
            'shipment_pickup_date': value['shipment_pickup_date'],
            'shipment_delivery_date': value['shipment_delivery_date'],
            'shipment_service': value['shipment_service'],
            'shipment_origin_country': value['shipment_origin_country'],
            'shipment_origin_postal_code': value['shipment_origin_postal_code'],
            'shipment_destination_country': value['shipment_destination_country'],
            'shipment_destination_postal_code': value['shipment_destination_postal_code'],
            'shipping_date': value['shipping_date'],
            'signed_by': value['signed_by'],
            'source': value['source'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function TrackingDataToJSON(json) {
        return TrackingDataToJSONTyped(json);
    }
    function TrackingDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'tracking_number': value['tracking_number'],
            'carrier_name': value['carrier_name'],
            'account_number': value['account_number'],
            'reference': value['reference'],
            'info': TrackingInfoToJSON(value['info']),
            'metadata': value['metadata'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function BatchTrackerDataToJSON(json) {
        return BatchTrackerDataToJSONTyped(json);
    }
    function BatchTrackerDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'trackers': (value['trackers'].map(TrackingDataToJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Boxknight interface.
     */
    function instanceOfBoxknight(value) {
        if (!('username' in value) || value['username'] === undefined)
            return false;
        if (!('password' in value) || value['password'] === undefined)
            return false;
        return true;
    }
    function BoxknightFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'username': json['username'],
            'password': json['password'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function BoxknightToJSON(json) {
        return BoxknightToJSONTyped(json);
    }
    function BoxknightToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'username': value['username'],
            'password': value['password'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Bpost interface.
     */
    function instanceOfBpost(value) {
        if (!('account_id' in value) || value['account_id'] === undefined)
            return false;
        if (!('passphrase' in value) || value['passphrase'] === undefined)
            return false;
        return true;
    }
    function BpostFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'account_id': json['account_id'],
            'passphrase': json['passphrase'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function BpostToJSON(json) {
        return BpostToJSONTyped(json);
    }
    function BpostToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'account_id': value['account_id'],
            'passphrase': value['passphrase'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    /**
     * Check if a given object implements the Canadapost interface.
     */
    function instanceOfCanadapost(value) {
        if (!('username' in value) || value['username'] === undefined)
            return false;
        if (!('password' in value) || value['password'] === undefined)
            return false;
        return true;
    }
    function CanadapostFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'username': json['username'],
            'password': json['password'],
            'customer_number': json['customer_number'] == null ? undefined : json['customer_number'],
            'contract_id': json['contract_id'] == null ? undefined : json['contract_id'],
            'language': json['language'] == null ? undefined : json['language'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function CanadapostToJSON(json) {
        return CanadapostToJSONTyped(json);
    }
    function CanadapostToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'username': value['username'],
            'password': value['password'],
            'customer_number': value['customer_number'],
            'contract_id': value['contract_id'],
            'language': value['language'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    /**
     * Check if a given object implements the Canpar interface.
     */
    function instanceOfCanpar(value) {
        if (!('username' in value) || value['username'] === undefined)
            return false;
        if (!('password' in value) || value['password'] === undefined)
            return false;
        return true;
    }
    function CanparFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'username': json['username'],
            'password': json['password'],
            'language': json['language'] == null ? undefined : json['language'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function CanparToJSON(json) {
        return CanparToJSONTyped(json);
    }
    function CanparToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'username': value['username'],
            'password': value['password'],
            'language': value['language'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    /**
     * Check if a given object implements the Chronopost interface.
     */
    function instanceOfChronopost(value) {
        if (!('account_number' in value) || value['account_number'] === undefined)
            return false;
        if (!('password' in value) || value['password'] === undefined)
            return false;
        return true;
    }
    function ChronopostFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'account_number': json['account_number'],
            'password': json['password'],
            'id_emit': json['id_emit'] == null ? undefined : json['id_emit'],
            'language': json['language'] == null ? undefined : json['language'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function ChronopostToJSON(json) {
        return ChronopostToJSONTyped(json);
    }
    function ChronopostToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'account_number': value['account_number'],
            'password': value['password'],
            'id_emit': value['id_emit'],
            'language': value['language'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Colissimo interface.
     */
    function instanceOfColissimo(value) {
        if (!('password' in value) || value['password'] === undefined)
            return false;
        if (!('contract_number' in value) || value['contract_number'] === undefined)
            return false;
        return true;
    }
    function ColissimoFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'password': json['password'],
            'contract_number': json['contract_number'],
            'laposte_api_key': json['laposte_api_key'] == null ? undefined : json['laposte_api_key'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function ColissimoToJSON(json) {
        return ColissimoToJSONTyped(json);
    }
    function ColissimoToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'password': value['password'],
            'contract_number': value['contract_number'],
            'laposte_api_key': value['laposte_api_key'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the DhlExpress interface.
     */
    function instanceOfDhlExpress(value) {
        if (!('site_id' in value) || value['site_id'] === undefined)
            return false;
        if (!('password' in value) || value['password'] === undefined)
            return false;
        return true;
    }
    function DhlExpressFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'site_id': json['site_id'],
            'password': json['password'],
            'account_number': json['account_number'] == null ? undefined : json['account_number'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function DhlExpressToJSON(json) {
        return DhlExpressToJSONTyped(json);
    }
    function DhlExpressToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'site_id': value['site_id'],
            'password': value['password'],
            'account_number': value['account_number'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the DhlParcelDe interface.
     */
    function instanceOfDhlParcelDe(value) {
        if (!('username' in value) || value['username'] === undefined)
            return false;
        if (!('password' in value) || value['password'] === undefined)
            return false;
        if (!('client_id' in value) || value['client_id'] === undefined)
            return false;
        if (!('client_secret' in value) || value['client_secret'] === undefined)
            return false;
        return true;
    }
    function DhlParcelDeFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'username': json['username'],
            'password': json['password'],
            'client_id': json['client_id'],
            'client_secret': json['client_secret'],
            'customer_number': json['customer_number'] == null ? undefined : json['customer_number'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function DhlParcelDeToJSON(json) {
        return DhlParcelDeToJSONTyped(json);
    }
    function DhlParcelDeToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'username': value['username'],
            'password': value['password'],
            'client_id': value['client_id'],
            'client_secret': value['client_secret'],
            'customer_number': value['customer_number'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the DhlPoland interface.
     */
    function instanceOfDhlPoland(value) {
        if (!('username' in value) || value['username'] === undefined)
            return false;
        if (!('password' in value) || value['password'] === undefined)
            return false;
        return true;
    }
    function DhlPolandFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'username': json['username'],
            'password': json['password'],
            'account_number': json['account_number'] == null ? undefined : json['account_number'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function DhlPolandToJSON(json) {
        return DhlPolandToJSONTyped(json);
    }
    function DhlPolandToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'username': value['username'],
            'password': value['password'],
            'account_number': value['account_number'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    /**
     * Check if a given object implements the DhlUniversal interface.
     */
    function instanceOfDhlUniversal(value) {
        if (!('consumer_key' in value) || value['consumer_key'] === undefined)
            return false;
        if (!('consumer_secret' in value) || value['consumer_secret'] === undefined)
            return false;
        return true;
    }
    function DhlUniversalFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'consumer_key': json['consumer_key'],
            'consumer_secret': json['consumer_secret'],
            'language': json['language'] == null ? undefined : json['language'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function DhlUniversalToJSON(json) {
        return DhlUniversalToJSONTyped(json);
    }
    function DhlUniversalToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'consumer_key': value['consumer_key'],
            'consumer_secret': value['consumer_secret'],
            'language': value['language'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Dicom interface.
     */
    function instanceOfDicom(value) {
        if (!('username' in value) || value['username'] === undefined)
            return false;
        if (!('password' in value) || value['password'] === undefined)
            return false;
        return true;
    }
    function DicomFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'username': json['username'],
            'password': json['password'],
            'billing_account': json['billing_account'] == null ? undefined : json['billing_account'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function DicomToJSON(json) {
        return DicomToJSONTyped(json);
    }
    function DicomToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'username': value['username'],
            'password': value['password'],
            'billing_account': value['billing_account'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Dpd interface.
     */
    function instanceOfDpd(value) {
        if (!('delis_id' in value) || value['delis_id'] === undefined)
            return false;
        if (!('password' in value) || value['password'] === undefined)
            return false;
        return true;
    }
    function DpdFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'delis_id': json['delis_id'],
            'password': json['password'],
            'depot': json['depot'] == null ? undefined : json['depot'],
            'message_language': json['message_language'] == null ? undefined : json['message_language'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function DpdToJSON(json) {
        return DpdToJSONTyped(json);
    }
    function DpdToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'delis_id': value['delis_id'],
            'password': value['password'],
            'depot': value['depot'],
            'message_language': value['message_language'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Dtdc interface.
     */
    function instanceOfDtdc(value) {
        if (!('api_key' in value) || value['api_key'] === undefined)
            return false;
        if (!('customer_code' in value) || value['customer_code'] === undefined)
            return false;
        return true;
    }
    function DtdcFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'api_key': json['api_key'],
            'customer_code': json['customer_code'],
            'username': json['username'] == null ? undefined : json['username'],
            'password': json['password'] == null ? undefined : json['password'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function DtdcToJSON(json) {
        return DtdcToJSONTyped(json);
    }
    function DtdcToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'api_key': value['api_key'],
            'customer_code': value['customer_code'],
            'username': value['username'],
            'password': value['password'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Easypost interface.
     */
    function instanceOfEasypost(value) {
        if (!('api_key' in value) || value['api_key'] === undefined)
            return false;
        return true;
    }
    function EasypostFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'api_key': json['api_key'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function EasypostToJSON(json) {
        return EasypostToJSONTyped(json);
    }
    function EasypostToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'api_key': value['api_key'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Easyship interface.
     */
    function instanceOfEasyship(value) {
        if (!('access_token' in value) || value['access_token'] === undefined)
            return false;
        return true;
    }
    function EasyshipFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'access_token': json['access_token'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function EasyshipToJSON(json) {
        return EasyshipToJSONTyped(json);
    }
    function EasyshipToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'access_token': value['access_token'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Eshipper interface.
     */
    function instanceOfEshipper(value) {
        if (!('principal' in value) || value['principal'] === undefined)
            return false;
        if (!('credential' in value) || value['credential'] === undefined)
            return false;
        return true;
    }
    function EshipperFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'principal': json['principal'],
            'credential': json['credential'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function EshipperToJSON(json) {
        return EshipperToJSONTyped(json);
    }
    function EshipperToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'principal': value['principal'],
            'credential': value['credential'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Fedex interface.
     */
    function FedexFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'api_key': json['api_key'] == null ? undefined : json['api_key'],
            'secret_key': json['secret_key'] == null ? undefined : json['secret_key'],
            'account_number': json['account_number'] == null ? undefined : json['account_number'],
            'track_api_key': json['track_api_key'] == null ? undefined : json['track_api_key'],
            'track_secret_key': json['track_secret_key'] == null ? undefined : json['track_secret_key'],
            'account_country_code': json['account_country_code'] == null ? undefined : json['account_country_code'],
        };
    }
    function FedexToJSON(json) {
        return FedexToJSONTyped(json);
    }
    function FedexToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'api_key': value['api_key'],
            'secret_key': value['secret_key'],
            'account_number': value['account_number'],
            'track_api_key': value['track_api_key'],
            'track_secret_key': value['track_secret_key'],
            'account_country_code': value['account_country_code'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ConnectionCredentialsFieldFromJSON(json) {
        return ConnectionCredentialsFieldFromJSONTyped(json);
    }
    function ConnectionCredentialsFieldFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        if (typeof json !== 'object') {
            return json;
        }
        if (instanceOfAramex(json)) {
            return AramexFromJSONTyped(json);
        }
        if (instanceOfAsendiaUs(json)) {
            return AsendiaUsFromJSONTyped(json);
        }
        if (instanceOfAustraliapost(json)) {
            return AustraliapostFromJSONTyped(json);
        }
        if (instanceOfBoxknight(json)) {
            return BoxknightFromJSONTyped(json);
        }
        if (instanceOfBpost(json)) {
            return BpostFromJSONTyped(json);
        }
        if (instanceOfCanadapost(json)) {
            return CanadapostFromJSONTyped(json);
        }
        if (instanceOfCanpar(json)) {
            return CanparFromJSONTyped(json);
        }
        if (instanceOfChronopost(json)) {
            return ChronopostFromJSONTyped(json);
        }
        if (instanceOfColissimo(json)) {
            return ColissimoFromJSONTyped(json);
        }
        if (instanceOfDhlExpress(json)) {
            return DhlExpressFromJSONTyped(json);
        }
        if (instanceOfDhlParcelDe(json)) {
            return DhlParcelDeFromJSONTyped(json);
        }
        if (instanceOfDhlPoland(json)) {
            return DhlPolandFromJSONTyped(json);
        }
        if (instanceOfDhlUniversal(json)) {
            return DhlUniversalFromJSONTyped(json);
        }
        if (instanceOfDicom(json)) {
            return DicomFromJSONTyped(json);
        }
        if (instanceOfDpd(json)) {
            return DpdFromJSONTyped(json);
        }
        if (instanceOfDtdc(json)) {
            return DtdcFromJSONTyped(json);
        }
        if (instanceOfEasypost(json)) {
            return EasypostFromJSONTyped(json);
        }
        if (instanceOfEasyship(json)) {
            return EasyshipFromJSONTyped(json);
        }
        if (instanceOfEshipper(json)) {
            return EshipperFromJSONTyped(json);
        }
        {
            return FedexFromJSONTyped(json);
        }
    }
    function ConnectionCredentialsFieldToJSON(json) {
        return ConnectionCredentialsFieldToJSONTyped(json);
    }
    function ConnectionCredentialsFieldToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        if (typeof value !== 'object') {
            return value;
        }
        if (instanceOfAramex(value)) {
            return AramexToJSON(value);
        }
        if (instanceOfAsendiaUs(value)) {
            return AsendiaUsToJSON(value);
        }
        if (instanceOfAustraliapost(value)) {
            return AustraliapostToJSON(value);
        }
        if (instanceOfBoxknight(value)) {
            return BoxknightToJSON(value);
        }
        if (instanceOfBpost(value)) {
            return BpostToJSON(value);
        }
        if (instanceOfCanadapost(value)) {
            return CanadapostToJSON(value);
        }
        if (instanceOfCanpar(value)) {
            return CanparToJSON(value);
        }
        if (instanceOfChronopost(value)) {
            return ChronopostToJSON(value);
        }
        if (instanceOfColissimo(value)) {
            return ColissimoToJSON(value);
        }
        if (instanceOfDhlExpress(value)) {
            return DhlExpressToJSON(value);
        }
        if (instanceOfDhlParcelDe(value)) {
            return DhlParcelDeToJSON(value);
        }
        if (instanceOfDhlPoland(value)) {
            return DhlPolandToJSON(value);
        }
        if (instanceOfDhlUniversal(value)) {
            return DhlUniversalToJSON(value);
        }
        if (instanceOfDicom(value)) {
            return DicomToJSON(value);
        }
        if (instanceOfDpd(value)) {
            return DpdToJSON(value);
        }
        if (instanceOfDtdc(value)) {
            return DtdcToJSON(value);
        }
        if (instanceOfEasypost(value)) {
            return EasypostToJSON(value);
        }
        if (instanceOfEasyship(value)) {
            return EasyshipToJSON(value);
        }
        if (instanceOfEshipper(value)) {
            return EshipperToJSON(value);
        }
        {
            return FedexToJSON(value);
        }
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function CarrierConnectionFromJSON(json) {
        return CarrierConnectionFromJSONTyped(json);
    }
    function CarrierConnectionFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'carrier_name': json['carrier_name'],
            'display_name': json['display_name'] == null ? undefined : json['display_name'],
            'carrier_id': json['carrier_id'],
            'credentials': json['credentials'] == null ? undefined : ConnectionCredentialsFieldFromJSON(json['credentials']),
            'capabilities': json['capabilities'] == null ? undefined : json['capabilities'],
            'config': json['config'] == null ? undefined : json['config'],
            'metadata': json['metadata'] == null ? undefined : json['metadata'],
            'is_system': json['is_system'],
            'active': json['active'],
            'test_mode': json['test_mode'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function CarrierConnectionDataToJSON(json) {
        return CarrierConnectionDataToJSONTyped(json);
    }
    function CarrierConnectionDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'carrier_name': value['carrier_name'],
            'carrier_id': value['carrier_id'],
            'credentials': ConnectionCredentialsFieldToJSON(value['credentials']),
            'capabilities': value['capabilities'],
            'config': value['config'],
            'metadata': value['metadata'],
            'active': value['active'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function CarrierConnectionListFromJSON(json) {
        return CarrierConnectionListFromJSONTyped(json);
    }
    function CarrierConnectionListFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'count': json['count'] == null ? undefined : json['count'],
            'next': json['next'] == null ? undefined : json['next'],
            'previous': json['previous'] == null ? undefined : json['previous'],
            'results': (json['results'].map(CarrierConnectionFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function CarrierDetailsFromJSON(json) {
        return CarrierDetailsFromJSONTyped(json);
    }
    function CarrierDetailsFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'carrier_name': json['carrier_name'],
            'display_name': json['display_name'],
            'integration_status': json['integration_status'],
            'capabilities': json['capabilities'] == null ? undefined : json['capabilities'],
            'connection_fields': json['connection_fields'] == null ? undefined : json['connection_fields'],
            'config_fields': json['config_fields'] == null ? undefined : json['config_fields'],
            'shipping_services': json['shipping_services'] == null ? undefined : json['shipping_services'],
            'shipping_options': json['shipping_options'] == null ? undefined : json['shipping_options'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Charge interface.
     */
    function ChargeFromJSON(json) {
        return ChargeFromJSONTyped(json);
    }
    function ChargeFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'name': json['name'] == null ? undefined : json['name'],
            'amount': json['amount'] == null ? undefined : json['amount'],
            'currency': json['currency'] == null ? undefined : json['currency'],
            'id': json['id'] == null ? undefined : json['id'],
        };
    }
    function ChargeToJSON(json) {
        return ChargeToJSONTyped(json);
    }
    function ChargeToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'name': value['name'],
            'amount': value['amount'],
            'currency': value['currency'],
            'id': value['id'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function CommodityFromJSON(json) {
        return CommodityFromJSONTyped(json);
    }
    function CommodityFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'weight': json['weight'],
            'weight_unit': json['weight_unit'],
            'title': json['title'] == null ? undefined : json['title'],
            'description': json['description'] == null ? undefined : json['description'],
            'quantity': json['quantity'] == null ? undefined : json['quantity'],
            'sku': json['sku'] == null ? undefined : json['sku'],
            'hs_code': json['hs_code'] == null ? undefined : json['hs_code'],
            'value_amount': json['value_amount'] == null ? undefined : json['value_amount'],
            'value_currency': json['value_currency'] == null ? undefined : json['value_currency'],
            'origin_country': json['origin_country'] == null ? undefined : json['origin_country'],
            'product_url': json['product_url'] == null ? undefined : json['product_url'],
            'image_url': json['image_url'] == null ? undefined : json['image_url'],
            'product_id': json['product_id'] == null ? undefined : json['product_id'],
            'variant_id': json['variant_id'] == null ? undefined : json['variant_id'],
            'parent_id': json['parent_id'] == null ? undefined : json['parent_id'],
            'metadata': json['metadata'] == null ? undefined : json['metadata'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
        };
    }
    function CommodityToJSON(json) {
        return CommodityToJSONTyped(json);
    }
    function CommodityToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'id': value['id'],
            'weight': value['weight'],
            'weight_unit': value['weight_unit'],
            'title': value['title'],
            'description': value['description'],
            'quantity': value['quantity'],
            'sku': value['sku'],
            'hs_code': value['hs_code'],
            'value_amount': value['value_amount'],
            'value_currency': value['value_currency'],
            'origin_country': value['origin_country'],
            'product_url': value['product_url'],
            'image_url': value['image_url'],
            'product_id': value['product_id'],
            'variant_id': value['variant_id'],
            'parent_id': value['parent_id'],
            'metadata': value['metadata'],
            'object_type': value['object_type'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function CustomsFromJSON(json) {
        return CustomsFromJSONTyped(json);
    }
    function CustomsFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'commodities': json['commodities'] == null ? undefined : (json['commodities'].map(CommodityFromJSON)),
            'duty': json['duty'] == null ? undefined : DutyFromJSON(json['duty']),
            'duty_billing_address': json['duty_billing_address'] == null ? undefined : AddressFromJSON(json['duty_billing_address']),
            'content_type': json['content_type'] == null ? undefined : json['content_type'],
            'content_description': json['content_description'] == null ? undefined : json['content_description'],
            'incoterm': json['incoterm'] == null ? undefined : json['incoterm'],
            'invoice': json['invoice'] == null ? undefined : json['invoice'],
            'invoice_date': json['invoice_date'] == null ? undefined : json['invoice_date'],
            'commercial_invoice': json['commercial_invoice'] == null ? undefined : json['commercial_invoice'],
            'certify': json['certify'] == null ? undefined : json['certify'],
            'signer': json['signer'] == null ? undefined : json['signer'],
            'options': json['options'] == null ? undefined : json['options'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the DocumentData interface.
     */
    function DocumentDataToJSON(json) {
        return DocumentDataToJSONTyped(json);
    }
    function DocumentDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'template_id': value['template_id'],
            'template': value['template'],
            'doc_format': value['doc_format'],
            'doc_name': value['doc_name'],
            'data': value['data'],
            'options': value['options'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the DocumentDetails interface.
     */
    function DocumentDetailsFromJSON(json) {
        return DocumentDetailsFromJSONTyped(json);
    }
    function DocumentDetailsFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'doc_id': json['doc_id'] == null ? undefined : json['doc_id'],
            'file_name': json['file_name'] == null ? undefined : json['file_name'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the DocumentFileData interface.
     */
    function DocumentFileDataToJSON(json) {
        return DocumentFileDataToJSONTyped(json);
    }
    function DocumentFileDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'doc_file': value['doc_file'],
            'doc_name': value['doc_name'],
            'doc_format': value['doc_format'],
            'doc_type': value['doc_type'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function DocumentTemplateFromJSON(json) {
        return DocumentTemplateFromJSONTyped(json);
    }
    function DocumentTemplateFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'name': json['name'],
            'slug': json['slug'],
            'template': json['template'],
            'active': json['active'] == null ? undefined : json['active'],
            'description': json['description'] == null ? undefined : json['description'],
            'metadata': json['metadata'] == null ? undefined : json['metadata'],
            'options': json['options'] == null ? undefined : json['options'],
            'related_object': json['related_object'] == null ? undefined : json['related_object'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'preview_url': json['preview_url'] == null ? undefined : json['preview_url'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function DocumentTemplateDataToJSON(json) {
        return DocumentTemplateDataToJSONTyped(json);
    }
    function DocumentTemplateDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'name': value['name'],
            'slug': value['slug'],
            'template': value['template'],
            'active': value['active'],
            'description': value['description'],
            'metadata': value['metadata'],
            'options': value['options'],
            'related_object': value['related_object'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function DocumentTemplateListFromJSON(json) {
        return DocumentTemplateListFromJSONTyped(json);
    }
    function DocumentTemplateListFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'count': json['count'] == null ? undefined : json['count'],
            'next': json['next'] == null ? undefined : json['next'],
            'previous': json['previous'] == null ? undefined : json['previous'],
            'results': (json['results'].map(DocumentTemplateFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function DocumentUploadDataToJSON(json) {
        return DocumentUploadDataToJSONTyped(json);
    }
    function DocumentUploadDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'shipment_id': value['shipment_id'],
            'document_files': (value['document_files'].map(DocumentFileDataToJSON)),
            'reference': value['reference'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Message interface.
     */
    function MessageFromJSON(json) {
        return MessageFromJSONTyped(json);
    }
    function MessageFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'message': json['message'] == null ? undefined : json['message'],
            'code': json['code'] == null ? undefined : json['code'],
            'details': json['details'] == null ? undefined : json['details'],
            'carrier_name': json['carrier_name'] == null ? undefined : json['carrier_name'],
            'carrier_id': json['carrier_id'] == null ? undefined : json['carrier_id'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function DocumentUploadRecordFromJSON(json) {
        return DocumentUploadRecordFromJSONTyped(json);
    }
    function DocumentUploadRecordFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'carrier_name': json['carrier_name'] == null ? undefined : json['carrier_name'],
            'carrier_id': json['carrier_id'] == null ? undefined : json['carrier_id'],
            'documents': json['documents'] == null ? undefined : (json['documents'].map(DocumentDetailsFromJSON)),
            'meta': json['meta'] == null ? undefined : json['meta'],
            'reference': json['reference'] == null ? undefined : json['reference'],
            'messages': json['messages'] == null ? undefined : (json['messages'].map(MessageFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function DocumentUploadRecordsFromJSON(json) {
        return DocumentUploadRecordsFromJSONTyped(json);
    }
    function DocumentUploadRecordsFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'count': json['count'] == null ? undefined : json['count'],
            'next': json['next'] == null ? undefined : json['next'],
            'previous': json['previous'] == null ? undefined : json['previous'],
            'results': (json['results'].map(DocumentUploadRecordFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Documents interface.
     */
    function DocumentsFromJSON(json) {
        return DocumentsFromJSONTyped(json);
    }
    function DocumentsFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'label': json['label'] == null ? undefined : json['label'],
            'invoice': json['invoice'] == null ? undefined : json['invoice'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the GeneratedDocument interface.
     */
    function GeneratedDocumentFromJSON(json) {
        return GeneratedDocumentFromJSONTyped(json);
    }
    function GeneratedDocumentFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'template_id': json['template_id'] == null ? undefined : json['template_id'],
            'doc_format': json['doc_format'] == null ? undefined : json['doc_format'],
            'doc_name': json['doc_name'] == null ? undefined : json['doc_name'],
            'doc_file': json['doc_file'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Images interface.
     */
    function ImagesFromJSON(json) {
        return ImagesFromJSONTyped(json);
    }
    function ImagesFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'delivery_image': json['delivery_image'] == null ? undefined : json['delivery_image'],
            'signature_image': json['signature_image'] == null ? undefined : json['signature_image'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function LineItemFromJSON(json) {
        return LineItemFromJSONTyped(json);
    }
    function LineItemFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'weight': json['weight'],
            'weight_unit': json['weight_unit'],
            'title': json['title'] == null ? undefined : json['title'],
            'description': json['description'] == null ? undefined : json['description'],
            'quantity': json['quantity'] == null ? undefined : json['quantity'],
            'sku': json['sku'] == null ? undefined : json['sku'],
            'hs_code': json['hs_code'] == null ? undefined : json['hs_code'],
            'value_amount': json['value_amount'] == null ? undefined : json['value_amount'],
            'value_currency': json['value_currency'] == null ? undefined : json['value_currency'],
            'origin_country': json['origin_country'] == null ? undefined : json['origin_country'],
            'product_url': json['product_url'] == null ? undefined : json['product_url'],
            'image_url': json['image_url'] == null ? undefined : json['image_url'],
            'product_id': json['product_id'] == null ? undefined : json['product_id'],
            'variant_id': json['variant_id'] == null ? undefined : json['variant_id'],
            'parent_id': json['parent_id'] == null ? undefined : json['parent_id'],
            'metadata': json['metadata'] == null ? undefined : json['metadata'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'unfulfilled_quantity': json['unfulfilled_quantity'] == null ? undefined : json['unfulfilled_quantity'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ManifestFromJSON(json) {
        return ManifestFromJSONTyped(json);
    }
    function ManifestFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'carrier_name': json['carrier_name'],
            'carrier_id': json['carrier_id'],
            'meta': json['meta'] == null ? undefined : json['meta'],
            'test_mode': json['test_mode'],
            'address': AddressDataFromJSON(json['address']),
            'options': json['options'] == null ? undefined : json['options'],
            'reference': json['reference'] == null ? undefined : json['reference'],
            'shipment_identifiers': json['shipment_identifiers'],
            'metadata': json['metadata'] == null ? undefined : json['metadata'],
            'manifest_url': json['manifest_url'] == null ? undefined : json['manifest_url'],
            'messages': json['messages'] == null ? undefined : (json['messages'].map(MessageFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ManifestDataToJSON(json) {
        return ManifestDataToJSONTyped(json);
    }
    function ManifestDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'carrier_name': value['carrier_name'],
            'address': AddressDataToJSON(value['address']),
            'options': value['options'],
            'reference': value['reference'],
            'shipment_ids': value['shipment_ids'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the ManifestDocument interface.
     */
    function ManifestDocumentFromJSON(json) {
        return ManifestDocumentFromJSONTyped(json);
    }
    function ManifestDocumentFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'manifest': json['manifest'] == null ? undefined : json['manifest'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ManifestDetailsFromJSON(json) {
        return ManifestDetailsFromJSONTyped(json);
    }
    function ManifestDetailsFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'carrier_name': json['carrier_name'],
            'carrier_id': json['carrier_id'],
            'doc': json['doc'] == null ? undefined : ManifestDocumentFromJSON(json['doc']),
            'meta': json['meta'] == null ? undefined : json['meta'],
            'test_mode': json['test_mode'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ManifestListFromJSON(json) {
        return ManifestListFromJSONTyped(json);
    }
    function ManifestListFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'count': json['count'] == null ? undefined : json['count'],
            'next': json['next'] == null ? undefined : json['next'],
            'previous': json['previous'] == null ? undefined : json['previous'],
            'results': (json['results'].map(ManifestFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ManifestRequestToJSON(json) {
        return ManifestRequestToJSONTyped(json);
    }
    function ManifestRequestToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'carrier_name': value['carrier_name'],
            'address': AddressDataToJSON(value['address']),
            'options': value['options'],
            'reference': value['reference'],
            'shipment_identifiers': value['shipment_identifiers'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ManifestResponseFromJSON(json) {
        return ManifestResponseFromJSONTyped(json);
    }
    function ManifestResponseFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'messages': json['messages'] == null ? undefined : (json['messages'].map(MessageFromJSON)),
            'manifest': json['manifest'] == null ? undefined : ManifestDetailsFromJSON(json['manifest']),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the Operation interface.
     */
    function OperationFromJSON(json) {
        return OperationFromJSONTyped(json);
    }
    function OperationFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'operation': json['operation'],
            'success': json['success'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the OperationConfirmation interface.
     */
    function OperationConfirmationFromJSON(json) {
        return OperationConfirmationFromJSONTyped(json);
    }
    function OperationConfirmationFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'operation': json['operation'],
            'success': json['success'],
            'carrier_name': json['carrier_name'],
            'carrier_id': json['carrier_id'] == null ? undefined : json['carrier_id'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function OperationResponseFromJSON(json) {
        return OperationResponseFromJSONTyped(json);
    }
    function OperationResponseFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'messages': json['messages'] == null ? undefined : (json['messages'].map(MessageFromJSON)),
            'confirmation': json['confirmation'] == null ? undefined : OperationConfirmationFromJSON(json['confirmation']),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ParcelFromJSON(json) {
        return ParcelFromJSONTyped(json);
    }
    function ParcelFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'weight': json['weight'],
            'width': json['width'] == null ? undefined : json['width'],
            'height': json['height'] == null ? undefined : json['height'],
            'length': json['length'] == null ? undefined : json['length'],
            'packaging_type': json['packaging_type'] == null ? undefined : json['packaging_type'],
            'package_preset': json['package_preset'] == null ? undefined : json['package_preset'],
            'description': json['description'] == null ? undefined : json['description'],
            'content': json['content'] == null ? undefined : json['content'],
            'is_document': json['is_document'] == null ? undefined : json['is_document'],
            'weight_unit': json['weight_unit'],
            'dimension_unit': json['dimension_unit'] == null ? undefined : json['dimension_unit'],
            'items': json['items'] == null ? undefined : (json['items'].map(CommodityFromJSON)),
            'reference_number': json['reference_number'] == null ? undefined : json['reference_number'],
            'freight_class': json['freight_class'] == null ? undefined : json['freight_class'],
            'options': json['options'] == null ? undefined : json['options'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
        };
    }
    function ParcelToJSON(json) {
        return ParcelToJSONTyped(json);
    }
    function ParcelToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'id': value['id'],
            'weight': value['weight'],
            'width': value['width'],
            'height': value['height'],
            'length': value['length'],
            'packaging_type': value['packaging_type'],
            'package_preset': value['package_preset'],
            'description': value['description'],
            'content': value['content'],
            'is_document': value['is_document'],
            'weight_unit': value['weight_unit'],
            'dimension_unit': value['dimension_unit'],
            'items': value['items'] == null ? undefined : (value['items'].map(CommodityToJSON)),
            'reference_number': value['reference_number'],
            'freight_class': value['freight_class'],
            'options': value['options'],
            'object_type': value['object_type'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function RateFromJSON(json) {
        return RateFromJSONTyped(json);
    }
    function RateFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'carrier_name': json['carrier_name'],
            'carrier_id': json['carrier_id'],
            'currency': json['currency'] == null ? undefined : json['currency'],
            'service': json['service'] == null ? undefined : json['service'],
            'total_charge': json['total_charge'] == null ? undefined : json['total_charge'],
            'transit_days': json['transit_days'] == null ? undefined : json['transit_days'],
            'extra_charges': json['extra_charges'] == null ? undefined : (json['extra_charges'].map(ChargeFromJSON)),
            'estimated_delivery': json['estimated_delivery'] == null ? undefined : json['estimated_delivery'],
            'meta': json['meta'] == null ? undefined : json['meta'],
            'test_mode': json['test_mode'],
        };
    }
    function RateToJSON(json) {
        return RateToJSONTyped(json);
    }
    function RateToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'id': value['id'],
            'object_type': value['object_type'],
            'carrier_name': value['carrier_name'],
            'carrier_id': value['carrier_id'],
            'currency': value['currency'],
            'service': value['service'],
            'total_charge': value['total_charge'],
            'transit_days': value['transit_days'],
            'extra_charges': value['extra_charges'] == null ? undefined : (value['extra_charges'].map(ChargeToJSON)),
            'estimated_delivery': value['estimated_delivery'],
            'meta': value['meta'],
            'test_mode': value['test_mode'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ShipmentFromJSON(json) {
        return ShipmentFromJSONTyped(json);
    }
    function ShipmentFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'tracking_url': json['tracking_url'] == null ? undefined : json['tracking_url'],
            'shipper': AddressFromJSON(json['shipper']),
            'recipient': AddressFromJSON(json['recipient']),
            'return_address': json['return_address'] == null ? undefined : AddressDataFromJSON(json['return_address']),
            'billing_address': json['billing_address'] == null ? undefined : AddressDataFromJSON(json['billing_address']),
            'parcels': (json['parcels'].map(ParcelFromJSON)),
            'services': json['services'] == null ? undefined : json['services'],
            'options': json['options'] == null ? undefined : json['options'],
            'payment': json['payment'] == null ? undefined : PaymentFromJSON(json['payment']),
            'customs': json['customs'] == null ? undefined : CustomsFromJSON(json['customs']),
            'rates': json['rates'] == null ? undefined : (json['rates'].map(RateFromJSON)),
            'reference': json['reference'] == null ? undefined : json['reference'],
            'label_type': json['label_type'] == null ? undefined : json['label_type'],
            'carrier_ids': json['carrier_ids'] == null ? undefined : json['carrier_ids'],
            'tracker_id': json['tracker_id'] == null ? undefined : json['tracker_id'],
            'created_at': json['created_at'],
            'metadata': json['metadata'] == null ? undefined : json['metadata'],
            'messages': json['messages'] == null ? undefined : (json['messages'].map(MessageFromJSON)),
            'status': json['status'] == null ? undefined : json['status'],
            'carrier_name': json['carrier_name'] == null ? undefined : json['carrier_name'],
            'carrier_id': json['carrier_id'] == null ? undefined : json['carrier_id'],
            'tracking_number': json['tracking_number'] == null ? undefined : json['tracking_number'],
            'shipment_identifier': json['shipment_identifier'] == null ? undefined : json['shipment_identifier'],
            'selected_rate': json['selected_rate'] == null ? undefined : RateFromJSON(json['selected_rate']),
            'meta': json['meta'] == null ? undefined : json['meta'],
            'service': json['service'] == null ? undefined : json['service'],
            'selected_rate_id': json['selected_rate_id'] == null ? undefined : json['selected_rate_id'],
            'test_mode': json['test_mode'],
            'label_url': json['label_url'] == null ? undefined : json['label_url'],
            'invoice_url': json['invoice_url'] == null ? undefined : json['invoice_url'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function OrderFromJSON(json) {
        return OrderFromJSONTyped(json);
    }
    function OrderFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'order_id': json['order_id'],
            'order_date': json['order_date'] == null ? undefined : json['order_date'],
            'source': json['source'] == null ? undefined : json['source'],
            'status': json['status'] == null ? undefined : json['status'],
            'shipping_to': AddressFromJSON(json['shipping_to']),
            'shipping_from': json['shipping_from'] == null ? undefined : AddressFromJSON(json['shipping_from']),
            'billing_address': json['billing_address'] == null ? undefined : AddressDataFromJSON(json['billing_address']),
            'line_items': (json['line_items'].map(LineItemFromJSON)),
            'options': json['options'] == null ? undefined : json['options'],
            'meta': json['meta'] == null ? undefined : json['meta'],
            'metadata': json['metadata'] == null ? undefined : json['metadata'],
            'shipments': json['shipments'] == null ? undefined : (json['shipments'].map(ShipmentFromJSON)),
            'test_mode': json['test_mode'],
            'created_at': json['created_at'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function OrderListFromJSON(json) {
        return OrderListFromJSONTyped(json);
    }
    function OrderListFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'count': json['count'] == null ? undefined : json['count'],
            'next': json['next'] == null ? undefined : json['next'],
            'previous': json['previous'] == null ? undefined : json['previous'],
            'results': (json['results'].map(OrderFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the OrderUpdateData interface.
     */
    function OrderUpdateDataToJSON(json) {
        return OrderUpdateDataToJSONTyped(json);
    }
    function OrderUpdateDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'options': value['options'],
            'metadata': value['metadata'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ParcelListFromJSON(json) {
        return ParcelListFromJSONTyped(json);
    }
    function ParcelListFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'count': json['count'] == null ? undefined : json['count'],
            'next': json['next'] == null ? undefined : json['next'],
            'previous': json['previous'] == null ? undefined : json['previous'],
            'results': (json['results'].map(ParcelFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function PatchedAddressDataToJSON(json) {
        return PatchedAddressDataToJSONTyped(json);
    }
    function PatchedAddressDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'postal_code': value['postal_code'],
            'city': value['city'],
            'federal_tax_id': value['federal_tax_id'],
            'state_tax_id': value['state_tax_id'],
            'person_name': value['person_name'],
            'company_name': value['company_name'],
            'country_code': value['country_code'],
            'email': value['email'],
            'phone_number': value['phone_number'],
            'state_code': value['state_code'],
            'residential': value['residential'],
            'street_number': value['street_number'],
            'address_line1': value['address_line1'],
            'address_line2': value['address_line2'],
            'validate_location': value['validate_location'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function PatchedCarrierConnectionDataToJSON(json) {
        return PatchedCarrierConnectionDataToJSONTyped(json);
    }
    function PatchedCarrierConnectionDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'carrier_name': value['carrier_name'],
            'carrier_id': value['carrier_id'],
            'credentials': ConnectionCredentialsFieldToJSON(value['credentials']),
            'capabilities': value['capabilities'],
            'config': value['config'],
            'metadata': value['metadata'],
            'active': value['active'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function PatchedDocumentTemplateDataToJSON(json) {
        return PatchedDocumentTemplateDataToJSONTyped(json);
    }
    function PatchedDocumentTemplateDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'name': value['name'],
            'slug': value['slug'],
            'template': value['template'],
            'active': value['active'],
            'description': value['description'],
            'metadata': value['metadata'],
            'options': value['options'],
            'related_object': value['related_object'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function PatchedParcelDataToJSON(json) {
        return PatchedParcelDataToJSONTyped(json);
    }
    function PatchedParcelDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'weight': value['weight'],
            'width': value['width'],
            'height': value['height'],
            'length': value['length'],
            'packaging_type': value['packaging_type'],
            'package_preset': value['package_preset'],
            'description': value['description'],
            'content': value['content'],
            'is_document': value['is_document'],
            'weight_unit': value['weight_unit'],
            'dimension_unit': value['dimension_unit'],
            'items': value['items'] == null ? undefined : (value['items'].map(CommodityDataToJSON)),
            'reference_number': value['reference_number'],
            'freight_class': value['freight_class'],
            'options': value['options'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function PatchedWebhookDataToJSON(json) {
        return PatchedWebhookDataToJSONTyped(json);
    }
    function PatchedWebhookDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'url': value['url'],
            'description': value['description'],
            'enabled_events': value['enabled_events'],
            'disabled': value['disabled'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function PickupFromJSON(json) {
        return PickupFromJSONTyped(json);
    }
    function PickupFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'carrier_name': json['carrier_name'],
            'carrier_id': json['carrier_id'],
            'confirmation_number': json['confirmation_number'],
            'pickup_date': json['pickup_date'] == null ? undefined : json['pickup_date'],
            'pickup_charge': json['pickup_charge'] == null ? undefined : ChargeFromJSON(json['pickup_charge']),
            'ready_time': json['ready_time'] == null ? undefined : json['ready_time'],
            'closing_time': json['closing_time'] == null ? undefined : json['closing_time'],
            'metadata': json['metadata'] == null ? undefined : json['metadata'],
            'meta': json['meta'] == null ? undefined : json['meta'],
            'address': AddressFromJSON(json['address']),
            'parcels': (json['parcels'].map(ParcelFromJSON)),
            'instruction': json['instruction'] == null ? undefined : json['instruction'],
            'package_location': json['package_location'] == null ? undefined : json['package_location'],
            'options': json['options'] == null ? undefined : json['options'],
            'test_mode': json['test_mode'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the PickupCancelData interface.
     */
    function PickupCancelDataToJSON(json) {
        return PickupCancelDataToJSONTyped(json);
    }
    function PickupCancelDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'reason': value['reason'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function PickupCancelRequestToJSON(json) {
        return PickupCancelRequestToJSONTyped(json);
    }
    function PickupCancelRequestToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'confirmation_number': value['confirmation_number'],
            'address': AddressDataToJSON(value['address']),
            'pickup_date': value['pickup_date'],
            'reason': value['reason'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function PickupDataToJSON(json) {
        return PickupDataToJSONTyped(json);
    }
    function PickupDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'pickup_date': value['pickup_date'],
            'address': AddressDataToJSON(value['address']),
            'ready_time': value['ready_time'],
            'closing_time': value['closing_time'],
            'instruction': value['instruction'],
            'package_location': value['package_location'],
            'options': value['options'],
            'tracking_numbers': value['tracking_numbers'],
            'metadata': value['metadata'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function PickupListFromJSON(json) {
        return PickupListFromJSONTyped(json);
    }
    function PickupListFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'count': json['count'] == null ? undefined : json['count'],
            'next': json['next'] == null ? undefined : json['next'],
            'previous': json['previous'] == null ? undefined : json['previous'],
            'results': (json['results'].map(PickupFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function PickupRequestToJSON(json) {
        return PickupRequestToJSONTyped(json);
    }
    function PickupRequestToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'pickup_date': value['pickup_date'],
            'address': AddressDataToJSON(value['address']),
            'parcels': (value['parcels'].map(ParcelDataToJSON)),
            'ready_time': value['ready_time'],
            'closing_time': value['closing_time'],
            'instruction': value['instruction'],
            'package_location': value['package_location'],
            'options': value['options'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function PickupResponseFromJSON(json) {
        return PickupResponseFromJSONTyped(json);
    }
    function PickupResponseFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'messages': json['messages'] == null ? undefined : (json['messages'].map(MessageFromJSON)),
            'pickup': json['pickup'] == null ? undefined : PickupFromJSON(json['pickup']),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function PickupUpdateDataToJSON(json) {
        return PickupUpdateDataToJSONTyped(json);
    }
    function PickupUpdateDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'pickup_date': value['pickup_date'],
            'address': AddressDataToJSON(value['address']),
            'ready_time': value['ready_time'],
            'closing_time': value['closing_time'],
            'instruction': value['instruction'],
            'package_location': value['package_location'],
            'options': value['options'],
            'tracking_numbers': value['tracking_numbers'],
            'metadata': value['metadata'],
            'confirmation_number': value['confirmation_number'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function PickupUpdateRequestToJSON(json) {
        return PickupUpdateRequestToJSONTyped(json);
    }
    function PickupUpdateRequestToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'pickup_date': value['pickup_date'],
            'address': AddressToJSON(value['address']),
            'parcels': (value['parcels'].map(ParcelToJSON)),
            'confirmation_number': value['confirmation_number'],
            'ready_time': value['ready_time'],
            'closing_time': value['closing_time'],
            'instruction': value['instruction'],
            'package_location': value['package_location'],
            'options': value['options'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function RateRequestToJSON(json) {
        return RateRequestToJSONTyped(json);
    }
    function RateRequestToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'shipper': AddressDataToJSON(value['shipper']),
            'recipient': AddressDataToJSON(value['recipient']),
            'parcels': (value['parcels'].map(ParcelDataToJSON)),
            'services': value['services'],
            'options': value['options'],
            'reference': value['reference'],
            'carrier_ids': value['carrier_ids'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function RateResponseFromJSON(json) {
        return RateResponseFromJSONTyped(json);
    }
    function RateResponseFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'messages': json['messages'] == null ? undefined : (json['messages'].map(MessageFromJSON)),
            'rates': (json['rates'].map(RateFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the ShipmentCancelRequest interface.
     */
    function ShipmentCancelRequestToJSON(json) {
        return ShipmentCancelRequestToJSONTyped(json);
    }
    function ShipmentCancelRequestToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'shipment_identifier': value['shipment_identifier'],
            'service': value['service'],
            'carrier_id': value['carrier_id'],
            'options': value['options'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ShipmentDataToJSON(json) {
        return ShipmentDataToJSONTyped(json);
    }
    function ShipmentDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'recipient': AddressDataToJSON(value['recipient']),
            'shipper': AddressDataToJSON(value['shipper']),
            'return_address': AddressDataToJSON(value['return_address']),
            'billing_address': AddressDataToJSON(value['billing_address']),
            'parcels': (value['parcels'].map(ParcelDataToJSON)),
            'options': value['options'],
            'payment': PaymentToJSON(value['payment']),
            'customs': CustomsDataToJSON(value['customs']),
            'reference': value['reference'],
            'label_type': value['label_type'],
            'service': value['service'],
            'services': value['services'],
            'carrier_ids': value['carrier_ids'],
            'metadata': value['metadata'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ShipmentPurchaseDataToJSON(json) {
        return ShipmentPurchaseDataToJSONTyped(json);
    }
    function ShipmentPurchaseDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'selected_rate_id': value['selected_rate_id'],
            'label_type': value['label_type'],
            'payment': PaymentToJSON(value['payment']),
            'reference': value['reference'],
            'metadata': value['metadata'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the ShipmentRateData interface.
     */
    function ShipmentRateDataToJSON(json) {
        return ShipmentRateDataToJSONTyped(json);
    }
    function ShipmentRateDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'services': value['services'],
            'carrier_ids': value['carrier_ids'],
            'options': value['options'],
            'reference': value['reference'],
            'metadata': value['metadata'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ShipmentUpdateDataToJSON(json) {
        return ShipmentUpdateDataToJSONTyped(json);
    }
    function ShipmentUpdateDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'label_type': value['label_type'],
            'payment': PaymentToJSON(value['payment']),
            'options': value['options'],
            'reference': value['reference'],
            'metadata': value['metadata'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ShippingRequestToJSON(json) {
        return ShippingRequestToJSONTyped(json);
    }
    function ShippingRequestToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'recipient': AddressDataToJSON(value['recipient']),
            'shipper': AddressDataToJSON(value['shipper']),
            'return_address': AddressDataToJSON(value['return_address']),
            'billing_address': AddressDataToJSON(value['billing_address']),
            'parcels': (value['parcels'].map(ParcelDataToJSON)),
            'options': value['options'],
            'payment': PaymentToJSON(value['payment']),
            'customs': CustomsDataToJSON(value['customs']),
            'reference': value['reference'],
            'label_type': value['label_type'],
            'selected_rate_id': value['selected_rate_id'],
            'rates': (value['rates'].map(RateToJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ShippingResponseFromJSON(json) {
        return ShippingResponseFromJSONTyped(json);
    }
    function ShippingResponseFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'tracking_url': json['tracking_url'] == null ? undefined : json['tracking_url'],
            'shipper': AddressFromJSON(json['shipper']),
            'recipient': AddressFromJSON(json['recipient']),
            'return_address': json['return_address'] == null ? undefined : AddressDataFromJSON(json['return_address']),
            'billing_address': json['billing_address'] == null ? undefined : AddressDataFromJSON(json['billing_address']),
            'parcels': (json['parcels'].map(ParcelFromJSON)),
            'services': json['services'] == null ? undefined : json['services'],
            'options': json['options'] == null ? undefined : json['options'],
            'payment': json['payment'] == null ? undefined : PaymentFromJSON(json['payment']),
            'customs': json['customs'] == null ? undefined : CustomsFromJSON(json['customs']),
            'rates': json['rates'] == null ? undefined : (json['rates'].map(RateFromJSON)),
            'reference': json['reference'] == null ? undefined : json['reference'],
            'label_type': json['label_type'] == null ? undefined : json['label_type'],
            'carrier_ids': json['carrier_ids'] == null ? undefined : json['carrier_ids'],
            'tracker_id': json['tracker_id'] == null ? undefined : json['tracker_id'],
            'created_at': json['created_at'],
            'metadata': json['metadata'] == null ? undefined : json['metadata'],
            'messages': json['messages'] == null ? undefined : (json['messages'].map(MessageFromJSON)),
            'status': json['status'] == null ? undefined : json['status'],
            'carrier_name': json['carrier_name'] == null ? undefined : json['carrier_name'],
            'carrier_id': json['carrier_id'] == null ? undefined : json['carrier_id'],
            'tracking_number': json['tracking_number'] == null ? undefined : json['tracking_number'],
            'shipment_identifier': json['shipment_identifier'] == null ? undefined : json['shipment_identifier'],
            'selected_rate': json['selected_rate'] == null ? undefined : RateFromJSON(json['selected_rate']),
            'docs': json['docs'] == null ? undefined : DocumentsFromJSON(json['docs']),
            'meta': json['meta'] == null ? undefined : json['meta'],
            'service': json['service'] == null ? undefined : json['service'],
            'selected_rate_id': json['selected_rate_id'] == null ? undefined : json['selected_rate_id'],
            'test_mode': json['test_mode'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the TrackingEvent interface.
     */
    function TrackingEventFromJSON(json) {
        return TrackingEventFromJSONTyped(json);
    }
    function TrackingEventFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'date': json['date'] == null ? undefined : json['date'],
            'description': json['description'] == null ? undefined : json['description'],
            'location': json['location'] == null ? undefined : json['location'],
            'code': json['code'] == null ? undefined : json['code'],
            'time': json['time'] == null ? undefined : json['time'],
            'latitude': json['latitude'] == null ? undefined : json['latitude'],
            'longitude': json['longitude'] == null ? undefined : json['longitude'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function TrackerDetailsFromJSON(json) {
        return TrackerDetailsFromJSONTyped(json);
    }
    function TrackerDetailsFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'carrier_name': json['carrier_name'],
            'carrier_id': json['carrier_id'],
            'tracking_number': json['tracking_number'],
            'info': json['info'] == null ? undefined : TrackingInfoFromJSON(json['info']),
            'events': json['events'] == null ? undefined : (json['events'].map(TrackingEventFromJSON)),
            'delivered': json['delivered'] == null ? undefined : json['delivered'],
            'test_mode': json['test_mode'],
            'status': json['status'] == null ? undefined : json['status'],
            'estimated_delivery': json['estimated_delivery'] == null ? undefined : json['estimated_delivery'],
            'meta': json['meta'] == null ? undefined : json['meta'],
            'images': json['images'] == null ? undefined : ImagesFromJSON(json['images']),
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'metadata': json['metadata'] == null ? undefined : json['metadata'],
            'messages': json['messages'] == null ? undefined : (json['messages'].map(MessageFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function TrackingStatusFromJSON(json) {
        return TrackingStatusFromJSONTyped(json);
    }
    function TrackingStatusFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'carrier_name': json['carrier_name'],
            'carrier_id': json['carrier_id'],
            'tracking_number': json['tracking_number'],
            'info': json['info'] == null ? undefined : TrackingInfoFromJSON(json['info']),
            'events': json['events'] == null ? undefined : (json['events'].map(TrackingEventFromJSON)),
            'delivered': json['delivered'] == null ? undefined : json['delivered'],
            'test_mode': json['test_mode'],
            'status': json['status'] == null ? undefined : json['status'],
            'estimated_delivery': json['estimated_delivery'] == null ? undefined : json['estimated_delivery'],
            'meta': json['meta'] == null ? undefined : json['meta'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'metadata': json['metadata'] == null ? undefined : json['metadata'],
            'messages': json['messages'] == null ? undefined : (json['messages'].map(MessageFromJSON)),
            'delivery_image_url': json['delivery_image_url'] == null ? undefined : json['delivery_image_url'],
            'signature_image_url': json['signature_image_url'] == null ? undefined : json['signature_image_url'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function TrackerListFromJSON(json) {
        return TrackerListFromJSONTyped(json);
    }
    function TrackerListFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'count': json['count'] == null ? undefined : json['count'],
            'next': json['next'] == null ? undefined : json['next'],
            'previous': json['previous'] == null ? undefined : json['previous'],
            'results': (json['results'].map(TrackingStatusFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function TrackerUpdateDataToJSON(json) {
        return TrackerUpdateDataToJSONTyped(json);
    }
    function TrackerUpdateDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'info': TrackingInfoToJSON(value['info']),
            'metadata': value['metadata'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function TrackingResponseFromJSON(json) {
        return TrackingResponseFromJSONTyped(json);
    }
    function TrackingResponseFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'messages': json['messages'] == null ? undefined : (json['messages'].map(MessageFromJSON)),
            'tracking': json['tracking'] == null ? undefined : TrackerDetailsFromJSON(json['tracking']),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function WebhookFromJSON(json) {
        return WebhookFromJSONTyped(json);
    }
    function WebhookFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'id': json['id'] == null ? undefined : json['id'],
            'url': json['url'],
            'description': json['description'] == null ? undefined : json['description'],
            'enabled_events': json['enabled_events'],
            'disabled': json['disabled'] == null ? undefined : json['disabled'],
            'object_type': json['object_type'] == null ? undefined : json['object_type'],
            'last_event_at': json['last_event_at'] == null ? undefined : (new Date(json['last_event_at'])),
            'secret': json['secret'],
            'test_mode': json['test_mode'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * @export
     */
    function WebhookDataToJSON(json) {
        return WebhookDataToJSONTyped(json);
    }
    function WebhookDataToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'url': value['url'],
            'description': value['description'],
            'enabled_events': value['enabled_events'],
            'disabled': value['disabled'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function WebhookListFromJSON(json) {
        return WebhookListFromJSONTyped(json);
    }
    function WebhookListFromJSONTyped(json, ignoreDiscriminator) {
        if (json == null) {
            return json;
        }
        return {
            'count': json['count'] == null ? undefined : json['count'],
            'next': json['next'] == null ? undefined : json['next'],
            'previous': json['previous'] == null ? undefined : json['previous'],
            'results': (json['results'].map(WebhookFromJSON)),
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     * Check if a given object implements the WebhookTestRequest interface.
     */
    function WebhookTestRequestToJSON(json) {
        return WebhookTestRequestToJSONTyped(json);
    }
    function WebhookTestRequestToJSONTyped(value, ignoreDiscriminator) {
        if (value == null) {
            return value;
        }
        return {
            'payload': value['payload'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['addressData'] == null) {
                                throw new RequiredError('addressData', 'Required parameter "addressData" was null or undefined when calling create().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/addresses";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: AddressDataToJSON(requestParameters['addressData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling discard().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/addresses/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/addresses";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling retrieve().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/addresses/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling update().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/addresses/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'PATCH',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PatchedAddressDataToJSON(requestParameters['patchedAddressData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     *
     */
    var APIApi = /** @class */ (function (_super) {
        __extends(APIApi, _super);
        function APIApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Data References
         */
        APIApi.prototype.dataRaw = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, urlPath, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            headerParameters = {};
                            urlPath = "/v1/references";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
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
         * Instance Metadata
         */
        APIApi.prototype.pingRaw = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, urlPath, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            headerParameters = {};
                            urlPath = "/";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
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
        return APIApi;
    }(BaseAPI));

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     *
     */
    var CarriersApi = /** @class */ (function (_super) {
        __extends(CarriersApi, _super);
        function CarriersApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Retrieve a carrier\'s details
         * Get carrier details
         */
        CarriersApi.prototype.getDetailsRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, urlPath, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters['carrierName'] == null) {
                                throw new RequiredError('carrierName', 'Required parameter "carrierName" was null or undefined when calling getDetails().');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            urlPath = "/v1/carriers/{carrier_name}";
                            urlPath = urlPath.replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters['carrierName'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return CarrierDetailsFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve a carrier\'s details
         * Get carrier details
         */
        CarriersApi.prototype.getDetails = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.getDetailsRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve a carrier\'s options
         * Get carrier options
         */
        CarriersApi.prototype.getOptionsRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, urlPath, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters['carrierName'] == null) {
                                throw new RequiredError('carrierName', 'Required parameter "carrierName" was null or undefined when calling getOptions().');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            urlPath = "/v1/carriers/{carrier_name}/options";
                            urlPath = urlPath.replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters['carrierName'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
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
         * Retrieve a carrier\'s options
         * Get carrier options
         */
        CarriersApi.prototype.getOptions = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.getOptionsRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve a carrier\'s services
         * Get carrier services
         */
        CarriersApi.prototype.getServicesRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, urlPath, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            if (requestParameters['carrierName'] == null) {
                                throw new RequiredError('carrierName', 'Required parameter "carrierName" was null or undefined when calling getServices().');
                            }
                            queryParameters = {};
                            headerParameters = {};
                            urlPath = "/v1/carriers/{carrier_name}/services";
                            urlPath = urlPath.replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters['carrierName'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
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
        CarriersApi.prototype.listRaw = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, urlPath, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            headerParameters = {};
                            urlPath = "/v1/carriers";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return jsonValue.map(CarrierDetailsFromJSON); })];
                    }
                });
            });
        };
        /**
         * Returns the list of configured carriers
         * List all carriers
         */
        CarriersApi.prototype.list = function (initOverrides) {
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
        return CarriersApi;
    }(BaseAPI));

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     *
     */
    var ConnectionsApi = /** @class */ (function (_super) {
        __extends(ConnectionsApi, _super);
        function ConnectionsApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Add a new carrier connection.
         * Add a carrier connection
         */
        ConnectionsApi.prototype.addRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['carrierConnectionData'] == null) {
                                throw new RequiredError('carrierConnectionData', 'Required parameter "carrierConnectionData" was null or undefined when calling add().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/connections";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: CarrierConnectionDataToJSON(requestParameters['carrierConnectionData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return CarrierConnectionFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Add a new carrier connection.
         * Add a carrier connection
         */
        ConnectionsApi.prototype.add = function (requestParameters, initOverrides) {
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
         * Retrieve all carrier connections
         * List carrier connections
         */
        ConnectionsApi.prototype.listRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters['active'] != null) {
                                queryParameters['active'] = requestParameters['active'];
                            }
                            if (requestParameters['carrierName'] != null) {
                                queryParameters['carrier_name'] = requestParameters['carrierName'];
                            }
                            if (requestParameters['metadataKey'] != null) {
                                queryParameters['metadata_key'] = requestParameters['metadataKey'];
                            }
                            if (requestParameters['metadataValue'] != null) {
                                queryParameters['metadata_value'] = requestParameters['metadataValue'];
                            }
                            if (requestParameters['systemOnly'] != null) {
                                queryParameters['system_only'] = requestParameters['systemOnly'];
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/connections";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return CarrierConnectionListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all carrier connections
         * List carrier connections
         */
        ConnectionsApi.prototype.list = function () {
            return __awaiter(this, arguments, void 0, function (requestParameters, initOverrides) {
                var response;
                if (requestParameters === void 0) { requestParameters = {}; }
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
         * Remove a carrier connection.
         * Remove a carrier connection
         */
        ConnectionsApi.prototype.removeRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling remove().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/connections/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return CarrierConnectionFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Remove a carrier connection.
         * Remove a carrier connection
         */
        ConnectionsApi.prototype.remove = function (requestParameters, initOverrides) {
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
         * Retrieve carrier connection.
         * Retrieve a connection
         */
        ConnectionsApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling retrieve().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/connections/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return CarrierConnectionFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve carrier connection.
         * Retrieve a connection
         */
        ConnectionsApi.prototype.retrieve = function (requestParameters, initOverrides) {
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
         * Update a carrier connection.
         * Update a connection
         */
        ConnectionsApi.prototype.updateRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling update().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/connections/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'PATCH',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PatchedCarrierConnectionDataToJSON(requestParameters['patchedCarrierConnectionData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return CarrierConnectionFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Update a carrier connection.
         * Update a connection
         */
        ConnectionsApi.prototype.update = function (requestParameters, initOverrides) {
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
        return ConnectionsApi;
    }(BaseAPI));

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['parcelData'] == null) {
                                throw new RequiredError('parcelData', 'Required parameter "parcelData" was null or undefined when calling create().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/parcels";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ParcelDataToJSON(requestParameters['parcelData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling discard().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/parcels/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/parcels";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling retrieve().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/parcels/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling update().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/parcels/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'PATCH',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PatchedParcelDataToJSON(requestParameters['patchedParcelData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling cancel().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/pickups/{id}/cancel";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupCancelDataToJSON(requestParameters['pickupCancelData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/pickups";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling retrieve().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/pickups/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['carrierName'] == null) {
                                throw new RequiredError('carrierName', 'Required parameter "carrierName" was null or undefined when calling schedule().');
                            }
                            if (requestParameters['pickupData'] == null) {
                                throw new RequiredError('pickupData', 'Required parameter "pickupData" was null or undefined when calling schedule().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/pickups/{carrier_name}/schedule";
                            urlPath = urlPath.replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters['carrierName'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupDataToJSON(requestParameters['pickupData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling update().');
                            }
                            if (requestParameters['pickupUpdateData'] == null) {
                                throw new RequiredError('pickupUpdateData', 'Required parameter "pickupUpdateData" was null or undefined when calling update().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/pickups/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupUpdateDataToJSON(requestParameters['pickupUpdateData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['shippingRequest'] == null) {
                                throw new RequiredError('shippingRequest', 'Required parameter "shippingRequest" was null or undefined when calling buyLabel().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/proxy/shipping";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShippingRequestToJSON(requestParameters['shippingRequest']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['carrierName'] == null) {
                                throw new RequiredError('carrierName', 'Required parameter "carrierName" was null or undefined when calling cancelPickup().');
                            }
                            if (requestParameters['pickupCancelRequest'] == null) {
                                throw new RequiredError('pickupCancelRequest', 'Required parameter "pickupCancelRequest" was null or undefined when calling cancelPickup().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/proxy/pickups/{carrier_name}/cancel";
                            urlPath = urlPath.replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters['carrierName'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupCancelRequestToJSON(requestParameters['pickupCancelRequest']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['rateRequest'] == null) {
                                throw new RequiredError('rateRequest', 'Required parameter "rateRequest" was null or undefined when calling fetchRates().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/proxy/rates";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: RateRequestToJSON(requestParameters['rateRequest']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
         *  Some carriers require shipment manifests to be created for pickups and dropoff. Creating a manifest for a shipment also kicks off billing as a commitment or confirmation of the shipment.
         * Create a manifest
         */
        ProxyApi.prototype.generateManifestRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['manifestRequest'] == null) {
                                throw new RequiredError('manifestRequest', 'Required parameter "manifestRequest" was null or undefined when calling generateManifest().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/proxy/manifest";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ManifestRequestToJSON(requestParameters['manifestRequest']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ManifestResponseFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         *  Some carriers require shipment manifests to be created for pickups and dropoff. Creating a manifest for a shipment also kicks off billing as a commitment or confirmation of the shipment.
         * Create a manifest
         */
        ProxyApi.prototype.generateManifest = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.generateManifestRaw(requestParameters, initOverrides)];
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['trackingData'] == null) {
                                throw new RequiredError('trackingData', 'Required parameter "trackingData" was null or undefined when calling getTracking().');
                            }
                            queryParameters = {};
                            if (requestParameters['hub'] != null) {
                                queryParameters['hub'] = requestParameters['hub'];
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/proxy/tracking";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: TrackingDataToJSON(requestParameters['trackingData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['carrierName'] == null) {
                                throw new RequiredError('carrierName', 'Required parameter "carrierName" was null or undefined when calling schedulePickup().');
                            }
                            if (requestParameters['pickupRequest'] == null) {
                                throw new RequiredError('pickupRequest', 'Required parameter "pickupRequest" was null or undefined when calling schedulePickup().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/proxy/pickups/{carrier_name}";
                            urlPath = urlPath.replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters['carrierName'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupRequestToJSON(requestParameters['pickupRequest']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['carrierName'] == null) {
                                throw new RequiredError('carrierName', 'Required parameter "carrierName" was null or undefined when calling trackShipment().');
                            }
                            if (requestParameters['trackingNumber'] == null) {
                                throw new RequiredError('trackingNumber', 'Required parameter "trackingNumber" was null or undefined when calling trackShipment().');
                            }
                            queryParameters = {};
                            if (requestParameters['hub'] != null) {
                                queryParameters['hub'] = requestParameters['hub'];
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/proxy/tracking/{carrier_name}/{tracking_number}";
                            urlPath = urlPath.replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters['carrierName'])));
                            urlPath = urlPath.replace("{".concat("tracking_number", "}"), encodeURIComponent(String(requestParameters['trackingNumber'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['carrierName'] == null) {
                                throw new RequiredError('carrierName', 'Required parameter "carrierName" was null or undefined when calling updatePickup().');
                            }
                            if (requestParameters['pickupUpdateRequest'] == null) {
                                throw new RequiredError('pickupUpdateRequest', 'Required parameter "pickupUpdateRequest" was null or undefined when calling updatePickup().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/proxy/pickups/{carrier_name}/update";
                            urlPath = urlPath.replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters['carrierName'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PickupUpdateRequestToJSON(requestParameters['pickupUpdateRequest']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['carrierName'] == null) {
                                throw new RequiredError('carrierName', 'Required parameter "carrierName" was null or undefined when calling voidLabel().');
                            }
                            if (requestParameters['shipmentCancelRequest'] == null) {
                                throw new RequiredError('shipmentCancelRequest', 'Required parameter "shipmentCancelRequest" was null or undefined when calling voidLabel().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/proxy/shipping/{carrier_name}/cancel";
                            urlPath = urlPath.replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters['carrierName'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentCancelRequestToJSON(requestParameters['shipmentCancelRequest']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling cancel().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/shipments/{id}/cancel";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['shipmentData'] == null) {
                                throw new RequiredError('shipmentData', 'Required parameter "shipmentData" was null or undefined when calling create().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/shipments";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentDataToJSON(requestParameters['shipmentData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters['address'] != null) {
                                queryParameters['address'] = requestParameters['address'];
                            }
                            if (requestParameters['carrierName'] != null) {
                                queryParameters['carrier_name'] = requestParameters['carrierName'];
                            }
                            if (requestParameters['createdAfter'] != null) {
                                queryParameters['created_after'] = requestParameters['createdAfter'].toISOString();
                            }
                            if (requestParameters['createdBefore'] != null) {
                                queryParameters['created_before'] = requestParameters['createdBefore'].toISOString();
                            }
                            if (requestParameters['hasManifest'] != null) {
                                queryParameters['has_manifest'] = requestParameters['hasManifest'];
                            }
                            if (requestParameters['hasTracker'] != null) {
                                queryParameters['has_tracker'] = requestParameters['hasTracker'];
                            }
                            if (requestParameters['id'] != null) {
                                queryParameters['id'] = requestParameters['id'];
                            }
                            if (requestParameters['keyword'] != null) {
                                queryParameters['keyword'] = requestParameters['keyword'];
                            }
                            if (requestParameters['metaKey'] != null) {
                                queryParameters['meta_key'] = requestParameters['metaKey'];
                            }
                            if (requestParameters['metaValue'] != null) {
                                queryParameters['meta_value'] = requestParameters['metaValue'];
                            }
                            if (requestParameters['metadataKey'] != null) {
                                queryParameters['metadata_key'] = requestParameters['metadataKey'];
                            }
                            if (requestParameters['metadataValue'] != null) {
                                queryParameters['metadata_value'] = requestParameters['metadataValue'];
                            }
                            if (requestParameters['optionKey'] != null) {
                                queryParameters['option_key'] = requestParameters['optionKey'];
                            }
                            if (requestParameters['optionValue'] != null) {
                                queryParameters['option_value'] = requestParameters['optionValue'];
                            }
                            if (requestParameters['reference'] != null) {
                                queryParameters['reference'] = requestParameters['reference'];
                            }
                            if (requestParameters['service'] != null) {
                                queryParameters['service'] = requestParameters['service'];
                            }
                            if (requestParameters['status'] != null) {
                                queryParameters['status'] = requestParameters['status'];
                            }
                            if (requestParameters['trackingNumber'] != null) {
                                queryParameters['tracking_number'] = requestParameters['trackingNumber'];
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/shipments";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ShipmentFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all shipments.
         * List all shipments
         */
        ShipmentsApi.prototype.list = function () {
            return __awaiter(this, arguments, void 0, function (requestParameters, initOverrides) {
                var response;
                if (requestParameters === void 0) { requestParameters = {}; }
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling purchase().');
                            }
                            if (requestParameters['shipmentPurchaseData'] == null) {
                                throw new RequiredError('shipmentPurchaseData', 'Required parameter "shipmentPurchaseData" was null or undefined when calling purchase().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/shipments/{id}/purchase";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentPurchaseDataToJSON(requestParameters['shipmentPurchaseData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling rates().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/shipments/{id}/rates";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentRateDataToJSON(requestParameters['shipmentRateData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling retrieve().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/shipments/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling update().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/shipments/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'PUT',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ShipmentUpdateDataToJSON(requestParameters['shipmentUpdateData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['trackingData'] == null) {
                                throw new RequiredError('trackingData', 'Required parameter "trackingData" was null or undefined when calling add().');
                            }
                            queryParameters = {};
                            if (requestParameters['hub'] != null) {
                                queryParameters['hub'] = requestParameters['hub'];
                            }
                            if (requestParameters['pendingPickup'] != null) {
                                queryParameters['pending_pickup'] = requestParameters['pendingPickup'];
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/trackers";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: TrackingDataToJSON(requestParameters['trackingData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['carrierName'] == null) {
                                throw new RequiredError('carrierName', 'Required parameter "carrierName" was null or undefined when calling create().');
                            }
                            if (requestParameters['carrierName2'] == null) {
                                throw new RequiredError('carrierName2', 'Required parameter "carrierName2" was null or undefined when calling create().');
                            }
                            if (requestParameters['trackingNumber'] == null) {
                                throw new RequiredError('trackingNumber', 'Required parameter "trackingNumber" was null or undefined when calling create().');
                            }
                            queryParameters = {};
                            if (requestParameters['carrierName2'] != null) {
                                queryParameters['carrier_name'] = requestParameters['carrierName2'];
                            }
                            if (requestParameters['hub'] != null) {
                                queryParameters['hub'] = requestParameters['hub'];
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/trackers/{carrier_name}/{tracking_number}";
                            urlPath = urlPath.replace("{".concat("carrier_name", "}"), encodeURIComponent(String(requestParameters['carrierName'])));
                            urlPath = urlPath.replace("{".concat("tracking_number", "}"), encodeURIComponent(String(requestParameters['trackingNumber'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters['carrierName'] != null) {
                                queryParameters['carrier_name'] = requestParameters['carrierName'];
                            }
                            if (requestParameters['createdAfter'] != null) {
                                queryParameters['created_after'] = requestParameters['createdAfter'].toISOString();
                            }
                            if (requestParameters['createdBefore'] != null) {
                                queryParameters['created_before'] = requestParameters['createdBefore'].toISOString();
                            }
                            if (requestParameters['status'] != null) {
                                queryParameters['status'] = requestParameters['status'];
                            }
                            if (requestParameters['trackingNumber'] != null) {
                                queryParameters['tracking_number'] = requestParameters['trackingNumber'];
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/trackers";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackerListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all shipment trackers.
         * List all package trackers
         */
        TrackersApi.prototype.list = function () {
            return __awaiter(this, arguments, void 0, function (requestParameters, initOverrides) {
                var response;
                if (requestParameters === void 0) { requestParameters = {}; }
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['idOrTrackingNumber'] == null) {
                                throw new RequiredError('idOrTrackingNumber', 'Required parameter "idOrTrackingNumber" was null or undefined when calling remove().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/trackers/{id_or_tracking_number}";
                            urlPath = urlPath.replace("{".concat("id_or_tracking_number", "}"), encodeURIComponent(String(requestParameters['idOrTrackingNumber'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
        TrackersApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['idOrTrackingNumber'] == null) {
                                throw new RequiredError('idOrTrackingNumber', 'Required parameter "idOrTrackingNumber" was null or undefined when calling retrieve().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/trackers/{id_or_tracking_number}";
                            urlPath = urlPath.replace("{".concat("id_or_tracking_number", "}"), encodeURIComponent(String(requestParameters['idOrTrackingNumber'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return TrackingStatusFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve a package tracker
         * Retrieves a package tracker
         */
        TrackersApi.prototype.retrieve = function (requestParameters, initOverrides) {
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
         * Mixin to log requests
         * Update tracker data
         */
        TrackersApi.prototype.updateRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['idOrTrackingNumber'] == null) {
                                throw new RequiredError('idOrTrackingNumber', 'Required parameter "idOrTrackingNumber" was null or undefined when calling update().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/trackers/{id_or_tracking_number}";
                            urlPath = urlPath.replace("{".concat("id_or_tracking_number", "}"), encodeURIComponent(String(requestParameters['idOrTrackingNumber'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'PUT',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: TrackerUpdateDataToJSON(requestParameters['trackerUpdateData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['webhookData'] == null) {
                                throw new RequiredError('webhookData', 'Required parameter "webhookData" was null or undefined when calling create().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/webhooks";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: WebhookDataToJSON(requestParameters['webhookData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/webhooks";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling remove().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/webhooks/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling retrieve().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/webhooks/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling test().');
                            }
                            if (requestParameters['webhookTestRequest'] == null) {
                                throw new RequiredError('webhookTestRequest', 'Required parameter "webhookTestRequest" was null or undefined when calling test().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/webhooks/{id}/test";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: WebhookTestRequestToJSON(requestParameters['webhookTestRequest']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling update().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/webhooks/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'PATCH',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PatchedWebhookDataToJSON(requestParameters['patchedWebhookData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling cancel().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/orders/{id}/cancel";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['orderData'] == null) {
                                throw new RequiredError('orderData', 'Required parameter "orderData" was null or undefined when calling create().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/orders";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: OrderDataToJSON(requestParameters['orderData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling dismiss().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/orders/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/orders";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling retrieve().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/orders/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling update().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/orders/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'PUT',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: OrderUpdateDataToJSON(requestParameters['orderUpdateData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     *
     */
    var BatchesApi = /** @class */ (function (_super) {
        __extends(BatchesApi, _super);
        function BatchesApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Create order batch. `Beta`
         * Create order batch
         */
        BatchesApi.prototype.createOrdersRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['batchOrderData'] == null) {
                                throw new RequiredError('batchOrderData', 'Required parameter "batchOrderData" was null or undefined when calling createOrders().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/batches/orders";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: BatchOrderDataToJSON(requestParameters['batchOrderData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return BatchOperationFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create order batch. `Beta`
         * Create order batch
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
         * Create shipment batch. `Beta`
         * Create shipment batch
         */
        BatchesApi.prototype.createShipmentsRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['batchShipmentData'] == null) {
                                throw new RequiredError('batchShipmentData', 'Required parameter "batchShipmentData" was null or undefined when calling createShipments().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/batches/shipments";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: BatchShipmentDataToJSON(requestParameters['batchShipmentData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return BatchOperationFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create shipment batch. `Beta`
         * Create shipment batch
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
         * Create tracker batch. `Beta`
         * Create tracker batch
         */
        BatchesApi.prototype.createTrackersRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['batchTrackerData'] == null) {
                                throw new RequiredError('batchTrackerData', 'Required parameter "batchTrackerData" was null or undefined when calling createTrackers().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/batches/trackers";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: BatchTrackerDataToJSON(requestParameters['batchTrackerData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return BatchOperationFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create tracker batch. `Beta`
         * Create tracker batch
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
         * Export data files
         */
        BatchesApi.prototype.exportFileRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['exportFormat'] == null) {
                                throw new RequiredError('exportFormat', 'Required parameter "exportFormat" was null or undefined when calling exportFile().');
                            }
                            if (requestParameters['resourceType'] == null) {
                                throw new RequiredError('resourceType', 'Required parameter "resourceType" was null or undefined when calling exportFile().');
                            }
                            queryParameters = {};
                            if (requestParameters['dataTemplate'] != null) {
                                queryParameters['data_template'] = requestParameters['dataTemplate'];
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/batches/data/export/{resource_type}.{export_format}";
                            urlPath = urlPath.replace("{".concat("export_format", "}"), encodeURIComponent(String(requestParameters['exportFormat'])));
                            urlPath = urlPath.replace("{".concat("resource_type", "}"), encodeURIComponent(String(requestParameters['resourceType'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new BlobApiResponse(response)];
                    }
                });
            });
        };
        /**
         * Export data files
         */
        BatchesApi.prototype.exportFile = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.exportFileRaw(requestParameters, initOverrides)];
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, consumes, canConsumeForm$1, formParams, useForm, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters['dataFile'] != null) {
                                queryParameters['data_file'] = requestParameters['dataFile'];
                            }
                            if (requestParameters['dataTemplate'] != null) {
                                queryParameters['data_template'] = requestParameters['dataTemplate'];
                            }
                            if (requestParameters['resourceType'] != null) {
                                queryParameters['resource_type'] = requestParameters['resourceType'];
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
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
                            if (requestParameters['resourceType2'] != null) {
                                formParams.append('resource_type', requestParameters['resourceType2']);
                            }
                            if (requestParameters['dataTemplate2'] != null) {
                                formParams.append('data_template', requestParameters['dataTemplate2']);
                            }
                            if (requestParameters['dataFile2'] != null) {
                                formParams.append('data_file', requestParameters['dataFile2']);
                            }
                            urlPath = "/v1/batches/data/import";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: formParams,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return BatchOperationFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Import csv, xls and xlsx data files for: `Beta`<br/> - trackers data - orders data - shipments data - billing data (soon)<br/><br/> **This operation will return a batch operation that you can poll to follow the import progression.**
         * Import data files
         */
        BatchesApi.prototype.importFile = function () {
            return __awaiter(this, arguments, void 0, function (requestParameters, initOverrides) {
                var response;
                if (requestParameters === void 0) { requestParameters = {}; }
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/batches/operations";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling retrieve().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/batches/operations/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     *
     */
    var DocumentsApi = /** @class */ (function (_super) {
        __extends(DocumentsApi, _super);
        function DocumentsApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Create a new template.
         * Create a template
         */
        DocumentsApi.prototype.createRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['documentTemplateData'] == null) {
                                throw new RequiredError('documentTemplateData', 'Required parameter "documentTemplateData" was null or undefined when calling create().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/documents/templates";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: DocumentTemplateDataToJSON(requestParameters['documentTemplateData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return DocumentTemplateFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create a new template.
         * Create a template
         */
        DocumentsApi.prototype.create = function (requestParameters, initOverrides) {
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
         * Delete a template.
         * Delete a template
         */
        DocumentsApi.prototype.discardRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling discard().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/documents/templates/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'DELETE',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return DocumentTemplateFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Delete a template.
         * Delete a template
         */
        DocumentsApi.prototype.discard = function (requestParameters, initOverrides) {
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
         * Generate any document. This API is designed to be used to generate GS1 labels, invoices and any document that requires external data.
         * Generate a document
         */
        DocumentsApi.prototype.generateDocumentRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/documents/generate";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: DocumentDataToJSON(requestParameters['documentData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return GeneratedDocumentFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Generate any document. This API is designed to be used to generate GS1 labels, invoices and any document that requires external data.
         * Generate a document
         */
        DocumentsApi.prototype.generateDocument = function () {
            return __awaiter(this, arguments, void 0, function (requestParameters, initOverrides) {
                var response;
                if (requestParameters === void 0) { requestParameters = {}; }
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.generateDocumentRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * Retrieve all templates.
         * List all templates
         */
        DocumentsApi.prototype.listRaw = function (initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/documents/templates";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return DocumentTemplateListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all templates.
         * List all templates
         */
        DocumentsApi.prototype.list = function (initOverrides) {
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
         * Retrieve a template.
         * Retrieve a template
         */
        DocumentsApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling retrieve().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/documents/templates/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return DocumentTemplateFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve a template.
         * Retrieve a template
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
         * Retrieve a shipping document upload record.
         * Retrieve upload record
         */
        DocumentsApi.prototype.retrieveUploadRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling retrieveUpload().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/documents/uploads/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return DocumentUploadRecordFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve a shipping document upload record.
         * Retrieve upload record
         */
        DocumentsApi.prototype.retrieveUpload = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.retrieveUploadRaw(requestParameters, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [4 /*yield*/, response.value()];
                        case 2: return [2 /*return*/, _a.sent()];
                    }
                });
            });
        };
        /**
         * update a template.
         * Update a template
         */
        DocumentsApi.prototype.updateRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling update().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/documents/templates/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'PATCH',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: PatchedDocumentTemplateDataToJSON(requestParameters['patchedDocumentTemplateData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return DocumentTemplateFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * update a template.
         * Update a template
         */
        DocumentsApi.prototype.update = function (requestParameters, initOverrides) {
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
        /**
         * Upload a shipping document.
         * Upload documents
         */
        DocumentsApi.prototype.uploadRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['documentUploadData'] == null) {
                                throw new RequiredError('documentUploadData', 'Required parameter "documentUploadData" was null or undefined when calling upload().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/documents/uploads";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: DocumentUploadDataToJSON(requestParameters['documentUploadData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
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
        /**
         * Retrieve all shipping document upload records.
         * List all upload records
         */
        DocumentsApi.prototype.uploadsRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters['createdAfter'] != null) {
                                queryParameters['created_after'] = requestParameters['createdAfter'].toISOString();
                            }
                            if (requestParameters['createdBefore'] != null) {
                                queryParameters['created_before'] = requestParameters['createdBefore'].toISOString();
                            }
                            if (requestParameters['shipmentId'] != null) {
                                queryParameters['shipment_id'] = requestParameters['shipmentId'];
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/documents/uploads";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return DocumentUploadRecordsFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all shipping document upload records.
         * List all upload records
         */
        DocumentsApi.prototype.uploads = function () {
            return __awaiter(this, arguments, void 0, function (requestParameters, initOverrides) {
                var response;
                if (requestParameters === void 0) { requestParameters = {}; }
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.uploadsRaw(requestParameters, initOverrides)];
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

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  Karrio is a multi-carrier shipping API that simplifies the integration of logistics carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2025.5rc35`.  Read our API changelog to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"count\": 100,     \"next\": \"/v1/shipments?limit=25&offset=50\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [         { ... },     ] } ```  ## Metadata  Updateable Karrio objects—including Shipment and Order have a metadata parameter. You can use this parameter to attach key-value data to these Karrio objects.  Metadata is useful for storing additional, structured information on an object. As an example, you could store your user\'s full name and corresponding unique identifier from your system on a Karrio Order object.  Do not store any sensitive information as metadata.  ## Authentication  API keys are used to authenticate requests. You can view and manage your API keys in the Dashboard.  Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.  Authentication to the API is performed via HTTP Basic Auth. Provide your API token as the basic auth username value. You do not need to provide a password.  ```shell $ curl https://instance.api.com/v1/shipments \\     -u key_xxxxxx: # The colon prevents curl from asking for a password. ```  If you need to authenticate via bearer auth (e.g., for a cross-origin request), use `-H \"Authorization: Token key_xxxxxx\"` instead of `-u key_xxxxxx`.  All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). API requests without authentication will also fail.
     *
     * The version of the OpenAPI document: 2025.5rc35
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    /**
     *
     */
    var ManifestsApi = /** @class */ (function (_super) {
        __extends(ManifestsApi, _super);
        function ManifestsApi() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        /**
         * Create a manifest for one or many shipments with labels already purchased.
         * Create a manifest
         */
        ManifestsApi.prototype.createRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['manifestData'] == null) {
                                throw new RequiredError('manifestData', 'Required parameter "manifestData" was null or undefined when calling create().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/manifests";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'POST',
                                    headers: headerParameters,
                                    query: queryParameters,
                                    body: ManifestDataToJSON(requestParameters['manifestData']),
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ManifestFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Create a manifest for one or many shipments with labels already purchased.
         * Create a manifest
         */
        ManifestsApi.prototype.create = function (requestParameters, initOverrides) {
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
         * Retrieve all manifests.
         * List manifests
         */
        ManifestsApi.prototype.listRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            queryParameters = {};
                            if (requestParameters['carrierName'] != null) {
                                queryParameters['carrier_name'] = requestParameters['carrierName'];
                            }
                            if (requestParameters['createdAfter'] != null) {
                                queryParameters['created_after'] = requestParameters['createdAfter'].toISOString();
                            }
                            if (requestParameters['createdBefore'] != null) {
                                queryParameters['created_before'] = requestParameters['createdBefore'].toISOString();
                            }
                            headerParameters = {};
                            if (!(this.configuration && this.configuration.accessToken)) return [3 /*break*/, 2];
                            // oauth required
                            _a = headerParameters;
                            _b = "Authorization";
                            return [4 /*yield*/, this.configuration.accessToken("OAuth2", [])];
                        case 1:
                            // oauth required
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/manifests";
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ManifestListFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve all manifests.
         * List manifests
         */
        ManifestsApi.prototype.list = function () {
            return __awaiter(this, arguments, void 0, function (requestParameters, initOverrides) {
                var response;
                if (requestParameters === void 0) { requestParameters = {}; }
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
         * Retrieve a shipping manifest.
         * Retrieve a manifest
         */
        ManifestsApi.prototype.retrieveRaw = function (requestParameters, initOverrides) {
            return __awaiter(this, void 0, void 0, function () {
                var queryParameters, headerParameters, _a, _b, _c, _d, _e, _f, urlPath, response;
                return __generator(this, function (_g) {
                    switch (_g.label) {
                        case 0:
                            if (requestParameters['id'] == null) {
                                throw new RequiredError('id', 'Required parameter "id" was null or undefined when calling retrieve().');
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
                            _a[_b] = _g.sent();
                            _g.label = 2;
                        case 2:
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 4];
                            _c = headerParameters;
                            _d = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 3:
                            _c[_d] = _g.sent(); // JWT authentication
                            _g.label = 4;
                        case 4:
                            if (this.configuration && (this.configuration.username !== undefined || this.configuration.password !== undefined)) {
                                headerParameters["Authorization"] = "Basic " + btoa(this.configuration.username + ":" + this.configuration.password);
                            }
                            if (!(this.configuration && this.configuration.apiKey)) return [3 /*break*/, 6];
                            _e = headerParameters;
                            _f = "Authorization";
                            return [4 /*yield*/, this.configuration.apiKey("Authorization")];
                        case 5:
                            _e[_f] = _g.sent(); // Token authentication
                            _g.label = 6;
                        case 6:
                            urlPath = "/v1/manifests/{id}";
                            urlPath = urlPath.replace("{".concat("id", "}"), encodeURIComponent(String(requestParameters['id'])));
                            return [4 /*yield*/, this.request({
                                    path: urlPath,
                                    method: 'GET',
                                    headers: headerParameters,
                                    query: queryParameters,
                                }, initOverrides)];
                        case 7:
                            response = _g.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ManifestFromJSON(jsonValue); })];
                    }
                });
            });
        };
        /**
         * Retrieve a shipping manifest.
         * Retrieve a manifest
         */
        ManifestsApi.prototype.retrieve = function (requestParameters, initOverrides) {
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
        return ManifestsApi;
    }(BaseAPI));

    var KarrioClient = /** @class */ (function () {
        function KarrioClient(clientConfig) {
            var config = new Configuration(__assign({ credentials: "include", headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                } }, clientConfig));
            this.config = clientConfig;
            this.API = new APIApi(config);
            this.addresses = new AddressesApi(config);
            this.carriers = new CarriersApi(config);
            this.connections = new ConnectionsApi(config);
            this.parcels = new ParcelsApi(config);
            this.pickups = new PickupsApi(config);
            this.proxy = new ProxyApi(config);
            this.shipments = new ShipmentsApi(config);
            this.trackers = new TrackersApi(config);
            this.webhooks = new WebhooksApi(config);
            this.orders = new OrdersApi(config);
            this.manifest = new ManifestsApi(config);
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
