// Map event types to images
export const eventImages: Record<string, string> = {
  'Sports': '/media/IMAGESEVENTLY/bernabeu.png',
  'Concert': '/media/IMAGESEVENTLY/concert.jpg',
  'Festival': '/media/IMAGESEVENTLY/festival.png',
  'Music Festival': '/media/IMAGESEVENTLY/festival2.png',
  'Cultural': '/media/IMAGESEVENTLY/lantern.jpg',
  'Conference': '/media/IMAGESEVENTLY/openai.png',
  'Technology': '/media/IMAGESEVENTLY/openai.png',
  // Default fallback
  'default': '/media/IMAGESEVENTLY/festival.png',
}

// Get image for event based on name and type
export const getEventImage = (eventType: string, eventName?: string): string => {
  const name = eventName?.toLowerCase() || ''
  
  // Check for specific event names first
  if (name.includes('marathon')) {
    return '/media/IMAGESEVENTLY/maraton.jpg'
  }
  
  if (name.includes('wimbledon') || name.includes('champions league') || name.includes('roland garros')) {
    return '/media/IMAGESEVENTLY/bernabeu.png'
  }
  
  if (name.includes('paris fashion week') || name.includes('mad cool')) {
    return '/media/IMAGESEVENTLY/concert.jpg'
  }
  
  if (name.includes('design week')) {
    return '/media/IMAGESEVENTLY/openai.png'
  }
  
  if (name.includes('berlin festival of lights')) {
    return '/media/IMAGESEVENTLY/lantern.jpg'
  }
  
  // Fallback to event type mapping
  return eventImages[eventType] || eventImages['default']
}
