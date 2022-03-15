(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
        typeof define === 'function' && define.amd ? define(factory) :
            (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.Karrio = factory());
})(this, (function () {
    'use strict';

    /*! *****************************************************************************
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

    var extendStatics = function (d, b) {
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

    var __assign = function () {
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
        var _ = { label: 0, sent: function () { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
        return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function () { return this; }), g;
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
    var isBlob = function (value) { return typeof Blob !== 'undefined' && value instanceof Blob; };
    /**
     * This is the base class for all generated API classes.
     */
    var BaseAPI = /** @class */ (function () {
        function BaseAPI(configuration) {
            var _this = this;
            if (configuration === void 0) { configuration = new Configuration(); }
            this.configuration = configuration;
            this.fetchApi = function (url, init) {
                return __awaiter(_this, void 0, void 0, function () {
                    var fetchParams, _i, _a, middleware, response, _b, _c, middleware;
                    return __generator(this, function (_d) {
                        switch (_d.label) {
                            case 0:
                                fetchParams = { url: url, init: init };
                                _i = 0, _a = this.middleware;
                                _d.label = 1;
                            case 1:
                                if (!(_i < _a.length)) return [3 /*break*/, 4];
                                middleware = _a[_i];
                                if (!middleware.pre) return [3 /*break*/, 3];
                                return [4 /*yield*/, middleware.pre(__assign({ fetch: this.fetchApi }, fetchParams))];
                            case 2:
                                fetchParams = (_d.sent()) || fetchParams;
                                _d.label = 3;
                            case 3:
                                _i++;
                                return [3 /*break*/, 1];
                            case 4: return [4 /*yield*/, (this.configuration.fetchApi || fetch)(fetchParams.url, fetchParams.init)];
                            case 5:
                                response = _d.sent();
                                _b = 0, _c = this.middleware;
                                _d.label = 6;
                            case 6:
                                if (!(_b < _c.length)) return [3 /*break*/, 9];
                                middleware = _c[_b];
                                if (!middleware.post) return [3 /*break*/, 8];
                                return [4 /*yield*/, middleware.post({
                                    fetch: this.fetchApi,
                                    url: fetchParams.url,
                                    init: fetchParams.init,
                                    response: response.clone(),
                                })];
                            case 7:
                                response = (_d.sent()) || response;
                                _d.label = 8;
                            case 8:
                                _b++;
                                return [3 /*break*/, 6];
                            case 9: return [2 /*return*/, response];
                        }
                    });
                });
            };
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
                        case 0:
                            _a = this.createFetchParams(context, initOverrides), url = _a.url, init = _a.init;
                            return [4 /*yield*/, this.fetchApi(url, init)];
                        case 1:
                            response = _b.sent();
                            if (response.status >= 200 && response.status < 300) {
                                return [2 /*return*/, response];
                            }
                            throw response;
                    }
                });
            });
        };
        BaseAPI.prototype.createFetchParams = function (context, initOverrides) {
            var url = this.configuration.basePath + context.path;
            if (context.query !== undefined && Object.keys(context.query).length !== 0) {
                // only add the querystring to the URL if there are query parameters.
                // this is done to avoid urls ending with a "?" character which buggy webservers
                // do not handle correctly sometimes.
                url += '?' + this.configuration.queryParamsStringify(context.query);
            }
            var body = ((typeof FormData !== "undefined" && context.body instanceof FormData) || context.body instanceof URLSearchParams || isBlob(context.body))
                ? context.body
                : JSON.stringify(context.body);
            var headers = Object.assign({}, this.configuration.headers, context.headers);
            var init = __assign({ method: context.method, headers: headers, body: body, credentials: this.configuration.credentials }, initOverrides);
            return { url: url, init: init };
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
    var Configuration = /** @class */ (function () {
        function Configuration(configuration) {
            if (configuration === void 0) { configuration = {}; }
            this.configuration = configuration;
        }
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
                    return typeof accessToken === 'function' ? accessToken : function () {
                        return __awaiter(_this, void 0, void 0, function () {
                            return __generator(this, function (_a) {
                                return [2 /*return*/, accessToken];
                            });
                        });
                    };
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
    function exists(json, key) {
        var value = json[key];
        return value !== null && value !== undefined;
    }
    function querystring(params, prefix) {
        if (prefix === void 0) { prefix = ''; }
        return Object.keys(params)
            .map(function (key) {
                var fullKey = prefix + (prefix.length ? "[" + key + "]" : key);
                var value = params[key];
                if (value instanceof Array) {
                    var multiValue = value.map(function (singleValue) { return encodeURIComponent(String(singleValue)); })
                        .join("&" + encodeURIComponent(fullKey) + "=");
                    return encodeURIComponent(fullKey) + "=" + multiValue;
                }
                if (value instanceof Date) {
                    return encodeURIComponent(fullKey) + "=" + encodeURIComponent(value.toISOString());
                }
                if (value instanceof Object) {
                    return querystring(value, fullKey);
                }
                return encodeURIComponent(fullKey) + "=" + encodeURIComponent(String(value));
            })
            .filter(function (part) { return part.length > 0; })
            .join('&');
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
    /**
    * @export
    * @enum {string}
    */
    var AddressCountryCodeEnum;
    (function (AddressCountryCodeEnum) {
        AddressCountryCodeEnum["Ad"] = "AD";
        AddressCountryCodeEnum["Ae"] = "AE";
        AddressCountryCodeEnum["Af"] = "AF";
        AddressCountryCodeEnum["Ag"] = "AG";
        AddressCountryCodeEnum["Ai"] = "AI";
        AddressCountryCodeEnum["Al"] = "AL";
        AddressCountryCodeEnum["Am"] = "AM";
        AddressCountryCodeEnum["An"] = "AN";
        AddressCountryCodeEnum["Ao"] = "AO";
        AddressCountryCodeEnum["Ar"] = "AR";
        AddressCountryCodeEnum["As"] = "AS";
        AddressCountryCodeEnum["At"] = "AT";
        AddressCountryCodeEnum["Au"] = "AU";
        AddressCountryCodeEnum["Aw"] = "AW";
        AddressCountryCodeEnum["Az"] = "AZ";
        AddressCountryCodeEnum["Ba"] = "BA";
        AddressCountryCodeEnum["Bb"] = "BB";
        AddressCountryCodeEnum["Bd"] = "BD";
        AddressCountryCodeEnum["Be"] = "BE";
        AddressCountryCodeEnum["Bf"] = "BF";
        AddressCountryCodeEnum["Bg"] = "BG";
        AddressCountryCodeEnum["Bh"] = "BH";
        AddressCountryCodeEnum["Bi"] = "BI";
        AddressCountryCodeEnum["Bj"] = "BJ";
        AddressCountryCodeEnum["Bm"] = "BM";
        AddressCountryCodeEnum["Bn"] = "BN";
        AddressCountryCodeEnum["Bo"] = "BO";
        AddressCountryCodeEnum["Br"] = "BR";
        AddressCountryCodeEnum["Bs"] = "BS";
        AddressCountryCodeEnum["Bt"] = "BT";
        AddressCountryCodeEnum["Bw"] = "BW";
        AddressCountryCodeEnum["By"] = "BY";
        AddressCountryCodeEnum["Bz"] = "BZ";
        AddressCountryCodeEnum["Ca"] = "CA";
        AddressCountryCodeEnum["Cd"] = "CD";
        AddressCountryCodeEnum["Cf"] = "CF";
        AddressCountryCodeEnum["Cg"] = "CG";
        AddressCountryCodeEnum["Ch"] = "CH";
        AddressCountryCodeEnum["Ci"] = "CI";
        AddressCountryCodeEnum["Ck"] = "CK";
        AddressCountryCodeEnum["Cl"] = "CL";
        AddressCountryCodeEnum["Cm"] = "CM";
        AddressCountryCodeEnum["Cn"] = "CN";
        AddressCountryCodeEnum["Co"] = "CO";
        AddressCountryCodeEnum["Cr"] = "CR";
        AddressCountryCodeEnum["Cu"] = "CU";
        AddressCountryCodeEnum["Cv"] = "CV";
        AddressCountryCodeEnum["Cy"] = "CY";
        AddressCountryCodeEnum["Cz"] = "CZ";
        AddressCountryCodeEnum["De"] = "DE";
        AddressCountryCodeEnum["Dj"] = "DJ";
        AddressCountryCodeEnum["Dk"] = "DK";
        AddressCountryCodeEnum["Dm"] = "DM";
        AddressCountryCodeEnum["Do"] = "DO";
        AddressCountryCodeEnum["Dz"] = "DZ";
        AddressCountryCodeEnum["Ec"] = "EC";
        AddressCountryCodeEnum["Ee"] = "EE";
        AddressCountryCodeEnum["Eg"] = "EG";
        AddressCountryCodeEnum["Er"] = "ER";
        AddressCountryCodeEnum["Es"] = "ES";
        AddressCountryCodeEnum["Et"] = "ET";
        AddressCountryCodeEnum["Fi"] = "FI";
        AddressCountryCodeEnum["Fj"] = "FJ";
        AddressCountryCodeEnum["Fk"] = "FK";
        AddressCountryCodeEnum["Fm"] = "FM";
        AddressCountryCodeEnum["Fo"] = "FO";
        AddressCountryCodeEnum["Fr"] = "FR";
        AddressCountryCodeEnum["Ga"] = "GA";
        AddressCountryCodeEnum["Gb"] = "GB";
        AddressCountryCodeEnum["Gd"] = "GD";
        AddressCountryCodeEnum["Ge"] = "GE";
        AddressCountryCodeEnum["Gf"] = "GF";
        AddressCountryCodeEnum["Gg"] = "GG";
        AddressCountryCodeEnum["Gh"] = "GH";
        AddressCountryCodeEnum["Gi"] = "GI";
        AddressCountryCodeEnum["Gl"] = "GL";
        AddressCountryCodeEnum["Gm"] = "GM";
        AddressCountryCodeEnum["Gn"] = "GN";
        AddressCountryCodeEnum["Gp"] = "GP";
        AddressCountryCodeEnum["Gq"] = "GQ";
        AddressCountryCodeEnum["Gr"] = "GR";
        AddressCountryCodeEnum["Gt"] = "GT";
        AddressCountryCodeEnum["Gu"] = "GU";
        AddressCountryCodeEnum["Gw"] = "GW";
        AddressCountryCodeEnum["Gy"] = "GY";
        AddressCountryCodeEnum["Hk"] = "HK";
        AddressCountryCodeEnum["Hn"] = "HN";
        AddressCountryCodeEnum["Hr"] = "HR";
        AddressCountryCodeEnum["Ht"] = "HT";
        AddressCountryCodeEnum["Hu"] = "HU";
        AddressCountryCodeEnum["Ic"] = "IC";
        AddressCountryCodeEnum["Id"] = "ID";
        AddressCountryCodeEnum["Ie"] = "IE";
        AddressCountryCodeEnum["Il"] = "IL";
        AddressCountryCodeEnum["In"] = "IN";
        AddressCountryCodeEnum["Iq"] = "IQ";
        AddressCountryCodeEnum["Ir"] = "IR";
        AddressCountryCodeEnum["Is"] = "IS";
        AddressCountryCodeEnum["It"] = "IT";
        AddressCountryCodeEnum["Je"] = "JE";
        AddressCountryCodeEnum["Jm"] = "JM";
        AddressCountryCodeEnum["Jo"] = "JO";
        AddressCountryCodeEnum["Jp"] = "JP";
        AddressCountryCodeEnum["Ke"] = "KE";
        AddressCountryCodeEnum["Kg"] = "KG";
        AddressCountryCodeEnum["Kh"] = "KH";
        AddressCountryCodeEnum["Ki"] = "KI";
        AddressCountryCodeEnum["Km"] = "KM";
        AddressCountryCodeEnum["Kn"] = "KN";
        AddressCountryCodeEnum["Kp"] = "KP";
        AddressCountryCodeEnum["Kr"] = "KR";
        AddressCountryCodeEnum["Kv"] = "KV";
        AddressCountryCodeEnum["Kw"] = "KW";
        AddressCountryCodeEnum["Ky"] = "KY";
        AddressCountryCodeEnum["Kz"] = "KZ";
        AddressCountryCodeEnum["La"] = "LA";
        AddressCountryCodeEnum["Lb"] = "LB";
        AddressCountryCodeEnum["Lc"] = "LC";
        AddressCountryCodeEnum["Li"] = "LI";
        AddressCountryCodeEnum["Lk"] = "LK";
        AddressCountryCodeEnum["Lr"] = "LR";
        AddressCountryCodeEnum["Ls"] = "LS";
        AddressCountryCodeEnum["Lt"] = "LT";
        AddressCountryCodeEnum["Lu"] = "LU";
        AddressCountryCodeEnum["Lv"] = "LV";
        AddressCountryCodeEnum["Ly"] = "LY";
        AddressCountryCodeEnum["Ma"] = "MA";
        AddressCountryCodeEnum["Mc"] = "MC";
        AddressCountryCodeEnum["Md"] = "MD";
        AddressCountryCodeEnum["Me"] = "ME";
        AddressCountryCodeEnum["Mg"] = "MG";
        AddressCountryCodeEnum["Mh"] = "MH";
        AddressCountryCodeEnum["Mk"] = "MK";
        AddressCountryCodeEnum["Ml"] = "ML";
        AddressCountryCodeEnum["Mm"] = "MM";
        AddressCountryCodeEnum["Mn"] = "MN";
        AddressCountryCodeEnum["Mo"] = "MO";
        AddressCountryCodeEnum["Mp"] = "MP";
        AddressCountryCodeEnum["Mq"] = "MQ";
        AddressCountryCodeEnum["Mr"] = "MR";
        AddressCountryCodeEnum["Ms"] = "MS";
        AddressCountryCodeEnum["Mt"] = "MT";
        AddressCountryCodeEnum["Mu"] = "MU";
        AddressCountryCodeEnum["Mv"] = "MV";
        AddressCountryCodeEnum["Mw"] = "MW";
        AddressCountryCodeEnum["Mx"] = "MX";
        AddressCountryCodeEnum["My"] = "MY";
        AddressCountryCodeEnum["Mz"] = "MZ";
        AddressCountryCodeEnum["Na"] = "NA";
        AddressCountryCodeEnum["Nc"] = "NC";
        AddressCountryCodeEnum["Ne"] = "NE";
        AddressCountryCodeEnum["Ng"] = "NG";
        AddressCountryCodeEnum["Ni"] = "NI";
        AddressCountryCodeEnum["Nl"] = "NL";
        AddressCountryCodeEnum["No"] = "NO";
        AddressCountryCodeEnum["Np"] = "NP";
        AddressCountryCodeEnum["Nr"] = "NR";
        AddressCountryCodeEnum["Nu"] = "NU";
        AddressCountryCodeEnum["Nz"] = "NZ";
        AddressCountryCodeEnum["Om"] = "OM";
        AddressCountryCodeEnum["Pa"] = "PA";
        AddressCountryCodeEnum["Pe"] = "PE";
        AddressCountryCodeEnum["Pf"] = "PF";
        AddressCountryCodeEnum["Pg"] = "PG";
        AddressCountryCodeEnum["Ph"] = "PH";
        AddressCountryCodeEnum["Pk"] = "PK";
        AddressCountryCodeEnum["Pl"] = "PL";
        AddressCountryCodeEnum["Pr"] = "PR";
        AddressCountryCodeEnum["Pt"] = "PT";
        AddressCountryCodeEnum["Pw"] = "PW";
        AddressCountryCodeEnum["Py"] = "PY";
        AddressCountryCodeEnum["Qa"] = "QA";
        AddressCountryCodeEnum["Re"] = "RE";
        AddressCountryCodeEnum["Ro"] = "RO";
        AddressCountryCodeEnum["Rs"] = "RS";
        AddressCountryCodeEnum["Ru"] = "RU";
        AddressCountryCodeEnum["Rw"] = "RW";
        AddressCountryCodeEnum["Sa"] = "SA";
        AddressCountryCodeEnum["Sb"] = "SB";
        AddressCountryCodeEnum["Sc"] = "SC";
        AddressCountryCodeEnum["Sd"] = "SD";
        AddressCountryCodeEnum["Se"] = "SE";
        AddressCountryCodeEnum["Sg"] = "SG";
        AddressCountryCodeEnum["Sh"] = "SH";
        AddressCountryCodeEnum["Si"] = "SI";
        AddressCountryCodeEnum["Sk"] = "SK";
        AddressCountryCodeEnum["Sl"] = "SL";
        AddressCountryCodeEnum["Sm"] = "SM";
        AddressCountryCodeEnum["Sn"] = "SN";
        AddressCountryCodeEnum["So"] = "SO";
        AddressCountryCodeEnum["Sr"] = "SR";
        AddressCountryCodeEnum["Ss"] = "SS";
        AddressCountryCodeEnum["St"] = "ST";
        AddressCountryCodeEnum["Sv"] = "SV";
        AddressCountryCodeEnum["Sy"] = "SY";
        AddressCountryCodeEnum["Sz"] = "SZ";
        AddressCountryCodeEnum["Tc"] = "TC";
        AddressCountryCodeEnum["Td"] = "TD";
        AddressCountryCodeEnum["Tg"] = "TG";
        AddressCountryCodeEnum["Th"] = "TH";
        AddressCountryCodeEnum["Tj"] = "TJ";
        AddressCountryCodeEnum["Tl"] = "TL";
        AddressCountryCodeEnum["Tn"] = "TN";
        AddressCountryCodeEnum["To"] = "TO";
        AddressCountryCodeEnum["Tr"] = "TR";
        AddressCountryCodeEnum["Tt"] = "TT";
        AddressCountryCodeEnum["Tv"] = "TV";
        AddressCountryCodeEnum["Tw"] = "TW";
        AddressCountryCodeEnum["Tz"] = "TZ";
        AddressCountryCodeEnum["Ua"] = "UA";
        AddressCountryCodeEnum["Ug"] = "UG";
        AddressCountryCodeEnum["Us"] = "US";
        AddressCountryCodeEnum["Uy"] = "UY";
        AddressCountryCodeEnum["Uz"] = "UZ";
        AddressCountryCodeEnum["Va"] = "VA";
        AddressCountryCodeEnum["Vc"] = "VC";
        AddressCountryCodeEnum["Ve"] = "VE";
        AddressCountryCodeEnum["Vg"] = "VG";
        AddressCountryCodeEnum["Vi"] = "VI";
        AddressCountryCodeEnum["Vn"] = "VN";
        AddressCountryCodeEnum["Vu"] = "VU";
        AddressCountryCodeEnum["Ws"] = "WS";
        AddressCountryCodeEnum["Xb"] = "XB";
        AddressCountryCodeEnum["Xc"] = "XC";
        AddressCountryCodeEnum["Xe"] = "XE";
        AddressCountryCodeEnum["Xm"] = "XM";
        AddressCountryCodeEnum["Xn"] = "XN";
        AddressCountryCodeEnum["Xs"] = "XS";
        AddressCountryCodeEnum["Xy"] = "XY";
        AddressCountryCodeEnum["Ye"] = "YE";
        AddressCountryCodeEnum["Yt"] = "YT";
        AddressCountryCodeEnum["Za"] = "ZA";
        AddressCountryCodeEnum["Zm"] = "ZM";
        AddressCountryCodeEnum["Zw"] = "ZW";
    })(AddressCountryCodeEnum || (AddressCountryCodeEnum = {}));
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
    /**
    * @export
    * @enum {string}
    */
    var AddressDataCountryCodeEnum;
    (function (AddressDataCountryCodeEnum) {
        AddressDataCountryCodeEnum["Ad"] = "AD";
        AddressDataCountryCodeEnum["Ae"] = "AE";
        AddressDataCountryCodeEnum["Af"] = "AF";
        AddressDataCountryCodeEnum["Ag"] = "AG";
        AddressDataCountryCodeEnum["Ai"] = "AI";
        AddressDataCountryCodeEnum["Al"] = "AL";
        AddressDataCountryCodeEnum["Am"] = "AM";
        AddressDataCountryCodeEnum["An"] = "AN";
        AddressDataCountryCodeEnum["Ao"] = "AO";
        AddressDataCountryCodeEnum["Ar"] = "AR";
        AddressDataCountryCodeEnum["As"] = "AS";
        AddressDataCountryCodeEnum["At"] = "AT";
        AddressDataCountryCodeEnum["Au"] = "AU";
        AddressDataCountryCodeEnum["Aw"] = "AW";
        AddressDataCountryCodeEnum["Az"] = "AZ";
        AddressDataCountryCodeEnum["Ba"] = "BA";
        AddressDataCountryCodeEnum["Bb"] = "BB";
        AddressDataCountryCodeEnum["Bd"] = "BD";
        AddressDataCountryCodeEnum["Be"] = "BE";
        AddressDataCountryCodeEnum["Bf"] = "BF";
        AddressDataCountryCodeEnum["Bg"] = "BG";
        AddressDataCountryCodeEnum["Bh"] = "BH";
        AddressDataCountryCodeEnum["Bi"] = "BI";
        AddressDataCountryCodeEnum["Bj"] = "BJ";
        AddressDataCountryCodeEnum["Bm"] = "BM";
        AddressDataCountryCodeEnum["Bn"] = "BN";
        AddressDataCountryCodeEnum["Bo"] = "BO";
        AddressDataCountryCodeEnum["Br"] = "BR";
        AddressDataCountryCodeEnum["Bs"] = "BS";
        AddressDataCountryCodeEnum["Bt"] = "BT";
        AddressDataCountryCodeEnum["Bw"] = "BW";
        AddressDataCountryCodeEnum["By"] = "BY";
        AddressDataCountryCodeEnum["Bz"] = "BZ";
        AddressDataCountryCodeEnum["Ca"] = "CA";
        AddressDataCountryCodeEnum["Cd"] = "CD";
        AddressDataCountryCodeEnum["Cf"] = "CF";
        AddressDataCountryCodeEnum["Cg"] = "CG";
        AddressDataCountryCodeEnum["Ch"] = "CH";
        AddressDataCountryCodeEnum["Ci"] = "CI";
        AddressDataCountryCodeEnum["Ck"] = "CK";
        AddressDataCountryCodeEnum["Cl"] = "CL";
        AddressDataCountryCodeEnum["Cm"] = "CM";
        AddressDataCountryCodeEnum["Cn"] = "CN";
        AddressDataCountryCodeEnum["Co"] = "CO";
        AddressDataCountryCodeEnum["Cr"] = "CR";
        AddressDataCountryCodeEnum["Cu"] = "CU";
        AddressDataCountryCodeEnum["Cv"] = "CV";
        AddressDataCountryCodeEnum["Cy"] = "CY";
        AddressDataCountryCodeEnum["Cz"] = "CZ";
        AddressDataCountryCodeEnum["De"] = "DE";
        AddressDataCountryCodeEnum["Dj"] = "DJ";
        AddressDataCountryCodeEnum["Dk"] = "DK";
        AddressDataCountryCodeEnum["Dm"] = "DM";
        AddressDataCountryCodeEnum["Do"] = "DO";
        AddressDataCountryCodeEnum["Dz"] = "DZ";
        AddressDataCountryCodeEnum["Ec"] = "EC";
        AddressDataCountryCodeEnum["Ee"] = "EE";
        AddressDataCountryCodeEnum["Eg"] = "EG";
        AddressDataCountryCodeEnum["Er"] = "ER";
        AddressDataCountryCodeEnum["Es"] = "ES";
        AddressDataCountryCodeEnum["Et"] = "ET";
        AddressDataCountryCodeEnum["Fi"] = "FI";
        AddressDataCountryCodeEnum["Fj"] = "FJ";
        AddressDataCountryCodeEnum["Fk"] = "FK";
        AddressDataCountryCodeEnum["Fm"] = "FM";
        AddressDataCountryCodeEnum["Fo"] = "FO";
        AddressDataCountryCodeEnum["Fr"] = "FR";
        AddressDataCountryCodeEnum["Ga"] = "GA";
        AddressDataCountryCodeEnum["Gb"] = "GB";
        AddressDataCountryCodeEnum["Gd"] = "GD";
        AddressDataCountryCodeEnum["Ge"] = "GE";
        AddressDataCountryCodeEnum["Gf"] = "GF";
        AddressDataCountryCodeEnum["Gg"] = "GG";
        AddressDataCountryCodeEnum["Gh"] = "GH";
        AddressDataCountryCodeEnum["Gi"] = "GI";
        AddressDataCountryCodeEnum["Gl"] = "GL";
        AddressDataCountryCodeEnum["Gm"] = "GM";
        AddressDataCountryCodeEnum["Gn"] = "GN";
        AddressDataCountryCodeEnum["Gp"] = "GP";
        AddressDataCountryCodeEnum["Gq"] = "GQ";
        AddressDataCountryCodeEnum["Gr"] = "GR";
        AddressDataCountryCodeEnum["Gt"] = "GT";
        AddressDataCountryCodeEnum["Gu"] = "GU";
        AddressDataCountryCodeEnum["Gw"] = "GW";
        AddressDataCountryCodeEnum["Gy"] = "GY";
        AddressDataCountryCodeEnum["Hk"] = "HK";
        AddressDataCountryCodeEnum["Hn"] = "HN";
        AddressDataCountryCodeEnum["Hr"] = "HR";
        AddressDataCountryCodeEnum["Ht"] = "HT";
        AddressDataCountryCodeEnum["Hu"] = "HU";
        AddressDataCountryCodeEnum["Ic"] = "IC";
        AddressDataCountryCodeEnum["Id"] = "ID";
        AddressDataCountryCodeEnum["Ie"] = "IE";
        AddressDataCountryCodeEnum["Il"] = "IL";
        AddressDataCountryCodeEnum["In"] = "IN";
        AddressDataCountryCodeEnum["Iq"] = "IQ";
        AddressDataCountryCodeEnum["Ir"] = "IR";
        AddressDataCountryCodeEnum["Is"] = "IS";
        AddressDataCountryCodeEnum["It"] = "IT";
        AddressDataCountryCodeEnum["Je"] = "JE";
        AddressDataCountryCodeEnum["Jm"] = "JM";
        AddressDataCountryCodeEnum["Jo"] = "JO";
        AddressDataCountryCodeEnum["Jp"] = "JP";
        AddressDataCountryCodeEnum["Ke"] = "KE";
        AddressDataCountryCodeEnum["Kg"] = "KG";
        AddressDataCountryCodeEnum["Kh"] = "KH";
        AddressDataCountryCodeEnum["Ki"] = "KI";
        AddressDataCountryCodeEnum["Km"] = "KM";
        AddressDataCountryCodeEnum["Kn"] = "KN";
        AddressDataCountryCodeEnum["Kp"] = "KP";
        AddressDataCountryCodeEnum["Kr"] = "KR";
        AddressDataCountryCodeEnum["Kv"] = "KV";
        AddressDataCountryCodeEnum["Kw"] = "KW";
        AddressDataCountryCodeEnum["Ky"] = "KY";
        AddressDataCountryCodeEnum["Kz"] = "KZ";
        AddressDataCountryCodeEnum["La"] = "LA";
        AddressDataCountryCodeEnum["Lb"] = "LB";
        AddressDataCountryCodeEnum["Lc"] = "LC";
        AddressDataCountryCodeEnum["Li"] = "LI";
        AddressDataCountryCodeEnum["Lk"] = "LK";
        AddressDataCountryCodeEnum["Lr"] = "LR";
        AddressDataCountryCodeEnum["Ls"] = "LS";
        AddressDataCountryCodeEnum["Lt"] = "LT";
        AddressDataCountryCodeEnum["Lu"] = "LU";
        AddressDataCountryCodeEnum["Lv"] = "LV";
        AddressDataCountryCodeEnum["Ly"] = "LY";
        AddressDataCountryCodeEnum["Ma"] = "MA";
        AddressDataCountryCodeEnum["Mc"] = "MC";
        AddressDataCountryCodeEnum["Md"] = "MD";
        AddressDataCountryCodeEnum["Me"] = "ME";
        AddressDataCountryCodeEnum["Mg"] = "MG";
        AddressDataCountryCodeEnum["Mh"] = "MH";
        AddressDataCountryCodeEnum["Mk"] = "MK";
        AddressDataCountryCodeEnum["Ml"] = "ML";
        AddressDataCountryCodeEnum["Mm"] = "MM";
        AddressDataCountryCodeEnum["Mn"] = "MN";
        AddressDataCountryCodeEnum["Mo"] = "MO";
        AddressDataCountryCodeEnum["Mp"] = "MP";
        AddressDataCountryCodeEnum["Mq"] = "MQ";
        AddressDataCountryCodeEnum["Mr"] = "MR";
        AddressDataCountryCodeEnum["Ms"] = "MS";
        AddressDataCountryCodeEnum["Mt"] = "MT";
        AddressDataCountryCodeEnum["Mu"] = "MU";
        AddressDataCountryCodeEnum["Mv"] = "MV";
        AddressDataCountryCodeEnum["Mw"] = "MW";
        AddressDataCountryCodeEnum["Mx"] = "MX";
        AddressDataCountryCodeEnum["My"] = "MY";
        AddressDataCountryCodeEnum["Mz"] = "MZ";
        AddressDataCountryCodeEnum["Na"] = "NA";
        AddressDataCountryCodeEnum["Nc"] = "NC";
        AddressDataCountryCodeEnum["Ne"] = "NE";
        AddressDataCountryCodeEnum["Ng"] = "NG";
        AddressDataCountryCodeEnum["Ni"] = "NI";
        AddressDataCountryCodeEnum["Nl"] = "NL";
        AddressDataCountryCodeEnum["No"] = "NO";
        AddressDataCountryCodeEnum["Np"] = "NP";
        AddressDataCountryCodeEnum["Nr"] = "NR";
        AddressDataCountryCodeEnum["Nu"] = "NU";
        AddressDataCountryCodeEnum["Nz"] = "NZ";
        AddressDataCountryCodeEnum["Om"] = "OM";
        AddressDataCountryCodeEnum["Pa"] = "PA";
        AddressDataCountryCodeEnum["Pe"] = "PE";
        AddressDataCountryCodeEnum["Pf"] = "PF";
        AddressDataCountryCodeEnum["Pg"] = "PG";
        AddressDataCountryCodeEnum["Ph"] = "PH";
        AddressDataCountryCodeEnum["Pk"] = "PK";
        AddressDataCountryCodeEnum["Pl"] = "PL";
        AddressDataCountryCodeEnum["Pr"] = "PR";
        AddressDataCountryCodeEnum["Pt"] = "PT";
        AddressDataCountryCodeEnum["Pw"] = "PW";
        AddressDataCountryCodeEnum["Py"] = "PY";
        AddressDataCountryCodeEnum["Qa"] = "QA";
        AddressDataCountryCodeEnum["Re"] = "RE";
        AddressDataCountryCodeEnum["Ro"] = "RO";
        AddressDataCountryCodeEnum["Rs"] = "RS";
        AddressDataCountryCodeEnum["Ru"] = "RU";
        AddressDataCountryCodeEnum["Rw"] = "RW";
        AddressDataCountryCodeEnum["Sa"] = "SA";
        AddressDataCountryCodeEnum["Sb"] = "SB";
        AddressDataCountryCodeEnum["Sc"] = "SC";
        AddressDataCountryCodeEnum["Sd"] = "SD";
        AddressDataCountryCodeEnum["Se"] = "SE";
        AddressDataCountryCodeEnum["Sg"] = "SG";
        AddressDataCountryCodeEnum["Sh"] = "SH";
        AddressDataCountryCodeEnum["Si"] = "SI";
        AddressDataCountryCodeEnum["Sk"] = "SK";
        AddressDataCountryCodeEnum["Sl"] = "SL";
        AddressDataCountryCodeEnum["Sm"] = "SM";
        AddressDataCountryCodeEnum["Sn"] = "SN";
        AddressDataCountryCodeEnum["So"] = "SO";
        AddressDataCountryCodeEnum["Sr"] = "SR";
        AddressDataCountryCodeEnum["Ss"] = "SS";
        AddressDataCountryCodeEnum["St"] = "ST";
        AddressDataCountryCodeEnum["Sv"] = "SV";
        AddressDataCountryCodeEnum["Sy"] = "SY";
        AddressDataCountryCodeEnum["Sz"] = "SZ";
        AddressDataCountryCodeEnum["Tc"] = "TC";
        AddressDataCountryCodeEnum["Td"] = "TD";
        AddressDataCountryCodeEnum["Tg"] = "TG";
        AddressDataCountryCodeEnum["Th"] = "TH";
        AddressDataCountryCodeEnum["Tj"] = "TJ";
        AddressDataCountryCodeEnum["Tl"] = "TL";
        AddressDataCountryCodeEnum["Tn"] = "TN";
        AddressDataCountryCodeEnum["To"] = "TO";
        AddressDataCountryCodeEnum["Tr"] = "TR";
        AddressDataCountryCodeEnum["Tt"] = "TT";
        AddressDataCountryCodeEnum["Tv"] = "TV";
        AddressDataCountryCodeEnum["Tw"] = "TW";
        AddressDataCountryCodeEnum["Tz"] = "TZ";
        AddressDataCountryCodeEnum["Ua"] = "UA";
        AddressDataCountryCodeEnum["Ug"] = "UG";
        AddressDataCountryCodeEnum["Us"] = "US";
        AddressDataCountryCodeEnum["Uy"] = "UY";
        AddressDataCountryCodeEnum["Uz"] = "UZ";
        AddressDataCountryCodeEnum["Va"] = "VA";
        AddressDataCountryCodeEnum["Vc"] = "VC";
        AddressDataCountryCodeEnum["Ve"] = "VE";
        AddressDataCountryCodeEnum["Vg"] = "VG";
        AddressDataCountryCodeEnum["Vi"] = "VI";
        AddressDataCountryCodeEnum["Vn"] = "VN";
        AddressDataCountryCodeEnum["Vu"] = "VU";
        AddressDataCountryCodeEnum["Ws"] = "WS";
        AddressDataCountryCodeEnum["Xb"] = "XB";
        AddressDataCountryCodeEnum["Xc"] = "XC";
        AddressDataCountryCodeEnum["Xe"] = "XE";
        AddressDataCountryCodeEnum["Xm"] = "XM";
        AddressDataCountryCodeEnum["Xn"] = "XN";
        AddressDataCountryCodeEnum["Xs"] = "XS";
        AddressDataCountryCodeEnum["Xy"] = "XY";
        AddressDataCountryCodeEnum["Ye"] = "YE";
        AddressDataCountryCodeEnum["Yt"] = "YT";
        AddressDataCountryCodeEnum["Za"] = "ZA";
        AddressDataCountryCodeEnum["Zm"] = "ZM";
        AddressDataCountryCodeEnum["Zw"] = "ZW";
    })(AddressDataCountryCodeEnum || (AddressDataCountryCodeEnum = {}));
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
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(AddressFromJSON)),
        };
    }

    /* tslint:disable */
    /**
    * @export
    * @enum {string}
    */
    var CarrierSettingsCarrierNameEnum;
    (function (CarrierSettingsCarrierNameEnum) {
        CarrierSettingsCarrierNameEnum["Aramex"] = "aramex";
        CarrierSettingsCarrierNameEnum["Australiapost"] = "australiapost";
        CarrierSettingsCarrierNameEnum["Canadapost"] = "canadapost";
        CarrierSettingsCarrierNameEnum["Canpar"] = "canpar";
        CarrierSettingsCarrierNameEnum["DhlExpress"] = "dhl_express";
        CarrierSettingsCarrierNameEnum["DhlPoland"] = "dhl_poland";
        CarrierSettingsCarrierNameEnum["DhlUniversal"] = "dhl_universal";
        CarrierSettingsCarrierNameEnum["Dicom"] = "dicom";
        CarrierSettingsCarrierNameEnum["Eshipper"] = "eshipper";
        CarrierSettingsCarrierNameEnum["Fedex"] = "fedex";
        CarrierSettingsCarrierNameEnum["Freightcom"] = "freightcom";
        CarrierSettingsCarrierNameEnum["Generic"] = "generic";
        CarrierSettingsCarrierNameEnum["Purolator"] = "purolator";
        CarrierSettingsCarrierNameEnum["Royalmail"] = "royalmail";
        CarrierSettingsCarrierNameEnum["Sendle"] = "sendle";
        CarrierSettingsCarrierNameEnum["SfExpress"] = "sf_express";
        CarrierSettingsCarrierNameEnum["Tnt"] = "tnt";
        CarrierSettingsCarrierNameEnum["Ups"] = "ups";
        CarrierSettingsCarrierNameEnum["Usps"] = "usps";
        CarrierSettingsCarrierNameEnum["UspsInternational"] = "usps_international";
        CarrierSettingsCarrierNameEnum["Yanwen"] = "yanwen";
        CarrierSettingsCarrierNameEnum["Yunexpress"] = "yunexpress";
    })(CarrierSettingsCarrierNameEnum || (CarrierSettingsCarrierNameEnum = {}));
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
            'test': json['test'],
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
    /**
    * @export
    * @enum {string}
    */
    var CommodityWeightUnitEnum;
    (function (CommodityWeightUnitEnum) {
        CommodityWeightUnitEnum["Kg"] = "KG";
        CommodityWeightUnitEnum["Lb"] = "LB";
    })(CommodityWeightUnitEnum || (CommodityWeightUnitEnum = {}));
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
            'value_amount': value.value_amount,
            'value_currency': value.value_currency,
            'origin_country': value.origin_country,
            'parent_id': value.parent_id,
            'metadata': value.metadata,
            'object_type': value.object_type,
        };
    }

    /* tslint:disable */
    /**
    * @export
    * @enum {string}
    */
    var CommodityDataWeightUnitEnum;
    (function (CommodityDataWeightUnitEnum) {
        CommodityDataWeightUnitEnum["Kg"] = "KG";
        CommodityDataWeightUnitEnum["Lb"] = "LB";
    })(CommodityDataWeightUnitEnum || (CommodityDataWeightUnitEnum = {}));
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
            'value_amount': value.value_amount,
            'value_currency': value.value_currency,
            'origin_country': value.origin_country,
            'parent_id': value.parent_id,
            'metadata': value.metadata,
        };
    }

    /* tslint:disable */
    /**
    * @export
    * @enum {string}
    */
    var DutyPaidByEnum;
    (function (DutyPaidByEnum) {
        DutyPaidByEnum["Sender"] = "sender";
        DutyPaidByEnum["Recipient"] = "recipient";
        DutyPaidByEnum["ThirdParty"] = "third_party";
    })(DutyPaidByEnum || (DutyPaidByEnum = {})); /**
    * @export
    * @enum {string}
    */
    var DutyCurrencyEnum;
    (function (DutyCurrencyEnum) {
        DutyCurrencyEnum["Eur"] = "EUR";
        DutyCurrencyEnum["Aed"] = "AED";
        DutyCurrencyEnum["Usd"] = "USD";
        DutyCurrencyEnum["Xcd"] = "XCD";
        DutyCurrencyEnum["Amd"] = "AMD";
        DutyCurrencyEnum["Ang"] = "ANG";
        DutyCurrencyEnum["Aoa"] = "AOA";
        DutyCurrencyEnum["Ars"] = "ARS";
        DutyCurrencyEnum["Aud"] = "AUD";
        DutyCurrencyEnum["Awg"] = "AWG";
        DutyCurrencyEnum["Azn"] = "AZN";
        DutyCurrencyEnum["Bam"] = "BAM";
        DutyCurrencyEnum["Bbd"] = "BBD";
        DutyCurrencyEnum["Bdt"] = "BDT";
        DutyCurrencyEnum["Xof"] = "XOF";
        DutyCurrencyEnum["Bgn"] = "BGN";
        DutyCurrencyEnum["Bhd"] = "BHD";
        DutyCurrencyEnum["Bif"] = "BIF";
        DutyCurrencyEnum["Bmd"] = "BMD";
        DutyCurrencyEnum["Bnd"] = "BND";
        DutyCurrencyEnum["Bob"] = "BOB";
        DutyCurrencyEnum["Brl"] = "BRL";
        DutyCurrencyEnum["Bsd"] = "BSD";
        DutyCurrencyEnum["Btn"] = "BTN";
        DutyCurrencyEnum["Bwp"] = "BWP";
        DutyCurrencyEnum["Byn"] = "BYN";
        DutyCurrencyEnum["Bzd"] = "BZD";
        DutyCurrencyEnum["Cad"] = "CAD";
        DutyCurrencyEnum["Cdf"] = "CDF";
        DutyCurrencyEnum["Xaf"] = "XAF";
        DutyCurrencyEnum["Chf"] = "CHF";
        DutyCurrencyEnum["Nzd"] = "NZD";
        DutyCurrencyEnum["Clp"] = "CLP";
        DutyCurrencyEnum["Cny"] = "CNY";
        DutyCurrencyEnum["Cop"] = "COP";
        DutyCurrencyEnum["Crc"] = "CRC";
        DutyCurrencyEnum["Cuc"] = "CUC";
        DutyCurrencyEnum["Cve"] = "CVE";
        DutyCurrencyEnum["Czk"] = "CZK";
        DutyCurrencyEnum["Djf"] = "DJF";
        DutyCurrencyEnum["Dkk"] = "DKK";
        DutyCurrencyEnum["Dop"] = "DOP";
        DutyCurrencyEnum["Dzd"] = "DZD";
        DutyCurrencyEnum["Egp"] = "EGP";
        DutyCurrencyEnum["Ern"] = "ERN";
        DutyCurrencyEnum["Etb"] = "ETB";
        DutyCurrencyEnum["Fjd"] = "FJD";
        DutyCurrencyEnum["Gbp"] = "GBP";
        DutyCurrencyEnum["Gel"] = "GEL";
        DutyCurrencyEnum["Ghs"] = "GHS";
        DutyCurrencyEnum["Gmd"] = "GMD";
        DutyCurrencyEnum["Gnf"] = "GNF";
        DutyCurrencyEnum["Gtq"] = "GTQ";
        DutyCurrencyEnum["Gyd"] = "GYD";
        DutyCurrencyEnum["Hkd"] = "HKD";
        DutyCurrencyEnum["Hnl"] = "HNL";
        DutyCurrencyEnum["Hrk"] = "HRK";
        DutyCurrencyEnum["Htg"] = "HTG";
        DutyCurrencyEnum["Huf"] = "HUF";
        DutyCurrencyEnum["Idr"] = "IDR";
        DutyCurrencyEnum["Ils"] = "ILS";
        DutyCurrencyEnum["Inr"] = "INR";
        DutyCurrencyEnum["Irr"] = "IRR";
        DutyCurrencyEnum["Isk"] = "ISK";
        DutyCurrencyEnum["Jmd"] = "JMD";
        DutyCurrencyEnum["Jod"] = "JOD";
        DutyCurrencyEnum["Jpy"] = "JPY";
        DutyCurrencyEnum["Kes"] = "KES";
        DutyCurrencyEnum["Kgs"] = "KGS";
        DutyCurrencyEnum["Khr"] = "KHR";
        DutyCurrencyEnum["Kmf"] = "KMF";
        DutyCurrencyEnum["Kpw"] = "KPW";
        DutyCurrencyEnum["Krw"] = "KRW";
        DutyCurrencyEnum["Kwd"] = "KWD";
        DutyCurrencyEnum["Kyd"] = "KYD";
        DutyCurrencyEnum["Kzt"] = "KZT";
        DutyCurrencyEnum["Lak"] = "LAK";
        DutyCurrencyEnum["Lkr"] = "LKR";
        DutyCurrencyEnum["Lrd"] = "LRD";
        DutyCurrencyEnum["Lsl"] = "LSL";
        DutyCurrencyEnum["Lyd"] = "LYD";
        DutyCurrencyEnum["Mad"] = "MAD";
        DutyCurrencyEnum["Mdl"] = "MDL";
        DutyCurrencyEnum["Mga"] = "MGA";
        DutyCurrencyEnum["Mkd"] = "MKD";
        DutyCurrencyEnum["Mmk"] = "MMK";
        DutyCurrencyEnum["Mnt"] = "MNT";
        DutyCurrencyEnum["Mop"] = "MOP";
        DutyCurrencyEnum["Mro"] = "MRO";
        DutyCurrencyEnum["Mur"] = "MUR";
        DutyCurrencyEnum["Mvr"] = "MVR";
        DutyCurrencyEnum["Mwk"] = "MWK";
        DutyCurrencyEnum["Mxn"] = "MXN";
        DutyCurrencyEnum["Myr"] = "MYR";
        DutyCurrencyEnum["Mzn"] = "MZN";
        DutyCurrencyEnum["Nad"] = "NAD";
        DutyCurrencyEnum["Xpf"] = "XPF";
        DutyCurrencyEnum["Ngn"] = "NGN";
        DutyCurrencyEnum["Nio"] = "NIO";
        DutyCurrencyEnum["Nok"] = "NOK";
        DutyCurrencyEnum["Npr"] = "NPR";
        DutyCurrencyEnum["Omr"] = "OMR";
        DutyCurrencyEnum["Pen"] = "PEN";
        DutyCurrencyEnum["Pgk"] = "PGK";
        DutyCurrencyEnum["Php"] = "PHP";
        DutyCurrencyEnum["Pkr"] = "PKR";
        DutyCurrencyEnum["Pln"] = "PLN";
        DutyCurrencyEnum["Pyg"] = "PYG";
        DutyCurrencyEnum["Qar"] = "QAR";
        DutyCurrencyEnum["Rsd"] = "RSD";
        DutyCurrencyEnum["Rub"] = "RUB";
        DutyCurrencyEnum["Rwf"] = "RWF";
        DutyCurrencyEnum["Sar"] = "SAR";
        DutyCurrencyEnum["Sbd"] = "SBD";
        DutyCurrencyEnum["Scr"] = "SCR";
        DutyCurrencyEnum["Sdg"] = "SDG";
        DutyCurrencyEnum["Sek"] = "SEK";
        DutyCurrencyEnum["Sgd"] = "SGD";
        DutyCurrencyEnum["Shp"] = "SHP";
        DutyCurrencyEnum["Sll"] = "SLL";
        DutyCurrencyEnum["Sos"] = "SOS";
        DutyCurrencyEnum["Srd"] = "SRD";
        DutyCurrencyEnum["Ssp"] = "SSP";
        DutyCurrencyEnum["Std"] = "STD";
        DutyCurrencyEnum["Syp"] = "SYP";
        DutyCurrencyEnum["Szl"] = "SZL";
        DutyCurrencyEnum["Thb"] = "THB";
        DutyCurrencyEnum["Tjs"] = "TJS";
        DutyCurrencyEnum["Tnd"] = "TND";
        DutyCurrencyEnum["Top"] = "TOP";
        DutyCurrencyEnum["Try"] = "TRY";
        DutyCurrencyEnum["Ttd"] = "TTD";
        DutyCurrencyEnum["Twd"] = "TWD";
        DutyCurrencyEnum["Tzs"] = "TZS";
        DutyCurrencyEnum["Uah"] = "UAH";
        DutyCurrencyEnum["Uyu"] = "UYU";
        DutyCurrencyEnum["Uzs"] = "UZS";
        DutyCurrencyEnum["Vef"] = "VEF";
        DutyCurrencyEnum["Vnd"] = "VND";
        DutyCurrencyEnum["Vuv"] = "VUV";
        DutyCurrencyEnum["Wst"] = "WST";
        DutyCurrencyEnum["Yer"] = "YER";
        DutyCurrencyEnum["Zar"] = "ZAR";
    })(DutyCurrencyEnum || (DutyCurrencyEnum = {}));
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
    /**
    * @export
    * @enum {string}
    */
    var CustomsContentTypeEnum;
    (function (CustomsContentTypeEnum) {
        CustomsContentTypeEnum["Documents"] = "documents";
        CustomsContentTypeEnum["Gift"] = "gift";
        CustomsContentTypeEnum["Sample"] = "sample";
        CustomsContentTypeEnum["Merchandise"] = "merchandise";
        CustomsContentTypeEnum["ReturnMerchandise"] = "return_merchandise";
        CustomsContentTypeEnum["Other"] = "other";
    })(CustomsContentTypeEnum || (CustomsContentTypeEnum = {})); /**
    * @export
    * @enum {string}
    */
    var CustomsIncotermEnum;
    (function (CustomsIncotermEnum) {
        CustomsIncotermEnum["Cfr"] = "CFR";
        CustomsIncotermEnum["Cif"] = "CIF";
        CustomsIncotermEnum["Cip"] = "CIP";
        CustomsIncotermEnum["Cpt"] = "CPT";
        CustomsIncotermEnum["Daf"] = "DAF";
        CustomsIncotermEnum["Ddp"] = "DDP";
        CustomsIncotermEnum["Ddu"] = "DDU";
        CustomsIncotermEnum["Deq"] = "DEQ";
        CustomsIncotermEnum["Des"] = "DES";
        CustomsIncotermEnum["Exw"] = "EXW";
        CustomsIncotermEnum["Fas"] = "FAS";
        CustomsIncotermEnum["Fca"] = "FCA";
        CustomsIncotermEnum["Fob"] = "FOB";
    })(CustomsIncotermEnum || (CustomsIncotermEnum = {}));
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
    /**
    * @export
    * @enum {string}
    */
    var CustomsDataContentTypeEnum;
    (function (CustomsDataContentTypeEnum) {
        CustomsDataContentTypeEnum["Documents"] = "documents";
        CustomsDataContentTypeEnum["Gift"] = "gift";
        CustomsDataContentTypeEnum["Sample"] = "sample";
        CustomsDataContentTypeEnum["Merchandise"] = "merchandise";
        CustomsDataContentTypeEnum["ReturnMerchandise"] = "return_merchandise";
        CustomsDataContentTypeEnum["Other"] = "other";
    })(CustomsDataContentTypeEnum || (CustomsDataContentTypeEnum = {})); /**
    * @export
    * @enum {string}
    */
    var CustomsDataIncotermEnum;
    (function (CustomsDataIncotermEnum) {
        CustomsDataIncotermEnum["Cfr"] = "CFR";
        CustomsDataIncotermEnum["Cif"] = "CIF";
        CustomsDataIncotermEnum["Cip"] = "CIP";
        CustomsDataIncotermEnum["Cpt"] = "CPT";
        CustomsDataIncotermEnum["Daf"] = "DAF";
        CustomsDataIncotermEnum["Ddp"] = "DDP";
        CustomsDataIncotermEnum["Ddu"] = "DDU";
        CustomsDataIncotermEnum["Deq"] = "DEQ";
        CustomsDataIncotermEnum["Des"] = "DES";
        CustomsDataIncotermEnum["Exw"] = "EXW";
        CustomsDataIncotermEnum["Fas"] = "FAS";
        CustomsDataIncotermEnum["Fca"] = "FCA";
        CustomsDataIncotermEnum["Fob"] = "FOB";
    })(CustomsDataIncotermEnum || (CustomsDataIncotermEnum = {}));
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
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(CustomsFromJSON)),
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
    function MessageFromJSON(json) {
        return MessageFromJSONTyped(json);
    }
    function MessageFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'carrier_name': !exists(json, 'carrier_name') ? undefined : json['carrier_name'],
            'carrier_id': !exists(json, 'carrier_id') ? undefined : json['carrier_id'],
            'message': !exists(json, 'message') ? undefined : json['message'],
            'code': !exists(json, 'code') ? undefined : json['code'],
            'details': !exists(json, 'details') ? undefined : json['details'],
        };
    }

    /* tslint:disable */
    function MetadataFromJSON(json) {
        return MetadataFromJSONTyped(json);
    }
    function MetadataFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'app_name': json['APP_NAME'],
            'app_version': json['APP_VERSION'],
            'app_website': !exists(json, 'APP_WEBSITE') ? undefined : json['APP_WEBSITE'],
            'multi_organizations': json['MULTI_ORGANIZATIONS'],
            'orders_management': json['ORDERS_MANAGEMENT'],
            'apps_management': json['APPS_MANAGEMENT'],
            'allow_signup': json['ALLOW_SIGNUP'],
            'admin': json['ADMIN'],
            'openapi': json['OPENAPI'],
            'graphql': json['GRAPHQL'],
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  ## API Reference  Karrio is an open source multi-carrier shipping API that simplifies the integration of logistic carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2022.2`.  Read our API changelog and to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"next\": \"/v1/shipments?limit=25&offset=25\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [     ] } ```  ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.
     *
     * The version of the OpenAPI document: 2022.2
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
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
    /* eslint-disable */
    /**
     * Karrio API
     *  ## API Reference  Karrio is an open source multi-carrier shipping API that simplifies the integration of logistic carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2022.2`.  Read our API changelog and to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"next\": \"/v1/shipments?limit=25&offset=25\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [     ] } ```  ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.
     *
     * The version of the OpenAPI document: 2022.2
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
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
    /**
    * @export
    * @enum {string}
    */
    var ParcelWeightUnitEnum;
    (function (ParcelWeightUnitEnum) {
        ParcelWeightUnitEnum["Kg"] = "KG";
        ParcelWeightUnitEnum["Lb"] = "LB";
    })(ParcelWeightUnitEnum || (ParcelWeightUnitEnum = {})); /**
    * @export
    * @enum {string}
    */
    var ParcelDimensionUnitEnum;
    (function (ParcelDimensionUnitEnum) {
        ParcelDimensionUnitEnum["Cm"] = "CM";
        ParcelDimensionUnitEnum["In"] = "IN";
    })(ParcelDimensionUnitEnum || (ParcelDimensionUnitEnum = {}));
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
            'object_type': value.object_type,
        };
    }

    /* tslint:disable */
    /**
    * @export
    * @enum {string}
    */
    var PaymentPaidByEnum;
    (function (PaymentPaidByEnum) {
        PaymentPaidByEnum["Sender"] = "sender";
        PaymentPaidByEnum["Recipient"] = "recipient";
        PaymentPaidByEnum["ThirdParty"] = "third_party";
    })(PaymentPaidByEnum || (PaymentPaidByEnum = {})); /**
    * @export
    * @enum {string}
    */
    var PaymentCurrencyEnum;
    (function (PaymentCurrencyEnum) {
        PaymentCurrencyEnum["Eur"] = "EUR";
        PaymentCurrencyEnum["Aed"] = "AED";
        PaymentCurrencyEnum["Usd"] = "USD";
        PaymentCurrencyEnum["Xcd"] = "XCD";
        PaymentCurrencyEnum["Amd"] = "AMD";
        PaymentCurrencyEnum["Ang"] = "ANG";
        PaymentCurrencyEnum["Aoa"] = "AOA";
        PaymentCurrencyEnum["Ars"] = "ARS";
        PaymentCurrencyEnum["Aud"] = "AUD";
        PaymentCurrencyEnum["Awg"] = "AWG";
        PaymentCurrencyEnum["Azn"] = "AZN";
        PaymentCurrencyEnum["Bam"] = "BAM";
        PaymentCurrencyEnum["Bbd"] = "BBD";
        PaymentCurrencyEnum["Bdt"] = "BDT";
        PaymentCurrencyEnum["Xof"] = "XOF";
        PaymentCurrencyEnum["Bgn"] = "BGN";
        PaymentCurrencyEnum["Bhd"] = "BHD";
        PaymentCurrencyEnum["Bif"] = "BIF";
        PaymentCurrencyEnum["Bmd"] = "BMD";
        PaymentCurrencyEnum["Bnd"] = "BND";
        PaymentCurrencyEnum["Bob"] = "BOB";
        PaymentCurrencyEnum["Brl"] = "BRL";
        PaymentCurrencyEnum["Bsd"] = "BSD";
        PaymentCurrencyEnum["Btn"] = "BTN";
        PaymentCurrencyEnum["Bwp"] = "BWP";
        PaymentCurrencyEnum["Byn"] = "BYN";
        PaymentCurrencyEnum["Bzd"] = "BZD";
        PaymentCurrencyEnum["Cad"] = "CAD";
        PaymentCurrencyEnum["Cdf"] = "CDF";
        PaymentCurrencyEnum["Xaf"] = "XAF";
        PaymentCurrencyEnum["Chf"] = "CHF";
        PaymentCurrencyEnum["Nzd"] = "NZD";
        PaymentCurrencyEnum["Clp"] = "CLP";
        PaymentCurrencyEnum["Cny"] = "CNY";
        PaymentCurrencyEnum["Cop"] = "COP";
        PaymentCurrencyEnum["Crc"] = "CRC";
        PaymentCurrencyEnum["Cuc"] = "CUC";
        PaymentCurrencyEnum["Cve"] = "CVE";
        PaymentCurrencyEnum["Czk"] = "CZK";
        PaymentCurrencyEnum["Djf"] = "DJF";
        PaymentCurrencyEnum["Dkk"] = "DKK";
        PaymentCurrencyEnum["Dop"] = "DOP";
        PaymentCurrencyEnum["Dzd"] = "DZD";
        PaymentCurrencyEnum["Egp"] = "EGP";
        PaymentCurrencyEnum["Ern"] = "ERN";
        PaymentCurrencyEnum["Etb"] = "ETB";
        PaymentCurrencyEnum["Fjd"] = "FJD";
        PaymentCurrencyEnum["Gbp"] = "GBP";
        PaymentCurrencyEnum["Gel"] = "GEL";
        PaymentCurrencyEnum["Ghs"] = "GHS";
        PaymentCurrencyEnum["Gmd"] = "GMD";
        PaymentCurrencyEnum["Gnf"] = "GNF";
        PaymentCurrencyEnum["Gtq"] = "GTQ";
        PaymentCurrencyEnum["Gyd"] = "GYD";
        PaymentCurrencyEnum["Hkd"] = "HKD";
        PaymentCurrencyEnum["Hnl"] = "HNL";
        PaymentCurrencyEnum["Hrk"] = "HRK";
        PaymentCurrencyEnum["Htg"] = "HTG";
        PaymentCurrencyEnum["Huf"] = "HUF";
        PaymentCurrencyEnum["Idr"] = "IDR";
        PaymentCurrencyEnum["Ils"] = "ILS";
        PaymentCurrencyEnum["Inr"] = "INR";
        PaymentCurrencyEnum["Irr"] = "IRR";
        PaymentCurrencyEnum["Isk"] = "ISK";
        PaymentCurrencyEnum["Jmd"] = "JMD";
        PaymentCurrencyEnum["Jod"] = "JOD";
        PaymentCurrencyEnum["Jpy"] = "JPY";
        PaymentCurrencyEnum["Kes"] = "KES";
        PaymentCurrencyEnum["Kgs"] = "KGS";
        PaymentCurrencyEnum["Khr"] = "KHR";
        PaymentCurrencyEnum["Kmf"] = "KMF";
        PaymentCurrencyEnum["Kpw"] = "KPW";
        PaymentCurrencyEnum["Krw"] = "KRW";
        PaymentCurrencyEnum["Kwd"] = "KWD";
        PaymentCurrencyEnum["Kyd"] = "KYD";
        PaymentCurrencyEnum["Kzt"] = "KZT";
        PaymentCurrencyEnum["Lak"] = "LAK";
        PaymentCurrencyEnum["Lkr"] = "LKR";
        PaymentCurrencyEnum["Lrd"] = "LRD";
        PaymentCurrencyEnum["Lsl"] = "LSL";
        PaymentCurrencyEnum["Lyd"] = "LYD";
        PaymentCurrencyEnum["Mad"] = "MAD";
        PaymentCurrencyEnum["Mdl"] = "MDL";
        PaymentCurrencyEnum["Mga"] = "MGA";
        PaymentCurrencyEnum["Mkd"] = "MKD";
        PaymentCurrencyEnum["Mmk"] = "MMK";
        PaymentCurrencyEnum["Mnt"] = "MNT";
        PaymentCurrencyEnum["Mop"] = "MOP";
        PaymentCurrencyEnum["Mro"] = "MRO";
        PaymentCurrencyEnum["Mur"] = "MUR";
        PaymentCurrencyEnum["Mvr"] = "MVR";
        PaymentCurrencyEnum["Mwk"] = "MWK";
        PaymentCurrencyEnum["Mxn"] = "MXN";
        PaymentCurrencyEnum["Myr"] = "MYR";
        PaymentCurrencyEnum["Mzn"] = "MZN";
        PaymentCurrencyEnum["Nad"] = "NAD";
        PaymentCurrencyEnum["Xpf"] = "XPF";
        PaymentCurrencyEnum["Ngn"] = "NGN";
        PaymentCurrencyEnum["Nio"] = "NIO";
        PaymentCurrencyEnum["Nok"] = "NOK";
        PaymentCurrencyEnum["Npr"] = "NPR";
        PaymentCurrencyEnum["Omr"] = "OMR";
        PaymentCurrencyEnum["Pen"] = "PEN";
        PaymentCurrencyEnum["Pgk"] = "PGK";
        PaymentCurrencyEnum["Php"] = "PHP";
        PaymentCurrencyEnum["Pkr"] = "PKR";
        PaymentCurrencyEnum["Pln"] = "PLN";
        PaymentCurrencyEnum["Pyg"] = "PYG";
        PaymentCurrencyEnum["Qar"] = "QAR";
        PaymentCurrencyEnum["Rsd"] = "RSD";
        PaymentCurrencyEnum["Rub"] = "RUB";
        PaymentCurrencyEnum["Rwf"] = "RWF";
        PaymentCurrencyEnum["Sar"] = "SAR";
        PaymentCurrencyEnum["Sbd"] = "SBD";
        PaymentCurrencyEnum["Scr"] = "SCR";
        PaymentCurrencyEnum["Sdg"] = "SDG";
        PaymentCurrencyEnum["Sek"] = "SEK";
        PaymentCurrencyEnum["Sgd"] = "SGD";
        PaymentCurrencyEnum["Shp"] = "SHP";
        PaymentCurrencyEnum["Sll"] = "SLL";
        PaymentCurrencyEnum["Sos"] = "SOS";
        PaymentCurrencyEnum["Srd"] = "SRD";
        PaymentCurrencyEnum["Ssp"] = "SSP";
        PaymentCurrencyEnum["Std"] = "STD";
        PaymentCurrencyEnum["Syp"] = "SYP";
        PaymentCurrencyEnum["Szl"] = "SZL";
        PaymentCurrencyEnum["Thb"] = "THB";
        PaymentCurrencyEnum["Tjs"] = "TJS";
        PaymentCurrencyEnum["Tnd"] = "TND";
        PaymentCurrencyEnum["Top"] = "TOP";
        PaymentCurrencyEnum["Try"] = "TRY";
        PaymentCurrencyEnum["Ttd"] = "TTD";
        PaymentCurrencyEnum["Twd"] = "TWD";
        PaymentCurrencyEnum["Tzs"] = "TZS";
        PaymentCurrencyEnum["Uah"] = "UAH";
        PaymentCurrencyEnum["Uyu"] = "UYU";
        PaymentCurrencyEnum["Uzs"] = "UZS";
        PaymentCurrencyEnum["Vef"] = "VEF";
        PaymentCurrencyEnum["Vnd"] = "VND";
        PaymentCurrencyEnum["Vuv"] = "VUV";
        PaymentCurrencyEnum["Wst"] = "WST";
        PaymentCurrencyEnum["Yer"] = "YER";
        PaymentCurrencyEnum["Zar"] = "ZAR";
    })(PaymentCurrencyEnum || (PaymentCurrencyEnum = {}));
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
            'discount': !exists(json, 'discount') ? undefined : json['discount'],
            'base_charge': !exists(json, 'base_charge') ? undefined : json['base_charge'],
            'total_charge': !exists(json, 'total_charge') ? undefined : json['total_charge'],
            'duties_and_taxes': !exists(json, 'duties_and_taxes') ? undefined : json['duties_and_taxes'],
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
            'discount': value.discount,
            'base_charge': value.base_charge,
            'total_charge': value.total_charge,
            'duties_and_taxes': value.duties_and_taxes,
            'transit_days': value.transit_days,
            'extra_charges': value.extra_charges === undefined ? undefined : (value.extra_charges.map(ChargeToJSON)),
            'meta': value.meta,
            'test_mode': value.test_mode,
        };
    }

    /* tslint:disable */
    /**
    * @export
    * @enum {string}
    */
    var ShipmentLabelTypeEnum;
    (function (ShipmentLabelTypeEnum) {
        ShipmentLabelTypeEnum["Pdf"] = "PDF";
        ShipmentLabelTypeEnum["Zpl"] = "ZPL";
    })(ShipmentLabelTypeEnum || (ShipmentLabelTypeEnum = {})); /**
    * @export
    * @enum {string}
    */
    var ShipmentStatusEnum;
    (function (ShipmentStatusEnum) {
        ShipmentStatusEnum["Draft"] = "draft";
        ShipmentStatusEnum["Purchased"] = "purchased";
        ShipmentStatusEnum["Cancelled"] = "cancelled";
        ShipmentStatusEnum["Shipped"] = "shipped";
        ShipmentStatusEnum["InTransit"] = "in_transit";
        ShipmentStatusEnum["Delivered"] = "delivered";
    })(ShipmentStatusEnum || (ShipmentStatusEnum = {}));
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
    /**
    * @export
    * @enum {string}
    */
    var OrderStatusEnum;
    (function (OrderStatusEnum) {
        OrderStatusEnum["Unfulfilled"] = "unfulfilled";
        OrderStatusEnum["Cancelled"] = "cancelled";
        OrderStatusEnum["Fulfilled"] = "fulfilled";
        OrderStatusEnum["Delivered"] = "delivered";
        OrderStatusEnum["Partial"] = "partial";
    })(OrderStatusEnum || (OrderStatusEnum = {}));
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
            'source': !exists(json, 'source') ? undefined : json['source'],
            'status': !exists(json, 'status') ? undefined : json['status'],
            'shipping_to': AddressFromJSON(json['shipping_to']),
            'shipping_from': !exists(json, 'shipping_from') ? undefined : AddressFromJSON(json['shipping_from']),
            'line_items': (json['line_items'].map(CommodityFromJSON)),
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
            'source': value.source,
            'shipping_to': AddressDataToJSON(value.shipping_to),
            'shipping_from': AddressDataToJSON(value.shipping_from),
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
    /**
    * @export
    * @enum {string}
    */
    var ParcelDataWeightUnitEnum;
    (function (ParcelDataWeightUnitEnum) {
        ParcelDataWeightUnitEnum["Kg"] = "KG";
        ParcelDataWeightUnitEnum["Lb"] = "LB";
    })(ParcelDataWeightUnitEnum || (ParcelDataWeightUnitEnum = {})); /**
    * @export
    * @enum {string}
    */
    var ParcelDataDimensionUnitEnum;
    (function (ParcelDataDimensionUnitEnum) {
        ParcelDataDimensionUnitEnum["Cm"] = "CM";
        ParcelDataDimensionUnitEnum["In"] = "IN";
    })(ParcelDataDimensionUnitEnum || (ParcelDataDimensionUnitEnum = {}));
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
    /* eslint-disable */
    /**
     * Karrio API
     *  ## API Reference  Karrio is an open source multi-carrier shipping API that simplifies the integration of logistic carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2022.2`.  Read our API changelog and to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"next\": \"/v1/shipments?limit=25&offset=25\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [     ] } ```  ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.
     *
     * The version of the OpenAPI document: 2022.2
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
    function ReferencesFromJSON(json) {
        return ReferencesFromJSONTyped(json);
    }
    function ReferencesFromJSONTyped(json, ignoreDiscriminator) {
        if ((json === undefined) || (json === null)) {
            return json;
        }
        return {
            'app_name': json['APP_NAME'],
            'app_version': json['APP_VERSION'],
            'app_website': json['APP_WEBSITE'],
            'multi_organizations': json['MULTI_ORGANIZATIONS'],
            'orders_management': json['ORDERS_MANAGEMENT'],
            'apps_management': json['APPS_MANAGEMENT'],
            'allow_signup': json['ALLOW_SIGNUP'],
            'admin': json['ADMIN'],
            'openapi': json['OPENAPI'],
            'graphql': json['GRAPHQL'],
            'address_auto_complete': json['ADDRESS_AUTO_COMPLETE'],
            'countries': json['countries'],
            'currencies': json['currencies'],
            'carriers': json['carriers'],
            'customs_content_type': json['customs_content_type'],
            'incoterms': json['incoterms'],
            'states': json['states'],
            'services': json['services'],
            'service_names': json['service_names'],
            'options': json['options'],
            'option_names': json['option_names'],
            'package_presets': json['package_presets'],
            'packaging_types': json['packaging_types'],
            'payment_types': json['payment_types'],
            'carrier_capabilities': json['carrier_capabilities'],
            'service_levels': json['service_levels'],
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
    /**
    * @export
    * @enum {string}
    */
    var ShipmentDataLabelTypeEnum;
    (function (ShipmentDataLabelTypeEnum) {
        ShipmentDataLabelTypeEnum["Pdf"] = "PDF";
        ShipmentDataLabelTypeEnum["Zpl"] = "ZPL";
    })(ShipmentDataLabelTypeEnum || (ShipmentDataLabelTypeEnum = {}));
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
            'next': !exists(json, 'next') ? undefined : json['next'],
            'previous': !exists(json, 'previous') ? undefined : json['previous'],
            'results': (json['results'].map(ShipmentFromJSON)),
        };
    }

    /* tslint:disable */
    /**
    * @export
    * @enum {string}
    */
    var ShipmentPurchaseDataLabelTypeEnum;
    (function (ShipmentPurchaseDataLabelTypeEnum) {
        ShipmentPurchaseDataLabelTypeEnum["Pdf"] = "PDF";
        ShipmentPurchaseDataLabelTypeEnum["Zpl"] = "ZPL";
    })(ShipmentPurchaseDataLabelTypeEnum || (ShipmentPurchaseDataLabelTypeEnum = {}));
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
    /**
    * @export
    * @enum {string}
    */
    var ShipmentUpdateDataLabelTypeEnum;
    (function (ShipmentUpdateDataLabelTypeEnum) {
        ShipmentUpdateDataLabelTypeEnum["Pdf"] = "PDF";
        ShipmentUpdateDataLabelTypeEnum["Zpl"] = "ZPL";
    })(ShipmentUpdateDataLabelTypeEnum || (ShipmentUpdateDataLabelTypeEnum = {}));
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
    /**
    * @export
    * @enum {string}
    */
    var ShippingRequestLabelTypeEnum;
    (function (ShippingRequestLabelTypeEnum) {
        ShippingRequestLabelTypeEnum["Pdf"] = "PDF";
        ShippingRequestLabelTypeEnum["Zpl"] = "ZPL";
    })(ShippingRequestLabelTypeEnum || (ShippingRequestLabelTypeEnum = {}));
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
    /**
    * @export
    * @enum {string}
    */
    var ShippingResponseLabelTypeEnum;
    (function (ShippingResponseLabelTypeEnum) {
        ShippingResponseLabelTypeEnum["Pdf"] = "PDF";
        ShippingResponseLabelTypeEnum["Zpl"] = "ZPL";
    })(ShippingResponseLabelTypeEnum || (ShippingResponseLabelTypeEnum = {})); /**
    * @export
    * @enum {string}
    */
    var ShippingResponseStatusEnum;
    (function (ShippingResponseStatusEnum) {
        ShippingResponseStatusEnum["Draft"] = "draft";
        ShippingResponseStatusEnum["Purchased"] = "purchased";
        ShippingResponseStatusEnum["Cancelled"] = "cancelled";
        ShippingResponseStatusEnum["Shipped"] = "shipped";
        ShippingResponseStatusEnum["InTransit"] = "in_transit";
        ShippingResponseStatusEnum["Delivered"] = "delivered";
    })(ShippingResponseStatusEnum || (ShippingResponseStatusEnum = {}));
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
            'org_id': value.org_id,
        };
    }

    /* tslint:disable */
    /* eslint-disable */
    /**
     * Karrio API
     *  ## API Reference  Karrio is an open source multi-carrier shipping API that simplifies the integration of logistic carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2022.2`.  Read our API changelog and to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"next\": \"/v1/shipments?limit=25&offset=25\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [     ] } ```  ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.
     *
     * The version of the OpenAPI document: 2022.2
     *
     *
     * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
     * https://openapi-generator.tech
     * Do not edit the class manually.
     */
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
            'org_id': value.org_id,
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
    /**
    * @export
    * @enum {string}
    */
    var TrackingStatusStatusEnum;
    (function (TrackingStatusStatusEnum) {
        TrackingStatusStatusEnum["Pending"] = "pending";
        TrackingStatusStatusEnum["InTransit"] = "in_transit";
        TrackingStatusStatusEnum["Incident"] = "incident";
        TrackingStatusStatusEnum["Delivered"] = "delivered";
    })(TrackingStatusStatusEnum || (TrackingStatusStatusEnum = {}));
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
    /**
    * @export
    * @enum {string}
    */
    var WebhookEnabledEventsEnum;
    (function (WebhookEnabledEventsEnum) {
        WebhookEnabledEventsEnum["All"] = "all";
        WebhookEnabledEventsEnum["ShipmentPurchased"] = "shipment.purchased";
        WebhookEnabledEventsEnum["ShipmentCancelled"] = "shipment.cancelled";
        WebhookEnabledEventsEnum["ShipmentFulfilled"] = "shipment.fulfilled";
        WebhookEnabledEventsEnum["TrackerCreated"] = "tracker.created";
        WebhookEnabledEventsEnum["TrackerUpdated"] = "tracker.updated";
        WebhookEnabledEventsEnum["OrderCreated"] = "order.created";
        WebhookEnabledEventsEnum["OrderFulfilled"] = "order.fulfilled";
        WebhookEnabledEventsEnum["OrderCancelled"] = "order.cancelled";
        WebhookEnabledEventsEnum["OrderDelivered"] = "order.delivered";
    })(WebhookEnabledEventsEnum || (WebhookEnabledEventsEnum = {}));
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
            'test_mode': json['test_mode'],
            'disabled': !exists(json, 'disabled') ? undefined : json['disabled'],
            'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
            'last_event_at': !exists(json, 'last_event_at') ? undefined : (json['last_event_at'] === null ? null : new Date(json['last_event_at'])),
            'secret': json['secret'],
        };
    }

    /* tslint:disable */
    /**
    * @export
    * @enum {string}
    */
    var WebhookDataEnabledEventsEnum;
    (function (WebhookDataEnabledEventsEnum) {
        WebhookDataEnabledEventsEnum["All"] = "all";
        WebhookDataEnabledEventsEnum["ShipmentPurchased"] = "shipment.purchased";
        WebhookDataEnabledEventsEnum["ShipmentCancelled"] = "shipment.cancelled";
        WebhookDataEnabledEventsEnum["ShipmentFulfilled"] = "shipment.fulfilled";
        WebhookDataEnabledEventsEnum["TrackerCreated"] = "tracker.created";
        WebhookDataEnabledEventsEnum["TrackerUpdated"] = "tracker.updated";
        WebhookDataEnabledEventsEnum["OrderCreated"] = "order.created";
        WebhookDataEnabledEventsEnum["OrderFulfilled"] = "order.fulfilled";
        WebhookDataEnabledEventsEnum["OrderCancelled"] = "order.cancelled";
        WebhookDataEnabledEventsEnum["OrderDelivered"] = "order.delivered";
    })(WebhookDataEnabledEventsEnum || (WebhookDataEnabledEventsEnum = {}));
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
            'test_mode': value.test_mode,
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/addresses/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/addresses/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/addresses/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return ReferencesFromJSON(jsonValue); })];
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
                var queryParameters, headerParameters, response;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            queryParameters = {};
                            headerParameters = {};
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
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return MetadataFromJSON(jsonValue); })];
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
         * Verify auth token
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
         * Verify auth token
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/carriers/{carrier_name}/services".replace("{" + "carrier_name" + "}", encodeURIComponent(String(requestParameters.carrierName))),
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
                            if (requestParameters.test !== undefined) {
                                queryParameters['test'] = requestParameters.test;
                            }
                            if (requestParameters.active !== undefined) {
                                queryParameters['active'] = requestParameters.active;
                            }
                            if (requestParameters.systemOnly !== undefined) {
                                queryParameters['system_only'] = requestParameters.systemOnly;
                            }
                            headerParameters = {};
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
    /**
        * @export
        * @enum {string}
        */
    var GetServicesCarrierNameEnum;
    (function (GetServicesCarrierNameEnum) {
        GetServicesCarrierNameEnum["Aramex"] = "aramex";
        GetServicesCarrierNameEnum["Australiapost"] = "australiapost";
        GetServicesCarrierNameEnum["Canadapost"] = "canadapost";
        GetServicesCarrierNameEnum["Canpar"] = "canpar";
        GetServicesCarrierNameEnum["DhlExpress"] = "dhl_express";
        GetServicesCarrierNameEnum["DhlPoland"] = "dhl_poland";
        GetServicesCarrierNameEnum["DhlUniversal"] = "dhl_universal";
        GetServicesCarrierNameEnum["Dicom"] = "dicom";
        GetServicesCarrierNameEnum["Eshipper"] = "eshipper";
        GetServicesCarrierNameEnum["Fedex"] = "fedex";
        GetServicesCarrierNameEnum["Freightcom"] = "freightcom";
        GetServicesCarrierNameEnum["Generic"] = "generic";
        GetServicesCarrierNameEnum["Purolator"] = "purolator";
        GetServicesCarrierNameEnum["Royalmail"] = "royalmail";
        GetServicesCarrierNameEnum["Sendle"] = "sendle";
        GetServicesCarrierNameEnum["SfExpress"] = "sf_express";
        GetServicesCarrierNameEnum["Tnt"] = "tnt";
        GetServicesCarrierNameEnum["Ups"] = "ups";
        GetServicesCarrierNameEnum["Usps"] = "usps";
        GetServicesCarrierNameEnum["UspsInternational"] = "usps_international";
        GetServicesCarrierNameEnum["Yanwen"] = "yanwen";
        GetServicesCarrierNameEnum["Yunexpress"] = "yunexpress";
    })(GetServicesCarrierNameEnum || (GetServicesCarrierNameEnum = {}));
    /**
        * @export
        * @enum {string}
        */
    var ListCarrierNameEnum$2;
    (function (ListCarrierNameEnum) {
        ListCarrierNameEnum["Aramex"] = "aramex";
        ListCarrierNameEnum["Australiapost"] = "australiapost";
        ListCarrierNameEnum["Canadapost"] = "canadapost";
        ListCarrierNameEnum["Canpar"] = "canpar";
        ListCarrierNameEnum["DhlExpress"] = "dhl_express";
        ListCarrierNameEnum["DhlPoland"] = "dhl_poland";
        ListCarrierNameEnum["DhlUniversal"] = "dhl_universal";
        ListCarrierNameEnum["Dicom"] = "dicom";
        ListCarrierNameEnum["Eshipper"] = "eshipper";
        ListCarrierNameEnum["Fedex"] = "fedex";
        ListCarrierNameEnum["Freightcom"] = "freightcom";
        ListCarrierNameEnum["Generic"] = "generic";
        ListCarrierNameEnum["Purolator"] = "purolator";
        ListCarrierNameEnum["Royalmail"] = "royalmail";
        ListCarrierNameEnum["Sendle"] = "sendle";
        ListCarrierNameEnum["SfExpress"] = "sf_express";
        ListCarrierNameEnum["Tnt"] = "tnt";
        ListCarrierNameEnum["Ups"] = "ups";
        ListCarrierNameEnum["Usps"] = "usps";
        ListCarrierNameEnum["UspsInternational"] = "usps_international";
        ListCarrierNameEnum["Yanwen"] = "yanwen";
        ListCarrierNameEnum["Yunexpress"] = "yunexpress";
    })(ListCarrierNameEnum$2 || (ListCarrierNameEnum$2 = {}));

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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/customs_info/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/customs_info/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/customs_info/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/parcels/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/parcels/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/parcels/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/pickups/{id}/cancel".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
                                method: 'POST',
                                headers: headerParameters,
                                query: queryParameters,
                                body: PickupCancelDataToJSON(requestParameters.data),
                            }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OperationConfirmationFromJSON(jsonValue); })];
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
                            if (requestParameters.testMode !== undefined) {
                                queryParameters['test_mode'] = requestParameters.testMode;
                            }
                            if (requestParameters.limit !== undefined) {
                                queryParameters['limit'] = requestParameters.limit;
                            }
                            if (requestParameters.offset !== undefined) {
                                queryParameters['offset'] = requestParameters.offset;
                            }
                            headerParameters = {};
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/pickups/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                            if (requestParameters.test !== undefined) {
                                queryParameters['test'] = requestParameters.test;
                            }
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/pickups/{carrier_name}/schedule".replace("{" + "carrier_name" + "}", encodeURIComponent(String(requestParameters.carrierName))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/pickups/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
                                method: 'PATCH',
                                headers: headerParameters,
                                query: queryParameters,
                                body: PickupUpdateDataToJSON(requestParameters.data),
                            }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OperationConfirmationFromJSON(jsonValue); })];
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
                            if (requestParameters.test !== undefined) {
                                queryParameters['test'] = requestParameters.test;
                            }
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/proxy/pickups/{carrier_name}/cancel".replace("{" + "carrier_name" + "}", encodeURIComponent(String(requestParameters.carrierName))),
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
                            if (requestParameters.test !== undefined) {
                                queryParameters['test'] = requestParameters.test;
                            }
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
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
                            if (requestParameters.test !== undefined) {
                                queryParameters['test'] = requestParameters.test;
                            }
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/proxy/pickups/{carrier_name}".replace("{" + "carrier_name" + "}", encodeURIComponent(String(requestParameters.carrierName))),
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
                            if (requestParameters.test !== undefined) {
                                queryParameters['test'] = requestParameters.test;
                            }
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/proxy/tracking/{carrier_name}/{tracking_number}".replace("{" + "tracking_number" + "}", encodeURIComponent(String(requestParameters.trackingNumber))).replace("{" + "carrier_name" + "}", encodeURIComponent(String(requestParameters.carrierName))),
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
                            if (requestParameters.test !== undefined) {
                                queryParameters['test'] = requestParameters.test;
                            }
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/proxy/pickups/{carrier_name}".replace("{" + "carrier_name" + "}", encodeURIComponent(String(requestParameters.carrierName))),
                                method: 'PUT',
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
                            if (requestParameters.test !== undefined) {
                                queryParameters['test'] = requestParameters.test;
                            }
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/proxy/shipping/{carrier_name}/cancel".replace("{" + "carrier_name" + "}", encodeURIComponent(String(requestParameters.carrierName))),
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
    /**
        * @export
        * @enum {string}
        */
    var CancelPickupCarrierNameEnum;
    (function (CancelPickupCarrierNameEnum) {
        CancelPickupCarrierNameEnum["Aramex"] = "aramex";
        CancelPickupCarrierNameEnum["Australiapost"] = "australiapost";
        CancelPickupCarrierNameEnum["Canadapost"] = "canadapost";
        CancelPickupCarrierNameEnum["Canpar"] = "canpar";
        CancelPickupCarrierNameEnum["DhlExpress"] = "dhl_express";
        CancelPickupCarrierNameEnum["DhlPoland"] = "dhl_poland";
        CancelPickupCarrierNameEnum["DhlUniversal"] = "dhl_universal";
        CancelPickupCarrierNameEnum["Dicom"] = "dicom";
        CancelPickupCarrierNameEnum["Eshipper"] = "eshipper";
        CancelPickupCarrierNameEnum["Fedex"] = "fedex";
        CancelPickupCarrierNameEnum["Freightcom"] = "freightcom";
        CancelPickupCarrierNameEnum["Generic"] = "generic";
        CancelPickupCarrierNameEnum["Purolator"] = "purolator";
        CancelPickupCarrierNameEnum["Royalmail"] = "royalmail";
        CancelPickupCarrierNameEnum["Sendle"] = "sendle";
        CancelPickupCarrierNameEnum["SfExpress"] = "sf_express";
        CancelPickupCarrierNameEnum["Tnt"] = "tnt";
        CancelPickupCarrierNameEnum["Ups"] = "ups";
        CancelPickupCarrierNameEnum["Usps"] = "usps";
        CancelPickupCarrierNameEnum["UspsInternational"] = "usps_international";
        CancelPickupCarrierNameEnum["Yanwen"] = "yanwen";
        CancelPickupCarrierNameEnum["Yunexpress"] = "yunexpress";
    })(CancelPickupCarrierNameEnum || (CancelPickupCarrierNameEnum = {}));
    /**
        * @export
        * @enum {string}
        */
    var SchedulePickupCarrierNameEnum;
    (function (SchedulePickupCarrierNameEnum) {
        SchedulePickupCarrierNameEnum["Aramex"] = "aramex";
        SchedulePickupCarrierNameEnum["Australiapost"] = "australiapost";
        SchedulePickupCarrierNameEnum["Canadapost"] = "canadapost";
        SchedulePickupCarrierNameEnum["Canpar"] = "canpar";
        SchedulePickupCarrierNameEnum["DhlExpress"] = "dhl_express";
        SchedulePickupCarrierNameEnum["DhlPoland"] = "dhl_poland";
        SchedulePickupCarrierNameEnum["DhlUniversal"] = "dhl_universal";
        SchedulePickupCarrierNameEnum["Dicom"] = "dicom";
        SchedulePickupCarrierNameEnum["Eshipper"] = "eshipper";
        SchedulePickupCarrierNameEnum["Fedex"] = "fedex";
        SchedulePickupCarrierNameEnum["Freightcom"] = "freightcom";
        SchedulePickupCarrierNameEnum["Generic"] = "generic";
        SchedulePickupCarrierNameEnum["Purolator"] = "purolator";
        SchedulePickupCarrierNameEnum["Royalmail"] = "royalmail";
        SchedulePickupCarrierNameEnum["Sendle"] = "sendle";
        SchedulePickupCarrierNameEnum["SfExpress"] = "sf_express";
        SchedulePickupCarrierNameEnum["Tnt"] = "tnt";
        SchedulePickupCarrierNameEnum["Ups"] = "ups";
        SchedulePickupCarrierNameEnum["Usps"] = "usps";
        SchedulePickupCarrierNameEnum["UspsInternational"] = "usps_international";
        SchedulePickupCarrierNameEnum["Yanwen"] = "yanwen";
        SchedulePickupCarrierNameEnum["Yunexpress"] = "yunexpress";
    })(SchedulePickupCarrierNameEnum || (SchedulePickupCarrierNameEnum = {}));
    /**
        * @export
        * @enum {string}
        */
    var TrackShipmentCarrierNameEnum;
    (function (TrackShipmentCarrierNameEnum) {
        TrackShipmentCarrierNameEnum["Aramex"] = "aramex";
        TrackShipmentCarrierNameEnum["Australiapost"] = "australiapost";
        TrackShipmentCarrierNameEnum["Canadapost"] = "canadapost";
        TrackShipmentCarrierNameEnum["Canpar"] = "canpar";
        TrackShipmentCarrierNameEnum["DhlExpress"] = "dhl_express";
        TrackShipmentCarrierNameEnum["DhlPoland"] = "dhl_poland";
        TrackShipmentCarrierNameEnum["DhlUniversal"] = "dhl_universal";
        TrackShipmentCarrierNameEnum["Dicom"] = "dicom";
        TrackShipmentCarrierNameEnum["Eshipper"] = "eshipper";
        TrackShipmentCarrierNameEnum["Fedex"] = "fedex";
        TrackShipmentCarrierNameEnum["Freightcom"] = "freightcom";
        TrackShipmentCarrierNameEnum["Generic"] = "generic";
        TrackShipmentCarrierNameEnum["Purolator"] = "purolator";
        TrackShipmentCarrierNameEnum["Royalmail"] = "royalmail";
        TrackShipmentCarrierNameEnum["Sendle"] = "sendle";
        TrackShipmentCarrierNameEnum["SfExpress"] = "sf_express";
        TrackShipmentCarrierNameEnum["Tnt"] = "tnt";
        TrackShipmentCarrierNameEnum["Ups"] = "ups";
        TrackShipmentCarrierNameEnum["Usps"] = "usps";
        TrackShipmentCarrierNameEnum["UspsInternational"] = "usps_international";
        TrackShipmentCarrierNameEnum["Yanwen"] = "yanwen";
        TrackShipmentCarrierNameEnum["Yunexpress"] = "yunexpress";
    })(TrackShipmentCarrierNameEnum || (TrackShipmentCarrierNameEnum = {}));
    /**
        * @export
        * @enum {string}
        */
    var UpdatePickupCarrierNameEnum;
    (function (UpdatePickupCarrierNameEnum) {
        UpdatePickupCarrierNameEnum["Aramex"] = "aramex";
        UpdatePickupCarrierNameEnum["Australiapost"] = "australiapost";
        UpdatePickupCarrierNameEnum["Canadapost"] = "canadapost";
        UpdatePickupCarrierNameEnum["Canpar"] = "canpar";
        UpdatePickupCarrierNameEnum["DhlExpress"] = "dhl_express";
        UpdatePickupCarrierNameEnum["DhlPoland"] = "dhl_poland";
        UpdatePickupCarrierNameEnum["DhlUniversal"] = "dhl_universal";
        UpdatePickupCarrierNameEnum["Dicom"] = "dicom";
        UpdatePickupCarrierNameEnum["Eshipper"] = "eshipper";
        UpdatePickupCarrierNameEnum["Fedex"] = "fedex";
        UpdatePickupCarrierNameEnum["Freightcom"] = "freightcom";
        UpdatePickupCarrierNameEnum["Generic"] = "generic";
        UpdatePickupCarrierNameEnum["Purolator"] = "purolator";
        UpdatePickupCarrierNameEnum["Royalmail"] = "royalmail";
        UpdatePickupCarrierNameEnum["Sendle"] = "sendle";
        UpdatePickupCarrierNameEnum["SfExpress"] = "sf_express";
        UpdatePickupCarrierNameEnum["Tnt"] = "tnt";
        UpdatePickupCarrierNameEnum["Ups"] = "ups";
        UpdatePickupCarrierNameEnum["Usps"] = "usps";
        UpdatePickupCarrierNameEnum["UspsInternational"] = "usps_international";
        UpdatePickupCarrierNameEnum["Yanwen"] = "yanwen";
        UpdatePickupCarrierNameEnum["Yunexpress"] = "yunexpress";
    })(UpdatePickupCarrierNameEnum || (UpdatePickupCarrierNameEnum = {}));
    /**
        * @export
        * @enum {string}
        */
    var VoidLabelCarrierNameEnum;
    (function (VoidLabelCarrierNameEnum) {
        VoidLabelCarrierNameEnum["Aramex"] = "aramex";
        VoidLabelCarrierNameEnum["Australiapost"] = "australiapost";
        VoidLabelCarrierNameEnum["Canadapost"] = "canadapost";
        VoidLabelCarrierNameEnum["Canpar"] = "canpar";
        VoidLabelCarrierNameEnum["DhlExpress"] = "dhl_express";
        VoidLabelCarrierNameEnum["DhlPoland"] = "dhl_poland";
        VoidLabelCarrierNameEnum["DhlUniversal"] = "dhl_universal";
        VoidLabelCarrierNameEnum["Dicom"] = "dicom";
        VoidLabelCarrierNameEnum["Eshipper"] = "eshipper";
        VoidLabelCarrierNameEnum["Fedex"] = "fedex";
        VoidLabelCarrierNameEnum["Freightcom"] = "freightcom";
        VoidLabelCarrierNameEnum["Generic"] = "generic";
        VoidLabelCarrierNameEnum["Purolator"] = "purolator";
        VoidLabelCarrierNameEnum["Royalmail"] = "royalmail";
        VoidLabelCarrierNameEnum["Sendle"] = "sendle";
        VoidLabelCarrierNameEnum["SfExpress"] = "sf_express";
        VoidLabelCarrierNameEnum["Tnt"] = "tnt";
        VoidLabelCarrierNameEnum["Ups"] = "ups";
        VoidLabelCarrierNameEnum["Usps"] = "usps";
        VoidLabelCarrierNameEnum["UspsInternational"] = "usps_international";
        VoidLabelCarrierNameEnum["Yanwen"] = "yanwen";
        VoidLabelCarrierNameEnum["Yunexpress"] = "yunexpress";
    })(VoidLabelCarrierNameEnum || (VoidLabelCarrierNameEnum = {}));

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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/shipments/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
                                method: 'DELETE',
                                headers: headerParameters,
                                query: queryParameters,
                            }, initOverrides)];
                        case 1:
                            response = _a.sent();
                            return [2 /*return*/, new JSONApiResponse(response, function (jsonValue) { return OperationResponseFromJSON(jsonValue); })];
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
                            if (requestParameters.test !== undefined) {
                                queryParameters['test'] = requestParameters.test;
                            }
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
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
                            if (requestParameters.testMode !== undefined) {
                                queryParameters['test_mode'] = requestParameters.testMode;
                            }
                            if (requestParameters.status !== undefined) {
                                queryParameters['status'] = requestParameters.status;
                            }
                            if (requestParameters.createdAfter !== undefined) {
                                queryParameters['created_after'] = requestParameters.createdAfter.toISOString();
                            }
                            if (requestParameters.createdBefore !== undefined) {
                                queryParameters['created_before'] = requestParameters.createdBefore.toISOString();
                            }
                            if (requestParameters.carrierId !== undefined) {
                                queryParameters['carrier_id'] = requestParameters.carrierId;
                            }
                            if (requestParameters.service !== undefined) {
                                queryParameters['service'] = requestParameters.service;
                            }
                            if (requestParameters.reference !== undefined) {
                                queryParameters['reference'] = requestParameters.reference;
                            }
                            if (requestParameters.limit !== undefined) {
                                queryParameters['limit'] = requestParameters.limit;
                            }
                            if (requestParameters.offset !== undefined) {
                                queryParameters['offset'] = requestParameters.offset;
                            }
                            if (requestParameters.carrierName !== undefined) {
                                queryParameters['carrier_name'] = requestParameters.carrierName;
                            }
                            headerParameters = {};
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/shipments/{id}/purchase".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/shipments/{id}/rates".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/shipments/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/shipments/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
    /**
        * @export
        * @enum {string}
        */
    var ListStatusEnum$2;
    (function (ListStatusEnum) {
        ListStatusEnum["Draft"] = "draft";
        ListStatusEnum["Purchased"] = "purchased";
        ListStatusEnum["Cancelled"] = "cancelled";
        ListStatusEnum["Shipped"] = "shipped";
        ListStatusEnum["InTransit"] = "in_transit";
        ListStatusEnum["Delivered"] = "delivered";
    })(ListStatusEnum$2 || (ListStatusEnum$2 = {}));
    /**
        * @export
        * @enum {string}
        */
    var ListCarrierNameEnum$1;
    (function (ListCarrierNameEnum) {
        ListCarrierNameEnum["Aramex"] = "aramex";
        ListCarrierNameEnum["Australiapost"] = "australiapost";
        ListCarrierNameEnum["Canadapost"] = "canadapost";
        ListCarrierNameEnum["Canpar"] = "canpar";
        ListCarrierNameEnum["DhlExpress"] = "dhl_express";
        ListCarrierNameEnum["DhlPoland"] = "dhl_poland";
        ListCarrierNameEnum["DhlUniversal"] = "dhl_universal";
        ListCarrierNameEnum["Dicom"] = "dicom";
        ListCarrierNameEnum["Eshipper"] = "eshipper";
        ListCarrierNameEnum["Fedex"] = "fedex";
        ListCarrierNameEnum["Freightcom"] = "freightcom";
        ListCarrierNameEnum["Generic"] = "generic";
        ListCarrierNameEnum["Purolator"] = "purolator";
        ListCarrierNameEnum["Royalmail"] = "royalmail";
        ListCarrierNameEnum["Sendle"] = "sendle";
        ListCarrierNameEnum["SfExpress"] = "sf_express";
        ListCarrierNameEnum["Tnt"] = "tnt";
        ListCarrierNameEnum["Ups"] = "ups";
        ListCarrierNameEnum["Usps"] = "usps";
        ListCarrierNameEnum["UspsInternational"] = "usps_international";
        ListCarrierNameEnum["Yanwen"] = "yanwen";
        ListCarrierNameEnum["Yunexpress"] = "yunexpress";
    })(ListCarrierNameEnum$1 || (ListCarrierNameEnum$1 = {}));

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
                            if (requestParameters.test !== undefined) {
                                queryParameters['test'] = requestParameters.test;
                            }
                            headerParameters = {};
                            if (this.configuration && this.configuration.apiKey) {
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/trackers/{carrier_name}/{tracking_number}".replace("{" + "tracking_number" + "}", encodeURIComponent(String(requestParameters.trackingNumber))).replace("{" + "carrier_name" + "}", encodeURIComponent(String(requestParameters.carrierName))),
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
                            if (requestParameters.testMode !== undefined) {
                                queryParameters['test_mode'] = requestParameters.testMode;
                            }
                            if (requestParameters.status !== undefined) {
                                queryParameters['status'] = requestParameters.status;
                            }
                            if (requestParameters.createdAfter !== undefined) {
                                queryParameters['created_after'] = requestParameters.createdAfter.toISOString();
                            }
                            if (requestParameters.createdBefore !== undefined) {
                                queryParameters['created_before'] = requestParameters.createdBefore.toISOString();
                            }
                            if (requestParameters.carrierId !== undefined) {
                                queryParameters['carrier_id'] = requestParameters.carrierId;
                            }
                            if (requestParameters.limit !== undefined) {
                                queryParameters['limit'] = requestParameters.limit;
                            }
                            if (requestParameters.offset !== undefined) {
                                queryParameters['offset'] = requestParameters.offset;
                            }
                            if (requestParameters.carrierName !== undefined) {
                                queryParameters['carrier_name'] = requestParameters.carrierName;
                            }
                            headerParameters = {};
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/trackers/{id_or_tracking_number}".replace("{" + "id_or_tracking_number" + "}", encodeURIComponent(String(requestParameters.idOrTrackingNumber))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/trackers/{id_or_tracking_number}".replace("{" + "id_or_tracking_number" + "}", encodeURIComponent(String(requestParameters.idOrTrackingNumber))),
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
    /**
        * @export
        * @enum {string}
        */
    var CreateCarrierNameEnum;
    (function (CreateCarrierNameEnum) {
        CreateCarrierNameEnum["Aramex"] = "aramex";
        CreateCarrierNameEnum["Australiapost"] = "australiapost";
        CreateCarrierNameEnum["Canadapost"] = "canadapost";
        CreateCarrierNameEnum["Canpar"] = "canpar";
        CreateCarrierNameEnum["DhlExpress"] = "dhl_express";
        CreateCarrierNameEnum["DhlPoland"] = "dhl_poland";
        CreateCarrierNameEnum["DhlUniversal"] = "dhl_universal";
        CreateCarrierNameEnum["Dicom"] = "dicom";
        CreateCarrierNameEnum["Eshipper"] = "eshipper";
        CreateCarrierNameEnum["Fedex"] = "fedex";
        CreateCarrierNameEnum["Freightcom"] = "freightcom";
        CreateCarrierNameEnum["Generic"] = "generic";
        CreateCarrierNameEnum["Purolator"] = "purolator";
        CreateCarrierNameEnum["Royalmail"] = "royalmail";
        CreateCarrierNameEnum["Sendle"] = "sendle";
        CreateCarrierNameEnum["SfExpress"] = "sf_express";
        CreateCarrierNameEnum["Tnt"] = "tnt";
        CreateCarrierNameEnum["Ups"] = "ups";
        CreateCarrierNameEnum["Usps"] = "usps";
        CreateCarrierNameEnum["UspsInternational"] = "usps_international";
        CreateCarrierNameEnum["Yanwen"] = "yanwen";
        CreateCarrierNameEnum["Yunexpress"] = "yunexpress";
    })(CreateCarrierNameEnum || (CreateCarrierNameEnum = {}));
    /**
        * @export
        * @enum {string}
        */
    var ListStatusEnum$1;
    (function (ListStatusEnum) {
        ListStatusEnum["Pending"] = "pending";
        ListStatusEnum["InTransit"] = "in_transit";
        ListStatusEnum["Incident"] = "incident";
        ListStatusEnum["Delivered"] = "delivered";
    })(ListStatusEnum$1 || (ListStatusEnum$1 = {}));
    /**
        * @export
        * @enum {string}
        */
    var ListCarrierNameEnum;
    (function (ListCarrierNameEnum) {
        ListCarrierNameEnum["Aramex"] = "aramex";
        ListCarrierNameEnum["Australiapost"] = "australiapost";
        ListCarrierNameEnum["Canadapost"] = "canadapost";
        ListCarrierNameEnum["Canpar"] = "canpar";
        ListCarrierNameEnum["DhlExpress"] = "dhl_express";
        ListCarrierNameEnum["DhlPoland"] = "dhl_poland";
        ListCarrierNameEnum["DhlUniversal"] = "dhl_universal";
        ListCarrierNameEnum["Dicom"] = "dicom";
        ListCarrierNameEnum["Eshipper"] = "eshipper";
        ListCarrierNameEnum["Fedex"] = "fedex";
        ListCarrierNameEnum["Freightcom"] = "freightcom";
        ListCarrierNameEnum["Generic"] = "generic";
        ListCarrierNameEnum["Purolator"] = "purolator";
        ListCarrierNameEnum["Royalmail"] = "royalmail";
        ListCarrierNameEnum["Sendle"] = "sendle";
        ListCarrierNameEnum["SfExpress"] = "sf_express";
        ListCarrierNameEnum["Tnt"] = "tnt";
        ListCarrierNameEnum["Ups"] = "ups";
        ListCarrierNameEnum["Usps"] = "usps";
        ListCarrierNameEnum["UspsInternational"] = "usps_international";
        ListCarrierNameEnum["Yanwen"] = "yanwen";
        ListCarrierNameEnum["Yunexpress"] = "yunexpress";
    })(ListCarrierNameEnum || (ListCarrierNameEnum = {}));

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
                            if (requestParameters.testMode !== undefined) {
                                queryParameters['test_mode'] = requestParameters.testMode;
                            }
                            headerParameters = {};
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/webhooks/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/webhooks/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/webhooks/{id}/test".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/webhooks/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/orders/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                            if (requestParameters.test !== undefined) {
                                queryParameters['test'] = requestParameters.test;
                            }
                            headerParameters = {};
                            headerParameters['Content-Type'] = 'application/json';
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
                            if (requestParameters.testMode !== undefined) {
                                queryParameters['test_mode'] = requestParameters.testMode;
                            }
                            if (requestParameters.status !== undefined) {
                                queryParameters['status'] = requestParameters.status;
                            }
                            if (requestParameters.createdAfter !== undefined) {
                                queryParameters['created_after'] = requestParameters.createdAfter.toISOString();
                            }
                            if (requestParameters.createdBefore !== undefined) {
                                queryParameters['created_before'] = requestParameters.createdBefore.toISOString();
                            }
                            if (requestParameters.limit !== undefined) {
                                queryParameters['limit'] = requestParameters.limit;
                            }
                            if (requestParameters.offset !== undefined) {
                                queryParameters['offset'] = requestParameters.offset;
                            }
                            headerParameters = {};
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/orders/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
                                headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // Token authentication
                            }
                            return [4 /*yield*/, this.request({
                                path: "/v1/orders/{id}".replace("{" + "id" + "}", encodeURIComponent(String(requestParameters.id))),
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
    /**
        * @export
        * @enum {string}
        */
    var ListStatusEnum;
    (function (ListStatusEnum) {
        ListStatusEnum["Unfulfilled"] = "unfulfilled";
        ListStatusEnum["Cancelled"] = "cancelled";
        ListStatusEnum["Fulfilled"] = "fulfilled";
        ListStatusEnum["Delivered"] = "delivered";
        ListStatusEnum["Partial"] = "partial";
    })(ListStatusEnum || (ListStatusEnum = {}));

    var KarrioClient = /** @class */ (function () {
        function KarrioClient(clientConfig) {
            var config = new Configuration(__assign({
                credentials: "include", headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            }, clientConfig));
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
        if (host === void 0) { host = 'https://app.karrio.io'; }
        if (apiKeyPrefix === void 0) { apiKeyPrefix = 'Token'; }
        var clientConfig = {
            basePath: host,
            apiKey: apiKeyPrefix + " " + apiKey,
        };
        return new KarrioClient(clientConfig);
    }
    Karrio.Client = KarrioClient;

    return Karrio;

}));
//# sourceMappingURL=karrio.js.map
