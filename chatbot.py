import sys
import wikipedia
import pyjokes
from datetime import datetime
import random
import urllib.parse
import os
import requests


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

def process_command(command):
    """Process a single command and return the response"""
    command = command.lower().strip()
    
    # Remove 'iris' or 'alexa' prefix if present
    if command.startswith('iris '):
        command = command.replace('iris ', '', 1).strip()
    if command.startswith('alexa '):
        command = command.replace('alexa ', '', 1).strip()
    
    try:
        if 'play' in command:
            song = command.replace('play', '').strip()
            if song:
                return search_music(song)
            else:
                return "Please specify a song to play"
        
        elif 'who is' in command or 'tell me about' in command:
            person = command.replace('who is', '').replace('tell me about', '').strip()
            if person:
                try:
                    info = wikipedia.summary(person, sentences=2)
                    return info
                except wikipedia.exceptions.DisambiguationError as e:
                    options = ', '.join(e.options[:5])
                    return f"Multiple results found. Did you mean: {options}?"
                except wikipedia.exceptions.PageError:
                    return f"I couldn't find information about {person}. Try being more specific."
                except Exception as e:
                    return f"Error retrieving information: {str(e)}"
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
            return "I'm Iris, your personal AI assistant. I'm here to help you with information, music, jokes, and more!"
        
        elif 'help' in command or 'what can you do' in command:
            return """I can help you with:
- Play music: 'play [song name]'
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
