import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Globe2, Mail, Github, Linkedin, Twitter } from 'lucide-react';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const footerSections = [
    {
      title: 'Product',
      links: [
        { name: 'Dashboard', path: '/dashboard' },
        { name: 'Events', path: '/events' },
        { name: 'Compare', path: '/compare' },
        { name: 'Predict', path: '/predict' },
        { name: 'What-If Analysis', path: '/simulator' },
      ],
    },
    {
      title: 'Company',
      links: [
        { name: 'About Us', path: '/about' },
        { name: 'Methodology', path: '/methodology' },
      ],
    },
    {
      title: 'Resources',
      links: [
        { name: 'Documentation', path: '#' },
        { name: 'API Reference', path: '#' },
        { name: 'Help Center', path: '#' },
        { name: 'Contact', path: '#' },
      ],
    },
  ];

  return (
    <footer className="bg-gradient-to-br from-mellow-cream to-mellow-ice border-t border-mellow-cream text-gray-900">
      <div className="max-w-7xl mx-auto px-6 pt-32 pb-12">
        {/* Top Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 mb-8">
          {/* Brand Section */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="flex items-center gap-2 mb-4"
            >
              <Globe2 className="w-8 h-8 text-gray-800" />
              <span className="text-2xl font-display text-gray-900">
                Evently
              </span>
            </motion.div>
            <p className="text-gray-700 mb-6 max-w-sm font-mono">
              Analyzing the economic and touristic impact of major urban events across global cities.
              Data-driven insights for smarter event planning.
            </p>
            <div className="flex gap-4">
              <motion.a
                href="#"
                whileHover={{ scale: 1.1 }}
                className="text-gray-700 hover:text-gray-900 transition-colors"
              >
                <Twitter className="w-5 h-5" />
              </motion.a>
              <motion.a
                href="#"
                whileHover={{ scale: 1.1 }}
                className="text-gray-700 hover:text-gray-900 transition-colors"
              >
                <Linkedin className="w-5 h-5" />
              </motion.a>
              <motion.a
                href="#"
                whileHover={{ scale: 1.1 }}
                className="text-gray-700 hover:text-gray-900 transition-colors"
              >
                <Github className="w-5 h-5" />
              </motion.a>
              <motion.a
                href="mailto:info@evently.com"
                whileHover={{ scale: 1.1 }}
                className="text-gray-700 hover:text-gray-900 transition-colors"
              >
                <Mail className="w-5 h-5" />
              </motion.a>
            </div>
          </div>

          {/* Links Sections */}
          {footerSections.map((section, idx) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.1 }}
            >
              <h3 className="font-semibold text-gray-900 mb-4">{section.title}</h3>
              <ul className="space-y-2">
                {section.links.map((link) => (
                  <li key={link.name}>
                    <Link
                      to={link.path}
                      className="text-gray-700 hover:text-gray-900 transition-colors text-sm font-mono"
                    >
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>

        {/* Bottom Section */}
        <div className="border-t border-mellow-ice pt-8 mt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-gray-700 text-sm font-mono">
              © {currentYear} Evently. All rights reserved.
            </p>
            <div className="flex gap-6 text-sm">
              <a href="#" className="text-gray-700 hover:text-gray-900 transition-colors font-mono">
                Privacy Policy
              </a>
              <a href="#" className="text-gray-700 hover:text-gray-900 transition-colors font-mono">
                Terms of Service
              </a>
              <a href="#" className="text-gray-700 hover:text-gray-900 transition-colors font-mono">
                Cookie Policy
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
