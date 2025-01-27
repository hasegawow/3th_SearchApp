import requests
from decouple import config
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy


# def get_spotify_client():
#     client_credentials = SpotifyClientCredentials(
#         client_id= config("CLIENT_ID"),
#         client_secret= config("CLIENT_SECRET")
#     )
#     sp = spotipy.Spotify(auth_manager=client_credentials)
#     return sp

# sp = get_spotify_client()

# results = sp.search(q="artist:鈴木雅之", type="artist", limit=1, market="JP")

# for artist in results['artists']['items']:
#     print(f"Name: {artist['name']}")
#     print(f"Popularity: {artist['popularity']}")
#     print(f"Followers: {artist['followers']['total']}")

# def search_artist(artist_name):
#     results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1, market="JP")

#     if results["artists"]["items"]:
#         for artist in results["artists"]["items"]:
#             print(f"アーティスト名: {artist['name']}")
#             print(f"フォロワー: {artist['followers']['total']}")
#             print(f"人気度: {artist['popularity']}")
#     else:
#         print("アーティストが見つかりませんでした。")

# search_artist("宇多田ヒカル")



import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotifyクライアントを設定
def get_token():
    client_credentials = SpotifyClientCredentials(
        client_id= config("CLIENT_ID"),
        client_secret= config("CLIENT_SECRET")
    )
    sp = spotipy.Spotify(auth_manager=client_credentials)
    return sp

# アーティスト情報を検索
def search_artist(artist_name):
    sp = get_token()
    results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)

    # 検索結果があるか確認
    if results["artists"]["items"]:
        artist = results["artists"]["items"][0]  # 最初のアーティスト情報を取得
        return {
            "name": artist["name"],
            "id": artist["id"],
            "followers": artist["followers"]["total"],
            "popularity": artist["popularity"],
            "genres": artist["genres"],
        }
    else:
        return None

# アーティストのトップトラックを取得
def get_artist_top_tracks(artist_id):
    sp = get_token()
    results = sp.artist_top_tracks(artist_id, country="JP")  # 日本のトップトラック
    tracks = []

    for track in results["tracks"]:
        tracks.append({
            "name": track["name"],
            "preview_url": track["preview_url"],  # 試聴用URL
            "album": track["album"]["name"],
        })
    return tracks

# メイン処理
if __name__ == "__main__":
    artist_name = input("アーティスト名を入力してください: ")

    # アーティスト情報を取得
    artist_info = search_artist(artist_name)

    if artist_info:
        print(f"アーティスト名: {artist_info['name']}")
        print(f"フォロワー数: {artist_info['followers']}")
        print(f"人気度: {artist_info['popularity']}")
        print(f"ジャンル: {', '.join(artist_info['genres'])}")

        # トップトラックを取得
        top_tracks = get_artist_top_tracks(artist_info["id"])
        print("\nトップトラック:")
        for i, track in enumerate(top_tracks, 1):
            print(f"{i}. {track['name']} (アルバム: {track['album']})")
            if track["preview_url"]:
                print(f"   試聴URL: {track['preview_url']}")
            else:
                print("   試聴URLなし")
    else:
        print("アーティストが見つかりませんでした。")