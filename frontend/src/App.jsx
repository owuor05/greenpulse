import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Alerts from "./pages/Alerts";
import AlertDetail from "./pages/AlertDetail";
import Education from "./pages/Education";
import ArticleDetail from "./pages/ArticleDetail";
import Reports from "./pages/Reports";
import About from "./pages/About";
import AI from "./pages/AI";

function App() {
  return (
    <Router
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true
      }}
    >
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/alerts" element={<Alerts />} />
          <Route path="/alerts/:id" element={<AlertDetail />} />
          <Route path="/education" element={<Education />} />
          <Route path="/education/:slug" element={<ArticleDetail />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/about" element={<About />} />
          <Route path="/ai" element={<AI />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
