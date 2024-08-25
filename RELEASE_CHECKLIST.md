# Release Checklist

1. Bump version in `src/main.py`.

2. Follow instructions in `README.md` to build locally.

3. Create `yoyoengine-hub-linux-amd64.tar.gz` by running the following command:

    ```bash
    tar -czf yoyoengine-hub-linux-amd64.tar.gz -C dist yoyoengine-hub
    ```

4. Create a tag on GitHub with the version number.

5. Upload the `yoyoengine-hub-linux-amd64.tar.gz` to the release.
