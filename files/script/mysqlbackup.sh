#!/bin/bash

MYSQL_ARGS="--defaults-extra-file=/etc/db_backup.cnf"
MYSQL="/usr/bin/mysql $MYSQL_ARGS "
MYSQLDUMP="/usr/bin/mysqldump $MYSQL_ARGS "

# Konfigurasi Dasar
BACKUP_DIR="/backup/mysql"
BACKUP_LOG="/backup/logs/mysql_backup_cron.log"
BACKUP_RETENTION_DAYS=30
EMAIL_ALERT="fahrudin.hariadi@gmail.com" # Ganti dengan email Anda
# Buat struktur direktori backup
mkdir -p "$BACKUP_DIR/databases"
mkdir -p "$BACKUP_DIR/logs"

# Tanggal untuk nama file backup
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
# Log file untuk mencatat proses backup
LOGFILE="$BACKUP_DIR/logs/backup_log_$(date +"%Y").log"

# Variabel untuk melacak status backup
BACKUP_FAILED=0
FAILED_DATABASES=""
SUCCESSFUL_DATABASES=""

# Fungsi logging
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOGFILE"
}

# Fungsi kirim email notifikasi
send_alert() {
    local SUBJECT="$1"
    local MESSAGE="$2"

    if [[ -n "$EMAIL_ALERT" ]]; then
        echo "$MESSAGE" | mail -s "$SUBJECT" "$EMAIL_ALERT"
    fi
}

# Fungsi validasi backup
validate_backup() {
    local BACKUP_FILE="$1"
    local DB_NAME="$2"

    # Periksa ukuran file
    if [ ! -s "$BACKUP_FILE" ]; then
        log "GAGAL: Backup $DB_NAME kosong" "ERROR"
        return 1
    fi

    # Coba unzip dan periksa integritas
    gzip -t "$BACKUP_FILE" 2>/dev/null
    if [ $? -ne 0 ]; then
        log "GAGAL: Backup $DB_NAME rusak" "ERROR"
        return 1
    fi

    return 0
}

# Fungsi backup database
backup_databases() {
    # Daftar database yang dikecualikan
    local EXCLUDED_DBS="mysql performance_schema information_schema phpmyadmin"

    # Dapatkan daftar semua database
    local DATABASES=$(MYSQL -BNe "SHOW DATABASES;" | grep -Ev "^(Database|${EXCLUDED_DBS// /|})")

    log "Memulai proses backup database"

    # Buat backup untuk setiap database
    for DB in $DATABASES; do
        # Buat nama file unik untuk setiap database
        local DB_BACKUP_DIR="$BACKUP_DIR/databases/$DB"
        mkdir -p "$DB_BACKUP_DIR"
        local BACKUP_FILE="$DB_BACKUP_DIR/$DB-$TIMESTAMP.sql.gz"

        log "Proses backup database: $DB"

        # Backup database dengan timeout dan penanganan error
        timeout 1h MYSQLDUMP \
            --single-transaction \
            --routines \
            --triggers \
            --databases "$DB" | gzip >"$BACKUP_FILE" 2>>"$LOGFILE"

        # Periksa status backup
        if [ $? -eq 0 ]; then
            # Validasi backup
            if validate_backup "$BACKUP_FILE" "$DB"; then
                log "Backup $DB berhasil"
                SUCCESSFUL_DATABASES+=" $DB"
            else
                log "Backup $DB gagal validasi"
                BACKUP_FAILED=$((BACKUP_FAILED + 1))
                FAILED_DATABASES+=" $DB"
                rm -f "$BACKUP_FILE"
            fi
        else
            log "Backup $DB gagal"
            BACKUP_FAILED=$((BACKUP_FAILED + 1))
            FAILED_DATABASES+=" $DB"
            rm -f "$BACKUP_FILE"
        fi
    done

    # Kirim alert jika ada backup yang gagal
    if [ $BACKUP_FAILED -gt 0 ]; then
        local ALERT_MESSAGE="Backup Gagal untuk Database:$FAILED_DATABASES\n
Backup Berhasil untuk Database:$SUCCESSFUL_DATABASES\n
Total Database Gagal: $BACKUP_FAILED\n
Lihat log lengkap di: $LOGFILE"

        log "PERINGATAN: $BACKUP_FAILED database gagal di-backup"
        send_alert "Backup MySQL Sebagian Gagal" "$ALERT_MESSAGE"
    else
        log "Semua database berhasil di-backup"
        send_alert "Backup MySQL Sukses" "Semua database berhasil di-backup"
    fi
}

# Fungsi hapus backup lama
cleanup_old_backups() {
    log "Menghapus backup yang lebih dari $BACKUP_RETENTION_DAYS hari"

    # Hapus file backup lama per database
    local DELETED_FILES=$(find "$BACKUP_DIR/databases" -name "*.sql.gz" -type f -mtime +$BACKUP_RETENTION_DAYS -delete -print | wc -l)

    # Hapus log backup lama
    find "$BACKUP_DIR/logs" -name "backup_log_*" -type f -mtime +$BACKUP_RETENTION_DAYS -delete

    log "Pembersihan backup lama selesai. $DELETED_FILES file dihapus"
}

# Fungsi kompresi backup lama (opsional)
compress_old_backups() {
    log "Memulai kompresi backup lama"

    # Cari file backup yang belum dikompresi
    find "$BACKUP_DIR/databases" -type f -name "*.sql" -mtime +7 | while read -r file; do
        if [ -f "$file" ]; then
            gzip "$file"
            log "Mengkompresi: $file"
        fi
    done

    log "Kompresi backup lama selesai"
}

# Fungsi utama
main() {
    log "Memulai proses backup database"

    # Reset variabel
    BACKUP_FAILED=0
    FAILED_DATABASES=""
    SUCCESSFUL_DATABASES=""

    # Jalankan backup
    backup_databases

    # Bersihkan backup lama
    cleanup_old_backups

    # Kompresi backup lama (opsional)
    # compress_old_backups

    log "Proses backup database selesai"

    # Kembalikan status untuk integrasi dengan sistem lain
    exit $BACKUP_FAILED
}

# Jalankan script
main
