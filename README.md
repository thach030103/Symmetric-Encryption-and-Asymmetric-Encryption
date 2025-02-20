# Symmetric-Encryption-and-Asymmetric-Encryption

<h3>Mã hóa đối xứng (Symmetric Encryption):</h3>
<ul>
  <li><strong>Mô tả:</strong> Cả mã hóa và giải mã đều sử dụng cùng một khóa.</li>
  <li><strong>Ưu điểm:</strong> Nhanh chóng, hiệu quả cho lượng dữ liệu lớn.</li>
  <li><strong>Nhược điểm:</strong> Cần có phương thức an toàn để chia sẻ khóa giữa các bên, nếu lộ khóa /cách mã hóa thì kẻ gian sẽ giải mã được.</li>
  <li><strong>Ví dụ:</strong> AES, DES, Blowfish.</li>
</ul>
<h3>Mã hóa bất đối xứng (Asymmetric Encryption):</h3>
<ul>
  <li><strong>Mô tả:</strong> Sử dụng một cặp khóa – khóa công khai (public key) và khóa riêng (private key). Khóa công khai để mã hóa và khóa riêng để giải mã, do đó khi lộ khóa (công khai) và cách mã hóa thì kẻ gian vẫn không thể giải mã được.</li>
  <li><strong>Ưu điểm:</strong> Bảo mật cao hơn vì không cần chia sẻ khóa riêng.</li>
  <li><strong>Nhược điểm:</strong> Chậm hơn mã hóa đối xứng.</li>
  <li><strong>Ví dụ:</strong> RSA, ECC (Elliptic Curve Cryptography).</li>
</ul>
<h3>Source code</h3>
<ul>
  <li>Mã đối xứng AFFINE</li>
  <li>Mã bất đối xứng RSA</li>
</ul>
