"""Music station satellites."""

from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import DelimitedResultParser, JSONResultParser
import json


# Play
music_play = Satellite(
    name="music_play",
    description="Start or resume music playback",
    category="music",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Music"
        activate
        play
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

# Pause
music_pause = Satellite(
    name="music_pause",
    description="Pause music playback",
    category="music",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Music"
        activate
        pause
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

# Next track
music_next = Satellite(
    name="music_next",
    description="Skip to next track",
    category="music",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Music"
        activate
        next track
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

# Previous track
music_previous = Satellite(
    name="music_previous",
    description="Go to previous track",
    category="music",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Music"
        activate
        previous track
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

# Get current track
music_get_current = Satellite(
    name="music_get_current",
    description="Get current track information",
    category="music",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Music"
        activate
        set currentTrack to current track
        if exists currentTrack then
            set trackName to name of currentTrack
            set trackArtist = artist of currentTrack
            set trackAlbum = album of currentTrack
            set trackDuration = duration of currentTrack
            set trackPosition = player position of currentTrack

            return trackName & "|" & trackArtist & "|" & trackAlbum & "|" & trackDuration & "|" & trackPosition
        else
            return "No track playing"
        end if
    end tell
    """,
    result_parser=lambda x: dict(zip(["name", "artist", "album", "duration", "position"], x.split("|", 4))) if "No track" not in x else {"status": "stopped"},
    examples=[
        {
            "input": {},
            "output": {
                "name": "Song Name",
                "artist": "Artist Name",
                "album": "Album Name",
                "duration": "3:45",
                "position": "0:45"
            }
        }
    ]
)

# Set volume
music_set_volume = Satellite(
    name="music_set_volume",
    description="Set Music app volume (0-100)",
    category="music",
    parameters=[
        SatelliteParameter(
            name="level",
            type="integer",
            description="Volume level (0-100)",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Music"
        activate
        set sound volume to {{ level }}
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {"level": 50},
            "output": "success"
        }
    ]
)

# Get volume
music_get_volume = Satellite(
    name="music_get_volume",
    description="Get Music app sound volume (0-100)",
    category="music",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Music"
        activate
        set soundVolume to sound volume
        return soundVolume as string
    end tell
    """,
    examples=[
        {
            "input": {},
            "output": {"volume": "50"}
        }
    ]
)

# Play specific track
music_play_track = Satellite(
    name="music_play_track",
    description="Play specific track by name",
    category="music",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Track name to play",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Music"
        activate
        try
            set targetTrack to first track whose name is "{{ name }}"
            play targetTrack
            return "success"
        on error errMsg
            return "Error: " & errMsg
        end try
    end tell
    """,
    examples=[
        {
            "input": {"name": "My Favorite Song"},
            "output": "success"
        }
    ]
)

# Search tracks
music_search = Satellite(
    name="music_search",
    description="Search for tracks by name",
    category="music",
    parameters=[
        SatelliteParameter(
            name="query",
            type="string",
            description="Search query",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Music"
        activate
        set trackList to {}
        set allTracks to every track

        repeat with currentTrack in allTracks
            set trackName to name of currentTrack
            if trackName contains "{{ query }}" then
                if (count of trackList) = 0 then
                    set end of trackList to (trackName & "|" & (album of currentTrack) & "|" & (artist of currentTrack))
                else
                    set end of trackList to "," & (trackName & "|" & (album of currentTrack) & "|" & (artist of currentTrack))
                end if
            end if
        end repeat
    end tell

    return trackList as string
    """,
    result_parser=lambda x: [dict(zip(["name", "album", "artist"], item.split("|", 2))) for item in x.split(",")] if x else [],
    examples=[
        {
            "input": {"query": "love"},
            "output": {
                "results": [
                    {"name": "Love Song", "album": "Album", "artist": "Artist"}
                ]
            }
        }
    ]
)

# Get playlists
music_get_playlists = Satellite(
    name="music_get_playlists",
    description="List all playlists",
    category="music",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Music"
        activate
        set playlistList = {}
        set allPlaylists = every playlist

        repeat with currentPlaylist in allPlaylists
            set playlistName = name of currentPlaylist
            set trackCount = count of tracks in currentPlaylist
            if (count of playlistList) = 0 then
                set end of playlistList to (playlistName & "|" & (trackCount as string))
            else
                set end of playlistList to "," & (playlistName & "|" & (trackCount as string))
            end if
        end repeat
    end tell

    return playlistList as string
    """,
    result_parser=lambda x: [dict(zip(["name", "count"], item.split("|"))) for item in x.split(",")] if x else [],
    examples=[
        {
            "input": {},
            "output": {
                "playlists": [
                    {"name": "Favorites", "count": "25"}
                ]
            }
        }
    ]
)

# Shuffle
music_shuffle = Satellite(
    name="music_shuffle",
    description="Shuffle current playlist",
    category="music",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Music"
        activate
        set shuffle enabled to true
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

# Export all music satellites
__all__ = [
    "music_play",
    "music_pause",
    "music_next",
    "music_previous",
    "music_get_current",
    "music_set_volume",
    "music_get_volume",
    "music_play_track",
    "music_search",
    "music_get_playlists",
    "music_shuffle",
]
