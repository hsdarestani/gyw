
const btn=document.querySelector('[data-menu]'),menu=document.querySelector('.mobile-menu'),closeBtn=document.querySelector('[data-close]');
function openMenu(){menu?.classList.add('open');document.body.classList.add('menu-open')}function closeMenu(){menu?.classList.remove('open');document.body.classList.remove('menu-open')}
btn?.addEventListener('click',openMenu);closeBtn?.addEventListener('click',closeMenu);menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible')}),{threshold:.1});document.querySelectorAll('.fade').forEach(el=>io.observe(el));
document.querySelectorAll('[data-newsletter]').forEach(form=>form.addEventListener('submit',e=>{e.preventDefault();const b=form.querySelector('button'),old=b.textContent;b.textContent='Thank you';setTimeout(()=>b.textContent=old,2400);form.reset()}));
const search=document.querySelector('[data-test-search]'),filter=document.querySelector('[data-test-filter]'),tests=[...document.querySelectorAll('[data-test]')];
function filterTests(){if(!tests.length)return;const q=(search?.value||'').toLowerCase(),c=filter?.value||'';tests.forEach(t=>{const okQ=t.textContent.toLowerCase().includes(q),okC=!c||t.dataset.category===c;t.classList.toggle('hide',!(okQ&&okC))})}
search?.addEventListener('input',filterTests);filter?.addEventListener('change',filterTests);
