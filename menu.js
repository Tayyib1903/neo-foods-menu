(() => {
 'use strict';
 const cfg=window.NEO_MENU,book=document.querySelector('.book'),status=document.querySelector('#status'),prev=document.querySelector('#prev'),next=document.querySelector('#next'),zoom=document.querySelector('.zoom'),zoomImg=zoom.querySelector('img'),text=document.querySelector('.text-menu');
 const mq=matchMedia('(max-width:800px)'),reduce=matchMedia('(prefers-reduced-motion:reduce)');
 let page=0,step=mq.matches?1:2,settle,drag=null,scale=1,zoomPage=0;
 if(cfg.pages.length===1){book.classList.add('single');document.querySelector('.viewer').classList.add('one-page')}
 const clamp=n=>Math.max(0,Math.min(cfg.pages.length-1,n));
 const requested=()=>{const n=Number(new URLSearchParams(location.hash.slice(1)).get('page'));return clamp(Number.isFinite(n)&&n>0?Math.floor(n)-1:0)};
 cfg.pages.forEach((p,i)=>{
  const sheet=document.createElement('article');sheet.className='sheet';sheet.setAttribute('aria-label',`${p.title}, Seite ${i+1}`);
  const img=new Image();img.src=p.image;img.alt=`${cfg.title}: ${p.title}, Seite ${i+1}. Vergrößerung und lesbare Textansicht unter der Karte.`;img.width=1414;img.height=2000;img.draggable=false;img.loading=i<2?'eager':'lazy';img.decoding='async';
  img.addEventListener('error',()=>sheet.classList.add('broken'));
  const note=document.createElement('p');note.className='loading-note';note.textContent='Die Seite konnte nicht geladen werden. Bitte nutze den PDF-Download oder die Textansicht.';
  sheet.append(img,note);sheet.addEventListener('dblclick',()=>openZoom(i));book.append(sheet);
 });
 function sync(){
  const start=Math.floor(page/step)*step,end=Math.min(start+step,cfg.pages.length);
  status.textContent=start+1===end?`Seite ${end} / ${cfg.pages.length}`:`Seiten ${start+1}–${end} / ${cfg.pages.length}`;
  prev.disabled=start===0;next.disabled=end>=cfg.pages.length;
  let active=cfg.categories[0];for(const cat of cfg.categories)if(cat.page<=page+1)active=cat;
  document.querySelectorAll('.categories a').forEach(a=>{if(a.dataset.page===String(active.page))a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
  const section=text.querySelector('pre');section.textContent=cfg.pages[page].text;
  text.querySelector('h2').textContent=cfg.pages[page].title;
 }
 function go(n,behavior='smooth',hash=true){
  page=clamp(n);const target=Math.floor(page/step)*step;
  book.scrollTo({left:target/step*book.clientWidth,behavior:reduce.matches?'auto':behavior});
  if(hash)history.replaceState(null,'',`#page=${page+1}`);
  sync();const sheet=book.children[target];sheet.classList.remove('turn');if(behavior==='smooth'&&!reduce.matches)requestAnimationFrame(()=>sheet.classList.add('turn'));
 }
 function shift(dir){go(Math.floor(page/step)*step+dir*step)}
 prev.onclick=()=>shift(-1);next.onclick=()=>shift(1);
 document.querySelectorAll('.categories a').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();go(Number(a.dataset.page)-1)}));
 book.addEventListener('scroll',()=>{clearTimeout(settle);settle=setTimeout(()=>{const p=clamp(Math.round(book.scrollLeft/book.clientWidth)*step);if(Math.floor(page/step)*step!==p){page=p;history.replaceState(null,'',`#page=${page+1}`);sync()}},140)},{passive:true});
 book.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse'||e.button!==0)return;drag={x:e.clientX,y:e.clientY,left:book.scrollLeft};book.setPointerCapture(e.pointerId);book.classList.add('dragging')});
 book.addEventListener('pointermove',e=>{if(drag)book.scrollLeft=drag.left+drag.x-e.clientX});
 function release(e){if(!drag)return;const dx=drag.x-e.clientX;book.classList.remove('dragging');drag=null;if(Math.abs(dx)>35)shift(dx>0?1:-1);else go(page,'auto',false)}
 book.addEventListener('pointerup',release);book.addEventListener('pointercancel',()=>{drag=null;book.classList.remove('dragging');go(page,'auto',false)});
 document.addEventListener('keydown',e=>{if(zoom.open||['INPUT','SELECT','TEXTAREA'].includes(e.target.tagName)||e.altKey||e.ctrlKey||e.metaKey)return;if(e.key==='ArrowRight'){e.preventDefault();shift(1)}if(e.key==='ArrowLeft'){e.preventDefault();shift(-1)}if(e.key==='Home'){e.preventDefault();go(0)}if(e.key==='End'){e.preventDefault();go(cfg.pages.length-1)}});
 window.addEventListener('hashchange',()=>go(requested(),'auto',false));
 let resizing;window.addEventListener('resize',()=>{clearTimeout(resizing);resizing=setTimeout(()=>{step=mq.matches?1:2;go(page,'auto',false)},100)});
 function setScale(s){scale=Math.max(1,Math.min(3,s));zoomImg.style.width=`${100*scale}%`;zoom.querySelector('#zoom-level').textContent=`${Math.round(scale*100)} %`;zoom.querySelector('#minus').disabled=scale===1;zoom.querySelector('#plus').disabled=scale===3}
 function openZoom(i=page){zoomPage=i;zoomImg.src=cfg.pages[i].image;zoomImg.alt=`${cfg.pages[i].title}, vergrößert`;setScale(1);zoom.showModal();document.body.style.overflow='hidden';zoom.querySelector('.zoom-scroll').scrollTo(0,0)}
 document.querySelector('#enlarge').onclick=()=>openZoom();zoom.querySelector('#plus').onclick=()=>setScale(scale+.5);zoom.querySelector('#minus').onclick=()=>setScale(scale-.5);zoom.querySelector('#close-zoom').onclick=()=>zoom.close();zoom.addEventListener('close',()=>{document.body.style.overflow='';document.querySelector('#enlarge').focus()});
 document.querySelector('#show-text').onclick=e=>{text.hidden=!text.hidden;e.currentTarget.setAttribute('aria-expanded',String(!text.hidden));if(!text.hidden)text.scrollIntoView({behavior:reduce.matches?'auto':'smooth'})};
 page=requested();go(page,'auto',false);
})();
