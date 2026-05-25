/** Lightweight markdown → HTML for Atlas chat messages */

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

export function renderMarkdown(text) {
  if (!text) return '';

  const blocks = [];
  let buf = [];
  const lines = text.split('\n');

  const flush = () => {
    if (buf.length) {
      blocks.push(buf.join('\n'));
      buf = [];
    }
  };

  for (const line of lines) {
    if (line.startsWith('```')) {
      flush();
      blocks.push(line);
    } else {
      buf.push(line);
    }
  }
  flush();

  let html = '';
  let inCode = false;
  let codeLang = '';
  let codeLines = [];

  for (const block of blocks) {
    if (block.startsWith('```')) {
      if (!inCode) {
        inCode = true;
        codeLang = block.slice(3).trim();
        codeLines = [];
      } else {
        inCode = false;
        html += `<pre><code>${escapeHtml(codeLines.join('\n'))}</code></pre>`;
      }
      continue;
    }

    if (inCode) {
      codeLines.push(block);
      continue;
    }

    html += renderBlock(block);
  }

  return html;
}

function renderBlock(block) {
  const lines = block.split('\n');
  let out = '';
  let inList = false;

  for (let line of lines) {
    if (line.trim() === '---') {
      if (inList) { out += '</ul>'; inList = false; }
      out += '<hr>';
      continue;
    }

    const h3 = line.match(/^### (.+)$/);
    const h2 = line.match(/^## (.+)$/);
    if (h3) {
      if (inList) { out += '</ul>'; inList = false; }
      out += `<h3>${inline(h3[1])}</h3>`;
      continue;
    }
    if (h2) {
      if (inList) { out += '</ul>'; inList = false; }
      out += `<h3>${inline(h2[1])}</h3>`;
      continue;
    }

    const li = line.match(/^[-*] (.+)$/);
    if (li) {
      if (!inList) { out += '<ul>'; inList = true; }
      out += `<li>${inline(li[1])}</li>`;
      continue;
    }

    if (inList) { out += '</ul>'; inList = false; }

    if (line.trim() === '') continue;
    out += `<p>${inline(line)}</p>`;
  }

  if (inList) out += '</ul>';
  return out;
}

function inline(s) {
  return escapeHtml(s)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code>$1</code>');
}
