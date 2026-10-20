(function () {
    'use strict';
  
    window.dataLayer = window.dataLayer || [];
  
    var debug = false;
    try { debug = window.localStorage.getItem('tracking_debug') === '1'; } catch (e) {}
  
    function send(payload) {
      window.dataLayer.push(payload);
      if (debug) { console.log('[tracking]', JSON.stringify(payload)); }
    }
  
    function lastSegment(path) {
      var parts = path.split('/').filter(Boolean);
      return parts.length ? parts[parts.length - 1] : '';
    }
  
    function linkLocation(a) {
      if (a.matches('a.project-row-card')) { return 'landing_card'; }
      if (a.matches('a.project.card')) { return 'projects_index'; }
      if (a.closest('.landing-buttons')) { return 'landing_button'; }
      if (a.closest('.navbar')) { return 'navbar'; }
      if (a.closest('footer')) { return 'footer'; }
      return 'page_body';
    }
  
    function textOf(a, selector) {
      var el = a.querySelector(selector);
      return el ? el.textContent.replace(/\s+/g, ' ').trim() : '';
    }
  
    document.addEventListener('click', function (event) {
      if (!event.target || !event.target.closest) { return; }
      var a = event.target.closest('a[href]');
      if (!a) { return; }
      if (a.id === 'theme-toggle' || a.closest('#attribution')) { return; }
  
      var u;
      try { u = new URL(a.href, window.location.href); } catch (e) { return; }
  
      var loc = linkLocation(a);
      var host = u.hostname.toLowerCase();
      var ownHost = window.location.hostname.toLowerCase();
  
      if (host === ownHost && /\/resume\.pdf$/i.test(u.pathname)) {
        send({ event: 'resume_download', file_name: lastSegment(u.pathname), link_location: loc });
        return;
      }
  
      if (a.matches('a.project-row-card') ||
          (a.matches('a.project.card') && window.location.pathname.indexOf('/projects') === 0)) {
        send({
          event: 'project_click',
          project_name: textOf(a, '.project-row-title, .card-title'),
          project_slug: lastSegment(u.pathname),
          link_location: loc
        });
        return;
      }
  
      var contact = '';
      if (u.protocol === 'mailto:') { contact = 'email'; }
      else if (/(^|\.)linkedin\.com$/.test(host) && /^\/in\/vivek-dhanwada\/?$/i.test(u.pathname)) { contact = 'linkedin'; }
      else if (host === 'github.com' && /^\/vivekdhanwada\/?$/i.test(u.pathname)) { contact = 'github'; }
  
      if (contact) {
        send({ event: 'contact_click', contact_method: contact, link_location: loc });
        return;
      }
  
      if ((u.protocol === 'http:' || u.protocol === 'https:') && host !== ownHost) {
        send({ event: 'outbound_click', link_domain: host, link_url: u.origin + u.pathname, link_location: loc });
      }
    }, true);
  
    var thresholds = [25, 50, 75, 100];
    var fired = {};
    var ticking = false;
  
    function checkScroll() {
      ticking = false;
      var doc = document.documentElement;
      var max = doc.scrollHeight - window.innerHeight;
      if (max <= 0) { return; }
      var y = window.pageYOffset || doc.scrollTop;
      var pct = (max - y <= 2) ? 100 : (y / max) * 100;
      thresholds.forEach(function (t) {
        if (pct >= t && !fired[t]) {
          fired[t] = true;
          send({ event: 'scroll_depth', depth_percent: t });
        }
      });
    }
  
    window.addEventListener('scroll', function () {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(checkScroll);
      }
    }, { passive: true });
  })();