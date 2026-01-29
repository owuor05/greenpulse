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
      title: "Land Rehabilitation Measures for Degraded Southern Rangelands in Kenya",
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
      title: "Conservation of Riparian Zones and Wetlands in Kenya for Land and Water Security",
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
      title: "Prevention of Desertification Through Sustainable Grazing and Rangeland Management in Northern Kenya",
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
      title: "Community Land Rights and Governance in Land Degradation Prevention in Kenya",
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
      title: "Climate-Smart Agriculture as a Tool for Land Rehabilitation in Kenya",
      category: "Agriculture / Rehabilitation",
      excerpt:
        "Learn how conservation agriculture, drought-tolerant crops, and water harvesting are rehabilitating degraded land while maintaining food production.",
      image:
        "https://scx2.b-cdn.net/gfx/news/2020/restorationo.jpg",
      readTime: "9 min read",
      slug: "climate-smart-agriculture-rehabilitation",
      author: "Dr. Esther Njoki",
      date: "2025-10-11",
    },
    {
      id: 7,
      title: "Tree Planting Initiatives and Forest Landscape Restoration in Kenya",
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
    <div className="min-h-screen bg-gray-50 font-sans">
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-600 to-green-700 text-white py-16 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-4">Education Hub</h1>
          <p className="text-xl text-green-100">
            Learn climate-smart farming practices and build resilience
          </p>
        </div>
      </div>

      {/* Category filters removed per request */}

      {/* Articles Grid */}
      <div className="max-w-7xl mx-auto py-12 px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {articles.map((article) => (
            <div
              key={article.id}
              className="bg-white rounded-xl shadow-md hover:shadow-xl transition overflow-hidden"
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

      {/* Additional Resources */}
      <div className="bg-green-50 py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-8 text-gray-800">
            Additional Resources
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-xl font-bold mb-2 text-gray-800">
                Video Tutorials
              </h3>
              <p className="text-gray-600 mb-4">
                Watch step-by-step guides on farming techniques (Coming Soon)
              </p>
            </div>
            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-xl font-bold mb-2 text-gray-800">
                Downloadable Guides
              </h3>
              <p className="text-gray-600 mb-4">
                PDF guides you can print and share with your community (Coming
                Soon)
              </p>
            </div>
            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-xl font-bold mb-2 text-gray-800">
                Ask Our AI
              </h3>
              <p className="text-gray-600 mb-4">
                Get instant answers to your farming questions via Telegram or
                WhatsApp
              </p>
              <div className="flex gap-3">
                <a
                  href="https://t.me/TerraGuard_Bot"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-green-600 hover:text-green-700 font-semibold"
                >
                  Telegram →
                </a>
                <a
                  href="https://wa.me/14155238886?text=join%20actual-mother"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-green-600 hover:text-green-700 font-semibold"
                >
                  WhatsApp →
                </a>
              </div>
            </div>
            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-xl font-bold mb-2 text-gray-800">
                Community Forums
              </h3>
              <p className="text-gray-600 mb-4">
                Connect with other farmers and share experiences (Coming Soon)
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="bg-gradient-to-r from-emerald-600 to-green-700 text-white py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">
            Stay Informed, Stay Protected
          </h2>
          <p className="text-xl mb-8 text-green-100">
            Subscribe to get climate alerts and the latest farming tips
          </p>
          <Link
            to="/#subscribe"
            className="inline-block bg-white text-green-700 px-8 py-3 rounded-lg font-bold hover:bg-green-50 transition shadow-lg"
          >
            Subscribe Now
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Education;
