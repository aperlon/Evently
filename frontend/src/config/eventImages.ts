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

// Get image for event type
export const getEventImage = (eventType: string): string => {
  return eventImages[eventType] || eventImages['default']
}
