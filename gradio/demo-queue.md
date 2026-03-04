`demo.queue()` is worth understanding. Here's the short version:

What it does
It enables Gradio's request queue system — without it, only one request can be processed at a time and concurrent requests just error out.


```
demo.queue()        # enable the queue with defaults
demo.launch()       # always called after queue()
```

Why it matters for `.then()`

Without the queue, `.then()` chaining is unreliable because Gradio can't maintain the stateful connection between steps. The queue is what keeps that WebSocket alive between chained calls.

Key options worth knowing

```
demo.queue(
    max_size=20, # max requests waiting in queue (default unlimited)
    default_concurrency_limit=5,  # how many run simultaneously
)
```

The simple rule

Just always put it before `.launch():`


`demo.queue().launch()   # chained - most common pattern`

You rarely need to tweak the options unless you're:

Deploying for multiple users
Running heavy ML models and need to throttle
Hitting timeout issues


For a learning app — `demo.queue().launch()`
