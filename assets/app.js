const btn=document.querySelector('[data-menu]'),menu=document.querySelector('.mobile-menu'),closeBtn=document.querySelector('[data-close]');
function openMenu(){menu?.classList.add('open');document.body.classList.add('menu-open')}
function closeMenu(){menu?.classList.remove('open');document.body.classList.remove('menu-open')}
btn?.addEventListener('click',openMenu);closeBtn?.addEventListener('click',closeMenu);menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible')}),{threshold:.1});document.querySelectorAll('.fade').forEach(el=>io.observe(el));
document.querySelectorAll('[data-newsletter]').forEach(form=>form.addEventListener('submit',e=>{e.preventDefault();const b=form.querySelector('button'),old=b.textContent;b.textContent='Thank you';setTimeout(()=>b.textContent=old,2200);form.reset()}));
const search=document.querySelector('#testSearch'),category=document.querySelector('#testCategory'),cards=[...document.querySelectorAll('.test-card')];
function filterTests(){if(!cards.length)return;const q=(search?.value||'').toLowerCase().trim(),c=(category?.value||'').toLowerCase();cards.forEach(card=>{const okQ=!q||card.dataset.name.includes(q)||card.dataset.category.includes(q),okC=!c||card.dataset.category===c;card.style.display=okQ&&okC?'':'none'})}
search?.addEventListener('input',filterTests);category?.addEventListener('change',filterTests);