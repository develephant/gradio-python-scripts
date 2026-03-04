The hidden event system
Under the hood Gradio uses:

FastAPI + Starlette (ASGI) for the server
WebSockets to push updates to the frontend
A queue system (demo.queue()) for managing concurrent requests
The frontend is actually a Svelte app, not React — so the reactivity model on the JS side is Svelte's store system
So the "events" you're used to controlling are basically RPC calls from browser → Python function → browser update, all mediated by Gradio's queue.

Where you can get more control:
`gr.on()` — multi-trigger event listener (newer API)
`.then()` chaining — chain async steps after an event
`gr.State` — your reactive state primitive

Custom JS — js= param on events lets you inject client-side logic
demo.load() — fires on page load (closest to useEffect on mount)

## The Core Idea

```py
btn.click(fn=step1, inputs=[...], outputs=[...]).then(
    fn=step2, inputs=[...], outputs=[...]
).then(
    fn=step3, inputs=[...], outputs=[...]
)
```

Each `.then()` fires after the previous step completes — the UI updates between each step, which is the killer feature. The user sees progress in real-time.

## Practical Example: Multi-step feedback

```py
import gradio as gr
import time

def validate_input(text):
    time.sleep(1)  # simulate work
    if not text:
        return "❌ Input is empty!", gr.update(interactive=False)
    return "✅ Input looks good!", gr.update(interactive=True)

def process_data(text):
    time.sleep(2)  # simulate heavy processing
    return f"⚙️ Processing: {text.upper()}"

def finalize(result):
    time.sleep(1)
    return f"🎉 Done! Final result: {result}"

with gr.Blocks() as demo:
    inp = gr.Textbox(label="Input")
    status = gr.Textbox(label="Status", interactive=False)
    result = gr.Textbox(label="Result", interactive=False)
    final = gr.Textbox(label="Final", interactive=False)
    btn = gr.Button("Run", interactive=True)

    btn.click(
        fn=validate_input,
        inputs=[inp],
        outputs=[status, btn]       # updates status + disables button
    ).then(
        fn=process_data,
        inputs=[inp],               # can re-use original inputs!
        outputs=[result]            # updates result box
    ).then(
        fn=finalize,
        inputs=[result],            # uses output from previous step
        outputs=[final]
    )

demo.launch()
```

Key things to understand:

1. UI updates between steps

Unlike a single function that does everything internally, each `.then()` step pushes an update to the browser before the next step runs. This is the main reason to use it.

2. inputs can be anything on the page

You're not limited to passing outputs forward — you can reference any component. Though note: `inputs=[result]` reads the current value of that component at the time that step runs.

3. It's not true async

It's sequential. Step 2 won't start until Step 1 finishes.

4. Queue required for chaining to work properly

`demo.queue().launch()  # needed for .then() to behave correctly`


If you find yourself needing a signal library in Gradio, it's usually a sign that either:

`.then()` chaining solves it and you haven't reached for it yet

`gr.State` solves it and state isn't flowing right

The app has grown complex enough that Gradio is the wrong tool and you should be in FastAPI + React
