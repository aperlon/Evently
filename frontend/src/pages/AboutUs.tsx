import { motion } from 'framer-motion';
import { Target, Users, TrendingUp, Globe2, Building2, Brain, Award } from 'lucide-react';

export default function AboutUs() {
  const targetAudiences = [
    {
      icon: Building2,
      title: 'Governments & City Planners',
      description: 'Make data-driven decisions on hosting major events and urban development projects.',
      color: 'blue',
    },
    {
      icon: Users,
      title: 'Event Organizers',
      description: 'Understand economic impact, optimize planning, and demonstrate ROI to stakeholders.',
      color: 'purple',
    },
    {
      icon: Building2,
      title: 'Hotels & Hospitality',
      description: 'Forecast demand, optimize pricing strategies, and maximize revenue during events.',
      color: 'green',
    },
    {
      icon: Brain,
      title: 'Consultancies',
      description: 'Provide clients with comprehensive impact analysis and strategic recommendations.',
      color: 'orange',
    },
  ];

  const values = [
    {
      icon: Target,
      title: 'Data-Driven',
      description: 'Every insight backed by real data, rigorous analysis, and proven methodologies.',
    },
    {
      icon: Globe2,
      title: 'Global Perspective',
      description: 'Coverage across 16 major cities spanning 5 continents worldwide.',
    },
    {
      icon: TrendingUp,
      title: 'Actionable Insights',
      description: 'Not just reports - practical recommendations that drive real business value.',
    },
    {
      icon: Award,
      title: 'Excellence',
      description: 'Combining Design Thinking with advanced analytics for innovative solutions.',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white py-20"
      >
        <div className="max-w-4xl mx-auto px-6 text-center">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-5xl font-bold mb-6"
          >
            About Evently and us
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-xl leading-relaxed opacity-90"
          >
            We transform complex event data into clear, actionable insights that help cities,
            organizers, and businesses make smarter decisions about major urban events.
          </motion.p>
        </div>
      </motion.section>

      {/* Mission & Vision */}
      <section className="py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100"
            >
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Target className="w-6 h-6 text-blue-600" />
              </div>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Mission</h2>
              <p className="text-gray-600 leading-relaxed">
                To democratize access to comprehensive event impact analysis, empowering
                stakeholders with the data and insights needed to create more successful,
                sustainable, and economically beneficial urban events worldwide.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100"
            >
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <Globe2 className="w-6 h-6 text-purple-600" />
              </div>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Vision</h2>
              <p className="text-gray-600 leading-relaxed">
                To become the global standard for event impact analysis, helping cities around
                the world maximize the positive economic and social benefits of major events
                while minimizing risks and uncertainties.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Value Proposition */}
      <section className="py-16 px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Why Choose Evently?</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              We combine advanced analytics, Design Thinking methodology, and real-world data
              to deliver insights that actually matter.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {values.map((value, idx) => (
              <motion.div
                key={value.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="bg-white p-6 rounded-xl shadow-md hover:shadow-xl transition-shadow"
              >
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mb-4">
                  <value.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">{value.title}</h3>
                <p className="text-gray-600 text-sm">{value.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Target Audience */}
      <section className="py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Who We Serve</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Evently is designed for decision-makers who need reliable data to plan,
              execute, and evaluate major urban events.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-8">
            {targetAudiences.map((audience, idx) => (
              <motion.div
                key={audience.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.15 }}
                className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 hover:border-blue-300 transition-all"
              >
                <div
                  className={`w-14 h-14 bg-${audience.color}-100 rounded-xl flex items-center justify-center mb-4`}
                >
                  <audience.icon className={`w-7 h-7 text-${audience.color}-600`} />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">{audience.title}</h3>
                <p className="text-gray-600 leading-relaxed">{audience.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-6 bg-gradient-to-br from-blue-600 to-purple-700 text-white">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl font-bold mb-4">Impact by Numbers</h2>
            <p className="text-xl opacity-90">
              Real results from our comprehensive event analysis platform
            </p>
          </motion.div>

          <div className="grid md:grid-cols-4 gap-8 text-center">
            {[
              { value: '$12.4B', label: 'Economic Impact Analyzed' },
              { value: '847K', label: 'Jobs Created' },
              { value: '16', label: 'Global Cities' },
              { value: '420%', label: 'Average Event ROI' },
            ].map((stat, idx) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
              >
                <div className="text-5xl font-bold mb-2">{stat.value}</div>
                <div className="text-lg opacity-80">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-6">
              Ready to Analyze Your Next Event?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Join leading cities and organizations using Evently to make data-driven decisions.
            </p>
            <div className="flex gap-4 justify-center">
              <a
                href="/dashboard"
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:shadow-lg transition-all"
              >
                Get Started
              </a>
              <a
                href="/case-studies"
                className="px-8 py-4 bg-white text-gray-900 font-semibold rounded-lg border-2 border-gray-300 hover:border-blue-600 transition-all"
              >
                View Case Studies
              </a>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
