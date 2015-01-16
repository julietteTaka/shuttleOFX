/* Modernizr 2.7.1 (Custom Build) | MIT & BSD */
;window.Modernizr=function(a,b,c){function A(a){j.cssText=a}function B(a,b){return A(m.join(a+";")+(b||""))}function C(a,b){return typeof a===b}function D(a,b){return!!~(""+a).indexOf(b)}function E(a,b){for(var d in a){var e=a[d];if(!D(e,"-")&&j[e]!==c)return b=="pfx"?e:!0}return!1}function F(a,b,d){for(var e in a){var f=b[a[e]];if(f!==c)return d===!1?a[e]:C(f,"function")?f.bind(d||b):f}return!1}function G(a,b,c){var d=a.charAt(0).toUpperCase()+a.slice(1),e=(a+" "+o.join(d+" ")+d).split(" ");return C(b,"string")||C(b,"undefined")?E(e,b):(e=(a+" "+p.join(d+" ")+d).split(" "),F(e,b,c))}var d="2.7.1",e={},f=!0,g=b.documentElement,h="modernizr",i=b.createElement(h),j=i.style,k,l={}.toString,m=" -webkit- -moz- -o- -ms- ".split(" "),n="Webkit Moz O ms",o=n.split(" "),p=n.toLowerCase().split(" "),q={svg:"http://www.w3.org/2000/svg"},r={},s={},t={},u=[],v=u.slice,w,x=function(a,c,d,e){var f,i,j,k,l=b.createElement("div"),m=b.body,n=m||b.createElement("body");if(parseInt(d,10))while(d--)j=b.createElement("div"),j.id=e?e[d]:h+(d+1),l.appendChild(j);return f=["&#173;",'<style id="s',h,'">',a,"</style>"].join(""),l.id=h,(m?l:n).innerHTML+=f,n.appendChild(l),m||(n.style.background="",n.style.overflow="hidden",k=g.style.overflow,g.style.overflow="hidden",g.appendChild(n)),i=c(l,a),m?l.parentNode.removeChild(l):(n.parentNode.removeChild(n),g.style.overflow=k),!!i},y={}.hasOwnProperty,z;!C(y,"undefined")&&!C(y.call,"undefined")?z=function(a,b){return y.call(a,b)}:z=function(a,b){return b in a&&C(a.constructor.prototype[b],"undefined")},Function.prototype.bind||(Function.prototype.bind=function(b){var c=this;if(typeof c!="function")throw new TypeError;var d=v.call(arguments,1),e=function(){if(this instanceof e){var a=function(){};a.prototype=c.prototype;var f=new a,g=c.apply(f,d.concat(v.call(arguments)));return Object(g)===g?g:f}return c.apply(b,d.concat(v.call(arguments)))};return e}),r.flexbox=function(){return G("flexWrap")},r.canvas=function(){var a=b.createElement("canvas");return!!a.getContext&&!!a.getContext("2d")},r.rgba=function(){return A("background-color:rgba(150,255,150,.5)"),D(j.backgroundColor,"rgba")},r.backgroundsize=function(){return G("backgroundSize")},r.borderradius=function(){return G("borderRadius")},r.boxshadow=function(){return G("boxShadow")},r.cssanimations=function(){return G("animationName")},r.csstransforms=function(){return!!G("transform")},r.csstransforms3d=function(){var a=!!G("perspective");return a&&"webkitPerspective"in g.style&&x("@media (transform-3d),(-webkit-transform-3d){#modernizr{left:9px;position:absolute;height:3px;}}",function(b,c){a=b.offsetLeft===9&&b.offsetHeight===3}),a},r.csstransitions=function(){return G("transition")},r.video=function(){var a=b.createElement("video"),c=!1;try{if(c=!!a.canPlayType)c=new Boolean(c),c.ogg=a.canPlayType('video/ogg; codecs="theora"').replace(/^no$/,""),c.h264=a.canPlayType('video/mp4; codecs="avc1.42E01E"').replace(/^no$/,""),c.webm=a.canPlayType('video/webm; codecs="vp8, vorbis"').replace(/^no$/,"")}catch(d){}return c},r.audio=function(){var a=b.createElement("audio"),c=!1;try{if(c=!!a.canPlayType)c=new Boolean(c),c.ogg=a.canPlayType('audio/ogg; codecs="vorbis"').replace(/^no$/,""),c.mp3=a.canPlayType("audio/mpeg;").replace(/^no$/,""),c.wav=a.canPlayType('audio/wav; codecs="1"').replace(/^no$/,""),c.m4a=(a.canPlayType("audio/x-m4a;")||a.canPlayType("audio/aac;")).replace(/^no$/,"")}catch(d){}return c},r.svg=function(){return!!b.createElementNS&&!!b.createElementNS(q.svg,"svg").createSVGRect};for(var H in r)z(r,H)&&(w=H.toLowerCase(),e[w]=r[H](),u.push((e[w]?"":"no-")+w));return e.addTest=function(a,b){if(typeof a=="object")for(var d in a)z(a,d)&&e.addTest(d,a[d]);else{a=a.toLowerCase();if(e[a]!==c)return e;b=typeof b=="function"?b():b,typeof f!="undefined"&&f&&(g.className+=" "+(b?"":"no-")+a),e[a]=b}return e},A(""),i=k=null,function(a,b){function l(a,b){var c=a.createElement("p"),d=a.getElementsByTagName("head")[0]||a.documentElement;return c.innerHTML="x<style>"+b+"</style>",d.insertBefore(c.lastChild,d.firstChild)}function m(){var a=s.elements;return typeof a=="string"?a.split(" "):a}function n(a){var b=j[a[h]];return b||(b={},i++,a[h]=i,j[i]=b),b}function o(a,c,d){c||(c=b);if(k)return c.createElement(a);d||(d=n(c));var g;return d.cache[a]?g=d.cache[a].cloneNode():f.test(a)?g=(d.cache[a]=d.createElem(a)).cloneNode():g=d.createElem(a),g.canHaveChildren&&!e.test(a)&&!g.tagUrn?d.frag.appendChild(g):g}function p(a,c){a||(a=b);if(k)return a.createDocumentFragment();c=c||n(a);var d=c.frag.cloneNode(),e=0,f=m(),g=f.length;for(;e<g;e++)d.createElement(f[e]);return d}function q(a,b){b.cache||(b.cache={},b.createElem=a.createElement,b.createFrag=a.createDocumentFragment,b.frag=b.createFrag()),a.createElement=function(c){return s.shivMethods?o(c,a,b):b.createElem(c)},a.createDocumentFragment=Function("h,f","return function(){var n=f.cloneNode(),c=n.createElement;h.shivMethods&&("+m().join().replace(/[\w\-]+/g,function(a){return b.createElem(a),b.frag.createElement(a),'c("'+a+'")'})+");return n}")(s,b.frag)}function r(a){a||(a=b);var c=n(a);return s.shivCSS&&!g&&!c.hasCSS&&(c.hasCSS=!!l(a,"article,aside,dialog,figcaption,figure,footer,header,hgroup,main,nav,section{display:block}mark{background:#FF0;color:#000}template{display:none}")),k||q(a,c),a}var c="3.7.0",d=a.html5||{},e=/^<|^(?:button|map|select|textarea|object|iframe|option|optgroup)$/i,f=/^(?:a|b|code|div|fieldset|h1|h2|h3|h4|h5|h6|i|label|li|ol|p|q|span|strong|style|table|tbody|td|th|tr|ul)$/i,g,h="_html5shiv",i=0,j={},k;(function(){try{var a=b.createElement("a");a.innerHTML="<xyz></xyz>",g="hidden"in a,k=a.childNodes.length==1||function(){b.createElement("a");var a=b.createDocumentFragment();return typeof a.cloneNode=="undefined"||typeof a.createDocumentFragment=="undefined"||typeof a.createElement=="undefined"}()}catch(c){g=!0,k=!0}})();var s={elements:d.elements||"abbr article aside audio bdi canvas data datalist details dialog figcaption figure footer header hgroup main mark meter nav output progress section summary template time video",version:c,shivCSS:d.shivCSS!==!1,supportsUnknownElements:k,shivMethods:d.shivMethods!==!1,type:"default",shivDocument:r,createElement:o,createDocumentFragment:p};a.html5=s,r(b)}(this,b),e._version=d,e._prefixes=m,e._domPrefixes=p,e._cssomPrefixes=o,e.testProp=function(a){return E([a])},e.testAllProps=G,e.testStyles=x,e.prefixed=function(a,b,c){return b?G(a,b,c):G(a,"pfx")},g.className=g.className.replace(/(^|\s)no-js(\s|$)/,"$1$2")+(f?" js "+u.join(" "):""),e}(this,this.document),function(a,b,c){function d(a){return"[object Function]"==o.call(a)}function e(a){return"string"==typeof a}function f(){}function g(a){return!a||"loaded"==a||"complete"==a||"uninitialized"==a}function h(){var a=p.shift();q=1,a?a.t?m(function(){("c"==a.t?B.injectCss:B.injectJs)(a.s,0,a.a,a.x,a.e,1)},0):(a(),h()):q=0}function i(a,c,d,e,f,i,j){function k(b){if(!o&&g(l.readyState)&&(u.r=o=1,!q&&h(),l.onload=l.onreadystatechange=null,b)){"img"!=a&&m(function(){t.removeChild(l)},50);for(var d in y[c])y[c].hasOwnProperty(d)&&y[c][d].onload()}}var j=j||B.errorTimeout,l=b.createElement(a),o=0,r=0,u={t:d,s:c,e:f,a:i,x:j};1===y[c]&&(r=1,y[c]=[]),"object"==a?l.data=c:(l.src=c,l.type=a),l.width=l.height="0",l.onerror=l.onload=l.onreadystatechange=function(){k.call(this,r)},p.splice(e,0,u),"img"!=a&&(r||2===y[c]?(t.insertBefore(l,s?null:n),m(k,j)):y[c].push(l))}function j(a,b,c,d,f){return q=0,b=b||"j",e(a)?i("c"==b?v:u,a,b,this.i++,c,d,f):(p.splice(this.i++,0,a),1==p.length&&h()),this}function k(){var a=B;return a.loader={load:j,i:0},a}var l=b.documentElement,m=a.setTimeout,n=b.getElementsByTagName("script")[0],o={}.toString,p=[],q=0,r="MozAppearance"in l.style,s=r&&!!b.createRange().compareNode,t=s?l:n.parentNode,l=a.opera&&"[object Opera]"==o.call(a.opera),l=!!b.attachEvent&&!l,u=r?"object":l?"script":"img",v=l?"script":u,w=Array.isArray||function(a){return"[object Array]"==o.call(a)},x=[],y={},z={timeout:function(a,b){return b.length&&(a.timeout=b[0]),a}},A,B;B=function(a){function b(a){var a=a.split("!"),b=x.length,c=a.pop(),d=a.length,c={url:c,origUrl:c,prefixes:a},e,f,g;for(f=0;f<d;f++)g=a[f].split("="),(e=z[g.shift()])&&(c=e(c,g));for(f=0;f<b;f++)c=x[f](c);return c}function g(a,e,f,g,h){var i=b(a),j=i.autoCallback;i.url.split(".").pop().split("?").shift(),i.bypass||(e&&(e=d(e)?e:e[a]||e[g]||e[a.split("/").pop().split("?")[0]]),i.instead?i.instead(a,e,f,g,h):(y[i.url]?i.noexec=!0:y[i.url]=1,f.load(i.url,i.forceCSS||!i.forceJS&&"css"==i.url.split(".").pop().split("?").shift()?"c":c,i.noexec,i.attrs,i.timeout),(d(e)||d(j))&&f.load(function(){k(),e&&e(i.origUrl,h,g),j&&j(i.origUrl,h,g),y[i.url]=2})))}function h(a,b){function c(a,c){if(a){if(e(a))c||(j=function(){var a=[].slice.call(arguments);k.apply(this,a),l()}),g(a,j,b,0,h);else if(Object(a)===a)for(n in m=function(){var b=0,c;for(c in a)a.hasOwnProperty(c)&&b++;return b}(),a)a.hasOwnProperty(n)&&(!c&&!--m&&(d(j)?j=function(){var a=[].slice.call(arguments);k.apply(this,a),l()}:j[n]=function(a){return function(){var b=[].slice.call(arguments);a&&a.apply(this,b),l()}}(k[n])),g(a[n],j,b,n,h))}else!c&&l()}var h=!!a.test,i=a.load||a.both,j=a.callback||f,k=j,l=a.complete||f,m,n;c(h?a.yep:a.nope,!!i),i&&c(i)}var i,j,l=this.yepnope.loader;if(e(a))g(a,0,l,0);else if(w(a))for(i=0;i<a.length;i++)j=a[i],e(j)?g(j,0,l,0):w(j)?B(j):Object(j)===j&&h(j,l);else Object(a)===a&&h(a,l)},B.addPrefix=function(a,b){z[a]=b},B.addFilter=function(a){x.push(a)},B.errorTimeout=1e4,null==b.readyState&&b.addEventListener&&(b.readyState="loading",b.addEventListener("DOMContentLoaded",A=function(){b.removeEventListener("DOMContentLoaded",A,0),b.readyState="complete"},0)),a.yepnope=k(),a.yepnope.executeStack=h,a.yepnope.injectJs=function(a,c,d,e,i,j){var k=b.createElement("script"),l,o,e=e||B.errorTimeout;k.src=a;for(o in d)k.setAttribute(o,d[o]);c=j?h:c||f,k.onreadystatechange=k.onload=function(){!l&&g(k.readyState)&&(l=1,c(),k.onload=k.onreadystatechange=null)},m(function(){l||(l=1,c(1))},e),i?k.onload():n.parentNode.insertBefore(k,n)},a.yepnope.injectCss=function(a,c,d,e,g,i){var e=b.createElement("link"),j,c=i?h:c||f;e.href=a,e.rel="stylesheet",e.type="text/css";for(j in d)e.setAttribute(j,d[j]);g||(n.parentNode.insertBefore(e,n),m(c,0))}}(this,document),Modernizr.load=function(){yepnope.apply(window,[].slice.call(arguments,0))};

