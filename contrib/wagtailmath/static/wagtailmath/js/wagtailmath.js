class Preview {
    /**
     * @param {HTMLElement} previewEl
     * @param {HTMLTextAreaElement} inputEl
     */
    constructor(previewEl, inputEl) {
        this.previewEl = previewEl;
        this.inputEl = inputEl;
        /** @type {number|undefined} */
        this.timeout = undefined;
    }

    update() {
        if (this.timeout) {
            clearTimeout(this.timeout);
        }
        this.timeout = setTimeout(() => {
            this.previewEl.innerHTML = MathJax.tex2svg(this.inputEl.value, {display: true}).outerHTML;
        }, 150);
    }
}
