let imageObserver = new IntersectionObserver(
    (entries, imgObserver) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            const lazyImage = entry.target;
            lazyImage.src = lazyImage.dataset.src;
            imgObserver.unobserve(lazyImage);
        }
    })
});