/*! skrollr 0.6.21 (2014-01-06) | Alexander Prinzhorn - https://github.com/Prinzhorn/skrollr | Free to use under terms of MIT license */
(function(e,t,r){"use strict";function n(r){if(o=t.documentElement,a=t.body,K(),it=this,r=r||{},ut=r.constants||{},r.easing)for(var n in r.easing)U[n]=r.easing[n];yt=r.edgeStrategy||"set",ct={beforerender:r.beforerender,render:r.render},ft=r.forceHeight!==!1,ft&&(zt=r.scale||1),pt=r.mobileDeceleration||E,gt=r.smoothScrolling!==!1,vt=r.smoothScrollingDuration||x,dt={targetTop:it.getScrollTop()},_t=(r.mobileCheck||function(){return/Android|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent||navigator.vendor||e.opera)})(),_t?(st=t.getElementById("skrollr-body"),st&&at(),X(),Ct(o,[y,S],[T])):Ct(o,[y,b],[T]),it.refresh(),St(e,"resize orientationchange",function(){var e=o.clientWidth,t=o.clientHeight;(t!==$t||e!==Lt)&&($t=t,Lt=e,Mt=!0)});var i=Y();return function l(){Z(),bt=i(l)}(),it}var o,a,i=e.skrollr={get:function(){return it},init:function(e){return it||new n(e)},VERSION:"0.6.21"},l=Object.prototype.hasOwnProperty,s=e.Math,c=e.getComputedStyle,f="touchstart",u="touchmove",p="touchcancel",m="touchend",g="skrollable",v=g+"-before",d=g+"-between",h=g+"-after",y="skrollr",T="no-"+y,b=y+"-desktop",S=y+"-mobile",w="linear",k=1e3,E=.004,x=200,A="start",F="end",C="center",D="bottom",H="___skrollable_id",N=/^(?:input|textarea|button|select)$/i,P=/^\s+|\s+$/g,V=/^data(?:-(_\w+))?(?:-?(-?\d*\.?\d+p?))?(?:-?(start|end|top|center|bottom))?(?:-?(top|center|bottom))?$/,z=/\s*([\w\-\[\]]+)\s*:\s*(.+?)\s*(?:;|$)/gi,O=/^([a-z\-]+)\[(\w+)\]$/,q=/-([a-z])/g,I=function(e,t){return t.toUpperCase()},L=/[\-+]?[\d]*\.?[\d]+/g,$=/\{\?\}/g,M=/rgba?\(\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+/g,B=/[a-z\-]+-gradient/g,_="",G="",K=function(){var e=/^(?:O|Moz|webkit|ms)|(?:-(?:o|moz|webkit|ms)-)/;if(c){var t=c(a,null);for(var n in t)if(_=n.match(e)||+n==n&&t[n].match(e))break;if(!_)return _=G="",r;_=_[0],"-"===_.slice(0,1)?(G=_,_={"-webkit-":"webkit","-moz-":"Moz","-ms-":"ms","-o-":"O"}[_]):G="-"+_.toLowerCase()+"-"}},Y=function(){var t=e.requestAnimationFrame||e[_.toLowerCase()+"RequestAnimationFrame"],r=Nt();return(_t||!t)&&(t=function(t){var n=Nt()-r,o=s.max(0,1e3/60-n);return e.setTimeout(function(){r=Nt(),t()},o)}),t},R=function(){var t=e.cancelAnimationFrame||e[_.toLowerCase()+"CancelAnimationFrame"];return(_t||!t)&&(t=function(t){return e.clearTimeout(t)}),t},U={begin:function(){return 0},end:function(){return 1},linear:function(e){return e},quadratic:function(e){return e*e},cubic:function(e){return e*e*e},swing:function(e){return-s.cos(e*s.PI)/2+.5},sqrt:function(e){return s.sqrt(e)},outCubic:function(e){return s.pow(e-1,3)+1},bounce:function(e){var t;if(.5083>=e)t=3;else if(.8489>=e)t=9;else if(.96208>=e)t=27;else{if(!(.99981>=e))return 1;t=91}return 1-s.abs(3*s.cos(1.028*e*t)/t)}};n.prototype.refresh=function(e){var n,o,a=!1;for(e===r?(a=!0,lt=[],Bt=0,e=t.getElementsByTagName("*")):e=[].concat(e),n=0,o=e.length;o>n;n++){var i=e[n],l=i,s=[],c=gt,f=yt;if(i.attributes){for(var u=0,p=i.attributes.length;p>u;u++){var m=i.attributes[u];if("data-anchor-target"!==m.name)if("data-smooth-scrolling"!==m.name)if("data-edge-strategy"!==m.name){var v=m.name.match(V);if(null!==v){var d={props:m.value,element:i};s.push(d);var h=v[1];h&&(d.constant=h.substr(1));var y=v[2];/p$/.test(y)?(d.isPercentage=!0,d.offset=(0|y.slice(0,-1))/100):d.offset=0|y;var T=v[3],b=v[4]||T;T&&T!==A&&T!==F?(d.mode="relative",d.anchors=[T,b]):(d.mode="absolute",T===F?d.isEnd=!0:d.isPercentage||(d.offset=d.offset*zt))}}else f=m.value;else c="off"!==m.value;else if(l=t.querySelector(m.value),null===l)throw'Unable to find anchor target "'+m.value+'"'}if(s.length){var S,w,k;!a&&H in i?(k=i[H],S=lt[k].styleAttr,w=lt[k].classAttr):(k=i[H]=Bt++,S=i.style.cssText,w=Ft(i)),lt[k]={element:i,styleAttr:S,classAttr:w,anchorTarget:l,keyFrames:s,smoothScrolling:c,edgeStrategy:f},Ct(i,[g],[])}}}for(Et(),n=0,o=e.length;o>n;n++){var E=lt[e[n][H]];E!==r&&(J(E),et(E))}return it},n.prototype.relativeToAbsolute=function(e,t,r){var n=o.clientHeight,a=e.getBoundingClientRect(),i=a.top,l=a.bottom-a.top;return t===D?i-=n:t===C&&(i-=n/2),r===D?i+=l:r===C&&(i+=l/2),i+=it.getScrollTop(),0|i+.5},n.prototype.animateTo=function(e,t){t=t||{};var n=Nt(),o=it.getScrollTop();return mt={startTop:o,topDiff:e-o,targetTop:e,duration:t.duration||k,startTime:n,endTime:n+(t.duration||k),easing:U[t.easing||w],done:t.done},mt.topDiff||(mt.done&&mt.done.call(it,!1),mt=r),it},n.prototype.stopAnimateTo=function(){mt&&mt.done&&mt.done.call(it,!0),mt=r},n.prototype.isAnimatingTo=function(){return!!mt},n.prototype.setScrollTop=function(t,r){return ht=r===!0,_t?Gt=s.min(s.max(t,0),Vt):e.scrollTo(0,t),it},n.prototype.getScrollTop=function(){return _t?Gt:e.pageYOffset||o.scrollTop||a.scrollTop||0},n.prototype.getMaxScrollTop=function(){return Vt},n.prototype.on=function(e,t){return ct[e]=t,it},n.prototype.off=function(e){return delete ct[e],it},n.prototype.destroy=function(){var e=R();e(bt),kt(),Ct(o,[T],[y,b,S]);for(var t=0,n=lt.length;n>t;t++)ot(lt[t].element);o.style.overflow=a.style.overflow="auto",o.style.height=a.style.height="auto",st&&i.setStyle(st,"transform","none"),it=r,st=r,ct=r,ft=r,Vt=0,zt=1,ut=r,pt=r,Ot="down",qt=-1,Lt=0,$t=0,Mt=!1,mt=r,gt=r,vt=r,dt=r,ht=r,Bt=0,yt=r,_t=!1,Gt=0,Tt=r};var X=function(){var n,i,l,c,g,v,d,h,y,T,b,S;St(o,[f,u,p,m].join(" "),function(e){var o=e.changedTouches[0];for(c=e.target;3===c.nodeType;)c=c.parentNode;switch(g=o.clientY,v=o.clientX,T=e.timeStamp,N.test(c.tagName)||e.preventDefault(),e.type){case f:n&&n.blur(),it.stopAnimateTo(),n=c,i=d=g,l=v,y=T;break;case u:N.test(c.tagName)&&t.activeElement!==c&&e.preventDefault(),h=g-d,S=T-b,it.setScrollTop(Gt-h,!0),d=g,b=T;break;default:case p:case m:var a=i-g,w=l-v,k=w*w+a*a;if(49>k){if(!N.test(n.tagName)){n.focus();var E=t.createEvent("MouseEvents");E.initMouseEvent("click",!0,!0,e.view,1,o.screenX,o.screenY,o.clientX,o.clientY,e.ctrlKey,e.altKey,e.shiftKey,e.metaKey,0,null),n.dispatchEvent(E)}return}n=r;var x=h/S;x=s.max(s.min(x,3),-3);var A=s.abs(x/pt),F=x*A+.5*pt*A*A,C=it.getScrollTop()-F,D=0;C>Vt?(D=(Vt-C)/F,C=Vt):0>C&&(D=-C/F,C=0),A*=1-D,it.animateTo(0|C+.5,{easing:"outCubic",duration:A})}}),e.scrollTo(0,0),o.style.overflow=a.style.overflow="hidden"},j=function(){var e,t,r,n,a,i,l,c,f,u,p,m=o.clientHeight,g=xt();for(c=0,f=lt.length;f>c;c++)for(e=lt[c],t=e.element,r=e.anchorTarget,n=e.keyFrames,a=0,i=n.length;i>a;a++)l=n[a],u=l.offset,p=g[l.constant]||0,l.frame=u,l.isPercentage&&(u*=m,l.frame=u),"relative"===l.mode&&(ot(t),l.frame=it.relativeToAbsolute(r,l.anchors[0],l.anchors[1])-u,ot(t,!0)),l.frame+=p,ft&&!l.isEnd&&l.frame>Vt&&(Vt=l.frame);for(Vt=s.max(Vt,At()),c=0,f=lt.length;f>c;c++){for(e=lt[c],n=e.keyFrames,a=0,i=n.length;i>a;a++)l=n[a],p=g[l.constant]||0,l.isEnd&&(l.frame=Vt-l.offset+p);e.keyFrames.sort(Pt)}},W=function(e,t){for(var r=0,n=lt.length;n>r;r++){var o,a,s=lt[r],c=s.element,f=s.smoothScrolling?e:t,u=s.keyFrames,p=u[0].frame,m=u[u.length-1].frame,y=p>f,T=f>m,b=u[y?0:u.length-1];if(y||T){if(y&&-1===s.edge||T&&1===s.edge)continue;switch(Ct(c,[y?v:h],[v,d,h]),s.edge=y?-1:1,s.edgeStrategy){case"reset":ot(c);continue;case"ease":f=b.frame;break;default:case"set":var S=b.props;for(o in S)l.call(S,o)&&(a=nt(S[o].value),i.setStyle(c,o,a));continue}}else 0!==s.edge&&(Ct(c,[g,d],[v,h]),s.edge=0);for(var w=0,k=u.length-1;k>w;w++)if(f>=u[w].frame&&u[w+1].frame>=f){var E=u[w],x=u[w+1];for(o in E.props)if(l.call(E.props,o)){var A=(f-E.frame)/(x.frame-E.frame);A=E.props[o].easing(A),a=rt(E.props[o].value,x.props[o].value,A),a=nt(a),i.setStyle(c,o,a)}break}}},Z=function(){Mt&&(Mt=!1,Et());var e,t,n=it.getScrollTop(),o=Nt();if(mt)o>=mt.endTime?(n=mt.targetTop,e=mt.done,mt=r):(t=mt.easing((o-mt.startTime)/mt.duration),n=0|mt.startTop+t*mt.topDiff),it.setScrollTop(n,!0);else if(!ht){var a=dt.targetTop-n;a&&(dt={startTop:qt,topDiff:n-qt,targetTop:n,startTime:It,endTime:It+vt}),dt.endTime>=o&&(t=U.sqrt((o-dt.startTime)/vt),n=0|dt.startTop+t*dt.topDiff)}if(_t&&st&&i.setStyle(st,"transform","translate(0, "+-Gt+"px) "+Tt),ht||qt!==n){Ot=n>qt?"down":qt>n?"up":Ot,ht=!1;var l={curTop:n,lastTop:qt,maxTop:Vt,direction:Ot},s=ct.beforerender&&ct.beforerender.call(it,l);s!==!1&&(W(n,it.getScrollTop()),qt=n,ct.render&&ct.render.call(it,l)),e&&e.call(it,!1)}It=o},J=function(e){for(var t=0,r=e.keyFrames.length;r>t;t++){for(var n,o,a,i,l=e.keyFrames[t],s={};null!==(i=z.exec(l.props));)a=i[1],o=i[2],n=a.match(O),null!==n?(a=n[1],n=n[2]):n=w,o=o.indexOf("!")?Q(o):[o.slice(1)],s[a]={value:o,easing:U[n]};l.props=s}},Q=function(e){var t=[];return M.lastIndex=0,e=e.replace(M,function(e){return e.replace(L,function(e){return 100*(e/255)+"%"})}),G&&(B.lastIndex=0,e=e.replace(B,function(e){return G+e})),e=e.replace(L,function(e){return t.push(+e),"{?}"}),t.unshift(e),t},et=function(e){var t,r,n={};for(t=0,r=e.keyFrames.length;r>t;t++)tt(e.keyFrames[t],n);for(n={},t=e.keyFrames.length-1;t>=0;t--)tt(e.keyFrames[t],n)},tt=function(e,t){var r;for(r in t)l.call(e.props,r)||(e.props[r]=t[r]);for(r in e.props)t[r]=e.props[r]},rt=function(e,t,r){var n,o=e.length;if(o!==t.length)throw"Can't interpolate between \""+e[0]+'" and "'+t[0]+'"';var a=[e[0]];for(n=1;o>n;n++)a[n]=e[n]+(t[n]-e[n])*r;return a},nt=function(e){var t=1;return $.lastIndex=0,e[0].replace($,function(){return e[t++]})},ot=function(e,t){e=[].concat(e);for(var r,n,o=0,a=e.length;a>o;o++)n=e[o],r=lt[n[H]],r&&(t?(n.style.cssText=r.dirtyStyleAttr,Ct(n,r.dirtyClassAttr)):(r.dirtyStyleAttr=n.style.cssText,r.dirtyClassAttr=Ft(n),n.style.cssText=r.styleAttr,Ct(n,r.classAttr)))},at=function(){Tt="translateZ(0)",i.setStyle(st,"transform",Tt);var e=c(st),t=e.getPropertyValue("transform"),r=e.getPropertyValue(G+"transform"),n=t&&"none"!==t||r&&"none"!==r;n||(Tt="")};i.setStyle=function(e,t,r){var n=e.style;if(t=t.replace(q,I).replace("-",""),"zIndex"===t)n[t]=isNaN(r)?r:""+(0|r);else if("float"===t)n.styleFloat=n.cssFloat=r;else try{_&&(n[_+t.slice(0,1).toUpperCase()+t.slice(1)]=r),n[t]=r}catch(o){}};var it,lt,st,ct,ft,ut,pt,mt,gt,vt,dt,ht,yt,Tt,bt,St=i.addEvent=function(t,r,n){var o=function(t){return t=t||e.event,t.target||(t.target=t.srcElement),t.preventDefault||(t.preventDefault=function(){t.returnValue=!1}),n.call(this,t)};r=r.split(" ");for(var a,i=0,l=r.length;l>i;i++)a=r[i],t.addEventListener?t.addEventListener(a,n,!1):t.attachEvent("on"+a,o),Kt.push({element:t,name:a,listener:n})},wt=i.removeEvent=function(e,t,r){t=t.split(" ");for(var n=0,o=t.length;o>n;n++)e.removeEventListener?e.removeEventListener(t[n],r,!1):e.detachEvent("on"+t[n],r)},kt=function(){for(var e,t=0,r=Kt.length;r>t;t++)e=Kt[t],wt(e.element,e.name,e.listener);Kt=[]},Et=function(){var e=it.getScrollTop();Vt=0,ft&&!_t&&(a.style.height="auto"),j(),ft&&!_t&&(a.style.height=Vt+o.clientHeight+"px"),_t?it.setScrollTop(s.min(it.getScrollTop(),Vt)):it.setScrollTop(e,!0),ht=!0},xt=function(){var e,t,r=o.clientHeight,n={};for(e in ut)t=ut[e],"function"==typeof t?t=t.call(it):/p$/.test(t)&&(t=t.slice(0,-1)/100*r),n[e]=t;return n},At=function(){var e=st&&st.offsetHeight||0,t=s.max(e,a.scrollHeight,a.offsetHeight,o.scrollHeight,o.offsetHeight,o.clientHeight);return t-o.clientHeight},Ft=function(t){var r="className";return e.SVGElement&&t instanceof e.SVGElement&&(t=t[r],r="baseVal"),t[r]},Ct=function(t,n,o){var a="className";if(e.SVGElement&&t instanceof e.SVGElement&&(t=t[a],a="baseVal"),o===r)return t[a]=n,r;for(var i=t[a],l=0,s=o.length;s>l;l++)i=Ht(i).replace(Ht(o[l])," ");i=Dt(i);for(var c=0,f=n.length;f>c;c++)-1===Ht(i).indexOf(Ht(n[c]))&&(i+=" "+n[c]);t[a]=Dt(i)},Dt=function(e){return e.replace(P,"")},Ht=function(e){return" "+e+" "},Nt=Date.now||function(){return+new Date},Pt=function(e,t){return e.frame-t.frame},Vt=0,zt=1,Ot="down",qt=-1,It=Nt(),Lt=0,$t=0,Mt=!1,Bt=0,_t=!1,Gt=0,Kt=[]})(window,document);

