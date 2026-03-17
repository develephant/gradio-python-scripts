# Gradio Cheat Sheet
## `gr.State`, `gr.update`, and `lambda` — ELI5

---

## `gr.State` — A Memory Box

Think of `gr.State` as a **sticky note** that Gradio holds onto for each user session.
Normal Python variables reset or get shared between users. `gr.State` keeps a **per-user, persistent value** that survives across events.

```python
generation_step = gr.State(0)   # starts at 0 for every user
output_history  = gr.State([])  # each user has their own list
```

To **read** it, put it in `inputs`. To **write** it, put it in `outputs` and return a new value from your function.

```python
.then(
    fn=lambda step: step + 1,   # reads step from inputs...
    inputs=generation_step,     # ...comes from here
    outputs=generation_step     # ...and the return value is written back here
)
```

> **Rule:** Plain Python variables can't be used as Gradio inputs/outputs. Always use `gr.State` when you need to track a value across events.

---

## `gr.update` — A Targeted Property Change

Every Gradio component has a **primary value** (e.g. the text in a Textbox, the number in a Slider) and **other properties** (e.g. `active`, `visible`, `interactive`).

When your function returns a **plain value**, Gradio sets the component's primary `value`:

```python
fn=lambda: 0,        outputs=generation_step   # sets State value → 0
fn=lambda: "Ready",  outputs=state_status       # sets Textbox value → "Ready"
```

When you need to change a **different property**, use `gr.update()`:

```python
fn=lambda: gr.update(active=False),  outputs=timer   # sets timer.active → False
                                                      # timer.value (interval) unchanged ✅
```

Without `gr.update`, a plain `False` would try to set the *interval* to `False` — wrong property, wrong result.

```python
fn=lambda: False,  outputs=timer   # ❌ tries to set interval = False — not what you want!
```

`gr.update` is **partial** — only the properties you name are changed, everything else stays as-is.

```python
gr.update(active=True)              # only toggles active
gr.update(active=True, value=1.0)   # changes two properties at once
```

---

## `lambda` — A Throwaway Function

A `lambda` is just a **function without a name**, used when the logic is too small to deserve a `def`.

```python
# These are identical:
def set_zero():
    return 0

lambda: 0
```

The expression after `:` is **always implicitly returned** — no `return` keyword needed.

```python
lambda: 0                          # returns 0
lambda: gr.update(active=False)    # returns a gr.update object
lambda step: step + 1              # takes one argument, returns it plus 1
lambda step, gens: step < gens     # takes two arguments, returns True or False
```

Arguments come from `inputs`, the return value goes to `outputs`:

```python
.then(
    fn=lambda step, gens: gr.update(active=step < gens),
    inputs=[generation_step, generations],   # → step, gens arguments
    outputs=timer                            # ← return value applied here
)
```

> **Limit:** Lambdas can only hold a **single expression**. No multi-line logic, no loops, no assignments. When you need more than one line, use a named `def` instead.

---

## Quick Reference

| Situation | What to use |
|---|---|
| Store a value across events | `gr.State(initial_value)` |
| Set a component's main value | Return a plain value from `fn` |
| Set any other component property | Return `gr.update(property=value)` |
| Simple one-liner function | `lambda` |
| Multi-line or complex logic | `def my_function():` |
