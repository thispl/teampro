(() => {
  var __defProp = Object.defineProperty;
  var __defProps = Object.defineProperties;
  var __getOwnPropDescs = Object.getOwnPropertyDescriptors;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __getOwnPropSymbols = Object.getOwnPropertySymbols;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __propIsEnum = Object.prototype.propertyIsEnumerable;
  var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
  var __spreadValues = (a, b) => {
    for (var prop in b || (b = {}))
      if (__hasOwnProp.call(b, prop))
        __defNormalProp(a, prop, b[prop]);
    if (__getOwnPropSymbols)
      for (var prop of __getOwnPropSymbols(b)) {
        if (__propIsEnum.call(b, prop))
          __defNormalProp(a, prop, b[prop]);
      }
    return a;
  };
  var __spreadProps = (a, b) => __defProps(a, __getOwnPropDescs(b));
  var __esm = (fn, res) => function __init() {
    return fn && (res = (0, fn[__getOwnPropNames(fn)[0]])(fn = 0)), res;
  };
  var __commonJS = (cb, mod) => function __require() {
    return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
  };

  // ../node_modules/@vue/shared/dist/shared.esm-bundler.js
  function makeMap(str) {
    const map2 = /* @__PURE__ */ Object.create(null);
    for (const key of str.split(","))
      map2[key] = 1;
    return (val) => val in map2;
  }
  function normalizeStyle(value) {
    if (isArray(value)) {
      const res = {};
      for (let i = 0; i < value.length; i++) {
        const item = value[i];
        const normalized = isString(item) ? parseStringStyle(item) : normalizeStyle(item);
        if (normalized) {
          for (const key in normalized) {
            res[key] = normalized[key];
          }
        }
      }
      return res;
    } else if (isString(value) || isObject(value)) {
      return value;
    }
  }
  function parseStringStyle(cssText) {
    const ret = {};
    cssText.replace(styleCommentRE, "").split(listDelimiterRE).forEach((item) => {
      if (item) {
        const tmp = item.split(propertyDelimiterRE);
        tmp.length > 1 && (ret[tmp[0].trim()] = tmp[1].trim());
      }
    });
    return ret;
  }
  function normalizeClass(value) {
    let res = "";
    if (isString(value)) {
      res = value;
    } else if (isArray(value)) {
      for (let i = 0; i < value.length; i++) {
        const normalized = normalizeClass(value[i]);
        if (normalized) {
          res += normalized + " ";
        }
      }
    } else if (isObject(value)) {
      for (const name in value) {
        if (value[name]) {
          res += name + " ";
        }
      }
    }
    return res.trim();
  }
  function includeBooleanAttr(value) {
    return !!value || value === "";
  }
  function looseCompareArrays(a, b) {
    if (a.length !== b.length)
      return false;
    let equal = true;
    for (let i = 0; equal && i < a.length; i++) {
      equal = looseEqual(a[i], b[i]);
    }
    return equal;
  }
  function looseEqual(a, b) {
    if (a === b)
      return true;
    let aValidType = isDate(a);
    let bValidType = isDate(b);
    if (aValidType || bValidType) {
      return aValidType && bValidType ? a.getTime() === b.getTime() : false;
    }
    aValidType = isSymbol(a);
    bValidType = isSymbol(b);
    if (aValidType || bValidType) {
      return a === b;
    }
    aValidType = isArray(a);
    bValidType = isArray(b);
    if (aValidType || bValidType) {
      return aValidType && bValidType ? looseCompareArrays(a, b) : false;
    }
    aValidType = isObject(a);
    bValidType = isObject(b);
    if (aValidType || bValidType) {
      if (!aValidType || !bValidType) {
        return false;
      }
      const aKeysCount = Object.keys(a).length;
      const bKeysCount = Object.keys(b).length;
      if (aKeysCount !== bKeysCount) {
        return false;
      }
      for (const key in a) {
        const aHasKey = a.hasOwnProperty(key);
        const bHasKey = b.hasOwnProperty(key);
        if (aHasKey && !bHasKey || !aHasKey && bHasKey || !looseEqual(a[key], b[key])) {
          return false;
        }
      }
    }
    return String(a) === String(b);
  }
  function looseIndexOf(arr, val) {
    return arr.findIndex((item) => looseEqual(item, val));
  }
  var EMPTY_OBJ, EMPTY_ARR, NOOP, NO, isOn, isModelListener, extend, remove, hasOwnProperty, hasOwn, isArray, isMap, isSet, isDate, isFunction, isString, isSymbol, isObject, isPromise, objectToString, toTypeString, toRawType, isPlainObject, isIntegerKey, isReservedProp, isBuiltInDirective, cacheStringFunction, camelizeRE, camelize, hyphenateRE, hyphenate, capitalize, toHandlerKey, hasChanged, invokeArrayFns, def, looseToNumber, _globalThis, getGlobalThis, listDelimiterRE, propertyDelimiterRE, styleCommentRE, HTML_TAGS, SVG_TAGS, MATH_TAGS, isHTMLTag, isSVGTag, isMathMLTag, specialBooleanAttrs, isSpecialBooleanAttr, isBooleanAttr, isRef, toDisplayString, replacer, stringifySymbol;
  var init_shared_esm_bundler = __esm({
    "../node_modules/@vue/shared/dist/shared.esm-bundler.js"() {
      EMPTY_OBJ = true ? Object.freeze({}) : {};
      EMPTY_ARR = true ? Object.freeze([]) : [];
      NOOP = () => {
      };
      NO = () => false;
      isOn = (key) => key.charCodeAt(0) === 111 && key.charCodeAt(1) === 110 && (key.charCodeAt(2) > 122 || key.charCodeAt(2) < 97);
      isModelListener = (key) => key.startsWith("onUpdate:");
      extend = Object.assign;
      remove = (arr, el) => {
        const i = arr.indexOf(el);
        if (i > -1) {
          arr.splice(i, 1);
        }
      };
      hasOwnProperty = Object.prototype.hasOwnProperty;
      hasOwn = (val, key) => hasOwnProperty.call(val, key);
      isArray = Array.isArray;
      isMap = (val) => toTypeString(val) === "[object Map]";
      isSet = (val) => toTypeString(val) === "[object Set]";
      isDate = (val) => toTypeString(val) === "[object Date]";
      isFunction = (val) => typeof val === "function";
      isString = (val) => typeof val === "string";
      isSymbol = (val) => typeof val === "symbol";
      isObject = (val) => val !== null && typeof val === "object";
      isPromise = (val) => {
        return (isObject(val) || isFunction(val)) && isFunction(val.then) && isFunction(val.catch);
      };
      objectToString = Object.prototype.toString;
      toTypeString = (value) => objectToString.call(value);
      toRawType = (value) => {
        return toTypeString(value).slice(8, -1);
      };
      isPlainObject = (val) => toTypeString(val) === "[object Object]";
      isIntegerKey = (key) => isString(key) && key !== "NaN" && key[0] !== "-" && "" + parseInt(key, 10) === key;
      isReservedProp = /* @__PURE__ */ makeMap(
        ",key,ref,ref_for,ref_key,onVnodeBeforeMount,onVnodeMounted,onVnodeBeforeUpdate,onVnodeUpdated,onVnodeBeforeUnmount,onVnodeUnmounted"
      );
      isBuiltInDirective = /* @__PURE__ */ makeMap(
        "bind,cloak,else-if,else,for,html,if,model,on,once,pre,show,slot,text,memo"
      );
      cacheStringFunction = (fn) => {
        const cache = /* @__PURE__ */ Object.create(null);
        return (str) => {
          const hit = cache[str];
          return hit || (cache[str] = fn(str));
        };
      };
      camelizeRE = /-\w/g;
      camelize = cacheStringFunction(
        (str) => {
          return str.replace(camelizeRE, (c) => c.slice(1).toUpperCase());
        }
      );
      hyphenateRE = /\B([A-Z])/g;
      hyphenate = cacheStringFunction(
        (str) => str.replace(hyphenateRE, "-$1").toLowerCase()
      );
      capitalize = cacheStringFunction((str) => {
        return str.charAt(0).toUpperCase() + str.slice(1);
      });
      toHandlerKey = cacheStringFunction(
        (str) => {
          const s = str ? `on${capitalize(str)}` : ``;
          return s;
        }
      );
      hasChanged = (value, oldValue) => !Object.is(value, oldValue);
      invokeArrayFns = (fns, ...arg) => {
        for (let i = 0; i < fns.length; i++) {
          fns[i](...arg);
        }
      };
      def = (obj, key, value, writable = false) => {
        Object.defineProperty(obj, key, {
          configurable: true,
          enumerable: false,
          writable,
          value
        });
      };
      looseToNumber = (val) => {
        const n = parseFloat(val);
        return isNaN(n) ? val : n;
      };
      getGlobalThis = () => {
        return _globalThis || (_globalThis = typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : typeof global !== "undefined" ? global : {});
      };
      listDelimiterRE = /;(?![^(]*\))/g;
      propertyDelimiterRE = /:([^]+)/;
      styleCommentRE = /\/\*[^]*?\*\//g;
      HTML_TAGS = "html,body,base,head,link,meta,style,title,address,article,aside,footer,header,hgroup,h1,h2,h3,h4,h5,h6,nav,section,div,dd,dl,dt,figcaption,figure,picture,hr,img,li,main,ol,p,pre,ul,a,b,abbr,bdi,bdo,br,cite,code,data,dfn,em,i,kbd,mark,q,rp,rt,ruby,s,samp,small,span,strong,sub,sup,time,u,var,wbr,area,audio,map,track,video,embed,object,param,source,canvas,script,noscript,del,ins,caption,col,colgroup,table,thead,tbody,td,th,tr,button,datalist,fieldset,form,input,label,legend,meter,optgroup,option,output,progress,select,textarea,details,dialog,menu,summary,template,blockquote,iframe,tfoot";
      SVG_TAGS = "svg,animate,animateMotion,animateTransform,circle,clipPath,color-profile,defs,desc,discard,ellipse,feBlend,feColorMatrix,feComponentTransfer,feComposite,feConvolveMatrix,feDiffuseLighting,feDisplacementMap,feDistantLight,feDropShadow,feFlood,feFuncA,feFuncB,feFuncG,feFuncR,feGaussianBlur,feImage,feMerge,feMergeNode,feMorphology,feOffset,fePointLight,feSpecularLighting,feSpotLight,feTile,feTurbulence,filter,foreignObject,g,hatch,hatchpath,image,line,linearGradient,marker,mask,mesh,meshgradient,meshpatch,meshrow,metadata,mpath,path,pattern,polygon,polyline,radialGradient,rect,set,solidcolor,stop,switch,symbol,text,textPath,title,tspan,unknown,use,view";
      MATH_TAGS = "annotation,annotation-xml,maction,maligngroup,malignmark,math,menclose,merror,mfenced,mfrac,mfraction,mglyph,mi,mlabeledtr,mlongdiv,mmultiscripts,mn,mo,mover,mpadded,mphantom,mprescripts,mroot,mrow,ms,mscarries,mscarry,msgroup,msline,mspace,msqrt,msrow,mstack,mstyle,msub,msubsup,msup,mtable,mtd,mtext,mtr,munder,munderover,none,semantics";
      isHTMLTag = /* @__PURE__ */ makeMap(HTML_TAGS);
      isSVGTag = /* @__PURE__ */ makeMap(SVG_TAGS);
      isMathMLTag = /* @__PURE__ */ makeMap(MATH_TAGS);
      specialBooleanAttrs = `itemscope,allowfullscreen,formnovalidate,ismap,nomodule,novalidate,readonly`;
      isSpecialBooleanAttr = /* @__PURE__ */ makeMap(specialBooleanAttrs);
      isBooleanAttr = /* @__PURE__ */ makeMap(
        specialBooleanAttrs + `,async,autofocus,autoplay,controls,default,defer,disabled,hidden,inert,loop,open,required,reversed,scoped,seamless,checked,muted,multiple,selected`
      );
      isRef = (val) => {
        return !!(val && val["__v_isRef"] === true);
      };
      toDisplayString = (val) => {
        return isString(val) ? val : val == null ? "" : isArray(val) || isObject(val) && (val.toString === objectToString || !isFunction(val.toString)) ? isRef(val) ? toDisplayString(val.value) : JSON.stringify(val, replacer, 2) : String(val);
      };
      replacer = (_key, val) => {
        if (isRef(val)) {
          return replacer(_key, val.value);
        } else if (isMap(val)) {
          return {
            [`Map(${val.size})`]: [...val.entries()].reduce(
              (entries, [key, val2], i) => {
                entries[stringifySymbol(key, i) + " =>"] = val2;
                return entries;
              },
              {}
            )
          };
        } else if (isSet(val)) {
          return {
            [`Set(${val.size})`]: [...val.values()].map((v) => stringifySymbol(v))
          };
        } else if (isSymbol(val)) {
          return stringifySymbol(val);
        } else if (isObject(val) && !isArray(val) && !isPlainObject(val)) {
          return String(val);
        }
        return val;
      };
      stringifySymbol = (v, i = "") => {
        var _a;
        return isSymbol(v) ? `Symbol(${(_a = v.description) != null ? _a : i})` : v;
      };
    }
  });

  // ../node_modules/@vue/reactivity/dist/reactivity.esm-bundler.js
  function warn(msg, ...args) {
    console.warn(`[Vue warn] ${msg}`, ...args);
  }
  function getCurrentScope() {
    return activeEffectScope;
  }
  function batch(sub, isComputed = false) {
    sub.flags |= 8;
    if (isComputed) {
      sub.next = batchedComputed;
      batchedComputed = sub;
      return;
    }
    sub.next = batchedSub;
    batchedSub = sub;
  }
  function startBatch() {
    batchDepth++;
  }
  function endBatch() {
    if (--batchDepth > 0) {
      return;
    }
    if (batchedComputed) {
      let e = batchedComputed;
      batchedComputed = void 0;
      while (e) {
        const next = e.next;
        e.next = void 0;
        e.flags &= -9;
        e = next;
      }
    }
    let error;
    while (batchedSub) {
      let e = batchedSub;
      batchedSub = void 0;
      while (e) {
        const next = e.next;
        e.next = void 0;
        e.flags &= -9;
        if (e.flags & 1) {
          try {
            ;
            e.trigger();
          } catch (err) {
            if (!error)
              error = err;
          }
        }
        e = next;
      }
    }
    if (error)
      throw error;
  }
  function prepareDeps(sub) {
    for (let link = sub.deps; link; link = link.nextDep) {
      link.version = -1;
      link.prevActiveLink = link.dep.activeLink;
      link.dep.activeLink = link;
    }
  }
  function cleanupDeps(sub) {
    let head;
    let tail = sub.depsTail;
    let link = tail;
    while (link) {
      const prev = link.prevDep;
      if (link.version === -1) {
        if (link === tail)
          tail = prev;
        removeSub(link);
        removeDep(link);
      } else {
        head = link;
      }
      link.dep.activeLink = link.prevActiveLink;
      link.prevActiveLink = void 0;
      link = prev;
    }
    sub.deps = head;
    sub.depsTail = tail;
  }
  function isDirty(sub) {
    for (let link = sub.deps; link; link = link.nextDep) {
      if (link.dep.version !== link.version || link.dep.computed && (refreshComputed(link.dep.computed) || link.dep.version !== link.version)) {
        return true;
      }
    }
    if (sub._dirty) {
      return true;
    }
    return false;
  }
  function refreshComputed(computed3) {
    if (computed3.flags & 4 && !(computed3.flags & 16)) {
      return;
    }
    computed3.flags &= -17;
    if (computed3.globalVersion === globalVersion) {
      return;
    }
    computed3.globalVersion = globalVersion;
    if (!computed3.isSSR && computed3.flags & 128 && (!computed3.deps && !computed3._dirty || !isDirty(computed3))) {
      return;
    }
    computed3.flags |= 2;
    const dep = computed3.dep;
    const prevSub = activeSub;
    const prevShouldTrack = shouldTrack;
    activeSub = computed3;
    shouldTrack = true;
    try {
      prepareDeps(computed3);
      const value = computed3.fn(computed3._value);
      if (dep.version === 0 || hasChanged(value, computed3._value)) {
        computed3.flags |= 128;
        computed3._value = value;
        dep.version++;
      }
    } catch (err) {
      dep.version++;
      throw err;
    } finally {
      activeSub = prevSub;
      shouldTrack = prevShouldTrack;
      cleanupDeps(computed3);
      computed3.flags &= -3;
    }
  }
  function removeSub(link, soft = false) {
    const { dep, prevSub, nextSub } = link;
    if (prevSub) {
      prevSub.nextSub = nextSub;
      link.prevSub = void 0;
    }
    if (nextSub) {
      nextSub.prevSub = prevSub;
      link.nextSub = void 0;
    }
    if (dep.subsHead === link) {
      dep.subsHead = nextSub;
    }
    if (dep.subs === link) {
      dep.subs = prevSub;
      if (!prevSub && dep.computed) {
        dep.computed.flags &= -5;
        for (let l = dep.computed.deps; l; l = l.nextDep) {
          removeSub(l, true);
        }
      }
    }
    if (!soft && !--dep.sc && dep.map) {
      dep.map.delete(dep.key);
    }
  }
  function removeDep(link) {
    const { prevDep, nextDep } = link;
    if (prevDep) {
      prevDep.nextDep = nextDep;
      link.prevDep = void 0;
    }
    if (nextDep) {
      nextDep.prevDep = prevDep;
      link.nextDep = void 0;
    }
  }
  function pauseTracking() {
    trackStack.push(shouldTrack);
    shouldTrack = false;
  }
  function resetTracking() {
    const last = trackStack.pop();
    shouldTrack = last === void 0 ? true : last;
  }
  function cleanupEffect(e) {
    const { cleanup } = e;
    e.cleanup = void 0;
    if (cleanup) {
      const prevSub = activeSub;
      activeSub = void 0;
      try {
        cleanup();
      } finally {
        activeSub = prevSub;
      }
    }
  }
  function addSub(link) {
    link.dep.sc++;
    if (link.sub.flags & 4) {
      const computed3 = link.dep.computed;
      if (computed3 && !link.dep.subs) {
        computed3.flags |= 4 | 16;
        for (let l = computed3.deps; l; l = l.nextDep) {
          addSub(l);
        }
      }
      const currentTail = link.dep.subs;
      if (currentTail !== link) {
        link.prevSub = currentTail;
        if (currentTail)
          currentTail.nextSub = link;
      }
      if (link.dep.subsHead === void 0) {
        link.dep.subsHead = link;
      }
      link.dep.subs = link;
    }
  }
  function track(target, type, key) {
    if (shouldTrack && activeSub) {
      let depsMap = targetMap.get(target);
      if (!depsMap) {
        targetMap.set(target, depsMap = /* @__PURE__ */ new Map());
      }
      let dep = depsMap.get(key);
      if (!dep) {
        depsMap.set(key, dep = new Dep());
        dep.map = depsMap;
        dep.key = key;
      }
      if (true) {
        dep.track({
          target,
          type,
          key
        });
      } else {
        dep.track();
      }
    }
  }
  function trigger(target, type, key, newValue, oldValue, oldTarget) {
    const depsMap = targetMap.get(target);
    if (!depsMap) {
      globalVersion++;
      return;
    }
    const run = (dep) => {
      if (dep) {
        if (true) {
          dep.trigger({
            target,
            type,
            key,
            newValue,
            oldValue,
            oldTarget
          });
        } else {
          dep.trigger();
        }
      }
    };
    startBatch();
    if (type === "clear") {
      depsMap.forEach(run);
    } else {
      const targetIsArray = isArray(target);
      const isArrayIndex = targetIsArray && isIntegerKey(key);
      if (targetIsArray && key === "length") {
        const newLength = Number(newValue);
        depsMap.forEach((dep, key2) => {
          if (key2 === "length" || key2 === ARRAY_ITERATE_KEY || !isSymbol(key2) && key2 >= newLength) {
            run(dep);
          }
        });
      } else {
        if (key !== void 0 || depsMap.has(void 0)) {
          run(depsMap.get(key));
        }
        if (isArrayIndex) {
          run(depsMap.get(ARRAY_ITERATE_KEY));
        }
        switch (type) {
          case "add":
            if (!targetIsArray) {
              run(depsMap.get(ITERATE_KEY));
              if (isMap(target)) {
                run(depsMap.get(MAP_KEY_ITERATE_KEY));
              }
            } else if (isArrayIndex) {
              run(depsMap.get("length"));
            }
            break;
          case "delete":
            if (!targetIsArray) {
              run(depsMap.get(ITERATE_KEY));
              if (isMap(target)) {
                run(depsMap.get(MAP_KEY_ITERATE_KEY));
              }
            }
            break;
          case "set":
            if (isMap(target)) {
              run(depsMap.get(ITERATE_KEY));
            }
            break;
        }
      }
    }
    endBatch();
  }
  function reactiveReadArray(array) {
    const raw = toRaw(array);
    if (raw === array)
      return raw;
    track(raw, "iterate", ARRAY_ITERATE_KEY);
    return isShallow(array) ? raw : raw.map(toReactive);
  }
  function shallowReadArray(arr) {
    track(arr = toRaw(arr), "iterate", ARRAY_ITERATE_KEY);
    return arr;
  }
  function toWrapped(target, item) {
    if (isReadonly(target)) {
      return isReactive(target) ? toReadonly(toReactive(item)) : toReadonly(item);
    }
    return toReactive(item);
  }
  function iterator(self2, method, wrapValue) {
    const arr = shallowReadArray(self2);
    const iter = arr[method]();
    if (arr !== self2 && !isShallow(self2)) {
      iter._next = iter.next;
      iter.next = () => {
        const result = iter._next();
        if (!result.done) {
          result.value = wrapValue(result.value);
        }
        return result;
      };
    }
    return iter;
  }
  function apply(self2, method, fn, thisArg, wrappedRetFn, args) {
    const arr = shallowReadArray(self2);
    const needsWrap = arr !== self2 && !isShallow(self2);
    const methodFn = arr[method];
    if (methodFn !== arrayProto[method]) {
      const result2 = methodFn.apply(self2, args);
      return needsWrap ? toReactive(result2) : result2;
    }
    let wrappedFn = fn;
    if (arr !== self2) {
      if (needsWrap) {
        wrappedFn = function(item, index) {
          return fn.call(this, toWrapped(self2, item), index, self2);
        };
      } else if (fn.length > 2) {
        wrappedFn = function(item, index) {
          return fn.call(this, item, index, self2);
        };
      }
    }
    const result = methodFn.call(arr, wrappedFn, thisArg);
    return needsWrap && wrappedRetFn ? wrappedRetFn(result) : result;
  }
  function reduce(self2, method, fn, args) {
    const arr = shallowReadArray(self2);
    let wrappedFn = fn;
    if (arr !== self2) {
      if (!isShallow(self2)) {
        wrappedFn = function(acc, item, index) {
          return fn.call(this, acc, toWrapped(self2, item), index, self2);
        };
      } else if (fn.length > 3) {
        wrappedFn = function(acc, item, index) {
          return fn.call(this, acc, item, index, self2);
        };
      }
    }
    return arr[method](wrappedFn, ...args);
  }
  function searchProxy(self2, method, args) {
    const arr = toRaw(self2);
    track(arr, "iterate", ARRAY_ITERATE_KEY);
    const res = arr[method](...args);
    if ((res === -1 || res === false) && isProxy(args[0])) {
      args[0] = toRaw(args[0]);
      return arr[method](...args);
    }
    return res;
  }
  function noTracking(self2, method, args = []) {
    pauseTracking();
    startBatch();
    const res = toRaw(self2)[method].apply(self2, args);
    endBatch();
    resetTracking();
    return res;
  }
  function hasOwnProperty2(key) {
    if (!isSymbol(key))
      key = String(key);
    const obj = toRaw(this);
    track(obj, "has", key);
    return obj.hasOwnProperty(key);
  }
  function createIterableMethod(method, isReadonly2, isShallow2) {
    return function(...args) {
      const target = this["__v_raw"];
      const rawTarget = toRaw(target);
      const targetIsMap = isMap(rawTarget);
      const isPair = method === "entries" || method === Symbol.iterator && targetIsMap;
      const isKeyOnly = method === "keys" && targetIsMap;
      const innerIterator = target[method](...args);
      const wrap = isShallow2 ? toShallow : isReadonly2 ? toReadonly : toReactive;
      !isReadonly2 && track(
        rawTarget,
        "iterate",
        isKeyOnly ? MAP_KEY_ITERATE_KEY : ITERATE_KEY
      );
      return extend(
        Object.create(innerIterator),
        {
          next() {
            const { value, done } = innerIterator.next();
            return done ? { value, done } : {
              value: isPair ? [wrap(value[0]), wrap(value[1])] : wrap(value),
              done
            };
          }
        }
      );
    };
  }
  function createReadonlyMethod(type) {
    return function(...args) {
      if (true) {
        const key = args[0] ? `on key "${args[0]}" ` : ``;
        warn(
          `${capitalize(type)} operation ${key}failed: target is readonly.`,
          toRaw(this)
        );
      }
      return type === "delete" ? false : type === "clear" ? void 0 : this;
    };
  }
  function createInstrumentations(readonly2, shallow) {
    const instrumentations = {
      get(key) {
        const target = this["__v_raw"];
        const rawTarget = toRaw(target);
        const rawKey = toRaw(key);
        if (!readonly2) {
          if (hasChanged(key, rawKey)) {
            track(rawTarget, "get", key);
          }
          track(rawTarget, "get", rawKey);
        }
        const { has } = getProto(rawTarget);
        const wrap = shallow ? toShallow : readonly2 ? toReadonly : toReactive;
        if (has.call(rawTarget, key)) {
          return wrap(target.get(key));
        } else if (has.call(rawTarget, rawKey)) {
          return wrap(target.get(rawKey));
        } else if (target !== rawTarget) {
          target.get(key);
        }
      },
      get size() {
        const target = this["__v_raw"];
        !readonly2 && track(toRaw(target), "iterate", ITERATE_KEY);
        return target.size;
      },
      has(key) {
        const target = this["__v_raw"];
        const rawTarget = toRaw(target);
        const rawKey = toRaw(key);
        if (!readonly2) {
          if (hasChanged(key, rawKey)) {
            track(rawTarget, "has", key);
          }
          track(rawTarget, "has", rawKey);
        }
        return key === rawKey ? target.has(key) : target.has(key) || target.has(rawKey);
      },
      forEach(callback, thisArg) {
        const observed = this;
        const target = observed["__v_raw"];
        const rawTarget = toRaw(target);
        const wrap = shallow ? toShallow : readonly2 ? toReadonly : toReactive;
        !readonly2 && track(rawTarget, "iterate", ITERATE_KEY);
        return target.forEach((value, key) => {
          return callback.call(thisArg, wrap(value), wrap(key), observed);
        });
      }
    };
    extend(
      instrumentations,
      readonly2 ? {
        add: createReadonlyMethod("add"),
        set: createReadonlyMethod("set"),
        delete: createReadonlyMethod("delete"),
        clear: createReadonlyMethod("clear")
      } : {
        add(value) {
          if (!shallow && !isShallow(value) && !isReadonly(value)) {
            value = toRaw(value);
          }
          const target = toRaw(this);
          const proto = getProto(target);
          const hadKey = proto.has.call(target, value);
          if (!hadKey) {
            target.add(value);
            trigger(target, "add", value, value);
          }
          return this;
        },
        set(key, value) {
          if (!shallow && !isShallow(value) && !isReadonly(value)) {
            value = toRaw(value);
          }
          const target = toRaw(this);
          const { has, get } = getProto(target);
          let hadKey = has.call(target, key);
          if (!hadKey) {
            key = toRaw(key);
            hadKey = has.call(target, key);
          } else if (true) {
            checkIdentityKeys(target, has, key);
          }
          const oldValue = get.call(target, key);
          target.set(key, value);
          if (!hadKey) {
            trigger(target, "add", key, value);
          } else if (hasChanged(value, oldValue)) {
            trigger(target, "set", key, value, oldValue);
          }
          return this;
        },
        delete(key) {
          const target = toRaw(this);
          const { has, get } = getProto(target);
          let hadKey = has.call(target, key);
          if (!hadKey) {
            key = toRaw(key);
            hadKey = has.call(target, key);
          } else if (true) {
            checkIdentityKeys(target, has, key);
          }
          const oldValue = get ? get.call(target, key) : void 0;
          const result = target.delete(key);
          if (hadKey) {
            trigger(target, "delete", key, void 0, oldValue);
          }
          return result;
        },
        clear() {
          const target = toRaw(this);
          const hadItems = target.size !== 0;
          const oldTarget = true ? isMap(target) ? new Map(target) : new Set(target) : void 0;
          const result = target.clear();
          if (hadItems) {
            trigger(
              target,
              "clear",
              void 0,
              void 0,
              oldTarget
            );
          }
          return result;
        }
      }
    );
    const iteratorMethods = [
      "keys",
      "values",
      "entries",
      Symbol.iterator
    ];
    iteratorMethods.forEach((method) => {
      instrumentations[method] = createIterableMethod(method, readonly2, shallow);
    });
    return instrumentations;
  }
  function createInstrumentationGetter(isReadonly2, shallow) {
    const instrumentations = createInstrumentations(isReadonly2, shallow);
    return (target, key, receiver) => {
      if (key === "__v_isReactive") {
        return !isReadonly2;
      } else if (key === "__v_isReadonly") {
        return isReadonly2;
      } else if (key === "__v_raw") {
        return target;
      }
      return Reflect.get(
        hasOwn(instrumentations, key) && key in target ? instrumentations : target,
        key,
        receiver
      );
    };
  }
  function checkIdentityKeys(target, has, key) {
    const rawKey = toRaw(key);
    if (rawKey !== key && has.call(target, rawKey)) {
      const type = toRawType(target);
      warn(
        `Reactive ${type} contains both the raw and reactive versions of the same object${type === `Map` ? ` as keys` : ``}, which can lead to inconsistencies. Avoid differentiating between the raw and reactive versions of an object and only use the reactive version if possible.`
      );
    }
  }
  function targetTypeMap(rawType) {
    switch (rawType) {
      case "Object":
      case "Array":
        return 1;
      case "Map":
      case "Set":
      case "WeakMap":
      case "WeakSet":
        return 2;
      default:
        return 0;
    }
  }
  function getTargetType(value) {
    return value["__v_skip"] || !Object.isExtensible(value) ? 0 : targetTypeMap(toRawType(value));
  }
  function reactive(target) {
    if (/* @__PURE__ */ isReadonly(target)) {
      return target;
    }
    return createReactiveObject(
      target,
      false,
      mutableHandlers,
      mutableCollectionHandlers,
      reactiveMap
    );
  }
  function shallowReactive(target) {
    return createReactiveObject(
      target,
      false,
      shallowReactiveHandlers,
      shallowCollectionHandlers,
      shallowReactiveMap
    );
  }
  function readonly(target) {
    return createReactiveObject(
      target,
      true,
      readonlyHandlers,
      readonlyCollectionHandlers,
      readonlyMap
    );
  }
  function shallowReadonly(target) {
    return createReactiveObject(
      target,
      true,
      shallowReadonlyHandlers,
      shallowReadonlyCollectionHandlers,
      shallowReadonlyMap
    );
  }
  function createReactiveObject(target, isReadonly2, baseHandlers, collectionHandlers, proxyMap) {
    if (!isObject(target)) {
      if (true) {
        warn(
          `value cannot be made ${isReadonly2 ? "readonly" : "reactive"}: ${String(
            target
          )}`
        );
      }
      return target;
    }
    if (target["__v_raw"] && !(isReadonly2 && target["__v_isReactive"])) {
      return target;
    }
    const targetType = getTargetType(target);
    if (targetType === 0) {
      return target;
    }
    const existingProxy = proxyMap.get(target);
    if (existingProxy) {
      return existingProxy;
    }
    const proxy = new Proxy(
      target,
      targetType === 2 ? collectionHandlers : baseHandlers
    );
    proxyMap.set(target, proxy);
    return proxy;
  }
  function isReactive(value) {
    if (/* @__PURE__ */ isReadonly(value)) {
      return /* @__PURE__ */ isReactive(value["__v_raw"]);
    }
    return !!(value && value["__v_isReactive"]);
  }
  function isReadonly(value) {
    return !!(value && value["__v_isReadonly"]);
  }
  function isShallow(value) {
    return !!(value && value["__v_isShallow"]);
  }
  function isProxy(value) {
    return value ? !!value["__v_raw"] : false;
  }
  function toRaw(observed) {
    const raw = observed && observed["__v_raw"];
    return raw ? /* @__PURE__ */ toRaw(raw) : observed;
  }
  function markRaw(value) {
    if (!hasOwn(value, "__v_skip") && Object.isExtensible(value)) {
      def(value, "__v_skip", true);
    }
    return value;
  }
  function isRef2(r) {
    return r ? r["__v_isRef"] === true : false;
  }
  function ref(value) {
    return createRef(value, false);
  }
  function createRef(rawValue, shallow) {
    if (/* @__PURE__ */ isRef2(rawValue)) {
      return rawValue;
    }
    return new RefImpl(rawValue, shallow);
  }
  function unref(ref2) {
    return /* @__PURE__ */ isRef2(ref2) ? ref2.value : ref2;
  }
  function proxyRefs(objectWithRefs) {
    return isReactive(objectWithRefs) ? objectWithRefs : new Proxy(objectWithRefs, shallowUnwrapHandlers);
  }
  function computed(getterOrOptions, debugOptions, isSSR = false) {
    let getter;
    let setter;
    if (isFunction(getterOrOptions)) {
      getter = getterOrOptions;
    } else {
      getter = getterOrOptions.get;
      setter = getterOrOptions.set;
    }
    const cRef = new ComputedRefImpl(getter, setter, isSSR);
    if (debugOptions && !isSSR) {
      cRef.onTrack = debugOptions.onTrack;
      cRef.onTrigger = debugOptions.onTrigger;
    }
    return cRef;
  }
  function onWatcherCleanup(cleanupFn, failSilently = false, owner = activeWatcher) {
    if (owner) {
      let cleanups = cleanupMap.get(owner);
      if (!cleanups)
        cleanupMap.set(owner, cleanups = []);
      cleanups.push(cleanupFn);
    } else if (!failSilently) {
      warn(
        `onWatcherCleanup() was called when there was no active watcher to associate with.`
      );
    }
  }
  function watch(source, cb, options = EMPTY_OBJ) {
    const { immediate, deep, once, scheduler, augmentJob, call: call2 } = options;
    const warnInvalidSource = (s) => {
      (options.onWarn || warn)(
        `Invalid watch source: `,
        s,
        `A watch source can only be a getter/effect function, a ref, a reactive object, or an array of these types.`
      );
    };
    const reactiveGetter = (source2) => {
      if (deep)
        return source2;
      if (isShallow(source2) || deep === false || deep === 0)
        return traverse(source2, 1);
      return traverse(source2);
    };
    let effect2;
    let getter;
    let cleanup;
    let boundCleanup;
    let forceTrigger = false;
    let isMultiSource = false;
    if (isRef2(source)) {
      getter = () => source.value;
      forceTrigger = isShallow(source);
    } else if (isReactive(source)) {
      getter = () => reactiveGetter(source);
      forceTrigger = true;
    } else if (isArray(source)) {
      isMultiSource = true;
      forceTrigger = source.some((s) => isReactive(s) || isShallow(s));
      getter = () => source.map((s) => {
        if (isRef2(s)) {
          return s.value;
        } else if (isReactive(s)) {
          return reactiveGetter(s);
        } else if (isFunction(s)) {
          return call2 ? call2(s, 2) : s();
        } else {
          warnInvalidSource(s);
        }
      });
    } else if (isFunction(source)) {
      if (cb) {
        getter = call2 ? () => call2(source, 2) : source;
      } else {
        getter = () => {
          if (cleanup) {
            pauseTracking();
            try {
              cleanup();
            } finally {
              resetTracking();
            }
          }
          const currentEffect = activeWatcher;
          activeWatcher = effect2;
          try {
            return call2 ? call2(source, 3, [boundCleanup]) : source(boundCleanup);
          } finally {
            activeWatcher = currentEffect;
          }
        };
      }
    } else {
      getter = NOOP;
      warnInvalidSource(source);
    }
    if (cb && deep) {
      const baseGetter = getter;
      const depth = deep === true ? Infinity : deep;
      getter = () => traverse(baseGetter(), depth);
    }
    const scope = getCurrentScope();
    const watchHandle = () => {
      effect2.stop();
      if (scope && scope.active) {
        remove(scope.effects, effect2);
      }
    };
    if (once && cb) {
      const _cb = cb;
      cb = (...args) => {
        _cb(...args);
        watchHandle();
      };
    }
    let oldValue = isMultiSource ? new Array(source.length).fill(INITIAL_WATCHER_VALUE) : INITIAL_WATCHER_VALUE;
    const job = (immediateFirstRun) => {
      if (!(effect2.flags & 1) || !effect2.dirty && !immediateFirstRun) {
        return;
      }
      if (cb) {
        const newValue = effect2.run();
        if (deep || forceTrigger || (isMultiSource ? newValue.some((v, i) => hasChanged(v, oldValue[i])) : hasChanged(newValue, oldValue))) {
          if (cleanup) {
            cleanup();
          }
          const currentWatcher = activeWatcher;
          activeWatcher = effect2;
          try {
            const args = [
              newValue,
              oldValue === INITIAL_WATCHER_VALUE ? void 0 : isMultiSource && oldValue[0] === INITIAL_WATCHER_VALUE ? [] : oldValue,
              boundCleanup
            ];
            oldValue = newValue;
            call2 ? call2(cb, 3, args) : cb(...args);
          } finally {
            activeWatcher = currentWatcher;
          }
        }
      } else {
        effect2.run();
      }
    };
    if (augmentJob) {
      augmentJob(job);
    }
    effect2 = new ReactiveEffect(getter);
    effect2.scheduler = scheduler ? () => scheduler(job, false) : job;
    boundCleanup = (fn) => onWatcherCleanup(fn, false, effect2);
    cleanup = effect2.onStop = () => {
      const cleanups = cleanupMap.get(effect2);
      if (cleanups) {
        if (call2) {
          call2(cleanups, 4);
        } else {
          for (const cleanup2 of cleanups)
            cleanup2();
        }
        cleanupMap.delete(effect2);
      }
    };
    if (true) {
      effect2.onTrack = options.onTrack;
      effect2.onTrigger = options.onTrigger;
    }
    if (cb) {
      if (immediate) {
        job(true);
      } else {
        oldValue = effect2.run();
      }
    } else if (scheduler) {
      scheduler(job.bind(null, true), true);
    } else {
      effect2.run();
    }
    watchHandle.pause = effect2.pause.bind(effect2);
    watchHandle.resume = effect2.resume.bind(effect2);
    watchHandle.stop = watchHandle;
    return watchHandle;
  }
  function traverse(value, depth = Infinity, seen) {
    if (depth <= 0 || !isObject(value) || value["__v_skip"]) {
      return value;
    }
    seen = seen || /* @__PURE__ */ new Map();
    if ((seen.get(value) || 0) >= depth) {
      return value;
    }
    seen.set(value, depth);
    depth--;
    if (isRef2(value)) {
      traverse(value.value, depth, seen);
    } else if (isArray(value)) {
      for (let i = 0; i < value.length; i++) {
        traverse(value[i], depth, seen);
      }
    } else if (isSet(value) || isMap(value)) {
      value.forEach((v) => {
        traverse(v, depth, seen);
      });
    } else if (isPlainObject(value)) {
      for (const key in value) {
        traverse(value[key], depth, seen);
      }
      for (const key of Object.getOwnPropertySymbols(value)) {
        if (Object.prototype.propertyIsEnumerable.call(value, key)) {
          traverse(value[key], depth, seen);
        }
      }
    }
    return value;
  }
  var activeEffectScope, EffectScope, activeSub, pausedQueueEffects, ReactiveEffect, batchDepth, batchedSub, batchedComputed, shouldTrack, trackStack, globalVersion, Link, Dep, targetMap, ITERATE_KEY, MAP_KEY_ITERATE_KEY, ARRAY_ITERATE_KEY, arrayInstrumentations, arrayProto, isNonTrackableKeys, builtInSymbols, BaseReactiveHandler, MutableReactiveHandler, ReadonlyReactiveHandler, mutableHandlers, readonlyHandlers, shallowReactiveHandlers, shallowReadonlyHandlers, toShallow, getProto, mutableCollectionHandlers, shallowCollectionHandlers, readonlyCollectionHandlers, shallowReadonlyCollectionHandlers, reactiveMap, shallowReactiveMap, readonlyMap, shallowReadonlyMap, toReactive, toReadonly, RefImpl, shallowUnwrapHandlers, ComputedRefImpl, INITIAL_WATCHER_VALUE, cleanupMap, activeWatcher;
  var init_reactivity_esm_bundler = __esm({
    "../node_modules/@vue/reactivity/dist/reactivity.esm-bundler.js"() {
      init_shared_esm_bundler();
      EffectScope = class {
        constructor(detached = false) {
          this.detached = detached;
          this._active = true;
          this._on = 0;
          this.effects = [];
          this.cleanups = [];
          this._isPaused = false;
          this.__v_skip = true;
          this.parent = activeEffectScope;
          if (!detached && activeEffectScope) {
            this.index = (activeEffectScope.scopes || (activeEffectScope.scopes = [])).push(
              this
            ) - 1;
          }
        }
        get active() {
          return this._active;
        }
        pause() {
          if (this._active) {
            this._isPaused = true;
            let i, l;
            if (this.scopes) {
              for (i = 0, l = this.scopes.length; i < l; i++) {
                this.scopes[i].pause();
              }
            }
            for (i = 0, l = this.effects.length; i < l; i++) {
              this.effects[i].pause();
            }
          }
        }
        resume() {
          if (this._active) {
            if (this._isPaused) {
              this._isPaused = false;
              let i, l;
              if (this.scopes) {
                for (i = 0, l = this.scopes.length; i < l; i++) {
                  this.scopes[i].resume();
                }
              }
              for (i = 0, l = this.effects.length; i < l; i++) {
                this.effects[i].resume();
              }
            }
          }
        }
        run(fn) {
          if (this._active) {
            const currentEffectScope = activeEffectScope;
            try {
              activeEffectScope = this;
              return fn();
            } finally {
              activeEffectScope = currentEffectScope;
            }
          } else if (true) {
            warn(`cannot run an inactive effect scope.`);
          }
        }
        on() {
          if (++this._on === 1) {
            this.prevScope = activeEffectScope;
            activeEffectScope = this;
          }
        }
        off() {
          if (this._on > 0 && --this._on === 0) {
            activeEffectScope = this.prevScope;
            this.prevScope = void 0;
          }
        }
        stop(fromParent) {
          if (this._active) {
            this._active = false;
            let i, l;
            for (i = 0, l = this.effects.length; i < l; i++) {
              this.effects[i].stop();
            }
            this.effects.length = 0;
            for (i = 0, l = this.cleanups.length; i < l; i++) {
              this.cleanups[i]();
            }
            this.cleanups.length = 0;
            if (this.scopes) {
              for (i = 0, l = this.scopes.length; i < l; i++) {
                this.scopes[i].stop(true);
              }
              this.scopes.length = 0;
            }
            if (!this.detached && this.parent && !fromParent) {
              const last = this.parent.scopes.pop();
              if (last && last !== this) {
                this.parent.scopes[this.index] = last;
                last.index = this.index;
              }
            }
            this.parent = void 0;
          }
        }
      };
      pausedQueueEffects = /* @__PURE__ */ new WeakSet();
      ReactiveEffect = class {
        constructor(fn) {
          this.fn = fn;
          this.deps = void 0;
          this.depsTail = void 0;
          this.flags = 1 | 4;
          this.next = void 0;
          this.cleanup = void 0;
          this.scheduler = void 0;
          if (activeEffectScope && activeEffectScope.active) {
            activeEffectScope.effects.push(this);
          }
        }
        pause() {
          this.flags |= 64;
        }
        resume() {
          if (this.flags & 64) {
            this.flags &= -65;
            if (pausedQueueEffects.has(this)) {
              pausedQueueEffects.delete(this);
              this.trigger();
            }
          }
        }
        notify() {
          if (this.flags & 2 && !(this.flags & 32)) {
            return;
          }
          if (!(this.flags & 8)) {
            batch(this);
          }
        }
        run() {
          if (!(this.flags & 1)) {
            return this.fn();
          }
          this.flags |= 2;
          cleanupEffect(this);
          prepareDeps(this);
          const prevEffect = activeSub;
          const prevShouldTrack = shouldTrack;
          activeSub = this;
          shouldTrack = true;
          try {
            return this.fn();
          } finally {
            if (activeSub !== this) {
              warn(
                "Active effect was not restored correctly - this is likely a Vue internal bug."
              );
            }
            cleanupDeps(this);
            activeSub = prevEffect;
            shouldTrack = prevShouldTrack;
            this.flags &= -3;
          }
        }
        stop() {
          if (this.flags & 1) {
            for (let link = this.deps; link; link = link.nextDep) {
              removeSub(link);
            }
            this.deps = this.depsTail = void 0;
            cleanupEffect(this);
            this.onStop && this.onStop();
            this.flags &= -2;
          }
        }
        trigger() {
          if (this.flags & 64) {
            pausedQueueEffects.add(this);
          } else if (this.scheduler) {
            this.scheduler();
          } else {
            this.runIfDirty();
          }
        }
        runIfDirty() {
          if (isDirty(this)) {
            this.run();
          }
        }
        get dirty() {
          return isDirty(this);
        }
      };
      batchDepth = 0;
      shouldTrack = true;
      trackStack = [];
      globalVersion = 0;
      Link = class {
        constructor(sub, dep) {
          this.sub = sub;
          this.dep = dep;
          this.version = dep.version;
          this.nextDep = this.prevDep = this.nextSub = this.prevSub = this.prevActiveLink = void 0;
        }
      };
      Dep = class {
        constructor(computed3) {
          this.computed = computed3;
          this.version = 0;
          this.activeLink = void 0;
          this.subs = void 0;
          this.map = void 0;
          this.key = void 0;
          this.sc = 0;
          this.__v_skip = true;
          if (true) {
            this.subsHead = void 0;
          }
        }
        track(debugInfo) {
          if (!activeSub || !shouldTrack || activeSub === this.computed) {
            return;
          }
          let link = this.activeLink;
          if (link === void 0 || link.sub !== activeSub) {
            link = this.activeLink = new Link(activeSub, this);
            if (!activeSub.deps) {
              activeSub.deps = activeSub.depsTail = link;
            } else {
              link.prevDep = activeSub.depsTail;
              activeSub.depsTail.nextDep = link;
              activeSub.depsTail = link;
            }
            addSub(link);
          } else if (link.version === -1) {
            link.version = this.version;
            if (link.nextDep) {
              const next = link.nextDep;
              next.prevDep = link.prevDep;
              if (link.prevDep) {
                link.prevDep.nextDep = next;
              }
              link.prevDep = activeSub.depsTail;
              link.nextDep = void 0;
              activeSub.depsTail.nextDep = link;
              activeSub.depsTail = link;
              if (activeSub.deps === link) {
                activeSub.deps = next;
              }
            }
          }
          if (activeSub.onTrack) {
            activeSub.onTrack(
              extend(
                {
                  effect: activeSub
                },
                debugInfo
              )
            );
          }
          return link;
        }
        trigger(debugInfo) {
          this.version++;
          globalVersion++;
          this.notify(debugInfo);
        }
        notify(debugInfo) {
          startBatch();
          try {
            if (true) {
              for (let head = this.subsHead; head; head = head.nextSub) {
                if (head.sub.onTrigger && !(head.sub.flags & 8)) {
                  head.sub.onTrigger(
                    extend(
                      {
                        effect: head.sub
                      },
                      debugInfo
                    )
                  );
                }
              }
            }
            for (let link = this.subs; link; link = link.prevSub) {
              if (link.sub.notify()) {
                ;
                link.sub.dep.notify();
              }
            }
          } finally {
            endBatch();
          }
        }
      };
      targetMap = /* @__PURE__ */ new WeakMap();
      ITERATE_KEY = /* @__PURE__ */ Symbol(
        true ? "Object iterate" : ""
      );
      MAP_KEY_ITERATE_KEY = /* @__PURE__ */ Symbol(
        true ? "Map keys iterate" : ""
      );
      ARRAY_ITERATE_KEY = /* @__PURE__ */ Symbol(
        true ? "Array iterate" : ""
      );
      arrayInstrumentations = {
        __proto__: null,
        [Symbol.iterator]() {
          return iterator(this, Symbol.iterator, (item) => toWrapped(this, item));
        },
        concat(...args) {
          return reactiveReadArray(this).concat(
            ...args.map((x) => isArray(x) ? reactiveReadArray(x) : x)
          );
        },
        entries() {
          return iterator(this, "entries", (value) => {
            value[1] = toWrapped(this, value[1]);
            return value;
          });
        },
        every(fn, thisArg) {
          return apply(this, "every", fn, thisArg, void 0, arguments);
        },
        filter(fn, thisArg) {
          return apply(
            this,
            "filter",
            fn,
            thisArg,
            (v) => v.map((item) => toWrapped(this, item)),
            arguments
          );
        },
        find(fn, thisArg) {
          return apply(
            this,
            "find",
            fn,
            thisArg,
            (item) => toWrapped(this, item),
            arguments
          );
        },
        findIndex(fn, thisArg) {
          return apply(this, "findIndex", fn, thisArg, void 0, arguments);
        },
        findLast(fn, thisArg) {
          return apply(
            this,
            "findLast",
            fn,
            thisArg,
            (item) => toWrapped(this, item),
            arguments
          );
        },
        findLastIndex(fn, thisArg) {
          return apply(this, "findLastIndex", fn, thisArg, void 0, arguments);
        },
        forEach(fn, thisArg) {
          return apply(this, "forEach", fn, thisArg, void 0, arguments);
        },
        includes(...args) {
          return searchProxy(this, "includes", args);
        },
        indexOf(...args) {
          return searchProxy(this, "indexOf", args);
        },
        join(separator) {
          return reactiveReadArray(this).join(separator);
        },
        lastIndexOf(...args) {
          return searchProxy(this, "lastIndexOf", args);
        },
        map(fn, thisArg) {
          return apply(this, "map", fn, thisArg, void 0, arguments);
        },
        pop() {
          return noTracking(this, "pop");
        },
        push(...args) {
          return noTracking(this, "push", args);
        },
        reduce(fn, ...args) {
          return reduce(this, "reduce", fn, args);
        },
        reduceRight(fn, ...args) {
          return reduce(this, "reduceRight", fn, args);
        },
        shift() {
          return noTracking(this, "shift");
        },
        some(fn, thisArg) {
          return apply(this, "some", fn, thisArg, void 0, arguments);
        },
        splice(...args) {
          return noTracking(this, "splice", args);
        },
        toReversed() {
          return reactiveReadArray(this).toReversed();
        },
        toSorted(comparer) {
          return reactiveReadArray(this).toSorted(comparer);
        },
        toSpliced(...args) {
          return reactiveReadArray(this).toSpliced(...args);
        },
        unshift(...args) {
          return noTracking(this, "unshift", args);
        },
        values() {
          return iterator(this, "values", (item) => toWrapped(this, item));
        }
      };
      arrayProto = Array.prototype;
      isNonTrackableKeys = /* @__PURE__ */ makeMap(`__proto__,__v_isRef,__isVue`);
      builtInSymbols = new Set(
        /* @__PURE__ */ Object.getOwnPropertyNames(Symbol).filter((key) => key !== "arguments" && key !== "caller").map((key) => Symbol[key]).filter(isSymbol)
      );
      BaseReactiveHandler = class {
        constructor(_isReadonly = false, _isShallow = false) {
          this._isReadonly = _isReadonly;
          this._isShallow = _isShallow;
        }
        get(target, key, receiver) {
          if (key === "__v_skip")
            return target["__v_skip"];
          const isReadonly2 = this._isReadonly, isShallow2 = this._isShallow;
          if (key === "__v_isReactive") {
            return !isReadonly2;
          } else if (key === "__v_isReadonly") {
            return isReadonly2;
          } else if (key === "__v_isShallow") {
            return isShallow2;
          } else if (key === "__v_raw") {
            if (receiver === (isReadonly2 ? isShallow2 ? shallowReadonlyMap : readonlyMap : isShallow2 ? shallowReactiveMap : reactiveMap).get(target) || Object.getPrototypeOf(target) === Object.getPrototypeOf(receiver)) {
              return target;
            }
            return;
          }
          const targetIsArray = isArray(target);
          if (!isReadonly2) {
            let fn;
            if (targetIsArray && (fn = arrayInstrumentations[key])) {
              return fn;
            }
            if (key === "hasOwnProperty") {
              return hasOwnProperty2;
            }
          }
          const res = Reflect.get(
            target,
            key,
            isRef2(target) ? target : receiver
          );
          if (isSymbol(key) ? builtInSymbols.has(key) : isNonTrackableKeys(key)) {
            return res;
          }
          if (!isReadonly2) {
            track(target, "get", key);
          }
          if (isShallow2) {
            return res;
          }
          if (isRef2(res)) {
            const value = targetIsArray && isIntegerKey(key) ? res : res.value;
            return isReadonly2 && isObject(value) ? readonly(value) : value;
          }
          if (isObject(res)) {
            return isReadonly2 ? readonly(res) : reactive(res);
          }
          return res;
        }
      };
      MutableReactiveHandler = class extends BaseReactiveHandler {
        constructor(isShallow2 = false) {
          super(false, isShallow2);
        }
        set(target, key, value, receiver) {
          let oldValue = target[key];
          const isArrayWithIntegerKey = isArray(target) && isIntegerKey(key);
          if (!this._isShallow) {
            const isOldValueReadonly = isReadonly(oldValue);
            if (!isShallow(value) && !isReadonly(value)) {
              oldValue = toRaw(oldValue);
              value = toRaw(value);
            }
            if (!isArrayWithIntegerKey && isRef2(oldValue) && !isRef2(value)) {
              if (isOldValueReadonly) {
                if (true) {
                  warn(
                    `Set operation on key "${String(key)}" failed: target is readonly.`,
                    target[key]
                  );
                }
                return true;
              } else {
                oldValue.value = value;
                return true;
              }
            }
          }
          const hadKey = isArrayWithIntegerKey ? Number(key) < target.length : hasOwn(target, key);
          const result = Reflect.set(
            target,
            key,
            value,
            isRef2(target) ? target : receiver
          );
          if (target === toRaw(receiver)) {
            if (!hadKey) {
              trigger(target, "add", key, value);
            } else if (hasChanged(value, oldValue)) {
              trigger(target, "set", key, value, oldValue);
            }
          }
          return result;
        }
        deleteProperty(target, key) {
          const hadKey = hasOwn(target, key);
          const oldValue = target[key];
          const result = Reflect.deleteProperty(target, key);
          if (result && hadKey) {
            trigger(target, "delete", key, void 0, oldValue);
          }
          return result;
        }
        has(target, key) {
          const result = Reflect.has(target, key);
          if (!isSymbol(key) || !builtInSymbols.has(key)) {
            track(target, "has", key);
          }
          return result;
        }
        ownKeys(target) {
          track(
            target,
            "iterate",
            isArray(target) ? "length" : ITERATE_KEY
          );
          return Reflect.ownKeys(target);
        }
      };
      ReadonlyReactiveHandler = class extends BaseReactiveHandler {
        constructor(isShallow2 = false) {
          super(true, isShallow2);
        }
        set(target, key) {
          if (true) {
            warn(
              `Set operation on key "${String(key)}" failed: target is readonly.`,
              target
            );
          }
          return true;
        }
        deleteProperty(target, key) {
          if (true) {
            warn(
              `Delete operation on key "${String(key)}" failed: target is readonly.`,
              target
            );
          }
          return true;
        }
      };
      mutableHandlers = /* @__PURE__ */ new MutableReactiveHandler();
      readonlyHandlers = /* @__PURE__ */ new ReadonlyReactiveHandler();
      shallowReactiveHandlers = /* @__PURE__ */ new MutableReactiveHandler(true);
      shallowReadonlyHandlers = /* @__PURE__ */ new ReadonlyReactiveHandler(true);
      toShallow = (value) => value;
      getProto = (v) => Reflect.getPrototypeOf(v);
      mutableCollectionHandlers = {
        get: /* @__PURE__ */ createInstrumentationGetter(false, false)
      };
      shallowCollectionHandlers = {
        get: /* @__PURE__ */ createInstrumentationGetter(false, true)
      };
      readonlyCollectionHandlers = {
        get: /* @__PURE__ */ createInstrumentationGetter(true, false)
      };
      shallowReadonlyCollectionHandlers = {
        get: /* @__PURE__ */ createInstrumentationGetter(true, true)
      };
      reactiveMap = /* @__PURE__ */ new WeakMap();
      shallowReactiveMap = /* @__PURE__ */ new WeakMap();
      readonlyMap = /* @__PURE__ */ new WeakMap();
      shallowReadonlyMap = /* @__PURE__ */ new WeakMap();
      toReactive = (value) => isObject(value) ? /* @__PURE__ */ reactive(value) : value;
      toReadonly = (value) => isObject(value) ? /* @__PURE__ */ readonly(value) : value;
      RefImpl = class {
        constructor(value, isShallow2) {
          this.dep = new Dep();
          this["__v_isRef"] = true;
          this["__v_isShallow"] = false;
          this._rawValue = isShallow2 ? value : toRaw(value);
          this._value = isShallow2 ? value : toReactive(value);
          this["__v_isShallow"] = isShallow2;
        }
        get value() {
          if (true) {
            this.dep.track({
              target: this,
              type: "get",
              key: "value"
            });
          } else {
            this.dep.track();
          }
          return this._value;
        }
        set value(newValue) {
          const oldValue = this._rawValue;
          const useDirectValue = this["__v_isShallow"] || isShallow(newValue) || isReadonly(newValue);
          newValue = useDirectValue ? newValue : toRaw(newValue);
          if (hasChanged(newValue, oldValue)) {
            this._rawValue = newValue;
            this._value = useDirectValue ? newValue : toReactive(newValue);
            if (true) {
              this.dep.trigger({
                target: this,
                type: "set",
                key: "value",
                newValue,
                oldValue
              });
            } else {
              this.dep.trigger();
            }
          }
        }
      };
      shallowUnwrapHandlers = {
        get: (target, key, receiver) => key === "__v_raw" ? target : unref(Reflect.get(target, key, receiver)),
        set: (target, key, value, receiver) => {
          const oldValue = target[key];
          if (/* @__PURE__ */ isRef2(oldValue) && !/* @__PURE__ */ isRef2(value)) {
            oldValue.value = value;
            return true;
          } else {
            return Reflect.set(target, key, value, receiver);
          }
        }
      };
      ComputedRefImpl = class {
        constructor(fn, setter, isSSR) {
          this.fn = fn;
          this.setter = setter;
          this._value = void 0;
          this.dep = new Dep(this);
          this.__v_isRef = true;
          this.deps = void 0;
          this.depsTail = void 0;
          this.flags = 16;
          this.globalVersion = globalVersion - 1;
          this.next = void 0;
          this.effect = this;
          this["__v_isReadonly"] = !setter;
          this.isSSR = isSSR;
        }
        notify() {
          this.flags |= 16;
          if (!(this.flags & 8) && activeSub !== this) {
            batch(this, true);
            return true;
          } else if (true)
            ;
        }
        get value() {
          const link = true ? this.dep.track({
            target: this,
            type: "get",
            key: "value"
          }) : this.dep.track();
          refreshComputed(this);
          if (link) {
            link.version = this.dep.version;
          }
          return this._value;
        }
        set value(newValue) {
          if (this.setter) {
            this.setter(newValue);
          } else if (true) {
            warn("Write operation failed: computed value is readonly");
          }
        }
      };
      INITIAL_WATCHER_VALUE = {};
      cleanupMap = /* @__PURE__ */ new WeakMap();
      activeWatcher = void 0;
    }
  });

  // ../node_modules/@vue/runtime-core/dist/runtime-core.esm-bundler.js
  function pushWarningContext(vnode) {
    stack.push(vnode);
  }
  function popWarningContext() {
    stack.pop();
  }
  function warn$1(msg, ...args) {
    if (isWarning)
      return;
    isWarning = true;
    pauseTracking();
    const instance = stack.length ? stack[stack.length - 1].component : null;
    const appWarnHandler = instance && instance.appContext.config.warnHandler;
    const trace = getComponentTrace();
    if (appWarnHandler) {
      callWithErrorHandling(
        appWarnHandler,
        instance,
        11,
        [
          msg + args.map((a) => {
            var _a, _b;
            return (_b = (_a = a.toString) == null ? void 0 : _a.call(a)) != null ? _b : JSON.stringify(a);
          }).join(""),
          instance && instance.proxy,
          trace.map(
            ({ vnode }) => `at <${formatComponentName(instance, vnode.type)}>`
          ).join("\n"),
          trace
        ]
      );
    } else {
      const warnArgs = [`[Vue warn]: ${msg}`, ...args];
      if (trace.length && true) {
        warnArgs.push(`
`, ...formatTrace(trace));
      }
      console.warn(...warnArgs);
    }
    resetTracking();
    isWarning = false;
  }
  function getComponentTrace() {
    let currentVNode = stack[stack.length - 1];
    if (!currentVNode) {
      return [];
    }
    const normalizedStack = [];
    while (currentVNode) {
      const last = normalizedStack[0];
      if (last && last.vnode === currentVNode) {
        last.recurseCount++;
      } else {
        normalizedStack.push({
          vnode: currentVNode,
          recurseCount: 0
        });
      }
      const parentInstance = currentVNode.component && currentVNode.component.parent;
      currentVNode = parentInstance && parentInstance.vnode;
    }
    return normalizedStack;
  }
  function formatTrace(trace) {
    const logs = [];
    trace.forEach((entry, i) => {
      logs.push(...i === 0 ? [] : [`
`], ...formatTraceEntry(entry));
    });
    return logs;
  }
  function formatTraceEntry({ vnode, recurseCount }) {
    const postfix = recurseCount > 0 ? `... (${recurseCount} recursive calls)` : ``;
    const isRoot = vnode.component ? vnode.component.parent == null : false;
    const open = ` at <${formatComponentName(
      vnode.component,
      vnode.type,
      isRoot
    )}`;
    const close = `>` + postfix;
    return vnode.props ? [open, ...formatProps(vnode.props), close] : [open + close];
  }
  function formatProps(props) {
    const res = [];
    const keys = Object.keys(props);
    keys.slice(0, 3).forEach((key) => {
      res.push(...formatProp(key, props[key]));
    });
    if (keys.length > 3) {
      res.push(` ...`);
    }
    return res;
  }
  function formatProp(key, value, raw) {
    if (isString(value)) {
      value = JSON.stringify(value);
      return raw ? value : [`${key}=${value}`];
    } else if (typeof value === "number" || typeof value === "boolean" || value == null) {
      return raw ? value : [`${key}=${value}`];
    } else if (isRef2(value)) {
      value = formatProp(key, toRaw(value.value), true);
      return raw ? value : [`${key}=Ref<`, value, `>`];
    } else if (isFunction(value)) {
      return [`${key}=fn${value.name ? `<${value.name}>` : ``}`];
    } else {
      value = toRaw(value);
      return raw ? value : [`${key}=`, value];
    }
  }
  function callWithErrorHandling(fn, instance, type, args) {
    try {
      return args ? fn(...args) : fn();
    } catch (err) {
      handleError(err, instance, type);
    }
  }
  function callWithAsyncErrorHandling(fn, instance, type, args) {
    if (isFunction(fn)) {
      const res = callWithErrorHandling(fn, instance, type, args);
      if (res && isPromise(res)) {
        res.catch((err) => {
          handleError(err, instance, type);
        });
      }
      return res;
    }
    if (isArray(fn)) {
      const values = [];
      for (let i = 0; i < fn.length; i++) {
        values.push(callWithAsyncErrorHandling(fn[i], instance, type, args));
      }
      return values;
    } else if (true) {
      warn$1(
        `Invalid value type passed to callWithAsyncErrorHandling(): ${typeof fn}`
      );
    }
  }
  function handleError(err, instance, type, throwInDev = true) {
    const contextVNode = instance ? instance.vnode : null;
    const { errorHandler, throwUnhandledErrorInProduction } = instance && instance.appContext.config || EMPTY_OBJ;
    if (instance) {
      let cur = instance.parent;
      const exposedInstance = instance.proxy;
      const errorInfo = true ? ErrorTypeStrings$1[type] : `https://vuejs.org/error-reference/#runtime-${type}`;
      while (cur) {
        const errorCapturedHooks = cur.ec;
        if (errorCapturedHooks) {
          for (let i = 0; i < errorCapturedHooks.length; i++) {
            if (errorCapturedHooks[i](err, exposedInstance, errorInfo) === false) {
              return;
            }
          }
        }
        cur = cur.parent;
      }
      if (errorHandler) {
        pauseTracking();
        callWithErrorHandling(errorHandler, null, 10, [
          err,
          exposedInstance,
          errorInfo
        ]);
        resetTracking();
        return;
      }
    }
    logError(err, type, contextVNode, throwInDev, throwUnhandledErrorInProduction);
  }
  function logError(err, type, contextVNode, throwInDev = true, throwInProd = false) {
    if (true) {
      const info = ErrorTypeStrings$1[type];
      if (contextVNode) {
        pushWarningContext(contextVNode);
      }
      warn$1(`Unhandled error${info ? ` during execution of ${info}` : ``}`);
      if (contextVNode) {
        popWarningContext();
      }
      if (throwInDev) {
        throw err;
      } else {
        console.error(err);
      }
    } else if (throwInProd) {
      throw err;
    } else {
      console.error(err);
    }
  }
  function nextTick(fn) {
    const p2 = currentFlushPromise || resolvedPromise;
    return fn ? p2.then(this ? fn.bind(this) : fn) : p2;
  }
  function findInsertionIndex(id) {
    let start = flushIndex + 1;
    let end = queue.length;
    while (start < end) {
      const middle = start + end >>> 1;
      const middleJob = queue[middle];
      const middleJobId = getId(middleJob);
      if (middleJobId < id || middleJobId === id && middleJob.flags & 2) {
        start = middle + 1;
      } else {
        end = middle;
      }
    }
    return start;
  }
  function queueJob(job) {
    if (!(job.flags & 1)) {
      const jobId = getId(job);
      const lastJob = queue[queue.length - 1];
      if (!lastJob || !(job.flags & 2) && jobId >= getId(lastJob)) {
        queue.push(job);
      } else {
        queue.splice(findInsertionIndex(jobId), 0, job);
      }
      job.flags |= 1;
      queueFlush();
    }
  }
  function queueFlush() {
    if (!currentFlushPromise) {
      currentFlushPromise = resolvedPromise.then(flushJobs);
    }
  }
  function queuePostFlushCb(cb) {
    if (!isArray(cb)) {
      if (activePostFlushCbs && cb.id === -1) {
        activePostFlushCbs.splice(postFlushIndex + 1, 0, cb);
      } else if (!(cb.flags & 1)) {
        pendingPostFlushCbs.push(cb);
        cb.flags |= 1;
      }
    } else {
      pendingPostFlushCbs.push(...cb);
    }
    queueFlush();
  }
  function flushPreFlushCbs(instance, seen, i = flushIndex + 1) {
    if (true) {
      seen = seen || /* @__PURE__ */ new Map();
    }
    for (; i < queue.length; i++) {
      const cb = queue[i];
      if (cb && cb.flags & 2) {
        if (instance && cb.id !== instance.uid) {
          continue;
        }
        if (checkRecursiveUpdates(seen, cb)) {
          continue;
        }
        queue.splice(i, 1);
        i--;
        if (cb.flags & 4) {
          cb.flags &= -2;
        }
        cb();
        if (!(cb.flags & 4)) {
          cb.flags &= -2;
        }
      }
    }
  }
  function flushPostFlushCbs(seen) {
    if (pendingPostFlushCbs.length) {
      const deduped = [...new Set(pendingPostFlushCbs)].sort(
        (a, b) => getId(a) - getId(b)
      );
      pendingPostFlushCbs.length = 0;
      if (activePostFlushCbs) {
        activePostFlushCbs.push(...deduped);
        return;
      }
      activePostFlushCbs = deduped;
      if (true) {
        seen = seen || /* @__PURE__ */ new Map();
      }
      for (postFlushIndex = 0; postFlushIndex < activePostFlushCbs.length; postFlushIndex++) {
        const cb = activePostFlushCbs[postFlushIndex];
        if (checkRecursiveUpdates(seen, cb)) {
          continue;
        }
        if (cb.flags & 4) {
          cb.flags &= -2;
        }
        if (!(cb.flags & 8))
          cb();
        cb.flags &= -2;
      }
      activePostFlushCbs = null;
      postFlushIndex = 0;
    }
  }
  function flushJobs(seen) {
    if (true) {
      seen = seen || /* @__PURE__ */ new Map();
    }
    const check = true ? (job) => checkRecursiveUpdates(seen, job) : NOOP;
    try {
      for (flushIndex = 0; flushIndex < queue.length; flushIndex++) {
        const job = queue[flushIndex];
        if (job && !(job.flags & 8)) {
          if (check(job)) {
            continue;
          }
          if (job.flags & 4) {
            job.flags &= ~1;
          }
          callWithErrorHandling(
            job,
            job.i,
            job.i ? 15 : 14
          );
          if (!(job.flags & 4)) {
            job.flags &= ~1;
          }
        }
      }
    } finally {
      for (; flushIndex < queue.length; flushIndex++) {
        const job = queue[flushIndex];
        if (job) {
          job.flags &= -2;
        }
      }
      flushIndex = -1;
      queue.length = 0;
      flushPostFlushCbs(seen);
      currentFlushPromise = null;
      if (queue.length || pendingPostFlushCbs.length) {
        flushJobs(seen);
      }
    }
  }
  function checkRecursiveUpdates(seen, fn) {
    const count = seen.get(fn) || 0;
    if (count > RECURSION_LIMIT) {
      const instance = fn.i;
      const componentName = instance && getComponentName(instance.type);
      handleError(
        `Maximum recursive updates exceeded${componentName ? ` in component <${componentName}>` : ``}. This means you have a reactive effect that is mutating its own dependencies and thus recursively triggering itself. Possible sources include component template, render function, updated hook or watcher source function.`,
        null,
        10
      );
      return true;
    }
    seen.set(fn, count + 1);
    return false;
  }
  function registerHMR(instance) {
    const id = instance.type.__hmrId;
    let record = map.get(id);
    if (!record) {
      createRecord(id, instance.type);
      record = map.get(id);
    }
    record.instances.add(instance);
  }
  function unregisterHMR(instance) {
    map.get(instance.type.__hmrId).instances.delete(instance);
  }
  function createRecord(id, initialDef) {
    if (map.has(id)) {
      return false;
    }
    map.set(id, {
      initialDef: normalizeClassComponent(initialDef),
      instances: /* @__PURE__ */ new Set()
    });
    return true;
  }
  function normalizeClassComponent(component) {
    return isClassComponent(component) ? component.__vccOpts : component;
  }
  function rerender(id, newRender) {
    const record = map.get(id);
    if (!record) {
      return;
    }
    record.initialDef.render = newRender;
    [...record.instances].forEach((instance) => {
      if (newRender) {
        instance.render = newRender;
        normalizeClassComponent(instance.type).render = newRender;
      }
      instance.renderCache = [];
      isHmrUpdating = true;
      if (!(instance.job.flags & 8)) {
        instance.update();
      }
      isHmrUpdating = false;
    });
  }
  function reload(id, newComp) {
    const record = map.get(id);
    if (!record)
      return;
    newComp = normalizeClassComponent(newComp);
    updateComponentDef(record.initialDef, newComp);
    const instances = [...record.instances];
    for (let i = 0; i < instances.length; i++) {
      const instance = instances[i];
      const oldComp = normalizeClassComponent(instance.type);
      let dirtyInstances = hmrDirtyComponents.get(oldComp);
      if (!dirtyInstances) {
        if (oldComp !== record.initialDef) {
          updateComponentDef(oldComp, newComp);
        }
        hmrDirtyComponents.set(oldComp, dirtyInstances = /* @__PURE__ */ new Set());
      }
      dirtyInstances.add(instance);
      instance.appContext.propsCache.delete(instance.type);
      instance.appContext.emitsCache.delete(instance.type);
      instance.appContext.optionsCache.delete(instance.type);
      if (instance.ceReload) {
        dirtyInstances.add(instance);
        instance.ceReload(newComp.styles);
        dirtyInstances.delete(instance);
      } else if (instance.parent) {
        queueJob(() => {
          if (!(instance.job.flags & 8)) {
            isHmrUpdating = true;
            instance.parent.update();
            isHmrUpdating = false;
            dirtyInstances.delete(instance);
          }
        });
      } else if (instance.appContext.reload) {
        instance.appContext.reload();
      } else if (typeof window !== "undefined") {
        window.location.reload();
      } else {
        console.warn(
          "[HMR] Root or manually mounted instance modified. Full reload required."
        );
      }
      if (instance.root.ce && instance !== instance.root) {
        instance.root.ce._removeChildStyle(oldComp);
      }
    }
    queuePostFlushCb(() => {
      hmrDirtyComponents.clear();
    });
  }
  function updateComponentDef(oldComp, newComp) {
    extend(oldComp, newComp);
    for (const key in oldComp) {
      if (key !== "__file" && !(key in newComp)) {
        delete oldComp[key];
      }
    }
  }
  function tryWrap(fn) {
    return (id, arg) => {
      try {
        return fn(id, arg);
      } catch (e) {
        console.error(e);
        console.warn(
          `[HMR] Something went wrong during Vue component hot-reload. Full reload required.`
        );
      }
    };
  }
  function emit$1(event, ...args) {
    if (devtools$1) {
      devtools$1.emit(event, ...args);
    } else if (!devtoolsNotInstalled) {
      buffer.push({ event, args });
    }
  }
  function setDevtoolsHook$1(hook, target) {
    var _a, _b;
    devtools$1 = hook;
    if (devtools$1) {
      devtools$1.enabled = true;
      buffer.forEach(({ event, args }) => devtools$1.emit(event, ...args));
      buffer = [];
    } else if (typeof window !== "undefined" && window.HTMLElement && !((_b = (_a = window.navigator) == null ? void 0 : _a.userAgent) == null ? void 0 : _b.includes("jsdom"))) {
      const replay = target.__VUE_DEVTOOLS_HOOK_REPLAY__ = target.__VUE_DEVTOOLS_HOOK_REPLAY__ || [];
      replay.push((newHook) => {
        setDevtoolsHook$1(newHook, target);
      });
      setTimeout(() => {
        if (!devtools$1) {
          target.__VUE_DEVTOOLS_HOOK_REPLAY__ = null;
          devtoolsNotInstalled = true;
          buffer = [];
        }
      }, 3e3);
    } else {
      devtoolsNotInstalled = true;
      buffer = [];
    }
  }
  function devtoolsInitApp(app, version2) {
    emit$1("app:init", app, version2, {
      Fragment,
      Text,
      Comment,
      Static
    });
  }
  function devtoolsUnmountApp(app) {
    emit$1("app:unmount", app);
  }
  function createDevtoolsComponentHook(hook) {
    return (component) => {
      emit$1(
        hook,
        component.appContext.app,
        component.uid,
        component.parent ? component.parent.uid : void 0,
        component
      );
    };
  }
  function createDevtoolsPerformanceHook(hook) {
    return (component, type, time) => {
      emit$1(hook, component.appContext.app, component.uid, component, type, time);
    };
  }
  function devtoolsComponentEmit(component, event, params) {
    emit$1(
      "component:emit",
      component.appContext.app,
      component,
      event,
      params
    );
  }
  function setCurrentRenderingInstance(instance) {
    const prev = currentRenderingInstance;
    currentRenderingInstance = instance;
    currentScopeId = instance && instance.type.__scopeId || null;
    return prev;
  }
  function withCtx(fn, ctx = currentRenderingInstance, isNonScopedSlot) {
    if (!ctx)
      return fn;
    if (fn._n) {
      return fn;
    }
    const renderFnWithContext = (...args) => {
      if (renderFnWithContext._d) {
        setBlockTracking(-1);
      }
      const prevInstance = setCurrentRenderingInstance(ctx);
      let res;
      try {
        res = fn(...args);
      } finally {
        setCurrentRenderingInstance(prevInstance);
        if (renderFnWithContext._d) {
          setBlockTracking(1);
        }
      }
      if (true) {
        devtoolsComponentUpdated(ctx);
      }
      return res;
    };
    renderFnWithContext._n = true;
    renderFnWithContext._c = true;
    renderFnWithContext._d = true;
    return renderFnWithContext;
  }
  function validateDirectiveName(name) {
    if (isBuiltInDirective(name)) {
      warn$1("Do not use built-in directive ids as custom directive id: " + name);
    }
  }
  function withDirectives(vnode, directives) {
    if (currentRenderingInstance === null) {
      warn$1(`withDirectives can only be used inside render functions.`);
      return vnode;
    }
    const instance = getComponentPublicInstance(currentRenderingInstance);
    const bindings = vnode.dirs || (vnode.dirs = []);
    for (let i = 0; i < directives.length; i++) {
      let [dir, value, arg, modifiers = EMPTY_OBJ] = directives[i];
      if (dir) {
        if (isFunction(dir)) {
          dir = {
            mounted: dir,
            updated: dir
          };
        }
        if (dir.deep) {
          traverse(value);
        }
        bindings.push({
          dir,
          instance,
          value,
          oldValue: void 0,
          arg,
          modifiers
        });
      }
    }
    return vnode;
  }
  function invokeDirectiveHook(vnode, prevVNode, instance, name) {
    const bindings = vnode.dirs;
    const oldBindings = prevVNode && prevVNode.dirs;
    for (let i = 0; i < bindings.length; i++) {
      const binding = bindings[i];
      if (oldBindings) {
        binding.oldValue = oldBindings[i].value;
      }
      let hook = binding.dir[name];
      if (hook) {
        pauseTracking();
        callWithAsyncErrorHandling(hook, instance, 8, [
          vnode.el,
          binding,
          vnode,
          prevVNode
        ]);
        resetTracking();
      }
    }
  }
  function provide(key, value) {
    if (true) {
      if (!currentInstance || currentInstance.isMounted) {
        warn$1(`provide() can only be used inside setup().`);
      }
    }
    if (currentInstance) {
      let provides = currentInstance.provides;
      const parentProvides = currentInstance.parent && currentInstance.parent.provides;
      if (parentProvides === provides) {
        provides = currentInstance.provides = Object.create(parentProvides);
      }
      provides[key] = value;
    }
  }
  function inject(key, defaultValue, treatDefaultAsFactory = false) {
    const instance = getCurrentInstance();
    if (instance || currentApp) {
      let provides = currentApp ? currentApp._context.provides : instance ? instance.parent == null || instance.ce ? instance.vnode.appContext && instance.vnode.appContext.provides : instance.parent.provides : void 0;
      if (provides && key in provides) {
        return provides[key];
      } else if (arguments.length > 1) {
        return treatDefaultAsFactory && isFunction(defaultValue) ? defaultValue.call(instance && instance.proxy) : defaultValue;
      } else if (true) {
        warn$1(`injection "${String(key)}" not found.`);
      }
    } else if (true) {
      warn$1(`inject() can only be used inside setup() or functional components.`);
    }
  }
  function watch2(source, cb, options) {
    if (!isFunction(cb)) {
      warn$1(
        `\`watch(fn, options?)\` signature has been moved to a separate API. Use \`watchEffect(fn, options?)\` instead. \`watch\` now only supports \`watch(source, cb, options?) signature.`
      );
    }
    return doWatch(source, cb, options);
  }
  function doWatch(source, cb, options = EMPTY_OBJ) {
    const { immediate, deep, flush, once } = options;
    if (!cb) {
      if (immediate !== void 0) {
        warn$1(
          `watch() "immediate" option is only respected when using the watch(source, callback, options?) signature.`
        );
      }
      if (deep !== void 0) {
        warn$1(
          `watch() "deep" option is only respected when using the watch(source, callback, options?) signature.`
        );
      }
      if (once !== void 0) {
        warn$1(
          `watch() "once" option is only respected when using the watch(source, callback, options?) signature.`
        );
      }
    }
    const baseWatchOptions = extend({}, options);
    if (true)
      baseWatchOptions.onWarn = warn$1;
    const runsImmediately = cb && immediate || !cb && flush !== "post";
    let ssrCleanup;
    if (isInSSRComponentSetup) {
      if (flush === "sync") {
        const ctx = useSSRContext();
        ssrCleanup = ctx.__watcherHandles || (ctx.__watcherHandles = []);
      } else if (!runsImmediately) {
        const watchStopHandle = () => {
        };
        watchStopHandle.stop = NOOP;
        watchStopHandle.resume = NOOP;
        watchStopHandle.pause = NOOP;
        return watchStopHandle;
      }
    }
    const instance = currentInstance;
    baseWatchOptions.call = (fn, type, args) => callWithAsyncErrorHandling(fn, instance, type, args);
    let isPre = false;
    if (flush === "post") {
      baseWatchOptions.scheduler = (job) => {
        queuePostRenderEffect(job, instance && instance.suspense);
      };
    } else if (flush !== "sync") {
      isPre = true;
      baseWatchOptions.scheduler = (job, isFirstRun) => {
        if (isFirstRun) {
          job();
        } else {
          queueJob(job);
        }
      };
    }
    baseWatchOptions.augmentJob = (job) => {
      if (cb) {
        job.flags |= 4;
      }
      if (isPre) {
        job.flags |= 2;
        if (instance) {
          job.id = instance.uid;
          job.i = instance;
        }
      }
    };
    const watchHandle = watch(source, cb, baseWatchOptions);
    if (isInSSRComponentSetup) {
      if (ssrCleanup) {
        ssrCleanup.push(watchHandle);
      } else if (runsImmediately) {
        watchHandle();
      }
    }
    return watchHandle;
  }
  function instanceWatch(source, value, options) {
    const publicThis = this.proxy;
    const getter = isString(source) ? source.includes(".") ? createPathGetter(publicThis, source) : () => publicThis[source] : source.bind(publicThis, publicThis);
    let cb;
    if (isFunction(value)) {
      cb = value;
    } else {
      cb = value.handler;
      options = value;
    }
    const reset = setCurrentInstance(this);
    const res = doWatch(getter, cb.bind(publicThis), options);
    reset();
    return res;
  }
  function createPathGetter(ctx, path) {
    const segments = path.split(".");
    return () => {
      let cur = ctx;
      for (let i = 0; i < segments.length && cur; i++) {
        cur = cur[segments[i]];
      }
      return cur;
    };
  }
  function setTransitionHooks(vnode, hooks) {
    if (vnode.shapeFlag & 6 && vnode.component) {
      vnode.transition = hooks;
      setTransitionHooks(vnode.component.subTree, hooks);
    } else if (vnode.shapeFlag & 128) {
      vnode.ssContent.transition = hooks.clone(vnode.ssContent);
      vnode.ssFallback.transition = hooks.clone(vnode.ssFallback);
    } else {
      vnode.transition = hooks;
    }
  }
  function markAsyncBoundary(instance) {
    instance.ids = [instance.ids[0] + instance.ids[2]++ + "-", 0, 0];
  }
  function isTemplateRefKey(refs, key) {
    let desc;
    return !!((desc = Object.getOwnPropertyDescriptor(refs, key)) && !desc.configurable);
  }
  function setRef(rawRef, oldRawRef, parentSuspense, vnode, isUnmount = false) {
    if (isArray(rawRef)) {
      rawRef.forEach(
        (r, i) => setRef(
          r,
          oldRawRef && (isArray(oldRawRef) ? oldRawRef[i] : oldRawRef),
          parentSuspense,
          vnode,
          isUnmount
        )
      );
      return;
    }
    if (isAsyncWrapper(vnode) && !isUnmount) {
      if (vnode.shapeFlag & 512 && vnode.type.__asyncResolved && vnode.component.subTree.component) {
        setRef(rawRef, oldRawRef, parentSuspense, vnode.component.subTree);
      }
      return;
    }
    const refValue = vnode.shapeFlag & 4 ? getComponentPublicInstance(vnode.component) : vnode.el;
    const value = isUnmount ? null : refValue;
    const { i: owner, r: ref2 } = rawRef;
    if (!owner) {
      warn$1(
        `Missing ref owner context. ref cannot be used on hoisted vnodes. A vnode with ref must be created inside the render function.`
      );
      return;
    }
    const oldRef = oldRawRef && oldRawRef.r;
    const refs = owner.refs === EMPTY_OBJ ? owner.refs = {} : owner.refs;
    const setupState = owner.setupState;
    const rawSetupState = toRaw(setupState);
    const canSetSetupRef = setupState === EMPTY_OBJ ? NO : (key) => {
      if (true) {
        if (hasOwn(rawSetupState, key) && !isRef2(rawSetupState[key])) {
          warn$1(
            `Template ref "${key}" used on a non-ref value. It will not work in the production build.`
          );
        }
        if (knownTemplateRefs.has(rawSetupState[key])) {
          return false;
        }
      }
      if (isTemplateRefKey(refs, key)) {
        return false;
      }
      return hasOwn(rawSetupState, key);
    };
    const canSetRef = (ref22, key) => {
      if (knownTemplateRefs.has(ref22)) {
        return false;
      }
      if (key && isTemplateRefKey(refs, key)) {
        return false;
      }
      return true;
    };
    if (oldRef != null && oldRef !== ref2) {
      invalidatePendingSetRef(oldRawRef);
      if (isString(oldRef)) {
        refs[oldRef] = null;
        if (canSetSetupRef(oldRef)) {
          setupState[oldRef] = null;
        }
      } else if (isRef2(oldRef)) {
        const oldRawRefAtom = oldRawRef;
        if (canSetRef(oldRef, oldRawRefAtom.k)) {
          oldRef.value = null;
        }
        if (oldRawRefAtom.k)
          refs[oldRawRefAtom.k] = null;
      }
    }
    if (isFunction(ref2)) {
      callWithErrorHandling(ref2, owner, 12, [value, refs]);
    } else {
      const _isString = isString(ref2);
      const _isRef = isRef2(ref2);
      if (_isString || _isRef) {
        const doSet = () => {
          if (rawRef.f) {
            const existing = _isString ? canSetSetupRef(ref2) ? setupState[ref2] : refs[ref2] : canSetRef(ref2) || !rawRef.k ? ref2.value : refs[rawRef.k];
            if (isUnmount) {
              isArray(existing) && remove(existing, refValue);
            } else {
              if (!isArray(existing)) {
                if (_isString) {
                  refs[ref2] = [refValue];
                  if (canSetSetupRef(ref2)) {
                    setupState[ref2] = refs[ref2];
                  }
                } else {
                  const newVal = [refValue];
                  if (canSetRef(ref2, rawRef.k)) {
                    ref2.value = newVal;
                  }
                  if (rawRef.k)
                    refs[rawRef.k] = newVal;
                }
              } else if (!existing.includes(refValue)) {
                existing.push(refValue);
              }
            }
          } else if (_isString) {
            refs[ref2] = value;
            if (canSetSetupRef(ref2)) {
              setupState[ref2] = value;
            }
          } else if (_isRef) {
            if (canSetRef(ref2, rawRef.k)) {
              ref2.value = value;
            }
            if (rawRef.k)
              refs[rawRef.k] = value;
          } else if (true) {
            warn$1("Invalid template ref type:", ref2, `(${typeof ref2})`);
          }
        };
        if (value) {
          const job = () => {
            doSet();
            pendingSetRefMap.delete(rawRef);
          };
          job.id = -1;
          pendingSetRefMap.set(rawRef, job);
          queuePostRenderEffect(job, parentSuspense);
        } else {
          invalidatePendingSetRef(rawRef);
          doSet();
        }
      } else if (true) {
        warn$1("Invalid template ref type:", ref2, `(${typeof ref2})`);
      }
    }
  }
  function invalidatePendingSetRef(rawRef) {
    const pendingSetRef = pendingSetRefMap.get(rawRef);
    if (pendingSetRef) {
      pendingSetRef.flags |= 8;
      pendingSetRefMap.delete(rawRef);
    }
  }
  function onActivated(hook, target) {
    registerKeepAliveHook(hook, "a", target);
  }
  function onDeactivated(hook, target) {
    registerKeepAliveHook(hook, "da", target);
  }
  function registerKeepAliveHook(hook, type, target = currentInstance) {
    const wrappedHook = hook.__wdc || (hook.__wdc = () => {
      let current = target;
      while (current) {
        if (current.isDeactivated) {
          return;
        }
        current = current.parent;
      }
      return hook();
    });
    injectHook(type, wrappedHook, target);
    if (target) {
      let current = target.parent;
      while (current && current.parent) {
        if (isKeepAlive(current.parent.vnode)) {
          injectToKeepAliveRoot(wrappedHook, type, target, current);
        }
        current = current.parent;
      }
    }
  }
  function injectToKeepAliveRoot(hook, type, target, keepAliveRoot) {
    const injected = injectHook(
      type,
      hook,
      keepAliveRoot,
      true
    );
    onUnmounted(() => {
      remove(keepAliveRoot[type], injected);
    }, target);
  }
  function injectHook(type, hook, target = currentInstance, prepend = false) {
    if (target) {
      const hooks = target[type] || (target[type] = []);
      const wrappedHook = hook.__weh || (hook.__weh = (...args) => {
        pauseTracking();
        const reset = setCurrentInstance(target);
        const res = callWithAsyncErrorHandling(hook, target, type, args);
        reset();
        resetTracking();
        return res;
      });
      if (prepend) {
        hooks.unshift(wrappedHook);
      } else {
        hooks.push(wrappedHook);
      }
      return wrappedHook;
    } else if (true) {
      const apiName = toHandlerKey(ErrorTypeStrings$1[type].replace(/ hook$/, ""));
      warn$1(
        `${apiName} is called when there is no active component instance to be associated with. Lifecycle injection APIs can only be used during execution of setup(). If you are using async setup(), make sure to register lifecycle hooks before the first await statement.`
      );
    }
  }
  function onErrorCaptured(hook, target = currentInstance) {
    injectHook("ec", hook, target);
  }
  function renderList(source, renderItem, cache, index) {
    let ret;
    const cached = cache && cache[index];
    const sourceIsArray = isArray(source);
    if (sourceIsArray || isString(source)) {
      const sourceIsReactiveArray = sourceIsArray && isReactive(source);
      let needsWrap = false;
      let isReadonlySource = false;
      if (sourceIsReactiveArray) {
        needsWrap = !isShallow(source);
        isReadonlySource = isReadonly(source);
        source = shallowReadArray(source);
      }
      ret = new Array(source.length);
      for (let i = 0, l = source.length; i < l; i++) {
        ret[i] = renderItem(
          needsWrap ? isReadonlySource ? toReadonly(toReactive(source[i])) : toReactive(source[i]) : source[i],
          i,
          void 0,
          cached && cached[i]
        );
      }
    } else if (typeof source === "number") {
      if (!Number.isInteger(source)) {
        warn$1(`The v-for range expect an integer value but got ${source}.`);
      }
      ret = new Array(source);
      for (let i = 0; i < source; i++) {
        ret[i] = renderItem(i + 1, i, void 0, cached && cached[i]);
      }
    } else if (isObject(source)) {
      if (source[Symbol.iterator]) {
        ret = Array.from(
          source,
          (item, i) => renderItem(item, i, void 0, cached && cached[i])
        );
      } else {
        const keys = Object.keys(source);
        ret = new Array(keys.length);
        for (let i = 0, l = keys.length; i < l; i++) {
          const key = keys[i];
          ret[i] = renderItem(source[key], key, i, cached && cached[i]);
        }
      }
    } else {
      ret = [];
    }
    if (cache) {
      cache[index] = ret;
    }
    return ret;
  }
  function renderSlot(slots, name, props = {}, fallback, noSlotted) {
    if (currentRenderingInstance.ce || currentRenderingInstance.parent && isAsyncWrapper(currentRenderingInstance.parent) && currentRenderingInstance.parent.ce) {
      const hasProps = Object.keys(props).length > 0;
      if (name !== "default")
        props.name = name;
      return openBlock(), createBlock(
        Fragment,
        null,
        [createVNode("slot", props, fallback && fallback())],
        hasProps ? -2 : 64
      );
    }
    let slot = slots[name];
    if (slot && slot.length > 1) {
      warn$1(
        `SSR-optimized slot function detected in a non-SSR-optimized render function. You need to mark this component with $dynamic-slots in the parent template.`
      );
      slot = () => [];
    }
    if (slot && slot._c) {
      slot._d = false;
    }
    openBlock();
    const validSlotContent = slot && ensureValidVNode(slot(props));
    const slotKey = props.key || validSlotContent && validSlotContent.key;
    const rendered = createBlock(
      Fragment,
      {
        key: (slotKey && !isSymbol(slotKey) ? slotKey : `_${name}`) + (!validSlotContent && fallback ? "_fb" : "")
      },
      validSlotContent || (fallback ? fallback() : []),
      validSlotContent && slots._ === 1 ? 64 : -2
    );
    if (!noSlotted && rendered.scopeId) {
      rendered.slotScopeIds = [rendered.scopeId + "-s"];
    }
    if (slot && slot._c) {
      slot._d = true;
    }
    return rendered;
  }
  function ensureValidVNode(vnodes) {
    return vnodes.some((child) => {
      if (!isVNode(child))
        return true;
      if (child.type === Comment)
        return false;
      if (child.type === Fragment && !ensureValidVNode(child.children))
        return false;
      return true;
    }) ? vnodes : null;
  }
  function createDevRenderContext(instance) {
    const target = {};
    Object.defineProperty(target, `_`, {
      configurable: true,
      enumerable: false,
      get: () => instance
    });
    Object.keys(publicPropertiesMap).forEach((key) => {
      Object.defineProperty(target, key, {
        configurable: true,
        enumerable: false,
        get: () => publicPropertiesMap[key](instance),
        set: NOOP
      });
    });
    return target;
  }
  function exposePropsOnRenderContext(instance) {
    const {
      ctx,
      propsOptions: [propsOptions]
    } = instance;
    if (propsOptions) {
      Object.keys(propsOptions).forEach((key) => {
        Object.defineProperty(ctx, key, {
          enumerable: true,
          configurable: true,
          get: () => instance.props[key],
          set: NOOP
        });
      });
    }
  }
  function exposeSetupStateOnRenderContext(instance) {
    const { ctx, setupState } = instance;
    Object.keys(toRaw(setupState)).forEach((key) => {
      if (!setupState.__isScriptSetup) {
        if (isReservedPrefix(key[0])) {
          warn$1(
            `setup() return property ${JSON.stringify(
              key
            )} should not start with "$" or "_" which are reserved prefixes for Vue internals.`
          );
          return;
        }
        Object.defineProperty(ctx, key, {
          enumerable: true,
          configurable: true,
          get: () => setupState[key],
          set: NOOP
        });
      }
    });
  }
  function normalizePropsOrEmits(props) {
    return isArray(props) ? props.reduce(
      (normalized, p2) => (normalized[p2] = null, normalized),
      {}
    ) : props;
  }
  function createDuplicateChecker() {
    const cache = /* @__PURE__ */ Object.create(null);
    return (type, key) => {
      if (cache[key]) {
        warn$1(`${type} property "${key}" is already defined in ${cache[key]}.`);
      } else {
        cache[key] = type;
      }
    };
  }
  function applyOptions(instance) {
    const options = resolveMergedOptions(instance);
    const publicThis = instance.proxy;
    const ctx = instance.ctx;
    shouldCacheAccess = false;
    if (options.beforeCreate) {
      callHook(options.beforeCreate, instance, "bc");
    }
    const {
      data: dataOptions,
      computed: computedOptions,
      methods,
      watch: watchOptions,
      provide: provideOptions,
      inject: injectOptions,
      created,
      beforeMount,
      mounted,
      beforeUpdate,
      updated,
      activated,
      deactivated,
      beforeDestroy,
      beforeUnmount,
      destroyed,
      unmounted,
      render: render23,
      renderTracked,
      renderTriggered,
      errorCaptured,
      serverPrefetch,
      expose,
      inheritAttrs,
      components,
      directives,
      filters
    } = options;
    const checkDuplicateProperties = true ? createDuplicateChecker() : null;
    if (true) {
      const [propsOptions] = instance.propsOptions;
      if (propsOptions) {
        for (const key in propsOptions) {
          checkDuplicateProperties("Props", key);
        }
      }
    }
    if (injectOptions) {
      resolveInjections(injectOptions, ctx, checkDuplicateProperties);
    }
    if (methods) {
      for (const key in methods) {
        const methodHandler = methods[key];
        if (isFunction(methodHandler)) {
          if (true) {
            Object.defineProperty(ctx, key, {
              value: methodHandler.bind(publicThis),
              configurable: true,
              enumerable: true,
              writable: true
            });
          } else {
            ctx[key] = methodHandler.bind(publicThis);
          }
          if (true) {
            checkDuplicateProperties("Methods", key);
          }
        } else if (true) {
          warn$1(
            `Method "${key}" has type "${typeof methodHandler}" in the component definition. Did you reference the function correctly?`
          );
        }
      }
    }
    if (dataOptions) {
      if (!isFunction(dataOptions)) {
        warn$1(
          `The data option must be a function. Plain object usage is no longer supported.`
        );
      }
      const data = dataOptions.call(publicThis, publicThis);
      if (isPromise(data)) {
        warn$1(
          `data() returned a Promise - note data() cannot be async; If you intend to perform data fetching before component renders, use async setup() + <Suspense>.`
        );
      }
      if (!isObject(data)) {
        warn$1(`data() should return an object.`);
      } else {
        instance.data = reactive(data);
        if (true) {
          for (const key in data) {
            checkDuplicateProperties("Data", key);
            if (!isReservedPrefix(key[0])) {
              Object.defineProperty(ctx, key, {
                configurable: true,
                enumerable: true,
                get: () => data[key],
                set: NOOP
              });
            }
          }
        }
      }
    }
    shouldCacheAccess = true;
    if (computedOptions) {
      for (const key in computedOptions) {
        const opt = computedOptions[key];
        const get = isFunction(opt) ? opt.bind(publicThis, publicThis) : isFunction(opt.get) ? opt.get.bind(publicThis, publicThis) : NOOP;
        if (get === NOOP) {
          warn$1(`Computed property "${key}" has no getter.`);
        }
        const set = !isFunction(opt) && isFunction(opt.set) ? opt.set.bind(publicThis) : true ? () => {
          warn$1(
            `Write operation failed: computed property "${key}" is readonly.`
          );
        } : NOOP;
        const c = computed2({
          get,
          set
        });
        Object.defineProperty(ctx, key, {
          enumerable: true,
          configurable: true,
          get: () => c.value,
          set: (v) => c.value = v
        });
        if (true) {
          checkDuplicateProperties("Computed", key);
        }
      }
    }
    if (watchOptions) {
      for (const key in watchOptions) {
        createWatcher(watchOptions[key], ctx, publicThis, key);
      }
    }
    if (provideOptions) {
      const provides = isFunction(provideOptions) ? provideOptions.call(publicThis) : provideOptions;
      Reflect.ownKeys(provides).forEach((key) => {
        provide(key, provides[key]);
      });
    }
    if (created) {
      callHook(created, instance, "c");
    }
    function registerLifecycleHook(register, hook) {
      if (isArray(hook)) {
        hook.forEach((_hook) => register(_hook.bind(publicThis)));
      } else if (hook) {
        register(hook.bind(publicThis));
      }
    }
    registerLifecycleHook(onBeforeMount, beforeMount);
    registerLifecycleHook(onMounted, mounted);
    registerLifecycleHook(onBeforeUpdate, beforeUpdate);
    registerLifecycleHook(onUpdated, updated);
    registerLifecycleHook(onActivated, activated);
    registerLifecycleHook(onDeactivated, deactivated);
    registerLifecycleHook(onErrorCaptured, errorCaptured);
    registerLifecycleHook(onRenderTracked, renderTracked);
    registerLifecycleHook(onRenderTriggered, renderTriggered);
    registerLifecycleHook(onBeforeUnmount, beforeUnmount);
    registerLifecycleHook(onUnmounted, unmounted);
    registerLifecycleHook(onServerPrefetch, serverPrefetch);
    if (isArray(expose)) {
      if (expose.length) {
        const exposed = instance.exposed || (instance.exposed = {});
        expose.forEach((key) => {
          Object.defineProperty(exposed, key, {
            get: () => publicThis[key],
            set: (val) => publicThis[key] = val,
            enumerable: true
          });
        });
      } else if (!instance.exposed) {
        instance.exposed = {};
      }
    }
    if (render23 && instance.render === NOOP) {
      instance.render = render23;
    }
    if (inheritAttrs != null) {
      instance.inheritAttrs = inheritAttrs;
    }
    if (components)
      instance.components = components;
    if (directives)
      instance.directives = directives;
    if (serverPrefetch) {
      markAsyncBoundary(instance);
    }
  }
  function resolveInjections(injectOptions, ctx, checkDuplicateProperties = NOOP) {
    if (isArray(injectOptions)) {
      injectOptions = normalizeInject(injectOptions);
    }
    for (const key in injectOptions) {
      const opt = injectOptions[key];
      let injected;
      if (isObject(opt)) {
        if ("default" in opt) {
          injected = inject(
            opt.from || key,
            opt.default,
            true
          );
        } else {
          injected = inject(opt.from || key);
        }
      } else {
        injected = inject(opt);
      }
      if (isRef2(injected)) {
        Object.defineProperty(ctx, key, {
          enumerable: true,
          configurable: true,
          get: () => injected.value,
          set: (v) => injected.value = v
        });
      } else {
        ctx[key] = injected;
      }
      if (true) {
        checkDuplicateProperties("Inject", key);
      }
    }
  }
  function callHook(hook, instance, type) {
    callWithAsyncErrorHandling(
      isArray(hook) ? hook.map((h2) => h2.bind(instance.proxy)) : hook.bind(instance.proxy),
      instance,
      type
    );
  }
  function createWatcher(raw, ctx, publicThis, key) {
    let getter = key.includes(".") ? createPathGetter(publicThis, key) : () => publicThis[key];
    if (isString(raw)) {
      const handler = ctx[raw];
      if (isFunction(handler)) {
        {
          watch2(getter, handler);
        }
      } else if (true) {
        warn$1(`Invalid watch handler specified by key "${raw}"`, handler);
      }
    } else if (isFunction(raw)) {
      {
        watch2(getter, raw.bind(publicThis));
      }
    } else if (isObject(raw)) {
      if (isArray(raw)) {
        raw.forEach((r) => createWatcher(r, ctx, publicThis, key));
      } else {
        const handler = isFunction(raw.handler) ? raw.handler.bind(publicThis) : ctx[raw.handler];
        if (isFunction(handler)) {
          watch2(getter, handler, raw);
        } else if (true) {
          warn$1(`Invalid watch handler specified by key "${raw.handler}"`, handler);
        }
      }
    } else if (true) {
      warn$1(`Invalid watch option: "${key}"`, raw);
    }
  }
  function resolveMergedOptions(instance) {
    const base = instance.type;
    const { mixins, extends: extendsOptions } = base;
    const {
      mixins: globalMixins,
      optionsCache: cache,
      config: { optionMergeStrategies }
    } = instance.appContext;
    const cached = cache.get(base);
    let resolved;
    if (cached) {
      resolved = cached;
    } else if (!globalMixins.length && !mixins && !extendsOptions) {
      {
        resolved = base;
      }
    } else {
      resolved = {};
      if (globalMixins.length) {
        globalMixins.forEach(
          (m) => mergeOptions(resolved, m, optionMergeStrategies, true)
        );
      }
      mergeOptions(resolved, base, optionMergeStrategies);
    }
    if (isObject(base)) {
      cache.set(base, resolved);
    }
    return resolved;
  }
  function mergeOptions(to, from, strats, asMixin = false) {
    const { mixins, extends: extendsOptions } = from;
    if (extendsOptions) {
      mergeOptions(to, extendsOptions, strats, true);
    }
    if (mixins) {
      mixins.forEach(
        (m) => mergeOptions(to, m, strats, true)
      );
    }
    for (const key in from) {
      if (asMixin && key === "expose") {
        warn$1(
          `"expose" option is ignored when declared in mixins or extends. It should only be declared in the base component itself.`
        );
      } else {
        const strat = internalOptionMergeStrats[key] || strats && strats[key];
        to[key] = strat ? strat(to[key], from[key]) : from[key];
      }
    }
    return to;
  }
  function mergeDataFn(to, from) {
    if (!from) {
      return to;
    }
    if (!to) {
      return from;
    }
    return function mergedDataFn() {
      return extend(
        isFunction(to) ? to.call(this, this) : to,
        isFunction(from) ? from.call(this, this) : from
      );
    };
  }
  function mergeInject(to, from) {
    return mergeObjectOptions(normalizeInject(to), normalizeInject(from));
  }
  function normalizeInject(raw) {
    if (isArray(raw)) {
      const res = {};
      for (let i = 0; i < raw.length; i++) {
        res[raw[i]] = raw[i];
      }
      return res;
    }
    return raw;
  }
  function mergeAsArray(to, from) {
    return to ? [...new Set([].concat(to, from))] : from;
  }
  function mergeObjectOptions(to, from) {
    return to ? extend(/* @__PURE__ */ Object.create(null), to, from) : from;
  }
  function mergeEmitsOrPropsOptions(to, from) {
    if (to) {
      if (isArray(to) && isArray(from)) {
        return [.../* @__PURE__ */ new Set([...to, ...from])];
      }
      return extend(
        /* @__PURE__ */ Object.create(null),
        normalizePropsOrEmits(to),
        normalizePropsOrEmits(from != null ? from : {})
      );
    } else {
      return from;
    }
  }
  function mergeWatchOptions(to, from) {
    if (!to)
      return from;
    if (!from)
      return to;
    const merged = extend(/* @__PURE__ */ Object.create(null), to);
    for (const key in from) {
      merged[key] = mergeAsArray(to[key], from[key]);
    }
    return merged;
  }
  function createAppContext() {
    return {
      app: null,
      config: {
        isNativeTag: NO,
        performance: false,
        globalProperties: {},
        optionMergeStrategies: {},
        errorHandler: void 0,
        warnHandler: void 0,
        compilerOptions: {}
      },
      mixins: [],
      components: {},
      directives: {},
      provides: /* @__PURE__ */ Object.create(null),
      optionsCache: /* @__PURE__ */ new WeakMap(),
      propsCache: /* @__PURE__ */ new WeakMap(),
      emitsCache: /* @__PURE__ */ new WeakMap()
    };
  }
  function createAppAPI(render23, hydrate) {
    return function createApp2(rootComponent, rootProps = null) {
      if (!isFunction(rootComponent)) {
        rootComponent = extend({}, rootComponent);
      }
      if (rootProps != null && !isObject(rootProps)) {
        warn$1(`root props passed to app.mount() must be an object.`);
        rootProps = null;
      }
      const context = createAppContext();
      const installedPlugins = /* @__PURE__ */ new WeakSet();
      const pluginCleanupFns = [];
      let isMounted = false;
      const app = context.app = {
        _uid: uid$1++,
        _component: rootComponent,
        _props: rootProps,
        _container: null,
        _context: context,
        _instance: null,
        version,
        get config() {
          return context.config;
        },
        set config(v) {
          if (true) {
            warn$1(
              `app.config cannot be replaced. Modify individual options instead.`
            );
          }
        },
        use(plugin, ...options) {
          if (installedPlugins.has(plugin)) {
            warn$1(`Plugin has already been applied to target app.`);
          } else if (plugin && isFunction(plugin.install)) {
            installedPlugins.add(plugin);
            plugin.install(app, ...options);
          } else if (isFunction(plugin)) {
            installedPlugins.add(plugin);
            plugin(app, ...options);
          } else if (true) {
            warn$1(
              `A plugin must either be a function or an object with an "install" function.`
            );
          }
          return app;
        },
        mixin(mixin) {
          if (true) {
            if (!context.mixins.includes(mixin)) {
              context.mixins.push(mixin);
            } else if (true) {
              warn$1(
                "Mixin has already been applied to target app" + (mixin.name ? `: ${mixin.name}` : "")
              );
            }
          } else if (true) {
            warn$1("Mixins are only available in builds supporting Options API");
          }
          return app;
        },
        component(name, component) {
          if (true) {
            validateComponentName(name, context.config);
          }
          if (!component) {
            return context.components[name];
          }
          if (context.components[name]) {
            warn$1(`Component "${name}" has already been registered in target app.`);
          }
          context.components[name] = component;
          return app;
        },
        directive(name, directive) {
          if (true) {
            validateDirectiveName(name);
          }
          if (!directive) {
            return context.directives[name];
          }
          if (context.directives[name]) {
            warn$1(`Directive "${name}" has already been registered in target app.`);
          }
          context.directives[name] = directive;
          return app;
        },
        mount(rootContainer, isHydrate, namespace) {
          if (!isMounted) {
            if (rootContainer.__vue_app__) {
              warn$1(
                `There is already an app instance mounted on the host container.
 If you want to mount another app on the same host container, you need to unmount the previous app by calling \`app.unmount()\` first.`
              );
            }
            const vnode = app._ceVNode || createVNode(rootComponent, rootProps);
            vnode.appContext = context;
            if (namespace === true) {
              namespace = "svg";
            } else if (namespace === false) {
              namespace = void 0;
            }
            if (true) {
              context.reload = () => {
                const cloned = cloneVNode(vnode);
                cloned.el = null;
                render23(cloned, rootContainer, namespace);
              };
            }
            if (isHydrate && hydrate) {
              hydrate(vnode, rootContainer);
            } else {
              render23(vnode, rootContainer, namespace);
            }
            isMounted = true;
            app._container = rootContainer;
            rootContainer.__vue_app__ = app;
            if (true) {
              app._instance = vnode.component;
              devtoolsInitApp(app, version);
            }
            return getComponentPublicInstance(vnode.component);
          } else if (true) {
            warn$1(
              `App has already been mounted.
If you want to remount the same app, move your app creation logic into a factory function and create fresh app instances for each mount - e.g. \`const createMyApp = () => createApp(App)\``
            );
          }
        },
        onUnmount(cleanupFn) {
          if (typeof cleanupFn !== "function") {
            warn$1(
              `Expected function as first argument to app.onUnmount(), but got ${typeof cleanupFn}`
            );
          }
          pluginCleanupFns.push(cleanupFn);
        },
        unmount() {
          if (isMounted) {
            callWithAsyncErrorHandling(
              pluginCleanupFns,
              app._instance,
              16
            );
            render23(null, app._container);
            if (true) {
              app._instance = null;
              devtoolsUnmountApp(app);
            }
            delete app._container.__vue_app__;
          } else if (true) {
            warn$1(`Cannot unmount an app that is not mounted.`);
          }
        },
        provide(key, value) {
          if (key in context.provides) {
            if (hasOwn(context.provides, key)) {
              warn$1(
                `App already provides property with key "${String(key)}". It will be overwritten with the new value.`
              );
            } else {
              warn$1(
                `App already provides property with key "${String(key)}" inherited from its parent element. It will be overwritten with the new value.`
              );
            }
          }
          context.provides[key] = value;
          return app;
        },
        runWithContext(fn) {
          const lastApp = currentApp;
          currentApp = app;
          try {
            return fn();
          } finally {
            currentApp = lastApp;
          }
        }
      };
      return app;
    };
  }
  function emit(instance, event, ...rawArgs) {
    if (instance.isUnmounted)
      return;
    const props = instance.vnode.props || EMPTY_OBJ;
    if (true) {
      const {
        emitsOptions,
        propsOptions: [propsOptions]
      } = instance;
      if (emitsOptions) {
        if (!(event in emitsOptions) && true) {
          if (!propsOptions || !(toHandlerKey(camelize(event)) in propsOptions)) {
            warn$1(
              `Component emitted event "${event}" but it is neither declared in the emits option nor as an "${toHandlerKey(camelize(event))}" prop.`
            );
          }
        } else {
          const validator = emitsOptions[event];
          if (isFunction(validator)) {
            const isValid = validator(...rawArgs);
            if (!isValid) {
              warn$1(
                `Invalid event arguments: event validation failed for event "${event}".`
              );
            }
          }
        }
      }
    }
    let args = rawArgs;
    const isModelListener2 = event.startsWith("update:");
    const modifiers = isModelListener2 && getModelModifiers(props, event.slice(7));
    if (modifiers) {
      if (modifiers.trim) {
        args = rawArgs.map((a) => isString(a) ? a.trim() : a);
      }
      if (modifiers.number) {
        args = rawArgs.map(looseToNumber);
      }
    }
    if (true) {
      devtoolsComponentEmit(instance, event, args);
    }
    if (true) {
      const lowerCaseEvent = event.toLowerCase();
      if (lowerCaseEvent !== event && props[toHandlerKey(lowerCaseEvent)]) {
        warn$1(
          `Event "${lowerCaseEvent}" is emitted in component ${formatComponentName(
            instance,
            instance.type
          )} but the handler is registered for "${event}". Note that HTML attributes are case-insensitive and you cannot use v-on to listen to camelCase events when using in-DOM templates. You should probably use "${hyphenate(
            event
          )}" instead of "${event}".`
        );
      }
    }
    let handlerName;
    let handler = props[handlerName = toHandlerKey(event)] || props[handlerName = toHandlerKey(camelize(event))];
    if (!handler && isModelListener2) {
      handler = props[handlerName = toHandlerKey(hyphenate(event))];
    }
    if (handler) {
      callWithAsyncErrorHandling(
        handler,
        instance,
        6,
        args
      );
    }
    const onceHandler = props[handlerName + `Once`];
    if (onceHandler) {
      if (!instance.emitted) {
        instance.emitted = {};
      } else if (instance.emitted[handlerName]) {
        return;
      }
      instance.emitted[handlerName] = true;
      callWithAsyncErrorHandling(
        onceHandler,
        instance,
        6,
        args
      );
    }
  }
  function normalizeEmitsOptions(comp, appContext, asMixin = false) {
    const cache = asMixin ? mixinEmitsCache : appContext.emitsCache;
    const cached = cache.get(comp);
    if (cached !== void 0) {
      return cached;
    }
    const raw = comp.emits;
    let normalized = {};
    let hasExtends = false;
    if (!isFunction(comp)) {
      const extendEmits = (raw2) => {
        const normalizedFromExtend = normalizeEmitsOptions(raw2, appContext, true);
        if (normalizedFromExtend) {
          hasExtends = true;
          extend(normalized, normalizedFromExtend);
        }
      };
      if (!asMixin && appContext.mixins.length) {
        appContext.mixins.forEach(extendEmits);
      }
      if (comp.extends) {
        extendEmits(comp.extends);
      }
      if (comp.mixins) {
        comp.mixins.forEach(extendEmits);
      }
    }
    if (!raw && !hasExtends) {
      if (isObject(comp)) {
        cache.set(comp, null);
      }
      return null;
    }
    if (isArray(raw)) {
      raw.forEach((key) => normalized[key] = null);
    } else {
      extend(normalized, raw);
    }
    if (isObject(comp)) {
      cache.set(comp, normalized);
    }
    return normalized;
  }
  function isEmitListener(options, key) {
    if (!options || !isOn(key)) {
      return false;
    }
    key = key.slice(2).replace(/Once$/, "");
    return hasOwn(options, key[0].toLowerCase() + key.slice(1)) || hasOwn(options, hyphenate(key)) || hasOwn(options, key);
  }
  function markAttrsAccessed() {
    accessedAttrs = true;
  }
  function renderComponentRoot(instance) {
    const {
      type: Component,
      vnode,
      proxy,
      withProxy,
      propsOptions: [propsOptions],
      slots,
      attrs,
      emit: emit2,
      render: render23,
      renderCache,
      props,
      data,
      setupState,
      ctx,
      inheritAttrs
    } = instance;
    const prev = setCurrentRenderingInstance(instance);
    let result;
    let fallthroughAttrs;
    if (true) {
      accessedAttrs = false;
    }
    try {
      if (vnode.shapeFlag & 4) {
        const proxyToUse = withProxy || proxy;
        const thisProxy = setupState.__isScriptSetup ? new Proxy(proxyToUse, {
          get(target, key, receiver) {
            warn$1(
              `Property '${String(
                key
              )}' was accessed via 'this'. Avoid using 'this' in templates.`
            );
            return Reflect.get(target, key, receiver);
          }
        }) : proxyToUse;
        result = normalizeVNode(
          render23.call(
            thisProxy,
            proxyToUse,
            renderCache,
            true ? shallowReadonly(props) : props,
            setupState,
            data,
            ctx
          )
        );
        fallthroughAttrs = attrs;
      } else {
        const render24 = Component;
        if (attrs === props) {
          markAttrsAccessed();
        }
        result = normalizeVNode(
          render24.length > 1 ? render24(
            true ? shallowReadonly(props) : props,
            true ? {
              get attrs() {
                markAttrsAccessed();
                return shallowReadonly(attrs);
              },
              slots,
              emit: emit2
            } : { attrs, slots, emit: emit2 }
          ) : render24(
            true ? shallowReadonly(props) : props,
            null
          )
        );
        fallthroughAttrs = Component.props ? attrs : getFunctionalFallthrough(attrs);
      }
    } catch (err) {
      blockStack.length = 0;
      handleError(err, instance, 1);
      result = createVNode(Comment);
    }
    let root = result;
    let setRoot = void 0;
    if (result.patchFlag > 0 && result.patchFlag & 2048) {
      [root, setRoot] = getChildRoot(result);
    }
    if (fallthroughAttrs && inheritAttrs !== false) {
      const keys = Object.keys(fallthroughAttrs);
      const { shapeFlag } = root;
      if (keys.length) {
        if (shapeFlag & (1 | 6)) {
          if (propsOptions && keys.some(isModelListener)) {
            fallthroughAttrs = filterModelListeners(
              fallthroughAttrs,
              propsOptions
            );
          }
          root = cloneVNode(root, fallthroughAttrs, false, true);
        } else if (!accessedAttrs && root.type !== Comment) {
          const allAttrs = Object.keys(attrs);
          const eventAttrs = [];
          const extraAttrs = [];
          for (let i = 0, l = allAttrs.length; i < l; i++) {
            const key = allAttrs[i];
            if (isOn(key)) {
              if (!isModelListener(key)) {
                eventAttrs.push(key[2].toLowerCase() + key.slice(3));
              }
            } else {
              extraAttrs.push(key);
            }
          }
          if (extraAttrs.length) {
            warn$1(
              `Extraneous non-props attributes (${extraAttrs.join(", ")}) were passed to component but could not be automatically inherited because component renders fragment or text or teleport root nodes.`
            );
          }
          if (eventAttrs.length) {
            warn$1(
              `Extraneous non-emits event listeners (${eventAttrs.join(", ")}) were passed to component but could not be automatically inherited because component renders fragment or text root nodes. If the listener is intended to be a component custom event listener only, declare it using the "emits" option.`
            );
          }
        }
      }
    }
    if (vnode.dirs) {
      if (!isElementRoot(root)) {
        warn$1(
          `Runtime directive used on component with non-element root node. The directives will not function as intended.`
        );
      }
      root = cloneVNode(root, null, false, true);
      root.dirs = root.dirs ? root.dirs.concat(vnode.dirs) : vnode.dirs;
    }
    if (vnode.transition) {
      if (!isElementRoot(root)) {
        warn$1(
          `Component inside <Transition> renders non-element root node that cannot be animated.`
        );
      }
      setTransitionHooks(root, vnode.transition);
    }
    if (setRoot) {
      setRoot(root);
    } else {
      result = root;
    }
    setCurrentRenderingInstance(prev);
    return result;
  }
  function filterSingleRoot(children, recurse = true) {
    let singleRoot;
    for (let i = 0; i < children.length; i++) {
      const child = children[i];
      if (isVNode(child)) {
        if (child.type !== Comment || child.children === "v-if") {
          if (singleRoot) {
            return;
          } else {
            singleRoot = child;
            if (recurse && singleRoot.patchFlag > 0 && singleRoot.patchFlag & 2048) {
              return filterSingleRoot(singleRoot.children);
            }
          }
        }
      } else {
        return;
      }
    }
    return singleRoot;
  }
  function shouldUpdateComponent(prevVNode, nextVNode, optimized) {
    const { props: prevProps, children: prevChildren, component } = prevVNode;
    const { props: nextProps, children: nextChildren, patchFlag } = nextVNode;
    const emits = component.emitsOptions;
    if ((prevChildren || nextChildren) && isHmrUpdating) {
      return true;
    }
    if (nextVNode.dirs || nextVNode.transition) {
      return true;
    }
    if (optimized && patchFlag >= 0) {
      if (patchFlag & 1024) {
        return true;
      }
      if (patchFlag & 16) {
        if (!prevProps) {
          return !!nextProps;
        }
        return hasPropsChanged(prevProps, nextProps, emits);
      } else if (patchFlag & 8) {
        const dynamicProps = nextVNode.dynamicProps;
        for (let i = 0; i < dynamicProps.length; i++) {
          const key = dynamicProps[i];
          if (hasPropValueChanged(nextProps, prevProps, key) && !isEmitListener(emits, key)) {
            return true;
          }
        }
      }
    } else {
      if (prevChildren || nextChildren) {
        if (!nextChildren || !nextChildren.$stable) {
          return true;
        }
      }
      if (prevProps === nextProps) {
        return false;
      }
      if (!prevProps) {
        return !!nextProps;
      }
      if (!nextProps) {
        return true;
      }
      return hasPropsChanged(prevProps, nextProps, emits);
    }
    return false;
  }
  function hasPropsChanged(prevProps, nextProps, emitsOptions) {
    const nextKeys = Object.keys(nextProps);
    if (nextKeys.length !== Object.keys(prevProps).length) {
      return true;
    }
    for (let i = 0; i < nextKeys.length; i++) {
      const key = nextKeys[i];
      if (hasPropValueChanged(nextProps, prevProps, key) && !isEmitListener(emitsOptions, key)) {
        return true;
      }
    }
    return false;
  }
  function hasPropValueChanged(nextProps, prevProps, key) {
    const nextProp = nextProps[key];
    const prevProp = prevProps[key];
    if (key === "style" && isObject(nextProp) && isObject(prevProp)) {
      return !looseEqual(nextProp, prevProp);
    }
    return nextProp !== prevProp;
  }
  function updateHOCHostEl({ vnode, parent }, el) {
    while (parent) {
      const root = parent.subTree;
      if (root.suspense && root.suspense.activeBranch === vnode) {
        root.el = vnode.el;
      }
      if (root === vnode) {
        (vnode = parent.vnode).el = el;
        parent = parent.parent;
      } else {
        break;
      }
    }
  }
  function initProps(instance, rawProps, isStateful, isSSR = false) {
    const props = {};
    const attrs = createInternalObject();
    instance.propsDefaults = /* @__PURE__ */ Object.create(null);
    setFullProps(instance, rawProps, props, attrs);
    for (const key in instance.propsOptions[0]) {
      if (!(key in props)) {
        props[key] = void 0;
      }
    }
    if (true) {
      validateProps(rawProps || {}, props, instance);
    }
    if (isStateful) {
      instance.props = isSSR ? props : shallowReactive(props);
    } else {
      if (!instance.type.props) {
        instance.props = attrs;
      } else {
        instance.props = props;
      }
    }
    instance.attrs = attrs;
  }
  function isInHmrContext(instance) {
    while (instance) {
      if (instance.type.__hmrId)
        return true;
      instance = instance.parent;
    }
  }
  function updateProps(instance, rawProps, rawPrevProps, optimized) {
    const {
      props,
      attrs,
      vnode: { patchFlag }
    } = instance;
    const rawCurrentProps = toRaw(props);
    const [options] = instance.propsOptions;
    let hasAttrsChanged = false;
    if (!isInHmrContext(instance) && (optimized || patchFlag > 0) && !(patchFlag & 16)) {
      if (patchFlag & 8) {
        const propsToUpdate = instance.vnode.dynamicProps;
        for (let i = 0; i < propsToUpdate.length; i++) {
          let key = propsToUpdate[i];
          if (isEmitListener(instance.emitsOptions, key)) {
            continue;
          }
          const value = rawProps[key];
          if (options) {
            if (hasOwn(attrs, key)) {
              if (value !== attrs[key]) {
                attrs[key] = value;
                hasAttrsChanged = true;
              }
            } else {
              const camelizedKey = camelize(key);
              props[camelizedKey] = resolvePropValue(
                options,
                rawCurrentProps,
                camelizedKey,
                value,
                instance,
                false
              );
            }
          } else {
            if (value !== attrs[key]) {
              attrs[key] = value;
              hasAttrsChanged = true;
            }
          }
        }
      }
    } else {
      if (setFullProps(instance, rawProps, props, attrs)) {
        hasAttrsChanged = true;
      }
      let kebabKey;
      for (const key in rawCurrentProps) {
        if (!rawProps || !hasOwn(rawProps, key) && ((kebabKey = hyphenate(key)) === key || !hasOwn(rawProps, kebabKey))) {
          if (options) {
            if (rawPrevProps && (rawPrevProps[key] !== void 0 || rawPrevProps[kebabKey] !== void 0)) {
              props[key] = resolvePropValue(
                options,
                rawCurrentProps,
                key,
                void 0,
                instance,
                true
              );
            }
          } else {
            delete props[key];
          }
        }
      }
      if (attrs !== rawCurrentProps) {
        for (const key in attrs) {
          if (!rawProps || !hasOwn(rawProps, key) && true) {
            delete attrs[key];
            hasAttrsChanged = true;
          }
        }
      }
    }
    if (hasAttrsChanged) {
      trigger(instance.attrs, "set", "");
    }
    if (true) {
      validateProps(rawProps || {}, props, instance);
    }
  }
  function setFullProps(instance, rawProps, props, attrs) {
    const [options, needCastKeys] = instance.propsOptions;
    let hasAttrsChanged = false;
    let rawCastValues;
    if (rawProps) {
      for (let key in rawProps) {
        if (isReservedProp(key)) {
          continue;
        }
        const value = rawProps[key];
        let camelKey;
        if (options && hasOwn(options, camelKey = camelize(key))) {
          if (!needCastKeys || !needCastKeys.includes(camelKey)) {
            props[camelKey] = value;
          } else {
            (rawCastValues || (rawCastValues = {}))[camelKey] = value;
          }
        } else if (!isEmitListener(instance.emitsOptions, key)) {
          if (!(key in attrs) || value !== attrs[key]) {
            attrs[key] = value;
            hasAttrsChanged = true;
          }
        }
      }
    }
    if (needCastKeys) {
      const rawCurrentProps = toRaw(props);
      const castValues = rawCastValues || EMPTY_OBJ;
      for (let i = 0; i < needCastKeys.length; i++) {
        const key = needCastKeys[i];
        props[key] = resolvePropValue(
          options,
          rawCurrentProps,
          key,
          castValues[key],
          instance,
          !hasOwn(castValues, key)
        );
      }
    }
    return hasAttrsChanged;
  }
  function resolvePropValue(options, props, key, value, instance, isAbsent) {
    const opt = options[key];
    if (opt != null) {
      const hasDefault = hasOwn(opt, "default");
      if (hasDefault && value === void 0) {
        const defaultValue = opt.default;
        if (opt.type !== Function && !opt.skipFactory && isFunction(defaultValue)) {
          const { propsDefaults } = instance;
          if (key in propsDefaults) {
            value = propsDefaults[key];
          } else {
            const reset = setCurrentInstance(instance);
            value = propsDefaults[key] = defaultValue.call(
              null,
              props
            );
            reset();
          }
        } else {
          value = defaultValue;
        }
        if (instance.ce) {
          instance.ce._setProp(key, value);
        }
      }
      if (opt[0]) {
        if (isAbsent && !hasDefault) {
          value = false;
        } else if (opt[1] && (value === "" || value === hyphenate(key))) {
          value = true;
        }
      }
    }
    return value;
  }
  function normalizePropsOptions(comp, appContext, asMixin = false) {
    const cache = asMixin ? mixinPropsCache : appContext.propsCache;
    const cached = cache.get(comp);
    if (cached) {
      return cached;
    }
    const raw = comp.props;
    const normalized = {};
    const needCastKeys = [];
    let hasExtends = false;
    if (!isFunction(comp)) {
      const extendProps = (raw2) => {
        hasExtends = true;
        const [props, keys] = normalizePropsOptions(raw2, appContext, true);
        extend(normalized, props);
        if (keys)
          needCastKeys.push(...keys);
      };
      if (!asMixin && appContext.mixins.length) {
        appContext.mixins.forEach(extendProps);
      }
      if (comp.extends) {
        extendProps(comp.extends);
      }
      if (comp.mixins) {
        comp.mixins.forEach(extendProps);
      }
    }
    if (!raw && !hasExtends) {
      if (isObject(comp)) {
        cache.set(comp, EMPTY_ARR);
      }
      return EMPTY_ARR;
    }
    if (isArray(raw)) {
      for (let i = 0; i < raw.length; i++) {
        if (!isString(raw[i])) {
          warn$1(`props must be strings when using array syntax.`, raw[i]);
        }
        const normalizedKey = camelize(raw[i]);
        if (validatePropName(normalizedKey)) {
          normalized[normalizedKey] = EMPTY_OBJ;
        }
      }
    } else if (raw) {
      if (!isObject(raw)) {
        warn$1(`invalid props options`, raw);
      }
      for (const key in raw) {
        const normalizedKey = camelize(key);
        if (validatePropName(normalizedKey)) {
          const opt = raw[key];
          const prop = normalized[normalizedKey] = isArray(opt) || isFunction(opt) ? { type: opt } : extend({}, opt);
          const propType = prop.type;
          let shouldCast = false;
          let shouldCastTrue = true;
          if (isArray(propType)) {
            for (let index = 0; index < propType.length; ++index) {
              const type = propType[index];
              const typeName = isFunction(type) && type.name;
              if (typeName === "Boolean") {
                shouldCast = true;
                break;
              } else if (typeName === "String") {
                shouldCastTrue = false;
              }
            }
          } else {
            shouldCast = isFunction(propType) && propType.name === "Boolean";
          }
          prop[0] = shouldCast;
          prop[1] = shouldCastTrue;
          if (shouldCast || hasOwn(prop, "default")) {
            needCastKeys.push(normalizedKey);
          }
        }
      }
    }
    const res = [normalized, needCastKeys];
    if (isObject(comp)) {
      cache.set(comp, res);
    }
    return res;
  }
  function validatePropName(key) {
    if (key[0] !== "$" && !isReservedProp(key)) {
      return true;
    } else if (true) {
      warn$1(`Invalid prop name: "${key}" is a reserved property.`);
    }
    return false;
  }
  function getType(ctor) {
    if (ctor === null) {
      return "null";
    }
    if (typeof ctor === "function") {
      return ctor.name || "";
    } else if (typeof ctor === "object") {
      const name = ctor.constructor && ctor.constructor.name;
      return name || "";
    }
    return "";
  }
  function validateProps(rawProps, props, instance) {
    const resolvedValues = toRaw(props);
    const options = instance.propsOptions[0];
    const camelizePropsKey = Object.keys(rawProps).map((key) => camelize(key));
    for (const key in options) {
      let opt = options[key];
      if (opt == null)
        continue;
      validateProp(
        key,
        resolvedValues[key],
        opt,
        true ? shallowReadonly(resolvedValues) : resolvedValues,
        !camelizePropsKey.includes(key)
      );
    }
  }
  function validateProp(name, value, prop, props, isAbsent) {
    const { type, required, validator, skipCheck } = prop;
    if (required && isAbsent) {
      warn$1('Missing required prop: "' + name + '"');
      return;
    }
    if (value == null && !required) {
      return;
    }
    if (type != null && type !== true && !skipCheck) {
      let isValid = false;
      const types = isArray(type) ? type : [type];
      const expectedTypes = [];
      for (let i = 0; i < types.length && !isValid; i++) {
        const { valid, expectedType } = assertType(value, types[i]);
        expectedTypes.push(expectedType || "");
        isValid = valid;
      }
      if (!isValid) {
        warn$1(getInvalidTypeMessage(name, value, expectedTypes));
        return;
      }
    }
    if (validator && !validator(value, props)) {
      warn$1('Invalid prop: custom validator check failed for prop "' + name + '".');
    }
  }
  function assertType(value, type) {
    let valid;
    const expectedType = getType(type);
    if (expectedType === "null") {
      valid = value === null;
    } else if (isSimpleType(expectedType)) {
      const t = typeof value;
      valid = t === expectedType.toLowerCase();
      if (!valid && t === "object") {
        valid = value instanceof type;
      }
    } else if (expectedType === "Object") {
      valid = isObject(value);
    } else if (expectedType === "Array") {
      valid = isArray(value);
    } else {
      valid = value instanceof type;
    }
    return {
      valid,
      expectedType
    };
  }
  function getInvalidTypeMessage(name, value, expectedTypes) {
    if (expectedTypes.length === 0) {
      return `Prop type [] for prop "${name}" won't match anything. Did you mean to use type Array instead?`;
    }
    let message = `Invalid prop: type check failed for prop "${name}". Expected ${expectedTypes.map(capitalize).join(" | ")}`;
    const expectedType = expectedTypes[0];
    const receivedType = toRawType(value);
    const expectedValue = styleValue(value, expectedType);
    const receivedValue = styleValue(value, receivedType);
    if (expectedTypes.length === 1 && isExplicable(expectedType) && !isBoolean(expectedType, receivedType)) {
      message += ` with value ${expectedValue}`;
    }
    message += `, got ${receivedType} `;
    if (isExplicable(receivedType)) {
      message += `with value ${receivedValue}.`;
    }
    return message;
  }
  function styleValue(value, type) {
    if (type === "String") {
      return `"${value}"`;
    } else if (type === "Number") {
      return `${Number(value)}`;
    } else {
      return `${value}`;
    }
  }
  function isExplicable(type) {
    const explicitTypes = ["string", "number", "boolean"];
    return explicitTypes.some((elem) => type.toLowerCase() === elem);
  }
  function isBoolean(...args) {
    return args.some((elem) => elem.toLowerCase() === "boolean");
  }
  function startMeasure(instance, type) {
    if (instance.appContext.config.performance && isSupported()) {
      perf.mark(`vue-${type}-${instance.uid}`);
    }
    if (true) {
      devtoolsPerfStart(instance, type, isSupported() ? perf.now() : Date.now());
    }
  }
  function endMeasure(instance, type) {
    if (instance.appContext.config.performance && isSupported()) {
      const startTag = `vue-${type}-${instance.uid}`;
      const endTag = startTag + `:end`;
      const measureName = `<${formatComponentName(instance, instance.type)}> ${type}`;
      perf.mark(endTag);
      perf.measure(measureName, startTag, endTag);
      perf.clearMeasures(measureName);
      perf.clearMarks(startTag);
      perf.clearMarks(endTag);
    }
    if (true) {
      devtoolsPerfEnd(instance, type, isSupported() ? perf.now() : Date.now());
    }
  }
  function isSupported() {
    if (supported !== void 0) {
      return supported;
    }
    if (typeof window !== "undefined" && window.performance) {
      supported = true;
      perf = window.performance;
    } else {
      supported = false;
    }
    return supported;
  }
  function initFeatureFlags() {
    const needWarn = [];
    if (false) {
      needWarn.push(`__VUE_OPTIONS_API__`);
      getGlobalThis().__VUE_OPTIONS_API__ = true;
    }
    if (false) {
      needWarn.push(`__VUE_PROD_DEVTOOLS__`);
      getGlobalThis().__VUE_PROD_DEVTOOLS__ = false;
    }
    if (typeof __VUE_PROD_HYDRATION_MISMATCH_DETAILS__ !== "boolean") {
      needWarn.push(`__VUE_PROD_HYDRATION_MISMATCH_DETAILS__`);
      getGlobalThis().__VUE_PROD_HYDRATION_MISMATCH_DETAILS__ = false;
    }
    if (needWarn.length) {
      const multi = needWarn.length > 1;
      console.warn(
        `Feature flag${multi ? `s` : ``} ${needWarn.join(", ")} ${multi ? `are` : `is`} not explicitly defined. You are running the esm-bundler build of Vue, which expects these compile-time feature flags to be globally injected via the bundler config in order to get better tree-shaking in the production bundle.

For more details, see https://link.vuejs.org/feature-flags.`
      );
    }
  }
  function createRenderer(options) {
    return baseCreateRenderer(options);
  }
  function baseCreateRenderer(options, createHydrationFns) {
    {
      initFeatureFlags();
    }
    const target = getGlobalThis();
    target.__VUE__ = true;
    if (true) {
      setDevtoolsHook$1(target.__VUE_DEVTOOLS_GLOBAL_HOOK__, target);
    }
    const {
      insert: hostInsert,
      remove: hostRemove,
      patchProp: hostPatchProp,
      createElement: hostCreateElement,
      createText: hostCreateText,
      createComment: hostCreateComment,
      setText: hostSetText,
      setElementText: hostSetElementText,
      parentNode: hostParentNode,
      nextSibling: hostNextSibling,
      setScopeId: hostSetScopeId = NOOP,
      insertStaticContent: hostInsertStaticContent
    } = options;
    const patch = (n1, n2, container, anchor = null, parentComponent = null, parentSuspense = null, namespace = void 0, slotScopeIds = null, optimized = isHmrUpdating ? false : !!n2.dynamicChildren) => {
      if (n1 === n2) {
        return;
      }
      if (n1 && !isSameVNodeType(n1, n2)) {
        anchor = getNextHostNode(n1);
        unmount(n1, parentComponent, parentSuspense, true);
        n1 = null;
      }
      if (n2.patchFlag === -2) {
        optimized = false;
        n2.dynamicChildren = null;
      }
      const { type, ref: ref2, shapeFlag } = n2;
      switch (type) {
        case Text:
          processText(n1, n2, container, anchor);
          break;
        case Comment:
          processCommentNode(n1, n2, container, anchor);
          break;
        case Static:
          if (n1 == null) {
            mountStaticNode(n2, container, anchor, namespace);
          } else if (true) {
            patchStaticNode(n1, n2, container, namespace);
          }
          break;
        case Fragment:
          processFragment(
            n1,
            n2,
            container,
            anchor,
            parentComponent,
            parentSuspense,
            namespace,
            slotScopeIds,
            optimized
          );
          break;
        default:
          if (shapeFlag & 1) {
            processElement(
              n1,
              n2,
              container,
              anchor,
              parentComponent,
              parentSuspense,
              namespace,
              slotScopeIds,
              optimized
            );
          } else if (shapeFlag & 6) {
            processComponent(
              n1,
              n2,
              container,
              anchor,
              parentComponent,
              parentSuspense,
              namespace,
              slotScopeIds,
              optimized
            );
          } else if (shapeFlag & 64) {
            type.process(
              n1,
              n2,
              container,
              anchor,
              parentComponent,
              parentSuspense,
              namespace,
              slotScopeIds,
              optimized,
              internals
            );
          } else if (shapeFlag & 128) {
            type.process(
              n1,
              n2,
              container,
              anchor,
              parentComponent,
              parentSuspense,
              namespace,
              slotScopeIds,
              optimized,
              internals
            );
          } else if (true) {
            warn$1("Invalid VNode type:", type, `(${typeof type})`);
          }
      }
      if (ref2 != null && parentComponent) {
        setRef(ref2, n1 && n1.ref, parentSuspense, n2 || n1, !n2);
      } else if (ref2 == null && n1 && n1.ref != null) {
        setRef(n1.ref, null, parentSuspense, n1, true);
      }
    };
    const processText = (n1, n2, container, anchor) => {
      if (n1 == null) {
        hostInsert(
          n2.el = hostCreateText(n2.children),
          container,
          anchor
        );
      } else {
        const el = n2.el = n1.el;
        if (n2.children !== n1.children) {
          hostSetText(el, n2.children);
        }
      }
    };
    const processCommentNode = (n1, n2, container, anchor) => {
      if (n1 == null) {
        hostInsert(
          n2.el = hostCreateComment(n2.children || ""),
          container,
          anchor
        );
      } else {
        n2.el = n1.el;
      }
    };
    const mountStaticNode = (n2, container, anchor, namespace) => {
      [n2.el, n2.anchor] = hostInsertStaticContent(
        n2.children,
        container,
        anchor,
        namespace,
        n2.el,
        n2.anchor
      );
    };
    const patchStaticNode = (n1, n2, container, namespace) => {
      if (n2.children !== n1.children) {
        const anchor = hostNextSibling(n1.anchor);
        removeStaticNode(n1);
        [n2.el, n2.anchor] = hostInsertStaticContent(
          n2.children,
          container,
          anchor,
          namespace
        );
      } else {
        n2.el = n1.el;
        n2.anchor = n1.anchor;
      }
    };
    const moveStaticNode = ({ el, anchor }, container, nextSibling) => {
      let next;
      while (el && el !== anchor) {
        next = hostNextSibling(el);
        hostInsert(el, container, nextSibling);
        el = next;
      }
      hostInsert(anchor, container, nextSibling);
    };
    const removeStaticNode = ({ el, anchor }) => {
      let next;
      while (el && el !== anchor) {
        next = hostNextSibling(el);
        hostRemove(el);
        el = next;
      }
      hostRemove(anchor);
    };
    const processElement = (n1, n2, container, anchor, parentComponent, parentSuspense, namespace, slotScopeIds, optimized) => {
      if (n2.type === "svg") {
        namespace = "svg";
      } else if (n2.type === "math") {
        namespace = "mathml";
      }
      if (n1 == null) {
        mountElement(
          n2,
          container,
          anchor,
          parentComponent,
          parentSuspense,
          namespace,
          slotScopeIds,
          optimized
        );
      } else {
        const customElement = n1.el && n1.el._isVueCE ? n1.el : null;
        try {
          if (customElement) {
            customElement._beginPatch();
          }
          patchElement(
            n1,
            n2,
            parentComponent,
            parentSuspense,
            namespace,
            slotScopeIds,
            optimized
          );
        } finally {
          if (customElement) {
            customElement._endPatch();
          }
        }
      }
    };
    const mountElement = (vnode, container, anchor, parentComponent, parentSuspense, namespace, slotScopeIds, optimized) => {
      let el;
      let vnodeHook;
      const { props, shapeFlag, transition, dirs } = vnode;
      el = vnode.el = hostCreateElement(
        vnode.type,
        namespace,
        props && props.is,
        props
      );
      if (shapeFlag & 8) {
        hostSetElementText(el, vnode.children);
      } else if (shapeFlag & 16) {
        mountChildren(
          vnode.children,
          el,
          null,
          parentComponent,
          parentSuspense,
          resolveChildrenNamespace(vnode, namespace),
          slotScopeIds,
          optimized
        );
      }
      if (dirs) {
        invokeDirectiveHook(vnode, null, parentComponent, "created");
      }
      setScopeId(el, vnode, vnode.scopeId, slotScopeIds, parentComponent);
      if (props) {
        for (const key in props) {
          if (key !== "value" && !isReservedProp(key)) {
            hostPatchProp(el, key, null, props[key], namespace, parentComponent);
          }
        }
        if ("value" in props) {
          hostPatchProp(el, "value", null, props.value, namespace);
        }
        if (vnodeHook = props.onVnodeBeforeMount) {
          invokeVNodeHook(vnodeHook, parentComponent, vnode);
        }
      }
      if (true) {
        def(el, "__vnode", vnode, true);
        def(el, "__vueParentComponent", parentComponent, true);
      }
      if (dirs) {
        invokeDirectiveHook(vnode, null, parentComponent, "beforeMount");
      }
      const needCallTransitionHooks = needTransition(parentSuspense, transition);
      if (needCallTransitionHooks) {
        transition.beforeEnter(el);
      }
      hostInsert(el, container, anchor);
      if ((vnodeHook = props && props.onVnodeMounted) || needCallTransitionHooks || dirs) {
        queuePostRenderEffect(() => {
          vnodeHook && invokeVNodeHook(vnodeHook, parentComponent, vnode);
          needCallTransitionHooks && transition.enter(el);
          dirs && invokeDirectiveHook(vnode, null, parentComponent, "mounted");
        }, parentSuspense);
      }
    };
    const setScopeId = (el, vnode, scopeId, slotScopeIds, parentComponent) => {
      if (scopeId) {
        hostSetScopeId(el, scopeId);
      }
      if (slotScopeIds) {
        for (let i = 0; i < slotScopeIds.length; i++) {
          hostSetScopeId(el, slotScopeIds[i]);
        }
      }
      if (parentComponent) {
        let subTree = parentComponent.subTree;
        if (subTree.patchFlag > 0 && subTree.patchFlag & 2048) {
          subTree = filterSingleRoot(subTree.children) || subTree;
        }
        if (vnode === subTree || isSuspense(subTree.type) && (subTree.ssContent === vnode || subTree.ssFallback === vnode)) {
          const parentVNode = parentComponent.vnode;
          setScopeId(
            el,
            parentVNode,
            parentVNode.scopeId,
            parentVNode.slotScopeIds,
            parentComponent.parent
          );
        }
      }
    };
    const mountChildren = (children, container, anchor, parentComponent, parentSuspense, namespace, slotScopeIds, optimized, start = 0) => {
      for (let i = start; i < children.length; i++) {
        const child = children[i] = optimized ? cloneIfMounted(children[i]) : normalizeVNode(children[i]);
        patch(
          null,
          child,
          container,
          anchor,
          parentComponent,
          parentSuspense,
          namespace,
          slotScopeIds,
          optimized
        );
      }
    };
    const patchElement = (n1, n2, parentComponent, parentSuspense, namespace, slotScopeIds, optimized) => {
      const el = n2.el = n1.el;
      if (true) {
        el.__vnode = n2;
      }
      let { patchFlag, dynamicChildren, dirs } = n2;
      patchFlag |= n1.patchFlag & 16;
      const oldProps = n1.props || EMPTY_OBJ;
      const newProps = n2.props || EMPTY_OBJ;
      let vnodeHook;
      parentComponent && toggleRecurse(parentComponent, false);
      if (vnodeHook = newProps.onVnodeBeforeUpdate) {
        invokeVNodeHook(vnodeHook, parentComponent, n2, n1);
      }
      if (dirs) {
        invokeDirectiveHook(n2, n1, parentComponent, "beforeUpdate");
      }
      parentComponent && toggleRecurse(parentComponent, true);
      if (isHmrUpdating) {
        patchFlag = 0;
        optimized = false;
        dynamicChildren = null;
      }
      if (oldProps.innerHTML && newProps.innerHTML == null || oldProps.textContent && newProps.textContent == null) {
        hostSetElementText(el, "");
      }
      if (dynamicChildren) {
        patchBlockChildren(
          n1.dynamicChildren,
          dynamicChildren,
          el,
          parentComponent,
          parentSuspense,
          resolveChildrenNamespace(n2, namespace),
          slotScopeIds
        );
        if (true) {
          traverseStaticChildren(n1, n2);
        }
      } else if (!optimized) {
        patchChildren(
          n1,
          n2,
          el,
          null,
          parentComponent,
          parentSuspense,
          resolveChildrenNamespace(n2, namespace),
          slotScopeIds,
          false
        );
      }
      if (patchFlag > 0) {
        if (patchFlag & 16) {
          patchProps(el, oldProps, newProps, parentComponent, namespace);
        } else {
          if (patchFlag & 2) {
            if (oldProps.class !== newProps.class) {
              hostPatchProp(el, "class", null, newProps.class, namespace);
            }
          }
          if (patchFlag & 4) {
            hostPatchProp(el, "style", oldProps.style, newProps.style, namespace);
          }
          if (patchFlag & 8) {
            const propsToUpdate = n2.dynamicProps;
            for (let i = 0; i < propsToUpdate.length; i++) {
              const key = propsToUpdate[i];
              const prev = oldProps[key];
              const next = newProps[key];
              if (next !== prev || key === "value") {
                hostPatchProp(el, key, prev, next, namespace, parentComponent);
              }
            }
          }
        }
        if (patchFlag & 1) {
          if (n1.children !== n2.children) {
            hostSetElementText(el, n2.children);
          }
        }
      } else if (!optimized && dynamicChildren == null) {
        patchProps(el, oldProps, newProps, parentComponent, namespace);
      }
      if ((vnodeHook = newProps.onVnodeUpdated) || dirs) {
        queuePostRenderEffect(() => {
          vnodeHook && invokeVNodeHook(vnodeHook, parentComponent, n2, n1);
          dirs && invokeDirectiveHook(n2, n1, parentComponent, "updated");
        }, parentSuspense);
      }
    };
    const patchBlockChildren = (oldChildren, newChildren, fallbackContainer, parentComponent, parentSuspense, namespace, slotScopeIds) => {
      for (let i = 0; i < newChildren.length; i++) {
        const oldVNode = oldChildren[i];
        const newVNode = newChildren[i];
        const container = oldVNode.el && (oldVNode.type === Fragment || !isSameVNodeType(oldVNode, newVNode) || oldVNode.shapeFlag & (6 | 64 | 128)) ? hostParentNode(oldVNode.el) : fallbackContainer;
        patch(
          oldVNode,
          newVNode,
          container,
          null,
          parentComponent,
          parentSuspense,
          namespace,
          slotScopeIds,
          true
        );
      }
    };
    const patchProps = (el, oldProps, newProps, parentComponent, namespace) => {
      if (oldProps !== newProps) {
        if (oldProps !== EMPTY_OBJ) {
          for (const key in oldProps) {
            if (!isReservedProp(key) && !(key in newProps)) {
              hostPatchProp(
                el,
                key,
                oldProps[key],
                null,
                namespace,
                parentComponent
              );
            }
          }
        }
        for (const key in newProps) {
          if (isReservedProp(key))
            continue;
          const next = newProps[key];
          const prev = oldProps[key];
          if (next !== prev && key !== "value") {
            hostPatchProp(el, key, prev, next, namespace, parentComponent);
          }
        }
        if ("value" in newProps) {
          hostPatchProp(el, "value", oldProps.value, newProps.value, namespace);
        }
      }
    };
    const processFragment = (n1, n2, container, anchor, parentComponent, parentSuspense, namespace, slotScopeIds, optimized) => {
      const fragmentStartAnchor = n2.el = n1 ? n1.el : hostCreateText("");
      const fragmentEndAnchor = n2.anchor = n1 ? n1.anchor : hostCreateText("");
      let { patchFlag, dynamicChildren, slotScopeIds: fragmentSlotScopeIds } = n2;
      if (isHmrUpdating || patchFlag & 2048) {
        patchFlag = 0;
        optimized = false;
        dynamicChildren = null;
      }
      if (fragmentSlotScopeIds) {
        slotScopeIds = slotScopeIds ? slotScopeIds.concat(fragmentSlotScopeIds) : fragmentSlotScopeIds;
      }
      if (n1 == null) {
        hostInsert(fragmentStartAnchor, container, anchor);
        hostInsert(fragmentEndAnchor, container, anchor);
        mountChildren(
          n2.children || [],
          container,
          fragmentEndAnchor,
          parentComponent,
          parentSuspense,
          namespace,
          slotScopeIds,
          optimized
        );
      } else {
        if (patchFlag > 0 && patchFlag & 64 && dynamicChildren && n1.dynamicChildren && n1.dynamicChildren.length === dynamicChildren.length) {
          patchBlockChildren(
            n1.dynamicChildren,
            dynamicChildren,
            container,
            parentComponent,
            parentSuspense,
            namespace,
            slotScopeIds
          );
          if (true) {
            traverseStaticChildren(n1, n2);
          } else if (n2.key != null || parentComponent && n2 === parentComponent.subTree) {
            traverseStaticChildren(
              n1,
              n2,
              true
            );
          }
        } else {
          patchChildren(
            n1,
            n2,
            container,
            fragmentEndAnchor,
            parentComponent,
            parentSuspense,
            namespace,
            slotScopeIds,
            optimized
          );
        }
      }
    };
    const processComponent = (n1, n2, container, anchor, parentComponent, parentSuspense, namespace, slotScopeIds, optimized) => {
      n2.slotScopeIds = slotScopeIds;
      if (n1 == null) {
        if (n2.shapeFlag & 512) {
          parentComponent.ctx.activate(
            n2,
            container,
            anchor,
            namespace,
            optimized
          );
        } else {
          mountComponent(
            n2,
            container,
            anchor,
            parentComponent,
            parentSuspense,
            namespace,
            optimized
          );
        }
      } else {
        updateComponent(n1, n2, optimized);
      }
    };
    const mountComponent = (initialVNode, container, anchor, parentComponent, parentSuspense, namespace, optimized) => {
      const instance = initialVNode.component = createComponentInstance(
        initialVNode,
        parentComponent,
        parentSuspense
      );
      if (instance.type.__hmrId) {
        registerHMR(instance);
      }
      if (true) {
        pushWarningContext(initialVNode);
        startMeasure(instance, `mount`);
      }
      if (isKeepAlive(initialVNode)) {
        instance.ctx.renderer = internals;
      }
      {
        if (true) {
          startMeasure(instance, `init`);
        }
        setupComponent(instance, false, optimized);
        if (true) {
          endMeasure(instance, `init`);
        }
      }
      if (isHmrUpdating)
        initialVNode.el = null;
      if (instance.asyncDep) {
        parentSuspense && parentSuspense.registerDep(instance, setupRenderEffect, optimized);
        if (!initialVNode.el) {
          const placeholder = instance.subTree = createVNode(Comment);
          processCommentNode(null, placeholder, container, anchor);
          initialVNode.placeholder = placeholder.el;
        }
      } else {
        setupRenderEffect(
          instance,
          initialVNode,
          container,
          anchor,
          parentSuspense,
          namespace,
          optimized
        );
      }
      if (true) {
        popWarningContext();
        endMeasure(instance, `mount`);
      }
    };
    const updateComponent = (n1, n2, optimized) => {
      const instance = n2.component = n1.component;
      if (shouldUpdateComponent(n1, n2, optimized)) {
        if (instance.asyncDep && !instance.asyncResolved) {
          if (true) {
            pushWarningContext(n2);
          }
          updateComponentPreRender(instance, n2, optimized);
          if (true) {
            popWarningContext();
          }
          return;
        } else {
          instance.next = n2;
          instance.update();
        }
      } else {
        n2.el = n1.el;
        instance.vnode = n2;
      }
    };
    const setupRenderEffect = (instance, initialVNode, container, anchor, parentSuspense, namespace, optimized) => {
      const componentUpdateFn = () => {
        if (!instance.isMounted) {
          let vnodeHook;
          const { el, props } = initialVNode;
          const { bm, m, parent, root, type } = instance;
          const isAsyncWrapperVNode = isAsyncWrapper(initialVNode);
          toggleRecurse(instance, false);
          if (bm) {
            invokeArrayFns(bm);
          }
          if (!isAsyncWrapperVNode && (vnodeHook = props && props.onVnodeBeforeMount)) {
            invokeVNodeHook(vnodeHook, parent, initialVNode);
          }
          toggleRecurse(instance, true);
          if (el && hydrateNode) {
            const hydrateSubTree = () => {
              if (true) {
                startMeasure(instance, `render`);
              }
              instance.subTree = renderComponentRoot(instance);
              if (true) {
                endMeasure(instance, `render`);
              }
              if (true) {
                startMeasure(instance, `hydrate`);
              }
              hydrateNode(
                el,
                instance.subTree,
                instance,
                parentSuspense,
                null
              );
              if (true) {
                endMeasure(instance, `hydrate`);
              }
            };
            if (isAsyncWrapperVNode && type.__asyncHydrate) {
              type.__asyncHydrate(
                el,
                instance,
                hydrateSubTree
              );
            } else {
              hydrateSubTree();
            }
          } else {
            if (root.ce && root.ce._hasShadowRoot()) {
              root.ce._injectChildStyle(type);
            }
            if (true) {
              startMeasure(instance, `render`);
            }
            const subTree = instance.subTree = renderComponentRoot(instance);
            if (true) {
              endMeasure(instance, `render`);
            }
            if (true) {
              startMeasure(instance, `patch`);
            }
            patch(
              null,
              subTree,
              container,
              anchor,
              instance,
              parentSuspense,
              namespace
            );
            if (true) {
              endMeasure(instance, `patch`);
            }
            initialVNode.el = subTree.el;
          }
          if (m) {
            queuePostRenderEffect(m, parentSuspense);
          }
          if (!isAsyncWrapperVNode && (vnodeHook = props && props.onVnodeMounted)) {
            const scopedInitialVNode = initialVNode;
            queuePostRenderEffect(
              () => invokeVNodeHook(vnodeHook, parent, scopedInitialVNode),
              parentSuspense
            );
          }
          if (initialVNode.shapeFlag & 256 || parent && isAsyncWrapper(parent.vnode) && parent.vnode.shapeFlag & 256) {
            instance.a && queuePostRenderEffect(instance.a, parentSuspense);
          }
          instance.isMounted = true;
          if (true) {
            devtoolsComponentAdded(instance);
          }
          initialVNode = container = anchor = null;
        } else {
          let { next, bu, u, parent, vnode } = instance;
          {
            const nonHydratedAsyncRoot = locateNonHydratedAsyncRoot(instance);
            if (nonHydratedAsyncRoot) {
              if (next) {
                next.el = vnode.el;
                updateComponentPreRender(instance, next, optimized);
              }
              nonHydratedAsyncRoot.asyncDep.then(() => {
                queuePostRenderEffect(() => {
                  if (!instance.isUnmounted)
                    update();
                }, parentSuspense);
              });
              return;
            }
          }
          let originNext = next;
          let vnodeHook;
          if (true) {
            pushWarningContext(next || instance.vnode);
          }
          toggleRecurse(instance, false);
          if (next) {
            next.el = vnode.el;
            updateComponentPreRender(instance, next, optimized);
          } else {
            next = vnode;
          }
          if (bu) {
            invokeArrayFns(bu);
          }
          if (vnodeHook = next.props && next.props.onVnodeBeforeUpdate) {
            invokeVNodeHook(vnodeHook, parent, next, vnode);
          }
          toggleRecurse(instance, true);
          if (true) {
            startMeasure(instance, `render`);
          }
          const nextTree = renderComponentRoot(instance);
          if (true) {
            endMeasure(instance, `render`);
          }
          const prevTree = instance.subTree;
          instance.subTree = nextTree;
          if (true) {
            startMeasure(instance, `patch`);
          }
          patch(
            prevTree,
            nextTree,
            hostParentNode(prevTree.el),
            getNextHostNode(prevTree),
            instance,
            parentSuspense,
            namespace
          );
          if (true) {
            endMeasure(instance, `patch`);
          }
          next.el = nextTree.el;
          if (originNext === null) {
            updateHOCHostEl(instance, nextTree.el);
          }
          if (u) {
            queuePostRenderEffect(u, parentSuspense);
          }
          if (vnodeHook = next.props && next.props.onVnodeUpdated) {
            queuePostRenderEffect(
              () => invokeVNodeHook(vnodeHook, parent, next, vnode),
              parentSuspense
            );
          }
          if (true) {
            devtoolsComponentUpdated(instance);
          }
          if (true) {
            popWarningContext();
          }
        }
      };
      instance.scope.on();
      const effect2 = instance.effect = new ReactiveEffect(componentUpdateFn);
      instance.scope.off();
      const update = instance.update = effect2.run.bind(effect2);
      const job = instance.job = effect2.runIfDirty.bind(effect2);
      job.i = instance;
      job.id = instance.uid;
      effect2.scheduler = () => queueJob(job);
      toggleRecurse(instance, true);
      if (true) {
        effect2.onTrack = instance.rtc ? (e) => invokeArrayFns(instance.rtc, e) : void 0;
        effect2.onTrigger = instance.rtg ? (e) => invokeArrayFns(instance.rtg, e) : void 0;
      }
      update();
    };
    const updateComponentPreRender = (instance, nextVNode, optimized) => {
      nextVNode.component = instance;
      const prevProps = instance.vnode.props;
      instance.vnode = nextVNode;
      instance.next = null;
      updateProps(instance, nextVNode.props, prevProps, optimized);
      updateSlots(instance, nextVNode.children, optimized);
      pauseTracking();
      flushPreFlushCbs(instance);
      resetTracking();
    };
    const patchChildren = (n1, n2, container, anchor, parentComponent, parentSuspense, namespace, slotScopeIds, optimized = false) => {
      const c1 = n1 && n1.children;
      const prevShapeFlag = n1 ? n1.shapeFlag : 0;
      const c2 = n2.children;
      const { patchFlag, shapeFlag } = n2;
      if (patchFlag > 0) {
        if (patchFlag & 128) {
          patchKeyedChildren(
            c1,
            c2,
            container,
            anchor,
            parentComponent,
            parentSuspense,
            namespace,
            slotScopeIds,
            optimized
          );
          return;
        } else if (patchFlag & 256) {
          patchUnkeyedChildren(
            c1,
            c2,
            container,
            anchor,
            parentComponent,
            parentSuspense,
            namespace,
            slotScopeIds,
            optimized
          );
          return;
        }
      }
      if (shapeFlag & 8) {
        if (prevShapeFlag & 16) {
          unmountChildren(c1, parentComponent, parentSuspense);
        }
        if (c2 !== c1) {
          hostSetElementText(container, c2);
        }
      } else {
        if (prevShapeFlag & 16) {
          if (shapeFlag & 16) {
            patchKeyedChildren(
              c1,
              c2,
              container,
              anchor,
              parentComponent,
              parentSuspense,
              namespace,
              slotScopeIds,
              optimized
            );
          } else {
            unmountChildren(c1, parentComponent, parentSuspense, true);
          }
        } else {
          if (prevShapeFlag & 8) {
            hostSetElementText(container, "");
          }
          if (shapeFlag & 16) {
            mountChildren(
              c2,
              container,
              anchor,
              parentComponent,
              parentSuspense,
              namespace,
              slotScopeIds,
              optimized
            );
          }
        }
      }
    };
    const patchUnkeyedChildren = (c1, c2, container, anchor, parentComponent, parentSuspense, namespace, slotScopeIds, optimized) => {
      c1 = c1 || EMPTY_ARR;
      c2 = c2 || EMPTY_ARR;
      const oldLength = c1.length;
      const newLength = c2.length;
      const commonLength = Math.min(oldLength, newLength);
      let i;
      for (i = 0; i < commonLength; i++) {
        const nextChild = c2[i] = optimized ? cloneIfMounted(c2[i]) : normalizeVNode(c2[i]);
        patch(
          c1[i],
          nextChild,
          container,
          null,
          parentComponent,
          parentSuspense,
          namespace,
          slotScopeIds,
          optimized
        );
      }
      if (oldLength > newLength) {
        unmountChildren(
          c1,
          parentComponent,
          parentSuspense,
          true,
          false,
          commonLength
        );
      } else {
        mountChildren(
          c2,
          container,
          anchor,
          parentComponent,
          parentSuspense,
          namespace,
          slotScopeIds,
          optimized,
          commonLength
        );
      }
    };
    const patchKeyedChildren = (c1, c2, container, parentAnchor, parentComponent, parentSuspense, namespace, slotScopeIds, optimized) => {
      let i = 0;
      const l2 = c2.length;
      let e1 = c1.length - 1;
      let e2 = l2 - 1;
      while (i <= e1 && i <= e2) {
        const n1 = c1[i];
        const n2 = c2[i] = optimized ? cloneIfMounted(c2[i]) : normalizeVNode(c2[i]);
        if (isSameVNodeType(n1, n2)) {
          patch(
            n1,
            n2,
            container,
            null,
            parentComponent,
            parentSuspense,
            namespace,
            slotScopeIds,
            optimized
          );
        } else {
          break;
        }
        i++;
      }
      while (i <= e1 && i <= e2) {
        const n1 = c1[e1];
        const n2 = c2[e2] = optimized ? cloneIfMounted(c2[e2]) : normalizeVNode(c2[e2]);
        if (isSameVNodeType(n1, n2)) {
          patch(
            n1,
            n2,
            container,
            null,
            parentComponent,
            parentSuspense,
            namespace,
            slotScopeIds,
            optimized
          );
        } else {
          break;
        }
        e1--;
        e2--;
      }
      if (i > e1) {
        if (i <= e2) {
          const nextPos = e2 + 1;
          const anchor = nextPos < l2 ? c2[nextPos].el : parentAnchor;
          while (i <= e2) {
            patch(
              null,
              c2[i] = optimized ? cloneIfMounted(c2[i]) : normalizeVNode(c2[i]),
              container,
              anchor,
              parentComponent,
              parentSuspense,
              namespace,
              slotScopeIds,
              optimized
            );
            i++;
          }
        }
      } else if (i > e2) {
        while (i <= e1) {
          unmount(c1[i], parentComponent, parentSuspense, true);
          i++;
        }
      } else {
        const s1 = i;
        const s2 = i;
        const keyToNewIndexMap = /* @__PURE__ */ new Map();
        for (i = s2; i <= e2; i++) {
          const nextChild = c2[i] = optimized ? cloneIfMounted(c2[i]) : normalizeVNode(c2[i]);
          if (nextChild.key != null) {
            if (keyToNewIndexMap.has(nextChild.key)) {
              warn$1(
                `Duplicate keys found during update:`,
                JSON.stringify(nextChild.key),
                `Make sure keys are unique.`
              );
            }
            keyToNewIndexMap.set(nextChild.key, i);
          }
        }
        let j;
        let patched = 0;
        const toBePatched = e2 - s2 + 1;
        let moved = false;
        let maxNewIndexSoFar = 0;
        const newIndexToOldIndexMap = new Array(toBePatched);
        for (i = 0; i < toBePatched; i++)
          newIndexToOldIndexMap[i] = 0;
        for (i = s1; i <= e1; i++) {
          const prevChild = c1[i];
          if (patched >= toBePatched) {
            unmount(prevChild, parentComponent, parentSuspense, true);
            continue;
          }
          let newIndex;
          if (prevChild.key != null) {
            newIndex = keyToNewIndexMap.get(prevChild.key);
          } else {
            for (j = s2; j <= e2; j++) {
              if (newIndexToOldIndexMap[j - s2] === 0 && isSameVNodeType(prevChild, c2[j])) {
                newIndex = j;
                break;
              }
            }
          }
          if (newIndex === void 0) {
            unmount(prevChild, parentComponent, parentSuspense, true);
          } else {
            newIndexToOldIndexMap[newIndex - s2] = i + 1;
            if (newIndex >= maxNewIndexSoFar) {
              maxNewIndexSoFar = newIndex;
            } else {
              moved = true;
            }
            patch(
              prevChild,
              c2[newIndex],
              container,
              null,
              parentComponent,
              parentSuspense,
              namespace,
              slotScopeIds,
              optimized
            );
            patched++;
          }
        }
        const increasingNewIndexSequence = moved ? getSequence(newIndexToOldIndexMap) : EMPTY_ARR;
        j = increasingNewIndexSequence.length - 1;
        for (i = toBePatched - 1; i >= 0; i--) {
          const nextIndex = s2 + i;
          const nextChild = c2[nextIndex];
          const anchorVNode = c2[nextIndex + 1];
          const anchor = nextIndex + 1 < l2 ? anchorVNode.el || resolveAsyncComponentPlaceholder(anchorVNode) : parentAnchor;
          if (newIndexToOldIndexMap[i] === 0) {
            patch(
              null,
              nextChild,
              container,
              anchor,
              parentComponent,
              parentSuspense,
              namespace,
              slotScopeIds,
              optimized
            );
          } else if (moved) {
            if (j < 0 || i !== increasingNewIndexSequence[j]) {
              move(nextChild, container, anchor, 2);
            } else {
              j--;
            }
          }
        }
      }
    };
    const move = (vnode, container, anchor, moveType, parentSuspense = null) => {
      const { el, type, transition, children, shapeFlag } = vnode;
      if (shapeFlag & 6) {
        move(vnode.component.subTree, container, anchor, moveType);
        return;
      }
      if (shapeFlag & 128) {
        vnode.suspense.move(container, anchor, moveType);
        return;
      }
      if (shapeFlag & 64) {
        type.move(vnode, container, anchor, internals);
        return;
      }
      if (type === Fragment) {
        hostInsert(el, container, anchor);
        for (let i = 0; i < children.length; i++) {
          move(children[i], container, anchor, moveType);
        }
        hostInsert(vnode.anchor, container, anchor);
        return;
      }
      if (type === Static) {
        moveStaticNode(vnode, container, anchor);
        return;
      }
      const needTransition2 = moveType !== 2 && shapeFlag & 1 && transition;
      if (needTransition2) {
        if (moveType === 0) {
          transition.beforeEnter(el);
          hostInsert(el, container, anchor);
          queuePostRenderEffect(() => transition.enter(el), parentSuspense);
        } else {
          const { leave, delayLeave, afterLeave } = transition;
          const remove22 = () => {
            if (vnode.ctx.isUnmounted) {
              hostRemove(el);
            } else {
              hostInsert(el, container, anchor);
            }
          };
          const performLeave = () => {
            if (el._isLeaving) {
              el[leaveCbKey](
                true
              );
            }
            leave(el, () => {
              remove22();
              afterLeave && afterLeave();
            });
          };
          if (delayLeave) {
            delayLeave(el, remove22, performLeave);
          } else {
            performLeave();
          }
        }
      } else {
        hostInsert(el, container, anchor);
      }
    };
    const unmount = (vnode, parentComponent, parentSuspense, doRemove = false, optimized = false) => {
      const {
        type,
        props,
        ref: ref2,
        children,
        dynamicChildren,
        shapeFlag,
        patchFlag,
        dirs,
        cacheIndex
      } = vnode;
      if (patchFlag === -2) {
        optimized = false;
      }
      if (ref2 != null) {
        pauseTracking();
        setRef(ref2, null, parentSuspense, vnode, true);
        resetTracking();
      }
      if (cacheIndex != null) {
        parentComponent.renderCache[cacheIndex] = void 0;
      }
      if (shapeFlag & 256) {
        parentComponent.ctx.deactivate(vnode);
        return;
      }
      const shouldInvokeDirs = shapeFlag & 1 && dirs;
      const shouldInvokeVnodeHook = !isAsyncWrapper(vnode);
      let vnodeHook;
      if (shouldInvokeVnodeHook && (vnodeHook = props && props.onVnodeBeforeUnmount)) {
        invokeVNodeHook(vnodeHook, parentComponent, vnode);
      }
      if (shapeFlag & 6) {
        unmountComponent(vnode.component, parentSuspense, doRemove);
      } else {
        if (shapeFlag & 128) {
          vnode.suspense.unmount(parentSuspense, doRemove);
          return;
        }
        if (shouldInvokeDirs) {
          invokeDirectiveHook(vnode, null, parentComponent, "beforeUnmount");
        }
        if (shapeFlag & 64) {
          vnode.type.remove(
            vnode,
            parentComponent,
            parentSuspense,
            internals,
            doRemove
          );
        } else if (dynamicChildren && !dynamicChildren.hasOnce && (type !== Fragment || patchFlag > 0 && patchFlag & 64)) {
          unmountChildren(
            dynamicChildren,
            parentComponent,
            parentSuspense,
            false,
            true
          );
        } else if (type === Fragment && patchFlag & (128 | 256) || !optimized && shapeFlag & 16) {
          unmountChildren(children, parentComponent, parentSuspense);
        }
        if (doRemove) {
          remove2(vnode);
        }
      }
      if (shouldInvokeVnodeHook && (vnodeHook = props && props.onVnodeUnmounted) || shouldInvokeDirs) {
        queuePostRenderEffect(() => {
          vnodeHook && invokeVNodeHook(vnodeHook, parentComponent, vnode);
          shouldInvokeDirs && invokeDirectiveHook(vnode, null, parentComponent, "unmounted");
        }, parentSuspense);
      }
    };
    const remove2 = (vnode) => {
      const { type, el, anchor, transition } = vnode;
      if (type === Fragment) {
        if (vnode.patchFlag > 0 && vnode.patchFlag & 2048 && transition && !transition.persisted) {
          vnode.children.forEach((child) => {
            if (child.type === Comment) {
              hostRemove(child.el);
            } else {
              remove2(child);
            }
          });
        } else {
          removeFragment(el, anchor);
        }
        return;
      }
      if (type === Static) {
        removeStaticNode(vnode);
        return;
      }
      const performRemove = () => {
        hostRemove(el);
        if (transition && !transition.persisted && transition.afterLeave) {
          transition.afterLeave();
        }
      };
      if (vnode.shapeFlag & 1 && transition && !transition.persisted) {
        const { leave, delayLeave } = transition;
        const performLeave = () => leave(el, performRemove);
        if (delayLeave) {
          delayLeave(vnode.el, performRemove, performLeave);
        } else {
          performLeave();
        }
      } else {
        performRemove();
      }
    };
    const removeFragment = (cur, end) => {
      let next;
      while (cur !== end) {
        next = hostNextSibling(cur);
        hostRemove(cur);
        cur = next;
      }
      hostRemove(end);
    };
    const unmountComponent = (instance, parentSuspense, doRemove) => {
      if (instance.type.__hmrId) {
        unregisterHMR(instance);
      }
      const { bum, scope, job, subTree, um, m, a } = instance;
      invalidateMount(m);
      invalidateMount(a);
      if (bum) {
        invokeArrayFns(bum);
      }
      scope.stop();
      if (job) {
        job.flags |= 8;
        unmount(subTree, instance, parentSuspense, doRemove);
      }
      if (um) {
        queuePostRenderEffect(um, parentSuspense);
      }
      queuePostRenderEffect(() => {
        instance.isUnmounted = true;
      }, parentSuspense);
      if (true) {
        devtoolsComponentRemoved(instance);
      }
    };
    const unmountChildren = (children, parentComponent, parentSuspense, doRemove = false, optimized = false, start = 0) => {
      for (let i = start; i < children.length; i++) {
        unmount(children[i], parentComponent, parentSuspense, doRemove, optimized);
      }
    };
    const getNextHostNode = (vnode) => {
      if (vnode.shapeFlag & 6) {
        return getNextHostNode(vnode.component.subTree);
      }
      if (vnode.shapeFlag & 128) {
        return vnode.suspense.next();
      }
      const el = hostNextSibling(vnode.anchor || vnode.el);
      const teleportEnd = el && el[TeleportEndKey];
      return teleportEnd ? hostNextSibling(teleportEnd) : el;
    };
    let isFlushing = false;
    const render23 = (vnode, container, namespace) => {
      let instance;
      if (vnode == null) {
        if (container._vnode) {
          unmount(container._vnode, null, null, true);
          instance = container._vnode.component;
        }
      } else {
        patch(
          container._vnode || null,
          vnode,
          container,
          null,
          null,
          null,
          namespace
        );
      }
      container._vnode = vnode;
      if (!isFlushing) {
        isFlushing = true;
        flushPreFlushCbs(instance);
        flushPostFlushCbs();
        isFlushing = false;
      }
    };
    const internals = {
      p: patch,
      um: unmount,
      m: move,
      r: remove2,
      mt: mountComponent,
      mc: mountChildren,
      pc: patchChildren,
      pbc: patchBlockChildren,
      n: getNextHostNode,
      o: options
    };
    let hydrate;
    let hydrateNode;
    if (createHydrationFns) {
      [hydrate, hydrateNode] = createHydrationFns(
        internals
      );
    }
    return {
      render: render23,
      hydrate,
      createApp: createAppAPI(render23, hydrate)
    };
  }
  function resolveChildrenNamespace({ type, props }, currentNamespace) {
    return currentNamespace === "svg" && type === "foreignObject" || currentNamespace === "mathml" && type === "annotation-xml" && props && props.encoding && props.encoding.includes("html") ? void 0 : currentNamespace;
  }
  function toggleRecurse({ effect: effect2, job }, allowed) {
    if (allowed) {
      effect2.flags |= 32;
      job.flags |= 4;
    } else {
      effect2.flags &= -33;
      job.flags &= -5;
    }
  }
  function needTransition(parentSuspense, transition) {
    return (!parentSuspense || parentSuspense && !parentSuspense.pendingBranch) && transition && !transition.persisted;
  }
  function traverseStaticChildren(n1, n2, shallow = false) {
    const ch1 = n1.children;
    const ch2 = n2.children;
    if (isArray(ch1) && isArray(ch2)) {
      for (let i = 0; i < ch1.length; i++) {
        const c1 = ch1[i];
        let c2 = ch2[i];
        if (c2.shapeFlag & 1 && !c2.dynamicChildren) {
          if (c2.patchFlag <= 0 || c2.patchFlag === 32) {
            c2 = ch2[i] = cloneIfMounted(ch2[i]);
            c2.el = c1.el;
          }
          if (!shallow && c2.patchFlag !== -2)
            traverseStaticChildren(c1, c2);
        }
        if (c2.type === Text) {
          if (c2.patchFlag === -1) {
            c2 = ch2[i] = cloneIfMounted(c2);
          }
          c2.el = c1.el;
        }
        if (c2.type === Comment && !c2.el) {
          c2.el = c1.el;
        }
        if (true) {
          c2.el && (c2.el.__vnode = c2);
        }
      }
    }
  }
  function getSequence(arr) {
    const p2 = arr.slice();
    const result = [0];
    let i, j, u, v, c;
    const len = arr.length;
    for (i = 0; i < len; i++) {
      const arrI = arr[i];
      if (arrI !== 0) {
        j = result[result.length - 1];
        if (arr[j] < arrI) {
          p2[i] = j;
          result.push(i);
          continue;
        }
        u = 0;
        v = result.length - 1;
        while (u < v) {
          c = u + v >> 1;
          if (arr[result[c]] < arrI) {
            u = c + 1;
          } else {
            v = c;
          }
        }
        if (arrI < arr[result[u]]) {
          if (u > 0) {
            p2[i] = result[u - 1];
          }
          result[u] = i;
        }
      }
    }
    u = result.length;
    v = result[u - 1];
    while (u-- > 0) {
      result[u] = v;
      v = p2[v];
    }
    return result;
  }
  function locateNonHydratedAsyncRoot(instance) {
    const subComponent = instance.subTree.component;
    if (subComponent) {
      if (subComponent.asyncDep && !subComponent.asyncResolved) {
        return subComponent;
      } else {
        return locateNonHydratedAsyncRoot(subComponent);
      }
    }
  }
  function invalidateMount(hooks) {
    if (hooks) {
      for (let i = 0; i < hooks.length; i++)
        hooks[i].flags |= 8;
    }
  }
  function resolveAsyncComponentPlaceholder(anchorVnode) {
    if (anchorVnode.placeholder) {
      return anchorVnode.placeholder;
    }
    const instance = anchorVnode.component;
    if (instance) {
      return resolveAsyncComponentPlaceholder(instance.subTree);
    }
    return null;
  }
  function queueEffectWithSuspense(fn, suspense) {
    if (suspense && suspense.pendingBranch) {
      if (isArray(fn)) {
        suspense.effects.push(...fn);
      } else {
        suspense.effects.push(fn);
      }
    } else {
      queuePostFlushCb(fn);
    }
  }
  function openBlock(disableTracking = false) {
    blockStack.push(currentBlock = disableTracking ? null : []);
  }
  function closeBlock() {
    blockStack.pop();
    currentBlock = blockStack[blockStack.length - 1] || null;
  }
  function setBlockTracking(value, inVOnce = false) {
    isBlockTreeEnabled += value;
    if (value < 0 && currentBlock && inVOnce) {
      currentBlock.hasOnce = true;
    }
  }
  function setupBlock(vnode) {
    vnode.dynamicChildren = isBlockTreeEnabled > 0 ? currentBlock || EMPTY_ARR : null;
    closeBlock();
    if (isBlockTreeEnabled > 0 && currentBlock) {
      currentBlock.push(vnode);
    }
    return vnode;
  }
  function createElementBlock(type, props, children, patchFlag, dynamicProps, shapeFlag) {
    return setupBlock(
      createBaseVNode(
        type,
        props,
        children,
        patchFlag,
        dynamicProps,
        shapeFlag,
        true
      )
    );
  }
  function createBlock(type, props, children, patchFlag, dynamicProps) {
    return setupBlock(
      createVNode(
        type,
        props,
        children,
        patchFlag,
        dynamicProps,
        true
      )
    );
  }
  function isVNode(value) {
    return value ? value.__v_isVNode === true : false;
  }
  function isSameVNodeType(n1, n2) {
    if (n2.shapeFlag & 6 && n1.component) {
      const dirtyInstances = hmrDirtyComponents.get(n2.type);
      if (dirtyInstances && dirtyInstances.has(n1.component)) {
        n1.shapeFlag &= -257;
        n2.shapeFlag &= -513;
        return false;
      }
    }
    return n1.type === n2.type && n1.key === n2.key;
  }
  function createBaseVNode(type, props = null, children = null, patchFlag = 0, dynamicProps = null, shapeFlag = type === Fragment ? 0 : 1, isBlockNode = false, needFullChildrenNormalization = false) {
    const vnode = {
      __v_isVNode: true,
      __v_skip: true,
      type,
      props,
      key: props && normalizeKey(props),
      ref: props && normalizeRef(props),
      scopeId: currentScopeId,
      slotScopeIds: null,
      children,
      component: null,
      suspense: null,
      ssContent: null,
      ssFallback: null,
      dirs: null,
      transition: null,
      el: null,
      anchor: null,
      target: null,
      targetStart: null,
      targetAnchor: null,
      staticCount: 0,
      shapeFlag,
      patchFlag,
      dynamicProps,
      dynamicChildren: null,
      appContext: null,
      ctx: currentRenderingInstance
    };
    if (needFullChildrenNormalization) {
      normalizeChildren(vnode, children);
      if (shapeFlag & 128) {
        type.normalize(vnode);
      }
    } else if (children) {
      vnode.shapeFlag |= isString(children) ? 8 : 16;
    }
    if (vnode.key !== vnode.key) {
      warn$1(`VNode created with invalid key (NaN). VNode type:`, vnode.type);
    }
    if (isBlockTreeEnabled > 0 && !isBlockNode && currentBlock && (vnode.patchFlag > 0 || shapeFlag & 6) && vnode.patchFlag !== 32) {
      currentBlock.push(vnode);
    }
    return vnode;
  }
  function _createVNode(type, props = null, children = null, patchFlag = 0, dynamicProps = null, isBlockNode = false) {
    if (!type || type === NULL_DYNAMIC_COMPONENT) {
      if (!type) {
        warn$1(`Invalid vnode type when creating vnode: ${type}.`);
      }
      type = Comment;
    }
    if (isVNode(type)) {
      const cloned = cloneVNode(
        type,
        props,
        true
      );
      if (children) {
        normalizeChildren(cloned, children);
      }
      if (isBlockTreeEnabled > 0 && !isBlockNode && currentBlock) {
        if (cloned.shapeFlag & 6) {
          currentBlock[currentBlock.indexOf(type)] = cloned;
        } else {
          currentBlock.push(cloned);
        }
      }
      cloned.patchFlag = -2;
      return cloned;
    }
    if (isClassComponent(type)) {
      type = type.__vccOpts;
    }
    if (props) {
      props = guardReactiveProps(props);
      let { class: klass, style } = props;
      if (klass && !isString(klass)) {
        props.class = normalizeClass(klass);
      }
      if (isObject(style)) {
        if (isProxy(style) && !isArray(style)) {
          style = extend({}, style);
        }
        props.style = normalizeStyle(style);
      }
    }
    const shapeFlag = isString(type) ? 1 : isSuspense(type) ? 128 : isTeleport(type) ? 64 : isObject(type) ? 4 : isFunction(type) ? 2 : 0;
    if (shapeFlag & 4 && isProxy(type)) {
      type = toRaw(type);
      warn$1(
        `Vue received a Component that was made a reactive object. This can lead to unnecessary performance overhead and should be avoided by marking the component with \`markRaw\` or using \`shallowRef\` instead of \`ref\`.`,
        `
Component that was made reactive: `,
        type
      );
    }
    return createBaseVNode(
      type,
      props,
      children,
      patchFlag,
      dynamicProps,
      shapeFlag,
      isBlockNode,
      true
    );
  }
  function guardReactiveProps(props) {
    if (!props)
      return null;
    return isProxy(props) || isInternalObject(props) ? extend({}, props) : props;
  }
  function cloneVNode(vnode, extraProps, mergeRef = false, cloneTransition = false) {
    const { props, ref: ref2, patchFlag, children, transition } = vnode;
    const mergedProps = extraProps ? mergeProps(props || {}, extraProps) : props;
    const cloned = {
      __v_isVNode: true,
      __v_skip: true,
      type: vnode.type,
      props: mergedProps,
      key: mergedProps && normalizeKey(mergedProps),
      ref: extraProps && extraProps.ref ? mergeRef && ref2 ? isArray(ref2) ? ref2.concat(normalizeRef(extraProps)) : [ref2, normalizeRef(extraProps)] : normalizeRef(extraProps) : ref2,
      scopeId: vnode.scopeId,
      slotScopeIds: vnode.slotScopeIds,
      children: patchFlag === -1 && isArray(children) ? children.map(deepCloneVNode) : children,
      target: vnode.target,
      targetStart: vnode.targetStart,
      targetAnchor: vnode.targetAnchor,
      staticCount: vnode.staticCount,
      shapeFlag: vnode.shapeFlag,
      patchFlag: extraProps && vnode.type !== Fragment ? patchFlag === -1 ? 16 : patchFlag | 16 : patchFlag,
      dynamicProps: vnode.dynamicProps,
      dynamicChildren: vnode.dynamicChildren,
      appContext: vnode.appContext,
      dirs: vnode.dirs,
      transition,
      component: vnode.component,
      suspense: vnode.suspense,
      ssContent: vnode.ssContent && cloneVNode(vnode.ssContent),
      ssFallback: vnode.ssFallback && cloneVNode(vnode.ssFallback),
      placeholder: vnode.placeholder,
      el: vnode.el,
      anchor: vnode.anchor,
      ctx: vnode.ctx,
      ce: vnode.ce
    };
    if (transition && cloneTransition) {
      setTransitionHooks(
        cloned,
        transition.clone(cloned)
      );
    }
    return cloned;
  }
  function deepCloneVNode(vnode) {
    const cloned = cloneVNode(vnode);
    if (isArray(vnode.children)) {
      cloned.children = vnode.children.map(deepCloneVNode);
    }
    return cloned;
  }
  function createTextVNode(text = " ", flag = 0) {
    return createVNode(Text, null, text, flag);
  }
  function createCommentVNode(text = "", asBlock = false) {
    return asBlock ? (openBlock(), createBlock(Comment, null, text)) : createVNode(Comment, null, text);
  }
  function normalizeVNode(child) {
    if (child == null || typeof child === "boolean") {
      return createVNode(Comment);
    } else if (isArray(child)) {
      return createVNode(
        Fragment,
        null,
        child.slice()
      );
    } else if (isVNode(child)) {
      return cloneIfMounted(child);
    } else {
      return createVNode(Text, null, String(child));
    }
  }
  function cloneIfMounted(child) {
    return child.el === null && child.patchFlag !== -1 || child.memo ? child : cloneVNode(child);
  }
  function normalizeChildren(vnode, children) {
    let type = 0;
    const { shapeFlag } = vnode;
    if (children == null) {
      children = null;
    } else if (isArray(children)) {
      type = 16;
    } else if (typeof children === "object") {
      if (shapeFlag & (1 | 64)) {
        const slot = children.default;
        if (slot) {
          slot._c && (slot._d = false);
          normalizeChildren(vnode, slot());
          slot._c && (slot._d = true);
        }
        return;
      } else {
        type = 32;
        const slotFlag = children._;
        if (!slotFlag && !isInternalObject(children)) {
          children._ctx = currentRenderingInstance;
        } else if (slotFlag === 3 && currentRenderingInstance) {
          if (currentRenderingInstance.slots._ === 1) {
            children._ = 1;
          } else {
            children._ = 2;
            vnode.patchFlag |= 1024;
          }
        }
      }
    } else if (isFunction(children)) {
      children = { default: children, _ctx: currentRenderingInstance };
      type = 32;
    } else {
      children = String(children);
      if (shapeFlag & 64) {
        type = 16;
        children = [createTextVNode(children)];
      } else {
        type = 8;
      }
    }
    vnode.children = children;
    vnode.shapeFlag |= type;
  }
  function mergeProps(...args) {
    const ret = {};
    for (let i = 0; i < args.length; i++) {
      const toMerge = args[i];
      for (const key in toMerge) {
        if (key === "class") {
          if (ret.class !== toMerge.class) {
            ret.class = normalizeClass([ret.class, toMerge.class]);
          }
        } else if (key === "style") {
          ret.style = normalizeStyle([ret.style, toMerge.style]);
        } else if (isOn(key)) {
          const existing = ret[key];
          const incoming = toMerge[key];
          if (incoming && existing !== incoming && !(isArray(existing) && existing.includes(incoming))) {
            ret[key] = existing ? [].concat(existing, incoming) : incoming;
          }
        } else if (key !== "") {
          ret[key] = toMerge[key];
        }
      }
    }
    return ret;
  }
  function invokeVNodeHook(hook, instance, vnode, prevVNode = null) {
    callWithAsyncErrorHandling(hook, instance, 7, [
      vnode,
      prevVNode
    ]);
  }
  function createComponentInstance(vnode, parent, suspense) {
    const type = vnode.type;
    const appContext = (parent ? parent.appContext : vnode.appContext) || emptyAppContext;
    const instance = {
      uid: uid++,
      vnode,
      type,
      parent,
      appContext,
      root: null,
      next: null,
      subTree: null,
      effect: null,
      update: null,
      job: null,
      scope: new EffectScope(
        true
      ),
      render: null,
      proxy: null,
      exposed: null,
      exposeProxy: null,
      withProxy: null,
      provides: parent ? parent.provides : Object.create(appContext.provides),
      ids: parent ? parent.ids : ["", 0, 0],
      accessCache: null,
      renderCache: [],
      components: null,
      directives: null,
      propsOptions: normalizePropsOptions(type, appContext),
      emitsOptions: normalizeEmitsOptions(type, appContext),
      emit: null,
      emitted: null,
      propsDefaults: EMPTY_OBJ,
      inheritAttrs: type.inheritAttrs,
      ctx: EMPTY_OBJ,
      data: EMPTY_OBJ,
      props: EMPTY_OBJ,
      attrs: EMPTY_OBJ,
      slots: EMPTY_OBJ,
      refs: EMPTY_OBJ,
      setupState: EMPTY_OBJ,
      setupContext: null,
      suspense,
      suspenseId: suspense ? suspense.pendingId : 0,
      asyncDep: null,
      asyncResolved: false,
      isMounted: false,
      isUnmounted: false,
      isDeactivated: false,
      bc: null,
      c: null,
      bm: null,
      m: null,
      bu: null,
      u: null,
      um: null,
      bum: null,
      da: null,
      a: null,
      rtg: null,
      rtc: null,
      ec: null,
      sp: null
    };
    if (true) {
      instance.ctx = createDevRenderContext(instance);
    } else {
      instance.ctx = { _: instance };
    }
    instance.root = parent ? parent.root : instance;
    instance.emit = emit.bind(null, instance);
    if (vnode.ce) {
      vnode.ce(instance);
    }
    return instance;
  }
  function validateComponentName(name, { isNativeTag }) {
    if (isBuiltInTag(name) || isNativeTag(name)) {
      warn$1(
        "Do not use built-in or reserved HTML elements as component id: " + name
      );
    }
  }
  function isStatefulComponent(instance) {
    return instance.vnode.shapeFlag & 4;
  }
  function setupComponent(instance, isSSR = false, optimized = false) {
    isSSR && setInSSRSetupState(isSSR);
    const { props, children } = instance.vnode;
    const isStateful = isStatefulComponent(instance);
    initProps(instance, props, isStateful, isSSR);
    initSlots(instance, children, optimized || isSSR);
    const setupResult = isStateful ? setupStatefulComponent(instance, isSSR) : void 0;
    isSSR && setInSSRSetupState(false);
    return setupResult;
  }
  function setupStatefulComponent(instance, isSSR) {
    const Component = instance.type;
    if (true) {
      if (Component.name) {
        validateComponentName(Component.name, instance.appContext.config);
      }
      if (Component.components) {
        const names = Object.keys(Component.components);
        for (let i = 0; i < names.length; i++) {
          validateComponentName(names[i], instance.appContext.config);
        }
      }
      if (Component.directives) {
        const names = Object.keys(Component.directives);
        for (let i = 0; i < names.length; i++) {
          validateDirectiveName(names[i]);
        }
      }
      if (Component.compilerOptions && isRuntimeOnly()) {
        warn$1(
          `"compilerOptions" is only supported when using a build of Vue that includes the runtime compiler. Since you are using a runtime-only build, the options should be passed via your build tool config instead.`
        );
      }
    }
    instance.accessCache = /* @__PURE__ */ Object.create(null);
    instance.proxy = new Proxy(instance.ctx, PublicInstanceProxyHandlers);
    if (true) {
      exposePropsOnRenderContext(instance);
    }
    const { setup } = Component;
    if (setup) {
      pauseTracking();
      const setupContext = instance.setupContext = setup.length > 1 ? createSetupContext(instance) : null;
      const reset = setCurrentInstance(instance);
      const setupResult = callWithErrorHandling(
        setup,
        instance,
        0,
        [
          true ? shallowReadonly(instance.props) : instance.props,
          setupContext
        ]
      );
      const isAsyncSetup = isPromise(setupResult);
      resetTracking();
      reset();
      if ((isAsyncSetup || instance.sp) && !isAsyncWrapper(instance)) {
        markAsyncBoundary(instance);
      }
      if (isAsyncSetup) {
        setupResult.then(unsetCurrentInstance, unsetCurrentInstance);
        if (isSSR) {
          return setupResult.then((resolvedResult) => {
            handleSetupResult(instance, resolvedResult, isSSR);
          }).catch((e) => {
            handleError(e, instance, 0);
          });
        } else {
          instance.asyncDep = setupResult;
          if (!instance.suspense) {
            const name = formatComponentName(instance, Component);
            warn$1(
              `Component <${name}>: setup function returned a promise, but no <Suspense> boundary was found in the parent component tree. A component with async setup() must be nested in a <Suspense> in order to be rendered.`
            );
          }
        }
      } else {
        handleSetupResult(instance, setupResult, isSSR);
      }
    } else {
      finishComponentSetup(instance, isSSR);
    }
  }
  function handleSetupResult(instance, setupResult, isSSR) {
    if (isFunction(setupResult)) {
      if (instance.type.__ssrInlineRender) {
        instance.ssrRender = setupResult;
      } else {
        instance.render = setupResult;
      }
    } else if (isObject(setupResult)) {
      if (isVNode(setupResult)) {
        warn$1(
          `setup() should not return VNodes directly - return a render function instead.`
        );
      }
      if (true) {
        instance.devtoolsRawSetupState = setupResult;
      }
      instance.setupState = proxyRefs(setupResult);
      if (true) {
        exposeSetupStateOnRenderContext(instance);
      }
    } else if (setupResult !== void 0) {
      warn$1(
        `setup() should return an object. Received: ${setupResult === null ? "null" : typeof setupResult}`
      );
    }
    finishComponentSetup(instance, isSSR);
  }
  function finishComponentSetup(instance, isSSR, skipOptions) {
    const Component = instance.type;
    if (!instance.render) {
      if (!isSSR && compile && !Component.render) {
        const template = Component.template || resolveMergedOptions(instance).template;
        if (template) {
          if (true) {
            startMeasure(instance, `compile`);
          }
          const { isCustomElement, compilerOptions } = instance.appContext.config;
          const { delimiters, compilerOptions: componentCompilerOptions } = Component;
          const finalCompilerOptions = extend(
            extend(
              {
                isCustomElement,
                delimiters
              },
              compilerOptions
            ),
            componentCompilerOptions
          );
          Component.render = compile(template, finalCompilerOptions);
          if (true) {
            endMeasure(instance, `compile`);
          }
        }
      }
      instance.render = Component.render || NOOP;
      if (installWithProxy) {
        installWithProxy(instance);
      }
    }
    if (true) {
      const reset = setCurrentInstance(instance);
      pauseTracking();
      try {
        applyOptions(instance);
      } finally {
        resetTracking();
        reset();
      }
    }
    if (!Component.render && instance.render === NOOP && !isSSR) {
      if (!compile && Component.template) {
        warn$1(
          `Component provided template option but runtime compilation is not supported in this build of Vue. Configure your bundler to alias "vue" to "vue/dist/vue.esm-bundler.js".`
        );
      } else {
        warn$1(`Component is missing template or render function: `, Component);
      }
    }
  }
  function getSlotsProxy(instance) {
    return new Proxy(instance.slots, {
      get(target, key) {
        track(instance, "get", "$slots");
        return target[key];
      }
    });
  }
  function createSetupContext(instance) {
    const expose = (exposed) => {
      if (true) {
        if (instance.exposed) {
          warn$1(`expose() should be called only once per setup().`);
        }
        if (exposed != null) {
          let exposedType = typeof exposed;
          if (exposedType === "object") {
            if (isArray(exposed)) {
              exposedType = "array";
            } else if (isRef2(exposed)) {
              exposedType = "ref";
            }
          }
          if (exposedType !== "object") {
            warn$1(
              `expose() should be passed a plain object, received ${exposedType}.`
            );
          }
        }
      }
      instance.exposed = exposed || {};
    };
    if (true) {
      let attrsProxy;
      let slotsProxy;
      return Object.freeze({
        get attrs() {
          return attrsProxy || (attrsProxy = new Proxy(instance.attrs, attrsProxyHandlers));
        },
        get slots() {
          return slotsProxy || (slotsProxy = getSlotsProxy(instance));
        },
        get emit() {
          return (event, ...args) => instance.emit(event, ...args);
        },
        expose
      });
    } else {
      return {
        attrs: new Proxy(instance.attrs, attrsProxyHandlers),
        slots: instance.slots,
        emit: instance.emit,
        expose
      };
    }
  }
  function getComponentPublicInstance(instance) {
    if (instance.exposed) {
      return instance.exposeProxy || (instance.exposeProxy = new Proxy(proxyRefs(markRaw(instance.exposed)), {
        get(target, key) {
          if (key in target) {
            return target[key];
          } else if (key in publicPropertiesMap) {
            return publicPropertiesMap[key](instance);
          }
        },
        has(target, key) {
          return key in target || key in publicPropertiesMap;
        }
      }));
    } else {
      return instance.proxy;
    }
  }
  function getComponentName(Component, includeInferred = true) {
    return isFunction(Component) ? Component.displayName || Component.name : Component.name || includeInferred && Component.__name;
  }
  function formatComponentName(instance, Component, isRoot = false) {
    let name = getComponentName(Component);
    if (!name && Component.__file) {
      const match = Component.__file.match(/([^/\\]+)\.\w+$/);
      if (match) {
        name = match[1];
      }
    }
    if (!name && instance) {
      const inferFromRegistry = (registry) => {
        for (const key in registry) {
          if (registry[key] === Component) {
            return key;
          }
        }
      };
      name = inferFromRegistry(instance.components) || instance.parent && inferFromRegistry(
        instance.parent.type.components
      ) || inferFromRegistry(instance.appContext.components);
    }
    return name ? classify(name) : isRoot ? `App` : `Anonymous`;
  }
  function isClassComponent(value) {
    return isFunction(value) && "__vccOpts" in value;
  }
  function initCustomFormatter() {
    if (typeof window === "undefined") {
      return;
    }
    const vueStyle = { style: "color:#3ba776" };
    const numberStyle = { style: "color:#1677ff" };
    const stringStyle = { style: "color:#f5222d" };
    const keywordStyle = { style: "color:#eb2f96" };
    const formatter = {
      __vue_custom_formatter: true,
      header(obj) {
        if (!isObject(obj)) {
          return null;
        }
        if (obj.__isVue) {
          return ["div", vueStyle, `VueInstance`];
        } else if (isRef2(obj)) {
          pauseTracking();
          const value = obj.value;
          resetTracking();
          return [
            "div",
            {},
            ["span", vueStyle, genRefFlag(obj)],
            "<",
            formatValue(value),
            `>`
          ];
        } else if (isReactive(obj)) {
          return [
            "div",
            {},
            ["span", vueStyle, isShallow(obj) ? "ShallowReactive" : "Reactive"],
            "<",
            formatValue(obj),
            `>${isReadonly(obj) ? ` (readonly)` : ``}`
          ];
        } else if (isReadonly(obj)) {
          return [
            "div",
            {},
            ["span", vueStyle, isShallow(obj) ? "ShallowReadonly" : "Readonly"],
            "<",
            formatValue(obj),
            ">"
          ];
        }
        return null;
      },
      hasBody(obj) {
        return obj && obj.__isVue;
      },
      body(obj) {
        if (obj && obj.__isVue) {
          return [
            "div",
            {},
            ...formatInstance(obj.$)
          ];
        }
      }
    };
    function formatInstance(instance) {
      const blocks = [];
      if (instance.type.props && instance.props) {
        blocks.push(createInstanceBlock("props", toRaw(instance.props)));
      }
      if (instance.setupState !== EMPTY_OBJ) {
        blocks.push(createInstanceBlock("setup", instance.setupState));
      }
      if (instance.data !== EMPTY_OBJ) {
        blocks.push(createInstanceBlock("data", toRaw(instance.data)));
      }
      const computed3 = extractKeys(instance, "computed");
      if (computed3) {
        blocks.push(createInstanceBlock("computed", computed3));
      }
      const injected = extractKeys(instance, "inject");
      if (injected) {
        blocks.push(createInstanceBlock("injected", injected));
      }
      blocks.push([
        "div",
        {},
        [
          "span",
          {
            style: keywordStyle.style + ";opacity:0.66"
          },
          "$ (internal): "
        ],
        ["object", { object: instance }]
      ]);
      return blocks;
    }
    function createInstanceBlock(type, target) {
      target = extend({}, target);
      if (!Object.keys(target).length) {
        return ["span", {}];
      }
      return [
        "div",
        { style: "line-height:1.25em;margin-bottom:0.6em" },
        [
          "div",
          {
            style: "color:#476582"
          },
          type
        ],
        [
          "div",
          {
            style: "padding-left:1.25em"
          },
          ...Object.keys(target).map((key) => {
            return [
              "div",
              {},
              ["span", keywordStyle, key + ": "],
              formatValue(target[key], false)
            ];
          })
        ]
      ];
    }
    function formatValue(v, asRaw = true) {
      if (typeof v === "number") {
        return ["span", numberStyle, v];
      } else if (typeof v === "string") {
        return ["span", stringStyle, JSON.stringify(v)];
      } else if (typeof v === "boolean") {
        return ["span", keywordStyle, v];
      } else if (isObject(v)) {
        return ["object", { object: asRaw ? toRaw(v) : v }];
      } else {
        return ["span", stringStyle, String(v)];
      }
    }
    function extractKeys(instance, type) {
      const Comp = instance.type;
      if (isFunction(Comp)) {
        return;
      }
      const extracted = {};
      for (const key in instance.ctx) {
        if (isKeyOfType(Comp, key, type)) {
          extracted[key] = instance.ctx[key];
        }
      }
      return extracted;
    }
    function isKeyOfType(Comp, key, type) {
      const opts = Comp[type];
      if (isArray(opts) && opts.includes(key) || isObject(opts) && key in opts) {
        return true;
      }
      if (Comp.extends && isKeyOfType(Comp.extends, key, type)) {
        return true;
      }
      if (Comp.mixins && Comp.mixins.some((m) => isKeyOfType(m, key, type))) {
        return true;
      }
    }
    function genRefFlag(v) {
      if (isShallow(v)) {
        return `ShallowRef`;
      }
      if (v.effect) {
        return `ComputedRef`;
      }
      return `Ref`;
    }
    if (window.devtoolsFormatters) {
      window.devtoolsFormatters.push(formatter);
    } else {
      window.devtoolsFormatters = [formatter];
    }
  }
  var stack, isWarning, ErrorTypeStrings$1, queue, flushIndex, pendingPostFlushCbs, activePostFlushCbs, postFlushIndex, resolvedPromise, currentFlushPromise, RECURSION_LIMIT, getId, isHmrUpdating, hmrDirtyComponents, map, devtools$1, buffer, devtoolsNotInstalled, devtoolsComponentAdded, devtoolsComponentUpdated, _devtoolsComponentRemoved, devtoolsComponentRemoved, devtoolsPerfStart, devtoolsPerfEnd, currentRenderingInstance, currentScopeId, ssrContextKey, useSSRContext, TeleportEndKey, isTeleport, leaveCbKey, knownTemplateRefs, pendingSetRefMap, requestIdleCallback, cancelIdleCallback, isAsyncWrapper, isKeepAlive, createHook, onBeforeMount, onMounted, onBeforeUpdate, onUpdated, onBeforeUnmount, onUnmounted, onServerPrefetch, onRenderTriggered, onRenderTracked, NULL_DYNAMIC_COMPONENT, getPublicInstance, publicPropertiesMap, isReservedPrefix, hasSetupBinding, PublicInstanceProxyHandlers, shouldCacheAccess, internalOptionMergeStrats, uid$1, currentApp, getModelModifiers, mixinEmitsCache, accessedAttrs, getChildRoot, getFunctionalFallthrough, filterModelListeners, isElementRoot, internalObjectProto, createInternalObject, isInternalObject, mixinPropsCache, isSimpleType, isInternalKey, normalizeSlotValue, normalizeSlot, normalizeObjectSlots, normalizeVNodeSlots, assignSlots, initSlots, updateSlots, supported, perf, queuePostRenderEffect, isSuspense, Fragment, Text, Comment, Static, blockStack, currentBlock, isBlockTreeEnabled, vnodeArgsTransformer, createVNodeWithArgsTransform, normalizeKey, normalizeRef, createVNode, emptyAppContext, uid, currentInstance, getCurrentInstance, internalSetCurrentInstance, setInSSRSetupState, setCurrentInstance, unsetCurrentInstance, isBuiltInTag, isInSSRComponentSetup, compile, installWithProxy, isRuntimeOnly, attrsProxyHandlers, classifyRE, classify, computed2, version, warn2;
  var init_runtime_core_esm_bundler = __esm({
    "../node_modules/@vue/runtime-core/dist/runtime-core.esm-bundler.js"() {
      init_reactivity_esm_bundler();
      init_reactivity_esm_bundler();
      init_shared_esm_bundler();
      init_shared_esm_bundler();
      stack = [];
      isWarning = false;
      ErrorTypeStrings$1 = {
        ["sp"]: "serverPrefetch hook",
        ["bc"]: "beforeCreate hook",
        ["c"]: "created hook",
        ["bm"]: "beforeMount hook",
        ["m"]: "mounted hook",
        ["bu"]: "beforeUpdate hook",
        ["u"]: "updated",
        ["bum"]: "beforeUnmount hook",
        ["um"]: "unmounted hook",
        ["a"]: "activated hook",
        ["da"]: "deactivated hook",
        ["ec"]: "errorCaptured hook",
        ["rtc"]: "renderTracked hook",
        ["rtg"]: "renderTriggered hook",
        [0]: "setup function",
        [1]: "render function",
        [2]: "watcher getter",
        [3]: "watcher callback",
        [4]: "watcher cleanup function",
        [5]: "native event handler",
        [6]: "component event handler",
        [7]: "vnode hook",
        [8]: "directive hook",
        [9]: "transition hook",
        [10]: "app errorHandler",
        [11]: "app warnHandler",
        [12]: "ref function",
        [13]: "async component loader",
        [14]: "scheduler flush",
        [15]: "component update",
        [16]: "app unmount cleanup function"
      };
      queue = [];
      flushIndex = -1;
      pendingPostFlushCbs = [];
      activePostFlushCbs = null;
      postFlushIndex = 0;
      resolvedPromise = /* @__PURE__ */ Promise.resolve();
      currentFlushPromise = null;
      RECURSION_LIMIT = 100;
      getId = (job) => job.id == null ? job.flags & 2 ? -1 : Infinity : job.id;
      isHmrUpdating = false;
      hmrDirtyComponents = /* @__PURE__ */ new Map();
      if (true) {
        getGlobalThis().__VUE_HMR_RUNTIME__ = {
          createRecord: tryWrap(createRecord),
          rerender: tryWrap(rerender),
          reload: tryWrap(reload)
        };
      }
      map = /* @__PURE__ */ new Map();
      buffer = [];
      devtoolsNotInstalled = false;
      devtoolsComponentAdded = /* @__PURE__ */ createDevtoolsComponentHook("component:added");
      devtoolsComponentUpdated = /* @__PURE__ */ createDevtoolsComponentHook("component:updated");
      _devtoolsComponentRemoved = /* @__PURE__ */ createDevtoolsComponentHook(
        "component:removed"
      );
      devtoolsComponentRemoved = (component) => {
        if (devtools$1 && typeof devtools$1.cleanupBuffer === "function" && !devtools$1.cleanupBuffer(component)) {
          _devtoolsComponentRemoved(component);
        }
      };
      devtoolsPerfStart = /* @__PURE__ */ createDevtoolsPerformanceHook("perf:start");
      devtoolsPerfEnd = /* @__PURE__ */ createDevtoolsPerformanceHook("perf:end");
      currentRenderingInstance = null;
      currentScopeId = null;
      ssrContextKey = /* @__PURE__ */ Symbol.for("v-scx");
      useSSRContext = () => {
        {
          const ctx = inject(ssrContextKey);
          if (!ctx) {
            warn$1(
              `Server rendering context not provided. Make sure to only call useSSRContext() conditionally in the server build.`
            );
          }
          return ctx;
        }
      };
      TeleportEndKey = /* @__PURE__ */ Symbol("_vte");
      isTeleport = (type) => type.__isTeleport;
      leaveCbKey = /* @__PURE__ */ Symbol("_leaveCb");
      knownTemplateRefs = /* @__PURE__ */ new WeakSet();
      pendingSetRefMap = /* @__PURE__ */ new WeakMap();
      requestIdleCallback = getGlobalThis().requestIdleCallback || ((cb) => setTimeout(cb, 1));
      cancelIdleCallback = getGlobalThis().cancelIdleCallback || ((id) => clearTimeout(id));
      isAsyncWrapper = (i) => !!i.type.__asyncLoader;
      isKeepAlive = (vnode) => vnode.type.__isKeepAlive;
      createHook = (lifecycle) => (hook, target = currentInstance) => {
        if (!isInSSRComponentSetup || lifecycle === "sp") {
          injectHook(lifecycle, (...args) => hook(...args), target);
        }
      };
      onBeforeMount = createHook("bm");
      onMounted = createHook("m");
      onBeforeUpdate = createHook(
        "bu"
      );
      onUpdated = createHook("u");
      onBeforeUnmount = createHook(
        "bum"
      );
      onUnmounted = createHook("um");
      onServerPrefetch = createHook(
        "sp"
      );
      onRenderTriggered = createHook("rtg");
      onRenderTracked = createHook("rtc");
      NULL_DYNAMIC_COMPONENT = /* @__PURE__ */ Symbol.for("v-ndc");
      getPublicInstance = (i) => {
        if (!i)
          return null;
        if (isStatefulComponent(i))
          return getComponentPublicInstance(i);
        return getPublicInstance(i.parent);
      };
      publicPropertiesMap = /* @__PURE__ */ extend(/* @__PURE__ */ Object.create(null), {
        $: (i) => i,
        $el: (i) => i.vnode.el,
        $data: (i) => i.data,
        $props: (i) => true ? shallowReadonly(i.props) : i.props,
        $attrs: (i) => true ? shallowReadonly(i.attrs) : i.attrs,
        $slots: (i) => true ? shallowReadonly(i.slots) : i.slots,
        $refs: (i) => true ? shallowReadonly(i.refs) : i.refs,
        $parent: (i) => getPublicInstance(i.parent),
        $root: (i) => getPublicInstance(i.root),
        $host: (i) => i.ce,
        $emit: (i) => i.emit,
        $options: (i) => true ? resolveMergedOptions(i) : i.type,
        $forceUpdate: (i) => i.f || (i.f = () => {
          queueJob(i.update);
        }),
        $nextTick: (i) => i.n || (i.n = nextTick.bind(i.proxy)),
        $watch: (i) => true ? instanceWatch.bind(i) : NOOP
      });
      isReservedPrefix = (key) => key === "_" || key === "$";
      hasSetupBinding = (state, key) => state !== EMPTY_OBJ && !state.__isScriptSetup && hasOwn(state, key);
      PublicInstanceProxyHandlers = {
        get({ _: instance }, key) {
          if (key === "__v_skip") {
            return true;
          }
          const { ctx, setupState, data, props, accessCache, type, appContext } = instance;
          if (key === "__isVue") {
            return true;
          }
          if (key[0] !== "$") {
            const n = accessCache[key];
            if (n !== void 0) {
              switch (n) {
                case 1:
                  return setupState[key];
                case 2:
                  return data[key];
                case 4:
                  return ctx[key];
                case 3:
                  return props[key];
              }
            } else if (hasSetupBinding(setupState, key)) {
              accessCache[key] = 1;
              return setupState[key];
            } else if (data !== EMPTY_OBJ && hasOwn(data, key)) {
              accessCache[key] = 2;
              return data[key];
            } else if (hasOwn(props, key)) {
              accessCache[key] = 3;
              return props[key];
            } else if (ctx !== EMPTY_OBJ && hasOwn(ctx, key)) {
              accessCache[key] = 4;
              return ctx[key];
            } else if (shouldCacheAccess) {
              accessCache[key] = 0;
            }
          }
          const publicGetter = publicPropertiesMap[key];
          let cssModule, globalProperties;
          if (publicGetter) {
            if (key === "$attrs") {
              track(instance.attrs, "get", "");
              markAttrsAccessed();
            } else if (key === "$slots") {
              track(instance, "get", key);
            }
            return publicGetter(instance);
          } else if ((cssModule = type.__cssModules) && (cssModule = cssModule[key])) {
            return cssModule;
          } else if (ctx !== EMPTY_OBJ && hasOwn(ctx, key)) {
            accessCache[key] = 4;
            return ctx[key];
          } else if (globalProperties = appContext.config.globalProperties, hasOwn(globalProperties, key)) {
            {
              return globalProperties[key];
            }
          } else if (currentRenderingInstance && (!isString(key) || key.indexOf("__v") !== 0)) {
            if (data !== EMPTY_OBJ && isReservedPrefix(key[0]) && hasOwn(data, key)) {
              warn$1(
                `Property ${JSON.stringify(
                  key
                )} must be accessed via $data because it starts with a reserved character ("$" or "_") and is not proxied on the render context.`
              );
            } else if (instance === currentRenderingInstance) {
              warn$1(
                `Property ${JSON.stringify(key)} was accessed during render but is not defined on instance.`
              );
            }
          }
        },
        set({ _: instance }, key, value) {
          const { data, setupState, ctx } = instance;
          if (hasSetupBinding(setupState, key)) {
            setupState[key] = value;
            return true;
          } else if (setupState.__isScriptSetup && hasOwn(setupState, key)) {
            warn$1(`Cannot mutate <script setup> binding "${key}" from Options API.`);
            return false;
          } else if (data !== EMPTY_OBJ && hasOwn(data, key)) {
            data[key] = value;
            return true;
          } else if (hasOwn(instance.props, key)) {
            warn$1(`Attempting to mutate prop "${key}". Props are readonly.`);
            return false;
          }
          if (key[0] === "$" && key.slice(1) in instance) {
            warn$1(
              `Attempting to mutate public property "${key}". Properties starting with $ are reserved and readonly.`
            );
            return false;
          } else {
            if (key in instance.appContext.config.globalProperties) {
              Object.defineProperty(ctx, key, {
                enumerable: true,
                configurable: true,
                value
              });
            } else {
              ctx[key] = value;
            }
          }
          return true;
        },
        has({
          _: { data, setupState, accessCache, ctx, appContext, props, type }
        }, key) {
          let cssModules;
          return !!(accessCache[key] || data !== EMPTY_OBJ && key[0] !== "$" && hasOwn(data, key) || hasSetupBinding(setupState, key) || hasOwn(props, key) || hasOwn(ctx, key) || hasOwn(publicPropertiesMap, key) || hasOwn(appContext.config.globalProperties, key) || (cssModules = type.__cssModules) && cssModules[key]);
        },
        defineProperty(target, key, descriptor) {
          if (descriptor.get != null) {
            target._.accessCache[key] = 0;
          } else if (hasOwn(descriptor, "value")) {
            this.set(target, key, descriptor.value, null);
          }
          return Reflect.defineProperty(target, key, descriptor);
        }
      };
      if (true) {
        PublicInstanceProxyHandlers.ownKeys = (target) => {
          warn$1(
            `Avoid app logic that relies on enumerating keys on a component instance. The keys will be empty in production mode to avoid performance overhead.`
          );
          return Reflect.ownKeys(target);
        };
      }
      shouldCacheAccess = true;
      internalOptionMergeStrats = {
        data: mergeDataFn,
        props: mergeEmitsOrPropsOptions,
        emits: mergeEmitsOrPropsOptions,
        methods: mergeObjectOptions,
        computed: mergeObjectOptions,
        beforeCreate: mergeAsArray,
        created: mergeAsArray,
        beforeMount: mergeAsArray,
        mounted: mergeAsArray,
        beforeUpdate: mergeAsArray,
        updated: mergeAsArray,
        beforeDestroy: mergeAsArray,
        beforeUnmount: mergeAsArray,
        destroyed: mergeAsArray,
        unmounted: mergeAsArray,
        activated: mergeAsArray,
        deactivated: mergeAsArray,
        errorCaptured: mergeAsArray,
        serverPrefetch: mergeAsArray,
        components: mergeObjectOptions,
        directives: mergeObjectOptions,
        watch: mergeWatchOptions,
        provide: mergeDataFn,
        inject: mergeInject
      };
      uid$1 = 0;
      currentApp = null;
      getModelModifiers = (props, modelName) => {
        return modelName === "modelValue" || modelName === "model-value" ? props.modelModifiers : props[`${modelName}Modifiers`] || props[`${camelize(modelName)}Modifiers`] || props[`${hyphenate(modelName)}Modifiers`];
      };
      mixinEmitsCache = /* @__PURE__ */ new WeakMap();
      accessedAttrs = false;
      getChildRoot = (vnode) => {
        const rawChildren = vnode.children;
        const dynamicChildren = vnode.dynamicChildren;
        const childRoot = filterSingleRoot(rawChildren, false);
        if (!childRoot) {
          return [vnode, void 0];
        } else if (childRoot.patchFlag > 0 && childRoot.patchFlag & 2048) {
          return getChildRoot(childRoot);
        }
        const index = rawChildren.indexOf(childRoot);
        const dynamicIndex = dynamicChildren ? dynamicChildren.indexOf(childRoot) : -1;
        const setRoot = (updatedRoot) => {
          rawChildren[index] = updatedRoot;
          if (dynamicChildren) {
            if (dynamicIndex > -1) {
              dynamicChildren[dynamicIndex] = updatedRoot;
            } else if (updatedRoot.patchFlag > 0) {
              vnode.dynamicChildren = [...dynamicChildren, updatedRoot];
            }
          }
        };
        return [normalizeVNode(childRoot), setRoot];
      };
      getFunctionalFallthrough = (attrs) => {
        let res;
        for (const key in attrs) {
          if (key === "class" || key === "style" || isOn(key)) {
            (res || (res = {}))[key] = attrs[key];
          }
        }
        return res;
      };
      filterModelListeners = (attrs, props) => {
        const res = {};
        for (const key in attrs) {
          if (!isModelListener(key) || !(key.slice(9) in props)) {
            res[key] = attrs[key];
          }
        }
        return res;
      };
      isElementRoot = (vnode) => {
        return vnode.shapeFlag & (6 | 1) || vnode.type === Comment;
      };
      internalObjectProto = {};
      createInternalObject = () => Object.create(internalObjectProto);
      isInternalObject = (obj) => Object.getPrototypeOf(obj) === internalObjectProto;
      mixinPropsCache = /* @__PURE__ */ new WeakMap();
      isSimpleType = /* @__PURE__ */ makeMap(
        "String,Number,Boolean,Function,Symbol,BigInt"
      );
      isInternalKey = (key) => key === "_" || key === "_ctx" || key === "$stable";
      normalizeSlotValue = (value) => isArray(value) ? value.map(normalizeVNode) : [normalizeVNode(value)];
      normalizeSlot = (key, rawSlot, ctx) => {
        if (rawSlot._n) {
          return rawSlot;
        }
        const normalized = withCtx((...args) => {
          if (currentInstance && !(ctx === null && currentRenderingInstance) && !(ctx && ctx.root !== currentInstance.root)) {
            warn$1(
              `Slot "${key}" invoked outside of the render function: this will not track dependencies used in the slot. Invoke the slot function inside the render function instead.`
            );
          }
          return normalizeSlotValue(rawSlot(...args));
        }, ctx);
        normalized._c = false;
        return normalized;
      };
      normalizeObjectSlots = (rawSlots, slots, instance) => {
        const ctx = rawSlots._ctx;
        for (const key in rawSlots) {
          if (isInternalKey(key))
            continue;
          const value = rawSlots[key];
          if (isFunction(value)) {
            slots[key] = normalizeSlot(key, value, ctx);
          } else if (value != null) {
            if (true) {
              warn$1(
                `Non-function value encountered for slot "${key}". Prefer function slots for better performance.`
              );
            }
            const normalized = normalizeSlotValue(value);
            slots[key] = () => normalized;
          }
        }
      };
      normalizeVNodeSlots = (instance, children) => {
        if (!isKeepAlive(instance.vnode) && true) {
          warn$1(
            `Non-function value encountered for default slot. Prefer function slots for better performance.`
          );
        }
        const normalized = normalizeSlotValue(children);
        instance.slots.default = () => normalized;
      };
      assignSlots = (slots, children, optimized) => {
        for (const key in children) {
          if (optimized || !isInternalKey(key)) {
            slots[key] = children[key];
          }
        }
      };
      initSlots = (instance, children, optimized) => {
        const slots = instance.slots = createInternalObject();
        if (instance.vnode.shapeFlag & 32) {
          const type = children._;
          if (type) {
            assignSlots(slots, children, optimized);
            if (optimized) {
              def(slots, "_", type, true);
            }
          } else {
            normalizeObjectSlots(children, slots);
          }
        } else if (children) {
          normalizeVNodeSlots(instance, children);
        }
      };
      updateSlots = (instance, children, optimized) => {
        const { vnode, slots } = instance;
        let needDeletionCheck = true;
        let deletionComparisonTarget = EMPTY_OBJ;
        if (vnode.shapeFlag & 32) {
          const type = children._;
          if (type) {
            if (isHmrUpdating) {
              assignSlots(slots, children, optimized);
              trigger(instance, "set", "$slots");
            } else if (optimized && type === 1) {
              needDeletionCheck = false;
            } else {
              assignSlots(slots, children, optimized);
            }
          } else {
            needDeletionCheck = !children.$stable;
            normalizeObjectSlots(children, slots);
          }
          deletionComparisonTarget = children;
        } else if (children) {
          normalizeVNodeSlots(instance, children);
          deletionComparisonTarget = { default: 1 };
        }
        if (needDeletionCheck) {
          for (const key in slots) {
            if (!isInternalKey(key) && deletionComparisonTarget[key] == null) {
              delete slots[key];
            }
          }
        }
      };
      queuePostRenderEffect = queueEffectWithSuspense;
      isSuspense = (type) => type.__isSuspense;
      Fragment = /* @__PURE__ */ Symbol.for("v-fgt");
      Text = /* @__PURE__ */ Symbol.for("v-txt");
      Comment = /* @__PURE__ */ Symbol.for("v-cmt");
      Static = /* @__PURE__ */ Symbol.for("v-stc");
      blockStack = [];
      currentBlock = null;
      isBlockTreeEnabled = 1;
      createVNodeWithArgsTransform = (...args) => {
        return _createVNode(
          ...vnodeArgsTransformer ? vnodeArgsTransformer(args, currentRenderingInstance) : args
        );
      };
      normalizeKey = ({ key }) => key != null ? key : null;
      normalizeRef = ({
        ref: ref2,
        ref_key,
        ref_for
      }) => {
        if (typeof ref2 === "number") {
          ref2 = "" + ref2;
        }
        return ref2 != null ? isString(ref2) || isRef2(ref2) || isFunction(ref2) ? { i: currentRenderingInstance, r: ref2, k: ref_key, f: !!ref_for } : ref2 : null;
      };
      createVNode = true ? createVNodeWithArgsTransform : _createVNode;
      emptyAppContext = createAppContext();
      uid = 0;
      currentInstance = null;
      getCurrentInstance = () => currentInstance || currentRenderingInstance;
      {
        const g = getGlobalThis();
        const registerGlobalSetter = (key, setter) => {
          let setters;
          if (!(setters = g[key]))
            setters = g[key] = [];
          setters.push(setter);
          return (v) => {
            if (setters.length > 1)
              setters.forEach((set) => set(v));
            else
              setters[0](v);
          };
        };
        internalSetCurrentInstance = registerGlobalSetter(
          `__VUE_INSTANCE_SETTERS__`,
          (v) => currentInstance = v
        );
        setInSSRSetupState = registerGlobalSetter(
          `__VUE_SSR_SETTERS__`,
          (v) => isInSSRComponentSetup = v
        );
      }
      setCurrentInstance = (instance) => {
        const prev = currentInstance;
        internalSetCurrentInstance(instance);
        instance.scope.on();
        return () => {
          instance.scope.off();
          internalSetCurrentInstance(prev);
        };
      };
      unsetCurrentInstance = () => {
        currentInstance && currentInstance.scope.off();
        internalSetCurrentInstance(null);
      };
      isBuiltInTag = /* @__PURE__ */ makeMap("slot,component");
      isInSSRComponentSetup = false;
      isRuntimeOnly = () => !compile;
      attrsProxyHandlers = true ? {
        get(target, key) {
          markAttrsAccessed();
          track(target, "get", "");
          return target[key];
        },
        set() {
          warn$1(`setupContext.attrs is readonly.`);
          return false;
        },
        deleteProperty() {
          warn$1(`setupContext.attrs is readonly.`);
          return false;
        }
      } : {
        get(target, key) {
          track(target, "get", "");
          return target[key];
        }
      };
      classifyRE = /(?:^|[-_])\w/g;
      classify = (str) => str.replace(classifyRE, (c) => c.toUpperCase()).replace(/[-_]/g, "");
      computed2 = (getterOrOptions, debugOptions) => {
        const c = computed(getterOrOptions, debugOptions, isInSSRComponentSetup);
        if (true) {
          const i = getCurrentInstance();
          if (i && i.appContext.config.warnRecursiveComputed) {
            c._warnRecursive = true;
          }
        }
        return c;
      };
      version = "3.5.29";
      warn2 = true ? warn$1 : NOOP;
    }
  });

  // ../node_modules/@vue/runtime-dom/dist/runtime-dom.esm-bundler.js
  function patchClass(el, value, isSVG) {
    const transitionClasses = el[vtcKey];
    if (transitionClasses) {
      value = (value ? [value, ...transitionClasses] : [...transitionClasses]).join(" ");
    }
    if (value == null) {
      el.removeAttribute("class");
    } else if (isSVG) {
      el.setAttribute("class", value);
    } else {
      el.className = value;
    }
  }
  function setDisplay(el, value) {
    el.style.display = value ? el[vShowOriginalDisplay] : "none";
    el[vShowHidden] = !value;
  }
  function patchStyle(el, prev, next) {
    const style = el.style;
    const isCssString = isString(next);
    let hasControlledDisplay = false;
    if (next && !isCssString) {
      if (prev) {
        if (!isString(prev)) {
          for (const key in prev) {
            if (next[key] == null) {
              setStyle(style, key, "");
            }
          }
        } else {
          for (const prevStyle of prev.split(";")) {
            const key = prevStyle.slice(0, prevStyle.indexOf(":")).trim();
            if (next[key] == null) {
              setStyle(style, key, "");
            }
          }
        }
      }
      for (const key in next) {
        if (key === "display") {
          hasControlledDisplay = true;
        }
        setStyle(style, key, next[key]);
      }
    } else {
      if (isCssString) {
        if (prev !== next) {
          const cssVarText = style[CSS_VAR_TEXT];
          if (cssVarText) {
            next += ";" + cssVarText;
          }
          style.cssText = next;
          hasControlledDisplay = displayRE.test(next);
        }
      } else if (prev) {
        el.removeAttribute("style");
      }
    }
    if (vShowOriginalDisplay in el) {
      el[vShowOriginalDisplay] = hasControlledDisplay ? style.display : "";
      if (el[vShowHidden]) {
        style.display = "none";
      }
    }
  }
  function setStyle(style, name, val) {
    if (isArray(val)) {
      val.forEach((v) => setStyle(style, name, v));
    } else {
      if (val == null)
        val = "";
      if (true) {
        if (semicolonRE.test(val)) {
          warn2(
            `Unexpected semicolon at the end of '${name}' style value: '${val}'`
          );
        }
      }
      if (name.startsWith("--")) {
        style.setProperty(name, val);
      } else {
        const prefixed = autoPrefix(style, name);
        if (importantRE.test(val)) {
          style.setProperty(
            hyphenate(prefixed),
            val.replace(importantRE, ""),
            "important"
          );
        } else {
          style[prefixed] = val;
        }
      }
    }
  }
  function autoPrefix(style, rawName) {
    const cached = prefixCache[rawName];
    if (cached) {
      return cached;
    }
    let name = camelize(rawName);
    if (name !== "filter" && name in style) {
      return prefixCache[rawName] = name;
    }
    name = capitalize(name);
    for (let i = 0; i < prefixes.length; i++) {
      const prefixed = prefixes[i] + name;
      if (prefixed in style) {
        return prefixCache[rawName] = prefixed;
      }
    }
    return rawName;
  }
  function patchAttr(el, key, value, isSVG, instance, isBoolean2 = isSpecialBooleanAttr(key)) {
    if (isSVG && key.startsWith("xlink:")) {
      if (value == null) {
        el.removeAttributeNS(xlinkNS, key.slice(6, key.length));
      } else {
        el.setAttributeNS(xlinkNS, key, value);
      }
    } else {
      if (value == null || isBoolean2 && !includeBooleanAttr(value)) {
        el.removeAttribute(key);
      } else {
        el.setAttribute(
          key,
          isBoolean2 ? "" : isSymbol(value) ? String(value) : value
        );
      }
    }
  }
  function patchDOMProp(el, key, value, parentComponent, attrName) {
    if (key === "innerHTML" || key === "textContent") {
      if (value != null) {
        el[key] = key === "innerHTML" ? unsafeToTrustedHTML(value) : value;
      }
      return;
    }
    const tag = el.tagName;
    if (key === "value" && tag !== "PROGRESS" && !tag.includes("-")) {
      const oldValue = tag === "OPTION" ? el.getAttribute("value") || "" : el.value;
      const newValue = value == null ? el.type === "checkbox" ? "on" : "" : String(value);
      if (oldValue !== newValue || !("_value" in el)) {
        el.value = newValue;
      }
      if (value == null) {
        el.removeAttribute(key);
      }
      el._value = value;
      return;
    }
    let needRemove = false;
    if (value === "" || value == null) {
      const type = typeof el[key];
      if (type === "boolean") {
        value = includeBooleanAttr(value);
      } else if (value == null && type === "string") {
        value = "";
        needRemove = true;
      } else if (type === "number") {
        value = 0;
        needRemove = true;
      }
    }
    try {
      el[key] = value;
    } catch (e) {
      if (!needRemove) {
        warn2(
          `Failed setting prop "${key}" on <${tag.toLowerCase()}>: value ${value} is invalid.`,
          e
        );
      }
    }
    needRemove && el.removeAttribute(attrName || key);
  }
  function addEventListener(el, event, handler, options) {
    el.addEventListener(event, handler, options);
  }
  function removeEventListener(el, event, handler, options) {
    el.removeEventListener(event, handler, options);
  }
  function patchEvent(el, rawName, prevValue, nextValue, instance = null) {
    const invokers = el[veiKey] || (el[veiKey] = {});
    const existingInvoker = invokers[rawName];
    if (nextValue && existingInvoker) {
      existingInvoker.value = true ? sanitizeEventValue(nextValue, rawName) : nextValue;
    } else {
      const [name, options] = parseName(rawName);
      if (nextValue) {
        const invoker = invokers[rawName] = createInvoker(
          true ? sanitizeEventValue(nextValue, rawName) : nextValue,
          instance
        );
        addEventListener(el, name, invoker, options);
      } else if (existingInvoker) {
        removeEventListener(el, name, existingInvoker, options);
        invokers[rawName] = void 0;
      }
    }
  }
  function parseName(name) {
    let options;
    if (optionsModifierRE.test(name)) {
      options = {};
      let m;
      while (m = name.match(optionsModifierRE)) {
        name = name.slice(0, name.length - m[0].length);
        options[m[0].toLowerCase()] = true;
      }
    }
    const event = name[2] === ":" ? name.slice(3) : hyphenate(name.slice(2));
    return [event, options];
  }
  function createInvoker(initialValue, instance) {
    const invoker = (e) => {
      if (!e._vts) {
        e._vts = Date.now();
      } else if (e._vts <= invoker.attached) {
        return;
      }
      callWithAsyncErrorHandling(
        patchStopImmediatePropagation(e, invoker.value),
        instance,
        5,
        [e]
      );
    };
    invoker.value = initialValue;
    invoker.attached = getNow();
    return invoker;
  }
  function sanitizeEventValue(value, propName) {
    if (isFunction(value) || isArray(value)) {
      return value;
    }
    warn2(
      `Wrong type passed as event handler to ${propName} - did you forget @ or : in front of your prop?
Expected function or array of functions, received type ${typeof value}.`
    );
    return NOOP;
  }
  function patchStopImmediatePropagation(e, value) {
    if (isArray(value)) {
      const originalStop = e.stopImmediatePropagation;
      e.stopImmediatePropagation = () => {
        originalStop.call(e);
        e._stopped = true;
      };
      return value.map(
        (fn) => (e2) => !e2._stopped && fn && fn(e2)
      );
    } else {
      return value;
    }
  }
  function shouldSetAsProp(el, key, value, isSVG) {
    if (isSVG) {
      if (key === "innerHTML" || key === "textContent") {
        return true;
      }
      if (key in el && isNativeOn(key) && isFunction(value)) {
        return true;
      }
      return false;
    }
    if (key === "spellcheck" || key === "draggable" || key === "translate" || key === "autocorrect") {
      return false;
    }
    if (key === "sandbox" && el.tagName === "IFRAME") {
      return false;
    }
    if (key === "form") {
      return false;
    }
    if (key === "list" && el.tagName === "INPUT") {
      return false;
    }
    if (key === "type" && el.tagName === "TEXTAREA") {
      return false;
    }
    if (key === "width" || key === "height") {
      const tag = el.tagName;
      if (tag === "IMG" || tag === "VIDEO" || tag === "CANVAS" || tag === "SOURCE") {
        return false;
      }
    }
    if (isNativeOn(key) && isString(value)) {
      return false;
    }
    return key in el;
  }
  function setChecked(el, { value, oldValue }, vnode) {
    el._modelValue = value;
    let checked;
    if (isArray(value)) {
      checked = looseIndexOf(value, vnode.props.value) > -1;
    } else if (isSet(value)) {
      checked = value.has(vnode.props.value);
    } else {
      if (value === oldValue)
        return;
      checked = looseEqual(value, getCheckboxValue(el, true));
    }
    if (el.checked !== checked) {
      el.checked = checked;
    }
  }
  function setSelected(el, value) {
    const isMultiple = el.multiple;
    const isArrayValue = isArray(value);
    if (isMultiple && !isArrayValue && !isSet(value)) {
      warn2(
        `<select multiple v-model> expects an Array or Set value for its binding, but got ${Object.prototype.toString.call(value).slice(8, -1)}.`
      );
      return;
    }
    for (let i = 0, l = el.options.length; i < l; i++) {
      const option = el.options[i];
      const optionValue = getValue(option);
      if (isMultiple) {
        if (isArrayValue) {
          const optionType = typeof optionValue;
          if (optionType === "string" || optionType === "number") {
            option.selected = value.some((v) => String(v) === String(optionValue));
          } else {
            option.selected = looseIndexOf(value, optionValue) > -1;
          }
        } else {
          option.selected = value.has(optionValue);
        }
      } else if (looseEqual(getValue(option), value)) {
        if (el.selectedIndex !== i)
          el.selectedIndex = i;
        return;
      }
    }
    if (!isMultiple && el.selectedIndex !== -1) {
      el.selectedIndex = -1;
    }
  }
  function getValue(el) {
    return "_value" in el ? el._value : el.value;
  }
  function getCheckboxValue(el, checked) {
    const key = checked ? "_trueValue" : "_falseValue";
    return key in el ? el[key] : checked;
  }
  function ensureRenderer() {
    return renderer || (renderer = createRenderer(rendererOptions));
  }
  function resolveRootNamespace(container) {
    if (container instanceof SVGElement) {
      return "svg";
    }
    if (typeof MathMLElement === "function" && container instanceof MathMLElement) {
      return "mathml";
    }
  }
  function injectNativeTagCheck(app) {
    Object.defineProperty(app.config, "isNativeTag", {
      value: (tag) => isHTMLTag(tag) || isSVGTag(tag) || isMathMLTag(tag),
      writable: false
    });
  }
  function injectCompilerOptionsCheck(app) {
    if (isRuntimeOnly()) {
      const isCustomElement = app.config.isCustomElement;
      Object.defineProperty(app.config, "isCustomElement", {
        get() {
          return isCustomElement;
        },
        set() {
          warn2(
            `The \`isCustomElement\` config option is deprecated. Use \`compilerOptions.isCustomElement\` instead.`
          );
        }
      });
      const compilerOptions = app.config.compilerOptions;
      const msg = `The \`compilerOptions\` config option is only respected when using a build of Vue.js that includes the runtime compiler (aka "full build"). Since you are using the runtime-only build, \`compilerOptions\` must be passed to \`@vue/compiler-dom\` in the build setup instead.
- For vue-loader: pass it via vue-loader's \`compilerOptions\` loader option.
- For vue-cli: see https://cli.vuejs.org/guide/webpack.html#modifying-options-of-a-loader
- For vite: pass it via @vitejs/plugin-vue options. See https://github.com/vitejs/vite-plugin-vue/tree/main/packages/plugin-vue#example-for-passing-options-to-vuecompiler-sfc`;
      Object.defineProperty(app.config, "compilerOptions", {
        get() {
          warn2(msg);
          return compilerOptions;
        },
        set() {
          warn2(msg);
        }
      });
    }
  }
  function normalizeContainer(container) {
    if (isString(container)) {
      const res = document.querySelector(container);
      if (!res) {
        warn2(
          `Failed to mount app: mount target selector "${container}" returned null.`
        );
      }
      return res;
    }
    if (window.ShadowRoot && container instanceof window.ShadowRoot && container.mode === "closed") {
      warn2(
        `mounting on a ShadowRoot with \`{mode: "closed"}\` may lead to unpredictable bugs`
      );
    }
    return container;
  }
  var policy, tt, unsafeToTrustedHTML, svgNS, mathmlNS, doc, templateContainer, nodeOps, vtcKey, vShowOriginalDisplay, vShowHidden, vShow, CSS_VAR_TEXT, displayRE, semicolonRE, importantRE, prefixes, prefixCache, xlinkNS, veiKey, optionsModifierRE, cachedNow, p, getNow, isNativeOn, patchProp, getModelAssigner, assignKey, vModelCheckbox, vModelSelect, rendererOptions, renderer, createApp;
  var init_runtime_dom_esm_bundler = __esm({
    "../node_modules/@vue/runtime-dom/dist/runtime-dom.esm-bundler.js"() {
      init_runtime_core_esm_bundler();
      init_runtime_core_esm_bundler();
      init_shared_esm_bundler();
      policy = void 0;
      tt = typeof window !== "undefined" && window.trustedTypes;
      if (tt) {
        try {
          policy = /* @__PURE__ */ tt.createPolicy("vue", {
            createHTML: (val) => val
          });
        } catch (e) {
          warn2(`Error creating trusted types policy: ${e}`);
        }
      }
      unsafeToTrustedHTML = policy ? (val) => policy.createHTML(val) : (val) => val;
      svgNS = "http://www.w3.org/2000/svg";
      mathmlNS = "http://www.w3.org/1998/Math/MathML";
      doc = typeof document !== "undefined" ? document : null;
      templateContainer = doc && /* @__PURE__ */ doc.createElement("template");
      nodeOps = {
        insert: (child, parent, anchor) => {
          parent.insertBefore(child, anchor || null);
        },
        remove: (child) => {
          const parent = child.parentNode;
          if (parent) {
            parent.removeChild(child);
          }
        },
        createElement: (tag, namespace, is, props) => {
          const el = namespace === "svg" ? doc.createElementNS(svgNS, tag) : namespace === "mathml" ? doc.createElementNS(mathmlNS, tag) : is ? doc.createElement(tag, { is }) : doc.createElement(tag);
          if (tag === "select" && props && props.multiple != null) {
            el.setAttribute("multiple", props.multiple);
          }
          return el;
        },
        createText: (text) => doc.createTextNode(text),
        createComment: (text) => doc.createComment(text),
        setText: (node, text) => {
          node.nodeValue = text;
        },
        setElementText: (el, text) => {
          el.textContent = text;
        },
        parentNode: (node) => node.parentNode,
        nextSibling: (node) => node.nextSibling,
        querySelector: (selector) => doc.querySelector(selector),
        setScopeId(el, id) {
          el.setAttribute(id, "");
        },
        insertStaticContent(content, parent, anchor, namespace, start, end) {
          const before = anchor ? anchor.previousSibling : parent.lastChild;
          if (start && (start === end || start.nextSibling)) {
            while (true) {
              parent.insertBefore(start.cloneNode(true), anchor);
              if (start === end || !(start = start.nextSibling))
                break;
            }
          } else {
            templateContainer.innerHTML = unsafeToTrustedHTML(
              namespace === "svg" ? `<svg>${content}</svg>` : namespace === "mathml" ? `<math>${content}</math>` : content
            );
            const template = templateContainer.content;
            if (namespace === "svg" || namespace === "mathml") {
              const wrapper = template.firstChild;
              while (wrapper.firstChild) {
                template.appendChild(wrapper.firstChild);
              }
              template.removeChild(wrapper);
            }
            parent.insertBefore(template, anchor);
          }
          return [
            before ? before.nextSibling : parent.firstChild,
            anchor ? anchor.previousSibling : parent.lastChild
          ];
        }
      };
      vtcKey = /* @__PURE__ */ Symbol("_vtc");
      vShowOriginalDisplay = /* @__PURE__ */ Symbol("_vod");
      vShowHidden = /* @__PURE__ */ Symbol("_vsh");
      vShow = {
        name: "show",
        beforeMount(el, { value }, { transition }) {
          el[vShowOriginalDisplay] = el.style.display === "none" ? "" : el.style.display;
          if (transition && value) {
            transition.beforeEnter(el);
          } else {
            setDisplay(el, value);
          }
        },
        mounted(el, { value }, { transition }) {
          if (transition && value) {
            transition.enter(el);
          }
        },
        updated(el, { value, oldValue }, { transition }) {
          if (!value === !oldValue)
            return;
          if (transition) {
            if (value) {
              transition.beforeEnter(el);
              setDisplay(el, true);
              transition.enter(el);
            } else {
              transition.leave(el, () => {
                setDisplay(el, false);
              });
            }
          } else {
            setDisplay(el, value);
          }
        },
        beforeUnmount(el, { value }) {
          setDisplay(el, value);
        }
      };
      CSS_VAR_TEXT = /* @__PURE__ */ Symbol(true ? "CSS_VAR_TEXT" : "");
      displayRE = /(?:^|;)\s*display\s*:/;
      semicolonRE = /[^\\];\s*$/;
      importantRE = /\s*!important$/;
      prefixes = ["Webkit", "Moz", "ms"];
      prefixCache = {};
      xlinkNS = "http://www.w3.org/1999/xlink";
      veiKey = /* @__PURE__ */ Symbol("_vei");
      optionsModifierRE = /(?:Once|Passive|Capture)$/;
      cachedNow = 0;
      p = /* @__PURE__ */ Promise.resolve();
      getNow = () => cachedNow || (p.then(() => cachedNow = 0), cachedNow = Date.now());
      isNativeOn = (key) => key.charCodeAt(0) === 111 && key.charCodeAt(1) === 110 && key.charCodeAt(2) > 96 && key.charCodeAt(2) < 123;
      patchProp = (el, key, prevValue, nextValue, namespace, parentComponent) => {
        const isSVG = namespace === "svg";
        if (key === "class") {
          patchClass(el, nextValue, isSVG);
        } else if (key === "style") {
          patchStyle(el, prevValue, nextValue);
        } else if (isOn(key)) {
          if (!isModelListener(key)) {
            patchEvent(el, key, prevValue, nextValue, parentComponent);
          }
        } else if (key[0] === "." ? (key = key.slice(1), true) : key[0] === "^" ? (key = key.slice(1), false) : shouldSetAsProp(el, key, nextValue, isSVG)) {
          patchDOMProp(el, key, nextValue);
          if (!el.tagName.includes("-") && (key === "value" || key === "checked" || key === "selected")) {
            patchAttr(el, key, nextValue, isSVG, parentComponent, key !== "value");
          }
        } else if (el._isVueCE && (/[A-Z]/.test(key) || !isString(nextValue))) {
          patchDOMProp(el, camelize(key), nextValue, parentComponent, key);
        } else {
          if (key === "true-value") {
            el._trueValue = nextValue;
          } else if (key === "false-value") {
            el._falseValue = nextValue;
          }
          patchAttr(el, key, nextValue, isSVG);
        }
      };
      getModelAssigner = (vnode) => {
        const fn = vnode.props["onUpdate:modelValue"] || false;
        return isArray(fn) ? (value) => invokeArrayFns(fn, value) : fn;
      };
      assignKey = /* @__PURE__ */ Symbol("_assign");
      vModelCheckbox = {
        deep: true,
        created(el, _, vnode) {
          el[assignKey] = getModelAssigner(vnode);
          addEventListener(el, "change", () => {
            const modelValue = el._modelValue;
            const elementValue = getValue(el);
            const checked = el.checked;
            const assign = el[assignKey];
            if (isArray(modelValue)) {
              const index = looseIndexOf(modelValue, elementValue);
              const found = index !== -1;
              if (checked && !found) {
                assign(modelValue.concat(elementValue));
              } else if (!checked && found) {
                const filtered = [...modelValue];
                filtered.splice(index, 1);
                assign(filtered);
              }
            } else if (isSet(modelValue)) {
              const cloned = new Set(modelValue);
              if (checked) {
                cloned.add(elementValue);
              } else {
                cloned.delete(elementValue);
              }
              assign(cloned);
            } else {
              assign(getCheckboxValue(el, checked));
            }
          });
        },
        mounted: setChecked,
        beforeUpdate(el, binding, vnode) {
          el[assignKey] = getModelAssigner(vnode);
          setChecked(el, binding, vnode);
        }
      };
      vModelSelect = {
        deep: true,
        created(el, { value, modifiers: { number } }, vnode) {
          const isSetModel = isSet(value);
          addEventListener(el, "change", () => {
            const selectedVal = Array.prototype.filter.call(el.options, (o) => o.selected).map(
              (o) => number ? looseToNumber(getValue(o)) : getValue(o)
            );
            el[assignKey](
              el.multiple ? isSetModel ? new Set(selectedVal) : selectedVal : selectedVal[0]
            );
            el._assigning = true;
            nextTick(() => {
              el._assigning = false;
            });
          });
          el[assignKey] = getModelAssigner(vnode);
        },
        mounted(el, { value }) {
          setSelected(el, value);
        },
        beforeUpdate(el, _binding, vnode) {
          el[assignKey] = getModelAssigner(vnode);
        },
        updated(el, { value }) {
          if (!el._assigning) {
            setSelected(el, value);
          }
        }
      };
      rendererOptions = /* @__PURE__ */ extend({ patchProp }, nodeOps);
      createApp = (...args) => {
        const app = ensureRenderer().createApp(...args);
        if (true) {
          injectNativeTagCheck(app);
          injectCompilerOptionsCheck(app);
        }
        const { mount } = app;
        app.mount = (containerOrSelector) => {
          const container = normalizeContainer(containerOrSelector);
          if (!container)
            return;
          const component = app._component;
          if (!isFunction(component) && !component.render && !component.template) {
            component.template = container.innerHTML;
          }
          if (container.nodeType === 1) {
            container.textContent = "";
          }
          const proxy = mount(container, false, resolveRootNamespace(container));
          if (container instanceof Element) {
            container.removeAttribute("v-cloak");
            container.setAttribute("data-v-app", "");
          }
          return proxy;
        };
        return app;
      };
    }
  });

  // ../node_modules/vue/dist/vue.runtime.esm-bundler.js
  function initDev() {
    {
      initCustomFormatter();
    }
  }
  var init_vue_runtime_esm_bundler = __esm({
    "../node_modules/vue/dist/vue.runtime.esm-bundler.js"() {
      init_runtime_dom_esm_bundler();
      init_runtime_dom_esm_bundler();
      if (true) {
        initDev();
      }
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/api.js
  function call(method, args = {}) {
    return frappe.call({ method: NS + method, args }).then((r) => r.message);
  }
  function callRaw(method, args = {}) {
    return frappe.call({ method, args }).then((r) => r.message);
  }
  function today() {
    return frappe.datetime.get_today();
  }
  function sysDate(v) {
    if (!v)
      return null;
    if (/^\d{4}-\d{2}-\d{2}/.test(v))
      return v.slice(0, 10);
    return frappe.datetime.user_to_str(v) || v;
  }
  function fmt(n, digits = 2) {
    const v = parseFloat(n);
    if (isNaN(v))
      return digits === 0 ? "0" : 0 .toFixed(digits);
    return v.toFixed(digits);
  }
  function splitPair(s) {
    const [a, b] = String(s || "0/0").split("/").map(Number);
    return { hr: isNaN(a) ? 0 : a, n: isNaN(b) ? 0 : b };
  }
  function cleanHtml(html) {
    return String(html || "").replace(/(\d+\.\d{3,})/g, (m) => (+m).toFixed(2));
  }
  function ensureXLSX() {
    if (window.XLSX)
      return Promise.resolve();
    if (!xlsxPromise) {
      xlsxPromise = frappe.require([
        "https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"
      ]);
    }
    return xlsxPromise;
  }
  function downloadRowsAsXlsx(filename, sheetName, rows) {
    return ensureXLSX().then(() => {
      const ws = XLSX.utils.aoa_to_sheet(rows);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, sheetName);
      XLSX.writeFile(wb, filename);
    });
  }
  function downloadUrl(url) {
    const a = document.createElement("a");
    a.href = url;
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    setTimeout(() => a.parentNode && a.parentNode.removeChild(a), 5e3);
  }
  var NS, xlsxPromise;
  var init_api = __esm({
    "../teampro/teampro/public/js/it_dashboard/api.js"() {
      NS = "teampro.teampro.page.new_it_dashboard.new_it.";
      xlsxPromise = null;
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/icons.js
  function icon(name, size = 16) {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${PATHS[name] || PATHS.folder}</svg>`;
  }
  var PATHS, Icon;
  var init_icons = __esm({
    "../teampro/teampro/public/js/it_dashboard/icons.js"() {
      PATHS = {
        folder: '<path d="M4 6a2 2 0 0 1 2-2h3l2 2h7a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/>',
        globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 4 5.6 4 9s-1.5 6.4-4 9c-2.5-2.6-4-5.6-4-9s1.5-6.4 4-9z"/>',
        wrench: '<path d="M14.7 6.3a4.5 4.5 0 0 0-6 6L3 18l3 3 5.7-5.7a4.5 4.5 0 0 0 6-6L14 13l-3-3z"/>',
        search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
        building: '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M9 8h2M13 8h2M9 12h2M13 12h2M9 16h2M13 16h2"/>',
        list: '<path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"/>',
        "folder-open": '<path d="M4 6a2 2 0 0 1 2-2h3l2 2h7a2 2 0 0 1 2 2v2"/><path d="M4 6v12a2 2 0 0 0 2 2h13l3-9a2 2 0 0 0-2-2H6.5a2 2 0 0 0-2 1.7z"/>',
        refresh: '<path d="M21 12a9 9 0 1 1-2.64-6.36M21 3v6h-6"/>',
        "user-check": '<path d="M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z"/><path d="M2 21a7 7 0 0 1 14 0M16 11l2 2 4-4"/>',
        users: '<path d="M8 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z"/><path d="M1 21a7 7 0 0 1 14 0"/><path d="M17 8a3 3 0 1 1 2-5.2M23 21a7 7 0 0 0-5-6.7"/>',
        download: '<path d="M12 3v12m0 0 4-4m-4 4-4-4"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/>',
        calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/>',
        clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        check: '<path d="m4 12.5 5 5L20 6.5"/>',
        eye: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
        "chevron-down": '<path d="m6 9 6 6 6-6"/>',
        "chevron-right": '<path d="m9 6 6 6-6 6"/>',
        "bar-chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
        layers: '<path d="m12 2 9 5-9 5-9-5z"/><path d="m3 12 9 5 9-5M3 17l9 5 9-5"/>',
        alert: '<path d="M12 3 2 21h20z"/><path d="M12 10v5m0 3h.01"/>',
        filter: '<path d="M3 4h18l-7 8v6l-4 2v-8z"/>',
        printer: '<path d="M6 9V3h12v6"/><rect x="4" y="9" width="16" height="8" rx="1"/><path d="M6 15h12v6H6z"/>'
      };
      Icon = {
        props: { name: String, size: { type: Number, default: 16 } },
        computed: {
          html() {
            return icon(this.name, this.size);
          }
        },
        template: `<span class="itd-icon" v-html="html"></span>`
      };
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/StatGroup.vue?type=script
  var StatGroup_default;
  var init_StatGroup = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/StatGroup.vue?type=script"() {
      init_icons();
      StatGroup_default = {
        __name: "StatGroup",
        props: {
          title: String,
          cards: { type: Array, default: () => [] },
          active: { type: String, default: null },
          loading: Boolean
        },
        emits: ["select"],
        setup(__props, { expose: __expose, emit: __emit }) {
          __expose();
          const emit2 = __emit;
          const __returned__ = { emit: emit2, get Icon() {
            return Icon;
          } };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/StatGroup.vue?type=template
  function render(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createElementBlock("div", _hoisted_1, [
      createBaseVNode("div", _hoisted_2, toDisplayString($props.title), 1),
      createBaseVNode("div", _hoisted_3, [
        $props.loading ? (openBlock(), createElementBlock(Fragment, { key: 0 }, renderList(5, (i) => {
          return createBaseVNode("div", {
            key: i,
            class: "itd-stat itd-skel-card"
          });
        }), 64)) : (openBlock(true), createElementBlock(Fragment, { key: 1 }, renderList($props.cards, (c) => {
          return openBlock(), createElementBlock("button", {
            key: c.key,
            class: normalizeClass(["itd-stat", { "itd-stat--active": $props.active === c.key, "itd-stat--clickable": true }]),
            style: normalizeStyle({ "--stat-color": c.color }),
            onClick: ($event) => $setup.emit("select", c.key)
          }, [
            createBaseVNode("span", _hoisted_5, [
              createVNode($setup["Icon"], {
                name: c.icon,
                size: 17
              }, null, 8, ["name"])
            ]),
            createBaseVNode("span", _hoisted_6, toDisplayString(c.title), 1),
            createBaseVNode("span", _hoisted_7, toDisplayString(c.value), 1),
            c.hours !== void 0 ? (openBlock(), createElementBlock("span", _hoisted_8, toDisplayString(c.hours) + " hr", 1)) : (openBlock(), createElementBlock("span", _hoisted_9, toDisplayString(c.subtitle), 1))
          ], 14, _hoisted_4);
        }), 128))
      ])
    ]);
  }
  var _hoisted_1, _hoisted_2, _hoisted_3, _hoisted_4, _hoisted_5, _hoisted_6, _hoisted_7, _hoisted_8, _hoisted_9;
  var init_StatGroup2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/StatGroup.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_1 = { class: "itd-statgroup" };
      _hoisted_2 = { class: "itd-statgroup-title" };
      _hoisted_3 = { class: "itd-stat-cards" };
      _hoisted_4 = ["onClick"];
      _hoisted_5 = { class: "itd-stat-icon" };
      _hoisted_6 = { class: "itd-stat-label" };
      _hoisted_7 = { class: "itd-stat-value" };
      _hoisted_8 = {
        key: 0,
        class: "itd-stat-hours"
      };
      _hoisted_9 = {
        key: 1,
        class: "itd-stat-sub"
      };
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/StatGroup.vue
  var StatGroup_default2;
  var init_StatGroup3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/StatGroup.vue"() {
      init_StatGroup();
      init_StatGroup2();
      StatGroup_default.render = render;
      StatGroup_default.__file = "../teampro/teampro/public/js/it_dashboard/components/StatGroup.vue";
      StatGroup_default2 = StatGroup_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProjectCounts.vue?type=script
  var ProjectCounts_default;
  var init_ProjectCounts = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProjectCounts.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_StatGroup3();
      ProjectCounts_default = {
        __name: "ProjectCounts",
        emits: ["select"],
        setup(__props, { expose: __expose, emit: __emit }) {
          __expose();
          const emit2 = __emit;
          const loading = ref(true);
          const cards = ref([]);
          const active = ref("Total");
          const PALETTE = [
            "#0096A6",
            "#2F8F46",
            "#C29100",
            "#540D6E",
            "#006D77",
            "#4169e1",
            "#8B0000",
            "#f9844a",
            "#bc5090",
            "#003f5c"
          ];
          const ICONS = {
            Total: "bar-chart",
            External: "globe",
            AMC: "wrench",
            Enquiry: "search",
            Internal: "building"
          };
          function select(key) {
            active.value = key;
            emit2("select", key === "Total" ? null : key);
          }
          onMounted(async () => {
            try {
              const m = await call("get_project_counts") || {};
              const list = [
                { key: "Total", title: "Total", value: m.total || 0, color: PALETTE[0], icon: "bar-chart", subtitle: "All Projects" }
              ];
              (m.projects || []).forEach((p2, i) => {
                if (p2.project_type === "Products")
                  return;
                list.push({
                  key: p2.project_type,
                  title: p2.project_type,
                  value: p2.count,
                  color: PALETTE[(i + 1) % PALETTE.length],
                  icon: ICONS[p2.project_type] || "folder",
                  subtitle: `${p2.project_type} type projects`
                });
              });
              cards.value = list;
            } finally {
              loading.value = false;
            }
          });
          const __returned__ = { emit: emit2, loading, cards, active, PALETTE, ICONS, select, ref, onMounted, get call() {
            return call;
          }, StatGroup: StatGroup_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProjectCounts.vue?type=template
  function render2(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["StatGroup"], {
      title: "Project Count",
      cards: $setup.cards,
      active: $setup.active,
      loading: $setup.loading,
      onSelect: $setup.select
    }, null, 8, ["cards", "active", "loading"]);
  }
  var init_ProjectCounts2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProjectCounts.vue?type=template"() {
      init_vue_runtime_esm_bundler();
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/ProjectCounts.vue
  var ProjectCounts_default2;
  var init_ProjectCounts3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/ProjectCounts.vue"() {
      init_ProjectCounts();
      init_ProjectCounts2();
      ProjectCounts_default.render = render2;
      ProjectCounts_default.__file = "../teampro/teampro/public/js/it_dashboard/components/ProjectCounts.vue";
      ProjectCounts_default2 = ProjectCounts_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/TaskCounts.vue?type=script
  var TaskCounts_default;
  var init_TaskCounts = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/TaskCounts.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_StatGroup3();
      TaskCounts_default = {
        __name: "TaskCounts",
        setup(__props, { expose: __expose }) {
          __expose();
          const loading = ref(true);
          const cards = ref([]);
          const META = {
            total: { title: "Total", color: "#0096A6", icon: "list", subtitle: "Total tasks" },
            open: { title: "Open", color: "#2F8F46", icon: "folder-open", subtitle: "Not yet started" },
            working: { title: "Working", color: "#C29100", icon: "clock", subtitle: "In progress now" },
            pr: { title: "Internal Review", color: "#540D6E", icon: "user-check", subtitle: "Awaiting internal review" },
            cr: { title: "Client Review", color: "#006D77", icon: "users", subtitle: "Awaiting client review" }
          };
          async function showTasks(key) {
            var _a;
            const rows = await call("get_tasks_project_wise", { type: key }) || [];
            const esc = frappe.utils.escape_html;
            const trs = rows.map(
              (p2) => `<tr>
				<td>${esc(p2.project || "No Project")}</td>
				<td>${p2.task_count}</td>
				<td>${fmt(p2.total_hours)}</td>
				<td style="text-align:left">${esc(p2.spoc || "No Spoc")}</td>
			</tr>`
            ).join("");
            const html = `<div style="max-height:400px;overflow-y:auto;">
		<table class="itd-dialog-table">
			<thead><tr><th>Project</th><th>Tasks</th><th>Hours</th><th>SPOC</th></tr></thead>
			<tbody>${trs || '<tr><td colspan="4" style="text-align:center">No tasks</td></tr>'}</tbody>
		</table></div>`;
            new frappe.ui.Dialog({
              title: ((_a = META[key]) == null ? void 0 : _a.title) || key,
              fields: [{ fieldname: "html_table", fieldtype: "HTML", options: html }]
            }).show();
          }
          onMounted(async () => {
            try {
              const tc = await call("get_task_summary") || {};
              cards.value = Object.keys(META).map((key) => ({
                key,
                title: META[key].title,
                value: tc[key] || 0,
                hours: fmt(tc[`${key}_total_hours`] || 0),
                color: META[key].color,
                icon: META[key].icon,
                subtitle: META[key].subtitle
              }));
            } finally {
              loading.value = false;
            }
          });
          const __returned__ = { loading, cards, META, showTasks, ref, onMounted, get call() {
            return call;
          }, get fmt() {
            return fmt;
          }, StatGroup: StatGroup_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/TaskCounts.vue?type=template
  function render3(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["StatGroup"], {
      title: "Task Count",
      cards: $setup.cards,
      loading: $setup.loading,
      onSelect: $setup.showTasks
    }, null, 8, ["cards", "loading"]);
  }
  var init_TaskCounts2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/TaskCounts.vue?type=template"() {
      init_vue_runtime_esm_bundler();
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/TaskCounts.vue
  var TaskCounts_default2;
  var init_TaskCounts3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/TaskCounts.vue"() {
      init_TaskCounts();
      init_TaskCounts2();
      TaskCounts_default.render = render3;
      TaskCounts_default.__file = "../teampro/teampro/public/js/it_dashboard/components/TaskCounts.vue";
      TaskCounts_default2 = TaskCounts_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SectionCard.vue?type=script
  var SectionCard_default;
  var init_SectionCard = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SectionCard.vue?type=script"() {
      SectionCard_default = {
        __name: "SectionCard",
        props: {
          title: String,
          subtitle: String,
          pad: { type: Boolean, default: false }
        },
        setup(__props, { expose: __expose }) {
          __expose();
          const __returned__ = {};
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SectionCard.vue?type=template
  function render4(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createElementBlock("section", _hoisted_12, [
      createBaseVNode("header", _hoisted_22, [
        createBaseVNode("h3", _hoisted_32, [
          createTextVNode(toDisplayString($props.title) + " ", 1),
          $props.subtitle ? (openBlock(), createElementBlock("span", _hoisted_42, toDisplayString($props.subtitle), 1)) : createCommentVNode("v-if", true)
        ]),
        createBaseVNode("div", _hoisted_52, [
          renderSlot(_ctx.$slots, "actions")
        ])
      ]),
      createBaseVNode("div", {
        class: normalizeClass(["itd-card-body", { "itd-card-body--pad": $props.pad }])
      }, [
        renderSlot(_ctx.$slots, "default")
      ], 2)
    ]);
  }
  var _hoisted_12, _hoisted_22, _hoisted_32, _hoisted_42, _hoisted_52;
  var init_SectionCard2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SectionCard.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_12 = { class: "itd-card" };
      _hoisted_22 = { class: "itd-card-head" };
      _hoisted_32 = { class: "itd-card-title" };
      _hoisted_42 = {
        key: 0,
        class: "itd-card-sub"
      };
      _hoisted_52 = { class: "itd-card-actions" };
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/SectionCard.vue
  var SectionCard_default2;
  var init_SectionCard3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/SectionCard.vue"() {
      init_SectionCard();
      init_SectionCard2();
      SectionCard_default.render = render4;
      SectionCard_default.__file = "../teampro/teampro/public/js/it_dashboard/components/SectionCard.vue";
      SectionCard_default2 = SectionCard_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SkeletonRows.vue?type=script
  var SkeletonRows_default;
  var init_SkeletonRows = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SkeletonRows.vue?type=script"() {
      SkeletonRows_default = {
        __name: "SkeletonRows",
        props: {
          rows: { type: Number, default: 6 },
          cols: { type: Number, default: 6 }
        },
        setup(__props, { expose: __expose }) {
          __expose();
          const __returned__ = {};
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SkeletonRows.vue?type=template
  function render5(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createElementBlock("div", _hoisted_13, [
      _hoisted_23,
      (openBlock(true), createElementBlock(Fragment, null, renderList($props.rows, (i) => {
        return openBlock(), createElementBlock("div", {
          key: i,
          class: "itd-skel-row"
        }, [
          (openBlock(true), createElementBlock(Fragment, null, renderList($props.cols, (j) => {
            return openBlock(), createElementBlock("div", {
              key: j,
              class: "itd-skel-cell"
            });
          }), 128))
        ]);
      }), 128))
    ]);
  }
  var _hoisted_13, _hoisted_23;
  var init_SkeletonRows2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SkeletonRows.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_13 = { class: "itd-skel-table" };
      _hoisted_23 = /* @__PURE__ */ createBaseVNode("div", { class: "itd-skel-head" }, null, -1);
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/SkeletonRows.vue
  var SkeletonRows_default2;
  var init_SkeletonRows3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/SkeletonRows.vue"() {
      init_SkeletonRows();
      init_SkeletonRows2();
      SkeletonRows_default.render = render5;
      SkeletonRows_default.__file = "../teampro/teampro/public/js/it_dashboard/components/SkeletonRows.vue";
      SkeletonRows_default2 = SkeletonRows_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/PsrTable.vue?type=script
  var PsrTable_default;
  var init_PsrTable = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/PsrTable.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_icons();
      init_SectionCard3();
      init_SkeletonRows3();
      PsrTable_default = {
        __name: "PsrTable",
        setup(__props, { expose: __expose }) {
          const rows = ref([]);
          const view = ref("overall");
          const typeFilter = ref(null);
          const loading = ref(true);
          onMounted(async () => {
            try {
              rows.value = await call("get_tasks_project_pivot") || [];
            } finally {
              loading.value = false;
            }
          });
          const filtered = computed2(
            () => typeFilter.value ? rows.value.filter((r) => r.project_type === typeFilter.value) : rows.value
          );
          const COLS = ["open", "working", "pr", "cr"];
          const totals = computed2(() => {
            const t = {};
            for (const c of COLS) {
              const key = view.value === "current" && c !== "open" ? `${c}_td` : c;
              t[c] = filtered.value.reduce(
                (acc, r) => {
                  const p2 = splitPair(r[key]);
                  acc.hr += p2.hr;
                  acc.n += p2.n;
                  return acc;
                },
                { hr: 0, n: 0 }
              );
            }
            return t;
          });
          function cellVal(row, col) {
            const key = view.value === "current" && col !== "open" ? `${col}_td` : col;
            const p2 = splitPair(row[key]);
            return `${p2.hr.toFixed(2)}/${p2.n}`;
          }
          function setTypeFilter(t) {
            typeFilter.value = t;
          }
          __expose({ setTypeFilter });
          function download() {
            const header = ["S.No", "Project", "Type", "Open", "Working", "PR", "CR"];
            const data = filtered.value.map((r, i) => [
              i + 1,
              r.project,
              r.project_type,
              cellVal(r, "open"),
              cellVal(r, "working"),
              cellVal(r, "pr"),
              cellVal(r, "cr")
            ]);
            downloadRowsAsXlsx(`PSR_${view.value}_${frappe.datetime.now_date()}.xlsx`, "PSR", [
              header,
              ...data
            ]);
          }
          const __returned__ = { rows, view, typeFilter, loading, filtered, COLS, totals, cellVal, setTypeFilter, download, ref, computed: computed2, onMounted, get call() {
            return call;
          }, get splitPair() {
            return splitPair;
          }, get fmt() {
            return fmt;
          }, get downloadRowsAsXlsx() {
            return downloadRowsAsXlsx;
          }, get Icon() {
            return Icon;
          }, SectionCard: SectionCard_default2, SkeletonRows: SkeletonRows_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/PsrTable.vue?type=template
  function render6(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["SectionCard"], {
      title: "Project Status Report",
      subtitle: "PSR",
      class: "itd-psr"
    }, {
      actions: withCtx(() => [
        createBaseVNode("div", _hoisted_14, [
          createBaseVNode("button", {
            class: normalizeClass(["itd-seg-btn", { "itd-seg-btn--on": $setup.view === "overall" }]),
            onClick: _cache[0] || (_cache[0] = ($event) => $setup.view = "overall")
          }, " Overall ", 2),
          createBaseVNode("button", {
            class: normalizeClass(["itd-seg-btn", { "itd-seg-btn--on": $setup.view === "current" }]),
            onClick: _cache[1] || (_cache[1] = ($event) => $setup.view = "current")
          }, " Current ", 2)
        ]),
        createBaseVNode("button", {
          class: "itd-iconbtn",
          title: "Download Excel",
          onClick: $setup.download
        }, [
          createVNode($setup["Icon"], {
            name: "download",
            size: 15
          })
        ])
      ]),
      default: withCtx(() => [
        $setup.loading ? (openBlock(), createBlock($setup["SkeletonRows"], {
          key: 0,
          rows: 8,
          cols: 7
        })) : !$setup.filtered.length ? (openBlock(), createElementBlock("div", _hoisted_24, "No projects found")) : (openBlock(), createElementBlock("div", _hoisted_33, [
          createBaseVNode("table", _hoisted_43, [
            _hoisted_53,
            createBaseVNode("tbody", null, [
              (openBlock(true), createElementBlock(Fragment, null, renderList($setup.filtered, (row) => {
                return openBlock(), createElementBlock("tr", {
                  key: row.project
                }, [
                  createBaseVNode("td", _hoisted_62, toDisplayString(row.s_no), 1),
                  createBaseVNode("td", _hoisted_72, [
                    createBaseVNode("a", {
                      href: `/app/project/${encodeURIComponent(row.project)}`,
                      target: "_blank",
                      class: "itd-link"
                    }, toDisplayString(row.project), 9, _hoisted_82)
                  ]),
                  createBaseVNode("td", _hoisted_92, [
                    createBaseVNode("span", _hoisted_10, toDisplayString(row.project_type), 1)
                  ]),
                  createBaseVNode("td", _hoisted_11, toDisplayString($setup.cellVal(row, "open")), 1),
                  createBaseVNode("td", _hoisted_122, toDisplayString($setup.cellVal(row, "working")), 1),
                  createBaseVNode("td", _hoisted_132, toDisplayString($setup.cellVal(row, "pr")), 1),
                  createBaseVNode("td", _hoisted_142, toDisplayString($setup.cellVal(row, "cr")), 1)
                ]);
              }), 128))
            ]),
            createBaseVNode("tfoot", null, [
              createBaseVNode("tr", null, [
                _hoisted_15,
                createBaseVNode("td", _hoisted_16, toDisplayString($setup.fmt($setup.totals.open.hr)) + "/" + toDisplayString($setup.totals.open.n), 1),
                createBaseVNode("td", _hoisted_17, toDisplayString($setup.fmt($setup.totals.working.hr)) + "/" + toDisplayString($setup.totals.working.n), 1),
                createBaseVNode("td", _hoisted_18, toDisplayString($setup.fmt($setup.totals.pr.hr)) + "/" + toDisplayString($setup.totals.pr.n), 1),
                createBaseVNode("td", _hoisted_19, toDisplayString($setup.fmt($setup.totals.cr.hr)) + "/" + toDisplayString($setup.totals.cr.n), 1)
              ])
            ])
          ])
        ]))
      ]),
      _: 1
    });
  }
  var _hoisted_14, _hoisted_24, _hoisted_33, _hoisted_43, _hoisted_53, _hoisted_62, _hoisted_72, _hoisted_82, _hoisted_92, _hoisted_10, _hoisted_11, _hoisted_122, _hoisted_132, _hoisted_142, _hoisted_15, _hoisted_16, _hoisted_17, _hoisted_18, _hoisted_19;
  var init_PsrTable2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/PsrTable.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_14 = { class: "itd-seg" };
      _hoisted_24 = {
        key: 1,
        class: "itd-empty"
      };
      _hoisted_33 = {
        key: 2,
        class: "itd-table-wrap itd-psr-scroll"
      };
      _hoisted_43 = { class: "itd-table" };
      _hoisted_53 = /* @__PURE__ */ createBaseVNode("thead", null, [
        /* @__PURE__ */ createBaseVNode("tr", null, [
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "S.No"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-left" }, "Project Name"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-left" }, "Type"),
          /* @__PURE__ */ createBaseVNode("th", {
            class: "itd-num",
            title: "Open tasks (hours / count)"
          }, "Open"),
          /* @__PURE__ */ createBaseVNode("th", {
            class: "itd-num",
            title: "Working (hours / count)"
          }, "W"),
          /* @__PURE__ */ createBaseVNode("th", {
            class: "itd-num",
            title: "Pending review (hours / count)"
          }, "PR"),
          /* @__PURE__ */ createBaseVNode("th", {
            class: "itd-num",
            title: "Client review (hours / count)"
          }, "CR")
        ])
      ], -1);
      _hoisted_62 = { class: "itd-num itd-muted" };
      _hoisted_72 = { class: "itd-left" };
      _hoisted_82 = ["href"];
      _hoisted_92 = { class: "itd-left" };
      _hoisted_10 = { class: "itd-tag" };
      _hoisted_11 = { class: "itd-num itd-mono" };
      _hoisted_122 = { class: "itd-num itd-mono" };
      _hoisted_132 = { class: "itd-num itd-mono" };
      _hoisted_142 = { class: "itd-num itd-mono" };
      _hoisted_15 = /* @__PURE__ */ createBaseVNode("td", { colspan: "3" }, "Total", -1);
      _hoisted_16 = { class: "itd-num" };
      _hoisted_17 = { class: "itd-num" };
      _hoisted_18 = { class: "itd-num" };
      _hoisted_19 = { class: "itd-num" };
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/PsrTable.vue
  var PsrTable_default2;
  var init_PsrTable3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/PsrTable.vue"() {
      init_PsrTable();
      init_PsrTable2();
      PsrTable_default.render = render6;
      PsrTable_default.__file = "../teampro/teampro/public/js/it_dashboard/components/PsrTable.vue";
      PsrTable_default2 = PsrTable_default;
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/store.js
  function teamKey(team) {
    return `t-${String(team || "").replace(/\s+/g, "_")}`;
  }
  function cbKey(team, cb) {
    return `cb-${String(team || "").replace(/\s+/g, "_")}-${String(cb || "").replace(/\s+/g, "_")}`;
  }
  function syncAllOpen() {
    prod.allOpen = prod.allTeams.length > 0 && prod.allTeams.every((t) => prod.openTeams.has(t)) && prod.allCbs.every((c) => prod.openCbs.has(c));
  }
  function setProdData(teams, cbs) {
    prod.allTeams = teams;
    prod.allCbs = cbs;
    prod.openTeams = new Set(teams);
    prod.openCbs = new Set(cbs);
    prod.allOpen = true;
  }
  function toggleProdAll(open) {
    if (open) {
      prod.openTeams = new Set(prod.allTeams);
      prod.openCbs = new Set(prod.allCbs);
    } else {
      prod.openTeams.clear();
      prod.openCbs.clear();
    }
    prod.allOpen = open;
  }
  function toggleProdTeam(team) {
    if (prod.openTeams.has(team))
      prod.openTeams.delete(team);
    else
      prod.openTeams.add(team);
    syncAllOpen();
  }
  function toggleProdCb(key) {
    if (prod.openCbs.has(key))
      prod.openCbs.delete(key);
    else
      prod.openCbs.add(key);
    syncAllOpen();
  }
  var prod;
  var init_store = __esm({
    "../teampro/teampro/public/js/it_dashboard/store.js"() {
      init_vue_runtime_esm_bundler();
      prod = reactive({
        date: null,
        openTeams: /* @__PURE__ */ new Set(),
        openCbs: /* @__PURE__ */ new Set(),
        allTeams: [],
        allCbs: [],
        allOpen: true,
        filters: { priority: null, sp: null, ro: null, cf: null, ts: null }
      });
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/FilterPills.vue?type=script
  var FilterPills_default;
  var init_FilterPills = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/FilterPills.vue?type=script"() {
      FilterPills_default = {
        __name: "FilterPills",
        props: {
          groups: { type: Array, default: () => [] },
          modelValue: { type: Object, default: () => ({}) }
        },
        emits: ["update:modelValue", "change"],
        setup(__props, { expose: __expose, emit: __emit }) {
          __expose();
          const props = __props;
          const emit2 = __emit;
          function toggle(groupKey, value) {
            const next = __spreadValues({}, props.modelValue);
            next[groupKey] = next[groupKey] === value ? null : value;
            emit2("update:modelValue", next);
            emit2("change", next);
          }
          const __returned__ = { props, emit: emit2, toggle };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/FilterPills.vue?type=template
  function render7(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createElementBlock("div", _hoisted_110, [
      (openBlock(true), createElementBlock(Fragment, null, renderList($props.groups, (g) => {
        return openBlock(), createElementBlock("div", {
          key: g.key,
          class: "itd-pill-group"
        }, [
          createBaseVNode("span", _hoisted_25, toDisplayString(g.label), 1),
          (openBlock(true), createElementBlock(Fragment, null, renderList(g.options, (o) => {
            return openBlock(), createElementBlock("button", {
              key: o.value,
              class: normalizeClass(["itd-pill", { "itd-pill--on": $props.modelValue[g.key] === o.value }]),
              onClick: ($event) => $setup.toggle(g.key, o.value)
            }, toDisplayString(o.label), 11, _hoisted_34);
          }), 128))
        ]);
      }), 128))
    ]);
  }
  var _hoisted_110, _hoisted_25, _hoisted_34;
  var init_FilterPills2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/FilterPills.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_110 = { class: "itd-pills" };
      _hoisted_25 = { class: "itd-pill-label" };
      _hoisted_34 = ["onClick"];
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/FilterPills.vue
  var FilterPills_default2;
  var init_FilterPills3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/FilterPills.vue"() {
      init_FilterPills();
      init_FilterPills2();
      FilterPills_default.render = render7;
      FilterPills_default.__file = "../teampro/teampro/public/js/it_dashboard/components/FilterPills.vue";
      FilterPills_default2 = FilterPills_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/FrappControl.vue?type=script
  var FrappControl_default;
  var init_FrappControl = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/FrappControl.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      FrappControl_default = {
        __name: "FrappControl",
        props: {
          df: { type: Object, required: true },
          modelValue: { type: [String, null], default: "" }
        },
        emits: ["update:modelValue", "change"],
        setup(__props, { expose: __expose, emit: __emit }) {
          const props = __props;
          const emit2 = __emit;
          const el = ref(null);
          let ctrl = null;
          onMounted(() => {
            ctrl = frappe.ui.form.make_control({
              parent: el.value,
              df: __spreadProps(__spreadValues({}, props.df), {
                onchange: () => {
                  const v = ctrl.get_value();
                  emit2("update:modelValue", v);
                  emit2("change", v);
                }
              }),
              render_input: true
            });
            if (props.modelValue)
              ctrl.set_value(props.modelValue);
          });
          watch2(
            () => props.modelValue,
            (v) => {
              if (ctrl && ctrl.get_value() !== v)
                ctrl.set_value(v || "");
            }
          );
          function set_value(v) {
            ctrl && ctrl.set_value(v);
          }
          function get_value() {
            return ctrl ? ctrl.get_value() : "";
          }
          __expose({ set_value, get_value });
          onBeforeUnmount(() => {
            el.value && (el.value.innerHTML = "");
          });
          const __returned__ = { props, emit: emit2, el, get ctrl() {
            return ctrl;
          }, set ctrl(v) {
            ctrl = v;
          }, set_value, get_value, onMounted, onBeforeUnmount, ref, watch: watch2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/FrappControl.vue?type=template
  function render8(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createElementBlock("div", _hoisted_111, null, 512);
  }
  var _hoisted_111;
  var init_FrappControl2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/FrappControl.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_111 = {
        ref: "el",
        class: "itd-ctrl"
      };
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/FrappControl.vue
  var FrappControl_default2;
  var init_FrappControl3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/FrappControl.vue"() {
      init_FrappControl();
      init_FrappControl2();
      FrappControl_default.render = render8;
      FrappControl_default.__file = "../teampro/teampro/public/js/it_dashboard/components/FrappControl.vue";
      FrappControl_default2 = FrappControl_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProductionSummary.vue?type=script
  var ProductionSummary_default;
  var init_ProductionSummary = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProductionSummary.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_store();
      init_SectionCard3();
      init_FilterPills3();
      init_FrappControl3();
      init_SkeletonRows3();
      ProductionSummary_default = {
        __name: "ProductionSummary",
        emits: [],
        setup(__props, { expose: __expose, emit: __emit }) {
          __expose();
          const emit2 = __emit;
          const loading = ref(true);
          const raw = ref({ data: [], team_order: [] });
          const FILTER_GROUPS = [
            {
              key: "priority",
              label: "Priority",
              options: [
                { label: "Low", value: "Low" },
                { label: "Medium", value: "Medium" },
                { label: "High", value: "High" },
                { label: "Urgent", value: "Critical" }
              ]
            },
            {
              key: "sp",
              label: "S/P",
              options: [
                { label: "Spot", value: "S" },
                { label: "Plan", value: "P" }
              ]
            },
            { key: "ro", label: "RO", options: [{ label: "Reopen", value: "RO" }] },
            { key: "cf", label: "CF", options: [{ label: "Carry Forward", value: "CF" }] }
          ];
          async function load() {
            loading.value = true;
            try {
              const args = prod.date ? { from_date: prod.date, to_date: prod.date } : {};
              raw.value = await call("get_today_task_data11", args) || { data: [], team_order: [] };
            } finally {
              loading.value = false;
            }
          }
          const teams = computed2(() => {
            const grouped = {};
            for (const row of raw.value.data || []) {
              if (!row[3])
                continue;
              const team = row[12] || "No Team";
              const cb = row[3];
              ((grouped[team] = grouped[team] || {})[cb] = grouped[team][cb] || []).push(row);
            }
            const order = raw.value.team_order || [];
            const names = order.filter((t) => grouped[t]);
            for (const t of Object.keys(grouped))
              if (!names.includes(t))
                names.push(t);
            return names.map((team) => {
              const cbs = Object.entries(grouped[team]).sort((a, b) => (a[1][0][25] || 0) - (b[1][0][25] || 0)).map(([cb, rs]) => {
                const r = rs[0];
                const aph = +r[24] || 0;
                const rt = +r[14] || 0;
                const ut = +r[13] || 0;
                return {
                  cb,
                  key: cbKey(team, cb),
                  img: r[18],
                  aph,
                  rt,
                  ut,
                  utp: aph > 0 ? ut / aph * 100 : 0
                };
              });
              const t = {
                name: team,
                key: teamKey(team),
                logo: cbs.length ? grouped[team][cbs[0].cb][0][19] : "",
                cbs,
                aph: cbs.reduce((s, c) => s + c.aph, 0),
                rt: cbs.reduce((s, c) => s + c.rt, 0),
                ut: cbs.reduce((s, c) => s + c.ut, 0)
              };
              t.utp = t.aph > 0 ? t.ut / t.aph * 100 : 0;
              return t;
            });
          });
          function onDate(v) {
            prod.date = sysDate(v);
            load();
          }
          function onFilters(v) {
            prod.filters = __spreadProps(__spreadValues({}, v), { priority: v.priority, sp: v.sp, ro: v.ro, cf: v.cf, ts: v.ts });
          }
          onMounted(load);
          const __returned__ = { emit: emit2, loading, raw, FILTER_GROUPS, load, teams, onDate, onFilters, ref, computed: computed2, watch: watch2, onMounted, get call() {
            return call;
          }, get fmt() {
            return fmt;
          }, get sysDate() {
            return sysDate;
          }, get prod() {
            return prod;
          }, get cbKey() {
            return cbKey;
          }, get teamKey() {
            return teamKey;
          }, get toggleProdTeam() {
            return toggleProdTeam;
          }, get toggleProdCb() {
            return toggleProdCb;
          }, get toggleProdAll() {
            return toggleProdAll;
          }, SectionCard: SectionCard_default2, FilterPills: FilterPills_default2, FrappControl: FrappControl_default2, SkeletonRows: SkeletonRows_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProductionSummary.vue?type=template
  function render9(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["SectionCard"], { title: "Production Summary" }, {
      actions: withCtx(() => [
        createBaseVNode("button", {
          class: "itd-textbtn",
          onClick: _cache[0] || (_cache[0] = ($event) => $setup.toggleProdAll(!$setup.prod.allOpen))
        }, toDisplayString($setup.prod.allOpen ? "\u2212 All" : "+ All"), 1),
        createVNode($setup["FilterPills"], {
          groups: $setup.FILTER_GROUPS,
          modelValue: $setup.prod.filters,
          "onUpdate:modelValue": _cache[1] || (_cache[1] = ($event) => $setup.prod.filters = $event),
          onChange: $setup.onFilters
        }, null, 8, ["modelValue"]),
        createVNode($setup["FrappControl"], {
          df: { fieldtype: "Date", fieldname: "prod_date", placeholder: "Select date" },
          modelValue: $setup.prod.date,
          "onUpdate:modelValue": $setup.onDate
        }, null, 8, ["modelValue"])
      ]),
      default: withCtx(() => [
        $setup.loading ? (openBlock(), createBlock($setup["SkeletonRows"], {
          key: 0,
          rows: 2,
          cols: 3
        })) : !$setup.teams.length ? (openBlock(), createElementBlock("div", _hoisted_112, "No production data")) : (openBlock(), createElementBlock("div", _hoisted_26, [
          (openBlock(true), createElementBlock(Fragment, null, renderList($setup.teams, (t) => {
            return openBlock(), createElementBlock("div", {
              key: t.key,
              class: "itd-teamcard"
            }, [
              createBaseVNode("header", {
                class: "itd-teamcard-head",
                onClick: ($event) => $setup.toggleProdTeam(t.name)
              }, [
                t.logo ? (openBlock(), createElementBlock("img", {
                  key: 0,
                  src: t.logo,
                  class: "itd-teamcard-logo",
                  alt: ""
                }, null, 8, _hoisted_44)) : createCommentVNode("v-if", true),
                createBaseVNode("span", _hoisted_54, toDisplayString(t.name), 1),
                createBaseVNode("span", _hoisted_63, [
                  createTextVNode(" APH "),
                  createBaseVNode("b", _hoisted_73, toDisplayString($setup.fmt(t.aph)), 1),
                  createTextVNode(" \xB7 RT "),
                  createBaseVNode("b", _hoisted_83, toDisplayString($setup.fmt(t.rt)), 1),
                  createTextVNode(" \xB7 UT "),
                  createBaseVNode("b", _hoisted_93, toDisplayString($setup.fmt(t.ut)), 1),
                  createTextVNode(" \xB7 UT% "),
                  createBaseVNode("b", null, toDisplayString(t.utp.toFixed(1)) + "%", 1)
                ])
              ], 8, _hoisted_35),
              createBaseVNode("div", _hoisted_102, [
                (openBlock(true), createElementBlock(Fragment, null, renderList(t.cbs, (m) => {
                  return openBlock(), createElementBlock("button", {
                    key: m.key,
                    class: "itd-member",
                    title: m.cb,
                    onClick: ($event) => $setup.toggleProdCb(m.key)
                  }, [
                    m.img ? (openBlock(), createElementBlock("img", {
                      key: 0,
                      src: m.img,
                      class: "itd-avatar",
                      alt: ""
                    }, null, 8, _hoisted_123)) : (openBlock(), createElementBlock("span", _hoisted_133, toDisplayString(m.cb), 1)),
                    createBaseVNode("span", _hoisted_143, toDisplayString(m.cb), 1),
                    createBaseVNode("span", _hoisted_152, [
                      createBaseVNode("span", null, [
                        createBaseVNode("i", _hoisted_162, toDisplayString($setup.fmt(m.aph)), 1),
                        createTextVNode(" / "),
                        createBaseVNode("i", _hoisted_172, toDisplayString($setup.fmt(m.rt)), 1)
                      ]),
                      createBaseVNode("span", null, [
                        createBaseVNode("i", _hoisted_182, toDisplayString($setup.fmt(m.ut)), 1),
                        createTextVNode(" / "),
                        createBaseVNode("i", null, toDisplayString(m.utp.toFixed(1)) + "%", 1)
                      ])
                    ])
                  ], 8, _hoisted_113);
                }), 128))
              ])
            ]);
          }), 128))
        ]))
      ]),
      _: 1
    });
  }
  var _hoisted_112, _hoisted_26, _hoisted_35, _hoisted_44, _hoisted_54, _hoisted_63, _hoisted_73, _hoisted_83, _hoisted_93, _hoisted_102, _hoisted_113, _hoisted_123, _hoisted_133, _hoisted_143, _hoisted_152, _hoisted_162, _hoisted_172, _hoisted_182;
  var init_ProductionSummary2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProductionSummary.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_112 = {
        key: 1,
        class: "itd-empty"
      };
      _hoisted_26 = {
        key: 2,
        class: "itd-teamgrid"
      };
      _hoisted_35 = ["onClick"];
      _hoisted_44 = ["src"];
      _hoisted_54 = { class: "itd-teamcard-name" };
      _hoisted_63 = { class: "itd-teamcard-metrics" };
      _hoisted_73 = { class: "c-green" };
      _hoisted_83 = { class: "c-blue" };
      _hoisted_93 = { class: "c-red" };
      _hoisted_102 = { class: "itd-teamcard-body" };
      _hoisted_113 = ["title", "onClick"];
      _hoisted_123 = ["src"];
      _hoisted_133 = {
        key: 1,
        class: "itd-avatar itd-avatar--fallback"
      };
      _hoisted_143 = { class: "itd-member-name" };
      _hoisted_152 = { class: "itd-member-metrics" };
      _hoisted_162 = { class: "c-green" };
      _hoisted_172 = { class: "c-blue" };
      _hoisted_182 = { class: "c-red" };
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/ProductionSummary.vue
  var ProductionSummary_default2;
  var init_ProductionSummary3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/ProductionSummary.vue"() {
      init_ProductionSummary();
      init_ProductionSummary2();
      ProductionSummary_default.render = render9;
      ProductionSummary_default.__file = "../teampro/teampro/public/js/it_dashboard/components/ProductionSummary.vue";
      ProductionSummary_default2 = ProductionSummary_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProductionTable.vue?type=script
  var ProductionTable_default;
  var init_ProductionTable = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProductionTable.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_store();
      init_icons();
      init_SectionCard3();
      init_SkeletonRows3();
      ProductionTable_default = {
        __name: "ProductionTable",
        setup(__props, { expose: __expose }) {
          const loading = ref(true);
          const raw = ref({ data: [], team_order: [] });
          const confirmBusy = ref({});
          async function load() {
            loading.value = true;
            try {
              const args = prod.date ? { from_date: prod.date, to_date: prod.date } : {};
              raw.value = await call("get_today_task_data1", args) || { data: [], team_order: [] };
              const t = [], c = [];
              for (const row of raw.value.data || []) {
                t.push(row[12] || "No Team");
                c.push(cbKey(row[12], row[3]));
              }
              setProdData([...new Set(t)], [...new Set(c)]);
            } finally {
              loading.value = false;
            }
          }
          const groups = computed2(() => {
            const byTeam = {};
            for (const row of raw.value.data || []) {
              const team = row[12] || "No Team";
              const cb = row[3] || "\u2014";
              ((byTeam[team] = byTeam[team] || {})[cb] = byTeam[team][cb] || []).push(row);
            }
            const order = raw.value.team_order || [];
            const names = order.filter((t) => byTeam[t]);
            for (const t of Object.keys(byTeam))
              if (!names.includes(t))
                names.push(t);
            return names.map((team) => {
              var _a;
              const cbs = Object.entries(byTeam[team]).sort((a, b) => (a[1][0][25] || 0) - (b[1][0][25] || 0)).map(([cb, tasks]) => ({ cb, key: cbKey(team, cb), tasks }));
              return { team, key: teamKey(team), logo: ((_a = cbs[0]) == null ? void 0 : _a.tasks[0][19]) || "", cbs };
            });
          });
          function passesFilters(row) {
            const f = prod.filters;
            if (f.priority && String(row[8] || "").toLowerCase() !== f.priority.toLowerCase())
              return false;
            if (f.sp && (row[21] == 1 ? "S" : "P") !== f.sp)
              return false;
            if (f.ro && !(parseInt(row[22]) > 0))
              return false;
            if (f.cf && !(parseInt(row[23]) > 0))
              return false;
            if (f.ts) {
              const p2 = progress(row);
              const band = p2 > 100 ? "red" : p2 > 75 ? "orange" : p2 > 0 ? "blue" : "";
              if (band !== f.ts)
                return false;
            }
            return true;
          }
          function progress(row) {
            const at = +row[13] || 0;
            const rt = +row[14] || 0;
            return rt > 0 ? Math.round(at / rt * 100) : 0;
          }
          function progressColor(p2) {
            return p2 > 100 ? "var(--itd-red)" : p2 > 75 ? "var(--itd-amber)" : "var(--itd-teal)";
          }
          const STATUS_LETTER = {
            Working: "W",
            "Pending Review": "PR",
            "Client Review": "CR",
            Completed: "\u2713"
          };
          function isOpen(team, cbkey) {
            return prod.openTeams.has(team) && prod.openCbs.has(cbkey);
          }
          const toggleAll = () => toggleProdAll(!prod.allOpen);
          const toggleTeam = (team) => toggleProdTeam(team);
          const toggleCb = (team, cb) => toggleProdCb(cbKey(team, cb));
          function sum(tasks, idx) {
            return tasks.reduce((s, r) => s + (+r[idx] || 0), 0);
          }
          function taskStatus(row) {
            return (row[10] || "").trim();
          }
          async function confirmTask(row) {
            const task = row[0];
            confirmBusy.value[task] = true;
            try {
              await callRaw("frappe.client.set_value", {
                doctype: "Task",
                name: task,
                fieldname: "is_confirmed",
                value: 1
              });
              row[20] = 1;
              frappe.show_alert({ message: "Task Confirmed", indicator: "green" });
            } finally {
              confirmBusy.value[task] = false;
            }
          }
          async function unconfirmTask(row) {
            const task = row[0];
            confirmBusy.value[task] = true;
            try {
              const running = await call("check_running_timesheet", { task });
              if (running) {
                frappe.msgprint({
                  title: "Not Allowed",
                  message: "This task is already running in a timesheet.",
                  indicator: "red"
                });
                return;
              }
              await callRaw("frappe.client.set_value", {
                doctype: "Task",
                name: task,
                fieldname: "is_confirmed",
                value: 0
              });
              row[20] = 0;
              frappe.show_alert({ message: "Task Unconfirmed", indicator: "orange" });
            } finally {
              confirmBusy.value[task] = false;
            }
          }
          async function showTaskInfo(task) {
            var _a, _b, _c, _d, _e, _f;
            const t = await callRaw("frappe.client.get", { doctype: "Task", name: task });
            if (!t)
              return;
            const row = (k, v) => `<tr><td class="tdl">${k}</td><td class="tdv">${v != null ? v : ""}</td></tr>`;
            const html = `
		<table class="itd-dialog-table">
			${row("Task", t.name)}${row("Project", t.project || "")}
			${row("Subject", t.subject || "")}${row("Description", t.description || "")}
			${row("ET", (_a = t.expected_time) != null ? _a : "")}${row("RT", (_b = t.rt) != null ? _b : "")}${row("AT", (_c = t.actual_time) != null ? _c : "")}
			${row("CF", (_d = t.custom_production_date_count) != null ? _d : "")}${row("RO", (_e = t.revisions) != null ? _e : "")}
			${row("Created On", t.creation ? frappe.datetime.str_to_user(t.creation) : "")}
			${row("Allocated On", t.custom_allocated_on ? frappe.datetime.str_to_user(t.custom_allocated_on) : "")}
			${row("Age", (_f = t.custom_age) != null ? _f : "")}
			${row("Developer Note", t.custom_developer_note || "")}
			${row("Remarks", t.custom_taskissue_action_taken || "")}
		</table>`;
            const d = new frappe.ui.Dialog({
              title: `Task Details \u2014 ${t.name}`,
              fields: [{ fieldtype: "HTML", fieldname: "d", options: html }]
            });
            d.show();
            d.$wrapper.find(".modal-dialog").css({ "max-width": "900px", width: "90%" });
          }
          function exportExcel() {
            var _a;
            if (!((_a = raw.value.data) == null ? void 0 : _a.length))
              return frappe.msgprint("No data available");
            const rows = [
              ["Sl No", "Sprint", "Project", "Task", "Subject", "S/P", "RO", "CF", "ET", "AT", "RT", "Priority", "Status"]
            ];
            let i = 1;
            for (const t of groups.value)
              for (const c of t.cbs)
                for (const r of c.tasks) {
                  if (!passesFilters(r))
                    continue;
                  rows.push([
                    i++,
                    r[15],
                    r[1],
                    r[0],
                    r[2],
                    r[21] == 1 ? "S" : "P",
                    r[22] || 0,
                    r[23] || 0,
                    +r[5] || 0,
                    +r[7] || 0,
                    +r[14] || 0,
                    r[8] || "",
                    taskStatus(r)
                  ]);
                }
            downloadRowsAsXlsx(`Production_Tasks_${frappe.datetime.now_date()}.xlsx`, "Production", rows);
          }
          watch2(() => prod.date, load);
          onMounted(load);
          __expose({ reload: load, toggleTeam, toggleCb });
          const __returned__ = { loading, raw, confirmBusy, load, groups, passesFilters, progress, progressColor, STATUS_LETTER, isOpen, toggleAll, toggleTeam, toggleCb, sum, taskStatus, confirmTask, unconfirmTask, showTaskInfo, exportExcel, ref, computed: computed2, watch: watch2, onMounted, get call() {
            return call;
          }, get callRaw() {
            return callRaw;
          }, get fmt() {
            return fmt;
          }, get downloadRowsAsXlsx() {
            return downloadRowsAsXlsx;
          }, get prod() {
            return prod;
          }, get cbKey() {
            return cbKey;
          }, get teamKey() {
            return teamKey;
          }, get setProdData() {
            return setProdData;
          }, get toggleProdAll() {
            return toggleProdAll;
          }, get toggleProdTeam() {
            return toggleProdTeam;
          }, get toggleProdCb() {
            return toggleProdCb;
          }, get Icon() {
            return Icon;
          }, SectionCard: SectionCard_default2, SkeletonRows: SkeletonRows_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProductionTable.vue?type=template
  function render10(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["SectionCard"], {
      title: "Production Table",
      class: "itd-prodtable"
    }, {
      actions: withCtx(() => [
        createBaseVNode("button", {
          class: "itd-textbtn",
          onClick: $setup.toggleAll
        }, toDisplayString($setup.prod.allOpen ? "\u2212 All" : "+ All"), 1),
        createBaseVNode("button", {
          class: "itd-iconbtn",
          title: "Download Excel",
          onClick: $setup.exportExcel
        }, [
          createVNode($setup["Icon"], {
            name: "download",
            size: 15
          })
        ])
      ]),
      default: withCtx(() => {
        var _a;
        return [
          $setup.loading ? (openBlock(), createBlock($setup["SkeletonRows"], {
            key: 0,
            rows: 10,
            cols: 12
          })) : !((_a = $setup.raw.data) == null ? void 0 : _a.length) ? (openBlock(), createElementBlock("div", _hoisted_114, "No production tasks for this date")) : (openBlock(), createElementBlock("div", _hoisted_27, [
            createBaseVNode("table", _hoisted_36, [
              _hoisted_45,
              (openBlock(true), createElementBlock(Fragment, null, renderList($setup.groups, (t) => {
                return openBlock(), createElementBlock("tbody", {
                  key: t.key
                }, [
                  createCommentVNode(" Team header "),
                  createBaseVNode("tr", _hoisted_55, [
                    createBaseVNode("td", null, [
                      t.logo ? (openBlock(), createElementBlock("img", {
                        key: 0,
                        src: t.logo,
                        class: "itd-teamlogo",
                        alt: ""
                      }, null, 8, _hoisted_64)) : createCommentVNode("v-if", true)
                    ]),
                    createBaseVNode("td", _hoisted_74, [
                      createBaseVNode("div", _hoisted_84, [
                        createBaseVNode("button", {
                          class: "itd-mini",
                          onClick: ($event) => $setup.toggleTeam(t.team)
                        }, toDisplayString($setup.prod.openTeams.has(t.team) ? "\u2212" : "+") + " All ", 9, _hoisted_94),
                        createBaseVNode("span", _hoisted_103, toDisplayString(t.team), 1),
                        (openBlock(true), createElementBlock(Fragment, null, renderList(t.cbs, (c) => {
                          return openBlock(), createElementBlock("button", {
                            key: c.key,
                            class: normalizeClass(["itd-cbchip", { "itd-cbchip--off": !$setup.prod.openCbs.has(c.key) }]),
                            title: c.cb,
                            onClick: ($event) => $setup.toggleCb(t.team, c.cb)
                          }, [
                            c.tasks[0][18] ? (openBlock(), createElementBlock("img", {
                              key: 0,
                              src: c.tasks[0][18],
                              class: "itd-avatar itd-avatar--sm",
                              alt: ""
                            }, null, 8, _hoisted_124)) : (openBlock(), createElementBlock("span", _hoisted_134, toDisplayString(c.cb), 1))
                          ], 10, _hoisted_115);
                        }), 128))
                      ])
                    ]),
                    createBaseVNode("td", _hoisted_144, [
                      createBaseVNode("b", null, toDisplayString($setup.fmt(t.cbs.reduce((s, c) => s + $setup.sum(c.tasks, 5), 0))), 1)
                    ]),
                    createBaseVNode("td", _hoisted_153, [
                      createBaseVNode("b", null, toDisplayString($setup.fmt(t.cbs.reduce((s, c) => s + $setup.sum(c.tasks, 7), 0))), 1)
                    ]),
                    createBaseVNode("td", _hoisted_163, [
                      createBaseVNode("b", null, toDisplayString($setup.fmt(t.cbs.reduce((s, c) => s + $setup.sum(c.tasks, 14), 0))), 1)
                    ]),
                    _hoisted_173
                  ]),
                  (openBlock(true), createElementBlock(Fragment, null, renderList(t.cbs, (c) => {
                    return openBlock(), createElementBlock(Fragment, {
                      key: c.key
                    }, [
                      createCommentVNode(" CB header "),
                      $setup.prod.openTeams.has(t.team) ? (openBlock(), createElementBlock("tr", {
                        key: 0,
                        class: "itd-row-cb",
                        onClick: ($event) => $setup.toggleCb(t.team, c.cb)
                      }, [
                        createBaseVNode("td", _hoisted_192, [
                          createVNode($setup["Icon"], {
                            name: $setup.prod.openCbs.has(c.key) ? "chevron-down" : "chevron-right",
                            size: 14
                          }, null, 8, ["name"])
                        ]),
                        createBaseVNode("td", _hoisted_20, toDisplayString(c.tasks[0][24] || c.cb), 1),
                        createBaseVNode("td", _hoisted_21, [
                          createBaseVNode("b", null, toDisplayString($setup.fmt($setup.sum(c.tasks, 5))), 1)
                        ]),
                        createBaseVNode("td", _hoisted_222, [
                          createBaseVNode("b", null, toDisplayString($setup.fmt($setup.sum(c.tasks, 7))), 1)
                        ]),
                        createBaseVNode("td", _hoisted_232, [
                          createBaseVNode("b", null, toDisplayString($setup.fmt($setup.sum(c.tasks, 14))), 1)
                        ]),
                        _hoisted_242
                      ], 8, _hoisted_183)) : createCommentVNode("v-if", true),
                      createCommentVNode(" Task rows "),
                      (openBlock(true), createElementBlock(Fragment, null, renderList(c.tasks, (r, ri) => {
                        return openBlock(), createElementBlock(Fragment, {
                          key: r[0] + "-" + ri
                        }, [
                          $setup.isOpen(t.team, c.key) && $setup.passesFilters(r) ? (openBlock(), createElementBlock("tr", _hoisted_252, [
                            createBaseVNode("td", _hoisted_262, toDisplayString(ri + 1), 1),
                            createBaseVNode("td", null, toDisplayString(r[15]), 1),
                            createBaseVNode("td", _hoisted_272, [
                              createBaseVNode("a", {
                                href: `/app/project/${encodeURIComponent(r[1])}`,
                                target: "_blank",
                                class: "itd-link"
                              }, toDisplayString(r[1]), 9, _hoisted_28)
                            ]),
                            createBaseVNode("td", null, [
                              createBaseVNode("span", _hoisted_29, [
                                createBaseVNode("button", {
                                  class: "itd-iconbtn itd-iconbtn--xs",
                                  title: "Task details",
                                  onClick: ($event) => $setup.showTaskInfo(r[0])
                                }, [
                                  createVNode($setup["Icon"], {
                                    name: "eye",
                                    size: 13
                                  })
                                ], 8, _hoisted_30),
                                createBaseVNode("a", {
                                  href: `/app/task/${encodeURIComponent(r[0])}`,
                                  target: "_blank",
                                  class: "itd-link"
                                }, toDisplayString(r[0]), 9, _hoisted_31)
                              ])
                            ]),
                            createBaseVNode("td", _hoisted_322, toDisplayString(r[2]), 1),
                            createBaseVNode("td", null, [
                              createBaseVNode("span", {
                                class: normalizeClass(["itd-tag", r[21] == 1 ? "itd-tag--spot" : "itd-tag--plan"])
                              }, toDisplayString(r[21] == 1 ? "S" : "P"), 3)
                            ]),
                            createBaseVNode("td", null, toDisplayString(r[22] || 0), 1),
                            createBaseVNode("td", null, toDisplayString(r[23] || 0), 1),
                            createBaseVNode("td", _hoisted_332, toDisplayString($setup.fmt(r[5])), 1),
                            createBaseVNode("td", _hoisted_342, toDisplayString($setup.fmt(r[7])), 1),
                            createBaseVNode("td", _hoisted_352, toDisplayString($setup.fmt(r[14])), 1),
                            createBaseVNode("td", null, [
                              r[8] ? (openBlock(), createElementBlock("span", {
                                key: 0,
                                class: normalizeClass(["itd-prio", "itd-prio--" + String(r[8]).toLowerCase()])
                              }, toDisplayString(r[8]), 3)) : createCommentVNode("v-if", true)
                            ]),
                            createBaseVNode("td", null, [
                              r[20] == 0 ? (openBlock(), createElementBlock("button", {
                                key: 0,
                                class: "itd-statusicon itd-statusicon--confirm",
                                disabled: $setup.confirmBusy[r[0]],
                                title: "Confirm task",
                                onClick: ($event) => $setup.confirmTask(r)
                              }, [
                                createVNode($setup["Icon"], {
                                  name: "check",
                                  size: 13
                                })
                              ], 8, _hoisted_362)) : (+r[13] || 0) > 0 ? (openBlock(), createElementBlock("div", {
                                key: 1,
                                class: "itd-prog",
                                title: `AT ${$setup.fmt(r[13])} / RT ${$setup.fmt(r[14])}`
                              }, [
                                createBaseVNode("div", _hoisted_38, [
                                  createBaseVNode("div", {
                                    class: "itd-prog-fill",
                                    style: normalizeStyle({ width: Math.min($setup.progress(r), 100) + "%", background: $setup.progressColor($setup.progress(r)) })
                                  }, null, 4)
                                ]),
                                createBaseVNode("span", _hoisted_39, toDisplayString($setup.STATUS_LETTER[$setup.taskStatus(r)] || "") + " " + toDisplayString($setup.progress(r)) + "%", 1)
                              ], 8, _hoisted_37)) : (openBlock(), createElementBlock("button", {
                                key: 2,
                                class: "itd-statusicon itd-statusicon--unconfirm",
                                disabled: $setup.confirmBusy[r[0]],
                                title: "Unconfirm task",
                                onClick: ($event) => $setup.unconfirmTask(r)
                              }, " C ", 8, _hoisted_40))
                            ])
                          ])) : createCommentVNode("v-if", true)
                        ], 64);
                      }), 128))
                    ], 64);
                  }), 128))
                ]);
              }), 128))
            ])
          ]))
        ];
      }),
      _: 1
    });
  }
  var _hoisted_114, _hoisted_27, _hoisted_36, _hoisted_45, _hoisted_55, _hoisted_64, _hoisted_74, _hoisted_84, _hoisted_94, _hoisted_103, _hoisted_115, _hoisted_124, _hoisted_134, _hoisted_144, _hoisted_153, _hoisted_163, _hoisted_173, _hoisted_183, _hoisted_192, _hoisted_20, _hoisted_21, _hoisted_222, _hoisted_232, _hoisted_242, _hoisted_252, _hoisted_262, _hoisted_272, _hoisted_28, _hoisted_29, _hoisted_30, _hoisted_31, _hoisted_322, _hoisted_332, _hoisted_342, _hoisted_352, _hoisted_362, _hoisted_37, _hoisted_38, _hoisted_39, _hoisted_40;
  var init_ProductionTable2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProductionTable.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_114 = {
        key: 1,
        class: "itd-empty"
      };
      _hoisted_27 = {
        key: 2,
        class: "itd-table-wrap"
      };
      _hoisted_36 = { class: "itd-table itd-table--fixed" };
      _hoisted_45 = /* @__PURE__ */ createBaseVNode("thead", null, [
        /* @__PURE__ */ createBaseVNode("tr", null, [
          /* @__PURE__ */ createBaseVNode("th", { style: { "width": "44px" } }, "#"),
          /* @__PURE__ */ createBaseVNode("th", { style: { "width": "88px" } }, "Sprint"),
          /* @__PURE__ */ createBaseVNode("th", {
            class: "itd-left",
            style: { "width": "170px" }
          }, "Project"),
          /* @__PURE__ */ createBaseVNode("th", { style: { "width": "120px" } }, "Task"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-left" }, "Subject"),
          /* @__PURE__ */ createBaseVNode("th", { title: "Spot / Plan" }, "S/P"),
          /* @__PURE__ */ createBaseVNode("th", { title: "Reopen count" }, "RO"),
          /* @__PURE__ */ createBaseVNode("th", { title: "Carry-forward count" }, "CF"),
          /* @__PURE__ */ createBaseVNode("th", {
            class: "itd-num",
            title: "Estimated time (hrs)"
          }, "ET"),
          /* @__PURE__ */ createBaseVNode("th", {
            class: "itd-num",
            title: "Actual time (hrs)"
          }, "AT"),
          /* @__PURE__ */ createBaseVNode("th", {
            class: "itd-num",
            title: "Remaining today (hrs)"
          }, "RT"),
          /* @__PURE__ */ createBaseVNode("th", null, "Priority"),
          /* @__PURE__ */ createBaseVNode("th", { style: { "width": "150px" } }, "Status")
        ])
      ], -1);
      _hoisted_55 = { class: "itd-row-team" };
      _hoisted_64 = ["src"];
      _hoisted_74 = {
        colspan: "7",
        class: "itd-left"
      };
      _hoisted_84 = { class: "itd-teamrow" };
      _hoisted_94 = ["onClick"];
      _hoisted_103 = { class: "itd-teamrow-name" };
      _hoisted_115 = ["title", "onClick"];
      _hoisted_124 = ["src"];
      _hoisted_134 = {
        key: 1,
        class: "itd-avatar itd-avatar--sm itd-avatar--fallback"
      };
      _hoisted_144 = { class: "itd-num" };
      _hoisted_153 = { class: "itd-num" };
      _hoisted_163 = { class: "itd-num" };
      _hoisted_173 = /* @__PURE__ */ createBaseVNode("td", { colspan: "2" }, null, -1);
      _hoisted_183 = ["onClick"];
      _hoisted_192 = { class: "itd-chev" };
      _hoisted_20 = {
        colspan: "7",
        class: "itd-left"
      };
      _hoisted_21 = { class: "itd-num" };
      _hoisted_222 = { class: "itd-num" };
      _hoisted_232 = { class: "itd-num" };
      _hoisted_242 = /* @__PURE__ */ createBaseVNode("td", { colspan: "2" }, null, -1);
      _hoisted_252 = {
        key: 0,
        class: "itd-row-task"
      };
      _hoisted_262 = { class: "itd-muted" };
      _hoisted_272 = { class: "itd-left" };
      _hoisted_28 = ["href"];
      _hoisted_29 = { class: "itd-taskcell" };
      _hoisted_30 = ["onClick"];
      _hoisted_31 = ["href"];
      _hoisted_322 = { class: "itd-left" };
      _hoisted_332 = { class: "itd-num itd-mono" };
      _hoisted_342 = { class: "itd-num itd-mono" };
      _hoisted_352 = { class: "itd-num itd-mono" };
      _hoisted_362 = ["disabled", "onClick"];
      _hoisted_37 = ["title"];
      _hoisted_38 = { class: "itd-prog-track" };
      _hoisted_39 = { class: "itd-prog-label" };
      _hoisted_40 = ["disabled", "onClick"];
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/ProductionTable.vue
  var ProductionTable_default2;
  var init_ProductionTable3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/ProductionTable.vue"() {
      init_ProductionTable();
      init_ProductionTable2();
      ProductionTable_default.render = render10;
      ProductionTable_default.__file = "../teampro/teampro/public/js/it_dashboard/components/ProductionTable.vue";
      ProductionTable_default2 = ProductionTable_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/NonAllocated.vue?type=script
  var NonAllocated_default;
  var init_NonAllocated = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/NonAllocated.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_icons();
      init_SectionCard3();
      init_SkeletonRows3();
      NonAllocated_default = {
        __name: "NonAllocated",
        setup(__props, { expose: __expose }) {
          __expose();
          const loading = ref(true);
          const data = ref([]);
          const view = ref("overall");
          const kt = ref("");
          const openProjects = ref(/* @__PURE__ */ new Set());
          async function load() {
            loading.value = true;
            try {
              const r = await call("get_non_allocated_tasks_test", {
                view: view.value,
                kt_confirmed: kt.value
              });
              data.value = (r == null ? void 0 : r.data) || [];
              openProjects.value = /* @__PURE__ */ new Set();
            } finally {
              loading.value = false;
            }
          }
          const groups = computed2(() => {
            const g = {};
            for (const t of data.value) {
              const p2 = t.project || "No Project";
              (g[p2] = g[p2] || []).push(t);
            }
            return Object.keys(g).sort().map((project) => {
              const tasks = g[project];
              return {
                project,
                tasks,
                et: tasks.reduce((s, t) => s + (+t.expected_time || 0), 0),
                rt: tasks.reduce((s, t) => s + (+t.rt || 0), 0),
                at: tasks.reduce((s, t) => s + (+t.actual_time || 0), 0)
              };
            });
          });
          const grand = computed2(() => ({
            et: groups.value.reduce((s, g) => s + g.et, 0),
            rt: groups.value.reduce((s, g) => s + g.rt, 0),
            at: groups.value.reduce((s, g) => s + g.at, 0)
          }));
          const allOpen = computed2(
            () => groups.value.length > 0 && openProjects.value.size === groups.value.length
          );
          function toggleAll() {
            openProjects.value = allOpen.value ? /* @__PURE__ */ new Set() : new Set(groups.value.map((g) => g.project));
          }
          function toggle(p2) {
            const s = new Set(openProjects.value);
            s.has(p2) ? s.delete(p2) : s.add(p2);
            openProjects.value = s;
          }
          function setView(v) {
            view.value = v;
            load();
          }
          function onKt(e) {
            kt.value = e.target.value;
            load();
          }
          function download() {
            if (!data.value.length)
              return frappe.msgprint("No data available to download");
            const rows = [["Project", "CB", "Sprint", "Task", "Subject", "ET", "RT", "AT", "AGE", "CF", "Priority", "Status"]];
            for (const g of groups.value)
              for (const t of g.tasks)
                rows.push([
                  g.project,
                  t.cb || "",
                  t.custom_sprint || "",
                  t.name || "",
                  t.subject || "",
                  +t.expected_time || 0,
                  +t.rt || 0,
                  +t.actual_time || 0,
                  t.custom_age || "",
                  t.custom_production_date_count || "",
                  t.priority || "",
                  t.status || ""
                ]);
            rows.push(["GRAND TOTAL", "", "", "", "", +grand.value.et.toFixed(2), +grand.value.rt.toFixed(2), +grand.value.at.toFixed(2), "", "", "", ""]);
            downloadRowsAsXlsx("NonAllocatedTasks.xlsx", "Non Allocated Tasks", rows);
          }
          onMounted(load);
          const __returned__ = { loading, data, view, kt, openProjects, load, groups, grand, allOpen, toggleAll, toggle, setView, onKt, download, ref, computed: computed2, onMounted, get call() {
            return call;
          }, get fmt() {
            return fmt;
          }, get downloadRowsAsXlsx() {
            return downloadRowsAsXlsx;
          }, get Icon() {
            return Icon;
          }, SectionCard: SectionCard_default2, SkeletonRows: SkeletonRows_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/NonAllocated.vue?type=template
  function render11(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["SectionCard"], { title: "Non-Allocated Total" }, {
      actions: withCtx(() => [
        createBaseVNode("div", _hoisted_116, [
          createBaseVNode("button", {
            class: normalizeClass(["itd-seg-btn", { "itd-seg-btn--on": $setup.view === "overall" }]),
            onClick: _cache[0] || (_cache[0] = ($event) => $setup.setView("overall"))
          }, " Overall ", 2),
          createBaseVNode("button", {
            class: normalizeClass(["itd-seg-btn", { "itd-seg-btn--on": $setup.view === "sprint" }]),
            onClick: _cache[1] || (_cache[1] = ($event) => $setup.setView("sprint"))
          }, " NA ", 2)
        ]),
        createBaseVNode("select", {
          class: "itd-select",
          onChange: $setup.onKt,
          value: $setup.kt,
          title: "KT Confirmed"
        }, [..._hoisted_65], 40, _hoisted_210),
        createBaseVNode("button", {
          class: "itd-iconbtn",
          title: "Download Excel",
          onClick: $setup.download
        }, [
          createVNode($setup["Icon"], {
            name: "download",
            size: 15
          })
        ])
      ]),
      default: withCtx(() => [
        $setup.loading ? (openBlock(), createBlock($setup["SkeletonRows"], {
          key: 0,
          rows: 6,
          cols: 10
        })) : !$setup.groups.length ? (openBlock(), createElementBlock("div", _hoisted_75, "No tasks found")) : (openBlock(), createElementBlock("div", _hoisted_85, [
          createBaseVNode("table", _hoisted_95, [
            createBaseVNode("thead", null, [
              createBaseVNode("tr", null, [
                createBaseVNode("th", {
                  class: "itd-left itd-th-toggle",
                  onClick: $setup.toggleAll
                }, toDisplayString($setup.allOpen ? "\u2212 All" : "+ All"), 1),
                _hoisted_104,
                _hoisted_117,
                _hoisted_125,
                _hoisted_135,
                _hoisted_145,
                _hoisted_154,
                _hoisted_164,
                _hoisted_174,
                _hoisted_184,
                _hoisted_193
              ])
            ]),
            (openBlock(true), createElementBlock(Fragment, null, renderList($setup.groups, (g) => {
              return openBlock(), createElementBlock("tbody", {
                key: g.project
              }, [
                createBaseVNode("tr", {
                  class: "itd-row-group",
                  onClick: ($event) => $setup.toggle(g.project)
                }, [
                  createBaseVNode("td", _hoisted_212, [
                    createVNode($setup["Icon"], {
                      name: $setup.openProjects.has(g.project) ? "chevron-down" : "chevron-right",
                      size: 13
                    }, null, 8, ["name"]),
                    createTextVNode(" " + toDisplayString(g.project), 1)
                  ]),
                  createBaseVNode("td", _hoisted_223, [
                    createBaseVNode("b", null, toDisplayString($setup.fmt(g.et)), 1)
                  ]),
                  createBaseVNode("td", _hoisted_233, [
                    createBaseVNode("b", null, toDisplayString($setup.fmt(g.rt)), 1)
                  ]),
                  createBaseVNode("td", _hoisted_243, [
                    createBaseVNode("b", null, toDisplayString($setup.fmt(g.at)), 1)
                  ]),
                  _hoisted_253
                ], 8, _hoisted_202),
                $setup.openProjects.has(g.project) ? (openBlock(true), createElementBlock(Fragment, { key: 0 }, renderList(g.tasks, (t) => {
                  return openBlock(), createElementBlock("tr", {
                    key: t.name,
                    class: normalizeClass({ "itd-row-alert": (+t.custom_age || 0) > 3 })
                  }, [
                    createBaseVNode("td", _hoisted_263, toDisplayString(t.cb || ""), 1),
                    createBaseVNode("td", null, toDisplayString(t.custom_sprint || ""), 1),
                    createBaseVNode("td", null, [
                      createBaseVNode("a", {
                        href: `/app/task/${encodeURIComponent(t.name)}`,
                        target: "_blank",
                        class: "itd-link"
                      }, toDisplayString(t.name), 9, _hoisted_273)
                    ]),
                    createBaseVNode("td", _hoisted_282, toDisplayString(t.subject || ""), 1),
                    createBaseVNode("td", _hoisted_292, toDisplayString($setup.fmt(t.expected_time)), 1),
                    createBaseVNode("td", _hoisted_302, toDisplayString($setup.fmt(t.rt)), 1),
                    createBaseVNode("td", _hoisted_312, toDisplayString($setup.fmt(t.actual_time)), 1),
                    createBaseVNode("td", _hoisted_323, toDisplayString(t.custom_age || ""), 1),
                    createBaseVNode("td", _hoisted_333, toDisplayString(t.custom_production_date_count || ""), 1),
                    createBaseVNode("td", null, [
                      t.priority ? (openBlock(), createElementBlock("span", {
                        key: 0,
                        class: normalizeClass(["itd-prio", "itd-prio--" + String(t.priority).toLowerCase()])
                      }, toDisplayString(t.priority), 3)) : createCommentVNode("v-if", true)
                    ]),
                    createBaseVNode("td", null, toDisplayString(t.status || ""), 1)
                  ], 2);
                }), 128)) : createCommentVNode("v-if", true)
              ]);
            }), 128)),
            createBaseVNode("tfoot", null, [
              createBaseVNode("tr", null, [
                _hoisted_343,
                createBaseVNode("td", _hoisted_353, toDisplayString($setup.fmt($setup.grand.et)), 1),
                createBaseVNode("td", _hoisted_363, toDisplayString($setup.fmt($setup.grand.rt)), 1),
                createBaseVNode("td", _hoisted_372, toDisplayString($setup.fmt($setup.grand.at)), 1),
                _hoisted_382
              ])
            ])
          ])
        ]))
      ]),
      _: 1
    });
  }
  var _hoisted_116, _hoisted_210, _hoisted_310, _hoisted_46, _hoisted_56, _hoisted_65, _hoisted_75, _hoisted_85, _hoisted_95, _hoisted_104, _hoisted_117, _hoisted_125, _hoisted_135, _hoisted_145, _hoisted_154, _hoisted_164, _hoisted_174, _hoisted_184, _hoisted_193, _hoisted_202, _hoisted_212, _hoisted_223, _hoisted_233, _hoisted_243, _hoisted_253, _hoisted_263, _hoisted_273, _hoisted_282, _hoisted_292, _hoisted_302, _hoisted_312, _hoisted_323, _hoisted_333, _hoisted_343, _hoisted_353, _hoisted_363, _hoisted_372, _hoisted_382;
  var init_NonAllocated2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/NonAllocated.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_116 = { class: "itd-seg" };
      _hoisted_210 = ["value"];
      _hoisted_310 = /* @__PURE__ */ createBaseVNode("option", { value: "" }, "KT Confirm", -1);
      _hoisted_46 = /* @__PURE__ */ createBaseVNode("option", { value: "Yes" }, "Yes", -1);
      _hoisted_56 = /* @__PURE__ */ createBaseVNode("option", { value: "No" }, "No", -1);
      _hoisted_65 = [
        _hoisted_310,
        _hoisted_46,
        _hoisted_56
      ];
      _hoisted_75 = {
        key: 1,
        class: "itd-empty"
      };
      _hoisted_85 = {
        key: 2,
        class: "itd-table-wrap itd-na-scroll"
      };
      _hoisted_95 = { class: "itd-table" };
      _hoisted_104 = /* @__PURE__ */ createBaseVNode("th", null, "Sprint", -1);
      _hoisted_117 = /* @__PURE__ */ createBaseVNode("th", null, "Task", -1);
      _hoisted_125 = /* @__PURE__ */ createBaseVNode("th", { class: "itd-left" }, "Subject", -1);
      _hoisted_135 = /* @__PURE__ */ createBaseVNode("th", {
        class: "itd-num",
        title: "Estimated time (hrs)"
      }, "ET", -1);
      _hoisted_145 = /* @__PURE__ */ createBaseVNode("th", {
        class: "itd-num",
        title: "Remaining time (hrs)"
      }, "RT", -1);
      _hoisted_154 = /* @__PURE__ */ createBaseVNode("th", {
        class: "itd-num",
        title: "Actual time (hrs)"
      }, "AT", -1);
      _hoisted_164 = /* @__PURE__ */ createBaseVNode("th", {
        class: "itd-num",
        title: "Age (days)"
      }, "Age", -1);
      _hoisted_174 = /* @__PURE__ */ createBaseVNode("th", {
        class: "itd-num",
        title: "Carry-forward count"
      }, "CF", -1);
      _hoisted_184 = /* @__PURE__ */ createBaseVNode("th", null, "Priority", -1);
      _hoisted_193 = /* @__PURE__ */ createBaseVNode("th", null, "Status", -1);
      _hoisted_202 = ["onClick"];
      _hoisted_212 = {
        colspan: "4",
        class: "itd-left"
      };
      _hoisted_223 = { class: "itd-num" };
      _hoisted_233 = { class: "itd-num" };
      _hoisted_243 = { class: "itd-num" };
      _hoisted_253 = /* @__PURE__ */ createBaseVNode("td", { colspan: "4" }, null, -1);
      _hoisted_263 = { class: "itd-muted" };
      _hoisted_273 = ["href"];
      _hoisted_282 = { class: "itd-left" };
      _hoisted_292 = { class: "itd-num itd-mono" };
      _hoisted_302 = { class: "itd-num itd-mono" };
      _hoisted_312 = { class: "itd-num itd-mono" };
      _hoisted_323 = { class: "itd-num" };
      _hoisted_333 = { class: "itd-num" };
      _hoisted_343 = /* @__PURE__ */ createBaseVNode("td", { colspan: "4" }, "Grand Total", -1);
      _hoisted_353 = { class: "itd-num" };
      _hoisted_363 = { class: "itd-num" };
      _hoisted_372 = { class: "itd-num" };
      _hoisted_382 = /* @__PURE__ */ createBaseVNode("td", { colspan: "4" }, null, -1);
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/NonAllocated.vue
  var NonAllocated_default2;
  var init_NonAllocated3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/NonAllocated.vue"() {
      init_NonAllocated();
      init_NonAllocated2();
      NonAllocated_default.render = render11;
      NonAllocated_default.__file = "../teampro/teampro/public/js/it_dashboard/components/NonAllocated.vue";
      NonAllocated_default2 = NonAllocated_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/HtmlSection.vue?type=script
  var HtmlSection_default;
  var init_HtmlSection = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/HtmlSection.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_SectionCard3();
      init_SkeletonRows3();
      HtmlSection_default = {
        __name: "HtmlSection",
        props: {
          title: String,
          method: { type: String, required: true },
          args: { type: Object, default: () => ({}) },
          reloadKey: { type: [String, Number], default: 0 },
          maxHeight: { type: String, default: "640px" }
        },
        emits: ["loaded"],
        setup(__props, { expose: __expose, emit: __emit }) {
          __expose();
          const props = __props;
          const emit2 = __emit;
          const html = ref("");
          const loading = ref(true);
          async function load() {
            loading.value = true;
            try {
              html.value = cleanHtml(await call(props.method, props.args));
            } finally {
              loading.value = false;
            }
            emit2("loaded");
          }
          watch2(() => [props.args, props.reloadKey], load, { deep: true });
          onMounted(load);
          const __returned__ = { props, emit: emit2, html, loading, load, ref, watch: watch2, onMounted, get call() {
            return call;
          }, get cleanHtml() {
            return cleanHtml;
          }, SectionCard: SectionCard_default2, SkeletonRows: SkeletonRows_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/HtmlSection.vue?type=template
  function render12(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["SectionCard"], { title: $props.title }, {
      actions: withCtx(() => [
        renderSlot(_ctx.$slots, "actions")
      ]),
      default: withCtx(() => [
        $setup.loading ? (openBlock(), createBlock($setup["SkeletonRows"], {
          key: 0,
          rows: 8,
          cols: 8
        })) : !$setup.html ? (openBlock(), createElementBlock("div", _hoisted_118, "No data found")) : (openBlock(), createElementBlock("div", {
          key: 2,
          class: "itd-html",
          style: normalizeStyle({ "--itd-html-maxh": $props.maxHeight }),
          innerHTML: $setup.html
        }, null, 12, _hoisted_211))
      ]),
      _: 3
    }, 8, ["title"]);
  }
  var _hoisted_118, _hoisted_211;
  var init_HtmlSection2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/HtmlSection.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_118 = {
        key: 1,
        class: "itd-empty"
      };
      _hoisted_211 = ["innerHTML"];
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/HtmlSection.vue
  var HtmlSection_default2;
  var init_HtmlSection3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/HtmlSection.vue"() {
      init_HtmlSection();
      init_HtmlSection2();
      HtmlSection_default.render = render12;
      HtmlSection_default.__file = "../teampro/teampro/public/js/it_dashboard/components/HtmlSection.vue";
      HtmlSection_default2 = HtmlSection_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/DsrDpr.vue?type=script
  var DsrDpr_default;
  var init_DsrDpr = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/DsrDpr.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_icons();
      init_FrappControl3();
      init_HtmlSection3();
      DsrDpr_default = {
        __name: "DsrDpr",
        setup(__props, { expose: __expose }) {
          __expose();
          const date = ref(today());
          const args = computed2(() => ({ date: sysDate(date.value) || today() }));
          function download() {
            const d = sysDate(date.value) || frappe.datetime.add_days(frappe.datetime.get_today(), -1);
            const NS2 = "/api/method/teampro.teampro.page.new_it_dashboard.new_it.";
            downloadUrl(`${NS2}download_dsr_excel?date=${d}`);
            setTimeout(() => downloadUrl(`${NS2}download_dpr_excel?date=${d}`), 1500);
          }
          const __returned__ = { date, args, download, ref, computed: computed2, get today() {
            return today;
          }, get sysDate() {
            return sysDate;
          }, get downloadUrl() {
            return downloadUrl;
          }, get Icon() {
            return Icon;
          }, FrappControl: FrappControl_default2, HtmlSection: HtmlSection_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/DsrDpr.vue?type=template
  function render13(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createElementBlock(Fragment, null, [
      createVNode($setup["HtmlSection"], {
        title: "DSR Summary",
        method: "dsr_table",
        args: $setup.args,
        "max-height": "520px"
      }, {
        actions: withCtx(() => [
          createVNode($setup["FrappControl"], {
            df: { fieldtype: "Date", fieldname: "dsr_date", placeholder: "Select Date" },
            modelValue: $setup.date,
            "onUpdate:modelValue": _cache[0] || (_cache[0] = ($event) => $setup.date = $event)
          }, null, 8, ["modelValue"]),
          createBaseVNode("button", {
            class: "itd-iconbtn",
            title: "Download DSR + DPR Excel",
            onClick: $setup.download
          }, [
            createVNode($setup["Icon"], {
              name: "download",
              size: 15
            })
          ])
        ]),
        _: 1
      }, 8, ["args"]),
      createVNode($setup["HtmlSection"], {
        title: "DPR Summary",
        method: "dpr_table",
        args: $setup.args,
        "max-height": "520px"
      }, null, 8, ["args"]),
      createVNode($setup["HtmlSection"], {
        title: "AMC Project SLA",
        method: "get_amc_project_sla_table",
        "max-height": "520px"
      }, {
        actions: withCtx(() => [
          createBaseVNode("button", {
            class: "itd-iconbtn",
            title: "Download Excel",
            onClick: _cache[1] || (_cache[1] = ($event) => $setup.downloadUrl("/api/method/teampro.teampro.page.new_it_dashboard.new_it.download_amc_project_sla_excel"))
          }, [
            createVNode($setup["Icon"], {
              name: "download",
              size: 15
            })
          ])
        ]),
        _: 1
      })
    ], 64);
  }
  var init_DsrDpr2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/DsrDpr.vue?type=template"() {
      init_vue_runtime_esm_bundler();
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/DsrDpr.vue
  var DsrDpr_default2;
  var init_DsrDpr3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/DsrDpr.vue"() {
      init_DsrDpr();
      init_DsrDpr2();
      DsrDpr_default.render = render13;
      DsrDpr_default.__file = "../teampro/teampro/public/js/it_dashboard/components/DsrDpr.vue";
      DsrDpr_default2 = DsrDpr_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/RetroSummary.vue?type=script
  var RetroSummary_default;
  var init_RetroSummary = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/RetroSummary.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_SectionCard3();
      init_FrappControl3();
      init_SkeletonRows3();
      RetroSummary_default = {
        __name: "RetroSummary",
        setup(__props, { expose: __expose }) {
          __expose();
          const loading = ref(true);
          const html = ref("");
          const sections = ref([]);
          const sprint = ref("");
          const team = ref("Summary");
          const mode = ref("hrs");
          const devTeams = ref([]);
          const sprintCtrl = ref(null);
          async function load() {
            loading.value = true;
            html.value = "";
            sections.value = [];
            try {
              if (team.value === "Summary") {
                html.value = cleanHtml(await call("summary_total_hrs_cols", { name: sprint.value }));
              } else {
                const d = await call("get_retro_summary_html", {
                  name: sprint.value,
                  dev_team: team.value === "ALL" ? "" : team.value
                });
                sections.value = (d || []).map((s) => __spreadProps(__spreadValues({}, s), { html: cleanHtml(s.html) }));
              }
            } finally {
              loading.value = false;
            }
          }
          function pickTeam(t) {
            team.value = t;
            load();
          }
          function onSprint(v) {
            sprint.value = v;
            load();
          }
          onMounted(async () => {
            const def2 = await call("update_sprint_filter");
            if (def2 && sprintCtrl.value)
              sprintCtrl.value.set_value(def2);
            devTeams.value = await frappe.db.get_list("Dev Team", {
              filters: { name: ["!=", "Others"] },
              fields: ["name"],
              order_by: "name"
            }) || [];
            await load();
          });
          const __returned__ = { loading, html, sections, sprint, team, mode, devTeams, sprintCtrl, load, pickTeam, onSprint, ref, onMounted, get call() {
            return call;
          }, get cleanHtml() {
            return cleanHtml;
          }, SectionCard: SectionCard_default2, FrappControl: FrappControl_default2, SkeletonRows: SkeletonRows_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/RetroSummary.vue?type=template
  function render14(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["SectionCard"], {
      title: "Sprint Retrospective",
      class: "itd-retro"
    }, {
      actions: withCtx(() => [
        createVNode($setup["FrappControl"], {
          ref: "sprintCtrl",
          df: { fieldtype: "Link", fieldname: "retro_sprint", options: "Task Sprint", placeholder: "Sprint" },
          onChange: $setup.onSprint
        }, null, 512),
        createBaseVNode("div", _hoisted_119, [
          (openBlock(true), createElementBlock(Fragment, null, renderList(["Summary", "ALL", ...$setup.devTeams.map((d) => d.name)], (t) => {
            return openBlock(), createElementBlock("button", {
              key: t,
              class: normalizeClass(["itd-pill", { "itd-pill--on": $setup.team === t }]),
              onClick: ($event) => $setup.pickTeam(t)
            }, toDisplayString(t), 11, _hoisted_213);
          }), 128))
        ]),
        createBaseVNode("div", _hoisted_311, [
          createBaseVNode("button", {
            class: normalizeClass(["itd-seg-btn", { "itd-seg-btn--on": $setup.mode === "hrs" }]),
            onClick: _cache[0] || (_cache[0] = ($event) => $setup.mode = "hrs")
          }, " Hrs ", 2),
          createBaseVNode("button", {
            class: normalizeClass(["itd-seg-btn", { "itd-seg-btn--on": $setup.mode === "count" }]),
            onClick: _cache[1] || (_cache[1] = ($event) => $setup.mode = "count")
          }, " Count ", 2)
        ])
      ]),
      default: withCtx(() => [
        $setup.loading ? (openBlock(), createBlock($setup["SkeletonRows"], {
          key: 0,
          rows: 8,
          cols: 10
        })) : (openBlock(), createElementBlock(Fragment, { key: 1 }, [
          $setup.html ? (openBlock(), createElementBlock("div", {
            key: 0,
            class: normalizeClass(["itd-html itd-retro-html", $setup.mode === "hrs" ? "itd-html--hrs" : "itd-html--count"]),
            innerHTML: $setup.html
          }, null, 10, _hoisted_47)) : $setup.sections.length ? (openBlock(true), createElementBlock(Fragment, { key: 1 }, renderList($setup.sections, (s) => {
            return openBlock(), createElementBlock("div", {
              key: s.team,
              class: "itd-retro-team"
            }, [
              createBaseVNode("h4", _hoisted_57, toDisplayString(s.team), 1),
              createBaseVNode("div", {
                class: normalizeClass(["itd-html itd-retro-html", $setup.mode === "hrs" ? "itd-html--hrs" : "itd-html--count"]),
                innerHTML: s.html
              }, null, 10, _hoisted_66)
            ]);
          }), 128)) : (openBlock(), createElementBlock("div", _hoisted_76, " No data found" + toDisplayString($setup.team !== "Summary" ? ` for ${$setup.team}` : "") + " in this sprint ", 1))
        ], 64))
      ]),
      _: 1
    });
  }
  var _hoisted_119, _hoisted_213, _hoisted_311, _hoisted_47, _hoisted_57, _hoisted_66, _hoisted_76;
  var init_RetroSummary2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/RetroSummary.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_119 = { class: "itd-pills itd-pills--scroll" };
      _hoisted_213 = ["onClick"];
      _hoisted_311 = { class: "itd-seg" };
      _hoisted_47 = ["innerHTML"];
      _hoisted_57 = { class: "itd-retro-teamname" };
      _hoisted_66 = ["innerHTML"];
      _hoisted_76 = {
        key: 2,
        class: "itd-empty"
      };
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/RetroSummary.vue
  var RetroSummary_default2;
  var init_RetroSummary3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/RetroSummary.vue"() {
      init_RetroSummary();
      init_RetroSummary2();
      RetroSummary_default.render = render14;
      RetroSummary_default.__file = "../teampro/teampro/public/js/it_dashboard/components/RetroSummary.vue";
      RetroSummary_default2 = RetroSummary_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SprintProgress.vue?type=script
  var SprintProgress_default;
  var init_SprintProgress = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SprintProgress.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_SectionCard3();
      init_SkeletonRows3();
      SprintProgress_default = {
        __name: "SprintProgress",
        props: {
          team: { type: String, default: "" },
          sprint: { type: String, default: "" }
        },
        setup(__props, { expose: __expose }) {
          __expose();
          const props = __props;
          const loading = ref(true);
          const message = ref(null);
          async function load() {
            loading.value = true;
            try {
              message.value = await call("get_sprint_chart_data", {
                team: props.team || "",
                sprint: props.sprint || ""
              });
            } finally {
              loading.value = false;
            }
          }
          const blocks = computed2(() => {
            var _a;
            const m = message.value;
            if (!((_a = m == null ? void 0 : m.labels) == null ? void 0 : _a.length))
              return [];
            const order = [];
            const map2 = {};
            m.labels.forEach((sc, i) => {
              var _a2, _b, _c, _d, _e;
              const team = ((_a2 = m.teams) == null ? void 0 : _a2[i]) || "Unassigned";
              if (!map2[team]) {
                map2[team] = { team, sprintId: ((_b = m.sprint_ids) == null ? void 0 : _b[i]) || "", cbs: [] };
                order.push(team);
              }
              const aph = parseFloat(((_c = m.available_hours) == null ? void 0 : _c[i]) || 0);
              const e = parseFloat(((_d = m.expected_hours) == null ? void 0 : _d[i]) || 0);
              const rv = parseFloat(((_e = m.sprint_avl_time) == null ? void 0 : _e[i]) || 0);
              map2[team].cbs.push({
                sc,
                aph,
                e,
                rv,
                rtPct: aph ? rv / aph * 100 : 0,
                lsPct: aph ? e / aph * 100 : 0,
                balance: aph - rv
              });
            });
            return order.map((t) => map2[t]);
          });
          function dotColor(c) {
            const ratio = c.aph ? c.rv / c.aph : 0;
            return ratio >= 0.9 ? "#4caf50" : ratio >= 0.5 ? "#ff9800" : "#f44336";
          }
          watch2(() => [props.team, props.sprint], load);
          onMounted(load);
          const __returned__ = { props, loading, message, load, blocks, dotColor, ref, computed: computed2, watch: watch2, onMounted, get call() {
            return call;
          }, get fmt() {
            return fmt;
          }, SectionCard: SectionCard_default2, SkeletonRows: SkeletonRows_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SprintProgress.vue?type=template
  function render15(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["SectionCard"], { title: "Sprint Progress" }, {
      default: withCtx(() => [
        $setup.loading ? (openBlock(), createBlock($setup["SkeletonRows"], {
          key: 0,
          rows: 4,
          cols: 4
        })) : !$setup.blocks.length ? (openBlock(), createElementBlock("div", _hoisted_120, " No Sprint Data Found for Today ")) : (openBlock(), createElementBlock("div", _hoisted_214, [
          _hoisted_313,
          (openBlock(true), createElementBlock(Fragment, null, renderList($setup.blocks, (b) => {
            return openBlock(), createElementBlock("div", {
              key: b.team,
              class: "itd-sp-team"
            }, [
              createBaseVNode("div", _hoisted_48, [
                createBaseVNode("h4", null, toDisplayString(b.team), 1),
                createBaseVNode("span", _hoisted_58, toDisplayString(b.sprintId || "\u2014"), 1)
              ]),
              createBaseVNode("div", _hoisted_67, [
                (openBlock(true), createElementBlock(Fragment, null, renderList(b.cbs, (c) => {
                  return openBlock(), createElementBlock("div", {
                    key: c.sc,
                    class: "itd-sp-card"
                  }, [
                    createBaseVNode("div", _hoisted_77, [
                      createBaseVNode("span", _hoisted_86, toDisplayString(c.sc), 1),
                      createBaseVNode("span", {
                        class: "itd-sp-dot",
                        style: normalizeStyle({ background: $setup.dotColor(c) })
                      }, null, 4)
                    ]),
                    createBaseVNode("div", _hoisted_96, [
                      createBaseVNode("span", _hoisted_105, [
                        createTextVNode(toDisplayString($setup.fmt(c.aph, 1)), 1),
                        _hoisted_1110
                      ]),
                      createBaseVNode("div", _hoisted_126, [
                        createBaseVNode("div", {
                          class: "itd-sp-fill",
                          style: normalizeStyle({ width: Math.min(Math.max(c.rtPct, 0), 100) + "%" })
                        }, [
                          c.rtPct >= 15 ? (openBlock(), createElementBlock("span", _hoisted_136, "RT " + toDisplayString(c.rtPct.toFixed(0)) + "%", 1)) : createCommentVNode("v-if", true)
                        ], 4),
                        createBaseVNode("div", {
                          class: "itd-sp-marker",
                          style: normalizeStyle({ left: Math.min(Math.max(c.lsPct, 0), 100) + "%" })
                        }, [
                          _hoisted_146,
                          createBaseVNode("div", _hoisted_155, "L " + toDisplayString($setup.fmt(c.e, 1)) + "h", 1)
                        ], 4)
                      ]),
                      createBaseVNode("span", _hoisted_165, [
                        createTextVNode(toDisplayString($setup.fmt(c.rv, 1)), 1),
                        _hoisted_175
                      ])
                    ]),
                    createBaseVNode("div", _hoisted_185, [
                      createBaseVNode("span", null, [
                        createTextVNode("RT / APH "),
                        createBaseVNode("b", null, toDisplayString(c.rtPct.toFixed(1)) + "%", 1)
                      ]),
                      createBaseVNode("span", null, [
                        createTextVNode("Lifespan "),
                        createBaseVNode("b", null, toDisplayString(c.lsPct.toFixed(1)) + "%", 1)
                      ]),
                      createBaseVNode("span", null, [
                        createTextVNode("Balance "),
                        createBaseVNode("b", null, toDisplayString($setup.fmt(c.balance, 1)) + "h", 1)
                      ])
                    ])
                  ]);
                }), 128))
              ])
            ]);
          }), 128))
        ]))
      ]),
      _: 1
    });
  }
  var _hoisted_120, _hoisted_214, _hoisted_313, _hoisted_48, _hoisted_58, _hoisted_67, _hoisted_77, _hoisted_86, _hoisted_96, _hoisted_105, _hoisted_1110, _hoisted_126, _hoisted_136, _hoisted_146, _hoisted_155, _hoisted_165, _hoisted_175, _hoisted_185;
  var init_SprintProgress2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SprintProgress.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_120 = {
        key: 1,
        class: "itd-empty itd-empty--warn"
      };
      _hoisted_214 = {
        key: 2,
        class: "itd-sprintprog"
      };
      _hoisted_313 = /* @__PURE__ */ createBaseVNode("div", { class: "itd-legend" }, [
        /* @__PURE__ */ createBaseVNode("span", { class: "itd-legend-item" }, [
          /* @__PURE__ */ createBaseVNode("i", { class: "itd-legend-dot itd-legend-dot--track" }),
          /* @__PURE__ */ createTextVNode(" APH (full track) ")
        ]),
        /* @__PURE__ */ createBaseVNode("span", { class: "itd-legend-item" }, [
          /* @__PURE__ */ createBaseVNode("i", { class: "itd-legend-dot itd-legend-dot--fill" }),
          /* @__PURE__ */ createTextVNode(" RT (filled portion) ")
        ]),
        /* @__PURE__ */ createBaseVNode("span", { class: "itd-legend-item" }, [
          /* @__PURE__ */ createBaseVNode("i", { class: "itd-legend-dot itd-legend-dot--marker" }),
          /* @__PURE__ */ createTextVNode(" Lifespan (marker) ")
        ])
      ], -1);
      _hoisted_48 = { class: "itd-sp-teamhead" };
      _hoisted_58 = { class: "itd-tag" };
      _hoisted_67 = { class: "itd-sp-grid" };
      _hoisted_77 = { class: "itd-sp-cardhead" };
      _hoisted_86 = { class: "itd-sp-cb" };
      _hoisted_96 = { class: "itd-sp-bar" };
      _hoisted_105 = { class: "itd-sp-aph" };
      _hoisted_1110 = /* @__PURE__ */ createBaseVNode("em", null, "APH", -1);
      _hoisted_126 = { class: "itd-sp-track" };
      _hoisted_136 = {
        key: 0,
        class: "itd-sp-fillpct"
      };
      _hoisted_146 = /* @__PURE__ */ createBaseVNode("div", { class: "itd-sp-markerline" }, null, -1);
      _hoisted_155 = { class: "itd-sp-markerflag" };
      _hoisted_165 = { class: "itd-sp-rt" };
      _hoisted_175 = /* @__PURE__ */ createBaseVNode("em", null, "RT", -1);
      _hoisted_185 = { class: "itd-sp-stats" };
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/SprintProgress.vue
  var SprintProgress_default2;
  var init_SprintProgress3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/SprintProgress.vue"() {
      init_SprintProgress();
      init_SprintProgress2();
      SprintProgress_default.render = render15;
      SprintProgress_default.__file = "../teampro/teampro/public/js/it_dashboard/components/SprintProgress.vue";
      SprintProgress_default2 = SprintProgress_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SprintOverall.vue?type=script
  var SprintOverall_default;
  var init_SprintOverall = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SprintOverall.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_icons();
      init_SectionCard3();
      init_SkeletonRows3();
      SprintOverall_default = {
        __name: "SprintOverall",
        props: {
          team: { type: String, default: "" },
          sprint: { type: String, default: "" }
        },
        setup(__props, { expose: __expose }) {
          __expose();
          const props = __props;
          const loading = ref(true);
          const teams = ref([]);
          const open = ref(/* @__PURE__ */ new Set());
          async function load() {
            loading.value = true;
            try {
              const r = await call("get_sprint_teamwise_summary", {
                team: props.team || "",
                sprint: props.sprint || ""
              });
              teams.value = (r == null ? void 0 : r.teams) || [];
              open.value = /* @__PURE__ */ new Set();
            } finally {
              loading.value = false;
            }
          }
          const COLS = [
            "aph",
            "planned_rt",
            "comp_rt",
            "work_rt",
            "nt_rt",
            "spot_rt",
            "spot_comp_rt",
            "spot_work_rt",
            "spot_nt_rt",
            "total_rt",
            "at",
            "completed_rt",
            "completed_at",
            "working_rt",
            "working_at",
            "total_nt_hours",
            "biometric_hrs",
            "nc_rt",
            "reopen_rt",
            "de_rt"
          ];
          const grand = computed2(() => {
            const g = Object.fromEntries(COLS.map((c) => [c, 0]));
            for (const t of teams.value) {
              const tot = t.totals || {};
              for (const c of COLS)
                g[c] += +tot[c] || 0;
            }
            return g;
          });
          const prod2 = (r) => r.aph ? r.completed_rt / r.aph * 100 : 0;
          const eff = (r) => r.completed_rt ? r.completed_at / r.completed_rt * 100 : 0;
          function toggle(i) {
            const s = new Set(open.value);
            s.has(i) ? s.delete(i) : s.add(i);
            open.value = s;
          }
          watch2(() => [props.team, props.sprint], load);
          onMounted(load);
          const __returned__ = { props, loading, teams, open, load, COLS, grand, prod: prod2, eff, toggle, ref, computed: computed2, watch: watch2, onMounted, get call() {
            return call;
          }, get fmt() {
            return fmt;
          }, get Icon() {
            return Icon;
          }, SectionCard: SectionCard_default2, SkeletonRows: SkeletonRows_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SprintOverall.vue?type=template
  function render16(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["SectionCard"], {
      title: "Overall Team Summary",
      subtitle: "Sprint"
    }, {
      default: withCtx(() => [
        $setup.loading ? (openBlock(), createBlock($setup["SkeletonRows"], {
          key: 0,
          rows: 6,
          cols: 12
        })) : !$setup.teams.length ? (openBlock(), createElementBlock("div", _hoisted_121, " No Sprint Data Found for Today ")) : (openBlock(), createElementBlock("div", _hoisted_215, [
          createBaseVNode("table", _hoisted_314, [
            _hoisted_49,
            (openBlock(true), createElementBlock(Fragment, null, renderList($setup.teams, (t, i) => {
              var _a, _b, _c, _d, _e, _f, _g, _h, _i, _j, _k, _l, _m, _n, _o, _p, _q, _r, _s, _t;
              return openBlock(), createElementBlock("tbody", {
                key: t.team
              }, [
                createBaseVNode("tr", {
                  class: "itd-row-group",
                  onClick: ($event) => $setup.toggle(i)
                }, [
                  createBaseVNode("td", _hoisted_68, [
                    createVNode($setup["Icon"], {
                      name: $setup.open.has(i) ? "chevron-down" : "chevron-right",
                      size: 13
                    }, null, 8, ["name"])
                  ]),
                  createBaseVNode("td", null, toDisplayString(i + 1), 1),
                  createBaseVNode("td", _hoisted_78, [
                    createBaseVNode("b", null, toDisplayString(t.team), 1)
                  ]),
                  createBaseVNode("td", null, toDisplayString(t.sprint_id || "\u2014"), 1),
                  createBaseVNode("td", _hoisted_87, toDisplayString($setup.fmt((_a = t.totals) == null ? void 0 : _a.aph)), 1),
                  createBaseVNode("td", _hoisted_97, toDisplayString($setup.fmt((_b = t.totals) == null ? void 0 : _b.planned_rt)), 1),
                  createBaseVNode("td", _hoisted_106, toDisplayString($setup.fmt((_c = t.totals) == null ? void 0 : _c.comp_rt)), 1),
                  createBaseVNode("td", _hoisted_1111, toDisplayString($setup.fmt((_d = t.totals) == null ? void 0 : _d.work_rt)), 1),
                  createBaseVNode("td", _hoisted_127, toDisplayString($setup.fmt((_e = t.totals) == null ? void 0 : _e.nt_rt)), 1),
                  createBaseVNode("td", _hoisted_137, toDisplayString($setup.fmt((_f = t.totals) == null ? void 0 : _f.spot_rt)), 1),
                  createBaseVNode("td", _hoisted_147, toDisplayString($setup.fmt((_g = t.totals) == null ? void 0 : _g.spot_comp_rt)), 1),
                  createBaseVNode("td", _hoisted_156, toDisplayString($setup.fmt((_h = t.totals) == null ? void 0 : _h.spot_work_rt)), 1),
                  createBaseVNode("td", _hoisted_166, toDisplayString($setup.fmt((_i = t.totals) == null ? void 0 : _i.spot_nt_rt)), 1),
                  createBaseVNode("td", _hoisted_176, [
                    createBaseVNode("b", null, toDisplayString($setup.fmt((_j = t.totals) == null ? void 0 : _j.total_rt)), 1)
                  ]),
                  createBaseVNode("td", _hoisted_186, toDisplayString($setup.fmt((_k = t.totals) == null ? void 0 : _k.at)), 1),
                  createBaseVNode("td", _hoisted_194, toDisplayString($setup.fmt((_l = t.totals) == null ? void 0 : _l.completed_rt)), 1),
                  createBaseVNode("td", _hoisted_203, toDisplayString($setup.fmt((_m = t.totals) == null ? void 0 : _m.completed_at)), 1),
                  createBaseVNode("td", _hoisted_216, toDisplayString($setup.fmt((_n = t.totals) == null ? void 0 : _n.working_rt)), 1),
                  createBaseVNode("td", _hoisted_224, toDisplayString($setup.fmt((_o = t.totals) == null ? void 0 : _o.working_at)), 1),
                  createBaseVNode("td", _hoisted_234, toDisplayString($setup.fmt((_p = t.totals) == null ? void 0 : _p.total_nt_hours)), 1),
                  createBaseVNode("td", _hoisted_244, toDisplayString($setup.fmt($setup.prod(t.totals || {}))) + "%", 1),
                  createBaseVNode("td", _hoisted_254, toDisplayString($setup.fmt($setup.eff(t.totals || {}))) + "%", 1),
                  createBaseVNode("td", _hoisted_264, toDisplayString($setup.fmt((_q = t.totals) == null ? void 0 : _q.biometric_hrs)), 1),
                  createBaseVNode("td", _hoisted_274, toDisplayString($setup.fmt((_r = t.totals) == null ? void 0 : _r.nc_rt)), 1),
                  createBaseVNode("td", _hoisted_283, toDisplayString($setup.fmt((_s = t.totals) == null ? void 0 : _s.reopen_rt)), 1),
                  createBaseVNode("td", _hoisted_293, toDisplayString($setup.fmt((_t = t.totals) == null ? void 0 : _t.de_rt)), 1)
                ], 8, _hoisted_59),
                (openBlock(true), createElementBlock(Fragment, null, renderList(t.cbs || [], (c) => {
                  return withDirectives((openBlock(), createElementBlock("tr", {
                    key: t.team + c.cb,
                    class: "itd-row-detail"
                  }, [
                    _hoisted_303,
                    _hoisted_315,
                    createBaseVNode("td", _hoisted_324, toDisplayString(c.cb), 1),
                    _hoisted_334,
                    createBaseVNode("td", _hoisted_344, toDisplayString($setup.fmt(c.aph)), 1),
                    createBaseVNode("td", _hoisted_354, toDisplayString($setup.fmt(c.planned_rt)), 1),
                    createBaseVNode("td", _hoisted_364, toDisplayString($setup.fmt(c.comp_rt)), 1),
                    createBaseVNode("td", _hoisted_373, toDisplayString($setup.fmt(c.work_rt)), 1),
                    createBaseVNode("td", _hoisted_383, toDisplayString($setup.fmt(c.nt_rt)), 1),
                    createBaseVNode("td", _hoisted_392, toDisplayString($setup.fmt(c.spot_rt)), 1),
                    createBaseVNode("td", _hoisted_402, toDisplayString($setup.fmt(c.spot_comp_rt)), 1),
                    createBaseVNode("td", _hoisted_41, toDisplayString($setup.fmt(c.spot_work_rt)), 1),
                    createBaseVNode("td", _hoisted_422, toDisplayString($setup.fmt(c.spot_nt_rt)), 1),
                    createBaseVNode("td", _hoisted_432, toDisplayString($setup.fmt(c.total_rt)), 1),
                    createBaseVNode("td", _hoisted_442, toDisplayString($setup.fmt(c.at)), 1),
                    createBaseVNode("td", _hoisted_452, toDisplayString($setup.fmt(c.completed_rt)), 1),
                    createBaseVNode("td", _hoisted_462, toDisplayString($setup.fmt(c.completed_at)), 1),
                    createBaseVNode("td", _hoisted_472, toDisplayString($setup.fmt(c.working_rt)), 1),
                    createBaseVNode("td", _hoisted_482, toDisplayString($setup.fmt(c.working_at)), 1),
                    createBaseVNode("td", _hoisted_492, toDisplayString($setup.fmt(c.total_nt_hours)), 1),
                    createBaseVNode("td", _hoisted_50, toDisplayString($setup.fmt($setup.prod(c))) + "%", 1),
                    createBaseVNode("td", _hoisted_51, toDisplayString($setup.fmt($setup.eff(c))) + "%", 1),
                    createBaseVNode("td", _hoisted_522, toDisplayString($setup.fmt(c.biometric_hrs)), 1),
                    createBaseVNode("td", _hoisted_532, toDisplayString($setup.fmt(c.nc_rt)), 1),
                    createBaseVNode("td", _hoisted_542, toDisplayString($setup.fmt(c.reopen_rt)), 1),
                    createBaseVNode("td", _hoisted_552, toDisplayString($setup.fmt(c.de_rt)), 1)
                  ])), [
                    [vShow, $setup.open.has(i)]
                  ]);
                }), 128))
              ]);
            }), 128)),
            createBaseVNode("tfoot", null, [
              createBaseVNode("tr", null, [
                _hoisted_562,
                createBaseVNode("td", _hoisted_572, toDisplayString($setup.fmt($setup.grand.aph)), 1),
                createBaseVNode("td", _hoisted_582, toDisplayString($setup.fmt($setup.grand.planned_rt)), 1),
                createBaseVNode("td", _hoisted_592, toDisplayString($setup.fmt($setup.grand.comp_rt)), 1),
                createBaseVNode("td", _hoisted_60, toDisplayString($setup.fmt($setup.grand.work_rt)), 1),
                createBaseVNode("td", _hoisted_61, toDisplayString($setup.fmt($setup.grand.nt_rt)), 1),
                createBaseVNode("td", _hoisted_622, toDisplayString($setup.fmt($setup.grand.spot_rt)), 1),
                createBaseVNode("td", _hoisted_632, toDisplayString($setup.fmt($setup.grand.spot_comp_rt)), 1),
                createBaseVNode("td", _hoisted_642, toDisplayString($setup.fmt($setup.grand.spot_work_rt)), 1),
                createBaseVNode("td", _hoisted_652, toDisplayString($setup.fmt($setup.grand.spot_nt_rt)), 1),
                createBaseVNode("td", _hoisted_662, toDisplayString($setup.fmt($setup.grand.total_rt)), 1),
                createBaseVNode("td", _hoisted_672, toDisplayString($setup.fmt($setup.grand.at)), 1),
                createBaseVNode("td", _hoisted_682, toDisplayString($setup.fmt($setup.grand.completed_rt)), 1),
                createBaseVNode("td", _hoisted_69, toDisplayString($setup.fmt($setup.grand.completed_at)), 1),
                createBaseVNode("td", _hoisted_70, toDisplayString($setup.fmt($setup.grand.working_rt)), 1),
                createBaseVNode("td", _hoisted_71, toDisplayString($setup.fmt($setup.grand.working_at)), 1),
                createBaseVNode("td", _hoisted_722, toDisplayString($setup.fmt($setup.grand.total_nt_hours)), 1),
                createBaseVNode("td", _hoisted_732, toDisplayString($setup.fmt($setup.prod($setup.grand))) + "%", 1),
                createBaseVNode("td", _hoisted_742, toDisplayString($setup.fmt($setup.eff($setup.grand))) + "%", 1),
                createBaseVNode("td", _hoisted_752, toDisplayString($setup.fmt($setup.grand.biometric_hrs)), 1),
                createBaseVNode("td", _hoisted_762, toDisplayString($setup.fmt($setup.grand.nc_rt)), 1),
                createBaseVNode("td", _hoisted_772, toDisplayString($setup.fmt($setup.grand.reopen_rt)), 1),
                createBaseVNode("td", _hoisted_782, toDisplayString($setup.fmt($setup.grand.de_rt)), 1)
              ])
            ])
          ])
        ]))
      ]),
      _: 1
    });
  }
  var _hoisted_121, _hoisted_215, _hoisted_314, _hoisted_49, _hoisted_59, _hoisted_68, _hoisted_78, _hoisted_87, _hoisted_97, _hoisted_106, _hoisted_1111, _hoisted_127, _hoisted_137, _hoisted_147, _hoisted_156, _hoisted_166, _hoisted_176, _hoisted_186, _hoisted_194, _hoisted_203, _hoisted_216, _hoisted_224, _hoisted_234, _hoisted_244, _hoisted_254, _hoisted_264, _hoisted_274, _hoisted_283, _hoisted_293, _hoisted_303, _hoisted_315, _hoisted_324, _hoisted_334, _hoisted_344, _hoisted_354, _hoisted_364, _hoisted_373, _hoisted_383, _hoisted_392, _hoisted_402, _hoisted_41, _hoisted_422, _hoisted_432, _hoisted_442, _hoisted_452, _hoisted_462, _hoisted_472, _hoisted_482, _hoisted_492, _hoisted_50, _hoisted_51, _hoisted_522, _hoisted_532, _hoisted_542, _hoisted_552, _hoisted_562, _hoisted_572, _hoisted_582, _hoisted_592, _hoisted_60, _hoisted_61, _hoisted_622, _hoisted_632, _hoisted_642, _hoisted_652, _hoisted_662, _hoisted_672, _hoisted_682, _hoisted_69, _hoisted_70, _hoisted_71, _hoisted_722, _hoisted_732, _hoisted_742, _hoisted_752, _hoisted_762, _hoisted_772, _hoisted_782;
  var init_SprintOverall2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SprintOverall.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_121 = {
        key: 1,
        class: "itd-empty itd-empty--warn"
      };
      _hoisted_215 = {
        key: 2,
        class: "itd-table-wrap"
      };
      _hoisted_314 = { class: "itd-table itd-table--wide" };
      _hoisted_49 = /* @__PURE__ */ createBaseVNode("thead", null, [
        /* @__PURE__ */ createBaseVNode("tr", null, [
          /* @__PURE__ */ createBaseVNode("th", {
            rowspan: "2",
            style: { "width": "30px" }
          }),
          /* @__PURE__ */ createBaseVNode("th", { rowspan: "2" }, "S.No"),
          /* @__PURE__ */ createBaseVNode("th", {
            rowspan: "2",
            class: "itd-left"
          }, "Team"),
          /* @__PURE__ */ createBaseVNode("th", { rowspan: "2" }, "Sprint ID"),
          /* @__PURE__ */ createBaseVNode("th", {
            rowspan: "2",
            class: "itd-num",
            title: "Available productive hours"
          }, "APH"),
          /* @__PURE__ */ createBaseVNode("th", {
            colspan: "4",
            class: "itd-thgrp itd-thgrp--a"
          }, "PLAN"),
          /* @__PURE__ */ createBaseVNode("th", {
            colspan: "4",
            class: "itd-thgrp itd-thgrp--b"
          }, "SPOT"),
          /* @__PURE__ */ createBaseVNode("th", {
            colspan: "9",
            class: "itd-thgrp itd-thgrp--c"
          }, "TOTAL"),
          /* @__PURE__ */ createBaseVNode("th", {
            rowspan: "2",
            class: "itd-num"
          }, "Biometric Hrs"),
          /* @__PURE__ */ createBaseVNode("th", {
            rowspan: "2",
            class: "itd-num"
          }, "NC RT"),
          /* @__PURE__ */ createBaseVNode("th", {
            rowspan: "2",
            class: "itd-num"
          }, "Reopen RT"),
          /* @__PURE__ */ createBaseVNode("th", {
            rowspan: "2",
            class: "itd-num"
          }, "DE RT")
        ]),
        /* @__PURE__ */ createBaseVNode("tr", null, [
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Planned RT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Comp RT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Work RT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "NT RT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Spot RT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Spot Comp RT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Spot Work RT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Spot NT RT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Total RT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "AT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Completed RT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Completed AT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Working RT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Working AT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Total NT RT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Productivity %"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Efficiency %")
        ])
      ], -1);
      _hoisted_59 = ["onClick"];
      _hoisted_68 = { class: "itd-chev" };
      _hoisted_78 = { class: "itd-left" };
      _hoisted_87 = { class: "itd-num" };
      _hoisted_97 = { class: "itd-num" };
      _hoisted_106 = { class: "itd-num" };
      _hoisted_1111 = { class: "itd-num" };
      _hoisted_127 = { class: "itd-num" };
      _hoisted_137 = { class: "itd-num" };
      _hoisted_147 = { class: "itd-num" };
      _hoisted_156 = { class: "itd-num" };
      _hoisted_166 = { class: "itd-num" };
      _hoisted_176 = { class: "itd-num" };
      _hoisted_186 = { class: "itd-num" };
      _hoisted_194 = { class: "itd-num" };
      _hoisted_203 = { class: "itd-num" };
      _hoisted_216 = { class: "itd-num" };
      _hoisted_224 = { class: "itd-num" };
      _hoisted_234 = { class: "itd-num" };
      _hoisted_244 = { class: "itd-num" };
      _hoisted_254 = { class: "itd-num" };
      _hoisted_264 = { class: "itd-num" };
      _hoisted_274 = { class: "itd-num" };
      _hoisted_283 = { class: "itd-num" };
      _hoisted_293 = { class: "itd-num" };
      _hoisted_303 = /* @__PURE__ */ createBaseVNode("td", null, null, -1);
      _hoisted_315 = /* @__PURE__ */ createBaseVNode("td", null, null, -1);
      _hoisted_324 = { class: "itd-left itd-indent" };
      _hoisted_334 = /* @__PURE__ */ createBaseVNode("td", null, null, -1);
      _hoisted_344 = { class: "itd-num" };
      _hoisted_354 = { class: "itd-num" };
      _hoisted_364 = { class: "itd-num" };
      _hoisted_373 = { class: "itd-num" };
      _hoisted_383 = { class: "itd-num" };
      _hoisted_392 = { class: "itd-num" };
      _hoisted_402 = { class: "itd-num" };
      _hoisted_41 = { class: "itd-num" };
      _hoisted_422 = { class: "itd-num" };
      _hoisted_432 = { class: "itd-num" };
      _hoisted_442 = { class: "itd-num" };
      _hoisted_452 = { class: "itd-num" };
      _hoisted_462 = { class: "itd-num" };
      _hoisted_472 = { class: "itd-num" };
      _hoisted_482 = { class: "itd-num" };
      _hoisted_492 = { class: "itd-num" };
      _hoisted_50 = { class: "itd-num" };
      _hoisted_51 = { class: "itd-num" };
      _hoisted_522 = { class: "itd-num" };
      _hoisted_532 = { class: "itd-num" };
      _hoisted_542 = { class: "itd-num" };
      _hoisted_552 = { class: "itd-num" };
      _hoisted_562 = /* @__PURE__ */ createBaseVNode("td", { colspan: "4" }, "GRAND TOTAL", -1);
      _hoisted_572 = { class: "itd-num" };
      _hoisted_582 = { class: "itd-num" };
      _hoisted_592 = { class: "itd-num" };
      _hoisted_60 = { class: "itd-num" };
      _hoisted_61 = { class: "itd-num" };
      _hoisted_622 = { class: "itd-num" };
      _hoisted_632 = { class: "itd-num" };
      _hoisted_642 = { class: "itd-num" };
      _hoisted_652 = { class: "itd-num" };
      _hoisted_662 = { class: "itd-num" };
      _hoisted_672 = { class: "itd-num" };
      _hoisted_682 = { class: "itd-num" };
      _hoisted_69 = { class: "itd-num" };
      _hoisted_70 = { class: "itd-num" };
      _hoisted_71 = { class: "itd-num" };
      _hoisted_722 = { class: "itd-num" };
      _hoisted_732 = { class: "itd-num" };
      _hoisted_742 = { class: "itd-num" };
      _hoisted_752 = { class: "itd-num" };
      _hoisted_762 = { class: "itd-num" };
      _hoisted_772 = { class: "itd-num" };
      _hoisted_782 = { class: "itd-num" };
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/SprintOverall.vue
  var SprintOverall_default2;
  var init_SprintOverall3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/SprintOverall.vue"() {
      init_SprintOverall();
      init_SprintOverall2();
      SprintOverall_default.render = render16;
      SprintOverall_default.__file = "../teampro/teampro/public/js/it_dashboard/components/SprintOverall.vue";
      SprintOverall_default2 = SprintOverall_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/RtAt.vue?type=script
  var RtAt_default;
  var init_RtAt = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/RtAt.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_SectionCard3();
      init_SkeletonRows3();
      RtAt_default = {
        __name: "RtAt",
        props: {
          team: { type: String, default: "" },
          sprint: { type: String, default: "" }
        },
        setup(__props, { expose: __expose }) {
          __expose();
          const props = __props;
          const loading = ref(true);
          const completed = ref([]);
          const working = ref([]);
          async function load() {
            loading.value = true;
            try {
              const r = await call("get_rtat_exception_data", {
                team: props.team || "",
                sprint: props.sprint || ""
              });
              completed.value = (r == null ? void 0 : r.completed) || [];
              working.value = (r == null ? void 0 : r.working) || [];
            } finally {
              loading.value = false;
            }
          }
          function grand(teams) {
            return {
              rt: teams.reduce((s, t) => s + (t.total_rt || 0), 0),
              at: teams.reduce((s, t) => s + (t.total_at || 0), 0),
              n: teams.reduce((s, t) => s + (t.total_count || 0), 0)
            };
          }
          const grandC = computed2(() => grand(completed.value));
          const grandW = computed2(() => grand(working.value));
          watch2(() => [props.team, props.sprint], load);
          onMounted(load);
          const __returned__ = { props, loading, completed, working, load, grand, grandC, grandW, ref, computed: computed2, watch: watch2, onMounted, get call() {
            return call;
          }, get fmt() {
            return fmt;
          }, SectionCard: SectionCard_default2, SkeletonRows: SkeletonRows_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/RtAt.vue?type=template
  function render17(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["SectionCard"], {
      title: "RT vs AT > 150%",
      subtitle: "Exceptions"
    }, {
      default: withCtx(() => [
        $setup.loading ? (openBlock(), createBlock($setup["SkeletonRows"], {
          key: 0,
          rows: 6,
          cols: 4
        })) : !$setup.completed.length && !$setup.working.length ? (openBlock(), createElementBlock("div", _hoisted_128, " No exceptions found ")) : (openBlock(), createElementBlock("div", _hoisted_217, [
          (openBlock(true), createElementBlock(Fragment, null, renderList([
            { label: "Completed Tasks", teams: $setup.completed, g: $setup.grandC },
            { label: "Working Tasks", teams: $setup.working, g: $setup.grandW }
          ], (sec, si) => {
            return openBlock(), createElementBlock("div", { key: si }, [
              createBaseVNode("h4", _hoisted_316, toDisplayString(sec.label), 1),
              !sec.teams.length ? (openBlock(), createElementBlock("div", _hoisted_410, "No exceptions found")) : (openBlock(), createElementBlock("div", _hoisted_510, [
                createBaseVNode("table", _hoisted_610, [
                  _hoisted_79,
                  (openBlock(true), createElementBlock(Fragment, null, renderList(sec.teams, (t) => {
                    return openBlock(), createElementBlock("tbody", {
                      key: t.team
                    }, [
                      createBaseVNode("tr", _hoisted_88, [
                        createBaseVNode("td", _hoisted_98, [
                          createBaseVNode("b", null, toDisplayString(t.team), 1)
                        ]),
                        createBaseVNode("td", _hoisted_107, [
                          createBaseVNode("b", null, toDisplayString($setup.fmt(t.total_rt)), 1)
                        ]),
                        createBaseVNode("td", _hoisted_1112, [
                          createBaseVNode("b", null, toDisplayString($setup.fmt(t.total_at)), 1)
                        ]),
                        createBaseVNode("td", _hoisted_129, [
                          createBaseVNode("b", null, toDisplayString(t.total_count), 1)
                        ])
                      ]),
                      (openBlock(true), createElementBlock(Fragment, null, renderList(t.cbs || [], (c) => {
                        return openBlock(), createElementBlock("tr", {
                          key: t.team + c.cb
                        }, [
                          createBaseVNode("td", _hoisted_138, toDisplayString(c.cb), 1),
                          createBaseVNode("td", _hoisted_148, toDisplayString($setup.fmt(c.sum_rt)), 1),
                          createBaseVNode("td", _hoisted_157, toDisplayString($setup.fmt(c.sum_at)), 1),
                          createBaseVNode("td", _hoisted_167, toDisplayString(c.task_count), 1)
                        ]);
                      }), 128))
                    ]);
                  }), 128)),
                  createBaseVNode("tfoot", null, [
                    createBaseVNode("tr", null, [
                      _hoisted_177,
                      createBaseVNode("td", _hoisted_187, toDisplayString($setup.fmt(sec.g.rt)), 1),
                      createBaseVNode("td", _hoisted_195, toDisplayString($setup.fmt(sec.g.at)), 1),
                      createBaseVNode("td", _hoisted_204, toDisplayString(sec.g.n), 1)
                    ])
                  ])
                ])
              ]))
            ]);
          }), 128))
        ]))
      ]),
      _: 1
    });
  }
  var _hoisted_128, _hoisted_217, _hoisted_316, _hoisted_410, _hoisted_510, _hoisted_610, _hoisted_79, _hoisted_88, _hoisted_98, _hoisted_107, _hoisted_1112, _hoisted_129, _hoisted_138, _hoisted_148, _hoisted_157, _hoisted_167, _hoisted_177, _hoisted_187, _hoisted_195, _hoisted_204;
  var init_RtAt2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/RtAt.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_128 = {
        key: 1,
        class: "itd-empty"
      };
      _hoisted_217 = {
        key: 2,
        class: "itd-cols2"
      };
      _hoisted_316 = { class: "itd-subhead" };
      _hoisted_410 = {
        key: 0,
        class: "itd-empty"
      };
      _hoisted_510 = {
        key: 1,
        class: "itd-table-wrap"
      };
      _hoisted_610 = { class: "itd-table" };
      _hoisted_79 = /* @__PURE__ */ createBaseVNode("thead", null, [
        /* @__PURE__ */ createBaseVNode("tr", null, [
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-left" }, "Team / CB"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Sum of RT"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Sum of AT Period"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Count of Task")
        ])
      ], -1);
      _hoisted_88 = { class: "itd-row-group" };
      _hoisted_98 = { class: "itd-left" };
      _hoisted_107 = { class: "itd-num" };
      _hoisted_1112 = { class: "itd-num" };
      _hoisted_129 = { class: "itd-num" };
      _hoisted_138 = { class: "itd-left itd-indent" };
      _hoisted_148 = { class: "itd-num" };
      _hoisted_157 = { class: "itd-num" };
      _hoisted_167 = { class: "itd-num" };
      _hoisted_177 = /* @__PURE__ */ createBaseVNode("td", { class: "itd-left" }, "Grand Total", -1);
      _hoisted_187 = { class: "itd-num" };
      _hoisted_195 = { class: "itd-num" };
      _hoisted_204 = { class: "itd-num" };
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/RtAt.vue
  var RtAt_default2;
  var init_RtAt3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/RtAt.vue"() {
      init_RtAt();
      init_RtAt2();
      RtAt_default.render = render17;
      RtAt_default.__file = "../teampro/teampro/public/js/it_dashboard/components/RtAt.vue";
      RtAt_default2 = RtAt_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/NtPriority.vue?type=script
  var NtPriority_default;
  var init_NtPriority = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/NtPriority.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_SectionCard3();
      init_SkeletonRows3();
      NtPriority_default = {
        __name: "NtPriority",
        props: {
          team: { type: String, default: "" },
          sprint: { type: String, default: "" },
          anySprint: { type: Boolean, default: false },
          title: { type: String, default: "NT High / Urgent" }
        },
        setup(__props, { expose: __expose }) {
          __expose();
          const props = __props;
          const loading = ref(true);
          const teams = ref([]);
          async function load() {
            loading.value = true;
            try {
              const r = await call("get_nt_priority_tasks", {
                team: props.team || "",
                sprint: props.sprint || "",
                any_sprint: props.anySprint ? 1 : 0
              });
              teams.value = (r == null ? void 0 : r.teams) || [];
            } finally {
              loading.value = false;
            }
          }
          const grand = computed2(() => ({
            high_rt: teams.value.reduce((s, t) => s + (t.high_rt || 0), 0),
            urgent_rt: teams.value.reduce((s, t) => s + (t.urgent_rt || 0), 0),
            high_count: teams.value.reduce((s, t) => s + (t.high_count || 0), 0),
            urgent_count: teams.value.reduce((s, t) => s + (t.urgent_count || 0), 0)
          }));
          watch2(() => [props.team, props.sprint], load);
          onMounted(load);
          const __returned__ = { props, loading, teams, load, grand, ref, computed: computed2, watch: watch2, onMounted, get call() {
            return call;
          }, get fmt() {
            return fmt;
          }, SectionCard: SectionCard_default2, SkeletonRows: SkeletonRows_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/NtPriority.vue?type=template
  function render18(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["SectionCard"], {
      title: $props.title,
      subtitle: "NT High / Urgent"
    }, {
      default: withCtx(() => [
        $setup.loading ? (openBlock(), createBlock($setup["SkeletonRows"], {
          key: 0,
          rows: 6,
          cols: 5
        })) : !$setup.teams.length ? (openBlock(), createElementBlock("div", _hoisted_130, " No NT tasks with High/Urgent priority found ")) : (openBlock(), createElementBlock("div", _hoisted_218, [
          createBaseVNode("table", _hoisted_317, [
            _hoisted_411,
            (openBlock(true), createElementBlock(Fragment, null, renderList($setup.teams, (t) => {
              return openBlock(), createElementBlock("tbody", {
                key: t.team
              }, [
                createBaseVNode("tr", _hoisted_511, [
                  createBaseVNode("td", _hoisted_611, [
                    createBaseVNode("b", null, toDisplayString(t.team), 1)
                  ]),
                  createBaseVNode("td", _hoisted_710, [
                    createBaseVNode("b", null, toDisplayString($setup.fmt(t.high_rt)), 1)
                  ]),
                  createBaseVNode("td", _hoisted_89, [
                    createBaseVNode("b", null, toDisplayString($setup.fmt(t.urgent_rt)), 1)
                  ]),
                  createBaseVNode("td", _hoisted_99, [
                    createBaseVNode("b", null, toDisplayString(t.high_count), 1)
                  ]),
                  createBaseVNode("td", _hoisted_108, [
                    createBaseVNode("b", null, toDisplayString(t.urgent_count), 1)
                  ])
                ]),
                (openBlock(true), createElementBlock(Fragment, null, renderList(t.cbs || [], (c) => {
                  return openBlock(), createElementBlock("tr", {
                    key: t.team + c.cb
                  }, [
                    createBaseVNode("td", _hoisted_1113, toDisplayString(c.cb), 1),
                    createBaseVNode("td", _hoisted_1210, toDisplayString($setup.fmt(c.high_rt)), 1),
                    createBaseVNode("td", _hoisted_139, toDisplayString($setup.fmt(c.urgent_rt)), 1),
                    createBaseVNode("td", _hoisted_149, toDisplayString(c.high_count), 1),
                    createBaseVNode("td", _hoisted_158, toDisplayString(c.urgent_count), 1)
                  ]);
                }), 128))
              ]);
            }), 128)),
            createBaseVNode("tfoot", null, [
              createBaseVNode("tr", null, [
                _hoisted_168,
                createBaseVNode("td", _hoisted_178, toDisplayString($setup.fmt($setup.grand.high_rt)), 1),
                createBaseVNode("td", _hoisted_188, toDisplayString($setup.fmt($setup.grand.urgent_rt)), 1),
                createBaseVNode("td", _hoisted_196, toDisplayString($setup.grand.high_count), 1),
                createBaseVNode("td", _hoisted_205, toDisplayString($setup.grand.urgent_count), 1)
              ])
            ])
          ])
        ]))
      ]),
      _: 1
    }, 8, ["title"]);
  }
  var _hoisted_130, _hoisted_218, _hoisted_317, _hoisted_411, _hoisted_511, _hoisted_611, _hoisted_710, _hoisted_89, _hoisted_99, _hoisted_108, _hoisted_1113, _hoisted_1210, _hoisted_139, _hoisted_149, _hoisted_158, _hoisted_168, _hoisted_178, _hoisted_188, _hoisted_196, _hoisted_205;
  var init_NtPriority2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/NtPriority.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_130 = {
        key: 1,
        class: "itd-empty"
      };
      _hoisted_218 = {
        key: 2,
        class: "itd-table-wrap"
      };
      _hoisted_317 = { class: "itd-table" };
      _hoisted_411 = /* @__PURE__ */ createBaseVNode("thead", null, [
        /* @__PURE__ */ createBaseVNode("tr", null, [
          /* @__PURE__ */ createBaseVNode("th", {
            rowspan: "2",
            class: "itd-left"
          }, "Team / CB"),
          /* @__PURE__ */ createBaseVNode("th", {
            colspan: "2",
            class: "itd-thgrp itd-thgrp--a"
          }, "Sum of RT"),
          /* @__PURE__ */ createBaseVNode("th", {
            colspan: "2",
            class: "itd-thgrp itd-thgrp--c"
          }, "Count of Task")
        ]),
        /* @__PURE__ */ createBaseVNode("tr", null, [
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "High"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Urgent"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "High"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Urgent")
        ])
      ], -1);
      _hoisted_511 = { class: "itd-row-group" };
      _hoisted_611 = { class: "itd-left" };
      _hoisted_710 = { class: "itd-num" };
      _hoisted_89 = { class: "itd-num" };
      _hoisted_99 = { class: "itd-num" };
      _hoisted_108 = { class: "itd-num" };
      _hoisted_1113 = { class: "itd-left itd-indent" };
      _hoisted_1210 = { class: "itd-num" };
      _hoisted_139 = { class: "itd-num" };
      _hoisted_149 = { class: "itd-num" };
      _hoisted_158 = { class: "itd-num" };
      _hoisted_168 = /* @__PURE__ */ createBaseVNode("td", { class: "itd-left" }, "Grand Total", -1);
      _hoisted_178 = { class: "itd-num" };
      _hoisted_188 = { class: "itd-num" };
      _hoisted_196 = { class: "itd-num" };
      _hoisted_205 = { class: "itd-num" };
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/NtPriority.vue
  var NtPriority_default2;
  var init_NtPriority3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/NtPriority.vue"() {
      init_NtPriority();
      init_NtPriority2();
      NtPriority_default.render = render18;
      NtPriority_default.__file = "../teampro/teampro/public/js/it_dashboard/components/NtPriority.vue";
      NtPriority_default2 = NtPriority_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SprintTab.vue?type=script
  var SprintTab_default;
  var init_SprintTab = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SprintTab.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_FrappControl3();
      init_SprintProgress3();
      init_SprintOverall3();
      init_RtAt3();
      init_NtPriority3();
      SprintTab_default = {
        __name: "SprintTab",
        setup(__props, { expose: __expose }) {
          __expose();
          const team = ref("");
          const sprint = ref("");
          const __returned__ = { team, sprint, ref, FrappControl: FrappControl_default2, SprintProgress: SprintProgress_default2, SprintOverall: SprintOverall_default2, RtAt: RtAt_default2, NtPriority: NtPriority_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SprintTab.vue?type=template
  function render19(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createElementBlock("div", _hoisted_131, [
      createBaseVNode("div", _hoisted_219, [
        createVNode($setup["FrappControl"], {
          df: { fieldtype: "Link", fieldname: "sprint_team", options: "Dev Team", placeholder: "Select Team" },
          modelValue: $setup.team,
          "onUpdate:modelValue": _cache[0] || (_cache[0] = ($event) => $setup.team = $event)
        }, null, 8, ["modelValue"]),
        createVNode($setup["FrappControl"], {
          df: { fieldtype: "Link", fieldname: "sprint_sprint", options: "Task Sprint", placeholder: "Select Sprint" },
          modelValue: $setup.sprint,
          "onUpdate:modelValue": _cache[1] || (_cache[1] = ($event) => $setup.sprint = $event)
        }, null, 8, ["modelValue"])
      ]),
      createVNode($setup["SprintProgress"], {
        team: $setup.team,
        sprint: $setup.sprint
      }, null, 8, ["team", "sprint"]),
      createVNode($setup["SprintOverall"], {
        team: $setup.team,
        sprint: $setup.sprint
      }, null, 8, ["team", "sprint"]),
      createVNode($setup["RtAt"], {
        team: $setup.team,
        sprint: $setup.sprint
      }, null, 8, ["team", "sprint"]),
      createBaseVNode("div", _hoisted_318, [
        createVNode($setup["NtPriority"], {
          team: $setup.team,
          sprint: $setup.sprint,
          title: "NT High / Urgent \u2014 Any Sprint",
          "any-sprint": true
        }, null, 8, ["team", "sprint"]),
        createVNode($setup["NtPriority"], {
          team: $setup.team,
          sprint: $setup.sprint,
          title: "NT High / Urgent \u2014 Current Sprint",
          "any-sprint": false
        }, null, 8, ["team", "sprint"])
      ])
    ]);
  }
  var _hoisted_131, _hoisted_219, _hoisted_318;
  var init_SprintTab2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/SprintTab.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_131 = { class: "itd-sprinttab" };
      _hoisted_219 = { class: "itd-toolbar" };
      _hoisted_318 = { class: "itd-cols2" };
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/SprintTab.vue
  var SprintTab_default2;
  var init_SprintTab3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/SprintTab.vue"() {
      init_SprintTab();
      init_SprintTab2();
      SprintTab_default.render = render19;
      SprintTab_default.__file = "../teampro/teampro/public/js/it_dashboard/components/SprintTab.vue";
      SprintTab_default2 = SprintTab_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/LiveBoard.vue?type=script
  var LiveBoard_default;
  var init_LiveBoard = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/LiveBoard.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_SectionCard3();
      init_SkeletonRows3();
      init_FrappControl3();
      LiveBoard_default = {
        __name: "LiveBoard",
        setup(__props, { expose: __expose }) {
          __expose();
          const loading = ref(true);
          const teams = ref([]);
          const generatedAt = ref("");
          const fromDm = ref(false);
          const dataDate = ref("");
          const selDate = ref(null);
          const autoRefresh = ref(true);
          const openCbs = ref(/* @__PURE__ */ new Set());
          let timer = null;
          async function load() {
            try {
              const r = await call("get_live_status", selDate.value ? { date: selDate.value } : {});
              teams.value = (r == null ? void 0 : r.teams) || [];
              generatedAt.value = (r == null ? void 0 : r.generated_at) || "";
              fromDm.value = !!(r == null ? void 0 : r.from_dm);
              dataDate.value = (r == null ? void 0 : r.date) || "";
            } finally {
              loading.value = false;
            }
          }
          function onDate(v) {
            selDate.value = sysDate(v);
            load();
          }
          const subtitle = computed2(() => {
            const when = dataDate.value && dataDate.value !== today() ? dataDate.value + " \xB7 " : "";
            return (fromDm.value ? "Plan vs actual \xB7 " : "No plan yet \xB7 ") + when + "As of " + fmtTime(generatedAt.value);
          });
          function toggleCb(team, cb) {
            const k = team + "|" + cb;
            const s = new Set(openCbs.value);
            s.has(k) ? s.delete(k) : s.add(k);
            openCbs.value = s;
          }
          function isOpen(team, cb) {
            return !openCbs.value.has(team + "|" + cb);
          }
          function pct(t) {
            const total = (t.at || 0) + (t.rt || 0);
            if (!total)
              return 0;
            return Math.min(100, Math.round((t.at || 0) / total * 100));
          }
          function barClass(t) {
            const p2 = (t.at || 0) / ((t.at || 0) + (t.rt || 0) || 1);
            if (p2 > 1)
              return "itd-fill--red";
            if (p2 > 0.8)
              return "itd-fill--amber";
            return "itd-fill--green";
          }
          function fmtTime(ts) {
            if (!ts)
              return "";
            try {
              return frappe.datetime.str_to_user(ts).split(" ").pop();
            } catch (e) {
              return ts;
            }
          }
          const totals = computed2(() => {
            let planned = 0, worked = 0;
            for (const t of teams.value)
              for (const m of t.members) {
                planned += m.planned || 0;
                worked += m.worked || 0;
              }
            return { planned, worked };
          });
          onMounted(() => {
            load();
            timer = setInterval(() => {
              if (autoRefresh.value)
                load();
            }, 6e4);
          });
          onBeforeUnmount(() => clearInterval(timer));
          const __returned__ = { loading, teams, generatedAt, fromDm, dataDate, selDate, autoRefresh, openCbs, get timer() {
            return timer;
          }, set timer(v) {
            timer = v;
          }, load, onDate, subtitle, toggleCb, isOpen, pct, barClass, fmtTime, totals, ref, computed: computed2, onMounted, onBeforeUnmount, get call() {
            return call;
          }, get fmt() {
            return fmt;
          }, get sysDate() {
            return sysDate;
          }, get today() {
            return today;
          }, SectionCard: SectionCard_default2, SkeletonRows: SkeletonRows_default2, FrappControl: FrappControl_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/LiveBoard.vue?type=template
  function render20(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["SectionCard"], {
      title: "Live Activity",
      subtitle: $setup.subtitle
    }, {
      actions: withCtx(() => [
        $setup.fromDm && $setup.totals.planned ? (openBlock(), createElementBlock("span", _hoisted_140, toDisplayString($setup.totals.worked) + "/" + toDisplayString($setup.totals.planned) + " tasks worked ", 1)) : createCommentVNode("v-if", true),
        createVNode($setup["FrappControl"], {
          df: { fieldtype: "Date", fieldname: "live_date", placeholder: "Select date" },
          modelValue: $setup.selDate,
          "onUpdate:modelValue": $setup.onDate
        }, null, 8, ["modelValue"]),
        createBaseVNode("label", _hoisted_220, [
          withDirectives(createBaseVNode("input", {
            type: "checkbox",
            "onUpdate:modelValue": _cache[0] || (_cache[0] = ($event) => $setup.autoRefresh = $event)
          }, null, 512), [
            [vModelCheckbox, $setup.autoRefresh]
          ]),
          createTextVNode(" Auto-refresh ")
        ]),
        createBaseVNode("button", {
          class: "itd-textbtn",
          onClick: $setup.load
        }, "Refresh")
      ]),
      default: withCtx(() => [
        $setup.loading ? (openBlock(), createBlock($setup["SkeletonRows"], {
          key: 0,
          rows: 8,
          cols: 6
        })) : !$setup.teams.length ? (openBlock(), createElementBlock("div", _hoisted_319, "No activity right now")) : (openBlock(), createElementBlock("div", _hoisted_412, [
          createBaseVNode("table", _hoisted_512, [
            _hoisted_612,
            (openBlock(true), createElementBlock(Fragment, null, renderList($setup.teams, (t) => {
              return openBlock(), createElementBlock("tbody", {
                key: t.team
              }, [
                createBaseVNode("tr", _hoisted_711, [
                  createBaseVNode("td", _hoisted_810, [
                    t.logo ? (openBlock(), createElementBlock("img", {
                      key: 0,
                      src: t.logo,
                      class: "itd-teamlogo",
                      alt: ""
                    }, null, 8, _hoisted_910)) : createCommentVNode("v-if", true),
                    createBaseVNode("b", null, toDisplayString(t.team), 1)
                  ])
                ]),
                (openBlock(true), createElementBlock(Fragment, null, renderList(t.members, (m) => {
                  return openBlock(), createElementBlock(Fragment, {
                    key: t.team + m.cb
                  }, [
                    createBaseVNode("tr", {
                      class: "itd-row-cb",
                      onClick: ($event) => $setup.toggleCb(t.team, m.cb)
                    }, [
                      createBaseVNode("td", _hoisted_1114, [
                        createBaseVNode("span", _hoisted_1211, [
                          m.image ? (openBlock(), createElementBlock("img", {
                            key: 0,
                            src: m.image,
                            class: "itd-avatar",
                            alt: ""
                          }, null, 8, _hoisted_1310)) : createCommentVNode("v-if", true),
                          createBaseVNode("b", null, toDisplayString(m.cb), 1),
                          createBaseVNode("span", _hoisted_1410, toDisplayString(m.employee), 1),
                          m.is_tl ? (openBlock(), createElementBlock("span", _hoisted_159, "TL")) : createCommentVNode("v-if", true),
                          $setup.fromDm ? (openBlock(), createElementBlock("span", _hoisted_169, toDisplayString(m.worked) + "/" + toDisplayString(m.planned) + " worked ", 1)) : (openBlock(), createElementBlock("span", _hoisted_179, "\xB7 " + toDisplayString(m.tasks.length) + " task" + toDisplayString(m.tasks.length === 1 ? "" : "s"), 1)),
                          createBaseVNode("span", _hoisted_189, "\xB7 " + toDisplayString($setup.fmt(m.today_hours)) + "h today", 1),
                          m.aph ? (openBlock(), createElementBlock("span", _hoisted_197, "\xB7 APH " + toDisplayString($setup.fmt(m.aph)), 1)) : createCommentVNode("v-if", true)
                        ])
                      ])
                    ], 8, _hoisted_109),
                    !m.tasks.length && !m.unplanned.length && $setup.isOpen(t.team, m.cb) ? (openBlock(), createElementBlock("tr", _hoisted_206, [..._hoisted_225])) : createCommentVNode("v-if", true),
                    (openBlock(true), createElementBlock(Fragment, null, renderList(m.tasks, (task) => {
                      return withDirectives((openBlock(), createElementBlock("tr", {
                        key: task.name,
                        class: normalizeClass(["itd-row-task", { "itd-row-idle": $setup.fromDm && !task.today && task.status === "Working" }])
                      }, [
                        createBaseVNode("td", _hoisted_235, [
                          createBaseVNode("a", {
                            href: `/app/task/${encodeURIComponent(task.name)}`,
                            target: "_blank",
                            class: "itd-link"
                          }, toDisplayString(task.name), 9, _hoisted_245)
                        ]),
                        createBaseVNode("td", _hoisted_255, toDisplayString(task.subject), 1),
                        createBaseVNode("td", _hoisted_265, toDisplayString(task.project), 1),
                        createBaseVNode("td", null, [
                          createBaseVNode("span", {
                            class: normalizeClass(["itd-prio", "itd-st--" + String(task.status || "").toLowerCase().replace(/ /g, "-")])
                          }, toDisplayString(task.status), 3)
                        ]),
                        createBaseVNode("td", null, [
                          task.priority ? (openBlock(), createElementBlock("span", {
                            key: 0,
                            class: normalizeClass(["itd-prio", "itd-prio--" + String(task.priority).toLowerCase()])
                          }, toDisplayString(task.priority), 3)) : createCommentVNode("v-if", true)
                        ]),
                        createBaseVNode("td", _hoisted_275, toDisplayString($setup.fmt(task.et)), 1),
                        createBaseVNode("td", _hoisted_284, toDisplayString($setup.fmt(task.at)), 1),
                        createBaseVNode("td", _hoisted_294, toDisplayString($setup.fmt(task.rt)), 1),
                        createBaseVNode("td", _hoisted_304, [
                          createBaseVNode("span", {
                            class: normalizeClass({ "itd-today-zero": $setup.fromDm && !task.today, "itd-today-yes": task.today })
                          }, toDisplayString($setup.fmt(task.today)), 3)
                        ]),
                        createBaseVNode("td", null, [
                          createBaseVNode("div", _hoisted_3110, [
                            createBaseVNode("div", _hoisted_325, [
                              createBaseVNode("div", {
                                class: normalizeClass(["itd-prog-fill", $setup.barClass(task)]),
                                style: normalizeStyle({ width: $setup.pct(task) + "%" })
                              }, null, 6)
                            ]),
                            createBaseVNode("span", _hoisted_335, toDisplayString($setup.pct(task)) + "%", 1)
                          ])
                        ])
                      ], 2)), [
                        [vShow, $setup.isOpen(t.team, m.cb)]
                      ]);
                    }), 128)),
                    (openBlock(true), createElementBlock(Fragment, null, renderList(m.unplanned, (task) => {
                      return withDirectives((openBlock(), createElementBlock("tr", {
                        key: "u-" + task.name,
                        class: "itd-row-task itd-row-unplanned"
                      }, [
                        createBaseVNode("td", _hoisted_345, [
                          createBaseVNode("a", {
                            href: `/app/task/${encodeURIComponent(task.name)}`,
                            target: "_blank",
                            class: "itd-link"
                          }, toDisplayString(task.name), 9, _hoisted_355)
                        ]),
                        createBaseVNode("td", _hoisted_365, toDisplayString(task.subject), 1),
                        createBaseVNode("td", _hoisted_374, toDisplayString(task.project), 1),
                        createBaseVNode("td", null, [
                          createBaseVNode("span", _hoisted_384, toDisplayString(task.status), 1),
                          _hoisted_393
                        ]),
                        _hoisted_403,
                        _hoisted_413,
                        _hoisted_423,
                        _hoisted_433,
                        createBaseVNode("td", _hoisted_443, toDisplayString($setup.fmt(task.today)), 1),
                        _hoisted_453
                      ])), [
                        [vShow, $setup.isOpen(t.team, m.cb)]
                      ]);
                    }), 128))
                  ], 64);
                }), 128))
              ]);
            }), 128))
          ])
        ]))
      ]),
      _: 1
    }, 8, ["subtitle"]);
  }
  var _hoisted_140, _hoisted_220, _hoisted_319, _hoisted_412, _hoisted_512, _hoisted_612, _hoisted_711, _hoisted_810, _hoisted_910, _hoisted_109, _hoisted_1114, _hoisted_1211, _hoisted_1310, _hoisted_1410, _hoisted_159, _hoisted_169, _hoisted_179, _hoisted_189, _hoisted_197, _hoisted_206, _hoisted_2110, _hoisted_225, _hoisted_235, _hoisted_245, _hoisted_255, _hoisted_265, _hoisted_275, _hoisted_284, _hoisted_294, _hoisted_304, _hoisted_3110, _hoisted_325, _hoisted_335, _hoisted_345, _hoisted_355, _hoisted_365, _hoisted_374, _hoisted_384, _hoisted_393, _hoisted_403, _hoisted_413, _hoisted_423, _hoisted_433, _hoisted_443, _hoisted_453;
  var init_LiveBoard2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/LiveBoard.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_140 = {
        key: 0,
        class: "itd-livecov"
      };
      _hoisted_220 = { class: "itd-check" };
      _hoisted_319 = {
        key: 1,
        class: "itd-empty"
      };
      _hoisted_412 = {
        key: 2,
        class: "itd-table-wrap"
      };
      _hoisted_512 = { class: "itd-table" };
      _hoisted_612 = /* @__PURE__ */ createBaseVNode("thead", null, [
        /* @__PURE__ */ createBaseVNode("tr", null, [
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-left" }, "Employee / Task"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-left" }, "Subject"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-left" }, "Project"),
          /* @__PURE__ */ createBaseVNode("th", null, "Status"),
          /* @__PURE__ */ createBaseVNode("th", null, "Priority"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "ET"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Spent"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Left"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-num" }, "Today"),
          /* @__PURE__ */ createBaseVNode("th", {
            class: "itd-left",
            style: { "min-width": "140px" }
          }, "Progress")
        ])
      ], -1);
      _hoisted_711 = { class: "itd-row-team" };
      _hoisted_810 = {
        colspan: "10",
        class: "itd-left"
      };
      _hoisted_910 = ["src"];
      _hoisted_109 = ["onClick"];
      _hoisted_1114 = {
        colspan: "10",
        class: "itd-left"
      };
      _hoisted_1211 = { class: "itd-cbhead" };
      _hoisted_1310 = ["src"];
      _hoisted_1410 = { class: "itd-muted" };
      _hoisted_159 = {
        key: 1,
        class: "itd-tag itd-tag--plan"
      };
      _hoisted_169 = {
        key: 2,
        class: "itd-livecov"
      };
      _hoisted_179 = {
        key: 3,
        class: "itd-muted"
      };
      _hoisted_189 = { class: "itd-muted" };
      _hoisted_197 = {
        key: 4,
        class: "itd-muted"
      };
      _hoisted_206 = {
        key: 0,
        class: "itd-row-task"
      };
      _hoisted_2110 = /* @__PURE__ */ createBaseVNode("td", {
        colspan: "10",
        class: "itd-left itd-indent itd-muted"
      }, "No tasks", -1);
      _hoisted_225 = [
        _hoisted_2110
      ];
      _hoisted_235 = { class: "itd-left itd-indent" };
      _hoisted_245 = ["href"];
      _hoisted_255 = { class: "itd-left" };
      _hoisted_265 = { class: "itd-left" };
      _hoisted_275 = { class: "itd-num itd-mono" };
      _hoisted_284 = { class: "itd-num itd-mono" };
      _hoisted_294 = { class: "itd-num itd-mono" };
      _hoisted_304 = { class: "itd-num itd-mono" };
      _hoisted_3110 = { class: "itd-prog" };
      _hoisted_325 = { class: "itd-prog-track" };
      _hoisted_335 = { class: "itd-prog-label" };
      _hoisted_345 = { class: "itd-left itd-indent" };
      _hoisted_355 = ["href"];
      _hoisted_365 = { class: "itd-left" };
      _hoisted_374 = { class: "itd-left" };
      _hoisted_384 = { class: "itd-prio itd-st--open" };
      _hoisted_393 = /* @__PURE__ */ createBaseVNode("span", { class: "itd-tag itd-tag--spot" }, "Unplanned", -1);
      _hoisted_403 = /* @__PURE__ */ createBaseVNode("td", null, null, -1);
      _hoisted_413 = /* @__PURE__ */ createBaseVNode("td", { class: "itd-num itd-muted" }, "\u2013", -1);
      _hoisted_423 = /* @__PURE__ */ createBaseVNode("td", { class: "itd-num itd-muted" }, "\u2013", -1);
      _hoisted_433 = /* @__PURE__ */ createBaseVNode("td", { class: "itd-num itd-muted" }, "\u2013", -1);
      _hoisted_443 = { class: "itd-num itd-mono itd-today-yes" };
      _hoisted_453 = /* @__PURE__ */ createBaseVNode("td", null, null, -1);
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/LiveBoard.vue
  var LiveBoard_default2;
  var init_LiveBoard3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/LiveBoard.vue"() {
      init_LiveBoard();
      init_LiveBoard2();
      LiveBoard_default.render = render20;
      LiveBoard_default.__file = "../teampro/teampro/public/js/it_dashboard/components/LiveBoard.vue";
      LiveBoard_default2 = LiveBoard_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProjectWip.vue?type=script
  var ProjectWip_default;
  var init_ProjectWip = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProjectWip.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_api();
      init_SectionCard3();
      init_FrappControl3();
      init_SkeletonRows3();
      ProjectWip_default = {
        __name: "ProjectWip",
        setup(__props, { expose: __expose }) {
          __expose();
          const loading = ref(true);
          const rows = ref([]);
          const types = ref([]);
          const project = ref("");
          const ptype = ref("");
          const pmEl = ref(null);
          let pmAssetReady = false;
          const projectDf = {
            fieldtype: "Link",
            options: "Project",
            placeholder: "All Projects",
            filters: { service: "IT-SW" }
          };
          async function load() {
            loading.value = true;
            try {
              const r = await call("get_project_wip", {
                project: project.value || null,
                project_type: ptype.value || null
              }) || {};
              rows.value = r.rows || [];
              types.value = r.types || [];
            } finally {
              loading.value = false;
            }
          }
          async function renderMonitor(name) {
            if (!name)
              return;
            if (!pmAssetReady) {
              await frappe.require(["/assets/teampro/js/project_monitoring.js?v=20260925-1"]);
              pmAssetReady = true;
            }
            await nextTick();
            const mon = window.teampro && teampro.project_monitoring;
            if (!mon || !pmEl.value)
              return;
            mon.load_css();
            const frm = {
              doc: { name, service: "IT-SW" },
              _pm_tab: { wrapper: $(pmEl.value) }
            };
            mon.load(frm, true);
          }
          function onProjectChange(v) {
            if (!v)
              return;
            renderMonitor(v);
          }
          function pickProject(name) {
            project.value = name;
            renderMonitor(name);
          }
          function clearProject() {
            project.value = "";
            load();
          }
          const fdate = (v) => v ? frappe.datetime.str_to_user(v) : "-";
          const STATUS_CLS = {
            Open: "itd-b-gray",
            Working: "itd-b-blue",
            "In Progress": "itd-b-blue",
            Completed: "itd-b-green",
            Hold: "itd-b-amber",
            Cancelled: "itd-b-gray",
            Overdue: "itd-b-red"
          };
          const totalRow = computed2(() => {
            const t = {
              open: 0,
              working: 0,
              review: 0,
              hold: 0,
              completed: 0,
              overdue: 0,
              et: 0,
              at: 0,
              meetings: 0,
              meetings_done: 0,
              so_value: 0,
              billed: 0,
              total: 0
            };
            for (const r of rows.value) {
              for (const k of Object.keys(t))
                t[k] += r[k] || 0;
            }
            return t;
          });
          function exportXlsx() {
            const head = [
              "Project",
              "Type",
              "Customer",
              "Status",
              "SPOC",
              "Open",
              "Working",
              "Review",
              "Hold",
              "Completed",
              "Overdue",
              "ET (Hrs)",
              "AT (Hrs)",
              "Meetings Done",
              "Meetings Total",
              "SLA From",
              "SLA To",
              "Expected End",
              "SO Value",
              "Billed"
            ];
            const data = rows.value.map((r) => [
              r.project_name,
              r.project_type || "",
              r.customer || "",
              r.status || "",
              r.spoc || "",
              r.open,
              r.working,
              r.review,
              r.hold,
              r.completed,
              r.overdue,
              r.et,
              r.at,
              r.meetings_done,
              r.meetings,
              r.sla_from || "",
              r.sla_to || "",
              r.expected_end_date || "",
              r.so_value,
              r.billed
            ]);
            downloadRowsAsXlsx("project-wip.xlsx", "Project WIP", [head, ...data]);
          }
          onMounted(load);
          const __returned__ = { loading, rows, types, project, ptype, pmEl, get pmAssetReady() {
            return pmAssetReady;
          }, set pmAssetReady(v) {
            pmAssetReady = v;
          }, projectDf, load, renderMonitor, onProjectChange, pickProject, clearProject, fdate, STATUS_CLS, totalRow, exportXlsx, ref, computed: computed2, onMounted, nextTick, get call() {
            return call;
          }, get fmt() {
            return fmt;
          }, get downloadRowsAsXlsx() {
            return downloadRowsAsXlsx;
          }, SectionCard: SectionCard_default2, FrappControl: FrappControl_default2, SkeletonRows: SkeletonRows_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProjectWip.vue?type=template
  function render21(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createBlock($setup["SectionCard"], {
      title: "PROJECT WIP",
      subtitle: "IT-SW projects \u2014 task & meeting rollup"
    }, {
      actions: withCtx(() => [
        createBaseVNode("div", _hoisted_141, [
          createBaseVNode("div", _hoisted_221, [
            createVNode($setup["FrappControl"], {
              df: $setup.projectDf,
              modelValue: $setup.project,
              "onUpdate:modelValue": _cache[0] || (_cache[0] = ($event) => $setup.project = $event),
              onChange: $setup.onProjectChange
            }, null, 8, ["modelValue"])
          ]),
          withDirectives(createBaseVNode("select", {
            "onUpdate:modelValue": _cache[1] || (_cache[1] = ($event) => $setup.ptype = $event),
            class: "form-control input-xs",
            style: { "width": "140px" },
            onChange: $setup.load
          }, [
            _hoisted_320,
            (openBlock(true), createElementBlock(Fragment, null, renderList($setup.types, (t) => {
              return openBlock(), createElementBlock("option", {
                key: t,
                value: t
              }, toDisplayString(t), 9, _hoisted_414);
            }), 128))
          ], 544), [
            [vModelSelect, $setup.ptype]
          ]),
          createBaseVNode("button", {
            class: "itd-iconbtn",
            title: "Export to Excel",
            onClick: $setup.exportXlsx
          }, "\u2B73")
        ])
      ]),
      default: withCtx(() => [
        $setup.project ? (openBlock(), createElementBlock("div", _hoisted_513, [
          createBaseVNode("div", _hoisted_613, [
            createBaseVNode("b", null, toDisplayString($setup.project), 1),
            createBaseVNode("button", {
              class: "itd-textbtn",
              onClick: $setup.clearProject
            }, "\u2715 Close monitoring")
          ]),
          createBaseVNode("div", _hoisted_712, null, 512)
        ])) : createCommentVNode("v-if", true),
        $setup.loading ? (openBlock(), createBlock($setup["SkeletonRows"], {
          key: 1,
          rows: 8,
          cols: 12
        })) : (openBlock(), createElementBlock("div", _hoisted_811, [
          createBaseVNode("table", _hoisted_911, [
            _hoisted_1010,
            createBaseVNode("tbody", null, [
              (openBlock(true), createElementBlock(Fragment, null, renderList($setup.rows, (r, i) => {
                return openBlock(), createElementBlock("tr", {
                  key: r.name
                }, [
                  createBaseVNode("td", null, toDisplayString(i + 1), 1),
                  createBaseVNode("td", _hoisted_1115, [
                    createBaseVNode("a", {
                      href: "javascript:void(0)",
                      onClick: ($event) => $setup.pickProject(r.name)
                    }, toDisplayString(r.project_name), 9, _hoisted_1212)
                  ]),
                  createBaseVNode("td", null, toDisplayString(r.project_type || "-"), 1),
                  createBaseVNode("td", _hoisted_1311, toDisplayString(r.customer || "-"), 1),
                  createBaseVNode("td", null, [
                    createBaseVNode("span", {
                      class: normalizeClass(["itd-badge", $setup.STATUS_CLS[r.status] || "itd-b-gray"])
                    }, toDisplayString(r.status || "-"), 3)
                  ]),
                  createBaseVNode("td", _hoisted_1411, toDisplayString(r.open), 1),
                  createBaseVNode("td", _hoisted_1510, toDisplayString(r.working), 1),
                  createBaseVNode("td", _hoisted_1610, toDisplayString(r.review), 1),
                  createBaseVNode("td", _hoisted_1710, toDisplayString(r.hold), 1),
                  createBaseVNode("td", _hoisted_1810, toDisplayString(r.completed), 1),
                  createBaseVNode("td", {
                    class: "itd-num",
                    style: normalizeStyle(r.overdue ? "color:#c53030;font-weight:700" : "")
                  }, toDisplayString(r.overdue), 5),
                  createBaseVNode("td", _hoisted_198, toDisplayString($setup.fmt(r.et)), 1),
                  createBaseVNode("td", _hoisted_207, toDisplayString($setup.fmt(r.at)), 1),
                  createBaseVNode("td", _hoisted_2111, toDisplayString(r.meetings_done) + "/" + toDisplayString(r.meetings), 1),
                  createBaseVNode("td", _hoisted_226, toDisplayString($setup.fdate(r.sla_to || r.expected_end_date)), 1),
                  createBaseVNode("td", _hoisted_236, toDisplayString($setup.fmt(r.so_value)), 1),
                  createBaseVNode("td", _hoisted_246, toDisplayString($setup.fmt(r.billed)), 1)
                ]);
              }), 128)),
              !$setup.rows.length ? (openBlock(), createElementBlock("tr", _hoisted_256, [..._hoisted_276])) : createCommentVNode("v-if", true)
            ]),
            $setup.rows.length ? (openBlock(), createElementBlock("tfoot", _hoisted_285, [
              createBaseVNode("tr", null, [
                _hoisted_295,
                createBaseVNode("td", _hoisted_305, "TOTAL (" + toDisplayString($setup.rows.length) + ")", 1),
                _hoisted_3111,
                createBaseVNode("td", null, toDisplayString($setup.totalRow.open), 1),
                createBaseVNode("td", null, toDisplayString($setup.totalRow.working), 1),
                createBaseVNode("td", null, toDisplayString($setup.totalRow.review), 1),
                createBaseVNode("td", null, toDisplayString($setup.totalRow.hold), 1),
                createBaseVNode("td", null, toDisplayString($setup.totalRow.completed), 1),
                createBaseVNode("td", null, toDisplayString($setup.totalRow.overdue), 1),
                createBaseVNode("td", null, toDisplayString($setup.fmt($setup.totalRow.et)), 1),
                createBaseVNode("td", null, toDisplayString($setup.fmt($setup.totalRow.at)), 1),
                createBaseVNode("td", null, toDisplayString($setup.totalRow.meetings_done) + "/" + toDisplayString($setup.totalRow.meetings), 1),
                _hoisted_326,
                createBaseVNode("td", null, toDisplayString($setup.fmt($setup.totalRow.so_value)), 1),
                createBaseVNode("td", null, toDisplayString($setup.fmt($setup.totalRow.billed)), 1)
              ])
            ])) : createCommentVNode("v-if", true)
          ])
        ]))
      ]),
      _: 1
    });
  }
  var _hoisted_141, _hoisted_221, _hoisted_320, _hoisted_414, _hoisted_513, _hoisted_613, _hoisted_712, _hoisted_811, _hoisted_911, _hoisted_1010, _hoisted_1115, _hoisted_1212, _hoisted_1311, _hoisted_1411, _hoisted_1510, _hoisted_1610, _hoisted_1710, _hoisted_1810, _hoisted_198, _hoisted_207, _hoisted_2111, _hoisted_226, _hoisted_236, _hoisted_246, _hoisted_256, _hoisted_266, _hoisted_276, _hoisted_285, _hoisted_295, _hoisted_305, _hoisted_3111, _hoisted_326;
  var init_ProjectWip2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/components/ProjectWip.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_141 = { class: "itd-wip-filters" };
      _hoisted_221 = { style: { "width": "210px" } };
      _hoisted_320 = /* @__PURE__ */ createBaseVNode("option", { value: "" }, "All Types", -1);
      _hoisted_414 = ["value"];
      _hoisted_513 = {
        key: 0,
        class: "itd-wip-monitor"
      };
      _hoisted_613 = { class: "itd-wip-monitor-head" };
      _hoisted_712 = { ref: "pmEl" };
      _hoisted_811 = {
        key: 2,
        class: "itd-table-wrap"
      };
      _hoisted_911 = { class: "itd-table itd-table--wide" };
      _hoisted_1010 = /* @__PURE__ */ createBaseVNode("thead", null, [
        /* @__PURE__ */ createBaseVNode("tr", null, [
          /* @__PURE__ */ createBaseVNode("th", null, "#"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-left" }, "Project"),
          /* @__PURE__ */ createBaseVNode("th", null, "Type"),
          /* @__PURE__ */ createBaseVNode("th", { class: "itd-left" }, "Customer"),
          /* @__PURE__ */ createBaseVNode("th", null, "Status"),
          /* @__PURE__ */ createBaseVNode("th", null, "Open"),
          /* @__PURE__ */ createBaseVNode("th", null, "Working"),
          /* @__PURE__ */ createBaseVNode("th", null, "Review"),
          /* @__PURE__ */ createBaseVNode("th", null, "Hold"),
          /* @__PURE__ */ createBaseVNode("th", null, "Comp."),
          /* @__PURE__ */ createBaseVNode("th", null, "Overdue"),
          /* @__PURE__ */ createBaseVNode("th", null, "ET (Hrs)"),
          /* @__PURE__ */ createBaseVNode("th", null, "AT (Hrs)"),
          /* @__PURE__ */ createBaseVNode("th", null, "Mtgs"),
          /* @__PURE__ */ createBaseVNode("th", null, "End / SLA"),
          /* @__PURE__ */ createBaseVNode("th", null, "SO Value"),
          /* @__PURE__ */ createBaseVNode("th", null, "Billed")
        ])
      ], -1);
      _hoisted_1115 = { class: "itd-left" };
      _hoisted_1212 = ["onClick"];
      _hoisted_1311 = { class: "itd-left" };
      _hoisted_1411 = { class: "itd-num" };
      _hoisted_1510 = { class: "itd-num" };
      _hoisted_1610 = { class: "itd-num" };
      _hoisted_1710 = { class: "itd-num" };
      _hoisted_1810 = { class: "itd-num" };
      _hoisted_198 = { class: "itd-num" };
      _hoisted_207 = { class: "itd-num" };
      _hoisted_2111 = { class: "itd-num" };
      _hoisted_226 = { class: "itd-num" };
      _hoisted_236 = { class: "itd-num" };
      _hoisted_246 = { class: "itd-num" };
      _hoisted_256 = { key: 0 };
      _hoisted_266 = /* @__PURE__ */ createBaseVNode("td", {
        colspan: "17",
        style: { "text-align": "center", "color": "#888" }
      }, "No projects match the filters.", -1);
      _hoisted_276 = [
        _hoisted_266
      ];
      _hoisted_285 = { key: 0 };
      _hoisted_295 = /* @__PURE__ */ createBaseVNode("td", null, null, -1);
      _hoisted_305 = { class: "itd-left" };
      _hoisted_3111 = /* @__PURE__ */ createBaseVNode("td", { colspan: "3" }, null, -1);
      _hoisted_326 = /* @__PURE__ */ createBaseVNode("td", null, null, -1);
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/components/ProjectWip.vue
  var ProjectWip_default2;
  var init_ProjectWip3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/components/ProjectWip.vue"() {
      init_ProjectWip();
      init_ProjectWip2();
      ProjectWip_default.render = render21;
      ProjectWip_default.__file = "../teampro/teampro/public/js/it_dashboard/components/ProjectWip.vue";
      ProjectWip_default2 = ProjectWip_default;
    }
  });

  // sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/ItDashboard.vue?type=script
  var ItDashboard_default;
  var init_ItDashboard = __esm({
    "sfc-script:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/ItDashboard.vue?type=script"() {
      init_vue_runtime_esm_bundler();
      init_ProjectCounts3();
      init_TaskCounts3();
      init_PsrTable3();
      init_ProductionSummary3();
      init_ProductionTable3();
      init_NonAllocated3();
      init_DsrDpr3();
      init_RetroSummary3();
      init_SprintTab3();
      init_LiveBoard3();
      init_ProjectWip3();
      ItDashboard_default = {
        __name: "ItDashboard",
        setup(__props, { expose: __expose }) {
          __expose();
          const tab = ref("dashboard");
          const sprintLoaded = ref(false);
          const liveLoaded = ref(false);
          const wipLoaded = ref(false);
          const now = ref("");
          const psr = ref(null);
          let clockTimer = null;
          function onProjectSelect(type) {
            var _a;
            (_a = psr.value) == null ? void 0 : _a.setTypeFilter(type);
          }
          function pickTab(t) {
            tab.value = t;
            if (t === "sprint")
              sprintLoaded.value = true;
            if (t === "live")
              liveLoaded.value = true;
            if (t === "wip")
              wipLoaded.value = true;
          }
          function tick() {
            now.value = frappe.datetime ? frappe.datetime.str_to_user(frappe.datetime.now_datetime()) : new Date().toLocaleString();
          }
          onMounted(() => {
            tick();
            clockTimer = setInterval(tick, 1e3);
          });
          onBeforeUnmount(() => clearInterval(clockTimer));
          const __returned__ = { tab, sprintLoaded, liveLoaded, wipLoaded, now, psr, get clockTimer() {
            return clockTimer;
          }, set clockTimer(v) {
            clockTimer = v;
          }, onProjectSelect, pickTab, tick, ref, onMounted, onBeforeUnmount, ProjectCounts: ProjectCounts_default2, TaskCounts: TaskCounts_default2, PsrTable: PsrTable_default2, ProductionSummary: ProductionSummary_default2, ProductionTable: ProductionTable_default2, NonAllocated: NonAllocated_default2, DsrDpr: DsrDpr_default2, RetroSummary: RetroSummary_default2, SprintTab: SprintTab_default2, LiveBoard: LiveBoard_default2, ProjectWip: ProjectWip_default2 };
          Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
          return __returned__;
        }
      };
    }
  });

  // sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/ItDashboard.vue?type=template
  function render22(_ctx, _cache, $props, $setup, $data, $options) {
    return openBlock(), createElementBlock("div", _hoisted_150, [
      createBaseVNode("header", _hoisted_227, [
        createBaseVNode("div", _hoisted_321, [
          createBaseVNode("button", {
            class: normalizeClass(["itd-tab", { "itd-tab--on": $setup.tab === "dashboard" }]),
            onClick: _cache[0] || (_cache[0] = ($event) => $setup.pickTab("dashboard"))
          }, " Dashboard ", 2),
          createBaseVNode("button", {
            class: normalizeClass(["itd-tab", { "itd-tab--on": $setup.tab === "live" }]),
            onClick: _cache[1] || (_cache[1] = ($event) => $setup.pickTab("live"))
          }, " Live ", 2),
          createBaseVNode("button", {
            class: normalizeClass(["itd-tab", { "itd-tab--on": $setup.tab === "sprint" }]),
            onClick: _cache[2] || (_cache[2] = ($event) => $setup.pickTab("sprint"))
          }, " Sprint ", 2),
          createBaseVNode("button", {
            class: normalizeClass(["itd-tab", { "itd-tab--on": $setup.tab === "wip" }]),
            onClick: _cache[3] || (_cache[3] = ($event) => $setup.pickTab("wip"))
          }, " Project WIP ", 2)
        ]),
        createBaseVNode("div", _hoisted_415, toDisplayString($setup.now), 1)
      ]),
      withDirectives(createBaseVNode("div", _hoisted_514, [
        createVNode($setup["ProjectCounts"], { onSelect: $setup.onProjectSelect }),
        createVNode($setup["TaskCounts"]),
        createVNode($setup["PsrTable"], { ref: "psr" }, null, 512),
        createVNode($setup["ProductionSummary"]),
        createVNode($setup["ProductionTable"]),
        createVNode($setup["NonAllocated"]),
        createVNode($setup["DsrDpr"]),
        createVNode($setup["RetroSummary"])
      ], 512), [
        [vShow, $setup.tab === "dashboard"]
      ]),
      $setup.liveLoaded ? withDirectives((openBlock(), createElementBlock("div", _hoisted_614, [
        createVNode($setup["LiveBoard"])
      ], 512)), [
        [vShow, $setup.tab === "live"]
      ]) : createCommentVNode("v-if", true),
      $setup.sprintLoaded ? withDirectives((openBlock(), createElementBlock("div", _hoisted_713, [
        createVNode($setup["SprintTab"])
      ], 512)), [
        [vShow, $setup.tab === "sprint"]
      ]) : createCommentVNode("v-if", true),
      $setup.wipLoaded ? withDirectives((openBlock(), createElementBlock("div", _hoisted_812, [
        createVNode($setup["ProjectWip"])
      ], 512)), [
        [vShow, $setup.tab === "wip"]
      ]) : createCommentVNode("v-if", true)
    ]);
  }
  var _hoisted_150, _hoisted_227, _hoisted_321, _hoisted_415, _hoisted_514, _hoisted_614, _hoisted_713, _hoisted_812;
  var init_ItDashboard2 = __esm({
    "sfc-template:/home/frappe/teampro-bench/apps/teampro/teampro/public/js/it_dashboard/ItDashboard.vue?type=template"() {
      init_vue_runtime_esm_bundler();
      _hoisted_150 = { class: "itd" };
      _hoisted_227 = { class: "itd-header" };
      _hoisted_321 = { class: "itd-tabs" };
      _hoisted_415 = { class: "itd-clock" };
      _hoisted_514 = { class: "itd-page" };
      _hoisted_614 = {
        key: 0,
        class: "itd-page"
      };
      _hoisted_713 = {
        key: 1,
        class: "itd-page"
      };
      _hoisted_812 = {
        key: 2,
        class: "itd-page"
      };
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/ItDashboard.vue
  var ItDashboard_default2;
  var init_ItDashboard3 = __esm({
    "../teampro/teampro/public/js/it_dashboard/ItDashboard.vue"() {
      init_ItDashboard();
      init_ItDashboard2();
      ItDashboard_default.render = render22;
      ItDashboard_default.__file = "../teampro/teampro/public/js/it_dashboard/ItDashboard.vue";
      ItDashboard_default2 = ItDashboard_default;
    }
  });

  // ../teampro/teampro/public/js/it_dashboard/it_dashboard.bundle.js
  var require_it_dashboard_bundle = __commonJS({
    "../teampro/teampro/public/js/it_dashboard/it_dashboard.bundle.js"() {
      init_vue_runtime_esm_bundler();
      init_ItDashboard3();
      var app = null;
      frappe.it_dashboard = {
        mount(wrapper) {
          this.unmount();
          const el = document.createElement("div");
          el.className = "itd-host";
          wrapper.appendChild(el);
          app = createApp(ItDashboard_default2);
          SetVueGlobals(app);
          app.mount(el);
        },
        unmount() {
          if (app) {
            app.unmount();
            app = null;
          }
        }
      };
    }
  });
  require_it_dashboard_bundle();
})();
/**
* @vue/reactivity v3.5.29
* (c) 2018-present Yuxi (Evan) You and Vue contributors
* @license MIT
**/
/**
* @vue/runtime-core v3.5.29
* (c) 2018-present Yuxi (Evan) You and Vue contributors
* @license MIT
**/
/**
* @vue/runtime-dom v3.5.29
* (c) 2018-present Yuxi (Evan) You and Vue contributors
* @license MIT
**/
/**
* @vue/shared v3.5.29
* (c) 2018-present Yuxi (Evan) You and Vue contributors
* @license MIT
**/
/**
* vue v3.5.29
* (c) 2018-present Yuxi (Evan) You and Vue contributors
* @license MIT
**/
//# sourceMappingURL=it_dashboard.bundle.DT37G6CM.js.map
