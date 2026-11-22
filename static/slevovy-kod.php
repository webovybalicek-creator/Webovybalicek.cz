<?php
// Slevový kód na pluginy Toret: návštěvník vyplní e-mail, pošleme mu stylový e-mail s kódem
// a nám přijde oznámení (seznam zájemců = tyto e-maily). Volá assets/js/main.js přes fetch, vrací JSON.
header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');
function out($code, $data) { http_response_code($code); echo json_encode($data, JSON_UNESCAPED_UNICODE); exit; }
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') out(405, ['ok' => false]);

$f = fn($k, $max = 200) => trim(mb_substr((string)($_POST[$k] ?? ''), 0, $max));
if ($f('web') !== '' || (int)$f('t') < 3000) out(200, ['ok' => true]); // spam: skryté pole / příliš rychle
$email = $f('email');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) out(422, ['ok' => false, 'error' => 'email']);

$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
$lock = sys_get_temp_dir() . '/wb_sleva_' . md5($ip);
if (is_file($lock) && time() - filemtime($lock) < 20) out(429, ['ok' => false, 'error' => 'rate']);
@touch($lock);

$CODE = '15webovybalicek';
$shop = 'https://toret.cz/ref/67/';
$from = 'noreply@webovybalicek.cz';
$enc = fn($s) => '=?UTF-8?B?' . base64_encode($s) . '?=';

$html = <<<HTML
<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Váš slevový kód</title></head>
<body style="margin:0;padding:0;background:#f0f0f0;">
<div style="display:none;max-height:0;overflow:hidden;">Kód $CODE vám dá 15 % slevu na pluginy Toret.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f0f0f0;"><tr><td align="center" style="padding:32px 16px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#ffffff;border-radius:24px;overflow:hidden;font-family:Arial,Helvetica,sans-serif;color:#0a1217;">
  <tr><td style="background:#0a1217;padding:28px 36px;">
    <span style="font-size:22px;font-weight:bold;letter-spacing:-0.5px;color:#ffffff;">webovybalicek</span>
  </td></tr>
  <tr><td style="padding:36px 36px 8px;">
    <p style="margin:0 0 10px;font:12px/1.4 'Courier New',monospace;letter-spacing:1px;text-transform:uppercase;color:#7b8084;">Pluginy Toret pro WooCommerce</p>
    <h1 style="margin:0 0 16px;font-size:30px;line-height:1.15;letter-spacing:-0.8px;">Tady je váš slevový kód <span style="background:#cdfe00;padding:0 6px;border-radius:6px;">−15 %</span></h1>
    <p style="margin:0;font-size:16px;line-height:1.6;color:#54595d;">Díky za zájem. Kód zadejte v košíku na toret.cz a sleva 15&nbsp;% se vám odečte z nákupu pluginů.</p>
  </td></tr>
  <tr><td style="padding:24px 36px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#0a1217;border-radius:16px;"><tr><td align="center" style="padding:26px 16px;">
      <p style="margin:0 0 8px;font:12px/1.4 'Courier New',monospace;letter-spacing:1px;text-transform:uppercase;color:#9aa0a4;">Slevový kód</p>
      <p style="margin:0;font:bold 30px/1.2 'Courier New',monospace;letter-spacing:1px;color:#cdfe00;">$CODE</p>
    </td></tr></table>
  </td></tr>
  <tr><td style="padding:0 36px 12px;">
    <table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="background:#cdfe00;border-radius:999px;">
      <a href="$shop" style="display:inline-block;padding:15px 28px;font-size:16px;font-weight:bold;color:#0a1217;text-decoration:none;">Vybrat pluginy na toret.cz &rarr;</a>
    </td></tr></table>
  </td></tr>
  <tr><td style="padding:20px 36px 32px;">
    <p style="margin:0;font-size:15px;line-height:1.6;color:#54595d;">Nevíte, který plugin se vám hodí, nebo ho chcete nainstalovat a nastavit? Odpovězte na tento e-mail nebo zavolejte na <a href="tel:+420723933774" style="color:#0a1217;">723 933 774</a>. Rádi poradíme.</p>
  </td></tr>
  <tr><td style="padding:20px 36px;border-top:1px solid #e6e7e8;font-size:13px;line-height:1.5;color:#7b8084;">
    webovybalicek · tvorba webů a e-shopů · <a href="https://webovybalicek.cz/doporucene-pluginy/" style="color:#7b8084;">webovybalicek.cz</a><br>
    Tento e-mail jste dostali, protože jste si o slevový kód požádali na našem webu.
  </td></tr>
</table>
</td></tr></table>
</body></html>
HTML;
$text = "Tady je váš slevový kód na pluginy Toret: $CODE\n\nKód zadejte v košíku na toret.cz a sleva 15 % se odečte z nákupu.\nPluginy: $shop\n\nPoradíme i s instalací: 723 933 774, webovybalicek@gmail.com\n\nwebovybalicek";

$b = 'wb' . bin2hex(random_bytes(8));
$body = "--$b\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($text))
      . "--$b\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($html)) . "--$b--";
$headers = implode("\r\n", [
  'From: ' . $enc('webovybalicek') . " <$from>",
  'Reply-To: webovybalicek@gmail.com',
  'MIME-Version: 1.0',
  "Content-Type: multipart/alternative; boundary=\"$b\"",
]);
$subject = $enc('Váš slevový kód 15 % na pluginy Toret');
$ok = @mail($email, $subject, $body, $headers, "-f$from");
if (!$ok) $ok = @mail($email, $subject, $body, $headers);

// oznámení nám = seznam zájemců
$nh = implode("\r\n", ['From: ' . $enc('Web webovybalicek') . " <$from>", "Reply-To: $email", 'MIME-Version: 1.0', 'Content-Type: text/plain; charset=UTF-8']);
@mail('webovybalicek@gmail.com', $enc('Slevový kód Toret – ' . $email), "Zájemce o slevový kód: $email\nOdesláno: " . date('j. n. Y H:i') . "\nKód odeslán: " . ($ok ? 'ano' : 'NE'), $nh, "-f$from");

out($ok ? 200 : 500, ['ok' => (bool)$ok]);
