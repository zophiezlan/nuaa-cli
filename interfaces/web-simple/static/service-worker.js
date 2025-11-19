/* ============================================
   Service Worker for PWA Support
   NUAA Web Tools
   ============================================ */

const CACHE_VERSION = "nuaa-tools-v2.0.0";
const STATIC_CACHE = `${CACHE_VERSION}-static`;
const DYNAMIC_CACHE = `${CACHE_VERSION}-dynamic`;
const IMAGE_CACHE = `${CACHE_VERSION}-images`;

// Assets to cache on install
const STATIC_ASSETS = [
  "/",
  "/static/css/main.css",
  "/static/css/dashboard.css",
  "/static/css/form.css",
  "/static/css/themes.css",
  "/static/js/main.js",
  "/static/js/dashboard.js",
  "/static/js/form.js",
  "/static/js/theme-switcher.js",
  "/static/js/version-history.js",
  "/static/js/keyboard-shortcuts.js",
  "/static/manifest.json",
  "/analytics",
  "/admin",
  "/offline",
];

// Install event - cache static assets
self.addEventListener("install", (event) => {
  console.log("[Service Worker] Installing...", CACHE_VERSION);

  event.waitUntil(
    caches
      .open(STATIC_CACHE)
      .then((cache) => {
        console.log("[Service Worker] Caching static assets");
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => self.skipWaiting())
      .catch((error) => {
        console.error("[Service Worker] Install failed:", error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener("activate", (event) => {
  console.log("[Service Worker] Activating...", CACHE_VERSION);

  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter(
              (name) =>
                name.startsWith("nuaa-tools-") &&
                name !== STATIC_CACHE &&
                name !== DYNAMIC_CACHE &&
                name !== IMAGE_CACHE
            )
            .map((name) => {
              console.log("[Service Worker] Deleting old cache:", name);
              return caches.delete(name);
            })
        );
      })
      .then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache, fall back to network
self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== "GET") {
    return;
  }

  // Skip chrome extensions
  if (url.protocol === "chrome-extension:") {
    return;
  }

  // Different strategies for different request types
  if (request.destination === "image") {
    event.respondWith(cacheFirst(request, IMAGE_CACHE));
  } else if (STATIC_ASSETS.includes(url.pathname)) {
    event.respondWith(cacheFirst(request, STATIC_CACHE));
  } else if (url.pathname.startsWith("/static/")) {
    event.respondWith(cacheFirst(request, STATIC_CACHE));
  } else if (url.pathname.startsWith("/api/")) {
    event.respondWith(networkFirst(request, DYNAMIC_CACHE));
  } else {
    event.respondWith(networkFirst(request, DYNAMIC_CACHE));
  }
});

// Cache-first strategy (for static assets)
async function cacheFirst(request, cacheName) {
  const cached = await caches.match(request);
  if (cached) {
    return cached;
  }

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    console.error("[Service Worker] Fetch failed:", error);
    return caches.match("/offline");
  }
}

// Network-first strategy (for dynamic content)
async function networkFirst(request, cacheName) {
  try {
    const response = await fetch(request);

    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }

    return response;
  } catch (error) {
    const cached = await caches.match(request);
    if (cached) {
      return cached;
    }

    // If it's a navigation request, show offline page
    if (request.mode === "navigate") {
      return caches.match("/offline");
    }

    return new Response("Network error", {
      status: 408,
      headers: { "Content-Type": "text/plain" },
    });
  }
}

// Background sync for offline submissions
self.addEventListener("sync", (event) => {
  console.log("[Service Worker] Background sync:", event.tag);

  if (event.tag === "sync-submissions") {
    event.waitUntil(syncSubmissions());
  }
});

async function syncSubmissions() {
  // Get pending submissions from IndexedDB
  // This would sync any forms submitted while offline
  console.log("[Service Worker] Syncing offline submissions...");

  // Implementation would go here - reading from IndexedDB and POSTing to server
}

// Push notifications (for future use)
self.addEventListener("push", (event) => {
  console.log("[Service Worker] Push received");

  const data = event.data ? event.data.json() : {};

  const options = {
    body: data.body || "New notification from NUAA Tools",
    icon: "/static/images/icon-192x192.png",
    badge: "/static/images/icon-72x72.png",
    vibrate: [200, 100, 200],
    data: {
      url: data.url || "/",
    },
    actions: [
      {
        action: "open",
        title: "Open",
      },
      {
        action: "close",
        title: "Close",
      },
    ],
  };

  event.waitUntil(
    self.registration.showNotification(data.title || "NUAA Tools", options)
  );
});

// Notification click handler
self.addEventListener("notificationclick", (event) => {
  event.notification.close();

  if (event.action === "open" || !event.action) {
    const urlToOpen = event.notification.data.url || "/";

    event.waitUntil(
      clients
        .matchAll({ type: "window", includeUncontrolled: true })
        .then((windowClients) => {
          // Check if there's already a window open
          for (let client of windowClients) {
            if (client.url === urlToOpen && "focus" in client) {
              return client.focus();
            }
          }
          // No window open, open a new one
          if (clients.openWindow) {
            return clients.openWindow(urlToOpen);
          }
        })
    );
  }
});

// Share target (when app receives shared content)
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  if (url.pathname === "/share" && event.request.method === "POST") {
    event.respondWith(handleShare(event.request));
  }
});

async function handleShare(request) {
  const formData = await request.formData();
  const title = formData.get("title") || "";
  const text = formData.get("text") || "";
  const url = formData.get("url") || "";
  const files = formData.getAll("media");

  // Store shared data in IndexedDB or cache
  // Then redirect to the app with the shared content

  return Response.redirect("/?shared=true", 303);
}

// Periodic background sync (for future use)
self.addEventListener("periodicsync", (event) => {
  if (event.tag === "update-content") {
    event.waitUntil(updateContent());
  }
});

async function updateContent() {
  // Update cached content in the background
  console.log("[Service Worker] Updating content in background...");
}

console.log("[Service Worker] Loaded", CACHE_VERSION);
