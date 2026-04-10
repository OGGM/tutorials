# OGGM tutorials

Tutorial notebooks for the [OGGM](https://oggm.org) model, powered by [hub.oggm.org](https://hub.oggm.org).

Web: https://tutorials.oggm.org

License: [BSD-3-Clause](https://github.com/OGGM/tutorials/blob/master/LICENSE.txt)

![img](https://docs.oggm.org/en/stable/_static/logo.png)

## Contributing

Before opening a PR, strip notebook outputs and kernelspec metadata:

```bash
python3 scripts/strip_notebook_outputs.py
```

Maintainers can request a docs link check in two ways:

- In GitHub, open the Actions tab, select `Linkcheck On Request`, and use `Run workflow`.
- On a PR targeting `master`, `stable`, or `v1.5.3`, add the label `run-linkcheck` to trigger the same workflow for that PR head.
- On a PR, add a comment containing exactly `/linkcheck` to trigger the same workflow for that PR head.
