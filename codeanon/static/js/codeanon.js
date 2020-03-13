document.addEventListener("DOMContentLoaded", () => {
  console.log("DOMContentLoaded");
  const burgers = [].slice.call(document.querySelectorAll(".navbar-burger"), 0);
  console.log(burgers);
  if (burgers.length > 0) {
    burgers.forEach(el => {
      el.addEventListener("click", () => {
        const target = document.getElementById(el.dataset.target);
        el.classList.toggle("is-active");
        target.classList.toggle("is-active");
      })
    })
  }
});
