'use strict';
initNav('cla');
initAuthGuard(function(user) {
  // Load AI analysis data, then render CLA
  fetchJSON('ai_analysis.json').then(function(aiData) {
    dataCache['ai_analysis.json'] = aiData;
    renderCLASummary(aiData);
    loadCLADeepData();
  });

  // ============================================================
  // CLA SUMMARY
  // ============================================================
  function renderCLASummary(aiData) {
    var container = document.getElementById('claContent');
    if (!aiData || !aiData.cla) { container.innerHTML = '<p class="text-muted">CLA分析データを取得できませんでした。</p>'; return; }

    var cla = aiData.cla;
    var catKeys = Object.keys(cla);

    var html = '<details class="report-card"><summary class="report-summary">' +
      '<span class="report-chevron">&#9654;</span>' +
      '<span class="report-label">最新CLA分析</span>' +
      '<span class="report-count">' + catKeys.length + '分野</span>' +
      '</summary><div class="report-body">';
    html += '<div class="pestle-grid">';

    catKeys.forEach(function(catKey) {
      var catData = cla[catKey];
      if (!catData) return;
      var info = PESTLE_CATS[catKey] || { labelJa: catKey, color: 'var(--accent)' };

      html += '<div class="pestle-card">';
      html += '<div class="pestle-card-top" style="background:' + info.color + '"></div>';
      html += '<div class="pestle-card-header"><span class="pestle-cat-name" style="color:' + info.color + '">' + info.labelJa + '</span></div>';
      html += '<div style="padding:0 20px 16px">';

      CLA_LAYERS.forEach(function(layer) {
        if (catData[layer.key]) {
          html += '<div style="padding:8px 0;border-bottom:1px solid var(--border-light)">' +
            '<div class="fs-label" style="font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;margin-bottom:3px">' + layer.labelJa + '</div>' +
            '<div class="fs-body-sm" style="line-height:1.7">' + escapeHtml(catData[layer.key]) + '</div></div>';
        }
      });

      html += '</div></div>';
    });

    html += '</div></div></details>';
    container.innerHTML = html;
    loadCLAArchive();
  }

  // ============================================================
  // CLA DEEP LAYER ENHANCEMENT
  // ============================================================
  var claDeepData = {};

  function switchCLADeepTab(tab) {
    document.querySelectorAll('.cla-deep-tab').forEach(function(b) {
      b.style.background = 'transparent'; b.style.color = 'var(--text-secondary)';
      b.classList.remove('active');
    });
    var btn = document.querySelector('.cla-deep-tab[data-tab="' + tab + '"]');
    if (btn) { btn.style.background = 'var(--accent)'; btn.style.color = '#fff'; btn.classList.add('active'); }
    document.querySelectorAll('.cla-deep-panel').forEach(function(p) { p.style.display = 'none'; });
    var panel = document.getElementById('claDeep' + tab.charAt(0).toUpperCase() + tab.slice(1));
    if (panel) panel.style.display = 'block';
  }

  // Inline sample data for immediate display (fallback if JSON fetch fails)
  var CLA_DEEP_SAMPLE = {
    ngram: {
      concepts: {
        'democracy': { pestle_category: 'Political', trend_10yr: -33.4, latest_value: 6.81e-06, data: [{year:1990,freq:1.2e-05},{year:1995,freq:1.15e-05},{year:2000,freq:1.1e-05},{year:2005,freq:1.0e-05},{year:2010,freq:9.5e-06},{year:2015,freq:8.2e-06},{year:2020,freq:7.0e-06}] },
        'artificial intelligence': { pestle_category: 'Technological', trend_10yr: 22.4, latest_value: 3.2e-06, data: [{year:1990,freq:8e-07},{year:1995,freq:1.2e-06},{year:2000,freq:1.8e-06},{year:2005,freq:2.0e-06},{year:2010,freq:2.2e-06},{year:2015,freq:2.5e-06},{year:2020,freq:3.2e-06}] },
        'resilience': { pestle_category: 'Social', trend_10yr: 51.5, latest_value: 5.1e-06, data: [{year:1990,freq:1.5e-06},{year:1995,freq:2.0e-06},{year:2000,freq:2.5e-06},{year:2005,freq:3.0e-06},{year:2010,freq:3.5e-06},{year:2015,freq:4.2e-06},{year:2020,freq:5.1e-06}] },
        'globalization': { pestle_category: 'Economic', trend_10yr: -45.0, latest_value: 4.8e-06, data: [{year:1990,freq:3.0e-06},{year:1995,freq:6.5e-06},{year:2000,freq:1.1e-05},{year:2005,freq:1.0e-05},{year:2010,freq:9.0e-06},{year:2015,freq:7.0e-06},{year:2020,freq:4.8e-06}] },
        'climate change': { pestle_category: 'Environmental', trend_10yr: 7.9, latest_value: 8.5e-06, data: [{year:1990,freq:2.0e-06},{year:1995,freq:3.0e-06},{year:2000,freq:5.0e-06},{year:2005,freq:7.0e-06},{year:2010,freq:9.0e-06},{year:2015,freq:8.5e-06},{year:2020,freq:8.5e-06}] },
        'progress': { pestle_category: 'Social', trend_10yr: -34.8, latest_value: 2.8e-05, data: [{year:1990,freq:4.5e-05},{year:1995,freq:4.2e-05},{year:2000,freq:4.0e-05},{year:2005,freq:3.8e-05},{year:2010,freq:3.5e-05},{year:2015,freq:3.2e-05},{year:2020,freq:2.8e-05}] },
        'dystopia': { pestle_category: 'Mythological', trend_10yr: 17.7, latest_value: 1.8e-06, data: [{year:1990,freq:5e-07},{year:1995,freq:6e-07},{year:2000,freq:8e-07},{year:2005,freq:1.0e-06},{year:2010,freq:1.2e-06},{year:2015,freq:1.5e-06},{year:2020,freq:1.8e-06}] },
        'apocalypse': { pestle_category: 'Mythological', trend_10yr: 10.2, latest_value: 2.1e-06, data: [{year:1990,freq:1.2e-06},{year:1995,freq:1.4e-06},{year:2000,freq:1.6e-06},{year:2005,freq:1.8e-06},{year:2010,freq:2.0e-06},{year:2015,freq:2.0e-06},{year:2020,freq:2.1e-06}] },
        'sustainability': { pestle_category: 'Environmental', trend_10yr: 3.6, latest_value: 7.5e-06, data: [{year:1990,freq:2.0e-06},{year:1995,freq:3.5e-06},{year:2000,freq:5.0e-06},{year:2005,freq:6.5e-06},{year:2010,freq:7.0e-06},{year:2015,freq:7.5e-06},{year:2020,freq:7.5e-06}] },
        'nationalism': { pestle_category: 'Political', trend_10yr: -32.6, latest_value: 5.5e-06, data: [{year:1990,freq:9.0e-06},{year:1995,freq:8.5e-06},{year:2000,freq:8.0e-06},{year:2005,freq:7.5e-06},{year:2010,freq:7.0e-06},{year:2015,freq:6.5e-06},{year:2020,freq:5.5e-06}] }
      },
      source: 'Google Books Ngram Viewer (en-2019, smoothing=3)',
      coverage: '1950-2022, 20 concepts'
    },
    network: {
      nodes: [
        {id:8,name:'スマートフォンOS事業者による生成AI排除と「プラットフォーム権力の第二段階」',pestle_categories:['技術','経済','法律','社会'],cla_depth:'worldview',composite_score:8.0,signal_type:'weak_signal',betweenness:1.0,eigenvector:1.0,in_degree:0.94,out_degree:1.0,cluster_id:1,is_supernode:true},
        {id:105,name:'超知能規制の階級的分裂による民主的コンセンサス構造の崩壊',pestle_categories:['技術','政治','法律'],cla_depth:'worldview',composite_score:8.6,signal_type:'paradigm_shift',betweenness:1.0,eigenvector:1.0,in_degree:0.91,out_degree:0.97,cluster_id:1,is_supernode:true},
        {id:106,name:'超知能規制の階級的分裂：市民拒否と国家安全保障機関の採用の並行進行',pestle_categories:['技術','政治','社会'],cla_depth:'worldview',composite_score:8.4,signal_type:'wild_card',betweenness:1.0,eigenvector:1.0,in_degree:0.93,out_degree:0.99,cluster_id:1,is_supernode:true},
        {id:2,name:'ホルムズ海峡複合インフラ脆弱性の構造化：エネルギー-情報-金融の同時遮断可能性',pestle_categories:['技術','経済','政治','環境'],cla_depth:'systemic',composite_score:8.2,signal_type:'weak_signal',betweenness:0.918,eigenvector:1.0,in_degree:1.0,out_degree:0.93,cluster_id:1,is_supernode:true},
        {id:115,name:'通貨政策と雇用目標の明示的分離による福祉国家の根本矛盾の露呈',pestle_categories:['経済','社会','政治'],cla_depth:'worldview',composite_score:7.8,signal_type:'paradigm_shift',betweenness:0.96,eigenvector:0.99,in_degree:0.85,out_degree:0.91,cluster_id:4,is_supernode:true}
      ],
      edges: [
        {source:105,target:106,impact_score:3.0,impact_type:'amplify',is_llm:true},
        {source:105,target:8,impact_score:3.0,impact_type:'catalyze',is_llm:true},
        {source:2,target:105,impact_score:2.5,impact_type:'amplify',is_llm:true},
        {source:105,target:115,impact_score:3.0,impact_type:'catalyze',is_llm:true}
      ],
      clusters: {
        '1': {label:'技術',color:'#dc2626',size:20,supernodes:5},
        '3': {label:'政治',color:'#2563eb',size:10,supernodes:0},
        '4': {label:'経済',color:'#d97706',size:11,supernodes:2},
        '0': {label:'環境',color:'#16a34a',size:4,supernodes:0}
      },
      stats: {total_nodes:30,total_edges:300,supernodes:7,llm_evaluated_edges:90}
    },
    myth: {
      thompson_summary: {
        'D': {name:'魔法・変容',name_en:'Magic',count:7149},
        'A': {name:'神話的モチーフ',name_en:'Mythological Motifs',count:5779},
        'F': {name:'異界・驚異',name_en:'Marvels',count:5349},
        'K': {name:'欺き',name_en:'Deceptions',count:3767},
        'J': {name:'賢者と愚者',name_en:'The Wise and the Foolish',count:3517},
        'H': {name:'試練',name_en:'Tests',count:2746},
        'B': {name:'動物',name_en:'Animals',count:2661},
        'E': {name:'死と復活',name_en:'The Dead',count:2186},
        'G': {name:'食人鬼・怪物',name_en:'Ogres',count:1744},
        'Q': {name:'報いと罰',name_en:'Rewards and Punishments',count:1495},
        'T': {name:'性',name_en:'Sex',count:1371},
        'C': {name:'タブー',name_en:'Tabu',count:1239},
        'V': {name:'宗教',name_en:'Religion',count:973},
        'N': {name:'偶然と運命',name_en:'Chance and Fate',count:948},
        'P': {name:'社会',name_en:'Society',count:846},
        'M': {name:'未来の定め',name_en:'Ordaining the Future',count:844},
        'X': {name:'ユーモア',name_en:'Humor',count:750}
      },
      thompson_total: 45496,
      keyword_to_thompson: {
        '変容':['D','E'],'技術':['D','F'],'救済':['A','V','Q'],'支配':['D','K','G'],
        '自由':['R','L'],'境界':['C','F'],'創造':['A'],'破壊':['E','S','G'],
        '運命':['M','N'],'試練':['H'],'復活':['E'],'英雄':['H','L'],
        'プロメテウス':['A','D','Q'],'パンドラ':['C','A'],'AI':['D','F'],
        '黙示録':['A','E'],'進歩':['D','U'],'民主':['P','J'],'権力':['P','K','G']
      },
      unesco_ich: {
        total: 849,
        archetype_distribution: {performance:302,cultural_practice:271,ritual:189,craft_knowledge:92,nature_knowledge:60,oral_tradition:59,food_culture:31,healing:11}
      },
      cla_myth_connection_guide: {
        example: {
          cla_text: '「技術的救世主」と「技術的啓示録」の並存',
          matched_keywords: ['技術','救済','黙示録'],
          thompson_categories: ['A (神話)','D (魔法・変容)','E (死と復活)','V (宗教)'],
          interpretation: '現代のAI神話はThompsonのD(Magic)カテゴリ — 7,149件の「変容」モチーフ群 — と構造的に同型'
        }
      }
    }
  };

  // ============================================================
  // LOAD CLA DEEP DATA
  // ============================================================
  async function loadCLADeepData() {
    // Render sample data immediately so tabs have content
    renderNgramOverlay(CLA_DEEP_SAMPLE.ngram);
    renderSignalNetwork(CLA_DEEP_SAMPLE.network);
    renderMythMapping(CLA_DEEP_SAMPLE.myth);

    // Attach tab switching
    var tabBar = document.getElementById('claDeepTabBar');
    if (tabBar && !tabBar._bound) {
      tabBar._bound = true;
      tabBar.addEventListener('click', function(e) {
        var btn = e.target.closest('[data-tab]');
        if (!btn) return;
        var tab = btn.getAttribute('data-tab');
        tabBar.querySelectorAll('.cla-deep-tab').forEach(function(b) {
          b.style.background = 'transparent'; b.style.color = 'var(--text-secondary)'; b.style.fontWeight = 'normal';
        });
        btn.style.background = 'var(--accent)'; btn.style.color = '#fff'; btn.style.fontWeight = '600';
        document.querySelectorAll('.cla-deep-panel').forEach(function(p) { p.style.display = 'none'; });
        var panel = document.getElementById('claDeep' + tab.charAt(0).toUpperCase() + tab.slice(1));
        if (panel) panel.style.display = 'block';
      });
    }

    // Then try to load full data from local data/ directory
    try {
      var results = await Promise.all([
        _fetchLocalJSON('data/cla_ngram_overlay.json'),
        _fetchLocalJSON('data/signal_network.json'),
        _fetchLocalJSON('data/cla_evidence.json'),
        _fetchLocalJSON('data/cla_myth_mapping.json')
      ]);
      if (results[0]) renderNgramOverlay(results[0]);
      if (results[1]) renderSignalNetwork(results[1]);
      if (results[2]) renderCLAEvidence(results[2]);
      if (results[3]) renderMythMapping(results[3]);
    } catch (e) {
      console.error('CLA deep data upgrade error (sample data shown):', e);
    }
  }

  // ============================================================
  // NGRAM OVERLAY
  // ============================================================
  function renderNgramOverlay(data) {
    var el = document.getElementById('claDeepNgram');
    if (!data || !data.concepts) { el.innerHTML = '<p class="text-muted">Ngramデータなし</p>'; return; }

    var groups = {};
    Object.entries(data.concepts).forEach(function(kv) {
      var name = kv[0], info = kv[1];
      var cat = info.pestle_category || 'Other';
      if (!groups[cat]) groups[cat] = [];
      groups[cat].push(Object.assign({ name: name }, info));
    });

    Object.values(groups).forEach(function(g) { g.sort(function(a, b) { return Math.abs(b.trend_10yr || 0) - Math.abs(a.trend_10yr || 0); }); });

    var catColors = { Political: '#2563eb', Economic: '#d97706', Social: '#8b5cf6', Technological: '#dc2626', Environmental: '#16a34a', Mythological: '#78350f' };

    var html = '<div style="margin-bottom:12px"><div class="fs-label" style="font-weight:700;margin-bottom:4px">Google Ngram 概念頻度トレンド（1950-2022）</div>';
    html += '<div class="fs-caption" style="color:var(--text-muted)">書籍コーパスにおける概念の使用頻度変化。CLA世界観層・神話層の定量的裏付け</div></div>';

    Object.entries(groups).forEach(function(kv) {
      var cat = kv[0], concepts = kv[1];
      var color = catColors[cat] || '#64748b';
      html += '<div style="margin-bottom:16px"><div class="fs-meta" style="font-weight:700;color:' + color + ';margin-bottom:8px">' + cat + '</div>';
      html += '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:8px">';
      concepts.forEach(function(c) {
        var trend = c.trend_10yr || 0;
        var arrow = trend > 0 ? '\u2191' : trend < 0 ? '\u2193' : '\u2192';
        var trendColor = trend > 10 ? '#16a34a' : trend < -10 ? '#dc2626' : '#64748b';
        var vals = (c.data || []).map(function(d) { return d.freq; });
        var sparkSvg = buildSparkline(vals, color, 120, 24);
        html += '<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:6px">';
        html += '<div style="flex:1;min-width:0"><div class="fs-body-sm" style="font-weight:600">' + c.name + '</div>';
        html += '<div class="fs-caption" style="color:' + trendColor + ';font-weight:700">' + arrow + ' ' + (trend > 0 ? '+' : '') + trend.toFixed(1) + '%</div></div>';
        html += '<div>' + sparkSvg + '</div></div>';
      });
      html += '</div></div>';
    });
    el.innerHTML = html;
  }

  function buildSparkline(values, color, width, height) {
    if (!values || values.length < 2) return '';
    var min = Math.min.apply(null, values.filter(function(v) { return v > 0; }));
    var max = Math.max.apply(null, values);
    var range = max - min || 1;
    var step = width / (values.length - 1);
    var path = '';
    values.forEach(function(v, i) {
      var x = i * step;
      var y = height - ((v - min) / range) * (height - 2) - 1;
      path += (i === 0 ? 'M' : 'L') + x.toFixed(1) + ',' + y.toFixed(1);
    });
    return '<svg width="' + width + '" height="' + height + '" viewBox="0 0 ' + width + ' ' + height + '"><path d="' + path + '" fill="none" stroke="' + color + '" stroke-width="1.5" opacity="0.7"/></svg>';
  }

  // ============================================================
  // SIGNAL NETWORK
  // ============================================================
  function renderSignalNetwork(data) {
    var el = document.getElementById('claDeepNetwork');
    if (!data || !data.nodes) { el.innerHTML = '<p class="text-muted">ネットワークデータなし</p>'; return; }

    var stats = data.stats || {};
    var supernodes = data.nodes.filter(function(n) { return n.is_supernode; });
    var clusterInfo = data.clusters || {};

    var html = '<div style="margin-bottom:12px"><div class="fs-label" style="font-weight:700;margin-bottom:4px">シグナル・スーパーノード・ネットワーク</div>';
    html += '<div class="fs-caption" style="color:var(--text-muted)">シグナル間のクロスインパクト分析。高媒介中心性ノードが複数ドメインを横断するカスケードのハブ</div></div>';

    html += '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px">';
    html += '<div style="padding:8px 14px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:6px;text-align:center"><div class="fs-body-sm" style="font-weight:700;color:var(--accent)">' + (stats.total_nodes || 0) + '</div><div class="fs-caption">シグナル</div></div>';
    html += '<div style="padding:8px 14px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:6px;text-align:center"><div class="fs-body-sm" style="font-weight:700;color:var(--accent)">' + (stats.total_edges || 0) + '</div><div class="fs-caption">影響関係</div></div>';
    html += '<div style="padding:8px 14px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:6px;text-align:center"><div class="fs-body-sm" style="font-weight:700;color:#dc2626">' + (stats.supernodes || 0) + '</div><div class="fs-caption">スーパーノード</div></div>';
    html += '<div style="padding:8px 14px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:6px;text-align:center"><div class="fs-body-sm" style="font-weight:700;color:var(--accent)">' + (stats.llm_evaluated_edges || 0) + '</div><div class="fs-caption">LLM精密評価</div></div>';
    html += '</div>';

    html += '<div class="fs-meta" style="font-weight:700;margin-bottom:8px">クラスター構造</div>';
    html += '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">';
    Object.entries(clusterInfo).forEach(function(kv) {
      var id = kv[0], cl = kv[1];
      html += '<div style="display:flex;align-items:center;gap:6px;padding:6px 12px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:6px">';
      html += '<div style="width:10px;height:10px;border-radius:50%;background:' + cl.color + '"></div>';
      html += '<span class="fs-body-sm" style="font-weight:600">' + cl.label + '</span>';
      html += '<span class="fs-caption">' + cl.size + '件</span>';
      if (cl.supernodes > 0) html += '<span class="fs-caption" style="color:#dc2626;font-weight:700">\u2605' + cl.supernodes + '</span>';
      html += '</div>';
    });
    html += '</div>';

    if (supernodes.length > 0) {
      html += '<div class="fs-meta" style="font-weight:700;margin-bottom:8px;color:#dc2626">スーパーノード（カスケード・ハブ）</div>';
      html += '<div style="display:flex;flex-direction:column;gap:8px">';
      supernodes.sort(function(a, b) { return b.betweenness - a.betweenness; });
      supernodes.forEach(function(sn, i) {
        var clColor = (clusterInfo[sn.cluster_id] && clusterInfo[sn.cluster_id].color) || '#64748b';
        html += '<div style="padding:12px 16px;background:var(--card-bg);border:1px solid var(--border-light);border-left:3px solid ' + clColor + ';border-radius:6px">';
        html += '<div class="fs-body-sm" style="font-weight:700">' + (i + 1) + '. ' + sn.name + '</div>';
        html += '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:6px">';
        var claLevel = sn.cla_depth === 'worldview' ? 3 : sn.cla_depth === 'myth' ? 4 : sn.cla_depth === 'systemic' ? 2 : 1;
        html += '<span class="fs-caption" style="background:var(--cla-' + claLevel + ');padding:2px 8px;border-radius:4px">' + sn.cla_depth + '</span>';
        html += '<span class="fs-caption">PESTLE: ' + sn.pestle_categories.join(', ') + '</span>';
        html += '<span class="fs-caption">媒介中心性: ' + sn.betweenness.toFixed(3) + '</span>';
        html += '<span class="fs-caption">Score: ' + sn.composite_score + '</span>';
        html += '</div></div>';
      });
      html += '</div>';
    }

    var llmEdges = data.edges.filter(function(e) { return e.is_llm; }).sort(function(a, b) { return Math.abs(b.impact_score) - Math.abs(a.impact_score); }).slice(0, 10);
    if (llmEdges.length > 0) {
      var nodeMap = {};
      data.nodes.forEach(function(n) { nodeMap[n.id] = n.name; });
      html += '<div style="margin-top:16px"><div class="fs-meta" style="font-weight:700;margin-bottom:8px">主要な影響連鎖（LLM評価）</div>';
      html += '<div style="display:flex;flex-direction:column;gap:4px">';
      llmEdges.forEach(function(e) {
        var scoreColor = e.impact_score > 0 ? '#16a34a' : '#dc2626';
        var typeLabel = { amplify: '増幅', inhibit: '抑制', transform: '変質', catalyze: '触媒', neutral: '中立' }[e.impact_type] || e.impact_type;
        html += '<div class="fs-caption" style="padding:4px 8px;background:var(--card-bg);border-radius:4px">';
        html += '<span style="color:' + scoreColor + ';font-weight:700">[' + (e.impact_score > 0 ? '+' : '') + e.impact_score.toFixed(1) + ' ' + typeLabel + ']</span> ';
        html += ((nodeMap[e.source] || '?').substring(0, 30)) + ' \u2192 ' + ((nodeMap[e.target] || '?').substring(0, 30));
        html += '</div>';
      });
      html += '</div></div>';
    }

    el.innerHTML = html;
  }

  // ============================================================
  // CLA EVIDENCE
  // ============================================================
  function renderCLAEvidence(data) {
    var el = document.getElementById('claDeepEvidence');
    if (!data || !data.indicators_by_pestle) { el.innerHTML = '<p class="text-muted">社会指標データなし</p>'; return; }

    var catColors = { Political: '#2563eb', Economic: '#d97706', Social: '#8b5cf6', Technological: '#dc2626', Environmental: '#16a34a' };

    var html = '<div style="margin-bottom:12px"><div class="fs-label" style="font-weight:700;margin-bottom:4px">社会指標エビデンス（World Bank + HDI）</div>';
    html += '<div class="fs-caption" style="color:var(--text-muted)">CLA各層の定量的裏付け。10指標\u00d78カ国\u00d735年の時系列データ</div></div>';

    if (data.hdi_summary) {
      html += '<div style="margin-bottom:16px"><div class="fs-meta" style="font-weight:700;margin-bottom:8px">人間開発指数（HDI）推移</div>';
      html += '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px">';
      Object.entries(data.hdi_summary).forEach(function(kv) {
        var cc = kv[0], vals = kv[1];
        var latest = vals[vals.length - 1];
        var first = vals[0];
        var change = latest && first ? ((latest.value - first.value) / first.value * 100).toFixed(1) : '?';
        var spark = buildSparkline(vals.map(function(v) { return v.value; }), '#8b5cf6', 80, 20);
        html += '<div style="padding:8px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:6px;text-align:center">';
        html += '<div class="fs-meta" style="font-weight:700">' + cc + '</div>';
        html += '<div class="fs-caption">' + (latest && latest.value ? latest.value.toFixed(3) : '?') + ' <span style="color:' + (parseFloat(change) > 0 ? '#16a34a' : '#dc2626') + '">(' + change + '%)</span></div>';
        html += '<div style="margin-top:4px">' + spark + '</div></div>';
      });
      html += '</div></div>';
    }

    Object.entries(data.indicators_by_pestle).forEach(function(kv) {
      var pestle = kv[0], indicators = kv[1];
      var color = catColors[pestle] || '#64748b';
      html += '<div style="margin-bottom:16px"><div class="fs-meta" style="font-weight:700;color:' + color + ';margin-bottom:8px">' + pestle + '</div>';
      indicators.forEach(function(ind) {
        html += '<div style="margin-bottom:8px;padding:8px 12px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:6px">';
        html += '<div class="fs-body-sm" style="font-weight:600;margin-bottom:6px">' + ind.name + '</div>';
        html += '<div style="display:flex;gap:8px;flex-wrap:wrap">';
        Object.entries(ind.countries).forEach(function(kv2) {
          var cc = kv2[0], vals = kv2[1];
          if (vals.length === 0) return;
          var latest = vals[vals.length - 1];
          var spark = buildSparkline(vals.map(function(v) { return v.value; }), color, 60, 16);
          html += '<div style="display:flex;align-items:center;gap:4px"><span class="fs-caption" style="font-weight:600;width:28px">' + cc.substring(0, 3) + '</span>' + spark + '<span class="fs-caption">' + (typeof (latest && latest.value) === 'number' ? (latest.value > 1000 ? (latest.value / 1000).toFixed(0) + 'K' : latest.value.toFixed(1)) : '?') + '</span></div>';
        });
        html += '</div></div>';
      });
      html += '</div>';
    });

    el.innerHTML = html;
  }

  // ============================================================
  // MYTH MAPPING
  // ============================================================
  function renderMythMapping(data) {
    var el = document.getElementById('claDeepMyth');
    if (!data || !data.thompson_summary) { el.innerHTML = '<p class="text-muted">神話データなし</p>'; return; }

    var html = '<div style="margin-bottom:12px"><div class="fs-label" style="font-weight:700;margin-bottom:4px">神話パターンマッピング</div>';
    html += '<div class="fs-caption" style="color:var(--text-muted)">Thompson Motif-Index（45,496モチーフ）+ UNESCO無形文化遺産（849件）とCLA神話層の接続</div></div>';

    var cats = Object.entries(data.thompson_summary).sort(function(a, b) { return b[1].count - a[1].count; });
    var maxCount = cats[0] ? cats[0][1].count : 1;
    var thomColors = ['#dc2626', '#d97706', '#16a34a', '#2563eb', '#8b5cf6', '#ec4899', '#14b8a6', '#f59e0b', '#6366f1', '#10b981', '#f43f5e', '#0ea5e9'];

    html += '<div class="fs-meta" style="font-weight:700;margin-bottom:8px">Thompson Motif-Index カテゴリ分布</div>';
    html += '<div style="display:flex;flex-direction:column;gap:3px;margin-bottom:16px">';
    cats.forEach(function(kv, i) {
      var cat = kv[0], info = kv[1];
      var pct = (info.count / maxCount * 100).toFixed(0);
      var color = thomColors[i % thomColors.length];
      html += '<div style="display:flex;align-items:center;gap:8px">';
      html += '<div class="fs-caption" style="width:180px;text-align:right;flex-shrink:0">' + cat + ' ' + (info.name_en || '') + '</div>';
      html += '<div style="flex:1;height:18px;background:var(--border-light);border-radius:3px;overflow:hidden"><div style="width:' + pct + '%;height:100%;background:' + color + ';border-radius:3px;transition:width 0.5s"></div></div>';
      html += '<div class="fs-caption" style="width:50px;flex-shrink:0">' + info.count.toLocaleString() + '</div>';
      html += '</div>';
    });
    html += '</div>';

    if (data.keyword_to_thompson) {
      html += '<div class="fs-meta" style="font-weight:700;margin-bottom:8px">CLA神話キーワード \u2192 Thompson分類マッピング</div>';
      html += '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px">';
      Object.entries(data.keyword_to_thompson).forEach(function(kv) {
        var kw = kv[0], categories = kv[1];
        html += '<div style="padding:4px 10px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:12px;font-size:12px">';
        html += '<span style="font-weight:600">' + kw + '</span> \u2192 <span style="color:var(--text-muted)">' + categories.join(',') + '</span></div>';
      });
      html += '</div>';
    }

    if (data.cla_myth_connection_guide && data.cla_myth_connection_guide.example) {
      var ex = data.cla_myth_connection_guide.example;
      html += '<div style="padding:12px 16px;background:var(--cla-4);border:1px solid var(--border-light);border-radius:8px;margin-bottom:16px">';
      html += '<div class="fs-meta" style="font-weight:700;margin-bottom:6px">接続例</div>';
      html += '<div class="fs-body-sm" style="margin-bottom:4px"><strong>CLAテキスト:</strong> ' + escapeHtml(ex.cla_text) + '</div>';
      html += '<div class="fs-caption" style="margin-bottom:2px"><strong>マッチキーワード:</strong> ' + ex.matched_keywords.join(', ') + '</div>';
      html += '<div class="fs-caption" style="margin-bottom:2px"><strong>Thompson分類:</strong> ' + ex.thompson_categories.join(', ') + '</div>';
      html += '<div class="fs-caption" style="color:var(--accent)"><strong>解釈:</strong> ' + escapeHtml(ex.interpretation) + '</div>';
      html += '</div>';
    }

    if (data.unesco_ich) {
      html += '<div class="fs-meta" style="font-weight:700;margin-bottom:8px">UNESCO無形文化遺産（生きた神話的実践）</div>';
      html += '<div class="fs-caption" style="margin-bottom:8px">全' + data.unesco_ich.total + '件の無形文化遺産データ</div>';
      if (data.unesco_ich.archetype_distribution) {
        html += '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px">';
        Object.entries(data.unesco_ich.archetype_distribution).sort(function(a, b) { return b[1] - a[1]; }).forEach(function(kv) {
          html += '<span style="padding:3px 10px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:12px;font-size:11px">' + kv[0] + ' <strong>' + kv[1] + '</strong></span>';
        });
        html += '</div>';
      }
    }

    el.innerHTML = html;
  }

  // ============================================================
  // CLA FIRESTORE IMPORT (console/admin utility)
  // ============================================================
  window.importCLAToFirestore = async function() {
    console.log('CLA Firestore import started...');
    var v = Date.now();
    var results = await Promise.all([
      fetch(DATA_BASE + '/cla_historical_yearly.json?v=' + v),
      fetch(DATA_BASE + '/cla_historical_quarterly.json?v=' + v),
      fetch(DATA_BASE + '/cla_meta_report.json?v=' + v)
    ]);
    var yearlyRaw = results[0].ok ? await results[0].json() : [];
    var quarterlyRaw = results[1].ok ? await results[1].json() : [];
    var meta = results[2].ok ? await results[2].json() : null;
    var yearly = Array.isArray(yearlyRaw) ? yearlyRaw : (yearlyRaw.entries || []);
    var quarterly = Array.isArray(quarterlyRaw) ? quarterlyRaw : (quarterlyRaw.entries || []);
    console.log('Fetched: ' + yearly.length + ' yearly, ' + quarterly.length + ' quarterly');

    var batch = db.batch();
    var count = 0;
    var allEntries = yearly.concat(quarterly);
    for (var i = 0; i < allEntries.length; i++) {
      var entry = allEntries[i];
      if (!entry.period) continue;
      var ref = db.collection('cla_historical').doc(entry.period);
      var type = entry.type || (entry.period.includes('-') || entry.period.includes('Q') ? 'quarterly' : 'yearly');
      batch.set(ref, {
        period: entry.period, type: type,
        categories: entry.categories || {},
        cross_category_synthesis: entry.cross_category_synthesis || '',
        imported_at: firebase.firestore.FieldValue.serverTimestamp()
      });
      count++;
      if (count % 400 === 0) { await batch.commit(); batch = db.batch(); console.log('Committed ' + count + '...'); }
    }
    if (count % 400 !== 0) await batch.commit();
    console.log('Historical: ' + count + ' entries imported');

    if (meta) {
      var regions = ['japan', 'global'];
      for (var r = 0; r < regions.length; r++) {
        var region = regions[r];
        if (meta[region]) {
          await db.collection('cla_meta').doc(region).set(Object.assign({}, meta[region], {
            data_coverage: meta.data_coverage || {},
            generated_at: meta.generated_at || '',
            imported_at: firebase.firestore.FieldValue.serverTimestamp()
          }));
          console.log('Meta (' + region + '): ' + (meta[region].report_text || '').length + ' chars');
        }
      }
    }
    console.log('CLA import complete! ' + count + ' historical + meta reports');
    return count;
  };

  // ============================================================
  // CLA V2 RENDER
  // ============================================================
  function renderCLAV2(data) {
    var el = document.getElementById('claV2View');
    var entries = data.entries || [];
    var snTypes = data.supernode_types || {};

    var decades = {};
    entries.forEach(function(e) {
      var dec = e.period.substring(0, 3) + '0s';
      if (e.period === '2025') dec = '2020s';
      if (!decades[dec]) decades[dec] = [];
      decades[dec].push(e);
    });

    var catColors = {Political:'var(--P)',Economic:'var(--E)',Social:'var(--S)',Technological:'var(--T)',Legal:'var(--L)',Environmental:'var(--En)'};
    var catJa = {Political:'政治',Economic:'経済',Social:'社会',Technological:'技術',Legal:'法律',Environmental:'環境'};
    var layerLabels = [
      {key:'litany',label:'リタニー',color:'#92400e'},
      {key:'systemic_causes',label:'社会的原因',color:'#1e40af'},
      {key:'worldview',label:'世界観',color:'#5b21b6'},
      {key:'myth_metaphor',label:'神話・メタファー',color:'#9d174d'},
      {key:'key_tension',label:'核心的緊張',color:'#991b1b'},
      {key:'emerging_narrative',label:'新たな物語',color:'#065f46'}
    ];

    var snColors = {'\u5371\u6a5f':'#dc2626','\u4e3b\u6a29\u79e9\u5e8f':'#2563eb','\u7d4c\u6e08\u69cb\u9020':'#d97706','\u69cb\u9020\u7684':'#6b635b','\u793e\u4f1a\u5206\u88c2':'#8b5cf6','\u6280\u8853\u6a29\u529b':'#f59e0b'};

    var html = '';
    html += '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">';
    html += '<div style="padding:6px 14px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:6px;font-size:12px"><strong>' + entries.length + '</strong> 年</div>';
    html += '<div style="padding:6px 14px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:6px;font-size:12px"><strong>' + (entries.length * 6) + '</strong> 分析</div>';
    Object.entries(snColors).forEach(function(kv) {
      var type = kv[0], color = kv[1];
      var count = (snTypes[type] && snTypes[type].years) ? snTypes[type].years.length : 0;
      if (count > 0) {
        html += '<div style="padding:6px 14px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:6px;font-size:12px;display:flex;align-items:center;gap:4px">';
        html += '<span style="width:8px;height:8px;border-radius:50%;background:' + color + '"></span>' + type + ' <strong>' + count + '</strong></div>';
      }
    });
    html += '</div>';

    html += '<div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid var(--border-light)">';
    entries.forEach(function(e, i) {
      var sn = e.supernode || {};
      var snColor = snColors[sn.type] || '#6b635b';
      var active = i === 0 ? 'background:' + snColor + ';color:#fff;border-color:' + snColor : '';
      html += '<button class="clav2-year-btn" data-idx="' + i + '" data-sncolor="' + snColor + '" style="padding:4px 10px;border:1px solid var(--border-light);border-radius:5px;background:transparent;color:var(--text-secondary);cursor:pointer;font-size:11px;font-weight:600;border-bottom:3px solid ' + snColor + ';' + active + '">' + e.period + '</button>';
    });
    html += '</div>';

    entries.forEach(function(e, i) {
      var sn = e.supernode || {};
      var snColor = snColors[sn.type] || '#6b635b';
      var display = i === 0 ? 'block' : 'none';

      html += '<div class="clav2-year-panel" id="clav2p-' + i + '" style="display:' + display + '">';
      html += '<div style="padding:10px 16px;background:var(--card-bg);border:1px solid var(--border-light);border-left:4px solid ' + snColor + ';border-radius:8px;margin-bottom:12px;display:flex;align-items:center;gap:10px">';
      html += '<span style="width:10px;height:10px;border-radius:50%;background:' + snColor + ';flex-shrink:0"></span>';
      html += '<div><div class="fs-meta" style="font-weight:700;color:' + snColor + '">' + (sn.type || '') + '</div>';
      html += '<div class="fs-caption" style="color:var(--text-muted)">' + (sn.description || '') + '</div></div></div>';

      var cats = Object.keys(e.categories || {});
      var catOrder = ['Political','Economic','Social','Technological','Legal','Environmental'];
      cats.sort(function(a,b) { return catOrder.indexOf(a) - catOrder.indexOf(b); });

      html += '<div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:12px">';
      cats.forEach(function(cat, ci) {
        var color = catColors[cat] || 'var(--accent)';
        var st = ci === 0 ? 'background:' + color + ';color:#fff' : '';
        html += '<button class="clav2-cat-btn" data-yi="' + i + '" data-cat="' + cat + '" style="padding:5px 12px;border:1px solid var(--border-light);border-radius:6px;background:transparent;color:var(--text-secondary);cursor:pointer;font-size:12px;font-weight:600;' + st + '">' + (catJa[cat] || cat) + '</button>';
      });
      html += '</div>';

      cats.forEach(function(cat, ci) {
        var catData = e.categories[cat] || {};
        var cdisplay = ci === 0 ? 'block' : 'none';

        html += '<div class="clav2-cat-panel" data-yi="' + i + '" data-cat="' + cat + '" style="display:' + cdisplay + '">';
        html += '<div style="background:var(--card-bg);border:1px solid var(--border-light);border-radius:10px;overflow:hidden">';

        layerLabels.forEach(function(layer) {
          var text = catData[layer.key] || '';
          if (!text) return;
          html += '<div style="padding:12px 16px;border-bottom:1px solid var(--border-light)">';
          html += '<div class="fs-label" style="font-weight:700;color:' + layer.color + ';margin-bottom:3px;font-size:11px;text-transform:uppercase;letter-spacing:0.04em">' + layer.label + '</div>';
          html += '<div class="fs-body-sm" style="line-height:1.85">' + escapeHtml(text) + '</div>';
          html += '</div>';
        });

        html += '</div></div>';
      });

      html += '</div>';
    });

    html += '<div style="margin-top:16px;padding:12px 16px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:8px;font-size:11px;color:var(--text-muted)">';
    html += '<strong>CLA v2</strong> \u2014 Thompson Motif-Index (45,496\u30e2\u30c1\u30fc\u30d5) + Google Ngram (20\u6982\u5ff5) + World Bank\u793e\u4f1a\u6307\u6a19 + \u5e74\u5225\u30b9\u30fc\u30d1\u30fc\u30ce\u30fc\u30c9\u5206\u6790\u3002';
    html += ' \u5b66\u8853\u7684\u6839\u62e0: Wahab(2024), Inayatullah(2024-2025), Sustainability Science(2025)\u3002</div>';

    el.innerHTML = html;

    // Event delegation for year/cat buttons
    el.addEventListener('click', function(e) {
      var yearBtn = e.target.closest('.clav2-year-btn');
      if (yearBtn) {
        var idx = parseInt(yearBtn.getAttribute('data-idx'));
        el.querySelectorAll('.clav2-year-btn').forEach(function(b) {
          b.style.background = 'transparent'; b.style.color = 'var(--text-secondary)';
        });
        var snColor2 = yearBtn.getAttribute('data-sncolor') || '#6b635b';
        yearBtn.style.background = snColor2; yearBtn.style.color = '#fff'; yearBtn.style.borderColor = snColor2;
        el.querySelectorAll('.clav2-year-panel').forEach(function(p) { p.style.display = 'none'; });
        var panel = document.getElementById('clav2p-' + idx);
        if (panel) panel.style.display = 'block';
        return;
      }

      var catBtn = e.target.closest('.clav2-cat-btn');
      if (catBtn) {
        var yi = catBtn.getAttribute('data-yi');
        var cat = catBtn.getAttribute('data-cat');
        var yearPanel = document.getElementById('clav2p-' + yi);
        if (!yearPanel) return;
        yearPanel.querySelectorAll('.clav2-cat-btn').forEach(function(b) {
          b.style.background = 'transparent'; b.style.color = 'var(--text-secondary)';
        });
        var cc = {Political:'var(--P)',Economic:'var(--E)',Social:'var(--S)',Technological:'var(--T)',Legal:'var(--L)',Environmental:'var(--En)'};
        catBtn.style.background = cc[cat] || 'var(--accent)'; catBtn.style.color = '#fff';
        yearPanel.querySelectorAll('.clav2-cat-panel').forEach(function(p) { p.style.display = 'none'; });
        var cp = yearPanel.querySelector('.clav2-cat-panel[data-cat="' + cat + '"]');
        if (cp) cp.style.display = 'block';
      }
    });
  }

  // ============================================================
  // CLA ARCHIVE
  // ============================================================
  async function loadCLAArchive() {
    try {
      var yearly = [], quarterly = [], metaData = null;
      var source = 'static';

      try {
        var snap = await db.collection('cla_historical').orderBy('period').get();
        if (snap.size > 0) {
          snap.forEach(function(doc) {
            var d = doc.data();
            if (d.type === 'quarterly' || (d.period && (d.period.includes('-') || d.period.includes('Q')))) {
              quarterly.push(d);
            } else {
              yearly.push(d);
            }
          });
          source = 'firestore';
          console.log('CLA data loaded from Firestore:', yearly.length, 'yearly,', quarterly.length, 'quarterly');

          var metaSnap = await db.collection('cla_meta').get();
          if (metaSnap.size > 0) {
            metaData = {};
            metaSnap.forEach(function(doc) { metaData[doc.id] = doc.data(); });
          }
        }
      } catch (fsErr) {
        console.log('Firestore CLA not available, falling back to static JSON:', fsErr.message);
      }

      if (source === 'static') {
        var results = await Promise.all([
          fetchJSON('cla_historical_yearly.json'),
          fetchJSON('cla_historical_quarterly.json'),
          fetchJSON('cla_meta_report.json')
        ]);
        yearly = Array.isArray(results[0]) ? results[0] : ((results[0] && results[0].entries) || []);
        quarterly = Array.isArray(results[1]) ? results[1] : ((results[1] && results[1].entries) || []);
        metaData = results[2];
        console.log('CLA data loaded from static JSON:', yearly.length, 'yearly,', quarterly.length, 'quarterly');
      }

      if (metaData) {
        renderCLAMetaReport(metaData);
      }

      window._claYearly = yearly;
      window._claQuarterly = quarterly;
      window._claMeta = metaData;
      window._claV1Backup = { yearly: yearly.slice(), quarterly: quarterly.slice() };

      renderCLAArchiveView();

      // Setup v2 toggle
      var toggle = document.getElementById('claVersionToggle');
      if (toggle && !toggle._bound) {
        toggle._bound = true;
        toggle.addEventListener('click', function(e) {
          var btn = e.target.closest('[data-claver]');
          if (!btn) return;
          var ver = btn.getAttribute('data-claver');
          var v1B = document.getElementById('claVerV1');
          var v2B = document.getElementById('claVerV2');

          if (ver === 'v2') {
            v1B.style.background='transparent'; v1B.style.color='var(--text-secondary)';
            v2B.style.background='var(--accent)'; v2B.style.color='#fff';

            if (window._claV2Loaded) {
              window._claYearly = window._claV2Loaded.entries || [];
              window._claQuarterly = [];
              renderCLAArchiveView();
            } else {
              var av = document.getElementById('claArchiveView');
              av.innerHTML = '<div class="loading-indicator"><div class="loading-spinner loading-spinner-sm"></div><div>v2\u30c7\u30fc\u30bf\u3092\u8aad\u307f\u8fbc\u307f\u4e2d...</div></div>';
              fetch('data/cla_v2.json?v=' + Date.now())
                .then(function(r) { return r.json(); })
                .then(function(d) {
                  window._claV2Loaded = d;
                  window._claYearly = d.entries || [];
                  window._claQuarterly = [];
                  renderCLAArchiveView();
                })
                .catch(function() {
                  av.innerHTML = '<p style="padding:20px;color:var(--text-muted)">v2\u30c7\u30fc\u30bf\u306e\u8aad\u307f\u8fbc\u307f\u306b\u5931\u6557\u3057\u307e\u3057\u305f\u3002</p>';
                });
            }
          } else {
            v2B.style.background='transparent'; v2B.style.color='var(--text-secondary)';
            v1B.style.background='var(--accent)'; v1B.style.color='#fff';
            if (window._claV1Backup) {
              window._claYearly = window._claV1Backup.yearly;
              window._claQuarterly = window._claV1Backup.quarterly;
              renderCLAArchiveView();
            }
          }
        });
      }
    } catch (e) { console.error('CLA archive load error:', e); }
  }

  // ============================================================
  // META REPORT
  // ============================================================
  function renderCLAMetaReport(metaData) {
    var metaContainer = document.getElementById('claMetaContent');
    if (!metaContainer) return;
    if (!metaData) { metaContainer.innerHTML = '<p class="text-muted">メタレポートデータがありません。</p>'; return; }

    var regions = [
      { key: 'japan', label: '日本メディアの視点' },
      { key: 'global', label: 'グローバルの視点' }
    ];

    var html = '<h2 class="section-title" style="margin-bottom:12px">メタ分析レポート</h2>';
    regions.forEach(function(region) {
      var data = metaData[region.key];
      if (!data || !data.report_text) return;
      var preview = (data.report_text || '').replace(/^#{1,6}\s+.*/gm, '').replace(/\n+/g, ' ').trim().substring(0, 350);
      var shifts = data.key_paradigm_shifts || [];

      html += '<details class="report-card" style="margin-bottom:10px">' +
        '<summary class="report-summary">' +
          '<span class="report-chevron">&#9654;</span>' +
          '<span class="report-label">' + escapeHtml(data.title || region.label) + '</span>' +
          (shifts.length > 0 ? '<span class="report-count">' + shifts.length + '件のパラダイムシフト</span>' : '') +
        '</summary><div class="report-body">' +
        '<div class="report-preview">' + escapeHtml(preview) + '...</div>';

      if (shifts.length > 0) {
        html += '<div class="myth-grid" style="margin-bottom:1rem">';
        shifts.slice(0, 4).forEach(function(shift) {
          html += '<div class="myth-box"><div class="myth-label" style="color:var(--accent)">' + escapeHtml(shift.period || '') + '</div>' +
            '<div class="myth-item">' + escapeHtml(shift.description || shift.shift || '') + '</div></div>';
        });
        html += '</div>';
      }

      html += '<details><summary class="fulltext-toggle">全文を読む</summary>' +
        '<div class="fulltext-body md-body">' + renderMarkdown(data.report_text) + '</div></details>';
      html += '</div></details>';
    });

    metaContainer.innerHTML = html;
  }

  // ============================================================
  // CLA DOWNLOAD FUNCTIONS
  // ============================================================
  var CLA_CATEGORY_LABELS = {
    Political: '政治', Economic: '経済', Social: '社会',
    Technological: '技術', Legal: '法律', Environmental: '環境'
  };
  var CLA_CATEGORY_ORDER = ['Political','Economic','Social','Technological','Legal','Environmental'];
  var CLA_LAYER_LABELS = {
    litany: 'Litany (表層・出来事)',
    systemic_causes: 'Systemic Causes (システム的原因)',
    worldview: 'Worldview (世界観・イデオロギー)',
    myth_metaphor: 'Myth / Metaphor (神話・メタファー)',
    key_tension: 'Key Tension (主要な緊張)',
    emerging_narrative: 'Emerging Narrative (立ち現れる物語)'
  };
  var CLA_LAYER_ORDER = ['litany','systemic_causes','worldview','myth_metaphor','key_tension','emerging_narrative'];

  function buildCLAText(yearly, quarterly, meta) {
    var bar = new Array(71).join('=');
    var lines = [];
    var now = new Date();
    var jst = new Date(now.getTime() + (9*60 - now.getTimezoneOffset()) * 60000);
    var ts = jst.toISOString().slice(0,16).replace('T',' ') + ' JST';
    var coverage = (meta && meta.data_coverage) || {};

    lines.push(bar);
    lines.push('CLA (Causal Layered Analysis) 36\u5e74\u5206\u6790');
    lines.push('1990 - 2026');
    lines.push(bar);
    lines.push('');
    lines.push('\u751f\u6210\u65e5\u6642: ' + ts + '\uff08\u30d6\u30e9\u30a6\u30b6\u5185\u751f\u6210\uff09');
    lines.push('\u30c7\u30fc\u30bf\u30bd\u30fc\u30b9: miratuku-news / future-insight-app');
    lines.push('\u30ab\u30d0\u30ec\u30c3\u30b8: \u5e74\u6b21 ' + (coverage.yearly_periods || yearly.length) + '\u4ef6 + \u56db\u534a\u671f ' + (coverage.quarterly_periods || quarterly.length) + '\u4ef6 = \u5408\u8a08 ' + (coverage.total_periods || (yearly.length + quarterly.length)) + '\u671f\u9593');
    lines.push('\u5e74\u7bc4\u56f2: ' + (coverage.year_range || '1990-2026'));
    lines.push('');
    lines.push('\u3010CLA\uff08\u56e0\u679c\u968e\u5c64\u5206\u6790\uff09\u3068\u306f\u3011');
    lines.push('  Sohail Inayatullah \u304c\u63d0\u5531\u3057\u305f\u672a\u6765\u5b66\u306e\u5206\u6790\u624b\u6cd5\u3002\u793e\u4f1a\u73fe\u8c61\u30924\u5c64');
    lines.push('  \uff08Litany / Systemic Causes / Worldview / Myth & Metaphor\uff09\u306b');
    lines.push('  \u5206\u89e3\u3057\u3001\u8868\u5c64\u306e\u51fa\u6765\u4e8b\u3068\u6df1\u5c64\u306e\u795e\u8a71\u3092\u5bfe\u5fdc\u4ed8\u3051\u308b\u3053\u3068\u3067\u3001');
    lines.push('  \u4ee3\u66ff\u7684\u672a\u6765\u306e\u53ef\u80fd\u6027\u3092\u69cb\u9020\u7684\u306b\u63a2\u7d22\u3059\u308b\u3002');
    lines.push('');

    function formatMetaRegion(regionKey, regionData) {
      if (!regionData) return '';
      var out = [];
      out.push(bar);
      out.push('\u30e1\u30bf\u5206\u6790: ' + regionKey.toUpperCase() + ' \u2014 ' + (regionData.title || regionKey));
      out.push(bar);
      out.push('');
      if (regionData.report_text) {
        out.push(String(regionData.report_text).trim());
        out.push('');
      }
      var shifts = regionData.key_paradigm_shifts || [];
      if (shifts.length) {
        out.push(new Array(61).join('-'));
        out.push('\u4e3b\u8981\u30d1\u30e9\u30c0\u30a4\u30e0\u30b7\u30d5\u30c8');
        out.push(new Array(61).join('-'));
        shifts.forEach(function(s, i) {
          var desc = s.description || s.shift || '';
          out.push((i+1) + '. [' + (s.period || '') + '] ' + desc);
        });
        out.push('');
      }
      var myths = regionData.dominant_myths_timeline || [];
      if (myths.length) {
        out.push(new Array(61).join('-'));
        out.push('\u652f\u914d\u7684\u306a\u795e\u8a71\u30fb\u30e1\u30bf\u30d5\u30a1\u30fc\u306e\u5909\u9077');
        out.push(new Array(61).join('-'));
        myths.forEach(function(m) {
          out.push('  [' + (m.period || '') + '] ' + (m.myth || m.metaphor || ''));
        });
        out.push('');
      }
      return out.join('\n');
    }

    if (meta) {
      ['japan','global'].forEach(function(rk) {
        var block = formatMetaRegion(rk, meta[rk]);
        if (block) { lines.push(block); lines.push(''); }
      });
    }

    function indentText(text, indent) {
      return String(text || '').split('\n').map(function(l) { return l ? indent + l : ''; }).join('\n');
    }

    function formatEntry(entry) {
      var out = [];
      var divider = new Array(61).join('-');
      out.push(divider);
      if (entry.type === 'quarterly') out.push('\u25a0 ' + entry.period + '\uff08\u56db\u534a\u671f\uff09');
      else out.push('\u25a0 ' + entry.period + '\u5e74');
      out.push(divider);
      out.push('');
      var cats = entry.categories || {};
      CLA_CATEGORY_ORDER.forEach(function(catKey) {
        var cat = cats[catKey];
        if (!cat) return;
        out.push('\u3010' + CLA_CATEGORY_LABELS[catKey] + ' (' + catKey + ')\u3011');
        CLA_LAYER_ORDER.forEach(function(layerKey) {
          var val = cat[layerKey];
          if (!val) return;
          out.push('  \u25c6 ' + CLA_LAYER_LABELS[layerKey]);
          out.push(indentText(String(val).trim(), '    '));
          out.push('');
        });
        out.push('');
      });
      var syn = entry.cross_category_synthesis;
      if (syn) {
        out.push('\u3010\u5206\u91ce\u6a2a\u65ad\u306e\u7d71\u5408\u3011');
        if (typeof syn === 'object') {
          Object.entries(syn).forEach(function(kv) {
            out.push('  \u25c6 ' + kv[0]);
            out.push(indentText(String(kv[1] || '').trim(), '    '));
            out.push('');
          });
        } else {
          out.push(indentText(String(syn).trim(), '  '));
          out.push('');
        }
      }
      return out.join('\n');
    }

    var sortedYearly = yearly.slice().sort(function(a,b) { return String(a.period).localeCompare(String(b.period)); });
    var sortedQuarterly = quarterly.slice().sort(function(a,b) { return String(a.period).localeCompare(String(b.period)); });

    lines.push('');
    lines.push(bar);
    lines.push('\u7b2cI\u90e8: \u5e74\u6b21\u5206\u6790 (' + sortedYearly.length + '\u4ef6)');
    lines.push(bar);
    lines.push('');
    sortedYearly.forEach(function(e) { lines.push(formatEntry(e)); lines.push(''); });

    lines.push('');
    lines.push(bar);
    lines.push('\u7b2cII\u90e8: \u56db\u534a\u671f\u5206\u6790 (' + sortedQuarterly.length + '\u4ef6)');
    lines.push(bar);
    lines.push('');
    sortedQuarterly.forEach(function(e) { lines.push(formatEntry(e)); lines.push(''); });

    lines.push('');
    lines.push(bar);
    lines.push('(\u7d42\u308f\u308a)');
    lines.push(bar);
    return lines.join('\n');
  }

  function triggerDownload(content, filename, mime) {
    var blob = new Blob([content], { type: mime });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function() { URL.revokeObjectURL(url); }, 0);
  }

  window.downloadCLALiveText = function() {
    var yearly = window._claYearly || [];
    var quarterly = window._claQuarterly || [];
    var meta = window._claMeta || null;
    if (yearly.length === 0 && quarterly.length === 0) {
      alert('CLA\u30c7\u30fc\u30bf\u304c\u307e\u3060\u8aad\u307f\u8fbc\u307e\u308c\u3066\u3044\u307e\u305b\u3093\u3002\u3057\u3070\u3089\u304f\u5f85\u3063\u3066\u304b\u3089\u518d\u5ea6\u304a\u8a66\u3057\u304f\u3060\u3055\u3044\u3002');
      return;
    }
    var text = buildCLAText(yearly, quarterly, meta);
    var stamp = new Date().toISOString().slice(0,10);
    triggerDownload(text, 'cla_36years_analysis_' + stamp + '.txt', 'text/plain;charset=utf-8');
  };

  window.downloadCLALiveJSON = function() {
    var yearly = window._claYearly || [];
    var quarterly = window._claQuarterly || [];
    var meta = window._claMeta || null;
    if (yearly.length === 0 && quarterly.length === 0) {
      alert('CLA\u30c7\u30fc\u30bf\u304c\u307e\u3060\u8aad\u307f\u8fbc\u307e\u308c\u3066\u3044\u307e\u305b\u3093\u3002\u3057\u3070\u3089\u304f\u5f85\u3063\u3066\u304b\u3089\u518d\u5ea6\u304a\u8a66\u3057\u304f\u3060\u3055\u3044\u3002');
      return;
    }
    var bundle = {
      generated_at: new Date().toISOString(),
      source: 'miratuku-news / future-insight-app',
      coverage: (meta && meta.data_coverage) || { yearly_periods: yearly.length, quarterly_periods: quarterly.length, total_periods: yearly.length + quarterly.length, year_range: '1990-2026' },
      meta_report: meta,
      yearly: yearly,
      quarterly: quarterly
    };
    var stamp = new Date().toISOString().slice(0,10);
    triggerDownload(JSON.stringify(bundle, null, 2), 'cla_36years_analysis_' + stamp + '.json', 'application/json');
  };

  // ============================================================
  // UNIFIED CLA ARCHIVE VIEW
  // ============================================================
  var claArchiveCatFilter = 'Overall';
  var claArchiveViewMode = 'timeline';
  var claArchiveSelectedPeriod = null;

  window.setCLAArchiveFilter = function(cat) {
    claArchiveCatFilter = cat;
    renderCLAArchiveView();
  };

  window.setCLAArchiveViewMode = function(mode) {
    claArchiveViewMode = mode;
    renderCLAArchiveView();
  };

  window.selectCLAPeriod = function(period) {
    claArchiveSelectedPeriod = period;
    renderCLAArchiveView();
  };

  function renderCLAArchiveView() {
    var container = document.getElementById('claArchiveView');
    if (!container) return;

    var yearly = window._claYearly || [];
    var quarterly = window._claQuarterly || [];
    if (yearly.length === 0 && quarterly.length === 0) {
      container.innerHTML = '<p class="text-muted">\u30a2\u30fc\u30ab\u30a4\u30d6\u30c7\u30fc\u30bf\u304c\u307e\u3060\u8aad\u307f\u8fbc\u307e\u308c\u3066\u3044\u307e\u305b\u3093\u3002</p>';
      return;
    }

    var allEntries = yearly.concat(quarterly);

    var catOptions = [
      { key: 'Overall', label: '\u5168\u4f53', color: 'var(--accent)' },
      { key: 'Political', label: '\u653f\u6cbb', color: 'var(--P)' },
      { key: 'Economic', label: '\u7d4c\u6e08', color: 'var(--E)' },
      { key: 'Social', label: '\u793e\u4f1a', color: 'var(--S)' },
      { key: 'Technological', label: '\u6280\u8853', color: 'var(--T)' },
      { key: 'Legal', label: '\u6cd5\u5f8b', color: 'var(--L)' },
      { key: 'Environmental', label: '\u74b0\u5883', color: 'var(--En)' }
    ];

    var html = '';

    html += '<div class="cla-controls">';
    html += '<div class="cla-control-group"><span class="cla-filter-label">\u5206\u91ce</span>';
    catOptions.forEach(function(opt) {
      var isActive = claArchiveCatFilter === opt.key;
      html += '<button class="cla-filter-btn" onclick="setCLAArchiveFilter(\'' + opt.key + '\')" style="border:1px solid ' + (isActive ? opt.color : 'var(--border-light)') + ';background:' + (isActive ? opt.color : 'transparent') + ';color:' + (isActive ? '#fff' : 'var(--text-secondary)') + '">' + opt.label + '</button>';
    });
    html += '</div>';
    html += '<div class="cla-control-group"><span class="cla-filter-label">\u8868\u793a</span>';
    html += '<button class="cla-filter-btn" onclick="setCLAArchiveViewMode(\'timeline\')" style="border:1px solid ' + (claArchiveViewMode === 'timeline' ? 'var(--accent)' : 'var(--border-light)') + ';background:' + (claArchiveViewMode === 'timeline' ? 'var(--accent)' : 'transparent') + ';color:' + (claArchiveViewMode === 'timeline' ? '#fff' : 'var(--text-secondary)') + '">\u5909\u9077\u4e00\u89a7</button>';
    html += '<button class="cla-filter-btn" onclick="setCLAArchiveViewMode(\'single\')" style="border:1px solid ' + (claArchiveViewMode === 'single' ? 'var(--accent)' : 'var(--border-light)') + ';background:' + (claArchiveViewMode === 'single' ? 'var(--accent)' : 'transparent') + ';color:' + (claArchiveViewMode === 'single' ? '#fff' : 'var(--text-secondary)') + '">\u500b\u5225\u8868\u793a</button>';
    html += '</div></div>';

    if (claArchiveViewMode === 'timeline') {
      var layers = [
        { key: 'litany', label: 'Layer 1: \u30ea\u30bf\u30cb\u30fc\uff08\u8868\u5c64\uff09', border: 'var(--accent-warm)' },
        { key: 'systemic_causes', label: 'Layer 2: \u793e\u4f1a\u7684\u30fb\u30b7\u30b9\u30c6\u30e0\u7684\u539f\u56e0', border: 'var(--accent-soft)' },
        { key: 'worldview', label: 'Layer 3: \u4e16\u754c\u89b3\u30fb\u30c7\u30a3\u30b9\u30b3\u30fc\u30b9', border: 'var(--accent)' },
        { key: 'myth_metaphor', label: 'Layer 4: \u795e\u8a71\u30fb\u30e1\u30bf\u30d5\u30a1\u30fc', border: '#4A7A8C' },
        { key: 'key_tension', label: '\u6838\u5fc3\u7684\u7dca\u5f35', border: 'var(--highlight)' },
        { key: 'emerging_narrative', label: '\u65b0\u305f\u306a\u7269\u8a9e', border: 'var(--S)' }
      ];

      var activeEntries = allEntries.filter(function(entry) {
        return layers.some(function(l) { var t = getCLAEntryText(entry, l.key, claArchiveCatFilter); return t && t.trim(); });
      });

      html += '<div class="cla-sync-scroll" id="claSyncScroll">';

      html += '<div class="cla-sync-row cla-sync-header">';
      html += '<div class="cla-sync-label"></div>';
      activeEntries.forEach(function(entry, idx) {
        var isCurrent = idx === activeEntries.length - 1;
        html += '<div class="cla-sync-col-header' + (isCurrent ? ' current' : '') + '">' + escapeHtml(formatCLAPeriodLabel(entry)) + '</div>';
      });
      html += '</div>';

      layers.forEach(function(layer) {
        var hasData = activeEntries.some(function(e) { var t = getCLAEntryText(e, layer.key, claArchiveCatFilter); return t && t.trim(); });
        if (!hasData) return;

        html += '<div class="cla-sync-row">';
        html += '<div class="cla-sync-label"><span style="width:6px;height:6px;border-radius:50%;background:' + layer.border + ';flex-shrink:0"></span>' + layer.label + '</div>';
        activeEntries.forEach(function(entry, idx) {
          var text = getCLAEntryText(entry, layer.key, claArchiveCatFilter);
          var isCurrent = idx === activeEntries.length - 1;
          if (text && text.trim()) {
            html += '<div class="cla-sync-cell' + (isCurrent ? ' current' : '') + '">' + escapeHtml(text) + '</div>';
          } else {
            html += '<div class="cla-sync-cell empty">\u2014</div>';
          }
        });
        html += '</div>';
      });

      html += '</div>';

    } else {
      if (!claArchiveSelectedPeriod && allEntries.length > 0) {
        claArchiveSelectedPeriod = allEntries[allEntries.length - 1].period;
      }

      var decades = {};
      allEntries.forEach(function(entry) {
        var year = parseInt(entry.period);
        var decade = isNaN(year) ? '2020s' : (Math.floor(year / 10) * 10 + 's');
        if (!decades[decade]) decades[decade] = [];
        decades[decade].push(entry);
      });

      html += '<div style="margin-bottom:20px">';
      Object.entries(decades).forEach(function(kv) {
        var decade = kv[0], entries = kv[1];
        html += '<div class="cla-decade-group">';
        html += '<div class="cla-decade-group-title">' + decade + '</div>';
        html += '<div class="cla-decade-group-btns">';
        entries.forEach(function(entry) {
          var isActive = entry.period === claArchiveSelectedPeriod;
          var label = formatCLAPeriodLabel(entry);
          html += '<button class="cla-period-btn' + (isActive ? ' active' : '') + '" onclick="selectCLAPeriod(\'' + escapeAttr(entry.period) + '\')">' + escapeHtml(label) + '</button>';
        });
        html += '</div></div>';
      });
      html += '</div>';

      var selected = allEntries.find(function(e) { return e.period === claArchiveSelectedPeriod; });
      if (selected) {
        html += renderCLADetailPanel(selected, claArchiveCatFilter);
      } else {
        html += '<div class="cla-detail-panel"><div class="cla-detail-placeholder">\u5e74\u3092\u9078\u629e\u3057\u3066\u304f\u3060\u3055\u3044</div></div>';
      }
    }

    container.innerHTML = html;
  }

  function renderCLADetailPanel(entry, catFilter) {
    if (!entry || !entry.categories) return '<div class="cla-detail-panel"><p class="text-muted">\u30c7\u30fc\u30bf\u304c\u3042\u308a\u307e\u305b\u3093\u3002</p></div>';

    var html = '<div class="cla-detail-panel">';
    html += '<h4 class="fs-h3" style="font-weight:700;color:var(--accent);margin-bottom:16px">' + escapeHtml(formatCLAPeriodLabel(entry)) + '</h4>';

    if (catFilter === 'Overall') {
      Object.entries(entry.categories).forEach(function(kv) {
        var catKey = kv[0], catData = kv[1];
        var info = PESTLE_CATS[catKey] || { labelJa: catKey, color: 'var(--accent)' };
        html += '<div class="cla-detail-cat-block">' +
          '<div class="cla-detail-cat-label"><span class="cla-detail-cat-dot" style="background:' + info.color + '"></span>' + info.labelJa + '</div>';
        CLA_LAYERS.forEach(function(layer) {
          if (catData[layer.key]) {
            html += '<div class="cla-detail-layer cla-layer-' + layer.depth + '">' +
              '<div class="cla-detail-layer-label">' + layer.labelJa + '</div>' +
              '<div class="cla-detail-layer-text">' + escapeHtml(catData[layer.key]) + '</div></div>';
          }
        });
        html += '</div>';
      });
    } else {
      var catData = entry.categories[catFilter];
      if (catData) {
        var info = PESTLE_CATS[catFilter] || { labelJa: catFilter, color: 'var(--accent)' };
        html += '<div class="cla-detail-cat-block">' +
          '<div class="cla-detail-cat-label"><span class="cla-detail-cat-dot" style="background:' + info.color + '"></span>' + info.labelJa + '</div>';
        CLA_LAYERS.forEach(function(layer) {
          if (catData[layer.key]) {
            html += '<div class="cla-detail-layer cla-layer-' + layer.depth + '">' +
              '<div class="cla-detail-layer-label">' + layer.labelJa + '</div>' +
              '<div class="cla-detail-layer-text">' + escapeHtml(catData[layer.key]) + '</div></div>';
          }
        });
        html += '</div>';
      } else {
        html += '<p class="text-muted">\u3053\u306e\u5206\u91ce\u306e\u30c7\u30fc\u30bf\u304c\u3042\u308a\u307e\u305b\u3093\u3002</p>';
      }
    }

    if (entry.cross_category_synthesis) {
      html += '<div class="cla-cross-synthesis"><div class="cla-cross-synthesis-label">\u30ab\u30c6\u30b4\u30ea\u6a2a\u65ad\u7d71\u5408</div>' +
        '<div class="cla-cross-synthesis-text">' + escapeHtml(entry.cross_category_synthesis) + '</div></div>';
    }
    html += '</div>';
    return html;
  }

  function getCLAEntryText(entry, layerKey, catFilter) {
    if (!entry) return '';
    if (layerKey === 'key_tension' || layerKey === 'emerging_narrative') {
      if (entry[layerKey]) return entry[layerKey];
      if (!entry.categories) return '';
      if (catFilter === 'Overall') {
        var parts = [];
        Object.entries(entry.categories).forEach(function(kv) {
          if (kv[1][layerKey]) parts.push(kv[1][layerKey]);
        });
        return parts.join('\n\n');
      } else {
        var catData = entry.categories[catFilter];
        return catData ? (catData[layerKey] || '') : '';
      }
    }
    if (!entry.categories) return '';
    if (catFilter === 'Overall') {
      var parts2 = [];
      Object.entries(entry.categories).forEach(function(kv) {
        if (kv[1][layerKey]) parts2.push(kv[1][layerKey]);
      });
      return parts2.join('\n\n');
    } else {
      var catData2 = entry.categories[catFilter];
      return catData2 ? (catData2[layerKey] || '') : '';
    }
  }

  function formatCLAPeriodLabel(entry) {
    var p = entry.period;
    if (!p) return '';
    if (p.includes('Q')) return p.replace(/(\d{4})-?Q(\d)/, '$1\u5e74Q$2');
    if (p.includes('-')) {
      var parts = p.split('-');
      return parts[0] + '\u5e74' + parseInt(parts[1]) + '\u6708';
    }
    return p + '\u5e74';
  }

});
