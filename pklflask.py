from flask import Flask, request, jsonify
from datetime import datetime, time
import pymysql
from flask_socketio import SocketIO
from flask_cors import CORS
from datetime import timedelta
import pytz
from collections import defaultdict



app = Flask(__name__)
app.secret_key = 'pkl_secret_anda_2025'

CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")

# Koneksi ke database MySQL
def get_db_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='',
                           database='sisfo',
                           cursorclass=pymysql.cursors.DictCursor)

# ✅ Route Registrasi Peserta PKL
@app.route('/register', methods=['POST'])
def register():
    print("📡 Headers:", request.headers)
    
    print("📡 Body:", request.get_data())
    data = request.get_json(force=True)
    if not data:
        return jsonify({'status': 'error', 'message': 'Format request harus JSON!'}), 400

    nama = data.get('nama_pkl')
    asal = data.get('asal_pkl')
    jurusan = data.get('jurusan_pkl')
    alamat = data.get('alamat_pkl')

    if not nama or not asal or not jurusan or not alamat:
        return jsonify({'status': 'error', 'message': 'Harap isi semua data!'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
                INSERT INTO tb_datapkl (nama_pkl, asal_pkl, jurusan_pkl, alamat_pkl, status_pkl)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nama, asal, jurusan, alamat, 'aktif'))
            conn.commit()
        return jsonify({'status': 'success', 'message': 'Pendaftaran berhasil!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Terjadi kesalahan: {e}'})
    finally:
        conn.close()

# ✅ Route Login Peserta PKL
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Format request harus JSON!'}), 400

    nama = data.get('nama_pkl')
    asal_sekolah = data.get('asal_pkl')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_datapkl WHERE nama_pkl = %s AND asal_pkl = %s", (nama, asal_sekolah))
    peserta = cursor.fetchone()

    

    conn.close()
    if peserta:
        role = 'admin' if peserta['nama_pkl'].lower() == 'admin' else 'user'
        return jsonify({'status': 'success', 'message': 'Login berhasil', 'role': role})
    else:
        return jsonify({'status': 'error', 'message': 'Nama atau asal sekolah tidak ditemukan!'})

