document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("formDaftar");
    const loginBtn = document.getElementById("loginBtn");
  
    // ✅ Registrasi Peserta PKL via AJAX
    if (registerForm) {
      registerForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const nama = document.querySelector("[name='nama_pkl']").value;
        const asal = document.querySelector("[name='asal_pkl']").value;
        const jurusan = document.querySelector("[name='jurusan_pkl']").value;
        const alamat = document.querySelector("[name='alamat_pkl']").value;
  
        fetch("http://10.2.1.200:5000/register", {
          method: "POST",
          headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            nama_pkl: nama,
            asal_pkl: asal,
            jurusan_pkl: jurusan,
            alamat_pkl: alamat
          })
        })
          .then(response => response.json())
          .then(data => {
            alert(data.message);
            if (data.status === "success") {
              registerForm.reset();
              toggleRegisterModal();
            }
          })
          .catch(error => console.error("Error:", error));
      });
    } else {
      console.warn("⚠️ registerForm tidak ditemukan di halaman ini.");
    }
  
    // ✅ Login via AJAX
    if (loginBtn) {
      loginBtn.addEventListener("click", function () {
        const nama = document.getElementById("nama").value;
        const asal = document.getElementById("asal_sekolah").value;
  
        fetch("http://10.2.1.200:5000/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ nama_pkl: nama, asal_pkl: asal })
        })
          .then(response => response.json())
          .then(data => {
            if (data.status === "success") {
              sessionStorage.setItem("nama", nama);
              if (data.role === "admin") {
                window.location.href = "rekap.html";
              } else {
                window.location.href = "absensi.html";
              }
          
            } else {
              const loginStatus = document.getElementById("login_status");
              if (loginStatus) {
                loginStatus.innerText = data.message;
              } else {
                console.warn("⚠️ login_status tidak ditemukan.");
              }
            }
          })
          .catch(error => console.error("Error:", error));
      });
    } else {
      console.warn("⚠️ loginBtn tidak ditemukan di halaman ini.");
    }
  });