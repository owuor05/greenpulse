import { useEffect } from "react";
import { Link } from "react-router-dom";

function Home() {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white font-sans">
      {/* Hero Section */}
      <section className="relative py-20 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-green-600 to-emerald-700 opacity-90"></div>
        <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage:
              "url('https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=1200')",
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        ></div>

        <div className="relative max-w-7xl mx-auto text-center text-white z-10">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight font-sans">
            TerraGuard
          </h1>
          <p className="text-2xl md:text-3xl mb-4 font-semibold">
            Guarding the Land. Mazingira yetu ni urithi wetu.
          </p>
          <p className="text-lg md:text-xl max-w-3xl mx-auto mb-10 leading-relaxed">
            Get real-time climate alerts with conservation advice powered by NASA
            data and AI. Protect your soil, rehabilitate degraded land, and build
            sustainable communities through tree planting and environmental stewardship.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="#subscribe"
              className="bg-white text-green-700 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-green-50 transition shadow-lg"
            >
              Start Learning
            </a>
            <Link
              to="/alerts"
              className="bg-green-800 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-green-900 transition shadow-lg"
            >
              View Land Data & Alerts
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
          <div className="p-6">
            <div className="text-4xl font-bold text-gray-900 mb-2">24/7</div>
            <p className="text-gray-600">Climate Monitoring</p>
          </div>
          <div className="p-6">
            <div className="text-4xl font-bold text-gray-900 mb-2">47</div>
            <p className="text-gray-600">Counties in Kenya</p>
          </div>
          <div className="p-6">
            <div className="text-4xl font-bold text-gray-900 mb-2">NASA</div>
            <p className="text-gray-600">Powered Data</p>
          </div>
          <div className="p-6">
            <div className="text-4xl font-bold text-gray-900 mb-2">AI</div>
            <p className="text-gray-600">Conservation Guidance</p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4 text-gray-800">
            How TerraGuard Protects Your Land
          </h2>
          <p className="text-center text-gray-600 mb-12 text-lg">
            Conservation intelligence and education delivered right to your phone
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition">
              <h3 className="text-2xl font-bold mb-3 text-gray-800">
                Real-Time Risk Detection
              </h3>
              <p className="text-gray-600 leading-relaxed">
                NASA satellite data analyzed daily to detect drought, flood
                risks, and temperature extremes before they impact your land and soil health.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition">
              <h3 className="text-2xl font-bold mb-3 text-gray-800">
                AI-Powered Conservation Advice
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Get personalized recommendations on land rehabilitation, soil protection,
                tree planting, and sustainable conservation practices using advanced AI.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition">
              <h3 className="text-2xl font-bold mb-3 text-gray-800">
                Chat Alerts & Education
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Receive instant alerts via Telegram or WhatsApp. Ask questions
                and get expert conservation advice and learning resources.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition">
              <h3 className="text-2xl font-bold mb-3 text-gray-800">
                Location-Specific Alerts
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Subscribe to your specific region. Get alerts relevant to your
                exact location and land conditions.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition">
              <h3 className="text-2xl font-bold mb-3 text-gray-800">
                Conservation Education
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Access practical guides on land rehabilitation, sustainable
                land use, soil health, tree planting, and combating erosion.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition">
              <h3 className="text-2xl font-bold mb-3 text-gray-800">
                Community Reports
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Share observations with your community. Report local land conditions
                and learn from shared conservation experiences.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Subscription Section */}
      <section id="subscribe" className="py-16 px-4 bg-gradient-to-r from-green-600 to-emerald-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-4 text-white">
            Get Conservation Alerts & Education
          </h2>
          <p className="text-xl mb-8 text-green-100">
            Stay informed with real-time climate alerts and conservation advice delivered directly to your Telegram or WhatsApp
          </p>

          <div className="bg-white rounded-xl shadow-2xl p-8 md:p-12">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">
              Choose Your Preferred Platform
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              {/* Telegram */}
              <a
                href="https://t.me/TerraGuard_Bot"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-blue-500 text-white p-8 rounded-xl font-semibold hover:bg-blue-600 transition shadow-lg hover:shadow-xl transform hover:-translate-y-1 flex flex-col items-center gap-4"
              >
                <div className="text-xl font-bold">Open Telegram Bot</div>
                <p className="text-blue-100 text-sm">
                  Get instant alerts and chat with our AI conservation assistant
                </p>
              </a>

              {/* WhatsApp */}
              <a
                href="https://wa.me/14155238886?text=join%20actual-mother"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-green-500 text-white p-8 rounded-xl font-semibold hover:bg-green-600 transition shadow-lg hover:shadow-xl transform hover:-translate-y-1 flex flex-col items-center gap-4"
              >
                <div className="text-xl font-bold">Open WhatsApp</div>
                <p className="text-green-100 text-sm">
                  Receive alerts and ask conservation questions anytime
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
                    <p className="font-semibold text-gray-800">Click a Button</p>
                    <p className="text-sm text-gray-600">Choose Telegram or WhatsApp</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <div className="flex-shrink-0 w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-bold">
                    2
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800">Start Chatting</p>
                    <p className="text-sm text-gray-600">Send a message to the bot</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <div className="flex-shrink-0 w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-bold">
                    3
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800">Get Informed</p>
                    <p className="text-sm text-gray-600">Receive land alerts & conservation tips</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-8 p-6 bg-green-50 rounded-lg border-2 border-green-200">
              <p className="text-gray-700">
                <strong>Tip:</strong> Our AI-powered bots can answer your land conservation questions, 
                help you subscribe to alerts for your region, and provide personalized environmental advice - all for free!
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Impact Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12 text-gray-800">
            Built for Kenyan Communities
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <img
                src="https://cdn.pixabay.com/photo/2015/07/03/08/36/kola-nut-829934_1280.jpg"
                alt="African farmer in field"
                className="rounded-xl shadow-lg"
              />
            </div>
            <div>
              <h3 className="text-2xl font-bold mb-4 text-gray-800">
                Why TerraGuard Matters
              </h3>
              <ul className="space-y-4 text-gray-600 text-lg">
                <li className="flex items-start gap-3">
                  <span className="text-green-600 font-bold text-xl">✓</span>
                  <span>
                    <strong>Early Warning:</strong> Get alerts 7-14 days before
                    climate events impact your land soil or crops. Stay prepared, protect your farm, and plan ahead.
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-green-600 font-bold text-xl">✓</span>
                  <span>
                    <strong>Land Health Insights:</strong> Track soil and vegetation trends in your area,
                    get AI-guided conservation tips, and learn how to restore degraded land through tree planting, terracing, and other sustainable methods.
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-green-600 font-bold text-xl">✓</span>
                  <span>
                    <strong>Local Language:</strong> Accessible in English and Swahili, with more local languages coming soon, 
                    making vital environmental knowledge available to every farmer and community member.
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-green-600 font-bold text-xl">✓</span>
                  <span>
                    <strong>100% Free:</strong>TerraGuard is completely free, ensuring that every farmer, student, 
                    and community leader can access real-time climate and land protection information.
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 bg-gradient-to-r from-emerald-600 to-green-700">
        <div className="max-w-4xl mx-auto text-center text-white">
          <h2 className="text-4xl font-bold mb-4">
            Ready to Protect Your Land?
          </h2>
          <p className="text-xl mb-8 text-green-100">
            Join thousands already learning conservation with TerraGuard
          </p>
          <a
            href="#subscribe"
            className="inline-block bg-white text-green-700 px-10 py-4 rounded-lg font-bold text-lg hover:bg-green-50 transition shadow-lg"
          >
            Get Started Now - Free Forever
          </a>
        </div>
      </section>
    </div>
  );
}

export default Home;