/* onScreen https://github.com/silvestreh/onScreen */
(function(e){e.fn.onScreen=function(t){var n=e.extend({container:window,direction:"vertical",toggleClass:null,doIn:null,doOut:null,tolerance:0,throttle:null,lazyAttr:null,lazyPlaceholder:"data:image/gif;base64,R0lGODlhEAAFAIAAAP///////yH/C05FVFNDQVBFMi4wAwEAAAAh+QQJCQAAACwAAAAAEAAFAAACCIyPqcvtD00BACH5BAkJAAIALAAAAAAQAAUAgfT29Pz6/P///wAAAAIQTGCiywKPmjxUNhjtMlWrAgAh+QQJCQAFACwAAAAAEAAFAIK8urzc2tzEwsS8vrzc3tz///8AAAAAAAADFEiyUf6wCEBHvLPemIHdTzCMDegkACH5BAkJAAYALAAAAAAQAAUAgoSChLS2tIyKjLy+vIyOjMTCxP///wAAAAMUWCQ09jAaAiqQmFosdeXRUAkBCCUAIfkECQkACAAsAAAAABAABQCDvLq83N7c3Nrc9Pb0xMLE/P78vL68/Pr8////AAAAAAAAAAAAAAAAAAAAAAAAAAAABCEwkCnKGbegvQn4RjGMx8F1HxBi5Il4oEiap2DcVYlpZwQAIfkECQkACAAsAAAAABAABQCDvLq85OLkxMLE9Pb0vL685ObkxMbE/Pr8////AAAAAAAAAAAAAAAAAAAAAAAAAAAABCDwnCGHEcIMxPn4VAGMQNBx0zQEZHkiYNiap5RaBKG9EQAh+QQJCQAJACwAAAAAEAAFAIOEgoTMysyMjozs6uyUlpSMiozMzsyUkpTs7uz///8AAAAAAAAAAAAAAAAAAAAAAAAEGTBJiYgoBM09DfhAwHEeKI4dGKLTIHzCwEUAIfkECQkACAAsAAAAABAABQCDvLq85OLkxMLE9Pb0vL685ObkxMbE/Pr8////AAAAAAAAAAAAAAAAAAAAAAAAAAAABCAQSTmMEGaco8+UBSACwWBqHxKOJYd+q1iaXFoRRMbtEQAh+QQJCQAIACwAAAAAEAAFAIO8urzc3tzc2tz09vTEwsT8/vy8vrz8+vz///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAEIhBJWc6wJZAtJh3gcRBAaXiIZV2kiRbgNZbA6VXiUAhGL0QAIfkECQkABgAsAAAAABAABQCChIKEtLa0jIqMvL68jI6MxMLE////AAAAAxRoumxFgoxGCbiANos145e3DJcQJAAh+QQJCQAFACwAAAAAEAAFAIK8urzc2tzEwsS8vrzc3tz///8AAAAAAAADFFi6XCQwtCmAHbPVm9kGWKcEQxkkACH5BAkJAAIALAAAAAAQAAUAgfT29Pz6/P///wAAAAIRlI8SAZsPYnuJMUCRnNksWwAAOw==",debug:false},t);return this.each(function(){function m(){if(v){return p<f-n.tolerance&&r<p+c-n.tolerance}else{return p<u-n.tolerance&&p>-c+n.tolerance}}function g(){if(v){return p+(c-n.tolerance)<r||p>f-n.tolerance}else{return p>u-n.tolerance||-c+n.tolerance>p}}function y(){if(v){return d<l-n.tolerance&&i<d+h-n.tolerance}else{return d<a-n.tolerance&&d>-h+n.tolerance}}function b(){if(v){return d+(h-n.tolerance)<i||d>l-n.tolerance}else{return d>a-n.tolerance||-h+n.tolerance>d}}function w(){if(t){return false}if(n.direction==="horizontal"){return y()}else{return m()}}function E(){if(!t){return false}if(n.direction==="horizontal"){return b()}else{return g()}}function S(e,t,n){var r,i,s;return function(){i=arguments;s=true;n=n||this;if(!r){(function(){if(s){e.apply(n,i);s=false;r=setTimeout(arguments.callee,t)}else{r=null}})()}}}var t=false;var r;var i;var s=e(this);var o;var u;var a;var f;var l;var c;var h;var p;var d;var v=e.isWindow(n.container);var x=function(){if(!v&&e(n.container).css("position")==="static"){e(n.container).css("position","relative")}o=e(n.container);u=o.height();a=o.width();f=o.scrollTop()+u;l=o.scrollLeft()+a;c=s.outerHeight(true);h=s.outerWidth(true);if(v){var m=s.offset();p=m.top;d=m.left}else{var g=s.position();p=g.top;d=g.left}r=o.scrollTop();i=o.scrollLeft();if(n.debug){console.log("Container: "+n.container+"\n"+"Width: "+u+"\n"+"Height: "+a+"\n"+"Bottom: "+f+"\n"+"Right: "+l);console.log("Matched element: "+(s.attr("class")!==undefined?s.prop("tagName").toLowerCase()+"."+s.attr("class"):s.prop("tagName").toLowerCase())+"\n"+"Left: "+d+"\n"+"Top: "+p+"\n"+"Width: "+h+"\n"+"Height: "+c)}if(w()){if(n.toggleClass){s.addClass(n.toggleClass)}if(e.isFunction(n.doIn)){n.doIn.call(s[0])}if(n.lazyAttr&&s.prop("tagName")==="IMG"){var y=s.attr(n.lazyAttr);s.css({background:"url("+n.lazyPlaceholder+") 50% 50% no-repeat",minHeight:"5px",minWidth:"16px"});s.prop("src",y)}t=true}else if(E()){if(n.toggleClass){s.removeClass(n.toggleClass)}if(e.isFunction(n.doOut)){n.doOut.call(s[0])}t=false}};if(window.location.hash){S(x,50)}else{x()}if(n.throttle){x=S(x,n.throttle)}e(n.container).on("scroll resize",x);if(typeof module==="object"&&module&&typeof module.exports==="object"){module.exports=jQuery}else{if(typeof define==="function"&&define.amd){define("jquery-onscreen",[],function(){return jQuery})}}})}})(jQuery);

