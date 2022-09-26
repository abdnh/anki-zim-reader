function showTooltipForSelection() {
    const selection = window.getSelection();
    const range = selection.getRangeAt(0);
    const selectedText = range.toString().trim();
    if (!selectedText) return;
    const fragment = range.extractContents();

    const span = document.createElement("span");
    span.appendChild(fragment);
    range.insertNode(span);

    const tooltip = tippy(span, {
        placement: "bottom",
        allowHTML: true,
        theme: "light",
        interactive: true,
        trigger: '',
        animation: "scale-extreme",
        appendTo: document.body,
        // TODO: maybe make configurable and make sure to update the value set on the iframe to match
        maxWidth: 600,
        onHide() {
            span.insertAdjacentHTML('afterend', span.innerHTML);
            span.remove();
        },
    });
    tooltip.show();
    globalThis.tippyInstance = tooltip;
    pycmd(`zim_server:popup:${selectedText}`);
}
