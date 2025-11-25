import { useState } from 'react';
import { motion } from 'framer-motion';
import { Calendar, Users, TrendingUp, Building2, Music, Trophy, Briefcase, Sparkles, DollarSign, Clock, Search } from 'lucide-react';

interface MockEvent {
  id: number;
  name: string;
  type: string;
  category: string;
  date: string;
  expectedAttendance: number;
  description: string;
  organizer: string;
  icon: any;
  status: 'seeking' | 'negotiating' | 'confirmed';
  cityRequirements: string[];
  preferredRegions: string[];
  budget: string;
  duration: string;
}

const mockEvents: MockEvent[] = [
  {
    id: 1,
    name: 'ZARA Marathon',
    type: 'Sports',
    category: 'marathon',
    date: '2025-06-15',
    expectedAttendance: 45000,
    description: 'Annual international marathon seeking a vibrant European city with excellent infrastructure, scenic routes, and strong community support. We bring world-class organization and international media coverage.',
    organizer: 'ZARA Foundation',
    icon: Trophy,
    status: 'seeking',
    cityRequirements: ['Airport access', 'Public transport', 'Scenic routes', 'Medical facilities'],
    preferredRegions: ['Europe', 'North America'],
    budget: '$500K - $1M',
    duration: '1 day',
  },
  {
    id: 2,
    name: 'STARTUP YC EVENT',
    type: 'Business',
    category: 'conference',
    date: '2025-05-20',
    expectedAttendance: 5000,
    description: 'Exclusive startup conference featuring Y Combinator alumni, investors, and industry leaders. Seeking a tech-forward city with modern conference facilities and strong startup ecosystem.',
    organizer: 'Y Combinator',
    icon: Briefcase,
    status: 'seeking',
    cityRequirements: ['Tech hub', 'Conference center', 'Hotel capacity', 'International airport'],
    preferredRegions: ['North America', 'Europe', 'Asia'],
    budget: '$300K - $600K',
    duration: '3 days',
  },
  {
    id: 3,
    name: 'Music Festival',
    type: 'Music',
    category: 'festival',
    date: '2025-07-10',
    expectedAttendance: 80000,
    description: 'Three-day music festival featuring top international artists. Looking for a coastal city with large outdoor venues, excellent weather, and vibrant nightlife scene.',
    organizer: 'International Music Events',
    icon: Music,
    status: 'negotiating',
    cityRequirements: ['Outdoor venue', 'Coastal location', 'Sound permits', 'Camping facilities'],
    preferredRegions: ['Europe', 'Mediterranean'],
    budget: '$2M - $4M',
    duration: '3 days',
  },
  {
    id: 4,
    name: 'Tech Summit',
    type: 'Business',
    category: 'summit',
    date: '2025-04-18',
    expectedAttendance: 12000,
    description: 'Premier technology summit bringing together innovators, entrepreneurs, and investors. Seeking a major metropolitan area with strong tech industry presence and world-class venues.',
    organizer: 'Global Tech Events',
    icon: Building2,
    status: 'seeking',
    cityRequirements: ['Tech ecosystem', 'Convention center', 'Business district', 'International connectivity'],
    preferredRegions: ['Europe', 'North America', 'Asia'],
    budget: '$800K - $1.5M',
    duration: '2 days',
  },
  {
    id: 5,
    name: 'Fashion Week',
    type: 'Culture',
    category: 'fashion',
    date: '2025-09-25',
    expectedAttendance: 25000,
    description: 'World-renowned fashion week showcasing latest collections. Looking for a fashion capital with luxury venues, media infrastructure, and cultural prestige.',
    organizer: 'Fédération de la Haute Couture',
    icon: Sparkles,
    status: 'seeking',
    cityRequirements: ['Fashion district', 'Luxury venues', 'Media facilities', 'Cultural prestige'],
    preferredRegions: ['Europe', 'North America'],
    budget: '$1.5M - $3M',
    duration: '7 days',
  },
  {
    id: 6,
    name: 'Innovation Expo',
    type: 'Business',
    category: 'expo',
    date: '2025-08-05',
    expectedAttendance: 30000,
    description: 'International innovation expo featuring cutting-edge technology and startups. Seeking a forward-thinking city with excellent expo facilities and strong innovation culture.',
    organizer: 'Global Innovation Hub',
    icon: TrendingUp,
    status: 'seeking',
    cityRequirements: ['Expo center', 'Innovation hub', 'International access', 'Tech infrastructure'],
    preferredRegions: ['Asia', 'Europe', 'North America'],
    budget: '$1M - $2M',
    duration: '5 days',
  },
  {
    id: 7,
    name: 'Startup Weekend',
    type: 'Business',
    category: 'workshop',
    date: '2025-05-10',
    expectedAttendance: 3000,
    description: 'Intensive 54-hour event where entrepreneurs pitch ideas and launch startups. Looking for a city with vibrant startup community and flexible event spaces.',
    organizer: 'Techstars',
    icon: Briefcase,
    status: 'seeking',
    cityRequirements: ['Startup ecosystem', 'Flexible venues', 'Co-working spaces', 'Tech community'],
    preferredRegions: ['Europe', 'North America'],
    budget: '$50K - $150K',
    duration: '3 days',
  },
  {
    id: 8,
    name: 'Design Fair',
    type: 'Culture',
    category: 'fair',
    date: '2025-06-28',
    expectedAttendance: 15000,
    description: 'Premier design fair showcasing contemporary design and creative industries. Seeking a design-forward city with exhibition spaces and strong creative community.',
    organizer: 'Dutch Design Foundation',
    icon: Sparkles,
    status: 'negotiating',
    cityRequirements: ['Exhibition halls', 'Design district', 'Creative community', 'Cultural venues'],
    preferredRegions: ['Europe', 'North America'],
    budget: '$400K - $800K',
    duration: '4 days',
  },
];

