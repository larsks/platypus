# change the behavior of asserts

this is an experiment that uses an ansible strategy plugin to change
the behavior of the `assert` module.  When this strategy is active,
failed `assert` tasks will show up as `changed` rather than `failed`.

We could also achieve the above behavior by using a modified `assert`
module.  The original goal here was to act more like the `assert` was
wrapped in a block/rescue: mark the task as failed, but continue to
process tasks on the host.

Due to the design of the ansible strategy plugin mechanism, achieving
the original goal is tricky if not impossible.
