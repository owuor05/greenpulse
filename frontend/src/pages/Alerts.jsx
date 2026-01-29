import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { loadGoogleMaps } from "../utils/googleMaps";
import KenyaRiskMap from "../components/KenyaRiskMap";

function Alerts() {
  // Land Data Explorer state
  const [landLocation, setLandLocation] = useState("");
  const [landData, setLandData] = useState(null);
  const [landLoading, setLandLoading] = useState(false);
  const [landError, setLandError] = useState("");
  const inputRef = useRef(null);
  const autocompleteRef = useRef(null);

  useEffect(() => {
    // Scroll to top when component mounts
    window.scrollTo(0, 0);
    // Initialize Google Places Autocomplete on the land location input
    const key = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
    if (key) {
      loadGoogleMaps(key)
        .then((google) => {
          if (!inputRef.current || autocompleteRef.current) return;
          // Guard: Autocomplete may not be available for new customers; fallback gracefully
          if (!google?.maps?.places?.Autocomplete) {
            console.error('Places Autocomplete failed to load - check API key and billing');
            return; // plain input works
          }
          const options = {
            fields: ["formatted_address", "geometry", "name"],
            componentRestrictions: { country: "KE" },
          };
          autocompleteRef.current = new google.maps.places.Autocomplete(
            inputRef.current,
            options
          );
          autocompleteRef.current.addListener("place_changed", () => {
            const place = autocompleteRef.current.getPlace();
            const value = place?.formatted_address || place?.name;
            if (value) setLandLocation(value);
          });
        })
        .catch((err) => {
          // Non-blocking: log and continue without autocomplete
          console.warn("Google Maps script load failed:", err);
        });
    }
  }, []);

  const handleCountyClick = (countyName, countyData) => {
    // When user clicks "Analyze Land Data" on a county marker
    setLandLocation(countyName);
    setLandError(""); // Clear any previous errors
    setLandData(null); // Clear previous data
    
    // Scroll to Land Data Explorer section (above the map)
    const landDataSection = document.getElementById('land-data-explorer');
    if (landDataSection) {
      landDataSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    // Auto-trigger the analysis with the county name directly
    setTimeout(() => {
      analyzeCounty(countyName);
    }, 600);
  };

  const analyzeCounty = async (locationName) => {
    console.log('Analyzing county:', locationName);
    setLandLoading(true);
    setLandError("");

    try {
      console.log('Sending request to:', "https://terraguard-api.onrender.com/api/land-data/analyze");
      console.log('With location:', locationName);
      
      const response = await axios.post(
        "https://terraguard-api.onrender.com/api/land-data/analyze",
        { location: locationName }
      );
      
      console.log('Response received:', response.data);
      setLandData(response.data.data);
    } catch (error) {
      console.error('Full error:', error);
      console.error('Error response:', error.response);
      setLandError(
        error.response?.data?.detail || "Failed to analyze location. Please try again."
      );
      console.error("Error fetching land data:", error);
    } finally {
      setLandLoading(false);
    }
  };

  const fetchLandData = async (e) => {
    e.preventDefault();
    if (!landLocation.trim()) {
      setLandError("Please enter a location");
      return;
    }

    setLandLoading(true);
    setLandError("");
    setLandData(null);

    try {
      const response = await axios.post(
        "https://terraguard-api.onrender.com/api/land-data/analyze",
        { location: landLocation.trim() }
      );
      setLandData(response.data.data);
    } catch (error) {
      setLandError(
        error.response?.data?.detail || "Failed to analyze location. Please try again."
      );
      console.error("Error fetching land data:", error);
    } finally {
      setLandLoading(false);
    }
  };

  const getRiskColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case "critical":
      case "high":
        return "text-red-600";
      case "moderate":
      case "medium":
        return "text-yellow-600";
      case "low":
        return "text-green-600";
      default:
        return "text-gray-600";
    }
  };

  const getRiskBgColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case "critical":
      case "high":
        return "bg-red-50 border-red-200";
      case "moderate":
      case "medium":
        return "bg-yellow-50 border-yellow-200";
      case "low":
        return "bg-green-50 border-green-200";
      default:
        return "bg-gray-50 border-gray-200";
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-600 to-green-700 text-white py-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            Active Climate Alerts
          </h1>
          <p className="text-xl md:text-2xl text-green-100">
            Real-time warnings for drought, floods, and extreme weather across
            Kenya
          </p>
        </div>
      </div>

      {/* Filters removed as requested */}

      {/* Land Data Explorer Section */}
      <div id="land-data-explorer" className="bg-white py-16 px-4 border-t-4 border-green-600">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-10">
            <h2 className="text-4xl md:text-5xl font-bold mb-4 text-gray-900">
              Land Data Explorer
            </h2>
            <p className="text-xl text-gray-700">
              Get comprehensive climate data, risk analysis, and AI-powered insights for any location in Kenya
            </p>
            <p className="text-sm text-gray-600 mt-3 max-w-3xl mx-auto">
              Critical areas are identified using NASA POWER data: <strong>Drought</strong> (less than 2mm daily rainfall + 20+ days without rain) and <strong>Flood</strong> (100mm+ daily rainfall or 5+ heavy rain days)
            </p>
          </div>

          {/* Search Form */}
          <form onSubmit={fetchLandData} className="max-w-2xl mx-auto mb-8">
            <div className="flex flex-col md:flex-row gap-3">
              <input
                type="text"
                value={landLocation}
                onChange={(e) => setLandLocation(e.target.value)}
                placeholder="Enter location (e.g., Nairobi, Kitui, Webuye...)"
                className="flex-1 px-6 py-4 text-lg rounded-lg border-2 border-green-500 focus:border-green-600 focus:outline-none focus:ring-2 focus:ring-green-200"
                disabled={landLoading}
                ref={inputRef}
              />
              <button
                type="submit"
                disabled={landLoading}
                className="bg-green-600 hover:bg-green-700 text-white px-8 py-4 rounded-lg font-bold text-lg transition disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
              >
                {landLoading ? "Analyzing..." : "Analyze"}
              </button>
            </div>
          </form>

          {/* Error Message */}
          {landError && (
            <div className="max-w-2xl mx-auto mb-8 bg-red-50 border-2 border-red-400 rounded-lg p-4 text-center">
              <p className="text-red-800 font-semibold">{landError}</p>
            </div>
          )}

          {/* Loading State */}
          {landLoading && (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
              <p className="mt-4 text-gray-700">Fetching climate data from NASA POWER...</p>
            </div>
          )}

          {/* Land Data Results */}
          {landData && !landLoading && (
            <div className="max-w-6xl mx-auto">
              {/* Location Header */}
              <div className="bg-gradient-to-r from-green-600 to-emerald-600 rounded-t-xl p-6 border-2 border-green-500 shadow-lg">
                <h3 className="text-3xl font-bold mb-2 text-white">
                  {landData.location_name.charAt(0).toUpperCase() + landData.location_name.slice(1)}
                </h3>
                <p className="text-green-100 text-lg">
                  Coordinates: {landData.latitude?.toFixed(4) || 'N/A'}°, {landData.longitude?.toFixed(4) || 'N/A'}°
                </p>
                {landData.cached && (
                  <p className="text-green-200 text-sm mt-2">Cached data (updated within 24 hours)</p>
                )}
              </div>

              {/* Main Data Grid */}
              <div className="bg-gray-50 border-x-2 border-green-500 p-6 shadow-lg">
                {/* Temperature Card */}
                <div className="bg-white border-2 border-green-300 rounded-xl p-6 mb-6 shadow-md">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <p className="text-sm text-gray-600 mb-1 font-semibold">Current Temperature</p>
                      <p className="text-5xl font-bold text-green-700">
                        {landData.current_temperature_celsius != null ? landData.current_temperature_celsius.toFixed(1) : 'N/A'}°C
                      </p>
                    </div>
                  </div>
                  <div className="mt-4 pt-4 border-t border-gray-200 grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600">Avg Max Temp (30d)</p>
                      <p className="text-lg font-bold text-gray-800">
                        {landData.historical_data?.avg_max_temperature_c != null ? landData.historical_data.avg_max_temperature_c.toFixed(1) : 'N/A'}°C
                      </p>
                    </div>
                    <div>
                      <p className="text-gray-600">Avg Precipitation (30d)</p>
                      <p className="text-lg font-bold text-gray-800">
                        {landData.historical_data?.avg_precipitation_mm != null ? landData.historical_data.avg_precipitation_mm.toFixed(1) : 'N/A'} mm/day
                      </p>
                    </div>
                  </div>
                </div>

                {/* Climate Risks Grid */}
                <div className="grid md:grid-cols-2 gap-6 mb-6">
                  {/* Drought Risk */}
                  <div className={`border-2 rounded-xl p-6 shadow-md ${
                    landData.climate_risks.drought.severity.toLowerCase() === 'critical' || 
                    landData.climate_risks.drought.severity.toLowerCase() === 'high'
                      ? 'bg-red-50 border-red-400'
                      : getRiskBgColor(landData.climate_risks.drought.severity)
                  }`}>
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="text-xl font-bold text-gray-900">Drought Risk</h4>
                      <span className={`text-2xl font-bold px-4 py-1 rounded-lg ${
                        landData.climate_risks.drought.severity.toLowerCase() === 'critical' || 
                        landData.climate_risks.drought.severity.toLowerCase() === 'high'
                          ? 'bg-red-600 text-white'
                          : getRiskColor(landData.climate_risks.drought.severity)
                      }`}>
                        {landData.climate_risks.drought.severity.toUpperCase()}
                      </span>
                    </div>
                    <div className="space-y-3 text-sm">
                      <div className="flex justify-between bg-white p-2 rounded">
                        <span className="text-gray-600">Avg Precipitation:</span>
                        <span className="font-bold text-gray-900">
                          {landData.climate_risks?.drought?.avg_precipitation_mm != null ? landData.climate_risks.drought.avg_precipitation_mm.toFixed(2) : 'N/A'} mm/day
                        </span>
                      </div>
                      <div className="flex justify-between bg-white p-2 rounded">
                        <span className="text-gray-600">Days Without Rain:</span>
                        <span className="font-bold text-gray-900">
                          {landData.climate_risks?.drought?.days_without_rain || 0} / {landData.climate_risks?.drought?.total_days_analyzed || 30}
                        </span>
                      </div>
                      <div className="flex justify-between bg-white p-2 rounded">
                        <span className="text-gray-600">Avg Max Temperature:</span>
                        <span className="font-bold text-gray-900">
                          {landData.climate_risks?.drought?.avg_max_temperature_c != null ? landData.climate_risks.drought.avg_max_temperature_c.toFixed(1) : 'N/A'}°C
                        </span>
                      </div>
                    </div>
                    {(landData.climate_risks.drought.severity.toLowerCase() === 'critical' || 
                      landData.climate_risks.drought.severity.toLowerCase() === 'high') && (
                      <div className="mt-4 pt-3 border-t border-red-300">
                        <p className="text-red-800 font-semibold text-sm">
                          WARNING: Critical Threshold: &lt;2mm daily rain + 20+ dry days
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Flood Risk */}
                  <div className={`border-2 rounded-xl p-6 shadow-md ${
                    landData.climate_risks.flood.severity.toLowerCase() === 'critical' || 
                    landData.climate_risks.flood.severity.toLowerCase() === 'high'
                      ? 'bg-red-50 border-red-400'
                      : getRiskBgColor(landData.climate_risks.flood.severity)
                  }`}>
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="text-xl font-bold text-gray-900">Flood Risk</h4>
                      <span className={`text-2xl font-bold px-4 py-1 rounded-lg ${
                        landData.climate_risks.flood.severity.toLowerCase() === 'critical' || 
                        landData.climate_risks.flood.severity.toLowerCase() === 'high'
                          ? 'bg-red-600 text-white'
                          : getRiskColor(landData.climate_risks.flood.severity)
                      }`}>
                        {landData.climate_risks.flood.severity.toUpperCase()}
                      </span>
                    </div>
                    <div className="space-y-3 text-sm">
                      <div className="flex justify-between bg-white p-2 rounded">
                        <span className="text-gray-600">Total Precipitation:</span>
                        <span className="font-bold text-gray-900">
                          {landData.climate_risks?.flood?.total_precipitation_mm != null ? landData.climate_risks.flood.total_precipitation_mm.toFixed(1) : 'N/A'} mm
                        </span>
                      </div>
                      <div className="flex justify-between bg-white p-2 rounded">
                        <span className="text-gray-600">Max Daily Rainfall:</span>
                        <span className="font-bold text-gray-900">
                          {landData.climate_risks?.flood?.max_daily_precipitation_mm != null ? landData.climate_risks.flood.max_daily_precipitation_mm.toFixed(1) : 'N/A'} mm
                        </span>
                      </div>
                      <div className="flex justify-between bg-white p-2 rounded">
                        <span className="text-gray-600">Heavy Rain Days:</span>
                        <span className="font-bold text-gray-900">
                          {landData.climate_risks?.flood?.heavy_rain_days || 0} / {landData.climate_risks?.flood?.total_days_analyzed || 30}
                        </span>
                      </div>
                    </div>
                    {(landData.climate_risks.flood.severity.toLowerCase() === 'critical' || 
                      landData.climate_risks.flood.severity.toLowerCase() === 'high') && (
                      <div className="mt-4 pt-3 border-t border-red-300">
                        <p className="text-red-800 font-semibold text-sm">
                          WARNING: Critical Threshold: 100mm+ daily OR 5+ heavy rain days
                        </p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Active Alerts */}
                {landData.active_alerts.length > 0 ? (
                  <div className="bg-red-50 border-2 border-red-400 rounded-xl p-6 mb-6 shadow-md">
                    <h4 className="text-xl font-bold text-red-800 mb-4">
                      Active Alerts ({landData.active_alerts.length})
                    </h4>
                    <div className="space-y-3">
                      {landData.active_alerts.map((alert, index) => (
                        <div key={index} className="bg-white border-2 border-red-300 rounded-lg p-4 shadow">
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-bold text-gray-900">{alert.risk_type.toUpperCase()}</span>
                            <span className="bg-red-600 text-white px-3 py-1 rounded-full text-xs font-bold">
                              {alert.severity.toUpperCase()}
                            </span>
                          </div>
                          <p className="text-gray-800">{alert.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="bg-green-50 border-2 border-green-400 rounded-xl p-6 mb-6 text-center shadow-md">
                    <p className="text-green-800 font-bold text-lg">No Active Alerts</p>
                    <p className="text-green-700 mt-1">Climate conditions are stable in this location</p>
                  </div>
                )}

                {/* AI Summary */}
                <div className="bg-white border-2 border-green-400 rounded-xl p-6 shadow-md">
                  <h4 className="text-xl font-bold text-gray-900 mb-4">
                    AI-Powered Conservation Analysis
                  </h4>
                  <div className="text-gray-800 leading-relaxed text-base whitespace-pre-line">
                    {landData.ai_summary}
                  </div>
                  <div className="mt-6 pt-4 border-t border-gray-200 text-sm text-gray-600">
                    <p>Data Source: {landData.data_source} | Last 30 days analyzed</p>
                    <p className="mt-1">Analyzed: {new Date(landData.analyzed_at).toLocaleString()}</p>
                  </div>
                </div>
              </div>

              {/* Footer Actions */}
              <div className="bg-green-600 border-2 border-green-500 rounded-b-xl p-6 text-center shadow-lg">
                <p className="text-white mb-4 text-lg">Want real-time alerts for this location?</p>
                <Link
                  to="/#subscribe"
                  className="inline-block bg-white hover:bg-gray-100 text-green-700 px-8 py-3 rounded-lg font-bold transition shadow-md hover:shadow-lg"
                >
                  Subscribe for Free Alerts
                </Link>
              </div>
            </div>
          )}

          {/* Info Section */}
          {!landData && !landLoading && (
            <div className="max-w-4xl mx-auto text-center mt-12">
              <div className="grid md:grid-cols-3 gap-6 text-left">
                <div className="bg-white border-2 border-green-500 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-2 text-green-600">Real NASA Data</h4>
                  <p className="text-gray-700 text-sm">
                    30 days of temperature and precipitation data from NASA POWER
                  </p>
                </div>
                <div className="bg-white border-2 border-green-500 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-2 text-green-600">Risk Analysis</h4>
                  <p className="text-gray-700 text-sm">
                    Automated drought and flood risk detection with severity levels
                  </p>
                </div>
                <div className="bg-white border-2 border-green-500 rounded-xl p-6 shadow-md">
                  <h4 className="font-bold text-lg mb-2 text-green-600">AI Insights</h4>
                  <p className="text-gray-700 text-sm">
                    Practical recommendations from AI for farmers and land managers
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Kenya Risk Map Section */}
      <div className="bg-gray-50 py-16 px-4 border-t-4 border-green-600">
        <div className="max-w-7xl mx-auto">
          <KenyaRiskMap onCountyClick={handleCountyClick} />
        </div>
      </div>

      {/* Info Section */}
      <div className="bg-green-50 border-t-4 border-green-600 py-12 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-2xl font-bold text-gray-800 mb-4">
            Want alerts delivered to your phone?
          </h3>
          <p className="text-gray-700 mb-6 text-lg">
            Subscribe to receive instant notifications when new alerts are
            issued for your region via Telegram or WhatsApp.
          </p>
          <Link
            to="/#subscribe"
            className="inline-block bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition"
          >
            Subscribe Now - It's Free!
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Alerts;
