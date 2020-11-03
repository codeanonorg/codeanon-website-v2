(function () {
    const blockRegex = /^(address|blockquote|body|center|dir|div|dl|fieldset|form|h[1-6]|hr|isindex|menu|noframes|noscript|ol|p|pre|table|ul|dd|dt|frameset|li|tbody|td|tfoot|th|thead|tr|html)$/i;

    /*
     * @param {Element} el
     * @returns {boolean}
     */
    function isBlockLevel(el) {
        return blockRegex.test(el.nodeName);
    }

    for (const /** @type {HTMLElement} */ el of document.querySelectorAll(".mathjax")) {
        let text = el.innerText;
        el.innerHTML = "";
        let display = isBlockLevel(el);
        console.log("Element display type", display);
        el.appendChild(MathJax.tex2svg(text, {display}));
    }
})()

