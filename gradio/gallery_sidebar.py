# Gallery Sidebar
import gradio as gr

with gr.Sidebar("Output", open=False, width=320):
    gr.Markdown("## 🌌Generations"),

    with gr.Row():
        with gr.Column():
            @gr.render(triggers=[output_image.change], inputs=[output_image])
            def add_image_mini(output_image):
                gallery_list = []
                counter = 0
                for img in image_paths:
                    counter = counter + 1
                    gallery_list.append((img, str(f"i{counter}")))

                gr.Gallery(
                    gallery_list, 
                    show_label=False, 
                    container=True, 
                    min_width=256, 
                    object_fit='scale-down', 
                    buttons=['download', 'fullscreen'], 
                    sources=None, 
                    allow_preview=True,
                    height=520)
