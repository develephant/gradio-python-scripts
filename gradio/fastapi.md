The catch with Gradio's API as "webhooks":

Gradio's API endpoints are designed to be called and return a result to the caller. They don't have great primitives for "fire and forget, update UI state." You'd need to expose a function that accepts the push payload and updates a gr.State, which works — but Gradio's streaming/SSE model means the UI only updates if a user has an active session connected. There's no persistent background state that auto-refreshes all viewers.

What actually works well:

A thin FastAPI endpoint mounted alongside Gradio (Gradio supports app.mount() or you can add routes to the underlying FastAPI app) would be a cleaner webhook target. It's essentially the same machine, same process, and you can update shared state that Gradio polls or streams from.

Bottom line: Fun and functional, yes — but Gradio's API endpoints are a slightly awkward fit for true webhooks. A hybrid (ComfyUI node → lightweight POST endpoint on the Gradio server → updates state the UI reads) is probably the cleanest path and still fits your "single machine" setup nicely.

 Add routes to Gradio's underlying FastAPI app (simpler, less boilerplate):

```
gradio_app = gr.Blocks(...) as app

# After defining the Blocks app, access the underlying FastAPI instance
@app.app.post("/webhook/progress")  # app.app is the FastAPI instance
async def comfy_webhook(payload: dict):
    ...

app.queue().launch(...)
```

Given your current app.py is already compact and Gradio-first, Option B is the path of least resistance — you just add routes directly to the underlying FastAPI app with app.app and you don't have to restructure anything.

The Gradio docs page you're thinking of is likely the one titled "Sharing Your App" or "Custom FastAPI Routes" — it covers gr.mount_gradio_app for Option A. But app.app for Option B is equally valid and barely documented, just a known pattern.


Yeah it's one of those things that's barely mentioned but super useful. The app.app accessor just exposes the underlying FastAPI instance that Gradio already created, so you get full FastAPI route capabilities with zero restructuring.

For your ComfyUI node side, it would just be a simple HTTP POST — something like requests.post("http://localhost:7860/webhook/progress", json={...}) — which is trivial to do from a custom node. You could push things like current step, preview images (as base64 or a filepath), or a completion signal.

The main thing to think through is how the webhook handler updates Gradio's UI state, since that's the tricky part of the push model I mentioned earlier. Worth exploring gr.State + some kind of polling component, or Gradio's newer streaming primitives, when you get to that point
