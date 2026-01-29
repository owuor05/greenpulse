import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { alertsService } from "../services/api";
import axios from "axios";

function AlertDetail() {
  const { id } = useParams();
  const [alert, setAlert] = useState(null);
  const [landData, setLandData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    // Scroll to top when component mounts
    window.scrollTo(0, 0);
    fetchAlertDetails();
  }, [id]);

  const fetchAlertDetails = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await alertsService.getAlertById(id);
      // API returns { success, alert }
      const alertObj = data?.alert || data;
      setAlert(alertObj);
      
      // Fetch comprehensive land data for this alert's region
      if (alertObj?.region) {
        try {
          const landResponse = await axios.post(
            "https://terraguard-api.onrender.com/api/land-data/analyze",
            { location: alertObj.region }
          );
          setLandData(landResponse.data.data);
        } catch (landErr) {
          console.warn("Could not fetch land data:", landErr);
          // Non-blocking - continue showing alert even if land data fails
        }
      }
    } catch (error) {
      setError("Failed to load alert details. Please try again.");
      console.error("Error fetching alert:", error);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case "critical":
      case "high":
      case "severe":
        return "bg-red-700";
      case "medium":
      case "moderate":
        return "bg-orange-600";
      case "low":
      case "mild":
        return "bg-yellow-600";
      default:
        // Fallback to red to emphasize alert context
        return "bg-red-700";
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

  // Normalize arrays to avoid .map on non-array values
  const getArray = (val) => (Array.isArray(val) ? val : []);

  // Try to parse JSON-like strings safely (handles single-quote JSON heuristically)
  const parseMaybeJson = (val) => {
    if (typeof val !== "string") return val;
    const s = val.trim();
    if (!s) return s;
    const looksJson = (s.startsWith("{") && s.endsWith("}")) || (s.startsWith("[") && s.endsWith("]"));
    if (!looksJson) return val;
    try {
      return JSON.parse(s);
    } catch (_) {
      try {
        const dq = s
          .replace(/'\s*:/g, '":')
          .replace(/:\s*'/g, ':"')
          .replace(/'/g, '"');
        return JSON.parse(dq);
      } catch (_) {
        return val; // give up, return raw string
      }
    }
  };

  // Normalize AI summary to a readable string
  const getAiSummary = () => {
    const v = alert?.ai_summary;
    if (!v) return null;
    const parsed = parseMaybeJson(v);
    if (typeof parsed === "object" && parsed) {
      if (typeof parsed.summary === "string") return parsed.summary;
      if (typeof parsed.text === "string") return parsed.text;
      const firstString = Object.values(parsed).find((x) => typeof x === "string");
      return firstString || null;
    }
    return typeof parsed === "string" ? parsed : null;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center font-sans">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-2 border-green-600"></div>
          <p className="mt-4 text-gray-600 text-lg">Loading alert details...</p>
        </div>
      </div>
    );
  }

  if (error || !alert) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4 font-sans">
        <div className="bg-red-50 border-2 border-red-300 rounded-lg p-8 max-w-md text-center">
          <p className="text-red-800 text-lg mb-4">
            {error || "Alert not found"}
          </p>
          <Link
            to="/alerts"
            className="inline-block bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition"
          >
            Back to Alerts
          </Link>
        </div>
      </div>
    );
  }

  // Helper: safely derive a plain summary from description (JSON or string)
  const getCleanDescription = () => {
    if (!alert?.description) return null;
    const raw = alert.description;
    const parsed = parseMaybeJson(raw);
    if (typeof parsed === "object" && parsed) {
      if (typeof parsed.summary === "string") return parsed.summary;
      try {
        return Object.values(parsed)
          .filter((v) => typeof v === "string")
          .join(" \n");
      } catch (_) {
        return String(raw);
      }
    }
    return typeof parsed === "string" ? parsed : String(parsed);
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      {/* Header */}
      <div
        className={`${getSeverityColor(alert.severity)} text-white py-16 px-4`}
      >
        <div className="max-w-4xl mx-auto">
          <Link to="/alerts" className="inline-block text-white/90 hover:text-white underline mb-4">
            Back to all alerts
          </Link>
          <div className="flex items-center gap-4 mb-4">
            <div>
              <h1 className="text-4xl font-bold mb-2">{alert.title}</h1>
              <div className="flex flex-wrap gap-2 mt-2">
                <span className="bg-white/15 px-3 py-1 rounded text-sm">Region: {alert.region}</span>
                <span className="bg-white/15 px-3 py-1 rounded text-sm capitalize">Risk: {alert.risk_type}</span>
                <span className="bg-white/15 px-3 py-1 rounded text-sm uppercase font-semibold">{alert.severity} severity</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto py-12 px-4">
        {/* Show comprehensive Land Data if available */}
        {landData && (
          <>
            {/* Temperature Card */}
            <div className="bg-white border-2 border-green-300 rounded-xl p-6 mb-6 shadow-md">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <p className="text-sm text-gray-600 mb-1 font-semibold">Current Temperature</p>
                  <p className="text-5xl font-bold text-green-700">
                    {landData.current_temperature_celsius.toFixed(1)}°C
                  </p>
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-gray-200 grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-600">Avg Max Temp (30d)</p>
                  <p className="text-lg font-bold text-gray-800">
                    {landData.historical_data.avg_max_temperature_c.toFixed(1)}°C
                  </p>
                </div>
                <div>
                  <p className="text-gray-600">Avg Precipitation (30d)</p>
                  <p className="text-lg font-bold text-gray-800">
                    {landData.historical_data.avg_precipitation_mm.toFixed(1)} mm/day
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
                      {landData.climate_risks.drought.avg_precipitation_mm.toFixed(2)} mm/day
                    </span>
                  </div>
                  <div className="flex justify-between bg-white p-2 rounded">
                    <span className="text-gray-600">Days Without Rain:</span>
                    <span className="font-bold text-gray-900">
                      {landData.climate_risks.drought.days_without_rain} / {landData.climate_risks.drought.total_days_analyzed}
                    </span>
                  </div>
                  <div className="flex justify-between bg-white p-2 rounded">
                    <span className="text-gray-600">Avg Max Temperature:</span>
                    <span className="font-bold text-gray-900">
                      {landData.climate_risks.drought.avg_max_temperature_c.toFixed(1)}°C
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
                      {landData.climate_risks.flood.total_precipitation_mm.toFixed(1)} mm
                    </span>
                  </div>
                  <div className="flex justify-between bg-white p-2 rounded">
                    <span className="text-gray-600">Max Daily Rainfall:</span>
                    <span className="font-bold text-gray-900">
                      {landData.climate_risks.flood.max_daily_precipitation_mm.toFixed(1)} mm
                    </span>
                  </div>
                  <div className="flex justify-between bg-white p-2 rounded">
                    <span className="text-gray-600">Heavy Rain Days:</span>
                    <span className="font-bold text-gray-900">
                      {landData.climate_risks.flood.heavy_rain_days} / {landData.climate_risks.flood.total_days_analyzed}
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

            {/* AI Summary */}
            <div className="bg-white border-2 border-green-400 rounded-xl p-6 shadow-md mb-6">
              <h4 className="text-xl font-bold text-gray-900 mb-4">
                AI-Powered Insights & Recommendations
              </h4>
              <p className="text-gray-800 leading-relaxed text-lg">
                {landData.ai_summary}
              </p>
              <div className="mt-4 pt-4 border-t border-gray-200 text-sm text-gray-600">
                <p>Data Source: {landData.data_source} | Last 30 days analyzed</p>
                <p className="mt-1">Analyzed: {new Date(landData.analyzed_at).toLocaleString()}</p>
              </div>
            </div>
          </>
        )}

        {/* Fallback: Show database description only if no land data */}
        {!landData && getCleanDescription() && (
          <div className="bg-white rounded-xl shadow-md p-8 mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Alert Description
            </h2>
            <p className="text-gray-800 text-lg leading-relaxed whitespace-pre-line">
              {getCleanDescription()}
            </p>
          </div>
        )}

        {/* Preventive Measures */}
        {getArray(alert.preventive_measures).length > 0 && (
          <div className="bg-green-50 rounded-xl shadow-md p-8 mb-6 border-2 border-green-300">
            <h2 className="text-2xl font-bold text-green-900 mb-4">
              Recommended Actions
            </h2>
            <p className="text-green-800 mb-4">
              Steps to protect your farm and community:
            </p>
            <ul className="list-disc pl-6 space-y-2">
              {getArray(alert.preventive_measures).map((measure, index) => (
                <li key={index} className="text-gray-800 text-lg">{measure}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Immediate Actions */}
        {getArray(alert.immediate_actions).length > 0 && (
          <div className="bg-red-50 rounded-xl shadow-md p-8 mb-6 border-2 border-red-300">
            <h2 className="text-2xl font-bold text-red-900 mb-4">
              Immediate Actions Required
            </h2>
            <p className="text-red-800 mb-4">Act now to minimize damage:</p>
            <ul className="list-disc pl-6 space-y-2">
              {getArray(alert.immediate_actions).map((action, index) => (
                <li key={index} className="text-gray-800 text-lg">{action}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Data Source - Only show if no land data */}
        {!landData && alert.data_source && (
          <div className="bg-blue-50 rounded-xl shadow-md p-8 mb-6 border-2 border-blue-300">
            <h2 className="text-2xl font-bold text-blue-900 mb-4">
              Data Source
            </h2>
            <div className="space-y-2 text-gray-800">
              {alert.data_source.api && (
                <p>
                  <strong>Source API:</strong> {alert.data_source.api}
                </p>
              )}
              {alert.data_source.rainfall_deficit && (
                <p>
                  <strong>Rainfall Deficit:</strong>{" "}
                  {alert.data_source.rainfall_deficit}
                </p>
              )}
              {alert.data_source.last_updated && (
                <p>
                  <strong>Last Updated:</strong>{" "}
                  {new Date(alert.data_source.last_updated).toLocaleString()}
                </p>
              )}
            </div>
          </div>
        )}

        {/* Metadata */}
        <div className="bg-white rounded-xl shadow-md p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            Alert Information
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-700">
            {alert.created_at && (
              <div>
                <p className="text-sm text-gray-500">Created</p>
                <p className="font-semibold">
                  {new Date(alert.created_at).toLocaleString("en-US", {
                    month: "long",
                    day: "numeric",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </p>
              </div>
            )}
            {alert.expires_at && (
              <div>
                <p className="text-sm text-gray-500">Expires</p>
                <p className="font-semibold">
                  {new Date(alert.expires_at).toLocaleString("en-US", {
                    month: "long",
                    day: "numeric",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Get Help Section */}
        <div className="mt-8 bg-gradient-to-r from-green-700 to-emerald-600 rounded-xl shadow-lg p-8 text-white">
          <h2 className="text-2xl font-bold mb-4">Need More Help?</h2>
          <p className="text-lg mb-6">
            Chat with our AI assistant for personalized advice about this alert:
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <a
              href="https://t.me/TerraGuard_Bot"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition text-center"
            >
              Chat on Telegram
            </a>
            <a
              href="https://wa.me/14155238886?text=join%20actual-mother"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white text-green-600 px-6 py-3 rounded-lg font-semibold hover:bg-green-50 transition text-center"
            >
              Chat on WhatsApp
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AlertDetail;
