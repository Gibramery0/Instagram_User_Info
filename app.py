from flask import Flask, render_template, request, jsonify
from instaloader import Instaloader, Profile
import os
from dotenv import load_dotenv
import time
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
load_dotenv()

# Instagram giriş bilgileri
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

L = Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
    compress_json=False,
    max_connection_attempts=3
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    username = request.form.get('username')
    if not username:
        return jsonify({'error': 'Kullanıcı adı gerekli'}), 400
        
    try:
        print(f"Profil analizi başlatılıyor: {username}")
        
        # Instagram'ın rate limit'ini aşmamak için bekleme
        time.sleep(2)
        
        profile = Profile.from_username(L.context, username)
        print(f"Profil bulundu: {profile.username}")
        
        if profile.is_private:
            return jsonify({'error': 'Bu hesap gizli. Sadece gizli olmayan hesaplar analiz edilebilir.'}), 400
        
        # Profil bilgilerini topla
        profile_data = {
            'username': profile.username,
            'full_name': profile.full_name,
            'biography': profile.biography,
            'followers': profile.followers,
            'following': profile.followees,
            'posts': profile.mediacount,
            'profile_pic_url': profile.profile_pic_url,
            'is_private': profile.is_private
        }
        
        print(f"Temel profil bilgileri alındı: {json.dumps(profile_data, indent=2)}")
        
        return jsonify(profile_data)
    except Exception as e:
        print(f"Genel hata: {str(e)}")
        return jsonify({'error': 'Instagram verilerine erişilemiyor. Lütfen daha sonra tekrar deneyin.'}), 400

if __name__ == '__main__':
    app.run(debug=True) 