import { useEffect } from "react";
import { Link } from "react-router-dom";

function Home() {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white font-sans">
      {/* Hero Section */}
      <section className="relative py-12 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 120% 80% at 0% 0%, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0.95) 20%, rgba(255, 255, 255, 0.7) 40%, rgba(34, 197, 94, 0.75) 55%, rgba(5, 150, 105, 0.9) 70%, rgb(4, 120, 87) 100%)",
          }}
        ></div>
        {/* <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage:
              "url('https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=1200')",
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        ></div> */}

        <div className="relative max-w-7xl mx-auto text-center text-white z-10">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight font-sans">
            GreenPulse
          </h1>
          <p
            className="text-2xl md:text-3xl mb-4 font-semibold"
            style={{ color: "#064e3b" }}
          >
            When climate data meets intelligence, action becomes possible.
          </p>
          <p className="text-lg md:text-xl max-w-3xl mx-auto mb-10 leading-relaxed">
            A B2B climate intelligence platform that helps companies analyze
            emissions, understand how their activities affect different regions,
            and use AI-driven insights to manage climate risk, compliance, and
            environmental impact.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/ai"
              className="bg-white text-green-700 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-green-50 transition shadow-lg"
            >
              Try GreenPulse AI
            </Link>
            <Link
              to="/alerts"
              className="bg-green-800 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-green-900 transition shadow-lg"
            >
              Explore Climate Data
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="relative py-10 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(180deg, rgb(4, 120, 87) 0%, rgb(3, 105, 78) 30%, rgb(2, 90, 68) 50%, rgb(2, 80, 60) 70%, rgb(4, 120, 87) 100%)",
          }}
        ></div>
        <div className="relative max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 text-center z-10">
          <div className="p-6">
            <div className="text-4xl font-bold text-white mb-2">24/7</div>
            <p className="text-green-100">Climate Monitoring</p>
          </div>
          <div className="p-6">
            <div className="text-4xl font-bold text-white mb-2">47</div>
            <p className="text-green-100">Counties in Kenya</p>
          </div>
          <div className="p-6">
            <div className="text-4xl font-bold text-white mb-2">NASA</div>
            <p className="text-green-100">Powered Data</p>
          </div>
          <div className="p-6">
            <div className="text-4xl font-bold text-white mb-2">AI</div>
            <p className="text-green-100">Conservation Guidance</p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="relative py-10 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(135deg, rgb(4, 120, 87) 0%, rgb(2, 80, 60) 25%, rgb(1, 50, 40) 50%, rgb(10, 30, 25) 75%, rgb(5, 15, 12) 100%)",
          }}
        ></div>
        <div className="relative max-w-7xl mx-auto z-10">
          <h2 className="text-4xl font-bold text-center mb-4 text-white">
            Climate Intelligence for Business
          </h2>
          <p className="text-center text-green-200 mb-12 text-lg">
            Data-driven insights to manage environmental risk and drive
            sustainable operations
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-lg p-8 hover:shadow-xl hover:bg-white transition">
              <h3 className="text-2xl font-bold mb-3 text-gray-800">
                Emissions Analysis
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Analyze your company's emissions and energy use across
                operations. Understand environmental impact with data-driven
                precision.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-lg p-8 hover:shadow-xl hover:bg-white transition">
              <h3 className="text-2xl font-bold mb-3 text-gray-800">
                AI-Powered Scenario Planning
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Ask "what-if" questions and predict how operational changes
                affect climate risk, emissions, and land health over time.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-lg p-8 hover:shadow-xl hover:bg-white transition">
              <h3 className="text-2xl font-bold mb-3 text-gray-800">
                Location-Specific Insights
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Get climate data for any region in Kenya - current conditions,
                historical trends, and future projections translated into
                actionable advice.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-lg p-8 hover:shadow-xl hover:bg-white transition">
              <h3 className="text-2xl font-bold mb-3 text-gray-800">
                Climate Risk Management
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Monitor drought, flooding, temperature extremes, and
                environmental risks that could impact operations or supply
                chains.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-lg p-8 hover:shadow-xl hover:bg-white transition">
              <h3 className="text-2xl font-bold mb-3 text-gray-800">
                Compliance & Mitigation
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Identify environmental risks and get advisory support for
                regulatory compliance and mitigation measures.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-lg p-8 hover:shadow-xl hover:bg-white transition">
              <h3 className="text-2xl font-bold mb-3 text-gray-800">
                Community Intelligence
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Leverage on-the-ground observations and local environmental data
                to complement climate datasets with real human insights.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Subscription Section */}
      <section id="subscribe" className="relative py-10 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(135deg, rgb(5, 15, 12) 0%, rgb(10, 25, 20) 20%, rgb(5, 40, 30) 40%, rgb(2, 50, 40) 60%, rgb(0, 0, 0) 100%)",
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto text-center z-10">
          <h2 className="text-4xl font-bold mb-4 text-white">
            Connect with GreenPulse AI
          </h2>
          <p className="text-xl mb-8 text-green-200">
            Get instant climate intelligence and environmental insights via our
            AI assistant
          </p>

          <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-2xl p-8 md:p-12">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">
              click to connect with our AI-powered bots:
            </h3>

            <div className="grid md:grid-cols-1 gap-6 mb-8 max-w-md mx-auto">
              {/* Telegram */}
              <a
                href="https://t.me/GreenPulse_AI_bot"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-blue-500 text-white p-8 rounded-xl font-semibold hover:bg-blue-600 transition shadow-lg hover:shadow-xl transform hover:-translate-y-1 flex flex-col items-center gap-4"
              >
                <div className="text-xl font-bold">Open GreenPulse AI Bot</div>
                <p className="text-blue-100 text-sm">
                  Chat with our climate intelligence assistant on Telegram
                </p>
              </a>
            </div>

            <div className="border-t border-gray-200 pt-8">
              <h4 className="font-semibold text-gray-800 mb-4 text-lg">
                How It Works:
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
                <div className="flex gap-3">
                  <div className="flex-shrink-0 w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-bold">
                    1
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800">Open Telegram</p>
                    <p className="text-sm text-gray-600">
                      Click to start chatting
                    </p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <div className="flex-shrink-0 w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-bold">
                    2
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800">Ask Questions</p>
                    <p className="text-sm text-gray-600">
                      Query climate data for any location
                    </p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <div className="flex-shrink-0 w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-bold">
                    3
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800">
                      Get Intelligence
                    </p>
                    <p className="text-sm text-gray-600">
                      Receive AI-powered climate insights
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-8 p-6 bg-green-50 rounded-lg border-2 border-green-200">
              <p className="text-gray-700">
                <strong>GreenPulse AI can:</strong> Analyze emissions data,
                answer climate questions, provide location-specific
                environmental insights, and help assess how operations affect
                different regions - powered by real climate data and AI
                reasoning.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Impact Section */}
      <section className="relative py-10 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 120% 120% at 100% 100%, rgb(4, 120, 87) 0%, rgba(5, 150, 105, 0.9) 20%, rgba(22, 163, 74, 0.8) 35%, rgb(10, 30, 25) 55%, rgb(5, 15, 12) 70%, rgb(0, 0, 0) 100%)",
          }}
        ></div>
        <div className="relative max-w-7xl mx-auto z-10">
          <h2 className="text-4xl font-bold text-center mb-12 text-white">
            Climate Intelligence for Kenya
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <img
                src="https://cdn.pixabay.com/photo/2015/07/03/08/36/kola-nut-829934_1280.jpg"
                alt="Kenya landscape"
                className="rounded-xl shadow-lg"
              />
            </div>
            <div>
              <h3 className="text-2xl font-bold mb-4 text-white">
                Why GreenPulse Matters
              </h3>
              <ul className="space-y-4 text-gray-200 text-lg">
                <li className="flex items-start gap-3">
                  <span className="text-green-400 font-bold text-xl">✓</span>
                  <span>
                    <strong className="text-white">
                      Data-Driven Decisions:
                    </strong>{" "}
                    Real climate data from NASA POWER and weather APIs analyzed
                    by AI to provide actionable intelligence for operations and
                    planning.
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-green-400 font-bold text-xl">✓</span>
                  <span>
                    <strong className="text-white">
                      Regional Impact Analysis:
                    </strong>{" "}
                    Understand how company activities affect climate, land, and
                    water conditions in specific locations across Kenya.
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-green-400 font-bold text-xl">✓</span>
                  <span>
                    <strong className="text-white">Risk Management:</strong>{" "}
                    Monitor environmental risks including drought, flooding,
                    soil degradation, and temperature extremes that could impact
                    business continuity.
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-green-400 font-bold text-xl">✓</span>
                  <span>
                    <strong className="text-white">Compliance Support:</strong>{" "}
                    Advisory guidance on environmental regulations and
                    mitigation measures to help meet compliance requirements.
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-10 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 120% 120% at 100% 100%, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0.9) 15%, rgba(255, 255, 255, 0.6) 30%, rgba(34, 197, 94, 0.7) 45%, rgba(5, 150, 105, 0.85) 60%, rgb(4, 120, 87) 80%, rgb(2, 80, 60) 100%)",
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto text-center z-10">
          <h2 className="text-4xl font-bold mb-4 text-white drop-shadow-lg">
            Ready for Climate Intelligence?
          </h2>
          <p className="text-xl mb-8 text-green-100 drop-shadow">
            When climate data meets intelligence, action becomes possible
          </p>
          <Link
            to="/ai"
            className="inline-block bg-white text-green-700 px-10 py-4 rounded-lg font-bold text-lg hover:bg-green-50 transition shadow-lg"
          >
            Try GreenPulse AI Now
          </Link>
        </div>
      </section>
    </div>
  );
}

export default Home;
