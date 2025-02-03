from django.shortcuts import render, redirect
from .models import Users2
from .spotify_utils.spotify import get_token, search_artist, get_artist_top_tracks
from urllib.parse import quote
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials,  SpotifyOAuth
from decouple import config


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        repassword = request.POST.get('repassword')

        if password == repassword:
            if not Users2.objects.filter(username=username).exists():
                user = Users2.objects.create(password=password, username=username, email=email)
                user.save()
                return redirect('search')
            else:
                error_message = "このユーザーネームはすでに使用されています、ボケが。"
                return render(request, 'signup.html', {'error_message': error_message})
        else:
            error_message = "パスワードが同じではありません。ボケが。"
            return render(request, 'signup.html', {'error_message': error_message})
    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Users2.objects.filter(username=username).exists() or Users2.objects.filter(email=username).exists():
            if Users2.objects.filter(password=password).exists():
                return redirect('search')
            else:
                error_message = "パスワードが違います"
                return render(request, 'login.html', {'error_message': error_message})
        else:
            error_message = "このユーザー名、メールアドレスは登録されていません。"
            return render(request, 'login.html', {'error_message': error_message})

    else:
        return render(request, 'login.html')

def artist_search(request):
    query = request.POST.get("query")  # ユーザーの検索キーワード
    results = []
    results_track = []
    resutls_album = []
    results_artist = []
    ranking_track = []

    if query:
        boolean = True
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=config("CLIENT_ID"),
            client_secret=config("CLIENT_SECRET")
            ))
        try:
            response = sp.search(q=query, type="artist,track,album", limit=50, market="JP")

            # アーティスト結果を追加
            for artist in response.get("artists", {}).get("items", []):
                results_artist.append({
                    "type": "artist",
                    "name": artist["name"],
                    "followers": artist["followers"]["total"],
                    "image": artist["images"][0]["url"] if artist["images"] else None
                })

            # トラック結果を追加
            for track in response.get("tracks", {}).get("items", []):
                    results_track.append({
                    "type": "track",
                    "name": track["name"],
                    "album": track["album"]["name"],
                    "artist": track["artists"][0]["name"],
                    "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None
                })

            # アルバム結果を追加
            for album in response.get("albums", {}).get("items", []):
                resutls_album.append({
                    "type": "album",
                    "name": album["name"],
                    "artist": album["artists"][0]["name"],
                    "image": album["images"][0]["url"] if album["images"] else None
                })

            # 検索結果が空の場合
            if not results:
                results = [{"message": "検索結果がありません。"}]

        except Exception as e:
            results = [{"error": f"エラーが発生しました: {str(e)}"}]
    else:
        boolean = False
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=config("CLIENT_ID"),
            client_secret=config("CLIENT_SECRET")
            ))

        playlist_id = "4Bsknjekv8HNfUF57ELNot"
        playlist = sp.playlist_tracks(playlist_id, market="JP")
        ranking_track = []

        for item in playlist['items']:
            track = item['track']

            duration_ms = track['duration_ms']
            minutes = duration_ms // 60000  # 分
            seconds = (duration_ms % 60000) // 1000  # 秒
            popularity = track['popularity']

            ranking_track.append({
                "type": "track",
                "name": track['name'],
                "artist": ', '.join(artist['name'] for artist in track['artists']),
                "image": track['album']['images'][0]['url'] if track['album']['images'] else None,
                "duration": f"{minutes}:{seconds}",
                "popularity": popularity
    })



    return render(request, "test2.html", {
        "results_track": results_track,
        "results_album": resutls_album,
        "results_artist": results_artist,
        "ranking_track": ranking_track,
        "request": query,
        "boolean": boolean
        })
def reset_search(request):

    return redirect('search')

