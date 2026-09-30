(() => {
  const viewer = document.createElement('dialog');
  viewer.className = 'image-viewer';
  viewer.setAttribute('aria-label', '이미지 확대 보기');
  viewer.innerHTML = '<button class="image-viewer-close" type="button" aria-label="이미지 닫기">닫기 ×</button><figure><img alt=""><figcaption></figcaption></figure>';
  document.body.append(viewer);
  const picture = viewer.querySelector('img');
  const caption = viewer.querySelector('figcaption');
  const closeButton = viewer.querySelector('button');
  let opener;

  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href]');
    if (!link || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const url = new URL(link.href);
    if (url.origin !== location.origin || !/\.(png|jpe?g|webp|gif|svg)$/i.test(url.pathname)) return;
    event.preventDefault();
    opener = link;
    picture.src = url.href;
    picture.alt = link.querySelector('img')?.alt || link.textContent.trim() || '확대 이미지';
    caption.textContent = picture.alt;
    viewer.showModal();
    document.documentElement.classList.add('image-viewer-open');
    closeButton.focus();
  });
  closeButton.addEventListener('click', () => viewer.close());
  viewer.addEventListener('click', (event) => {
    if (event.target === viewer) viewer.close();
  });
  viewer.addEventListener('close', () => {
    document.documentElement.classList.remove('image-viewer-open');
    picture.removeAttribute('src');
    opener?.focus({ preventScroll: true });
  });
})();
