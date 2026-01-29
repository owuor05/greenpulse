import { Link } from "react-router-dom";
import { useEffect } from "react";

function About() {
  useEffect(() => {
    // Scroll to top when component mounts
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-green-600 to-emerald-700 text-white py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-6">About GreenPulse</h1>
          <p className="text-2xl text-green-100">
            Empowering African farmers with AI-powered climate intelligence
          </p>
        </div>
      </div>

      {/* Mission Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-8 text-gray-800">
            Our Mission
          </h2>
          <p className="text-xl text-gray-700 leading-relaxed text-center mb-8">
            GreenPulse exists to protect African farmers from climate-related
            losses by providing early warnings, actionable insights, and expert
            guidance powered by artificial intelligence and real-time satellite
            data.
          </p>
          <div className="bg-green-50 border-l-4 border-green-600 p-6 rounded-r-lg">
            <p className="text-lg text-gray-800 italic">
              "We believe every farmer deserves access to the same climate
              intelligence that large agricultural corporations use. GreenPulse
              democratizes this technology, making it free and accessible via
              simple chat tools many farmers already use."
            </p>
          </div>
        </div>
      </section>

      {/* The Problem */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12 text-gray-800">
            The Problem We're Solving
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-xl font-bold mb-3 text-gray-800">
                Climate Uncertainty
              </h3>
              <p className="text-gray-600">
                Unpredictable weather patterns are becoming the norm. Farmers
                need advance warning to prepare and adapt.
              </p>
            </div>
            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-xl font-bold mb-3 text-gray-800">
                Information Gap
              </h3>
              <p className="text-gray-600">
                Most climate data services require internet and smartphones. 80%
                of rural farmers only have basic phones.
              </p>
            </div>
            <div className="bg-white rounded-xl shadow-md p-6">
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

      {/* How It Works */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12 text-gray-800">
            How GreenPulse Works
          </h2>
          <div className="space-y-8">
            <div className="flex gap-6 items-start">
              <div className="flex-shrink-0 w-12 h-12 bg-green-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                1
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2 text-gray-800">
                  Data Collection
                </h3>
                <p className="text-gray-600">
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
                <h3 className="text-xl font-bold mb-2 text-gray-800">
                  AI Analysis
                </h3>
                <p className="text-gray-600">
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
                <h3 className="text-xl font-bold mb-2 text-gray-800">
                  Alert Generation
                </h3>
                <p className="text-gray-600">
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
                <h3 className="text-xl font-bold mb-2 text-gray-800">
                  Multi-Channel Delivery
                </h3>
                <p className="text-gray-600">
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
                <h3 className="text-xl font-bold mb-2 text-gray-800">
                  Interactive Support
                </h3>
                <p className="text-gray-600">
                  You can ask follow-up questions via chat. Our AI provides
                  personalized advice based on your location, crops, and current
                  conditions.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12 text-gray-800">
            Technology Powering GreenPulse
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="bg-white rounded-lg shadow p-6 text-center">
              <p className="font-semibold text-gray-800">NASA POWER</p>
              <p className="text-sm text-gray-600">Satellite Data</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6 text-center">
              <p className="font-semibold text-gray-800">DeepSeek AI</p>
              <p className="text-sm text-gray-600">Intelligence</p>
            </div>

            <div className="bg-white rounded-lg shadow p-6 text-center">
              <p className="font-semibold text-gray-800">FastAPI</p>
              <p className="text-sm text-gray-600">Backend</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6 text-center">
              <p className="font-semibold text-gray-800">React</p>
              <p className="text-sm text-gray-600">Web Platform</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6 text-center">
              <p className="font-semibold text-gray-800">Telegram</p>
              <p className="text-sm text-gray-600">Bot API</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6 text-center">
              <p className="font-semibold text-gray-800">WhatsApp</p>
              <p className="text-sm text-gray-600">Business API</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6 text-center">
              <p className="font-semibold text-gray-800">Google Maps</p>
              <p className="text-sm text-gray-600">Geocoding</p>
            </div>
          </div>
        </div>
      </section>

      {/* Connect Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-8 text-gray-800">
            Connect With GreenPulse
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <a
              href="https://t.me/TerraGuard_Bot"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-blue-500 text-white p-8 rounded-xl shadow-lg hover:bg-blue-600 transition text-center"
            >
              <h3 className="text-xl font-bold mb-2">Telegram Bot</h3>
              <p className="text-blue-100">@GreenPulse_Bot</p>
            </a>
            <a
              href="https://wa.me/14155238886?text=join%20actual-mother"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-green-500 text-white p-8 rounded-xl shadow-lg hover:bg-green-600 transition text-center"
            >
              <h3 className="text-xl font-bold mb-2">WhatsApp</h3>
              <p className="text-green-100">+1 415 523 8886</p>
            </a>
            <Link
              to="/#subscribe"
              className="md:col-span-2 inline-block bg-white text-green-700 px-10 py-4 rounded-lg font-bold text-lg hover:bg-green-50 transition shadow-lg text-center"
            >
              Get Started Free
            </Link>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 px-4 bg-gradient-to-r from-green-600 to-emerald-700 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-4">Join the Movement</h2>
          <p className="text-xl mb-8 text-green-100">
            Be part of the climate-smart farming revolution in Africa
          </p>
          <Link
            to="/#subscribe"
            className="inline-block bg-white text-green-700 px-10 py-4 rounded-lg font-bold text-lg hover:bg-green-50 transition shadow-lg"
          >
            Get Started Free
          </Link>
        </div>
      </section>
    </div>
  );
}

export default About;
