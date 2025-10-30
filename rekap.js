document.addEventListener("DOMContentLoaded", function () {
    // Initialize Bootstrap Modal
    const editModal = new bootstrap.Modal(document.getElementById('editStatusModal'));
    
    // Handle Edit Status Button Click
    document.getElementById('btnSimpanStatus').addEventListener('click', function() {
        const tanggal = document.getElementById('editTanggal').value;
        const nama = document.getElementById('editNama').value;
        const status = document.getElementById('editStatus').value;
        const keterangan = document.getElementById('editKeterangan').value;

        fetch("http://127.0.0.1:5000/update-status", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                nama_pkl: nama,
                tanggal: tanggal,
                status: status,
                keterangan: keterangan
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                editModal.hide();
                // Refresh the table
                document.getElementById("filterForm").dispatchEvent(new Event('submit'));
            } else {
                alert(data.message);
            }
        });
    });
    const namaSelect = document.getElementById("nama");
  
    // Fetch nama peserta untuk dropdown
    fetch("http://127.0.0.1:5000/daftar-peserta")
      .then(res => res.json())
      .then(data => {
        data.forEach(p => {
          const opt = document.createElement("option");
          opt.value = p.nama_pkl;
          opt.textContent = p.nama_pkl;
          namaSelect.appendChild(opt);
        });
      });
  
    document.getElementById("filterForm").addEventListener("submit", function (e) {
      e.preventDefault();
  
      const nama = namaSelect.value;
      const mulai = document.getElementById("tanggalMulai").value;
      const sampai = document.getElementById("tanggalSampai").value;
  
      fetch("http://127.0.0.1:5000/rekap", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nama_pkl: nama, dari: mulai, sampai: sampai })
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === "success") {
            const p = data.peserta;
            document.getElementById("infoPeserta").style.display = "block";
            document.getElementById("infoNama").textContent = p.nama;
            document.getElementById("infoAsal").textContent = p.asal;
            document.getElementById("infoJurusan").textContent = p.jurusan;
            document.getElementById("infoTanggal").textContent = `${p.dari} s/d ${p.sampai}`;
          const tbody = document.querySelector("#tabelRekap tbody");
          tbody.innerHTML = "";
  
          let total = 0, hadir = 0, terlambat = 0, absen = 0, izin = 0, sakit = 0;
  
          data.data.forEach(row => {
            const tr = document.createElement("tr");
            const status = row.status ? row.status.trim().toLowerCase() : "";

            if (status === "libur") {
                tr.classList.add("baris-libur");
            }

            const canEdit = status === "izin" || status === "absen"; // Allow editing only for these statuses
            const editButton = canEdit ? `
              <button class="btn btn-sm btn-outline-primary edit-status" 
                data-tanggal="${row.tanggal}"
                data-nama="${nama}">
                Ubah Status
              </button>` : '-';

            tr.innerHTML = `
              <td>${row.tanggal}</td>
              <td>${row.hari}</td>
              <td>${row.jam_masuk || '-'}</td>
              <td>${row.jam_pulang || '-'}</td>
              <td>${row.status}</td>
              <td>${row.keterangan ? row.keterangan : '-'}</td>
              <td>${editButton}</td>
            `;
            tbody.appendChild(tr);

            // Add click handler for edit button
            const editBtn = tr.querySelector('.edit-status');
            if (editBtn) {
                editBtn.addEventListener('click', function() {
                    document.getElementById('editTanggal').value = this.dataset.tanggal;
                    document.getElementById('editNama').value = this.dataset.nama;
                    document.getElementById('editKeterangan').value = '';
                    editModal.show();
                });
            }
  
            total++;
            if (row.status === "hadir") hadir++;
            else if (row.status === "terlambat") terlambat++;
            else if (row.status === "absen") absen++;
            else if (row.status === "izin") izin++;
            else if (row.status === "sakit") sakit++;
          });
  
          document.getElementById("jumlahHariKerja").textContent = total;
          document.getElementById("jumlahHadir").textContent = hadir;
          document.getElementById("jumlahTerlambat").textContent = terlambat;
          document.getElementById("jumlahAbsen").textContent = absen;
          document.getElementById("jumlahIzin").textContent = izin;
          document.getElementById("jumlahSakit").textContent = sakit;
          document.getElementById("tanggalRekap").textContent = new Date().toLocaleDateString("id-ID");
  
          document.getElementById("hasilRekap").style.display = "block";
        }
      });
    });
  });