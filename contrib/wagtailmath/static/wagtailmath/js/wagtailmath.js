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

/** @typedef {{idForLabel: string, getValue(): string, getState(): unknown, setState(state: unknown): void, focus(soft: bool): void}} BoundWidget */

class MathJaxWidget {
    /**
     * @param {string} idForLabel
     * @param {string} initialValue
     */
    constructor(idForLabel, initialValue) {
        this.idForLabel = idForLabel;
        this.initialValue = initialValue;
    }

    /**
     * @param {HTMLElement} container
     * @param {string} name
     * @param {string} id
     * @param {unknown} initialState
     * @returns {BoundWidget}
     */
    render(container, name, id, initialState) {
        const inputEl = document.createElement("input");
        const displayEl = document.createElement("div");
        const update = () => displayEl.innerHTML = MathJax.tex2svg(inputEl.value).outerHTML;

        if(this.initialValue)
            inputEl.value = this.initialValue;
        inputEl.id = this.idForLabel;
        inputEl.name = name;
        displayEl.attributes.cols = "50";
        displayEl.attributes.rows = "10";
        displayEl.classList.add("richtext");
        displayEl.id = "mathjax-preview-"+id;

        update();

        inputEl.addEventListener("input", update);

        container.append(inputEl, displayEl);

        return {
            idForLabel: this.idForLabel,
            getValue() {
                return inputEl.value;
            },
            getState() {
                return initialState;
            },
            setState() {
            },
            focus() {
                inputEl.focus();
            }
        }
    }
}

window.telepath.register("contrib.wagtailmath.blocks.MathJaxWidget", MathJaxWidget);