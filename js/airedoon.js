import { ComfyWidgets } from "/scripts/widgets.js";
import { app } from "/scripts/app.js";


app.registerExtension({
    name: "Comfy.AIRedoon.Nodes",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name == "AIRedoonPreviewText") {
            const widgets_count = 1;

            function populate(text) {
                // 移除在初始状态上增加的widgets
                if (this.widgets) {
                    for (let i = widgets_count; i < this.widgets.length; i++) {
                        this.widgets[i].onRemove?.()
                    }
                    this.widgets.length = widgets_count;
                }
                
                const v = [...text];
                let msg = "";
                if (v.length == 1) {
                    msg = v[0];
                    
                    const w = ComfyWidgets["STRING"](this, "text", ["STRING", { multiline: true }], app).widget;
                    console.log("AIRedoon widget: ", w, msg)
                    // Insert element has a delay
                    setTimeout(() => {
                        w.inputEl.readOnly = true;
                        w.inputEl.style.opacity = 0.6;
                        w.value = msg;
                    }, 50);
                    
                    requestAnimationFrame(() => {
                        const sz = this.computeSize();
                        if (sz[0] < this.size[0]) {
                            sz[0] = this.size[0];
                        }
                        if (sz[1] < this.size[1]) {
                            sz[1] = this.size[1];
                        }
                        this.onResize?.(sz);
                        app.graph.setDirtyCanvas(true, false);
                    })
                }
            }

            // When the node is executed we will be sent the input text, display this in the widget
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function(message) {
                console.log("AIRedoon message: ", message)
                onExecuted?.apply(this, arguments);
                populate.call(this, message.text);
            }

            const onConfigure = nodeType.prototype.onConfigure;
            nodeType.prototype.onConfigure = function() {
                onConfigure?.apply(this, arguments);
                console.log("AIRedoon init values: ", this.widgets_values)
                if (this.widgets_values?.length) {
                    populate.call(this, this.widgets_values);
                }
            }
        }
    },
});