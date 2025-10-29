import sys
import wikipedia
import pyjokes
from datetime import datetime
import random
import urllib.parse
import os
import requests


def get_weather(city):
    """Get weather information for a city using Open-Meteo API (free, no key needed)"""
    try:
        # Get coordinates for the city
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}
        geo_response = requests.get(geo_url, params=geo_params, timeout=5)
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return f"I couldn't find weather data for {city}. Try another city."
        
        location = geo_data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        
        # Get weather data
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,weather_code,wind_speed_10m",
            "temperature_unit": "fahrenheit"
        }
        weather_response = requests.get(weather_url, params=weather_params, timeout=5)
        weather_data = weather_response.json()
        
        current = weather_data["current"]
        temp = current["temperature_2m"]
        wind = current["wind_speed_10m"]
        
        weather_codes = {
            0: "Clear sky ☀️",
            1: "Mainly clear 🌤️",
            2: "Partly cloudy ⛅",
            3: "Overcast ☁️",
            45: "Foggy 🌫️",
            48: "Foggy 🌫️",
            51: "Light drizzle 🌧️",
            61: "Slight rain 🌧️",
            80: "Moderate rain 🌧️",
            95: "Thunderstorm ⛈️"
        }
        
        weather_desc = weather_codes.get(current["weather_code"], "Unknown")
        
        return f"🌍 Weather in {location['name']}, {location.get('country', '')}:\n\n🌡️ Temperature: {temp}°F\n💨 Wind Speed: {wind} km/h\n{weather_desc}"
    
    except Exception as e:
        return f"I couldn't fetch weather data right now. Try again later."

def get_random_quote():
    """Get a random inspirational quote"""
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Innovation distinguishes between a leader and a follower. - Steve Jobs",
        "Life is what happens when you're busy making other plans. - John Lennon",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "It is during our darkest moments that we must focus to see the light. - Aristotle",
        "The only impossible journey is the one you never begin. - Tony Robbins",
        "Success is not final, failure is not fatal. - Winston Churchill",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
        "Your time is limited, don't waste it living someone else's life. - Steve Jobs"
    ]
    return random.choice(quotes)

def get_trivia():
    """Get a random fun trivia fact"""
    trivia_facts = [
        "🧠 Did you know? Honey never spoils. Archaeologists have found 3,000-year-old honey in Egyptian tombs that was still edible!",
        "🐙 Did you know? Octopuses have three hearts - two pump blood to the gills, one pumps it to the rest of the body.",
        "🌍 Did you know? A day on Venus is longer than a year on Venus!",
        "🦁 Did you know? A lion's roar can be heard from 5 miles away.",
        "🧬 Did you know? Your body contains about 37.2 trillion cells.",
        "🌳 Did you know? Trees can communicate with each other through an underground network called the 'Wood Wide Web'.",
        "🐠 Did you know? Goldfish have a memory span of about 3 seconds.",
        "⚡ Did you know? Lightning is about 5 times hotter than the surface of the sun.",
        "🦋 Did you know? Butterflies taste with their feet.",
        "🧊 Did you know? Antarctica is the largest desert in the world."
    ]
    return random.choice(trivia_facts)

def calculate(expression):
    """Simple calculator for basic math"""
    try:
        # Only allow safe operations
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return "I can only do basic math operations. Try something like '2 + 2' or '10 * 5'."
        
        result = eval(expression)
        return f"🧮 {expression} = {result}"
    except:
        return "I couldn't calculate that. Try a simpler expression like '2 + 2'."

def search_spotify(song_name):
    """Generate a Spotify search link for the song"""
    encoded_song = urllib.parse.quote(song_name)
    return f"🎵 Search on Spotify: https://open.spotify.com/search/{encoded_song}"

def search_youtube(song_name):
    """Generate a YouTube search link for the song"""
    encoded_song = urllib.parse.quote(song_name)
    return f"🎬 Search on YouTube: https://www.youtube.com/results?search_query={encoded_song}"

def search_music(song_name):
    """Generate direct playable links for the song"""
    try:
        # Try Last.fm API to get song info
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "track.search",
            "track": song_name,
            "api_key": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
            "format": "json",
            "limit": 1
        }
        
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        encoded_song = urllib.parse.quote(song_name)
        spotify_url = f"https://open.spotify.com/search/{encoded_song}"
        youtube_url = f"https://www.youtube.com/results?search_query={encoded_song}"
        
        return f"🎵 Playing '{song_name}':\n\n🎧 Spotify: {spotify_url}\n🎬 YouTube: {youtube_url}"
    
    except Exception as e:
        # Fallback to simple links
        encoded_song = urllib.parse.quote(song_name)
        spotify_url = f"https://open.spotify.com/search/{encoded_song}"
        youtube_url = f"https://www.youtube.com/results?search_query={encoded_song}"
        return f"🎵 Playing '{song_name}':\n\n🎧 Spotify: {spotify_url}\n🎬 YouTube: {youtube_url}"

