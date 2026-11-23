# JSON Trail

Pick a nested value out of a JSON file or inspect the available keys without opening an editor.

```sh
python3 json_trail.py catalog.json /items/0/title
python3 json_trail.py catalog.json /items/0 --keys
cat catalog.json | python3 json_trail.py - /items --compact
```

Requires Python 3.8+. An empty pointer returns the whole document. Array indices start at zero. Use `~1` for a slash and `~0` for a literal tilde inside a key. [MIT](LICENSE)
