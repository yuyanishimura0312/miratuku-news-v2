'use strict';

// ==============================================================
// IndexedDB Cache (stale-while-revalidate)
// ==============================================================
var IDB_NAME = 'miratuku-news-cache';
var IDB_STORE = 'json-data';
var IDB_VERSION = 1;
// Max age before background revalidation (5 min); data is shown immediately from cache
var CACHE_MAX_AGE_MS = 5 * 60 * 1000;

var _idb = null;
function openIDB() {
  if (_idb) return Promise.resolve(_idb);
  return new Promise(function(resolve, reject) {
    var req = indexedDB.open(IDB_NAME, IDB_VERSION);
    req.onupgradeneeded = function() { req.result.createObjectStore(IDB_STORE); };
    req.onsuccess = function() { _idb = req.result; resolve(_idb); };
    req.onerror = function() { resolve(null); };
  });
}
async function idbGet(key) {
  try {
    var db = await openIDB();
    if (!db) return null;
    return new Promise(function(resolve) {
      var tx = db.transaction(IDB_STORE, 'readonly');
      var req = tx.objectStore(IDB_STORE).get(key);
      req.onsuccess = function() { resolve(req.result || null); };
      req.onerror = function() { resolve(null); };
    });
  } catch(e) { return null; }
}
async function idbSet(key, value) {
  try {
    var db = await openIDB();
    if (!db) return;
    var tx = db.transaction(IDB_STORE, 'readwrite');
    tx.objectStore(IDB_STORE).put(value, key);
  } catch(e) {}
}

// ==============================================================
// DATA FETCHING
// ==============================================================
async function fetchJSON(filename) {
  if (dataCache[filename]) return dataCache[filename];

  // 1. Try IndexedDB cache first (instant display for returning visitors)
  var cached = await idbGet(filename);
  var now = Date.now();
  if (cached && cached.data) {
    dataCache[filename] = cached.data;
    // If cache is fresh enough, skip network entirely
    if (cached.ts && (now - cached.ts) < CACHE_MAX_AGE_MS) {
      return cached.data;
    }
    // Cache is stale: return it now, revalidate in background
    _revalidate(filename, cached.etag, cached.lastMod);
    return cached.data;
  }

  // 2. No cache — fetch from network (first visit)
  return _fetchAndCache(filename);
}

async function _fetchAndCache(filename) {
  try {
    var res = await fetch(DATA_BASE + '/' + filename + cacheBust());
    if (!res.ok) throw new Error('HTTP ' + res.status);
    var data = await res.json();
    dataCache[filename] = data;
    // Store in IndexedDB with metadata
    idbSet(filename, {
      data: data,
      ts: Date.now(),
      etag: res.headers.get('etag') || '',
      lastMod: res.headers.get('last-modified') || ''
    });
    return data;
  } catch (e) { console.error('Failed to fetch ' + filename + ':', e); return null; }
}

function _revalidate(filename, etag, lastMod) {
  // Background revalidation — don't block rendering
  var headers = {};
  if (etag) headers['If-None-Match'] = etag;
  if (lastMod) headers['If-Modified-Since'] = lastMod;

  // No cacheBust here — conditional requests need stable URLs for 304 responses
  fetch(DATA_BASE + '/' + filename, { headers: headers })
    .then(function(res) {
      if (res.status === 304) {
        // Not modified — just refresh timestamp
        idbGet(filename).then(function(c) {
          if (c) { c.ts = Date.now(); idbSet(filename, c); }
        });
        return;
      }
      if (!res.ok) return;
      return res.json().then(function(data) {
        dataCache[filename] = data;
        idbSet(filename, {
          data: data,
          ts: Date.now(),
          etag: res.headers.get('etag') || '',
          lastMod: res.headers.get('last-modified') || ''
        });
      });
    })
    .catch(function() {}); // Silently fail — stale data is already displayed
}

// Simple local JSON fetch (for files in data/ directory, not DATA_BASE)
function _fetchLocalJSON(path) {
  return fetch(path + '?v=' + Date.now()).then(function(r) { return r.ok ? r.json() : null; }).catch(function() { return null; });
}
