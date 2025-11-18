import { motion } from 'framer-motion';
import {
  TrendingUp,
  Users,
  DollarSign,
  Hotel,
  MapPin,
  Calendar,
  Award,
  ArrowUpRight,
  CheckCircle2,
} from 'lucide-react';
import { useState } from 'react';

export default function CaseStudies() {
  const [selectedCase, setSelectedCase] = useState<'rio' | 'paris' | 'tokyo'>('rio');

  const caseStudies = {
    rio: {
      title: 'Rio Carnival 2024',
      city: 'Rio de Janeiro',
      country: 'Brazil',
      date: 'February 9-14, 2024',
      duration: '6 days',
      description:
        'The largest carnival in the world, attracting millions of visitors to Rio de Janeiro for a week of parades, music, and cultural celebration.',
      hero_image_color: 'from-yellow-500 to-orange-600',
      stats: {
        visitors: '2.1M',
        economic_impact: '$1.2B',
        jobs_created: '47,000',
        hotel_occupancy: '98%',
        price_increase: '185%',
        roi: '520%',
      },
      keyInsights: [
        'Hotel prices increased by 185% compared to baseline period',
        'Created 47,000 temporary jobs across hospitality and entertainment sectors',
        'Generated $1.2B in total economic impact (direct + indirect spending)',
        'Tourist spending averaged $890 per person during event period',
        'Hotels achieved 98% occupancy rate, compared to 67% baseline',
        'Economic multiplier effect of 2.8x on direct spending',
      ],
      breakdown: [
        { category: 'Direct Spending', amount: '$430M', percentage: 36 },
        { category: 'Indirect Effects', amount: '$510M', percentage: 42 },
        { category: 'Induced Effects', amount: '$260M', percentage: 22 },
      ],
      timeline: [
        {
          phase: 'Pre-Event (30 days before)',
          metrics: 'Avg hotel price: $120/night, Occupancy: 67%, Daily tourists: 75K',
        },
        {
          phase: 'Event Period (6 days)',
          metrics: 'Avg hotel price: $342/night, Occupancy: 98%, Daily tourists: 350K',
        },
        {
          phase: 'Post-Event (7 days after)',
          metrics: 'Avg hotel price: $145/night, Occupancy: 71%, Daily tourists: 85K',
        },
      ],
    },
    paris: {
      title: 'Paris Fashion Week Fall/Winter 2024',
      city: 'Paris',
      country: 'France',
      date: 'February 26 - March 5, 2024',
      duration: '8 days',
      description:
        'One of the most prestigious fashion events globally, showcasing haute couture and attracting industry professionals and luxury tourists.',
      hero_image_color: 'from-pink-500 to-purple-600',
      stats: {
        visitors: '320K',
        economic_impact: '$685M',
        jobs_created: '12,500',
        hotel_occupancy: '94%',
        price_increase: '142%',
        roi: '380%',
      },
      keyInsights: [
        'Luxury hotel segment saw 210% price increase during event',
        'High-spending tourists averaged $2,340 per person',
        'Fashion industry buyers generated 45% of total economic impact',
        'Michelin-starred restaurants reported 87% increase in reservations',
        'Retail sales in luxury boutiques increased by 156%',
        'Media coverage reached 2.8 billion impressions globally',
      ],
      breakdown: [
        { category: 'Direct Spending', amount: '$275M', percentage: 40 },
        { category: 'Indirect Effects', amount: '$274M', percentage: 40 },
        { category: 'Induced Effects', amount: '$136M', percentage: 20 },
      ],
      timeline: [
        {
          phase: 'Pre-Event (30 days before)',
          metrics: 'Avg hotel price: $245/night, Occupancy: 78%, Daily tourists: 42K',
        },
        {
          phase: 'Event Period (8 days)',
          metrics: 'Avg hotel price: $593/night, Occupancy: 94%, Daily tourists: 40K',
        },
        {
          phase: 'Post-Event (7 days after)',
          metrics: 'Avg hotel price: $268/night, Occupancy: 80%, Daily tourists: 43K',
        },
      ],
    },
    tokyo: {
      title: 'Tokyo Game Show 2024',
      city: 'Tokyo',
      country: 'Japan',
      date: 'September 26-29, 2024',
      duration: '4 days',
      description:
        'Asia\'s largest gaming convention, attracting gamers, developers, and industry professionals from around the world.',
      hero_image_color: 'from-blue-500 to-cyan-600',
      stats: {
        visitors: '243K',
        economic_impact: '$428M',
        jobs_created: '8,900',
        hotel_occupancy: '91%',
        price_increase: '98%',
        roi: '340%',
      },
      keyInsights: [
        'International attendees comprised 35% of total visitors',
        'Gaming merchandise sales exceeded $45M during the event',
        'Nearby restaurants reported 165% increase in revenue',
        'Public transportation usage increased by 28% in the area',
        'Hotels within 5km radius achieved 95% occupancy',
        'Social media engagement generated 1.2B impressions',
      ],
      breakdown: [
        { category: 'Direct Spending', amount: '$172M', percentage: 40 },
        { category: 'Indirect Effects', amount: '$171M', percentage: 40 },
        { category: 'Induced Effects', amount: '$85M', percentage: 20 },
      ],
      timeline: [
        {
          phase: 'Pre-Event (30 days before)',
          metrics: 'Avg hotel price: $180/night, Occupancy: 82%, Daily tourists: 95K',
        },
        {
          phase: 'Event Period (4 days)',
          metrics: 'Avg hotel price: $356/night, Occupancy: 91%, Daily tourists: 60K',
        },
        {
          phase: 'Post-Event (7 days after)',
          metrics: 'Avg hotel price: $195/night, Occupancy: 84%, Daily tourists: 98K',
        },
      ],
    },
  };

  const currentCase = caseStudies[selectedCase];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className={`bg-gradient-to-br ${currentCase.hero_image_color} text-white py-20`}
      >
        <div className="max-w-6xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="flex items-center gap-2 mb-4">
              <Award className="w-6 h-6" />
              <span className="text-sm uppercase tracking-wide font-semibold">Case Study</span>
            </div>
            <h1 className="text-5xl font-bold mb-4">{currentCase.title}</h1>
            <div className="flex flex-wrap gap-4 text-lg opacity-90 mb-6">
              <div className="flex items-center gap-2">
                <MapPin className="w-5 h-5" />
                {currentCase.city}, {currentCase.country}
              </div>
              <div className="flex items-center gap-2">
                <Calendar className="w-5 h-5" />
                {currentCase.date}
              </div>
            </div>
            <p className="text-xl leading-relaxed opacity-90 max-w-3xl">
              {currentCase.description}
            </p>
          </motion.div>
        </div>
      </motion.section>

      {/* Case Study Tabs */}
      <section className="border-b bg-white sticky top-0 z-10 shadow-sm">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex gap-2 overflow-x-auto">
            {Object.entries(caseStudies).map(([key, study]) => (
              <button
                key={key}
                onClick={() => setSelectedCase(key as any)}
                className={`px-6 py-4 font-semibold whitespace-nowrap transition-all ${
                  selectedCase === key
                    ? 'border-b-4 border-blue-600 text-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {study.city}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Key Stats */}
      <section className="py-12 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6"
          >
            {[
              { icon: Users, label: 'Visitors', value: currentCase.stats.visitors, color: 'blue' },
              {
                icon: DollarSign,
                label: 'Economic Impact',
                value: currentCase.stats.economic_impact,
                color: 'green',
              },
              {
                icon: Users,
                label: 'Jobs Created',
                value: currentCase.stats.jobs_created,
                color: 'purple',
              },
              {
                icon: Hotel,
                label: 'Occupancy',
                value: currentCase.stats.hotel_occupancy,
                color: 'orange',
              },
              {
                icon: TrendingUp,
                label: 'Price Increase',
                value: currentCase.stats.price_increase,
                color: 'red',
              },
              { icon: Award, label: 'ROI', value: currentCase.stats.roi, color: 'cyan' },
            ].map((stat, idx) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.05 }}
                className="bg-gradient-to-br from-gray-50 to-white p-6 rounded-xl shadow-md border border-gray-100"
              >
                <stat.icon className={`w-8 h-8 text-${stat.color}-500 mb-3`} />
                <div className="text-3xl font-bold text-gray-900 mb-1">{stat.value}</div>
                <div className="text-sm text-gray-600">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Economic Breakdown */}
      <section className="py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Economic Impact Breakdown</h2>
            <p className="text-xl text-gray-600">
              How the {currentCase.stats.economic_impact} total impact was distributed across the
              economy
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6">
            {currentCase.breakdown.map((item, idx) => (
              <motion.div
                key={item.category}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100"
              >
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-bold text-gray-900">{item.category}</h3>
                  <span className="text-sm font-semibold text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
                    {item.percentage}%
                  </span>
                </div>
                <div className="text-4xl font-bold text-gray-900 mb-4">{item.amount}</div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full"
                    style={{ width: `${item.percentage}%` }}
                  />
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Key Insights */}
      <section className="py-16 px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Key Insights</h2>
            <p className="text-xl text-gray-600">
              Critical findings from our comprehensive analysis
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-4">
            {currentCase.keyInsights.map((insight, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.05 }}
                className="flex items-start gap-3 bg-white p-4 rounded-lg shadow-sm border border-gray-100"
              >
                <CheckCircle2 className="w-6 h-6 text-green-500 flex-shrink-0 mt-0.5" />
                <p className="text-gray-700">{insight}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Impact Timeline</h2>
            <p className="text-xl text-gray-600">
              How metrics evolved before, during, and after the event
            </p>
          </motion.div>

          <div className="space-y-6">
            {currentCase.timeline.map((period, idx) => (
              <motion.div
                key={period.phase}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="flex gap-6 items-start"
              >
                <div className="flex flex-col items-center">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold flex-shrink-0">
                    {idx + 1}
                  </div>
                  {idx < currentCase.timeline.length - 1 && (
                    <div className="w-0.5 h-full bg-gray-300 mt-2" style={{ minHeight: '40px' }} />
                  )}
                </div>
                <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100 flex-1">
                  <h3 className="text-xl font-bold text-gray-900 mb-3">{period.phase}</h3>
                  <p className="text-gray-600">{period.metrics}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Conclusion */}
      <section className="py-16 px-6 bg-gradient-to-br from-blue-600 to-purple-700 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <Award className="w-16 h-16 mx-auto mb-6" />
            <h2 className="text-4xl font-bold mb-6">Conclusion</h2>
            <p className="text-xl leading-relaxed opacity-90 mb-8">
              The {currentCase.title} demonstrates the significant economic value that major events
              bring to cities. With a {currentCase.stats.roi} ROI and{' '}
              {currentCase.stats.economic_impact} in total economic impact, this event showcases
              how strategic event planning and execution can deliver substantial benefits to local
              economies, businesses, and communities.
            </p>
            <div className="flex gap-4 justify-center">
              <a
                href="/dashboard"
                className="inline-flex items-center gap-2 px-8 py-4 bg-white text-blue-600 font-semibold rounded-lg hover:shadow-lg transition-all"
              >
                Analyze Your Event
                <ArrowUpRight className="w-5 h-5" />
              </a>
              <a
                href="/methodology"
                className="px-8 py-4 bg-white bg-opacity-10 backdrop-blur-sm text-white font-semibold rounded-lg border-2 border-white border-opacity-30 hover:bg-opacity-20 transition-all"
              >
                Learn Our Methodology
              </a>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
