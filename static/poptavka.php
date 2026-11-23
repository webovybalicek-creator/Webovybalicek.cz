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

$types = ['' => 'Nevím, poraďte mi', 'ai' => 'AI web', 'wordpress' => 'Prezentační web', 'eshop' => 'E-shop', 'hybrid' => 'Hybridní web', 'sprava' => 'Správa stávajícího webu',
  'a-nevim' => 'Spolupráce: zatím neví, probrat', 'a-agentura' => 'Spolupráce: agentura, potřebuje postavit web', 'a-freelancer' => 'Spolupráce: freelancer, má klienta na web', 'a-sluzby' => 'Spolupráce: nabízí své služby (PPC, texty, grafika…)', 'a-vypomoc' => 'Spolupráce: dlouhodobá výpomoc s vývojem'];
$agency = $f('segment', 20) === 'agentura';
$name = preg_replace('/[\r\n]+/', ' ', $f('name', 120));
$phone = preg_replace('/[\r\n]+/', ' ', $f('phone', 40));
$type = $types[$f('type', 20)] ?? 'Neuvedeno';
$msg = $f('message', 5000);
$urgent = $f('urgent') !== '' ? 'ANO' : 'ne';
$page = $f('page', 200);

$body = ($agency ? "Nová poptávka SPOLUPRÁCE (agentura / freelancer)\n\n" : "Nová poptávka z webu\n\n")
  . "Jméno: $name\nE-mail: $email\nTelefon: $phone\nCo potřebuje: $type\nSpěchá: $urgent\n\n"
  . "Zpráva:\n$msg\n\n---\nOdesláno ze stránky: $page\n" . date('j. n. Y H:i');

$to = 'webovybalicek@gmail.com';
$subject = '=?UTF-8?B?' . base64_encode(($agency ? 'Spolupráce – ' : 'Poptávka webu – ') . ($name !== '' ? $name : $email)) . '?=';
$from = 'noreply@webovybalicek.cz';
$headers = implode("\r\n", [
  'From: =?UTF-8?B?' . base64_encode('Web webovybalicek') . "?= <$from>",
  "Reply-To: $email",
  'MIME-Version: 1.0',
  'Content-Type: text/plain; charset=UTF-8',
  'Content-Transfer-Encoding: 8bit',
]);

$ok = @mail($to, $subject, $body, $headers, "-f$from");
if (!$ok) $ok = @mail($to, $subject, $body, $headers);

// kopie do Slacku (webhook je v slack-config.php, generuje ho deploy ze secretu SLACK_WEBHOOK)
$SLACK_WEBHOOK = '';
if (is_file(__DIR__ . '/slack-config.php')) include __DIR__ . '/slack-config.php';
if ($SLACK_WEBHOOK !== '' && function_exists('curl_init')) {
  $esc = fn($s) => str_replace(['&', '<', '>'], ['&amp;', '&lt;', '&gt;'], $s);
  $field = fn($t, $v) => ['title' => $t, 'value' => $esc($v !== '' ? $v : '—'), 'short' => false];
  // stejná podoba jako dřív z Elementoru: barevný pruh, nadpis, pod sebou pole tučně + hodnota
  $payload = ['attachments' => [[
    'color' => '#cdfe00',
    'title' => $agency ? 'Nová poptávka spolupráce' : 'Nová poptávka',
    'text' => 'Nová poptávka z formuláře na webu',
    'fields' => [
      $field('Jméno', $name), $field('E-mail', $email), $field('Telefon', $phone),
      $field('Co potřebuje', $type), $field('Zpráva', $msg),
      $field('Spěchá', $urgent === 'ANO' ? 'Potřebuji web rychle' : 'ne'),
      $field('Stránka', $page),
    ],
    'footer' => 'webovybalicek.cz',
    'ts' => time(),
  ]]];
  $ch = curl_init($SLACK_WEBHOOK);
  curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
    CURLOPT_POSTFIELDS => json_encode($payload, JSON_UNESCAPED_UNICODE), CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 5]);
  $slackOk = curl_exec($ch) === 'ok';
  curl_close($ch);
  $ok = $ok || $slackOk;
}
out($ok ? 200 : 500, ['ok' => (bool)$ok]);
