/* The data payload is generated from public extracts; all geometry is editorial. */
(() => {
  'use strict';
  const model = window.CONSTELLATION;
  const svg = document.querySelector('#network');
  const selector = document.querySelector('#issue-select');
  const panel = document.querySelector('#context');
  const tip = document.querySelector('#tooltip');
  const byId = new Map(model.nodes.map(n => [n.node_id, n]));
  const nodeElements = new Map();
  const edgeElements = new Map();
  let selected = 'DQ-EXP-001';
  const ns = 'http://www.w3.org/2000/svg';
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function element(tag, attributes, parent) {
    const el = document.createElementNS(ns, tag);
    Object.entries(attributes).forEach(([k,v]) => el.setAttribute(k,v));
    parent.append(el); return el;
  }
  for (const e of model.edges) {
    const a = byId.get(e.from_node), b = byId.get(e.to_node);
    const path = element('path', {d:`M${a.x},${a.y} C${e.c1x},${e.c1y} ${e.c2x},${e.c2y} ${b.x},${b.y}`,
      class:`edge ${e.edge_kind === 'DECISION_ASSOCIATION' ? 'decision' : 'evidence'}`,
      'data-edge':e.edge_id, 'data-issue':e.issue_id, 'aria-hidden':'true'}, document.querySelector('#edges'));
    edgeElements.set(e.edge_id,path);
  }
  for (const n of model.nodes) {
    const group = element('g', {class:'node', 'data-node':n.node_id,'data-type':n.node_type,
      tabindex:'0', role:n.node_type === 'ISSUE' ? 'button' : 'img',
      'aria-label':`${n.node_type === 'ISSUE' ? n.node_id + ': ' : ''}${n.label}${n.node_type === 'ISSUE' ? '. Select investigation.' : '. Focus to reveal registered associations.'}`},document.querySelector('#nodes'));
    element('circle',{class:'hit',cx:n.x,cy:n.y,r:16},group);
    element('circle',{class:'halo',cx:n.x,cy:n.y,r:13},group);
    if (n.node_type === 'ISSUE') element('circle',{class:'glyph',cx:n.x,cy:n.y,r:5.5},group);
    else element('rect',{class:'glyph',x:n.x-4.5,y:n.y-4.5,width:9,height:9,rx:n.node_type === 'DECISION' ? 1 : 0,
      transform:`rotate(${n.node_type === 'SOURCE' ? 45 : 0} ${n.x} ${n.y})`},group);
    const label = element('text',{x:n.label_x,y:n.label_y,'text-anchor':n.label_align === 'right' ? 'end' : 'start'},group);
    if (n.node_type === 'DECISION') {
      const parts = n.short_label.split(' ');
      element('tspan',{x:n.label_x,dy:'-3'},label).textContent = parts[0];
      element('tspan',{x:n.label_x,dy:'13'},label).textContent = parts.slice(1).join(' ');
    } else label.textContent = n.short_label;
    group.addEventListener('click',() => { if(n.node_type === 'ISSUE') select(n.issue_id); });
    group.addEventListener('keydown',event => {
      if(n.node_type === 'ISSUE' && ['Enter',' '].includes(event.key)){event.preventDefault(); select(n.issue_id);}
      if(event.key === 'Escape') hideTip();
    });
    group.addEventListener('mouseenter',() => showTip(n,group));
    group.addEventListener('mouseleave',hideTip);
    group.addEventListener('focus',() => showTip(n,group));
    group.addEventListener('blur',hideTip);
    nodeElements.set(n.node_id,group);
  }
  const all = new Option('All registered associations','__ALL__'); selector.add(all);
  for(const row of model.issue_context) selector.add(new Option(`${row.issue_id} · ${byId.get(row.issue_id).short_label}`,row.issue_id));
  selector.addEventListener('change',() => select(selector.value));
  document.querySelector('#reset').addEventListener('click',() => select('__ALL__'));
  function showTip(n, group) {
    const edges = model.edges.filter(e => e.from_node === n.node_id || e.to_node === n.node_id);
    for(const edge of edges) edgeElements.get(edge.edge_id).classList.add('hovered');
    const detail = n.node_type === 'SOURCE' ? `${edges.length} registered issue association${edges.length === 1 ? '' : 's'}.` :
      n.node_type === 'DECISION' ? `${edges.length} issue${edges.length === 1 ? '' : 's'} in this AI-proposed decision category.` : 'Select to inspect evidence and competing explanations.';
    tip.innerHTML = `<small>${escape(n.node_type)}${n.issue_id ? ' / '+escape(n.issue_id) : ''}</small>${escape(n.label)}<p>${escape(detail)}</p>`;
    tip.hidden = false;
    const box = group.getBoundingClientRect(), wrap = document.querySelector('.chart-wrap').getBoundingClientRect();
    tip.style.left = Math.max(8, Math.min(box.left-wrap.left+10, wrap.width-tip.offsetWidth-12))+'px';
    tip.style.top = Math.max(8, Math.min(box.top-wrap.top+24,wrap.height-tip.offsetHeight-12))+'px';
  }
  function hideTip(){tip.hidden=true;for(const el of edgeElements.values()) el.classList.remove('hovered');}
  function select(issue) {
    selected = issue; selector.value = issue; panel.dataset.issue = issue; hideTip();
    const activeEdges = model.edges.filter(e => e.issue_id === selected || selected === '__ALL__');
    const activeNodes = new Set(activeEdges.flatMap(e => [e.from_node,e.to_node]));
    for(const e of model.edges) edgeElements.get(e.edge_id).classList.toggle('active',e.issue_id === selected || selected === '__ALL__');
    for(const [id,el] of nodeElements){
      el.classList.toggle('active',activeNodes.has(id)); el.classList.toggle('chosen',id === selected);
      if(byId.get(id).node_type === 'ISSUE') el.setAttribute('aria-pressed',String(id === selected));
    }
    if(selected === '__ALL__') {
      panel.innerHTML = '<div class="empty-state"><p class="eyebrow">THE FULL REGISTER</p><h3>Every question has<br>an evidence trail.</h3><p>Select a circular question in the constellation, or choose one above, to see its sources, competing explanations and next evidence request.</p><p>33 source–issue connections represent 35 lineage records. Two pairs each hold two roles.</p><p>Amber connections are issue-to-category associations from AI-proposed decision framing. All human reviews remain pending.</p></div>';
      return;
    }
    const row = model.issue_context.find(r => r.issue_id === selected);
    const evidence = activeEdges.filter(e => e.edge_kind === 'EVIDENCE_ASSOCIATION');
    const metrics = model.issue_metrics.filter(r => r.issue_id === selected);
    panel.innerHTML = `<div class="issue-meta"><span>${escape(selected)}</span><span class="pending">REVIEW PENDING</span></div>
      <h3 class="issue-title">${escape(row.title)}</h3>
      <section class="context-section"><h4>THE BUSINESS DECISION</h4><p>${escape(row.business_decision)}</p></section>
      <section class="context-section"><h4>COMPETING EXPLANATIONS</h4><ul class="explanations">${row.competing_explanations.split('|').map(s => `<li>${escape(s.trim())}</li>`).join('')}</ul></section>
      <section class="next-ask"><h4>THE NEXT PIECE OF EVIDENCE</h4><p>${escape(row.next_evidence_request)}</p></section>
      <p class="review-note"><b>AI-proposed framing.</b> Requires human review.<br>Source semantics remain unresolved.</p>
      <p class="evidence-summary">${row.source_count} sources · ${row.lineage_record_count} lineage records</p>
      <details class="context-details"><summary>Inspect the evidence trail</summary><ul class="ledger">${evidence.map(e => `<li><b>${escape(e.source_id)}</b><span>${escape(e.roles.split('|').join(' + '))}</span></li>`).join('')}</ul><p>Roles describe the registered relationship. A contributing population is not an affected population.</p><a href="../../../${escape(row.evidence_ref.split('#')[0])}">Issue registry ↗</a></details>
      <details class="context-details"><summary>What remains uncertain</summary><p>${escape(row.claim_limit)}</p><p>${escape(row.recommendation)}</p><p>Decision category: ${escape(row.decision_category)}<br>Evidence class: ${escape(row.evidence_class)}</p></details>
      ${metrics.length ? `<details class="context-details"><summary>Source metrics · ${metrics.length} separate measure${metrics.length > 1 ? 's' : ''}</summary>${metrics.map(m => `<div class="metric"><b>${escape(m.metric_key)}: ${escape(m.affected_count || 'Unknown')} ${escape(m.unit)}</b>Population: ${escape(m.population)}<br>Denominator: ${escape(m.denominator || 'Unknown')} · ${escape(m.denominator_definition)}<br>Calculation: ${escape(m.calculation)}<br>${escape(m.additivity)}; cross-issue sum: ${escape(m.cross_issue_sum_allowed)}</div>`).join('')}</details>` : ''}`;
  }
  select(selected);
})();