# ✅ Route Absensi Masuk dan Pulang
@app.route('/absen', methods=['POST'])
def absen():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Format request harus JSON!'}), 400

    nama = data.get('nama_pkl')
    zona_wita = pytz.timezone('Asia/Makassar')
    waktu_sekarang = datetime.now(pytz.utc).astimezone(zona_wita)
    jam_sekarang = waktu_sekarang.time()
    tanggal_hari_ini = waktu_sekarang.strftime('%Y-%m-%d')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_datapkl WHERE nama_pkl = %s", (nama,))
    peserta = cursor.fetchone()

    if not peserta:
        return jsonify({'status': 'error', 'message': 'Peserta PKL tidak ditemukan'})

    # Cek apakah peserta sudah mengajukan Izin atau Sakit hari ini
    cursor.execute("SELECT status FROM tb_absenpkl WHERE nama_pkl = %s AND DATE(tanggal) = %s", (nama, tanggal_hari_ini))
    hari_ini_record = cursor.fetchone()

    if hari_ini_record and hari_ini_record.get('status') and hari_ini_record['status'].lower() in ('izin', 'sakit'):
        # Khusus pesan ketika sudah mengajukan izin/sakit
        conn.close()
        return jsonify({'status': 'error', 'message': 'Tidak bisa absen: kamu sudah mengajukan Izin/Sakit hari ini.'}), 409

    cursor.execute("SELECT * FROM tb_absenpkl WHERE nama_pkl = %s AND jam_masuk IS NOT NULL AND tanggal = %s", (nama, tanggal_hari_ini))
    absen_masuk = cursor.fetchone()

    if data.get('masuk') and not absen_masuk:
        status = 'Hadir' if time(4, 0) <= jam_sekarang <= time(8, 0) else 'Terlambat'

        #status = 'Hadir' if '06:00' <= waktu_sekarang <= '08:30' else 'Terlambat'
        cursor.execute("INSERT INTO tb_absenpkl (nama_pkl, jam_masuk, status, tanggal) VALUES (%s, %s, %s, %s)",
                       (nama, waktu_sekarang, status, tanggal_hari_ini))
        conn.commit()
        # Cek peserta aktif lain
        cursor.execute("""
            SELECT nama_pkl FROM tb_datapkl
            WHERE status_pkl = 'aktif' 
        """)
        semua_peserta_aktif = cursor.fetchall()

        # Loop tanggal sebelum hari ini (misalnya 7 hari ke belakang)
        jumlah_hari_ke_belakang = 7  # atau sesuaikan
        for i in range(1, jumlah_hari_ke_belakang + 1):
            tanggal_terlewat = datetime.now(pytz.utc).astimezone(zona_wita) - timedelta(days=i)
            tanggal_str = tanggal_terlewat.strftime('%Y-%m-%d')
            hari = tanggal_terlewat.strftime('%A')

            status_otomatis = 'Libur' if hari in ['Saturday', 'Sunday'] else 'Absen'

            for peserta in semua_peserta_aktif:
                cursor.execute("""
                    SELECT 1 FROM tb_absenpkl
                    WHERE nama_pkl = %s AND tanggal = %s
                """, (peserta['nama_pkl'], tanggal_str))
                sudah_absen = cursor.fetchone()

                if not sudah_absen:
                    cursor.execute("""
                        INSERT INTO tb_absenpkl (nama_pkl, status, tanggal)
                        VALUES (%s, %s, %s)
                    """, (peserta['nama_pkl'], status_otomatis, tanggal_str))
        conn.commit()

        conn.close()
        return jsonify({'status': 'success', 'message': 'Absensi masuk berhasil', 'status_kehadiran': status})



    elif data.get('pulang') and absen_masuk:
        if time(16, 0) <= jam_sekarang <= time(18, 0):
            cursor.execute("UPDATE tb_absenpkl SET jam_pulang = %s WHERE nama_pkl = %s AND tanggal = %s",
                           (waktu_sekarang, nama, tanggal_hari_ini))
            conn.commit()
            conn.close()
            return jsonify({'status': 'success', 'message': 'Absensi pulang berhasil'})
        else:
            return jsonify({'status': 'error', 'message': 'Belum waktunya pulang'})

    return jsonify({'status': 'error', 'message': 'Format absensi tidak valid'})

