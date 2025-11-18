import { motion } from 'framer-motion';
import {
  Database,
  Zap,
  BarChart3,
  Brain,
  TrendingUp,
  ArrowRight,
  CheckCircle2,
  Lightbulb,
  Users,
  Target,
  Rocket,
} from 'lucide-react';

export default function Methodology() {
  const etlSteps = [
    {
      icon: Database,
      title: 'Extract',
      description: 'Data Collection',
      details: [
        'Tourism statistics from official sources',
        'Hotel pricing & occupancy data',
        'Economic indicators & metrics',
        'Mobility & transportation data',
        'CSV/XLSX file uploads',
      ],
      color: 'blue',
    },
    {
      icon: Zap,
      title: 'Transform',
      description: 'Data Processing',
      details: [
        'Data cleaning & validation',
        'Normalization across cities',
        'Baseline period calculation',
        'Statistical analysis',
        'Anomaly detection',
      ],
      color: 'purple',
    },
    {
      icon: BarChart3,
      title: 'Load',
      description: 'Analysis & Insights',
      details: [
        'Impact metrics calculation',
        'ROI & economic multipliers',
        'Visualization generation',
        'Comparative analysis',
        'Predictive modeling',
      ],
      color: 'green',
    },
  ];

  const designThinkingPhases = [
    {
      icon: Lightbulb,
      title: 'Empathize',
      description:
        'Understanding stakeholder needs - governments, organizers, hotels, and consultancies.',
      color: 'yellow',
    },
    {
      icon: Target,
      title: 'Define',
      description:
        'Clearly articulating the problem: measuring real economic impact of urban events.',
      color: 'red',
    },
    {
      icon: Brain,
      title: 'Ideate',
      description:
        'Brainstorming solutions combining data analytics, visualization, and scenario planning.',
      color: 'purple',
    },
    {
      icon: Rocket,
      title: 'Prototype',
      description:
        'Building an interactive platform with real data and actionable insights.',
      color: 'blue',
    },
    {
      icon: Users,
      title: 'Test',
      description:
        'Validating with real-world events and iterating based on stakeholder feedback.',
      color: 'green',
    },
  ];

  const analyticsMetrics = [
    {
      category: 'Tourism Impact',
      metrics: ['Visitor increase %', 'Tourist spending', 'Accommodation nights', 'Avg stay duration'],
    },
    {
      category: 'Hotel Metrics',
      metrics: ['Occupancy rate change', 'Price increase %', 'Revenue per room', 'Booking lead time'],
    },
    {
      category: 'Economic Impact',
      metrics: [
        'Total economic impact ($)',
        'Direct spending',
        'Indirect/induced effects',
        'Jobs created',
      ],
    },
    {
      category: 'ROI Analysis',
      metrics: ['Investment vs returns', 'Economic multiplier', 'Tax revenue generated', 'ROI ratio'],
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-gradient-to-br from-purple-600 via-blue-600 to-purple-800 text-white py-20"
      >
        <div className="max-w-4xl mx-auto px-6 text-center">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-5xl font-bold mb-6"
          >
            Our Methodology
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-xl leading-relaxed opacity-90"
          >
            Combining Design Thinking with advanced ETL pipelines and analytics to deliver
            comprehensive event impact insights.
          </motion.p>
        </div>
      </motion.section>

      {/* Design Thinking */}
      <section className="py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Design Thinking Approach</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              We apply human-centered Design Thinking to ensure our solution truly meets
              stakeholder needs.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-5 gap-4">
            {designThinkingPhases.map((phase, idx) => (
              <motion.div
                key={phase.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="relative"
              >
                <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100 h-full">
                  <div
                    className={`w-12 h-12 bg-${phase.color}-100 rounded-lg flex items-center justify-center mb-3`}
                  >
                    <phase.icon className={`w-6 h-6 text-${phase.color}-600`} />
                  </div>
                  <h3 className="text-lg font-bold text-gray-900 mb-2">{phase.title}</h3>
                  <p className="text-sm text-gray-600">{phase.description}</p>
                </div>
                {idx < designThinkingPhases.length - 1 && (
                  <div className="hidden md:block absolute -right-2 top-1/2 transform -translate-y-1/2 z-10">
                    <ArrowRight className="w-4 h-4 text-gray-400" />
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ETL Pipeline */}
      <section className="py-16 px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">ETL Data Pipeline</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our robust Extract-Transform-Load pipeline ensures data quality and reliable
              insights.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {etlSteps.map((step, idx) => (
              <motion.div
                key={step.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.2 }}
                className="relative"
              >
                <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100">
                  <div
                    className={`w-16 h-16 bg-gradient-to-br from-${step.color}-500 to-${step.color}-700 rounded-xl flex items-center justify-center mb-4`}
                  >
                    <step.icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{step.title}</h3>
                  <p className="text-lg text-gray-600 mb-4">{step.description}</p>
                  <ul className="space-y-2">
                    {step.details.map((detail) => (
                      <li key={detail} className="flex items-start gap-2 text-sm text-gray-600">
                        <CheckCircle2 className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span>{detail}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                {idx < etlSteps.length - 1 && (
                  <div className="hidden md:block absolute -right-4 top-1/2 transform -translate-y-1/2 z-10">
                    <ArrowRight className="w-6 h-6 text-blue-500" />
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Analytics Engine */}
      <section className="py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Analytics Engine</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Comprehensive metrics across multiple dimensions to capture the full impact of
              events.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {analyticsMetrics.map((category, idx) => (
              <motion.div
                key={category.category}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="bg-gradient-to-br from-white to-gray-50 p-6 rounded-xl shadow-lg border border-gray-100"
              >
                <h3 className="text-lg font-bold text-gray-900 mb-4 pb-3 border-b border-gray-200">
                  {category.category}
                </h3>
                <ul className="space-y-2">
                  {category.metrics.map((metric) => (
                    <li key={metric} className="flex items-start gap-2 text-sm text-gray-600">
                      <TrendingUp className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                      <span>{metric}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Impact Calculation */}
      <section className="py-16 px-6 bg-gradient-to-br from-blue-600 to-purple-700 text-white">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl font-bold mb-4">How We Calculate Impact</h2>
            <p className="text-xl opacity-90">
              Our proprietary methodology for measuring event impact
            </p>
          </motion.div>

          <div className="bg-white bg-opacity-10 backdrop-blur-md rounded-2xl p-8 border border-white border-opacity-20">
            <div className="space-y-6">
              <div className="flex items-start gap-4">
                <div className="w-8 h-8 bg-blue-400 rounded-full flex items-center justify-center flex-shrink-0 font-bold">
                  1
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">Baseline Period Analysis</h3>
                  <p className="opacity-90">
                    We analyze 30 days before the event to establish normal patterns in tourism,
                    hotel demand, and economic activity.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="w-8 h-8 bg-purple-400 rounded-full flex items-center justify-center flex-shrink-0 font-bold">
                  2
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">Event Period Measurement</h3>
                  <p className="opacity-90">
                    During and after the event, we track actual performance across all key
                    metrics in real-time.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="w-8 h-8 bg-green-400 rounded-full flex items-center justify-center flex-shrink-0 font-bold">
                  3
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">Comparative Analysis</h3>
                  <p className="opacity-90">
                    We calculate percentage changes and absolute differences to quantify the
                    event's impact.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="w-8 h-8 bg-orange-400 rounded-full flex items-center justify-center flex-shrink-0 font-bold">
                  4
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">Economic Multiplier Effects</h3>
                  <p className="opacity-90">
                    We apply economic multipliers to estimate direct, indirect, and induced
                    spending effects throughout the local economy.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="w-8 h-8 bg-red-400 rounded-full flex items-center justify-center flex-shrink-0 font-bold">
                  5
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">ROI Calculation</h3>
                  <p className="opacity-90">
                    Finally, we calculate return on investment by comparing total economic
                    benefits against event costs and public investment.
                  </p>
                </div>
              </div>
            </div>
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
              See Our Methodology in Action
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Explore real case studies and see how we've analyzed major events worldwide.
            </p>
            <div className="flex gap-4 justify-center">
              <a
                href="/case-studies"
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:shadow-lg transition-all"
              >
                View Case Studies
              </a>
              <a
                href="/dashboard"
                className="px-8 py-4 bg-white text-gray-900 font-semibold rounded-lg border-2 border-gray-300 hover:border-blue-600 transition-all"
              >
                Try the Platform
              </a>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
