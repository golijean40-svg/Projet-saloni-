importScripts('https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.23.0/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyD2V04148tPm3Yit-Gwj3aR6ybeLcciAI",
  authDomain: "saloni-manager-1c0d3.firebaseapp.com",
  projectId: "saloni-manager-1c0d3",
  storageBucket: "saloni-manager-1c0d3.firebasestorage.app",
  messagingSenderId: "372199257115",
  appId: "1:372199257115:web:7e2aaacd4b30900acdb4be"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  const notifTitle = payload.notification.title || 'Saloni Manager';
  const notifOptions = {
    body: payload.notification.body || '',
    icon: './icon-192.png',
    badge: './icon-192.png',
    vibrate: [200, 100, 200]
  };
  self.registration.showNotification(notifTitle, notifOptions);
});

self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window' }).then(function(clientList) {
      for (var client of clientList) {
        if ('focus' in client) return client.focus();
      }
      if (clients.openWindow) return clients.openWindow('./index.html');
    })
  );
});
