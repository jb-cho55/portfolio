(() => {
  const viewer = document.createElement('dialog');
  viewer.className = 'image-viewer';
  viewer.setAttribute('aria-label', '이미지 확대 보기');
  viewer.innerHTML = '<div class="image-viewer-controls"><button class="image-viewer-zoom" type="button" aria-pressed="false">원본 크기 (100%)</button><button class="image-viewer-close" type="button" aria-label="이미지 닫기">닫기 ×</button></div><div class="image-viewer-stage"><figure><img alt=""><figcaption></figcaption></figure></div>';
  document.body.append(viewer);
  const picture = viewer.querySelector('img');
  const caption = viewer.querySelector('figcaption');
  const closeButton = viewer.querySelector('.image-viewer-close');
  const zoomButton = viewer.querySelector('.image-viewer-zoom');
  const stage = viewer.querySelector('.image-viewer-stage');
  let opener;

  const setZoom = (zoomed) => {
    viewer.classList.toggle('image-viewer-zoomed', zoomed);
    zoomButton.setAttribute('aria-pressed', String(zoomed));
    zoomButton.textContent = zoomed ? '화면에 맞추기' : '원본 크기 (100%)';
    stage.scrollTo(0, 0);
  };

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
    setZoom(false);
    viewer.showModal();
    document.documentElement.classList.add('image-viewer-open');
    closeButton.focus();
  });
  closeButton.addEventListener('click', () => viewer.close());
  zoomButton.addEventListener('click', () => setZoom(zoomButton.getAttribute('aria-pressed') !== 'true'));
  viewer.addEventListener('click', (event) => {
    if (event.target === viewer || event.target === stage) viewer.close();
  });
  viewer.addEventListener('close', () => {
    document.documentElement.classList.remove('image-viewer-open');
    picture.removeAttribute('src');
    opener?.focus({ preventScroll: true });
  });
})();
