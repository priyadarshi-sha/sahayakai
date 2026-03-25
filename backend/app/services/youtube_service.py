from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from app.core.config import YOUTUBE_API_KEY
import re





def is_relevant(title: str, description: str) -> bool:
    text = f"{title} {description}".lower()

    

    
    return True


def find_timestamps_from_transcript(video_id: str, keywords):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(f"Error fetching transcript for {video_id}: {str(e)}")
        return []

    timestamps = []

    for entry in transcript:
        try:
            line = entry["text"].lower()
            if any(k in line for k in keywords):
                t = int(entry["start"])
                timestamps.append(f"{t // 60}:{t % 60:02d}")
        except Exception as e:
            print(f"Error processing transcript entry: {str(e)}")
            continue

    return list(dict.fromkeys(timestamps))[:5]


def get_youtube_videos(question: str):
    try:
        if not YOUTUBE_API_KEY:
            print("Warning: YOUTUBE_API_KEY not configured")
            return []

        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

        # SPPU university restriction
        search_query = f"{question}"

        search_response = youtube.search().list(
            q=search_query,
            part="snippet",
            maxResults=10,
            type="video",
            relevanceLanguage="en"
        ).execute()

        keywords = [k.lower() for k in question.split() if len(k) > 3]
        results = []

        for item in search_response.get("items", []):
            try:
                video_id = item["id"]["videoId"]
                title = item["snippet"]["title"]

                details = youtube.videos().list(
                    part="snippet",
                    id=video_id
                ).execute()

                snippet = details["items"][0]["snippet"]
                description = snippet.get("description", "")

                if not is_relevant(title, description):
                    continue

                timestamps = find_timestamps_from_transcript(video_id, keywords)

                results.append({
                    "title": title,
                    "videoId": video_id,
                    "timestamps": timestamps
                })

                if len(results) == 3:
                    break
            except Exception as e:
                print(f"Error processing video: {str(e)}")
                continue

        return results
    
    except Exception as e:
        print(f"Error in get_youtube_videos: {str(e)}")
        return []
