// Lightweight Google Maps JavaScript API loader (Places library)
// Ensures the script is loaded only once across the app.

let loadPromise = null;

export function loadGoogleMaps(apiKey) {
  if (typeof window !== "undefined" && window.google && window.google.maps) {
    return Promise.resolve(window.google);
  }

  if (loadPromise) return loadPromise;

  loadPromise = new Promise((resolve, reject) => {
    try {
      const existing = document.querySelector(
        'script[data-source="google-maps-js"]'
      );
      if (existing) {
        existing.addEventListener("load", () => resolve(window.google));
        existing.addEventListener("error", reject);
        return;
      }

      const script = document.createElement("script");
      script.type = "text/javascript";
      script.async = true;
      script.defer = true;
      script.dataset.source = "google-maps-js";
      const libs = "maps,places,marker"; // Load maps, places, and marker libraries
      // Add loading=async per Google best-practice to avoid blocking
      script.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(
        apiKey
      )}&libraries=${libs}&v=weekly&loading=async`;
      script.onload = () => resolve(window.google);
      script.onerror = (e) => reject(e);
      document.head.appendChild(script);
    } catch (err) {
      reject(err);
    }
  });

  return loadPromise;
}
