//function lazy() {
let imageObserver = new IntersectionObserver((entries, imgObserver) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            const lazyImage = entry.target;
            lazyImage.src = lazyImage.dataset.src;
            imgObserver.unobserve(lazyImage);
        }
    })
});
    // const arr = document.querySelectorAll('img.cover_track');
    // arr.forEach((v) => {imageObserver.observe(v);});
//}


