const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const PORT = 3000;
const ROOT = path.resolve(__dirname, '..');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.enc': 'application/octet-stream',
  '.pdf': 'application/pdf',
  '.webmanifest': 'application/manifest+json; charset=utf-8'
};

function getLocalIpAddresses() {
  const interfaces = os.networkInterfaces();
  const addresses = [];
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        addresses.push(iface.address);
      }
    }
  }
  return addresses;
}

const server = http.createServer((req, res) => {
  const urlPath = req.url.split('?')[0];
  let filePath = urlPath === '/' ? '/prototype/index.html' : urlPath;
  const fullPath = path.join(ROOT, decodeURIComponent(filePath));

  if (!fullPath.startsWith(ROOT)) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('403 Forbidden');
    return;
  }

  fs.stat(fullPath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Not Found: ' + urlPath);
      return;
    }

    const ext = path.extname(fullPath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    res.writeHead(200, {
      'Content-Type': contentType,
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Access-Control-Allow-Origin': '*'
    });

    const stream = fs.createReadStream(fullPath);
    stream.pipe(res);
  });
});

server.listen(PORT, '0.0.0.0', () => {
  const ips = getLocalIpAddresses();
  console.log('\n======================================================');
  console.log('📱 MISSA MVP 개발자 전용 태블릿 테스트 로컬 서버 실행 중');
  console.log('======================================================');
  console.log(`\n[PC 브라우저 접속]`);
  console.log(`👉 http://localhost:${PORT}/prototype/index.html`);
  console.log(`👉 http://localhost:${PORT}/review/08-integration-v1.html (통합 검수용)`);
  
  if (ips.length > 0) {
    console.log(`\n[태블릿 접속 (동일 Wi-Fi 연결 시 태블릿 브라우저에 입력)]`);
    ips.forEach(ip => {
      console.log(`📲 http://${ip}:${PORT}/prototype/index.html`);
    });
  } else {
    console.log('\n[알림] 로컬 Wi-Fi IP를 찾지 못했습니다. 네트워크 연결을 확인하세요.');
  }
  console.log('\n종료하려면 터미널에서 Ctrl+C를 누르세요.\n');
});
