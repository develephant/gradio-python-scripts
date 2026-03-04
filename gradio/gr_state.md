## gr.State

Outside a function = use `.value`

`some_val = gr.State("fun")`

`print(some_val)        # ❌ prints the component object, not "fun"`

`print(some_val.value)  # ✅ prints "fun"`

Inside an event handler function = Gradio passes the raw value

`some_val = gr.State("fun")`

```
def my_fn(state):        # Gradio unwraps it, you get "fun" directly
    print(state)         # ✅ "fun"
    print(state.value)   # ❌ AttributeError - it's already a string here
    return state

btn.click(my_fn, inputs=[some_val], outputs=[some_val])
```

The mental model

`gr.State` is a component wrapper around your value. Gradio unwraps it automatically when passing to/from functions, but outside of that context you're holding the wrapper, not the value.

Updating state inside a function

```
def my_fn(state):
    state["key"] = "new"   # mutating works for dicts/lists
    return state            # return it to persist the change
```

```
# OR replace it entirely
def my_fn(state):
    return "new value"      # just return the new value
```


The three gotchas worth burning into memory for Gradio:

`gr.State` — `.value` outside functions, raw value inside
`gr.update()` — meaningless without the outputs positional context
`.then()` — needs `demo.queue()` or it misbehaves

Those three alone probably cover 80% of the "why isn't this working" moments.
