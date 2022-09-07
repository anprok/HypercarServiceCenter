def tracklist(**tracks):
    for band, albums in tracks.items():
        print(band)
        for album, track in albums.items():
            print(f"ALBUM: {album} TRACK: {track}")
