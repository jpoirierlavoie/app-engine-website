// This is the service worker with the Cache-first network
// Check compatibility for the browser we're running this in
if ("serviceWorker" in navigator) {
  if (navigator.serviceWorker.controller) {
    console.log("CLIENT: Active service worker found, no need to register.");
    // Register the service worker
  } else {
    console.log("CLIENT: Service worker registration in progress.");
    navigator.serviceWorker.register("/service-worker.js").then(function() {
      console.log("CLIENT: Service worker registration complete.");},
        function() {
          console.log("CLIENT: Service worker registration failure.");}
        );
      }
    }
else {console.log("CLIENT: Browser does not support service workers.");}
