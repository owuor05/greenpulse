import { Link } from "react-router-dom";

function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">T</span>
              </div>
              <span className="font-display font-bold text-xl text-white">
                GreenPulse
              </span>
            </div>
            <p className="text-sm text-gray-400">
              Guarding the Land. Empowering the People.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <Link
                  to="/alerts"
                  className="text-sm hover:text-primary-400 transition-colors"
                >
                  View Alerts
                </Link>
              </li>
              <li>
                <Link
                  to="/education"
                  className="text-sm hover:text-primary-400 transition-colors"
                >
                  Education Hub
                </Link>
              </li>
              <li>
                <Link
                  to="/reports"
                  className="text-sm hover:text-primary-400 transition-colors"
                >
                  Community Reports
                </Link>
              </li>
              <li>
                <Link
                  to="/about"
                  className="text-sm hover:text-primary-400 transition-colors"
                >
                  About Us
                </Link>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="text-white font-semibold mb-4">Resources</h4>
            <ul className="space-y-2">
              <li>
                <a
                  href="#"
                  className="text-sm hover:text-primary-400 transition-colors"
                >
                  Climate Data
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-sm hover:text-primary-400 transition-colors"
                >
                  API Documentation
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-sm hover:text-primary-400 transition-colors"
                >
                  Research Papers
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-sm hover:text-primary-400 transition-colors"
                >
                  Partner Organizations
                </a>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-white font-semibold mb-4">Contact</h4>
            <ul className="space-y-2">
              <li className="text-sm">
                <span className="text-gray-400">Email:</span>{" "}
                <a
                  href="mailto:info@terraguard.com"
                  className="hover:text-primary-400 transition-colors"
                >
                  info@greenpulse.com
                </a>
              </li>

              <li className="text-sm">
                <span className="text-gray-400">Location:</span>{" "}
                <span>Nairobi, Kenya</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm">
          <p>
            &copy; {new Date().getFullYear()} GreenPulse. 
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
