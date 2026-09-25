
const btn=document.querySelector('[data-menu]');
const menu=document.querySelector('.mobile-menu');
const closeBtn=document.querySelector('[data-close]');
function openMenu(){menu?.classList.add('open');document.body.classList.add('menu-open')}
function closeMenu(){menu?.classList.remove('open');document.body.classList.remove('menu-open')}
btn?.addEventListener('click',openMenu);
closeBtn?.addEventListener('click',closeMenu);
menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible')}),{threshold:.12});
document.querySelectorAll('.fade').forEach(el=>io.observe(el));
document.querySelectorAll('[data-newsletter]').forEach(form=>form.addEventListener('submit',e=>{
  e.preventDefault();
  const button=form.querySelector('button');
  const old=button.textContent;
  button.textContent='Thank you';
  setTimeout(()=>button.textContent=old,2400);
  form.reset();
}));