def search_person_info(person_name):
    """Search for person information using multiple sources for better accuracy"""
    try:
        # First try Wikipedia with better error handling
        try:
            # Search for the person first to get the most relevant result
            search_results = wikipedia.search(person_name, results=1)
            if search_results:
                info = wikipedia.summary(search_results[0], sentences=3)
                return info
            else:
                return f"I couldn't find information about {person_name}. Try being more specific."
        except wikipedia.exceptions.DisambiguationError as e:
            # If disambiguation error, try the first option
            if e.options:
                try:
                    info = wikipedia.summary(e.options[0], sentences=2)
                    return info
                except:
                    options = ', '.join(e.options[:3])
                    return f"Multiple results found. Did you mean: {options}?"
            return f"Multiple results found for {person_name}. Please be more specific."
        except wikipedia.exceptions.PageError:
            return f"I couldn't find a Wikipedia page for {person_name}. Try another search term."
        except Exception as e:
            return f"Error retrieving information: {str(e)}"
    except Exception as e:
        return f"I couldn't fetch information right now. Try again later."

def process_command(command):
    """Process a single command and return the response"""
    command = command.lower().strip()
    
    # Remove 'iris' or 'alexa' prefix if present
    if command.startswith('iris '):
        command = command.replace('iris ', '', 1).strip()
    if command.startswith('alexa '):
        command = command.replace('alexa ', '', 1).strip()
    
    try:
        if 'weather' in command:
            city = command.replace('weather', '').replace('in', '').replace('for', '').strip()
            if city:
                return get_weather(city)
            else:
                return "Please specify a city. Try 'weather in New York' or 'weather for London'."
        
        elif 'quote' in command or 'inspire' in command or 'motivation' in command:
            return get_random_quote()
        
        elif 'trivia' in command or 'fun fact' in command or 'did you know' in command:
            return get_trivia()
        
        elif any(op in command for op in ['+', '-', '*', '/', '=']):
            # Simple calculator
            expression = command.replace('calculate', '').replace('what is', '').strip()
            if expression:
                return calculate(expression)
        
        elif 'play' in command:
            song = command.replace('play', '').strip()
            if song:
                return search_music(song)
            else:
                return "Please specify a song to play"
        
        elif 'who is' in command or 'tell me about' in command:
            person = command.replace('who is', '').replace('tell me about', '').strip()
            if person:
                return search_person_info(person)
            else:
                return "Please specify who you want to know about"
        
        elif 'joke' in command or 'tell me a joke' in command:
            try:
                return pyjokes.get_joke()
            except Exception as e:
                return "I couldn't fetch a joke right now. Try again later."
        
        elif 'time' in command or 'what time' in command:
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}"
        
        elif 'date' in command or 'what date' in command or 'today' in command:
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current_date}"
        
        elif 'hello' in command or 'hi' in command or 'hey' in command:
            greetings = [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Hey! What's on your mind?",
                "Greetings! How may I assist you?"
            ]
            return random.choice(greetings)
        
        elif 'how are you' in command:
            responses = [
                "I'm doing great, thanks for asking! How about you?",
                "I'm functioning perfectly! Ready to help you.",
                "All systems operational! What can I do for you?"
            ]
            return random.choice(responses)
        
        elif 'your name' in command or 'who are you' in command:
            return "I'm Iris, your personal AI assistant. I'm here to help you with information, music, jokes, weather, and more!"
        
        elif 'help' in command or 'what can you do' in command:
            return """I can help you with:
- Play music: 'play [song name]'
- Get weather: 'weather in [city]'
- Get quotes: 'give me a quote' or 'inspire me'
- Fun facts: 'tell me a trivia' or 'fun fact'
- Calculator: 'what is 2 + 2' or '10 * 5'
- Get information: 'who is [person]' or 'tell me about [topic]'
- Tell jokes: 'tell me a joke'
- Check time: 'what time is it'
- Check date: 'what's today's date'
- And more! Just ask me anything."""
        
        elif 'shutdown' in command or 'exit' in command or 'quit' in command:
            return "Shutting down. Goodbye!"
        
        else:
            return "I'm not sure I understand that command. Try 'help' to see what I can do."
    
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_command = " ".join(sys.argv[1:])
        response = process_command(user_command)
        print(response)
    else:
        print("No command provided")
