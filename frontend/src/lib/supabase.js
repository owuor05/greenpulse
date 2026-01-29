import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

// Create Supabase client only if credentials are provided
let supabase = null;

// Debug logging
console.log("Supabase Configuration Check:");
console.log("URL provided:", !!supabaseUrl);
console.log("Key provided:", !!supabaseAnonKey);
console.log(
  "URL value:",
  supabaseUrl ? `${supabaseUrl.substring(0, 20)}...` : "undefined"
);

if (
  supabaseUrl &&
  supabaseAnonKey &&
  supabaseUrl !== "your_supabase_project_url_here" &&
  supabaseAnonKey !== "your_supabase_anon_key_here"
) {
  try {
    supabase = createClient(supabaseUrl, supabaseAnonKey);
    console.log("✅ Supabase client created successfully");
  } catch (error) {
    console.warn("❌ Failed to create Supabase client:", error);
    supabase = null;
  }
} else {
  console.log("⚠️ Supabase not configured - using sample data mode");
}

export { supabase };

// Helper function to check if Supabase is configured
export const isSupabaseConfigured = () => {
  return supabase !== null;
};

// Helper to get configuration status
export const getSupabaseStatus = () => {
  return {
    configured: supabase !== null,
    url: supabaseUrl ? `${supabaseUrl.substring(0, 20)}...` : "Not set",
    keyProvided: !!supabaseAnonKey,
  };
};
