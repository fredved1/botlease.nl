// Serves Google Search Console verification file content.
// Bypasses Vercel's cleanUrls .html-redirect behavior.
export default function handler(_req, res) {
  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  res.status(200).send('google-site-verification: googled352441549b06d7c.html');
}
