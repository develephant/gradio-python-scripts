`gr.update()`

It's basically a partial component update — lets you change specific properties of a component without rebuilding it. Think of it like setState for a single component's props.


# Instead of returning a new value, you return instructions to update the component

`gr.update(value="new text", visible=True, interactive=False)`

The problem it solves

A function's outputs map 1:1 to return values. But what if you want to update a component's visibility or interactivity without changing its value? Or skip updating it entirely?


# WITHOUT gr.update() - you're forced to return a value
```
def my_fn():
    return "some value"   # replaces content, no control over other props
```    

# WITH gr.update() - you control exactly what changes

```
def my_fn():
    return gr.update(visible=False)        # hide it, don't touch the value
    return gr.update(interactive=False)    # disable it, keep current value
    return gr.update(value="hi", label="New Label")  # change multiple props
```

Common patterns

Disable button while processing, re-enable after:

```
def start():
    return gr.update(interactive=False, value="Running...")

def finish():
    return gr.update(interactive=True, value="Run")

btn.click(start, outputs=[btn]).then(do_work, ...).then(finish, outputs=[btn])
```

Show/hide components dynamically:

```
def toggle_panel(show):
    return gr.update(visible=show)

checkbox.change(toggle_panel, inputs=[checkbox], outputs=[panel])
```

Update choices in a dropdown:

```
def refresh_options():
    new_options = fetch_from_api()   # your async HTTP call
    return gr.update(choices=new_options, value=None)
```

`btn.click(refresh_options, outputs=[dropdown])`

One gotcha

If you have multiple outputs and only want to update some of them, return `gr.update()` with no args for the ones you want to skip:

```
def my_fn():
    return gr.update(value="updated"), gr.update()  # update first, skip second
```

So in your case, the async HTTP calls feeding into a dropdown refresh or similar — that's a perfect combo of `async def + gr.update(choices=...)`.


The context is determined by where you put it in the outputs list. Gradio maps return values positionally to outputs:

```
btn.click(
    fn=my_fn,
    inputs=[...],
    outputs=[textbox, dropdown, btn]  # position 0, 1, 2
)

def my_fn():
    return (
        gr.update(value="hello"),           # → textbox (pos 0)
        gr.update(choices=["a", "b"]),      # → dropdown (pos 1)  
        gr.update(interactive=False)        # → btn (pos 2)
    )
```

Gradio knows which component each `gr.update()` targets purely by position — the update object itself has no idea what component it is, it's just a bag of props. Gradio applies them to the matching output component.
