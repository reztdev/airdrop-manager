import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = "airdrop_manager_secret_key"  # Digunakan untuk flash messages

# Konfigurasi database
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "airdrop_manager.db")

def get_db_connection():
    """Membuat koneksi ke database SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Memungkinkan akses kolom dengan nama
    return conn

def init_db():
    """Inisialisasi database dan buat tabel jika belum ada"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Buat tabel projects jika belum ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT,
            twitter_url TEXT,
            discord_url TEXT,
            faucet_url TEXT,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Cek apakah kolom twitter_url dan discord_url sudah ada, jika belum maka tambahkan
    try:
        cursor.execute("SELECT twitter_url FROM projects LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE projects ADD COLUMN twitter_url TEXT")
    
    try:
        cursor.execute("SELECT discord_url FROM projects LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE projects ADD COLUMN discord_url TEXT")

    try:
        cursor.execute("SELECT faucet_url FROM projects LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE projects ADD COLUMN faucet_url TEXT")
    
    conn.commit()
    conn.close()

# Inisialisasi database saat aplikasi dimulai
init_db()

@app.route('/')
def index():
    """Halaman utama yang menampilkan daftar project"""
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects ORDER BY date_added DESC').fetchall()
    conn.close()
    return render_template('index.html', projects=projects)

@app.route('/add', methods=['POST'])
def add_project():
    """Menambahkan project baru ke database"""
    name = request.form['name'].strip()
    url = request.form['url'].strip()
    description = request.form['description'].strip()
    twitter_url = request.form.get('twitter_url', '').strip()
    discord_url = request.form.get('discord_url', '').strip()
    faucet_url = request.form.get('faucet_url', '').strip()
    
    # Validasi input
    if not name or not url:
        flash('Nama project dan URL harus diisi!', 'error')
        return redirect(url_for('index'))
    
    # Validasi dan koreksi URL
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://' + url
    
    # Validasi dan koreksi Twitter URL
    if twitter_url and not (twitter_url.startswith('http://') or twitter_url.startswith('https://')):
        twitter_url = 'https://' + twitter_url
    
    # Validasi dan koreksi Discord URL
    if discord_url and not (discord_url.startswith('http://') or discord_url.startswith('https://')):
        discord_url = 'https://' + discord_url

    if faucet_url and not (faucet_url.startswith('http://') or faucet_url.startswith('https://')):
        faucet_url = 'https://' + faucet_url
    
    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO projects (name, url, description, twitter_url, discord_url, faucet_url) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, url, description, twitter_url, discord_url, faucet_url))
        conn.commit()
        conn.close()
        
        flash('Project berhasil ditambahkan!', 'success')
    except sqlite3.Error as e:
        flash(f'Error: {e}', 'error')
    
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    """Mengedit project yang ada"""
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM projects WHERE id = ?', (id,)).fetchone()
    
    if not project:
        flash('Project tidak ditemukan!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name'].strip()
        url = request.form['url'].strip()
        description = request.form['description'].strip()
        twitter_url = request.form.get('twitter_url', '').strip()
        discord_url = request.form.get('discord_url', '').strip()
        faucet_url = request.form.get('faucet_url', '').strip()
        
        # Validasi input
        if not name or not url:
            flash('Nama project dan URL harus diisi!', 'error')
            return redirect(url_for('index'))
        
        # Validasi dan koreksi URL
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
        
        # Validasi dan koreksi Twitter URL
        if twitter_url and not (twitter_url.startswith('http://') or twitter_url.startswith('https://')):
            twitter_url = 'https://' + twitter_url
        
        # Validasi dan koreksi Discord URL
        if discord_url and not (discord_url.startswith('http://') or discord_url.startswith('https://')):
            discord_url = 'https://' + discord_url

        if faucet_url and not (faucet_url.startswith('http://') or faucet_url.startswith('https://')):
            faucet_url = 'https://' + faucet_url
        
        try:
            conn.execute('''
                UPDATE projects 
                SET name = ?, url = ?, description = ?, twitter_url = ?, discord_url = ?, faucet_url = ?
                WHERE id = ?
            ''', (name, url, description, twitter_url, discord_url, faucet_url, id))
            conn.commit()
            
            flash('Project berhasil diperbarui!', 'success')
        except sqlite3.Error as e:
            flash(f'Error: {e}', 'error')
    
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_project(id):
    """Menghapus project dari database"""
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM projects WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        flash('Project berhasil dihapus!', 'success')
    except sqlite3.Error as e:
        flash(f'Error: {e}', 'error')
    
    return redirect(url_for('index'))

@app.route('/open/<int:id>')
def open_url(id):
    """Redirect ke URL project (untuk membuka di tab baru)"""
    conn = get_db_connection()
    project = conn.execute('SELECT url FROM projects WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if project:
        return redirect(project['url'])
    else:
        flash('Project tidak ditemukan!', 'error')
        return redirect(url_for('index'))

@app.route('/open/twitter/<int:id>')
def open_twitter(id):
    """Redirect ke URL Twitter (untuk membuka di tab baru)"""
    conn = get_db_connection()
    project = conn.execute('SELECT twitter_url FROM projects WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if project and project['twitter_url']:
        return redirect(project['twitter_url'])
    else:
        flash('URL Twitter tidak ditemukan!', 'error')
        return redirect(url_for('index'))

@app.route('/open/discord/<int:id>')
def open_discord(id):
    """Redirect ke URL Discord (untuk membuka di tab baru)"""
    conn = get_db_connection()
    project = conn.execute('SELECT discord_url FROM projects WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if project and project['discord_url']:
        return redirect(project['discord_url'])
    else:
        flash('URL Discord tidak ditemukan!', 'error')
        return redirect(url_for('index'))

@app.route('/open/faucet/<int:id>')
def open_faucet(id):
    """Redirect ke URL Faucet (untuk membuka di tab baru)"""
    conn = get_db_connection()
    project = conn.execute('SELECT faucet_url FROM projects WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if project and project['faucet_url']:
        return redirect(project['faucet_url'])
    else:
        flash('URL faucet tidak ditemukan!', 'error')
        return redirect(url_for('index'))

@app.route('/get_all_urls')
def get_all_urls():
    conn = get_db_connection()
    projects = conn.execute('SELECT id, name, url FROM projects').fetchall()
    conn.close()
    
    urls = [{'id': row['id'], 'name': row['name'], 'url': row['url']} for row in projects]
    return jsonify(urls)

if __name__ == '__main__':
    app.run(debug=True)
