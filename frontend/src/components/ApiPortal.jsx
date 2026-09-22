import React, { useState } from 'react';
import { Code2, Key, Download, Copy, Check, Terminal, ExternalLink } from 'lucide-react';

export default function ApiPortal({ onExportCsv }) {
  const [copiedIndex, setCopiedIndex] = useState(null);
  const [apiKey] = useState('mospi_live_key_9f8d7c6b5a4e3f21');

  const copyToClipboard = (text, idx) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(idx);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const codeSnippets = [
    {
      title: 'Python (MoSPI Data Pipeline Integration)',
      language: 'python',
      code: `import requests

url = "http://127.0.0.1:8000/api/v1/apix/summary"
headers = {"X-MoSPI-API-Key": "${apiKey}"}

response = requests.get(url, headers=headers)
data = response.json()

print(f"Latest APIx National Index: {data['apix_national']}")
print(f"Fisher Ideal Index: {data['apix_national']}, CPI Benchmark: {data['cpi_transport_benchmark']}")`
    },
    {
      title: 'cURL Request (RBI Macroeconomic Model)',
      language: 'bash',
      code: `curl -X GET "http://127.0.0.1:8000/api/v1/apix/history?days=30" \\
     -H "Accept: application/json" \\
     -H "X-MoSPI-API-Key: ${apiKey}"`
    }
  ];

  return (
    <div className="glass-panel p-6 mb-6">
      
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 mb-6 border-b border-slate-800 gap-4">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Code2 className="w-5 h-5 text-sky-400" />
            MoSPI & RBI Open Data REST API & Export Portal
          </h2>
          <p className="text-xs text-slate-400">
            OpenAPI compliance endpoints for direct automated ingestion into MoSPI e-Sankhyiki portal & RBI monetary policy models
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={onExportCsv}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-lg shadow-emerald-600/20 transition-all"
          >
            <Download className="w-4 h-4" />
            Download Full Quotes CSV
          </button>
          
          <a
            href="http://127.0.0.1:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-sky-400 text-xs font-semibold border border-slate-700 transition-all"
          >
            <ExternalLink className="w-4 h-4" />
            Interactive Swagger Docs
          </a>
        </div>
      </div>

      {/* API Key Box */}
      <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 mb-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-sky-500/10 text-sky-400">
            <Key className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold text-slate-200">MoSPI Institutional API Key</span>
            <p className="text-[11px] font-mono text-slate-400">{apiKey}</p>
          </div>
        </div>
        <button
          onClick={() => copyToClipboard(apiKey, 'key')}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 text-xs font-medium border border-slate-700 hover:text-white"
        >
          {copiedIndex === 'key' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          {copiedIndex === 'key' ? 'Copied' : 'Copy Key'}
        </button>
      </div>

      {/* Code Snippets */}
      <div className="space-y-4">
        {codeSnippets.map((snippet, idx) => (
          <div key={idx} className="rounded-xl bg-slate-950 border border-slate-800 overflow-hidden">
            <div className="px-4 py-2.5 bg-slate-900 border-b border-slate-800 flex items-center justify-between text-xs">
              <span className="font-semibold text-slate-300 flex items-center gap-2">
                <Terminal className="w-3.5 h-3.5 text-sky-400" />
                {snippet.title}
              </span>
              <button
                onClick={() => copyToClipboard(snippet.code, idx)}
                className="flex items-center gap-1 text-[11px] text-slate-400 hover:text-white"
              >
                {copiedIndex === idx ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                {copiedIndex === idx ? 'Copied' : 'Copy Code'}
              </button>
            </div>
            <pre className="p-4 text-xs font-mono text-slate-300 overflow-x-auto leading-relaxed">
              <code>{snippet.code}</code>
            </pre>
          </div>
        ))}
      </div>

    </div>
  );
}
