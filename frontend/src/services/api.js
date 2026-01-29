import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "https://terraguard-api.onrender.com";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
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
  getAlerts: async (region = null) => {
    const params = region ? { region } : {};
    const response = await api.get("/api/alerts", { params });
    return response.data;
  },

  getAlertById: async (alertId) => {
    const response = await api.get(`/api/alerts/${alertId}`);
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
  askQuestion: async (question) => {
    const response = await api.post("/api/ai/answer", { question });
    return response.data;
  },

  getStatus: async () => {
    const response = await api.get("/api/ai/status");
    return response.data;
  },
};

export default api;
