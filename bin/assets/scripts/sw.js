importScripts('https://cdnjs.cloudflare.com/ajax/libs/localforage/1.10.0/localforage.min.js');

const NEW_URL = location.origin + '/new';

self.addEventListener('install', () => {
  console.log('Installed Service Worker.');
  self.skipWaiting();
});
self.addEventListener('activate', () => self.clients.claim());

// As the redirection mode of the form POST request
// is 'manual', we cannot get the the redirection URL
// from the request (opaqueredirect). A trick, is to store
// the event.request.resultingClientId, which seems to be
// the same only for the form POST request and the fetch
// of the redirection URL. This allows us to intercept
// the correct redirection URL request and thus obtain
// the ID.
const tokens = new Map();
self.addEventListener('fetch', (event) => {
  let token;
  // Intercept the request when the form is submitted
  if (event.request.url === NEW_URL && event.request.method === 'POST') {
    event.respondWith(fetch(event.request.clone()).then(async (response) => {
      // Store the resultingClientId only if the request is successful.
      if (response.type === 'opaqueredirect') {
        tokens.set(event.request.resultingClientId,
                   new URLSearchParams(await event.request.text()).get('token'));
      }
      return response;
    }));

  // If the request's resultingClientId is the same as
  // the submitted form request's resultingClientId,
  // then this request is the fetch of the redirection URL.
  } else if (token = tokens.get(event.request.resultingClientId)) {
    tokens.delete(event.request.resultingClientId);
    localforage.setItem(event.request.url.slice(event.request.url.lastIndexOf('/') + 1,
                                                event.request.url.lastIndexOf('.')), token);
  }
});
