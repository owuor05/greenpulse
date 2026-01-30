import axios from "axios";

// Get the API base URL from environment variables
const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  import.meta.env.VITE_API_BASE_URL ||
  "https://greenpulse-production-370c.up.railway.app";

console.log("API Base URL:", API_BASE_URL);

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 120000, // 2 minutes timeout for AI responses
});

// Climate Risk Services
export const riskService = {
  detectRisks: async (region) => {
    const response = await api.post("/api/risk/detect", { region });
    return response.data;
  },

  getRiskForecast: async (region) => {
    const response = await api.post("/api/risk/forecast", { region });
    return response.data;
  },

  analyzeCoordinates: async (latitude, longitude) => {
    const response = await api.post("/api/risk/analyze-coordinates", {
      latitude,
      longitude,
    });
    return response.data;
  },
};

// Alerts Services
export const alertsService = {
  getAll: async () => {
    const response = await api.get("/api/alerts");
    return response.data;
  },

  getByRegion: async (region) => {
    const response = await api.get(`/api/alerts/region/${region}`);
    return response.data;
  },
};

// Subscription Services
export const subscriptionService = {
  subscribe: async (data) => {
    const response = await api.post("/api/subscribe", data);
    return response.data;
  },
};

// Regions Service
export const regionsService = {
  getRegions: async () => {
    const response = await api.get("/api/regions");
    return response.data;
  },
};

// Geocoding Service
export const geocodeService = {
  geocodeLocation: async (region) => {
    const response = await api.post("/api/geocode", { region });
    return response.data;
  },
};

// Reports Service
export const reportsService = {
  getAllReports: async () => {
    // This will be implemented in the Reports component using Supabase directly
    // to avoid CORS issues with the backend
    throw new Error("Use Supabase client directly in component");
  },

  submitReport: async (reportData) => {
    // This will be implemented in the Reports component using Supabase directly
    // to avoid CORS issues with the backend
    throw new Error("Use Supabase client directly in component");
  },
};

// AI Service
export const aiService = {
  // Ask a question to the AI assistant (with optional file attachment)
  askQuestion: async (question, file = null) => {
    console.log(
      "🔵 Sending to AI:",
      question,
      file ? `with file: ${file.name}` : "text only",
    );

    try {
      // ALWAYS use FormData for /api/ai/ask endpoint (backend expects multipart/form-data)
      const formData = new FormData();
      formData.append("question", question);

      if (file) {
        formData.append("file", file);
        console.log(
          "📎 File attached:",
          file.name,
          "(" + file.size + " bytes)",
        );
      }

      console.log("📤 Posting to /api/ai/ask...");
      const response = await api.post("/api/ai/ask", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        timeout: 180000, // 3 minutes for AI processing
      });

      console.log(
        "✅ AI Response received:",
        response.data.success ? "SUCCESS" : "FAILED",
      );
      return response.data;
    } catch (error) {
      console.error(
        "❌ AI Service Error:",
        error.response?.data || error.message || error,
      );
      throw error;
    }
  },
};

// Land Data Service
export const landDataService = {
  analyze: async (location) => {
    console.log("🌍 Analyzing land data for:", location);
    try {
      const response = await api.post("/api/land-data/analyze", { location });
      console.log(
        "✅ Land data received:",
        response.data.success ? "SUCCESS" : "FAILED",
      );
      return response.data;
    } catch (error) {
      console.error(
        "❌ Land Data Error:",
        error.response?.data || error.message,
      );
      throw error;
    }
  },
};

export default api;