@app.route('/izin', methods=['POST'])
def izin():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Format request harus JSON!'}), 400

    nama = data.get('nama_pkl')
    # Terima 'status' (recommended) atau fallback ke 'jenis' untuk kompatibilitas
    status = data.get('status')  # 'izin' atau 'sakit' - used only to determine status value
    keterangan = data.get('keterangan', '')

    if not nama or not status:
        return jsonify({'status': 'error', 'message': 'Data tidak lengkap!'}), 400

    zona_wita = pytz.timezone('Asia/Makassar')
    waktu_sekarang = datetime.now(pytz.utc).astimezone(zona_wita)
    tanggal_hari_ini = waktu_sekarang.strftime('%Y-%m-%d')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Cek apakah sudah ada record absensi hari ini
        cursor.execute("""
            SELECT * FROM tb_absenpkl 
            WHERE nama_pkl = %s AND DATE(tanggal) = %s
        """, (nama, tanggal_hari_ini))
        existing = cursor.fetchone()

        if existing:
            return jsonify({'status': 'error', 'message': 'Sudah melakukan absensi atau mengajukan Izin/Sakit hari ini!'}), 409

        # Insert absensi dengan status Izin/Sakit
        status_value = status.capitalize()
        cursor.execute("""
            INSERT INTO tb_absenpkl (nama_pkl, tanggal, status, keterangan, jam_masuk, jam_pulang)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nama, tanggal_hari_ini, status_value, keterangan, '-', '-'))

        conn.commit()
        return jsonify({'status': 'success', 'message': f'Berhasil mengajukan {status}!'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Terjadi kesalahan: {str(e)}'})
    finally:
        conn.close()


def format_jam(value):
    if not value:
        return None
    if isinstance(value, str):
        return value[-8:] if len(value) >= 8 else value
    return value.strftime('%H:%M:%S')
@app.route('/absensi/mingguan', methods=['POST'])

def absensi_mingguan():
    data = request.get_json()
    nama = data.get('nama_pkl')

    if not nama:
        return jsonify({'status': 'error', 'message': 'Nama PKL diperlukan'}), 400
    
    zona_wita = pytz.timezone('Asia/Makassar')
    now = datetime.now(pytz.utc).astimezone(zona_wita)
    

    start_of_week = now - timedelta(days=now.weekday())  # Senin minggu ini
    start_date = start_of_week.date()
    today = now.date()

    tujuh_hari = (datetime.now(pytz.utc)
                  .astimezone(pytz.timezone('Asia/Makassar')) - timedelta(days=6)).date()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE(tanggal) AS tanggal, status, jam_masuk, jam_pulang
        FROM tb_absenpkl
        WHERE nama_pkl = %s AND DATE(tanggal) BETWEEN %s AND %s
        ORDER BY tanggal ASC
    """, (nama, start_date, today))

    hasil = cursor.fetchall()
    # Buat kamus untuk pencocokan tanggal
    absensi_map = {row['tanggal']: row for row in hasil}

    hasil_dengan_dummy = []

    for i in range((today - start_date).days + 1):
        tanggal = start_date + timedelta(days=i)
        hari = tanggal.strftime('%A')
        nama_hari = {
            'Monday': 'Senin',
            'Tuesday': 'Selasa',
            'Wednesday': 'Rabu',
            'Thursday': 'Kamis',
            'Friday': 'Jumat',
            'Saturday': 'Sabtu',
            'Sunday': 'Minggu'
        }.get(hari, hari)

        if tanggal in absensi_map:
            baris = absensi_map[tanggal]
            jam_masuk = format_jam(baris['jam_masuk'])
            jam_pulang = format_jam(baris['jam_pulang'])


            hasil_dengan_dummy.append({
                'hari': nama_hari,
                'tanggal': str(tanggal),
                'status': baris['status'],
                'jam_masuk': jam_masuk,
                'jam_pulang': jam_pulang
            })
        else:
            hasil_dengan_dummy.append({
                'hari': nama_hari,
                'tanggal': str(tanggal),
                'status': 'Belum Absen',
                'jam_masuk': None,
                'jam_pulang': None
            })

    return jsonify({'status': 'success', 'data': hasil_dengan_dummy})

@app.route('/rekap', methods=['POST'])
def rekap_peserta():
    data = request.get_json()
    nama = data.get('nama_pkl')
    tanggal_mulai = data.get('dari')
    tanggal_sampai = data.get('sampai')

    cursor = get_db_connection().cursor()
    cursor.execute("""
        SELECT tanggal, status, jam_masuk, jam_pulang
        FROM tb_absenpkl
        WHERE nama_pkl = %s AND DATE(tanggal) BETWEEN %s AND %s
        ORDER BY tanggal ASC
    """, (nama, tanggal_mulai, tanggal_sampai))
    hasil = cursor.fetchall()

    cursor.execute("SELECT asal_pkl, jurusan_pkl FROM tb_datapkl WHERE nama_pkl = %s", (nama,))
    profil = cursor.fetchone()

    
    result = []
    nama_hari = {
        'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu',
        'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu', 'Sunday': 'Minggu'
    }

    hasil_bersih = []
    for r in hasil:
        tanggal_dt = r['tanggal']
        hari = nama_hari.get(tanggal_dt.strftime('%A'), '-')
        hasil_bersih.append({
            'tanggal': tanggal_dt.strftime('%Y-%m-%d'),
            'hari': hari,
            'status': r['status'],
            'jam_masuk': format_jam(r['jam_masuk']),
            'jam_pulang': format_jam(r['jam_pulang'])
        })

    #return jsonify({'status': 'success', 'data': result})
    return jsonify({
    'status': 'success',
    'data': hasil_bersih,
    'peserta': {
        'nama': nama,
        'asal': profil['asal_pkl'],
        'jurusan': profil['jurusan_pkl'],
        'dari': tanggal_mulai,
        'sampai': tanggal_sampai
            }
        })

@app.route('/daftar-peserta', methods=['GET'])
def daftar_peserta():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nama_pkl FROM tb_datapkl WHERE status_pkl = 'aktif'")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/', methods=['GET'])
def home():
    return '🟢 Server Absensi PKL Aktif!'

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)