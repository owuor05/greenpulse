import { useState, useEffect, useRef } from "react";
import { supabase, isSupabaseConfigured } from "../lib/supabase";
import { loadGoogleMaps } from "../utils/googleMaps";

function Reports() {
  const [formData, setFormData] = useState({
    region: "",
    title: "",
    description: "",
    isAnonymous: false,
    name: "",
  });
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [reports, setReports] = useState([]);
  const [error, setError] = useState("");
  const [loadingReports, setLoadingReports] = useState(true);
  const [coords, setCoords] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileError, setFileError] = useState("");
  const inputRef = useRef(null);
  const fileInputRef = useRef(null);
  const autocompleteRef = useRef(null);

  // Helper: split a single description field into [title, body]
  const splitDescription = (desc) => {
    if (!desc || typeof desc !== "string") return ["Community Report", ""];
    // Prefer a blank-line separator (we store as: title + blank line + body)
    const parts = desc.split(/\n\s*\n/);
    if (parts.length >= 2) {
      const title = parts[0].trim();
      const body = parts.slice(1).join("\n\n").trim();
      return [title || "Community Report", body];
    }
    // Fallback: derive a title from the first ~12 words
    const words = desc.trim().split(/\s+/);
    const cutoff = Math.min(12, words.length);
    const titleWords = words.slice(0, cutoff);
    const bodyWords = words.slice(cutoff);
    let title = titleWords.join(" ");
    if (words.length > cutoff) title += " ...";
    const body = bodyWords.join(" ");
    return [title || "Community Report", body];
  };

  useEffect(() => {
    // Scroll to top when component mounts
    window.scrollTo(0, 0);
    fetchReports();
  }, []);

  // Initialize Google Places Autocomplete for the location input
  useEffect(() => {
    const key = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
    if (!key) return; // fallback to manual text input
    let listener = null;

    loadGoogleMaps(key)
      .then((google) => {
        if (!inputRef.current) return;
        if (!google?.maps?.places?.Autocomplete) {
          console.warn(
            "Google Maps loaded but Places library is unavailable. Ensure Places API is enabled for your key."
          );
          return; // keep plain text input
        }

        const ac = new google.maps.places.Autocomplete(inputRef.current, {
          fields: [
            "address_components",
            "geometry",
            "formatted_address",
            "name",
          ],
          types: ["geocode"],
        });
        autocompleteRef.current = ac;
        listener = ac.addListener("place_changed", () => {
          const place = ac.getPlace();
          if (!place) return;
          const regionName = extractRegionFromPlace(place);
          const lat = place.geometry?.location?.lat();
          const lng = place.geometry?.location?.lng();
          setFormData((prev) => ({
            ...prev,
            region:
              regionName ||
              place.formatted_address ||
              place.name ||
              prev.region,
          }));
          if (lat && lng) setCoords({ lat, lng });
        });
      })
      .catch((e) => console.warn("Google Maps load failed", e));

    return () => {
      if (listener && listener.remove) listener.remove();
    };
  }, []);

  const extractRegionFromPlace = (place) => {
    const comps = place.address_components || [];
    const findType = (type) =>
      comps.find((c) => (c.types || []).includes(type))?.long_name;
    return (
      findType("administrative_area_level_2") ||
      findType("administrative_area_level_1") ||
      findType("locality") ||
      findType("sublocality") ||
      place.name ||
      place.formatted_address ||
      ""
    );
  };

  const fetchReports = async () => {
    setLoadingReports(true);
    try {
      if (!isSupabaseConfigured()) {
        console.info("Supabase not configured, using sample data");
        // Use sample data when Supabase is not configured
        setReports([
          {
            id: 1,
            region: "Kitui County",
            title: "Increased soil erosion after recent rains",
            description:
              "The eastern hills are experiencing significant soil loss. Need to implement terracing.",
            reportedAt: "2025-10-08",
            reporterName: "Community Member",
          },
          {
            id: 2,
            region: "Machakos County",
            title: "Water table dropping in southern wells",
            description:
              "Community wells are 2 meters lower than last year at this time.",
            reportedAt: "2025-10-07",
            reporterName: "Community Member",
          },
        ]);
        return;
      }

      const { data, error } = await supabase
        .from("community_reports")
        .select("*")
        .order("created_at", { ascending: false })
        .limit(20);

      if (error) {
        console.error("Supabase error details:", error);
        throw error;
      }

      console.log("Successfully fetched reports:", data);

      // Transform data to match our UI format
      const transformedReports = data.map((report) => {
        const [derivedTitle, derivedBody] = splitDescription(
          report.description || ""
        );
        return {
          id: report.id,
          region: report.region,
          title: derivedTitle,
          description: derivedBody,
          reportedAt: (report.created_at || new Date().toISOString()).split(
            "T"
          )[0],
          reporterName: "Community Member", // For privacy, we'll use generic name
        };
      });

      setReports(transformedReports);
    } catch (error) {
      console.error("Error fetching reports:", error);

      // Show specific error message based on error type
      if (error.code === "PGRST116" || error.message?.includes("401")) {
        console.warn("Database authentication error - using sample data");
        setError("Database connection issue. Using sample data for now.");
      } else if (
        error.message?.includes("relation") ||
        error.message?.includes("does not exist")
      ) {
        console.warn("Database schema not set up - using sample data");
        setError("Database not set up yet. Using sample data for now.");
      } else {
        setError("Unable to load reports. Using sample data for now.");
      }

      // Fallback to sample data if Supabase fails
      setReports([
        {
          id: 1,
          region: "Kitui County",
          title: "Increased soil erosion after recent rains",
          description:
            "The eastern hills are experiencing significant soil loss. Need to implement terracing.",
          reportedAt: "2025-10-08",
          reporterName: "Community Member",
        },
        {
          id: 2,
          region: "Machakos County",
          title: "Water table dropping in southern wells",
          description:
            "Community wells are 2 meters lower than last year at this time.",
          reportedAt: "2025-10-07",
          reporterName: "Community Member",
        },
      ]);
    } finally {
      setLoadingReports(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const titleTrim = formData.title.trim();
      let bodyTrim = formData.description.trim();
      if (bodyTrim.toLowerCase() === titleTrim.toLowerCase()) {
        bodyTrim = "";
      } else if (bodyTrim.toLowerCase().startsWith(titleTrim.toLowerCase())) {
        bodyTrim = bodyTrim.slice(titleTrim.length).trimStart();
      }

      let attachmentUrl = null;

      if (!isSupabaseConfigured()) {
        console.info("Supabase not configured, simulating report submission");
        setSubmitted(true);

        setTimeout(() => {
          setSubmitted(false);
          setFormData({
            region: "",
            title: "",
            description: "",
            isAnonymous: false,
            name: "",
          });
          setSelectedFile(null);
          if (fileInputRef.current) fileInputRef.current.value = "";
        }, 3000);
        return;
      }

      // Upload file if selected
      if (selectedFile) {
        attachmentUrl = await uploadFile(selectedFile);
      }

      const reportData = {
        region: formData.region,
        report_type: "community_observation",
        description: `${titleTrim}\n\n${bodyTrim}`,
        status: "pending",
        verified: false,
        latitude: coords?.lat ?? null,
        longitude: coords?.lng ?? null,
        attachment_url: attachmentUrl,
      };

      console.log("Attempting to submit report to Supabase...");
      const { data, error } = await supabase
        .from("community_reports")
        .insert([reportData])
        .select();

      if (error) {
        console.error("Supabase submission error:", error);
        throw error;
      }

      console.log("Successfully submitted report:", data);

      const newReport = {
        id: data[0].id,
        region: formData.region,
        title: titleTrim,
        description: bodyTrim,
        reportedAt: new Date().toISOString().split("T")[0],
        reporterName: formData.isAnonymous
          ? "Anonymous"
          : formData.name || "Anonymous",
        attachmentUrl: attachmentUrl,
      };

      setReports((prev) => [newReport, ...prev]);
      setSubmitted(true);

      setTimeout(() => {
        setSubmitted(false);
        setFormData({
          region: "",
          title: "",
          description: "",
          isAnonymous: false,
          name: "",
        });
        setCoords(null);
        setSelectedFile(null);
        if (fileInputRef.current) fileInputRef.current.value = "";
      }, 3000);
    } catch (error) {
      console.error("Error submitting report:", error);

      if (error.code === "PGRST116" || error.message?.includes("401")) {
        setError(
          "Database authentication error. Please check your Supabase configuration."
        );
      } else if (
        error.message?.includes("relation") ||
        error.message?.includes("does not exist")
      ) {
        setError(
          "Database not set up properly. Please run the database schema setup."
        );
      } else if (error.message?.includes("permission")) {
        setError(
          "Permission denied. Database policies may need to be configured."
        );
      } else {
        setError(
          error.message || "Failed to submit report. Please try again or contact support."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    setFileError("");
    
    if (!file) {
      setSelectedFile(null);
      return;
    }

    // Validate file type (PDF only)
    if (file.type !== "application/pdf") {
      setFileError("Only PDF files are allowed");
      setSelectedFile(null);
      e.target.value = "";
      return;
    }

    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      setFileError("File size must be less than 10MB");
      setSelectedFile(null);
      e.target.value = "";
      return;
    }

    setSelectedFile(file);
  };

  const uploadFile = async (file) => {
    if (!file || !isSupabaseConfigured()) return null;

    const fileExt = file.name.split('.').pop();
    const fileName = `${Date.now()}-${Math.random().toString(36).substring(7)}.${fileExt}`;
    const filePath = `reports/${fileName}`;

    const { data, error } = await supabase.storage
      .from("report-attachments")
      .upload(filePath, file, {
        cacheControl: "3600",
        upsert: false,
      });

    if (error) {
      console.error("File upload error:", error);
      throw new Error("Failed to upload file. Please try again.");
    }

    // Get public URL
    const { data: urlData } = supabase.storage
      .from("report-attachments")
      .getPublicUrl(filePath);

    return urlData?.publicUrl || null;
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  return (
    <div className="min-h-screen font-sans">
      {/* Header - White to Green radial */}
      <section className="relative py-16 px-4 overflow-hidden">
        <div 
          className="absolute inset-0" 
          style={{
            background: "radial-gradient(ellipse 120% 80% at 0% 0%, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0.95) 20%, rgba(255, 255, 255, 0.7) 40%, rgba(34, 197, 94, 0.75) 55%, rgba(5, 150, 105, 0.9) 70%, rgb(4, 120, 87) 100%)"
          }}
        ></div>
        <div className="relative max-w-7xl mx-auto text-center z-10">
          <h1 className="text-5xl font-bold mb-4 text-white drop-shadow-lg" style={{ color: 'black' }}>Community Reports</h1>
          <p className="text-xl text-green-100 drop-shadow">
            Share observations and learn from fellow farmers
          </p>
        </div>
      </section>

      {/* Main Content - Flowing green */}
      <section className="relative py-12 px-4 overflow-hidden">
        <div 
          className="absolute inset-0" 
          style={{
            background: "linear-gradient(180deg, rgb(4, 120, 87) 0%, rgb(3, 105, 78) 30%, rgb(2, 90, 68) 50%, rgb(2, 80, 60) 70%, rgb(4, 120, 87) 100%)"
          }}
        ></div>
        <div className="relative max-w-7xl mx-auto z-10">
          {/* Development Notice */}
          {!isSupabaseConfigured() && (
            <div className="mb-8 bg-yellow-50 border-2 border-yellow-200 rounded-xl p-6">
              <div className="flex items-center gap-3">
                <div className="text-yellow-600 text-2xl">⚙️</div>
                <div>
                  <h3 className="text-lg font-bold text-yellow-800">
                    Development Mode
                  </h3>
                  <p className="text-yellow-700">
                    Reports are currently using sample data. Connect Supabase
                    database for persistent storage. See .env.local.example for
                    configuration details.
                  </p>
                </div>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Submit Report Form */}
            <div>
              <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-lg p-8 hover:bg-white transition">
                <h2 className="text-3xl font-bold text-gray-800 mb-6">
                  Submit a Report
                </h2>
                <p className="text-gray-600 mb-6">
                  Help your community by sharing local climate and farming
                  observations.
                </p>

                {submitted && (
                  <div className="mb-6 p-4 bg-green-100 text-green-800 rounded-lg">
                    {isSupabaseConfigured()
                      ? "Thank you! Your report has been submitted and will appear here once reviewed by our team."
                      : "Thank you! Your report has been submitted successfully. (Demo mode - connect Supabase for persistent storage)."
                    }
                  </div>
                )}

                {error && (
                  <div className="mb-6 p-4 bg-red-100 text-red-800 rounded-lg">
                    {error}
                  </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-gray-700 font-semibold mb-2">
                      Location (search and select) *
                    </label>
                    <input
                      ref={inputRef}
                      type="text"
                      name="region"
                      value={formData.region}
                      onChange={handleChange}
                      placeholder="Search county, town, or village"
                      className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-green-600"
                      required
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Start typing and choose a location; coordinates will be
                      captured.
                    </p>
                  </div>

                  <div>
                    <label className="block text-gray-700 font-semibold mb-2">
                      Title *
                    </label>
                    <input
                      type="text"
                      name="title"
                      value={formData.title}
                      onChange={handleChange}
                      placeholder="Brief description of what you observed"
                      className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-green-600"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-gray-700 font-semibold mb-2">
                      Detailed Description *
                    </label>
                    <div className="relative">
                      <textarea
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        placeholder="Provide more details about what you observed..."
                        rows="5"
                        className="w-full px-4 py-3 pr-12 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-green-600"
                        required
                      ></textarea>
                      
                      {/* PDF Upload Button */}
                      <button
                        type="button"
                        onClick={() => fileInputRef.current?.click()}
                        className="absolute right-3 bottom-3 p-2 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-lg transition"
                        title="Attach PDF document"
                      >
                        <svg 
                          xmlns="http://www.w3.org/2000/svg" 
                          className="h-6 w-6" 
                          fill="none" 
                          viewBox="0 0 24 24" 
                          stroke="currentColor"
                        >
                          <path 
                            strokeLinecap="round" 
                            strokeLinejoin="round" 
                            strokeWidth={2} 
                            d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" 
                          />
                          <path 
                            strokeLinecap="round" 
                            strokeLinejoin="round" 
                            strokeWidth={2} 
                            d="M9 9h1m4 0h1m-6 4h6m-6 4h4" 
                          />
                        </svg>
                      </button>
                    </div>
                    
                    {/* Hidden file input */}
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept=".pdf,application/pdf"
                      onChange={handleFileSelect}
                      className="hidden"
                    />
                    
                    {/* File selection feedback */}
                    {selectedFile && (
                      <div className="mt-2 flex items-center gap-2 p-2 bg-green-50 border border-green-200 rounded-lg">
                        <svg 
                          xmlns="http://www.w3.org/2000/svg" 
                          className="h-5 w-5 text-green-600" 
                          fill="none" 
                          viewBox="0 0 24 24" 
                          stroke="currentColor"
                        >
                          <path 
                            strokeLinecap="round" 
                            strokeLinejoin="round" 
                            strokeWidth={2} 
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
                          />
                        </svg>
                        <span className="text-sm text-green-700 flex-1 truncate">
                          {selectedFile.name}
                        </span>
                        <span className="text-xs text-green-600">
                          ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                        </span>
                        <button
                          type="button"
                          onClick={() => {
                            setSelectedFile(null);
                            if (fileInputRef.current) fileInputRef.current.value = "";
                          }}
                          className="text-red-500 hover:text-red-700 p-1"
                          title="Remove file"
                        >
                          <svg 
                            xmlns="http://www.w3.org/2000/svg" 
                            className="h-4 w-4" 
                            fill="none" 
                            viewBox="0 0 24 24" 
                            stroke="currentColor"
                          >
                            <path 
                              strokeLinecap="round" 
                              strokeLinejoin="round" 
                              strokeWidth={2} 
                              d="M6 18L18 6M6 6l12 12" 
                            />
                          </svg>
                        </button>
                      </div>
                    )}
                    
                    {/* File error message */}
                    {fileError && (
                      <p className="mt-1 text-sm text-red-600">{fileError}</p>
                    )}
                    
                    <p className="text-xs text-gray-500 mt-1">
                      You can attach a PDF document (max 10MB) by clicking the file icon
                    </p>
                  </div>

                  <div className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      name="isAnonymous"
                      checked={formData.isAnonymous}
                      onChange={handleChange}
                      className="w-5 h-5"
                    />
                    <label className="text-gray-700">Submit anonymously</label>
                  </div>

                  {!formData.isAnonymous && (
                    <div>
                      <label className="block text-gray-700 font-semibold mb-2">
                        Your Name (Optional)
                      </label>
                      <input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="Your name"
                        className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-green-600"
                      />
                    </div>
                  )}

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-green-700 text-white py-4 rounded-lg font-semibold text-lg hover:bg-green-800 transition disabled:opacity-50"
                  >
                    {loading ? "Submitting..." : "Submit Report"}
                  </button>
                </form>
              </div>
            </div>

            {/* Community Reports List */}
            <div>
              <h2 className="text-3xl font-bold text-white mb-6">
                Recent Community Reports
              </h2>

              {loadingReports ? (
                <div className="text-center py-8">
                  <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
                  <p className="mt-4 text-green-100">
                    Loading community reports...
                  </p>
                </div>
              ) : (
                <div className="space-y-6">
                  {reports.length === 0 ? (
                    <div className="bg-white/95 backdrop-blur-sm rounded-xl p-8 text-center">
                      <p className="text-gray-600 text-lg">
                        No community reports available yet.
                      </p>
                      <p className="text-gray-500 mt-2">
                        Be the first to share an observation!
                      </p>
                    </div>
                  ) : (
                    reports.map((report) => (
                      <div
                        key={report.id}
                        className="bg-white/95 backdrop-blur-sm rounded-xl shadow-md p-6 hover:shadow-lg hover:bg-white transition"
                      >
                        <div className="flex items-start justify-between mb-3">
                          <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold">
                            {report.region}
                          </span>
                          <span className="text-sm text-gray-500">
                            {new Date(report.reportedAt).toLocaleDateString(
                              "en-US",
                              {
                                month: "short",
                                day: "numeric",
                              }
                            )}
                          </span>
                        </div>
                        <h3 className="text-2xl font-extrabold tracking-tight text-gray-900 mb-1">
                          {report.title}
                        </h3>
                        {report.description &&
                          report.description.trim() !== report.title.trim() && (
                            <p className="text-gray-700 leading-relaxed mb-4 whitespace-pre-line font-normal">
                              {report.description}
                            </p>
                          )}
                        <p className="text-sm text-gray-500">
                          Reported by: <strong>{report.reporterName}</strong>
                        </p>
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Info Section - Green to Dark */}
      <section className="relative py-16 px-4 overflow-hidden">
        <div 
          className="absolute inset-0" 
          style={{
            background: "linear-gradient(135deg, rgb(4, 120, 87) 0%, rgb(2, 80, 60) 25%, rgb(1, 50, 40) 50%, rgb(10, 30, 25) 75%, rgb(5, 15, 12) 100%)"
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto z-10">
          <h2 className="text-3xl font-bold text-center mb-8 text-white">
            Why Community Reports Matter
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-md p-6 text-center hover:bg-white transition">
              <h3 className="font-bold text-gray-800 mb-2">Early Detection</h3>
              <p className="text-gray-600 text-sm">
                Local observations often spot issues before satellites
              </p>
            </div>
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-md p-6 text-center hover:bg-white transition">
              <h3 className="font-bold text-gray-800 mb-2">
                Community Support
              </h3>
              <p className="text-gray-600 text-sm">
                Learn from others' experiences in your region
              </p>
            </div>
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-md p-6 text-center hover:bg-white transition">
              <h3 className="font-bold text-gray-800 mb-2">Better Data</h3>
              <p className="text-gray-600 text-sm">
                Your reports help improve our AI predictions
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA - Green to White radial */}
      <section className="relative py-16 px-4 overflow-hidden">
        <div 
          className="absolute inset-0" 
          style={{
            background: "radial-gradient(ellipse 120% 120% at 100% 100%, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0.9) 15%, rgba(255, 255, 255, 0.6) 30%, rgba(34, 197, 94, 0.7) 45%, rgba(5, 150, 105, 0.85) 60%, rgb(4, 120, 87) 80%, rgb(2, 80, 60) 100%)"
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto text-center z-10">
          <h2 className="text-3xl font-bold mb-4 text-white drop-shadow-lg">Stay Connected</h2>
          <p className="text-xl mb-8 text-green-100 drop-shadow">
            Get instant alerts and share observations via messaging
          </p>
          <div className="flex justify-center">
            <a
              href="https://t.me/TerraGuard_Bot"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white text-green-700 px-8 py-3 rounded-lg font-bold hover:bg-green-50 transition shadow-lg"
            >
              Telegram Bot
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Reports;
