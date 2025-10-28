-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 27 Okt 2025 pada 08.39
-- Versi server: 10.4.28-MariaDB
-- Versi PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sisfo`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_datapkl`
--

CREATE TABLE `tb_datapkl` (
  `id_pkl` int(11) NOT NULL,
  `nama_pkl` varchar(30) NOT NULL,
  `asal_pkl` varchar(50) NOT NULL,
  `jurusan_pkl` varchar(50) NOT NULL,
  `alamat_pkl` varchar(60) NOT NULL,
  `status_pkl` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tb_datapkl`
--

INSERT INTO `tb_datapkl` (`id_pkl`, `nama_pkl`, `asal_pkl`, `jurusan_pkl`, `alamat_pkl`, `status_pkl`) VALUES
(1, 'andi', 'unhas', '', '', ''),
(3, 'budi', 'unm', 'elektro', 'mess', ''),
(11, 'udin', 'ut', 'teknik', 'parepare', ''),
(12, 'admin', 'admin', '', '', ''),
(13, 'Rosalinda', 'SMKN 3 Parepare', 'TKJ', 'jl. Jendral Ahmad yani', 'aktif'),
(14, 'Shira Ulzoefia', 'SMKN 3 Parepare', 'TKJ', 'Jl. Wirabuana', 'aktif'),
(15, 'Nurul ikhsan bahri', 'SMKN 5 BARRU ', 'REKAYASA PERANGKAT LUNAK', 'LAWALLU', 'aktif'),
(16, 'MUHAMMAD AS\'AD', 'SMKN 5 BARRU ', 'REKAYASA PERANGKAT LUNAK', 'LAWALLU', 'aktif'),
(17, 'JUMADIL', 'SMKN 5 BARRU ', 'REKAYASA PERANGKAT LUNAK', 'SIDDO', 'aktif'),
(18, 'SYAHRIL', 'SMKN 5 BARRU ', 'REKAYASA PERANGKAT LUNAK', 'LAMPOKO', 'aktif'),
(19, 'RAHMAT TRIKALBU', 'SMKN 5 BARRU ', 'REKAYASA PERANGKAT LUNAK', 'BATURROBANGE', 'aktif'),
(20, 'AKIL', 'SMKN 5 BARRU ', 'REKAYASA PERANGKAT LUNAK', 'CALLACCU', 'aktif'),
(21, 'Achmad Bilal Haq', 'SMK Negeri 1 Parepare', 'Desain Komunikasi Visual (DKV)', 'JL. Sejahtera', 'aktif'),
(22, 'Muhammad Syahdad', 'SMKN 1 PAREPARE', 'Desain Komunikasi Visual [DKV]', 'JL REFORMASI KEC. BACUKIKI BARAT ', 'tidak aktif'),
(23, 'MUHAMMAD SYAHDAD ', 'SMKN1PAREPARE ', 'DESAIN KOMUNIKASI VISUAL ', 'JL REFORMASI KEC.BACUKIKI BARAT ', 'aktif'),
(24, 'rusia', 'rusia', 'rusia', 'rusia', 'tidak aktif'),
(25, 'Thoariq musaddik', 'Institut Teknologi Bacharuddin jusuf habibie', 'Ilmu komputer', 'Jln Pinisi cappa galung', 'aktif'),
(26, 'M. Fauzan Iskandar', 'Institut Teknologi B. J. Habibie', 'Ilmu Komputer', 'Graha D Naila Blok R5', 'aktif'),
(27, 'assalamu\'alaikum', 'assalamu\'alaikum', 'assalamu\'alaikum', 'assalamu\'alaikum', 'aktif');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `tb_datapkl`
--
ALTER TABLE `tb_datapkl`
  ADD PRIMARY KEY (`id_pkl`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `tb_datapkl`
--
ALTER TABLE `tb_datapkl`
  MODIFY `id_pkl` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