const eventTypes = ['All', 'Sports', 'Business', 'Music', 'Culture'];
const categories = ['All', 'marathon', 'conference', 'festival', 'summit', 'fashion', 'expo', 'workshop', 'fair'];

function CitiesComparison() {
  const [selectedType, setSelectedType] = useState('All');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredEvents = mockEvents.filter((event) => {
    const matchesType = selectedType === 'All' || event.type === selectedType;
    const matchesCategory = selectedCategory === 'All' || event.category === selectedCategory;
    const matchesSearch =
      event.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      event.organizer.toLowerCase().includes(searchQuery.toLowerCase()) ||
      event.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      event.preferredRegions.some((region) => region.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesType && matchesCategory && matchesSearch;
  });

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  };

  return (
    <div className="min-h-screen bg-sky-50">
      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-sky-50 text-gray-900 py-16"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <h1 className="text-3xl font-display text-gray-900 leading-tight mb-4">
              Event Portal
            </h1>
            <p className="text-gray-800 font-mono max-w-3xl mx-auto">
              Events seeking host cities. Browse events looking for the perfect location to bring their vision to life.
            </p>
          </motion.div>

          {/* Search and Filters */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 mb-8">
            <div className="space-y-4">
              {/* Search Bar */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search events, organizers, regions, or keywords..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-200 lg:border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 bg-gray-50 lg:bg-white text-gray-700 lg:text-gray-800 font-mono"
                />
              </div>

              {/* Filters */}
              <div className="flex flex-wrap gap-4">
                <div>
                  <label className="block text-sm text-gray-700 font-mono mb-2">Event Type</label>
                  <select
                    value={selectedType}
                    onChange={(e) => setSelectedType(e.target.value)}
                    className="px-4 py-2 border border-gray-200 lg:border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 bg-gray-50 lg:bg-white text-gray-700 lg:text-gray-800 font-mono"
                  >
                    {eventTypes.map((type) => (
                      <option key={type} value={type}>
                        {type}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-gray-700 font-mono mb-2">Category</label>
                  <select
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                    className="px-4 py-2 border border-gray-200 lg:border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 bg-gray-50 lg:bg-white text-gray-700 lg:text-gray-800 font-mono"
                  >
                    {categories.map((category) => (
                      <option key={category} value={category}>
                        {category.charAt(0).toUpperCase() + category.slice(1)}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Events Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredEvents.map((event, idx) => {
              const IconComponent = event.icon;
              return (
                <motion.div
                  key={event.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all"
                >
                  {/* Event Header */}
                  <div className="bg-gradient-to-br from-sky-100 to-sky-50 p-6 border-b border-gray-100">
                    <div className="flex items-start justify-between mb-4">
                      <div className="w-12 h-12 bg-white rounded-lg flex items-center justify-center shadow-sm">
                        <IconComponent className="w-6 h-6 text-sky-600" />
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-mono border ${
                        event.status === 'seeking' 
                          ? 'bg-yellow-100 text-yellow-800 border-yellow-200'
                          : event.status === 'negotiating'
                          ? 'bg-blue-100 text-blue-800 border-blue-200'
                          : 'bg-green-100 text-green-800 border-green-200'
                      }`}>
                        {event.status}
                      </span>
                    </div>
                    <h3 className="text-xl font-display text-gray-900 mb-2">{event.name}</h3>
                    <p className="text-sm text-gray-800 font-mono">{event.organizer}</p>
                  </div>

                  {/* Event Body */}
                  <div className="p-6 space-y-4">
                    <p className="text-gray-800 font-mono text-sm leading-relaxed">{event.description}</p>

                    <div className="space-y-2 pt-4 border-t border-gray-100">
                      <div className="flex items-center gap-2 text-sm text-gray-800 font-mono">
                        <Calendar className="w-4 h-4 text-sky-600 flex-shrink-0" />
                        <span>Target date: {formatDate(event.date)}</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-gray-800 font-mono">
                        <Clock className="w-4 h-4 text-sky-600 flex-shrink-0" />
                        <span>Duration: {event.duration}</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-gray-800 font-mono">
                        <Users className="w-4 h-4 text-sky-600 flex-shrink-0" />
                        <span>{event.expectedAttendance.toLocaleString()} expected attendees</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-gray-800 font-mono">
                        <DollarSign className="w-4 h-4 text-sky-600 flex-shrink-0" />
                        <span>Budget: {event.budget}</span>
                      </div>
                    </div>

                    {/* City Requirements */}
                    <div className="pt-4 border-t border-gray-100">
                      <p className="text-xs text-gray-700 font-mono mb-2 font-semibold">City Requirements:</p>
                      <div className="flex flex-wrap gap-2">
                        {event.cityRequirements.map((req, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-1 bg-gray-50 text-gray-700 rounded text-xs font-mono border border-gray-200"
                          >
                            {req}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Preferred Regions */}
                    <div className="pt-4 border-t border-gray-100">
                      <p className="text-xs text-gray-700 font-mono mb-2 font-semibold">Preferred Regions:</p>
                      <div className="flex flex-wrap gap-2">
                        {event.preferredRegions.map((region, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-1 bg-sky-50 text-sky-800 rounded text-xs font-mono border border-sky-200"
                          >
                            {region}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Tags */}
                    <div className="flex items-center gap-2 pt-4 border-t border-gray-100">
                      <span className="px-3 py-1 bg-sky-50 text-sky-800 rounded-full text-xs font-mono border border-sky-200">
                        {event.type}
                      </span>
                      <span className="px-3 py-1 bg-gray-50 text-gray-800 rounded-full text-xs font-mono border border-gray-200">
                        {event.category}
                      </span>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>

          {filteredEvents.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-800 font-mono">No events found matching your criteria.</p>
            </div>
          )}
        </div>
      </motion.section>
    </div>
  );
}

export default CitiesComparison;
