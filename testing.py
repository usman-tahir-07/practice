import requests
import json
import wave
import base64

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

def generate_tts_rest_api():
    api_key = "AIzaSyBDzfm8YCmPzkZsZP09aoEyiMz_XMiUp0w"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Say cheerfully: Have a wonderful day!"
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": "Kore"
                    }
                }
            }
        }
    }
    
    try:
        print("Making REST API request...")
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✓ TTS generation successful")
            
            # Extract audio data
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    if len(parts) > 0 and 'inlineData' in parts[0]:
                        # The audio data is base64 encoded
                        audio_data_b64 = parts[0]['inlineData']['data']
                        audio_data = base64.b64decode(audio_data_b64)
                        
                        file_name = 'out_rest.wav'
                        wave_file(file_name, audio_data)
                        print(f"✓ Audio saved as {file_name}")
                        return True
            
            print("✗ Could not extract audio data from response")
            print(f"Response structure: {json.dumps(result, indent=2)[:500]}...")
            
        else:
            print(f"✗ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"✗ Error in REST API call: {e}")
        import traceback
        traceback.print_exc()
        
    return False

if __name__ == "__main__":
    generate_tts_rest_api()