/* countTo https://github.com/mhuggins/jquery-countTo */
(function(e){function t(e,t){return e.toFixed(t.decimals)}e.fn.countTo=function(t){t=t||{};return e(this).each(function(){function l(){a+=i;u++;c(a);if(typeof n.onUpdate=="function"){n.onUpdate.call(s,a)}if(u>=r){o.removeData("countTo");clearInterval(f.interval);a=n.to;if(typeof n.onComplete=="function"){n.onComplete.call(s,a)}}}function c(e){var t=n.formatter.call(s,e,n);o.text(t)}var n=e.extend({},e.fn.countTo.defaults,{from:e(this).data("from"),to:e(this).data("to"),speed:e(this).data("speed"),refreshInterval:e(this).data("refresh-interval"),decimals:e(this).data("decimals")},t);var r=Math.ceil(n.speed/n.refreshInterval),i=(n.to-n.from)/r;var s=this,o=e(this),u=0,a=n.from,f=o.data("countTo")||{};o.data("countTo",f);if(f.interval){clearInterval(f.interval)}f.interval=setInterval(l,n.refreshInterval);c(a)})};e.fn.countTo.defaults={from:0,to:0,speed:1e3,refreshInterval:100,decimals:0,formatter:t,onUpdate:null,onComplete:null}})(jQuery);




	/* Animated header */
		
	$(function(){
		var shrinkHeader = 200;
		$(window).scroll(function() {
			var scroll = getCurrentScroll();
			if ( scroll >= shrinkHeader ) {
				$('header').addClass('shrink');
	            $('header').addClass('shrink-color');
	        }
	        else {
	        	$('header').removeClass('shrink');
            $('header').removeClass('shrink-color');
        }
    });
		function getCurrentScroll() {
			return window.pageYOffset || document.documentElement.scrollTop;
		}
	});



	/* Smooth scroll */

	function smoothScroll() {
		$('a[href*=#]:not([href=#])').click(function () {
			if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') || location.hostname == this.hostname) {
				var target = $(this.hash);
				target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
				if (target.length) {
					$('html,body').animate({
						scrollTop: target.offset().top
					}, 500);
					return false;
				}
			}
		});
	}
	smoothScroll();


	/* Work overlay center */

	// function centerOverlay() {
	// 	var WorkOverlay = $('.overlay-content');
	// 	if (WorkOverlay.length) {
	// 		WorkOverlay.each(function () {
	// 			var $this = $(this),
	// 			itemPortfolioHeight = $this.closest('.item').height(),
	// 			PortfolioOverlayHeight = $this.height(),
	// 			PortfolioIcon = $this.children('.post-type');
	// 			PortfolioIconHeight = PortfolioIcon.children('i').height();
	// 			$this.css({
	// 				marginTop: (itemPortfolioHeight - PortfolioOverlayHeight) / 2
	// 			});
	// 		});
	// 	}
	// }
	// centerOverlay();
	// $(window).on('load', centerOverlay);
	// $(window).on('resize', centerOverlay);



	/* Milestone */

	var countItem = $('.count-item');

	function milestone() {

		countItem.each(function () {

			var $this = $(this);

			$this.onScreen({
				doIn: function () {
					var countNumber = $this.find('.count-number'),
					countTitle = $this.find('.count-subject');
					countNumber.countTo({
						onComplete: function () {
							countTitle.delay(100).addClass('subject-on');
							countNumber.removeClass('count-number').addClass('count-number-done');
						}
					});
				},
			});

		});
	}

	if (countItem.length) {
		milestone();
	}



	/* Parallax header */

	$(function(){
		if ($('#intro-wrap').length) {
		    var e = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
		    if (e) {
		        $('body').addClass("no-parallax")
		    } else if (!$('body').hasClass("mobile") && !$('body').hasClass("no-parallax")) {
		        $('#intro').attr("data-anchor-target", "#intro-wrap");
		        $('header').attr("data-anchor-target", "#intro-wrap");
		        $('#intro').attr("data-top", "transform:translateY(0px);");
		        $('header').attr("data-top", "transform:translateY(0px);");
		        if (e) {
		            $('#intro').attr("data-top-bottom", "transform:translateY(0px);");
		            $('header').attr("data-top-bottom", "transform:translateY(0px);");
		            $('header').addClass("transition")
		        } else {
		            $('#intro').attr("data-top-bottom", "transform:translateY(" + "-" + $('#intro-wrap').height() / 4 + "px);")
		        }
		        animDone = false;
		        skrollr.init({
		            forceHeight: false,
		            smoothScrolling: false,
		            mobileCheck: function() {
		                return false
		            },
		            render: function() {}
		        }).refresh();
		        $('#intro').find('.caption').each(function() {
		            var e = $(this);
		            e.css({top: ($('#intro-wrap').height() + $('header').outerHeight(true) / 2 - e.outerHeight()) / 2})
		        })
		    } else {
		        skrollr.init().destroy();
		        $('main').css({
		            marginTop: 0 + "px"
		        });
		        var t = $("#intro"),
		            n = t[0].attributes,
		            r, i;
		        for (i = n.length - 1; i >= 0; --i) {
		            r = n[i].nodeName;
		            if (r.substring(0, 5) === "data-") {
		                t.removeAttr(r)
		            }
		        }
		        t.css({"-webkit-transform": "","-moz-transform": "",transform: "",backgroundPosition: ""}).removeClass("skrollable-after");
		        $('#intro').find('.caption').each(function() {
		            var e = $(this);
		            if (!$('body').hasClass("mobile") && $('body').hasClass("no-parallax")) {
		                e.css({top: ($('#intro-wrap').height() + $('header').outerHeight(true) - e.outerHeight()) / 2})
		            } else {
		                e.css({top: ($('#intro-wrap').height() - e.outerHeight()) / 2})
		            }
		        })
		    }
		} else {
		    if (!$('body').hasClass("mobile")) {
		        $('main').css({marginTop: $('header').outerHeight(true) + "px"})
		    } else {
		        $('main').css({marginTop: 0})
		    }
		}
	});
