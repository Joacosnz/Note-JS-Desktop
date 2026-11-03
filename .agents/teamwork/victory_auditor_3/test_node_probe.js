const fs = require('fs');
const code = fs.readFileSync('frontend/app.js', 'utf8');

// Mock browser environment
const NOTION_COLOR_HEX_MAP = {
  red: '#e03e3e',
  yellow: '#dfab01',
  blue: '#0b6e99',
  red_background: '#fbded5'
};
const window = {
  NOTION_COLOR_HEX_MAP,
  location: { search: '' },
  localStorage: { getItem: () => null, setItem: () => {} }
};
const document = {
  addEventListener: () => {},
  getElementById: () => null,
  querySelector: () => null,
  querySelectorAll: () => [],
  createElement: (tag) => {
    return {
      tagName: tag.toUpperCase(),
      className: '',
      style: {},
      attributes: {},
      innerHTML: '',
      setAttribute(k, v) { this.attributes[k] = v; },
      getAttribute(k) { return this.attributes[k]; }
    };
  }
};
global.window = window;
global.document = document;
global.escapeHtml = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
global.sanitizeLinkUrl = (u) => String(u || '');
global.NOTION_COLOR_HEX_MAP = NOTION_COLOR_HEX_MAP;

// Extract parseRichTextToHtml
const regex = /function parseRichTextToHtml\([\s\S]*?window\.parseRichTextToHtml = parseRichTextToHtml;/;
const match = code.match(regex);
if (!match) throw new Error('parseRichTextToHtml not found in app.js');

eval(match[0]);

const tuples = [
  ['Bold and italic', [['b'], ['i']]],
  [' and ', []],
  ['colored code', [['c'], ['h', 'red']]]
];

const html = window.parseRichTextToHtml(tuples);
console.log('RENDERED_HTML:', html);

if (!html.includes('<em><strong>Bold and italic</strong></em>') && !html.includes('<strong><em>Bold and italic</em></strong>')) {
  throw new Error('Bold/italic nesting failed: ' + html);
}
if (!html.includes('<mark style="color: #e03e3e;" class="notion-color-red" data-color="red"><code>colored code</code></mark>')) {
  throw new Error('Colored code failed: ' + html);
}

console.log('NODE_FRONTEND_PROBE_SUCCESS');
