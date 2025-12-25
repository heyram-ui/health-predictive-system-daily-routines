// static/js/service-worker.js
const CACHE_NAME = 'healthpredict-v1';
const urlsToCache = [
  '/',
  '/dashboard',
  '/static/css/styles.css',
  '/static/js/app.js',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});