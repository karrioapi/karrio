import{v as d,R as y,u as p,a as k,d as f}from"./globals-Bbmrmuzb.js";/**
 * @license lucide-react v0.525.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const w=[["path",{d:"M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49",key:"ct8e1f"}],["path",{d:"M14.084 14.158a3 3 0 0 1-4.242-4.242",key:"151rxh"}],["path",{d:"M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143",key:"13bj9a"}],["path",{d:"m2 2 20 20",key:"1ooewy"}]],l=d("eye-off",w);/**
 * @license lucide-react v0.525.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const m=[["path",{d:"M12 20h9",key:"t2du7b"}],["path",{d:"M16.376 3.622a1 1 0 0 1 3.002 3.002L7.368 18.635a2 2 0 0 1-.855.506l-2.872.838a.5.5 0 0 1-.62-.62l.838-2.872a2 2 0 0 1 .506-.854z",key:"1ykcvy"}]],v=d("pen-line",m);/**
 * @license lucide-react v0.525.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const q=[["path",{d:"M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8",key:"1357e3"}],["path",{d:"M3 3v5h5",key:"1xhq8a"}]],M=d("rotate-ccw",q);y.createContext({});function g(){const{host:o,token:i,headers:r,graphqlRequest:c}=p();return y.useMemo(()=>{const s=async(e,a,u)=>{const n=await fetch(`${o}${a}`,{method:e,headers:r,body:u?JSON.stringify(u):void 0}),t=await n.json();if(!n.ok){const h=new Error((t==null?void 0:t.detail)||(t==null?void 0:t.message)||"Request failed");throw h.response={status:n.status,data:t},h}return{data:t,status:n.status}};return{graphql:{request:c},webhooks:{create:({webhookData:e})=>s("POST","/v1/webhooks",e),update:({id:e,patchedWebhookData:a})=>s("PATCH",`/v1/webhooks/${e}`,a),remove:({id:e})=>s("DELETE",`/v1/webhooks/${e}`),test:({id:e,webhookTestRequest:a})=>s("POST",`/v1/webhooks/${e}/test`,a)},documents:{generateDocument:({documentData:e})=>s("POST","/v1/documents/generate",e)},axios:{post:async(e,a)=>s("POST",e,a),get:async e=>s("GET",e)},isAuthenticated:!0,pageData:{}}},[o,i,r,c])}function E(o){const{enabled:i=!0,requireAuth:r,...c}=o;return k({...c,enabled:i,retry:(s,e)=>{var a,u,n,t;return((n=(u=(a=e==null?void 0:e.response)==null?void 0:a.errors)==null?void 0:u[0])==null?void 0:n.code)==="authentication_required"||(t=e==null?void 0:e.message)!=null&&t.includes("authentication")?!1:s<1}})}function _(o){return f(o)}export{l as E,v as P,M as R,E as a,_ as b,g as u};
