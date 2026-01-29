import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";

function ArticleDetail() {
  const { slug } = useParams();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);

  const articles = {
    "land-rehabilitation-southern-rangelands": {
      id: 1,
      title: "Land Rehabilitation Measures for Degraded Southern Rangelands in Kenya",
      category: "Land Rehabilitation / Community Impact",
      author: "Dr. Lillian Mwangi",
      date: "2025-10-11",
      content: `
        <h2>Introduction</h2>
        <p>The rangelands in southern Kenya, particularly in counties such as Kajiado and Narok, have suffered from overgrazing, deforestation, and unsustainable farming. Soil fertility has declined, vegetation cover has reduced, and erosion is widespread. Rehabilitation is essential to restore ecological balance and sustain community livelihoods.</p>

        <h2>Rehabilitation and Prevention Measures</h2>
        <p>Efforts underway include:</p>
        <ul>
          <li><strong>Assisted natural regeneration</strong>: Restrict grazing in degraded patches to allow native grasses and shrubs to recover.</li>
          <li><strong>Agroforestry</strong>: Planting trees on farms, integrating fodder trees and shrubs to improve soil structure, shade, and fodder supply.</li>
          <li><strong>Gully plugging and check dams</strong>: In erosion-prone areas, constructing barriers to slow water flow and capture sediment.</li>
          <li><strong>Contour farming and terraces</strong>: On slopes, shaping land to follow contours to reduce runoff and soil loss.</li>
          <li><strong>Mulching and cover crops</strong>: Protecting soil surface, retaining moisture, adding organic matter.</li>
        </ul>

        <h2>Effects on Local Communities</h2>
        <ul>
          <li><strong>Improved pasture</strong>: As vegetation recovers, grazing quality improves for livestock, reducing migration and stress.</li>
          <li><strong>Water retention</strong>: Soil holds more moisture, springs and small streams last longer into dry season.</li>
          <li><strong>Boosted crop yields</strong>: Rehabilitated land yields better harvests, even under erratic rainfall.</li>
          <li><strong>Alternative incomes</strong>: Tree products, seed banks, nursery work provide extra revenue.</li>
          <li><strong>Reduced vulnerability to climate shocks</strong>: Communities are more resilient in droughts or heavy rains.</li>
        </ul>

        <h2>Why It Matters</h2>
        <ul>
          <li><strong>Ecological recovery</strong>: Restoring vegetation reduces erosion, improves soil fertility, enhances biodiversity.</li>
          <li><strong>Climate mitigation</strong>: Trees and soil biomass sequester carbon.</li>
          <li><strong>Food and water security</strong>: Stable land supports steady food production and safer water supplies.</li>
          <li><strong>Economic stability</strong>: Less loss of inputs (fertiliser, seed), less need for emergency aid when lands degrade severely.</li>
        </ul>

        <h2>Case Study: Kajiado Landscape Restoration</h2>
        <p>In Kajiado County, under AFR100 and county-government initiatives, degraded rangeland is being rehabilitated. Communities are planting indigenous trees, protecting riparian zones, controlling grazing. Reports show improved pasture condition, more stable water supplies, and increased incomes from tree seedling nurseries.</p>

        <h2>Conclusion</h2>
        <p>Land rehabilitation in Kenya's southern rangelands is not optional. It secures livelihoods, ecological functions, and community resilience. With sustained investment, technical support, and community ownership, restored land becomes a foundation for resilient futures.</p>
      `,
    },
    "conservation-riparian-zones-wetlands": {
      id: 2,
      title: "Conservation of Riparian Zones and Wetlands in Kenya for Land and Water Security",
      category: "Water & Land Conservation",
      author: "Prof. James Odhiambo",
      date: "2025-10-11",
      content: `
        <h2>Introduction</h2>
        <p>Kenya's rivers, wetlands and riparian zones are under constant threat from encroachment, deforestation, pollution, and unsustainable farming practices. These zones play a vital role in regulating water flow, maintaining water quality, supporting biodiversity, and reducing land degradation.</p>

        <h2>Conservation and Prevention Measures</h2>
        <ul>
          <li><strong>Buffer vegetation zones</strong>: Planting native trees, shrubs along riverbanks to prevent soil erosion and filter runoff.</li>
          <li><strong>Wetland restoration</strong>: Rehabilitating degraded wetlands, re-establishing hydrological flows, planting wetland species.</li>
          <li><strong>Regulation of land use</strong>: Zoning laws, bylaws to restrict development near riparian areas, enforcement to prevent illegal clearing.</li>
          <li><strong>Community sensitisation</strong>: Educate local communities about importance of wetlands; establishing committees to monitor usage and protection.</li>
          <li><strong>Pollution control</strong>: Reducing chemical runoff from farms, controlling waste disposal into waterways.</li>
        </ul>

        <h2>Effects on Local Communities</h2>
        <ul>
          <li><strong>Cleaner water</strong>: Reduced siltation and pollution leads to safer drinking water, lower disease incidence.</li>
          <li><strong>Reduced flood risk</strong>: Riparian zones absorb excess rainwater, reduce overtopping of banks.</li>
          <li><strong>Enhanced biodiversity</strong>: Fish, birds, amphibians recover; wetlands serve as breeding grounds.</li>
          <li><strong>Livelihoods from wetland produce</strong>: Reeds, fish, ecotourism, crafts.</li>
          <li><strong>Climate regulation</strong>: Wetlands store carbon and help in cooling local micro-climates.</li>
        </ul>

        <h2>Why It Matters</h2>
        <ul>
          <li><strong>Water security</strong>: Riparian zones help maintain flow and recharge groundwater.</li>
          <li><strong>Disaster risk reduction</strong>: Mitigates flooding, soil erosion.</li>
          <li><strong>Ecological balance</strong>: Supports many species and ecological services.</li>
          <li><strong>Sustainable development</strong>: Preserves land resources for future generations.</li>
        </ul>

        <h2>Case Study: Ondiri Wetland and Nairobi River Basin</h2>
        <p>Ondiri Wetland in Kiambu County has been restored through community efforts. Tree planting, clean-ups, protection of springs have been part of the effort. Water clarity has improved; bird species diversity increased; local community members report improved domestic and agricultural water availability.</p>

        <h2>Conclusion</h2>
        <p>The conservation of riparian zones and wetlands is critical in Kenya for land and water security. Protecting these areas safeguards ecosystems, community health, livelihoods, and resilience against climate change.</p>
      `,
    },
    "prevention-desertification-northern-kenya": {
      id: 3,
      title: "Prevention of Desertification Through Sustainable Grazing and Rangeland Management in Northern Kenya",
      category: "Land Governance / Prevention Measures",
      author: "Dr. Mary Wambui",
      date: "2025-10-11",
      content: `
        <h2>Introduction</h2>
        <p>Desertification is increasingly affecting northern Kenya counties such as Turkana, Marsabit, Samburu. Traditional grazing, low vegetation cover, frequent drought, and weak institutional support contribute. Preventing desertification is critical for sustaining pastoral livelihoods and ecosystem health.</p>

        <h2>Measures for Prevention</h2>
        <ul>
          <li><strong>Rotational grazing</strong>: Moving livestock between grazing areas to allow vegetation rest and recovery.</li>
          <li><strong>Rangeland enclosures</strong>: Fencing off degraded patches to restore grasses and reduce soil erosion.</li>
          <li><strong>Re-seeding indigenous grasses</strong>: Reintroducing native drought-tolerant grass species to stabilize soil.</li>
          <li><strong>Water harvesting and small scale dams</strong>: Capturing seasonal rivers for livestock and soil moisture support.</li>
          <li><strong>Capacity building</strong>: Training pastoralists in sustainable practices, land rights, climate knowledge.</li>
        </ul>

        <h2>Effects on Communities</h2>
        <ul>
          <li><strong>Livestock survival improved</strong>: Better grazing reduces mortality in drought periods.</li>
          <li><strong>Reduced migration pressure</strong>: Pastoralist families can stay closer to home.</li>
          <li><strong>Food security</strong>: More reliable milk and meat production.</li>
          <li><strong>Social stability</strong>: Fewer conflicts over grazing land and water resources.</li>
          <li><strong>Empowerment</strong>: Local leadership takes part in decision making over rangeland use.</li>
        </ul>

        <h2>Why Important</h2>
        <ul>
          <li><strong>Ecological resilience</strong>: Protecting soil, reducing erosion, maintaining vegetation cover.</li>
          <li><strong>Adaptation to climate change</strong>: When droughts increase, healthy rangelands buffer shocks.</li>
          <li><strong>Economic viability</strong>: Pastoralism contributes to livelihoods; prevention reduces cost of restoration.</li>
          <li><strong>Preservation of culture</strong>: Many communities have traditional grazing practices; keeping lands viable preserves heritage.</li>
        </ul>

        <h2>Case Study: Samburu & Turkana Counties</h2>
        <p>In Samburu, the Sarara Foundation and other groups have trained women in erosion control, built gabions, and helped re-seed native grasses. Results include reduced gullies, improved forage, better livestock health. Communities report greater food and water stability in formerly degraded dry areas.</p>

        <h2>Conclusion</h2>
        <p>Preventing desertification in Kenya's northern rangelands requires both technical measures and governance reforms. The cost of prevention is far less than full restoration. With community engagement, native species, and sustainable grazing, these landscapes can recover and remain productive.</p>
      `,
    },
    "restoring-soil-health-kenya": {
      id: 4,
      title: "Restoring Soil Health in Kenya for Agricultural Productivity",
      category: "Soil Health / Rehabilitation",
      author: "Dr. Robert Thompson",
      date: "2025-10-11",
      content: `
        <h2>Introduction</h2>
        <p>Most smallholder farms in Kenya face declining soil fertility due to repeated cropping without replenishing nutrients, erosion, and loss of organic matter. Restoring soil health is central to increasing yields, reducing input costs, and building long-term sustainability.</p>

        <h2>Measures for Soil Health Restoration</h2>
        <ul>
          <li><strong>Use of compost and manure</strong>: Adding organic amendments to rebuild soil structure and nutrient levels.</li>
          <li><strong>Cover cropping</strong>: Planting legumes or cover plants during fallow periods to fix nitrogen, prevent erosion.</li>
          <li><strong>Reduced tillage</strong>: Minimizing soil disturbance so microbial life and soil aggregates are preserved.</li>
          <li><strong>Crop rotation and intercropping</strong>: Rotating crops and intercropping with legumes or deep-rooted plants to diversify root structures and nutrients.</li>
          <li><strong>Biochar and soil amendments</strong>: Where available, using charcoal-derived soil enhancers to improve water retention and fertility.</li>
        </ul>

        <h2>Effects on Communities</h2>
        <ul>
          <li><strong>Improved yields</strong>: Higher crop output with fewer external fertiliser inputs.</li>
          <li><strong>Reduced costs</strong>: Less spending on chemical inputs, less soil loss.</li>
          <li><strong>Food security</strong>: More stable harvests, especially in seasons with suboptimal rainfall.</li>
          <li><strong>Healthier soils to support diverse crops</strong>: Crop diversity supports nutrition and market resilience.</li>
          <li><strong>Environmental benefits</strong>: Increased organic carbon, water infiltration, reduced erosion.</li>
        </ul>

        <h2>Why It Matters</h2>
        <ul>
          <li><strong>Long-term productivity</strong>: Soil is the foundation of agriculture.</li>
          <li><strong>Climate resilience</strong>: Healthy soils buffer droughts and heavy rains.</li>
          <li><strong>Sustainability</strong>: Less dependency on synthetic fertilisers, more dependence on ecosystem services.</li>
          <li><strong>Economic potential</strong>: More income for farmers, reduced risk.</li>
        </ul>

        <h2>Case Study: Smallholder Farms in Western Kenya</h2>
        <p>In counties like Kisumu, Bungoma and Kakamega, farmers practising cover cropping, improved composting and intercropping have seen soil health improve significantly. The incorporation of organic matter increases moisture retention, reducing risks of crop failure in dry spells.</p>

        <h2>Conclusion</h2>
        <p>Restoration of soil health is a critical component of land rehabilitation in Kenya. It underpins food security, climate resilience, and economic well-being. Scaling up techniques, access to inputs, extension services, and awareness are essential for impact.</p>
      `,
    },
    "community-land-rights-governance": {
      id: 5,
      title: "Community Land Rights and Governance in Land Degradation Prevention in Kenya",
      category: "Land Governance / Prevention Measures",
      author: "Prof. Gladys Wanjiru",
      date: "2025-10-11",
      content: `
        <h2>Introduction</h2>
        <p>Land degradation in Kenya is often worsened by insecure land tenure, land subdivision without sustainable planning, and weak enforcement of environmental laws. Empowering communities with land rights and good governance helps prevent degradation before it becomes irreversible.</p>

        <h2>Preventive Governance Measures</h2>
        <ul>
          <li><strong>Community land registration</strong>: Formal recognition of communal land, group ranches, trust land, to enable local decision making.</li>
          <li><strong>Participatory land‐use planning</strong>: Engaging landowners, pastoralists, farmers in defining how land is used—where to conserve, where to farm, where to graze.</li>
          <li><strong>Bylaws and local rules</strong>: Local councils or committees setting rules about grazing, cutting trees, farming near waterways, enforcing them.</li>
          <li><strong>Legal enforcement</strong>: Strengthening implementation of existing laws (Community Land Act, Environment Management laws, Forest laws). Ensuring penalties for violation.</li>
          <li><strong>Inclusive decision making</strong>: Involvement of women, youth, marginalized groups in governance and benefit sharing.</li>
        </ul>

        <h2>Effects on Communities</h2>
        <ul>
          <li><strong>Greater ownership and motivation</strong>: People take more care of land they legally own or manage.</li>
          <li><strong>Reduced encroachment and misuse</strong>: Less illegal logging, unplanned settlements, destructive farming.</li>
          <li><strong>Improved conflict resolution</strong>: Clear rights, boundaries, and rules reduce disputes among communities.</li>
          <li><strong>Equity</strong>: More inclusion of vulnerable groups leads to fairer benefit sharing and recognition.</li>
        </ul>

        <h2>Why It Matters</h2>
        <ul>
          <li><strong>Prevention is cheaper</strong>: Avoiding degradation is less costly than full restoration.</li>
          <li><strong>Sustainable resource use</strong>: Clear rights encourage conservation rather than exploitation.</li>
          <li><strong>Resilience to climate shocks</strong>: Secure land rights allow communities to invest in long-term conservation practices.</li>
          <li><strong>Social and economic justice</strong>: Ensures land users have rights, responsibilities, and benefits.</li>
        </ul>

        <h2>Case Study: Namati Community Land Protection Program</h2>
        <p>Namati and partners have helped communities register lands, map boundaries, set local governance rules. In places where this has succeeded, there is less illegal land conversion, better vegetation cover, and more sustained land care practices.</p>

        <h2>Conclusion</h2>
        <p>Governance and land rights are fundamental to prevent land degradation. They enable durable solutions and ensure conservation efforts are not undermined by insecure tenure or inequitable decision-making.</p>
      `,
    },
    "climate-smart-agriculture-rehabilitation": {
      id: 6,
      title: "Climate-Smart Agriculture as a Tool for Land Rehabilitation in Kenya",
      category: "Agriculture / Rehabilitation",
      author: "Dr. Esther Njoki",
      date: "2025-10-11",
      content: `
        <h2>Introduction</h2>
        <p>Climate-smart agriculture (CSA) integrates adaptation, mitigation and productivity to respond to climate challenges. For Kenya's farming communities, CSA offers practices that rehabilitate degraded land while maintaining food production under changeable climate.</p>

        <h2>Practices Under Climate-Smart Agriculture</h2>
        <ul>
          <li><strong>Conservation agriculture</strong>: Minimal tillage, permanent soil cover, crop rotations.</li>
          <li><strong>Drought-tolerant and improved seed varieties</strong>: Selecting crops that tolerate dry spells or erratic rainfall.</li>
          <li><strong>Water harvesting</strong>: Rainwater ponds, zai pits, contour bunds to capture runoff.</li>
          <li><strong>Integrated soil fertility management</strong>: Combining organic and inorganic fertilisers wisely.</li>
          <li><strong>Use of shade trees and agroforestry</strong>: Trees interspersed with crops to reduce heat stress, improve microclimates.</li>
        </ul>

        <h2>Effects on Communities</h2>
        <ul>
          <li><strong>Yield stability</strong>: Even in tough seasons, farms perform better.</li>
          <li><strong>Lower input costs</strong>: Less reliance on chemical fertilisers and heavy ploughing.</li>
          <li><strong>Improved resilience</strong>: Farms better able to resist droughts, storms.</li>
          <li><strong>Healthier ecosystems</strong>: Good soil moisture, less erosion, more organic matter.</li>
          <li><strong>Livelihood diversification</strong>: Agroforestry products, water harvesting structures provide extra income.</li>
        </ul>

        <h2>Why It Matters</h2>
        <ul>
          <li><strong>Food security</strong>: Feeding communities reliably under climatic uncertainty.</li>
          <li><strong>Environmental sustainability</strong>: Reducing greenhouse gas emissions, improving land health.</li>
          <li><strong>Adaptation and mitigation combined</strong>: CSA helps communities adapt while contributing to mitigation.</li>
          <li><strong>Economical benefits</strong>: More efficient use of water, soil, inputs leads to savings and improved incomes.</li>
        </ul>

        <h2>Case Study: Semi-arid Eastern Kenya (Kitui, Makueni, Embu)</h2>
        <p>Farmers in these counties applying conservation agriculture and water harvesting structures report better harvests and soil moisture retention. NGO programmes including extension support have helped scale up these practices.</p>

        <h2>Conclusion</h2>
        <p>Climate-smart agriculture offers a viable pathway for rehabilitating land in Kenya while securing livelihoods. Scaling up requires access to knowledge, seeds, water infrastructure, and policy support.</p>
      `,
    },
    "tree-planting-forest-restoration": {
      id: 7,
      title: "Tree Planting Initiatives and Forest Landscape Restoration in Kenya",
      category: "Forest Conservation / Rehabilitation",
      author: "Prof. Samuel Kipchumba",
      date: "2025-10-11",
      content: `
        <h2>Introduction</h2>
        <p>Forests in Kenya have been lost through deforestation for agriculture, charcoal, logging, and settlement expansion. Restoration via landscape-scale tree planting is part of national and local strategies to rehabilitate land, mitigate climate change, and support communities.</p>

        <h2>Key Measures in Tree Planting Initiatives</h2>
        <ul>
          <li><strong>National tree-growing programmes</strong>: Initiatives like the 15 Billion Tree Campaign, AFR100 to restore degraded landscapes.</li>
          <li><strong>Community nurseries</strong>: Locally managed tree nurseries raise indigenous seedlings for planting.</li>
          <li><strong>Agroforestry systems</strong>: Combining trees with crops and livestock for multiple benefits.</li>
          <li><strong>Forest restoration and assisted natural regeneration</strong>: Protecting degraded forests, allowing regrowth, enriching with native species.</li>
          <li><strong>Monitoring and maintenance</strong>: Ensuring survival of planted trees, pruning, pest control.</li>
        </ul>

        <h2>Effects on Communities</h2>
        <ul>
          <li><strong>Improved climate regulation</strong>: Trees help moderate temperature, rainfall patterns, reduce soil evaporation.</li>
          <li><strong>Income from tree products</strong>: Fruits, wood, fuelwood (if sustainable), honey, timber.</li>
          <li><strong>Environmental services</strong>: Soil retention, water cycle regulation, habitat protection.</li>
          <li><strong>Carbon sequestration</strong>: Trees capture carbon helping Kenya meet climate goals.</li>
          <li><strong>Social cohesion</strong>: Collective planting and forest management bring communities together.</li>
        </ul>

        <h2>Why It Matters</h2>
        <ul>
          <li><strong>Mitigating climate change</strong>: Forests are key carbon sinks.</li>
          <li><strong>Preventing land degradation</strong>: Vegetation cover protects soil, reduces erosion and runoff.</li>
          <li><strong>Biodiversity conservation</strong>: Native species restored, wildlife habitat improved.</li>
          <li><strong>Economic potential</strong>: Forest ecotourism, sustainable harvesting, restoration jobs.</li>
        </ul>

        <h2>Case Study: The Highlands & Mt Kenya Region Restoration</h2>
        <p>In the Mt Kenya and Aberdare regions, government and local communities have established tree nurseries, planted indigenous trees, restored forest corridors. Rainfall retention and water catchment functions have shown improvement; downstream communities benefit from better water flows.</p>

        <h2>Conclusion</h2>
        <p>Tree planting and forest restoration are powerful tools for rehabilitating Kenya's degraded landscapes. With long-term maintenance, community involvement, and careful species selection, these initiatives can significantly contribute to ecological, economic, and social resilience.</p>
      `,
    },
  };

  useEffect(() => {
    // Scroll to top when component mounts
    window.scrollTo(0, 0);

    const fetchArticle = () => {
      setLoading(true);
      setTimeout(() => {
        const foundArticle = articles[slug];
        setArticle(foundArticle);
        setLoading(false);
      }, 500);
    };

    fetchArticle();
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center font-sans">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-2 border-green-600"></div>
          <p className="mt-4 text-gray-600 text-lg">Loading article...</p>
        </div>
      </div>
    );
  }

  if (!article) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4 font-sans">
        <div className="bg-red-50 border-2 border-red-300 rounded-lg p-8 max-w-md text-center">
          <p className="text-red-800 text-lg mb-4">Article not found</p>
          <Link
            to="/education"
            className="inline-block bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition"
          >
            Back to Education
          </Link>
        </div>
      </div>
    );
  }

  const getCategoryColor = (category) => {
    // Use consistent green theme for all articles
    return "bg-gradient-to-r from-emerald-600 to-green-700";
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      {/* Header */}
      <div
        className={`${getCategoryColor(
          article.category
        )} text-white py-16 px-4`}
      >
        <div className="max-w-4xl mx-auto">
          <Link
            to="/education"
            className="inline-flex items-center text-white hover:text-gray-200 mb-6 transition"
          >
            ← Back to Education Hub
          </Link>
          <div className="mb-4">
            <span className="bg-white bg-opacity-20 px-4 py-2 rounded-full text-sm font-medium">
              {article.category}
            </span>
          </div>
          <h1 className="text-4xl font-bold mb-4">{article.title}</h1>
          <div className="flex items-center gap-6 text-white text-opacity-90">
            <span>By {article.author}</span>
            <span>Published {new Date(article.date).toLocaleDateString()}</span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto py-12 px-4">
        <div className="bg-white rounded-xl shadow-md p-8 lg:p-12">
          <div
            className="prose prose-lg max-w-none"
            dangerouslySetInnerHTML={{ __html: article.content }}
            style={{
              fontFamily:
                'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif',
              lineHeight: "1.7",
            }}
          />
        </div>

        {/* Related Articles */}
        <div className="mt-12 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-8 border-2 border-green-200">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            Explore More Educational Content
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Link
              to="/education"
              className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition group"
            >
              <h3 className="text-lg font-semibold text-gray-800 group-hover:text-green-600 transition">
                Climate Adaptation Hub
              </h3>
              <p className="text-gray-600 mt-2">
                Discover strategies to adapt your farming practices to changing
                climate conditions.
              </p>
            </Link>
            <a
              href="https://t.me/TerraGuard_Bot"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition group"
            >
              <h3 className="text-lg font-semibold text-gray-800 group-hover:text-blue-600 transition">
                Ask Our AI Assistant
              </h3>
              <p className="text-gray-600 mt-2">
                Get personalized advice about this topic from our AI-powered
                farming assistant.
              </p>
            </a>
          </div>
        </div>

        {/* Subscription CTA */}
        <div className="mt-8 bg-gradient-to-r from-green-600 to-emerald-600 rounded-xl shadow-lg p-8 text-white">
          <h2 className="text-2xl font-bold mb-4">
            Stay Updated with TerraGuard
          </h2>
          <p className="text-lg mb-6">
            Get the latest climate alerts, educational content, and farming tips
            delivered to you.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <a
              href="https://t.me/TerraGuard_Bot"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition text-center"
            >
              Follow on Telegram
            </a>
            <a
              href="https://wa.me/14155238886?text=join%20actual-mother"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white text-green-600 px-6 py-3 rounded-lg font-semibold hover:bg-green-50 transition text-center"
            >
              Join WhatsApp Updates
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ArticleDetail;
