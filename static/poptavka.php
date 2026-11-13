<?php
// Odeslání poptávky z formuláře na webu (volá assets/js/main.js přes fetch, vrací JSON).
header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');

function out($code, $data) { http_response_code($code); echo json_encode($data, JSON_UNESCAPED_UNICODE); exit; }

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') out(405, ['ok' => false, 'error' => 'method']);

$f = fn($k, $max = 200) => trim(mb_substr((string)($_POST[$k] ?? ''), 0, $max));
// ochrana proti spamu: skryté pole musí zůstat prázdné a formulář se nesmí odeslat dřív než za 3 s
if ($f('web') !== '' || (int)$f('t') < 3000) out(200, ['ok' => true]);

$email = $f('email');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) out(422, ['ok' => false, 'error' => 'email']);

// jednoduchý limit: jedna poptávka za 30 s z jedné IP
$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
$lock = sys_get_temp_dir() . '/wb_poptavka_' . md5($ip);
if (is_file($lock) && time() - filemtime($lock) < 30) out(429, ['ok' => false, 'error' => 'rate']);
@touch($lock);

$types = ['' => 'Nevím, poraďte mi', 'ai' => 'AI web', 'wordpress' => 'Web na WordPressu', 'eshop' => 'E-shop', 'hybrid' => 'Hybridní web', 'sprava' => 'Správa stávajícího webu'];
$name = preg_replace('/[\r\n]+/', ' ', $f('name', 120));
$phone = preg_replace('/[\r\n]+/', ' ', $f('phone', 40));
$type = $types[$f('type', 20)] ?? 'Neuvedeno';
$msg = $f('message', 5000);
$urgent = $f('urgent') !== '' ? 'ANO' : 'ne';
$page = $f('page', 200);

$body = "Nová poptávka z webu\n\n"
  . "Jméno: $name\nE-mail: $email\nTelefon: $phone\nCo potřebuje: $type\nSpěchá: $urgent\n\n"
  . "Zpráva:\n$msg\n\n---\nOdesláno ze stránky: $page\n" . date('j. n. Y H:i');

$to = 'webovybalicek@gmail.com';
$subject = '=?UTF-8?B?' . base64_encode('Poptávka webu – ' . ($name !== '' ? $name : $email)) . '?=';
$from = 'noreply@webovybalicek.cz';
$headers = implode("\r\n", [
  'From: =?UTF-8?B?' . base64_encode('Web Webový balíček') . "?= <$from>",
  "Reply-To: $email",
  'MIME-Version: 1.0',
  'Content-Type: text/plain; charset=UTF-8',
  'Content-Transfer-Encoding: 8bit',
]);

$ok = @mail($to, $subject, $body, $headers, "-f$from");
if (!$ok) $ok = @mail($to, $subject, $body, $headers);
out($ok ? 200 : 500, ['ok' => (bool)$ok]);
