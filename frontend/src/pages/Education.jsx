import { Link } from "react-router-dom";
import { useEffect } from "react";

function Education() {
  useEffect(() => {
    // Scroll to top when component mounts
    window.scrollTo(0, 0);
  }, []);

  // Educational articles about land rehabilitation in Kenya
  const articles = [
    {
      id: 1,
      title:
        "Land Rehabilitation Measures for Degraded Southern Rangelands in Kenya",
      category: "Land Rehabilitation / Community Impact",
      excerpt:
        "Discover how rehabilitation efforts in Kajiado and Narok are restoring ecological balance and sustaining community livelihoods through assisted natural regeneration and agroforestry.",
      image:
        "https://images.squarespace-cdn.com/content/v1/6197abe80515bc685501422b/e046bafd-dcde-4c5e-b5a5-894c8aeea5b2/6%29%2BGlobe%2BGone%2BGreen%2B-%2BSchools%2B-%2BTree%2BPlanting%2B-%2B2022.jpg",
      readTime: "10 min read",
      slug: "land-rehabilitation-southern-rangelands",
      author: "Dr. Lillian Mwangi",
      date: "2025-10-11",
    },
    {
      id: 2,
      title:
        "Conservation of Riparian Zones and Wetlands in Kenya for Land and Water Security",
      category: "Water & Land Conservation",
      excerpt:
        "Learn how protecting rivers, wetlands, and riparian zones is vital for regulating water flow, maintaining quality, and reducing land degradation across Kenya.",
      image:
        "https://i.natgeofe.com/n/5d47979a-f140-4760-9430-ceb575df3f82/01-trees-africa-climate-change.jpg",
      readTime: "9 min read",
      slug: "conservation-riparian-zones-wetlands",
      author: "Prof. James Odhiambo",
      date: "2025-10-11",
    },
    {
      id: 3,
      title:
        "Prevention of Desertification Through Sustainable Grazing and Rangeland Management in Northern Kenya",
      category: "Land Governance / Prevention Measures",
      excerpt:
        "Explore how rotational grazing, rangeland enclosures, and capacity building are preventing desertification in Turkana, Marsabit, and Samburu counties.",
      image:
        "https://big3africa.org/wp-content/uploads/2024/06/8e97eecd-9e04-4468-b5bf-f36a59bce109.jpg",
      readTime: "11 min read",
      slug: "prevention-desertification-northern-kenya",
      author: "Dr. Mary Wambui",
      date: "2025-10-11",
    },
    {
      id: 4,
      title: "Restoring Soil Health in Kenya for Agricultural Productivity",
      category: "Soil Health / Rehabilitation",
      excerpt:
        "Discover how compost, cover cropping, and reduced tillage are rebuilding soil fertility and increasing yields on smallholder farms across Kenya.",
      image:
        "https://static1.squarespace.com/static/609d274b1bf1ca3944208968/60a9531b9c566c5897a70c74/63359128ec4b9f0d3370c2e6/1751367661577/Erosion%2BControl%2B_%2BThe%2BSarara%2BFoundation%2Bcopy.JPEG?format=1500w",
      readTime: "8 min read",
      slug: "restoring-soil-health-kenya",
      author: "Dr. Robert Thompson",
      date: "2025-10-11",
    },
    {
      id: 5,
      title:
        "Community Land Rights and Governance in Land Degradation Prevention in Kenya",
      category: "Land Governance / Prevention Measures",
      excerpt:
        "Understand how secure land tenure, participatory planning, and local governance are preventing land degradation before it becomes irreversible.",
      image:
        "https://gumlet.assettype.com/downtoearth%2F2025-03-11%2Fcw7zy74w%2FLand-degradation.jpg?ar=40%3A21&auto=format%2Ccompress&enlarge=true&mode=crop&ogImage=true&overlay=false&overlay_position=bottom&overlay_width=100&w=1200",
      readTime: "10 min read",
      slug: "community-land-rights-governance",
      author: "Prof. Gladys Wanjiru",
      date: "2025-10-11",
    },
    {
      id: 6,
      title:
        "Climate-Smart Agriculture as a Tool for Land Rehabilitation in Kenya",
      category: "Agriculture / Rehabilitation",
      excerpt:
        "Learn how conservation agriculture, drought-tolerant crops, and water harvesting are rehabilitating degraded land while maintaining food production.",
      image: "https://scx2.b-cdn.net/gfx/news/2020/restorationo.jpg",
      readTime: "9 min read",
      slug: "climate-smart-agriculture-rehabilitation",
      author: "Dr. Esther Njoki",
      date: "2025-10-11",
    },
    {
      id: 7,
      title:
        "Tree Planting Initiatives and Forest Landscape Restoration in Kenya",
      category: "Forest Conservation / Rehabilitation",
      excerpt:
        "Explore how the 15 Billion Tree Campaign and community nurseries are restoring forests, mitigating climate change, and supporting livelihoods across Kenya.",
      image:
        "https://media.springernature.com/lw685/springer-static/image/chp%3A10.1007%2F698_2022_929/MediaObjects/504861_1_En_929_Fig5_HTML.jpg",
      readTime: "12 min read",
      slug: "tree-planting-forest-restoration",
      author: "Prof. Samuel Kipchumba",
      date: "2025-10-11",
    },
  ];

  const categories = [
    // categories kept for future use; filters are hidden per design update
  ];

  return (
    <div className="min-h-screen font-sans">
      {/* Header - White to Green radial gradient */}
      <section className="relative py-10 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 120% 80% at 0% 0%, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0.95) 20%, rgba(255, 255, 255, 0.7) 40%, rgba(34, 197, 94, 0.75) 55%, rgba(5, 150, 105, 0.9) 70%, rgb(4, 120, 87) 100%)",
          }}
        ></div>
        <div className="relative max-w-7xl mx-auto text-center z-10">
          <h1
            className="text-5xl font-bold mb-4 text-white drop-shadow-lg"
            style={{ color: "black" }}
          >
            Education Hub
          </h1>
          <p className="text-xl text-green-100 drop-shadow">
            Learn climate-smart farming practices and build resilience
          </p>
        </div>
      </section>

      {/* Articles Grid - Flowing green gradient */}
      <section className="relative py-12 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(180deg, rgb(4, 120, 87) 0%, rgb(3, 105, 78) 30%, rgb(2, 90, 68) 50%, rgb(2, 80, 60) 70%, rgb(4, 120, 87) 100%)",
          }}
        ></div>
        <div className="relative max-w-7xl mx-auto z-10">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {articles.map((article) => (
              <div
                key={article.id}
                className="bg-white/95 backdrop-blur-sm rounded-xl shadow-md hover:shadow-xl hover:bg-white transition overflow-hidden"
              >
                <img
                  src={article.image}
                  alt={article.title}
                  className="w-full h-48 object-cover"
                />
                <div className="p-6">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-sm font-semibold text-green-700">
                      {article.category}
                    </span>
                    <span className="text-sm text-gray-500">
                      {article.readTime}
                    </span>
                  </div>
                  <h3 className="text-xl font-bold text-gray-800 mb-3">
                    {article.title}
                  </h3>
                  <p className="text-gray-600 mb-4">{article.excerpt}</p>
                  <Link
                    to={`/education/${article.slug}`}
                    className="inline-block text-green-700 font-semibold hover:text-green-800 transition"
                  >
                    Read Article →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Additional Resources - Green to Dark gradient */}
      <section className="relative py-10 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(135deg, rgb(4, 120, 87) 0%, rgb(2, 80, 60) 25%, rgb(1, 50, 40) 50%, rgb(10, 30, 25) 75%, rgb(5, 15, 12) 100%)",
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto z-10">
          <h2 className="text-3xl font-bold text-center mb-8 text-white">
            Additional Resources
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-md p-6 hover:bg-white transition">
              <h3 className="text-xl font-bold mb-2 text-gray-800">
                Video Tutorials
              </h3>
              <p className="text-gray-600 mb-4">
                Watch step-by-step guides on farming techniques (Coming Soon)
              </p>
            </div>
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-md p-6 hover:bg-white transition">
              <h3 className="text-xl font-bold mb-2 text-gray-800">
                Downloadable Guides
              </h3>
              <p className="text-gray-600 mb-4">
                PDF guides you can print and share with your community (Coming
                Soon)
              </p>
            </div>
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-md p-6 hover:bg-white transition">
              <h3 className="text-xl font-bold mb-2 text-gray-800">
                Ask GreenPulse AI
              </h3>
              <p className="text-gray-600 mb-4">
                Get instant climate intelligence answers via Telegram
              </p>
              <div className="flex gap-3">
                <a
                  href="https://t.me/GreenPulse_AI_bot"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-green-600 hover:text-green-700 font-semibold"
                >
                  Telegram Bot →
                </a>
              </div>
            </div>
            <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-md p-6 hover:bg-white transition">
              <h3 className="text-xl font-bold mb-2 text-gray-800">
                Community Forums
              </h3>
              <p className="text-gray-600 mb-4">
                Connect with other farmers and share experiences (Coming Soon)
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Middle Dark Section - Dark/Black transition */}
      <section className="relative py-10 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(135deg, rgb(5, 15, 12) 0%, rgb(10, 25, 20) 20%, rgb(5, 40, 30) 40%, rgb(2, 50, 40) 60%, rgb(0, 0, 0) 100%)",
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto text-center z-10">
          <h2 className="text-3xl font-bold mb-4 text-white">
            Knowledge is Power
          </h2>
          <p className="text-xl text-green-200 mb-8">
            Empowering Kenyan communities with the information they need to
            protect and rehabilitate their land
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-4xl font-bold text-green-400 mb-2">7+</div>
              <p className="text-green-100">Educational Articles</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-400 mb-2">AI</div>
              <p className="text-green-100">Powered Assistance</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-400 mb-2">Free</div>
              <p className="text-green-100">Forever Access</p>
            </div>
          </div>
        </div>
      </section>

      {/* Impact Section - Dark to Green radial */}
      <section className="relative py-10 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 120% 120% at 100% 100%, rgb(4, 120, 87) 0%, rgba(5, 150, 105, 0.9) 20%, rgba(22, 163, 74, 0.8) 35%, rgb(10, 30, 25) 55%, rgb(5, 15, 12) 70%, rgb(0, 0, 0) 100%)",
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto text-center z-10">
          <h2 className="text-3xl font-bold mb-4 text-white">
            Learn From Experts
          </h2>
          <p className="text-xl text-gray-200 mb-8">
            Our articles are written by agricultural scientists, environmental
            experts, and local practitioners with deep knowledge of Kenyan
            landscapes
          </p>
        </div>
      </section>

      {/* CTA - Green to White radial at bottom right */}
      <section className="relative py-10 px-4 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 120% 120% at 100% 100%, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0.9) 15%, rgba(255, 255, 255, 0.6) 30%, rgba(34, 197, 94, 0.7) 45%, rgba(5, 150, 105, 0.85) 60%, rgb(4, 120, 87) 80%, rgb(2, 80, 60) 100%)",
          }}
        ></div>
        <div className="relative max-w-4xl mx-auto text-center z-10">
          <h2 className="text-3xl font-bold mb-4 text-white drop-shadow-lg">
            Stay Informed, Stay Protected
          </h2>
          <p className="text-xl mb-8 text-green-100 drop-shadow">
            Subscribe to get climate alerts and the latest farming tips
          </p>
          <Link
            to="/#subscribe"
            className="inline-block bg-white text-green-700 px-8 py-3 rounded-lg font-bold hover:bg-green-50 transition shadow-lg"
          >
            Subscribe Now
          </Link>
        </div>
      </section>
    </div>
  );
}

export default Education;
