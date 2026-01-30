import { Link } from "react-router-dom";
import { useEffect } from "react";

function About() {
  useEffect(() => {
    // Scroll to top when component mounts
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="min-h-screen font-sans">
      {/* Hero Section - White to Green radial */}
      <section className="relative py-20 px-4 overflow-hidden">
        <div 
          className="absolute inset-0" 
          style={{
            background: "radial-gradient(ellipse 120% 80% at 0% 0%, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0.95) 20%, rgba(255, 255, 255, 0.7) 40%, rgba(34, 197, 94, 0.75) 55%, rgba(5, 150, 105, 0.9) 70%, rgb(4, 120, 87) 100%)"
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto text-center z-10">
          <h1 className="text-5xl font-bold mb-6 text-blac drop-shadow-lg">About GreenPulse</h1>
          <p className="text-2xl text-green-100 drop-shadow">
            GreenPulse is a B2B climate intelligence platform that helps companies analyze emissions, 
            understand how their activities affect different regions, and use AI-driven insights to 
            manage climate risk, compliance, and environmental impact.
          </p>
        </div>
      </section>

      {/* Mission Section - Flowing green */}
      <section className="relative py-16 px-4 overflow-hidden">
        <div 
          className="absolute inset-0" 
          style={{
            background: "linear-gradient(180deg, rgb(4, 120, 87) 0%, rgb(3, 105, 78) 30%, rgb(2, 90, 68) 50%, rgb(2, 80, 60) 70%, rgb(4, 120, 87) 100%)"
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto z-10">
          <h2 className="text-4xl font-bold text-center mb-8 text-white">
            Our Mission
          </h2>
          <p className="text-xl text-green-100 leading-relaxed text-center mb-8">
            GreenPulse exists to provide businesses, communities, and decision-makers 
            with climate data and AI-driven intelligence to understand, manage, and 
            reduce environmental and climate impact across Kenya.
          </p>
          <div className="bg-white/95 backdrop-blur-sm border-l-4 border-green-600 p-6 rounded-r-lg">
            <p className="text-lg text-gray-800 italic">
              "When climate data meets intelligence, action becomes possible. GreenPulse 
              combines climate datasets, AI reasoning, and human insight to help businesses 
              reduce environmental risk and help communities adapt to climate change."
            </p>
          </div>
        </div>
      </section>

      {/* The Problem - Green to Dark */}
      <section className="relative py-16 px-4 overflow-hidden">
        <div 
          className="absolute inset-0" 
          style={{
            background: "linear-gradient(135deg, rgb(4, 120, 87) 0%, rgb(2, 80, 60) 25%, rgb(1, 50, 40) 50%, rgb(10, 30, 25) 75%, rgb(5, 15, 12) 100%)"
          }}
        ></div>
        <div className="relative max-w-6xl mx-auto z-10">
          <h2 className="text-4xl font-bold text-center mb-12 text-white">
            The Problem We're Solving
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-md p-6 hover:bg-white transition">
              <h3 className="text-xl font-bold mb-3 text-gray-800">
                Climate Uncertainty
              </h3>
              <p className="text-gray-600">
                Unpredictable weather patterns are becoming the norm. Farmers
                need advance warning to prepare and adapt.
              </p>
            </div>
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-md p-6 hover:bg-white transition">
              <h3 className="text-xl font-bold mb-3 text-gray-800">
                Information Gap
              </h3>
              <p className="text-gray-600">
                Most climate data services require internet and smartphones. 80%
                of rural farmers only have basic phones.
              </p>
            </div>
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-md p-6 hover:bg-white transition">
              <h3 className="text-xl font-bold mb-3 text-gray-800">
                Economic Losses
              </h3>
              <p className="text-gray-600">
                Climate events destroy billions in crops annually. Early
                warnings can prevent 60-80% of these losses.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works - Dark/Black */}
      <section className="relative py-16 px-4 overflow-hidden">
        <div 
          className="absolute inset-0" 
          style={{
            background: "linear-gradient(135deg, rgb(5, 15, 12) 0%, rgb(10, 25, 20) 20%, rgb(5, 40, 30) 40%, rgb(2, 50, 40) 60%, rgb(0, 0, 0) 100%)"
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto z-10">
          <h2 className="text-4xl font-bold text-center mb-12 text-white">
            How GreenPulse Works
          </h2>
          <div className="space-y-8">
            <div className="flex gap-6 items-start">
              <div className="flex-shrink-0 w-12 h-12 bg-green-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                1
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2 text-white">
                  Data Collection
                </h3>
                <p className="text-gray-300">
                  We pull real-time climate data from NASA POWER satellites,
                  which monitor rainfall, temperature, soil moisture, and other
                  critical factors across Africa daily.
                </p>
              </div>
            </div>

            <div className="flex gap-6 items-start">
              <div className="flex-shrink-0 w-12 h-12 bg-green-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                2
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2 text-white">
                  AI Analysis
                </h3>
                <p className="text-gray-300">
                  Our AI algorithms (powered by DeepSeek) analyze the data to
                  detect drought conditions, flood risks, and temperature
                  extremes before they become critical.
                </p>
              </div>
            </div>

            <div className="flex gap-6 items-start">
              <div className="flex-shrink-0 w-12 h-12 bg-green-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                3
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2 text-white">
                  Alert Generation
                </h3>
                <p className="text-gray-300">
                  When risks are detected, our AI generates clear, actionable
                  alerts in plain language, with specific recommendations for
                  your region and crop type.
                </p>
              </div>
            </div>

            <div className="flex gap-6 items-start">
              <div className="flex-shrink-0 w-12 h-12 bg-green-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                4
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2 text-white">
                  Multi-Channel Delivery
                </h3>
                <p className="text-gray-300">
                  Alerts are delivered via Telegram, WhatsApp, and displayed on
                  our web platform. You choose how you want to receive
                  information.
                </p>
              </div>
            </div>

            <div className="flex gap-6 items-start">
              <div className="flex-shrink-0 w-12 h-12 bg-green-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                5
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2 text-white">
                  Interactive Support
                </h3>
                <p className="text-gray-300">
                  You can ask follow-up questions via chat. Our AI provides
                  personalized advice based on your location, crops, and current
                  conditions.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Stack - Dark to Green radial */}
      <section className="relative py-16 px-4 overflow-hidden">
        <div 
          className="absolute inset-0" 
          style={{
            background: "radial-gradient(ellipse 120% 120% at 100% 100%, rgb(4, 120, 87) 0%, rgba(5, 150, 105, 0.9) 20%, rgba(22, 163, 74, 0.8) 35%, rgb(10, 30, 25) 55%, rgb(5, 15, 12) 70%, rgb(0, 0, 0) 100%)"
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto z-10">
          <h2 className="text-4xl font-bold text-center mb-12 text-white">
            Technology Powering GreenPulse
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="bg-white/95 backdrop-blur-sm rounded-lg shadow p-6 text-center hover:bg-white transition">
              <p className="font-semibold text-gray-800">NASA POWER</p>
              <p className="text-sm text-gray-600">Satellite Data</p>
            </div>
            <div className="bg-white/95 backdrop-blur-sm rounded-lg shadow p-6 text-center hover:bg-white transition">
              <p className="font-semibold text-gray-800">DeepSeek AI</p>
              <p className="text-sm text-gray-600">Intelligence</p>
            </div>
            <div className="bg-white/95 backdrop-blur-sm rounded-lg shadow p-6 text-center hover:bg-white transition">
              <p className="font-semibold text-gray-800">FastAPI</p>
              <p className="text-sm text-gray-600">Backend</p>
            </div>
            <div className="bg-white/95 backdrop-blur-sm rounded-lg shadow p-6 text-center hover:bg-white transition">
              <p className="font-semibold text-gray-800">React</p>
              <p className="text-sm text-gray-600">Web Platform</p>
            </div>
            <div className="bg-white/95 backdrop-blur-sm rounded-lg shadow p-6 text-center hover:bg-white transition">
              <p className="font-semibold text-gray-800">Telegram</p>
              <p className="text-sm text-gray-600">Bot API</p>
            </div>
            <div className="bg-white/95 backdrop-blur-sm rounded-lg shadow p-6 text-center hover:bg-white transition">
              <p className="font-semibold text-gray-800">WhatsApp</p>
              <p className="text-sm text-gray-600">Business API</p>
            </div>
            <div className="bg-white/95 backdrop-blur-sm rounded-lg shadow p-6 text-center hover:bg-white transition">
              <p className="font-semibold text-gray-800">Google Maps</p>
              <p className="text-sm text-gray-600">Geocoding</p>
            </div>
          </div>
        </div>
      </section>

      {/* Connect Section - Green flowing */}
      <section className="relative py-16 px-4 overflow-hidden">
        <div 
          className="absolute inset-0" 
          style={{
            background: "linear-gradient(180deg, rgb(4, 120, 87) 0%, rgb(3, 105, 78) 30%, rgb(2, 90, 68) 50%, rgb(2, 80, 60) 70%, rgb(4, 120, 87) 100%)"
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto z-10">
          <h2 className="text-4xl font-bold text-center mb-8 text-white">
            Connect With GreenPulse
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <a
              href="https://t.me/TerraGuard_Bot"
              target="_blank"
              rel="noopener norefGreenPulse_AI_bot"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-blue-500 text-white p-8 rounded-xl shadow-lg hover:bg-blue-600 transition text-center"
            >
              <h3 className="text-xl font-bold mb-2">Telegram Bot</h3>
              <p className="text-blue-100">@GreenPulse_AI_bot</p>
            </a>
            <Link
              to="/ai"
              className="inline-block bg-white text-green-700 px-10 py-4 rounded-lg font-bold text-lg hover:bg-green-50 transition shadow-lg text-center"
            >
              Try GreenPulse AI
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
          <h2 className="text-4xl font-bold mb-4 text-white drop-shadow-lg">Join the Movement</h2>
          <p className="text-xl mb-8 text-green-100 drop-shadow">
            Be part of the climate-smart farming revolution in Africa
          </p>
          <Link
            to="/#subscribe"
            className="inline-block bg-white text-green-700 px-10 py-4 rounded-lg font-bold text-lg hover:bg-green-50 transition shadow-lg"
          >
            Get Started Free
          </Link>Ready for Climate Intelligence?</h2>
          <p className="text-xl mb-8 text-green-100 drop-shadow">
            When climate data meets intelligence, action becomes possible
          </p>
          <Link
            to="/ai"
            className="inline-block bg-white text-green-700 px-10 py-4 rounded-lg font-bold text-lg hover:bg-green-50 transition shadow-lg"
          >
            Try GreenPulse AI